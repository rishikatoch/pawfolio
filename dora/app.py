import os
import statistics
import time
from datetime import datetime

import requests
from flask import Flask, Response
from prometheus_client import CollectorRegistry, Gauge, generate_latest

app = Flask(__name__)

GITHUB_REPO = os.getenv("GITHUB_REPO", "rishikatoch/pawfolio")
WORKFLOW_NAME = os.getenv("GITHUB_WORKFLOW", "Deploy to Production")
LOOKBACK_RUNS = int(os.getenv("DORA_LOOKBACK_RUNS", "50"))
CACHE_SECONDS = int(os.getenv("DORA_CACHE_SECONDS", "300"))

cache = {
    "timestamp": 0,
    "metrics": {},
}


def github_get(url, params=None):
    response = requests.get(
        url,
        params=params,
        headers={"Accept": "application/vnd.github+json"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def parse_time(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def get_workflow_runs():
    data = github_get(
        f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows",
    )

    workflow = next(
        (
            item
            for item in data.get("workflows", [])
            if item.get("name") == WORKFLOW_NAME
        ),
        None,
    )

    if not workflow:
        raise RuntimeError(f"Workflow not found: {WORKFLOW_NAME}")

    runs = github_get(
        f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/"
        f"{workflow['id']}/runs",
        params={"per_page": LOOKBACK_RUNS},
    )

    return runs.get("workflow_runs", [])


def get_commit_timestamps():
    commits = github_get(
        f"https://api.github.com/repos/{GITHUB_REPO}/commits",
        params={"per_page": 100},
    )

    timestamps = {}

    for commit in commits:
        sha = commit.get("sha")
        timestamp = (
            commit.get("commit", {})
            .get("author", {})
            .get("date")
        )

        if sha and timestamp:
            timestamps[sha] = parse_time(timestamp)

    return timestamps


def calculate_metrics(runs):
    completed = [
        run
        for run in runs
        if run.get("status") == "completed"
        and run.get("conclusion") in {"success", "failure"}
        and run.get("run_started_at")
        and run.get("updated_at")
    ]

    successful = [
        run for run in completed if run.get("conclusion") == "success"
    ]

    failed = [
        run for run in completed if run.get("conclusion") == "failure"
    ]

    # Deployment frequency: successful production deployments per day.
    deployment_frequency = len(successful) / 30.0

    lead_times_hours = []
    commit_timestamps = get_commit_timestamps()

    for run in successful:
        commit_time = commit_timestamps.get(run["head_sha"])

        if not commit_time:
            continue

        deploy_time = parse_time(run["updated_at"])
        lead_time = (
            deploy_time - commit_time
        ).total_seconds() / 3600

        if lead_time >= 0:
            lead_times_hours.append(lead_time)

    lead_time_hours = (
        statistics.median(lead_times_hours)
        if lead_times_hours
        else 0
    )

    total_attempts = len(completed)

    change_failure_rate = (
        (len(failed) / total_attempts) * 100
        if total_attempts
        else 0
    )

    recovery_hours = []

    ordered = sorted(
        completed,
        key=lambda run: parse_time(run["updated_at"]),
    )

    for index, run in enumerate(ordered):
        if run.get("conclusion") != "failure":
            continue

        failure_time = parse_time(run["updated_at"])

        for recovery in ordered[index + 1:]:
            if recovery.get("conclusion") == "success":
                recovery_time = parse_time(recovery["updated_at"])
                recovery_hours.append(
                    (recovery_time - failure_time).total_seconds() / 3600
                )
                break

    mttr_hours = (
        statistics.median(recovery_hours)
        if recovery_hours
        else 0
    )

    return {
        "deployment_frequency_per_day": deployment_frequency,
        "lead_time_hours": lead_time_hours,
        "change_failure_rate_percent": change_failure_rate,
        "mttr_hours": mttr_hours,
        "successful_deployments": len(successful),
        "failed_deployments": len(failed),
        "total_deployments": total_attempts,
    }


def get_metrics():
    now = time.time()

    if now - cache["timestamp"] < CACHE_SECONDS:
        return cache["metrics"]

    runs = get_workflow_runs()
    metrics = calculate_metrics(runs)

    cache["timestamp"] = now
    cache["metrics"] = metrics

    return metrics


@app.route("/metrics")
def metrics():
    registry = CollectorRegistry()
    values = get_metrics()

    definitions = {
        "pawfolio_deployment_frequency_per_day": (
            "Successful production deployments per day."
        ),
        "pawfolio_lead_time_hours": (
            "Median lead time from commit to production deployment."
        ),
        "pawfolio_change_failure_rate_percent": (
            "Percentage of failed production deployment attempts."
        ),
        "pawfolio_mttr_hours": (
            "Median recovery time from failed deployment to next successful deployment."
        ),
        "pawfolio_successful_deployments_total": (
            "Successful production deployments in the lookback window."
        ),
        "pawfolio_failed_deployments_total": (
            "Failed production deployments in the lookback window."
        ),
        "pawfolio_deployment_attempts_total": (
            "Production deployment attempts in the lookback window."
        ),
    }

    mapping = {
        "pawfolio_deployment_frequency_per_day":
            "deployment_frequency_per_day",
        "pawfolio_lead_time_hours":
            "lead_time_hours",
        "pawfolio_change_failure_rate_percent":
            "change_failure_rate_percent",
        "pawfolio_mttr_hours":
            "mttr_hours",
        "pawfolio_successful_deployments_total":
            "successful_deployments",
        "pawfolio_failed_deployments_total":
            "failed_deployments",
        "pawfolio_deployment_attempts_total":
            "total_deployments",
    }

    for metric_name, description in definitions.items():
        gauge = Gauge(
            metric_name,
            description,
            registry=registry,
        )
        gauge.set(values[mapping[metric_name]])

    return Response(
        generate_latest(registry),
        mimetype="text/plain",
    )


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
