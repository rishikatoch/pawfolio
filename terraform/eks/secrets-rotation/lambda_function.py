import json
import secrets

import boto3

secretsmanager = boto3.client("secretsmanager")


def lambda_handler(event, context):
    secret_id = event["SecretId"]
    token = event["ClientRequestToken"]
    step = event["Step"]

    metadata = secretsmanager.describe_secret(SecretId=secret_id)

    if token not in metadata["VersionIdsToStages"]:
        raise ValueError("Secret version is not associated with this rotation token.")

    if "AWSCURRENT" in metadata["VersionIdsToStages"][token]:
        return

    if "AWSPENDING" not in metadata["VersionIdsToStages"][token]:
        raise ValueError("Secret version is not staged as AWSPENDING.")

    if step == "createSecret":
        create_secret(secret_id, token)

    elif step == "setSecret":
        set_secret(secret_id, token)

    elif step == "testSecret":
        test_secret(secret_id, token)

    elif step == "finishSecret":
        finish_secret(secret_id, token)

    else:
        raise ValueError(f"Unsupported rotation step: {step}")


def create_secret(secret_id, token):
    try:
        secretsmanager.get_secret_value(
            SecretId=secret_id,
            VersionId=token,
            VersionStage="AWSPENDING",
        )
        return
    except secretsmanager.exceptions.ResourceNotFoundException:
        pass

    current = get_secret(secret_id, "AWSCURRENT")

    current["SECRET_KEY"] = secrets.token_urlsafe(64)

    secretsmanager.put_secret_value(
        SecretId=secret_id,
        ClientRequestToken=token,
        SecretString=json.dumps(current),
        VersionStages=["AWSPENDING"],
    )


def set_secret(secret_id, token):
    # SECRET_KEY is consumed by the application.
    # No external database credential needs to be changed.
    get_secret(secret_id, "AWSPENDING", token)


def test_secret(secret_id, token):
    pending = get_secret(secret_id, "AWSPENDING", token)

    if not pending.get("SECRET_KEY"):
        raise ValueError("Rotated SECRET_KEY is missing.")

    if len(pending["SECRET_KEY"]) < 32:
        raise ValueError("Rotated SECRET_KEY is unexpectedly short.")


def finish_secret(secret_id, token):
    metadata = secretsmanager.describe_secret(SecretId=secret_id)

    current_version = None

    for version_id, stages in metadata["VersionIdsToStages"].items():
        if "AWSCURRENT" in stages:
            current_version = version_id
            break

    if current_version == token:
        return

    secretsmanager.update_secret_version_stage(
        SecretId=secret_id,
        VersionStage="AWSCURRENT",
        MoveToVersionId=token,
        RemoveFromVersionId=current_version,
    )


def get_secret(secret_id, stage, version_id=None):
    kwargs = {
        "SecretId": secret_id,
        "VersionStage": stage,
    }

    if version_id:
        kwargs["VersionId"] = version_id

    response = secretsmanager.get_secret_value(**kwargs)

    return json.loads(response["SecretString"])
