FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt constraints.txt .

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip setuptools && \
    pip install --no-cache-dir -c constraints.txt -r requirements.txt

COPY . .

# Create a non-root application user matching
# the Kubernetes securityContext UID/GID.
RUN groupadd --gid 10001 appgroup && \
    useradd --uid 10001 --gid 10001 --create-home --shell /usr/sbin/nologin appuser && \
    mkdir -p /app/app/static/uploads/pets && \
    chown -R 10001:10001 /app

USER 10001:10001

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl --fail http://localhost:5000/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "2", "run:app"]
