import logging
import time
import requests
from flask import Flask, jsonify, request

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)

app = Flask(__name__)

SERVICE = "B"
SERVICE_A_URL = "http://127.0.0.1:8080"
TIMEOUT = 2  # seconds


@app.route("/health")
def health():
    start = time.time()
    payload = jsonify({"service": SERVICE, "status": "ok"})
    latency_ms = (time.time() - start) * 1000
    logging.info(
        "service=%s endpoint=/health status=200 latency_ms=%.2f",
        SERVICE, latency_ms,
    )
    return payload, 200


@app.route("/call-echo")
def call_echo():
    start = time.time()
    msg = request.args.get("msg", "")

    try:
        resp = requests.get(
            f"{SERVICE_A_URL}/echo",
            params={"msg": msg},
            timeout=TIMEOUT,
        )
        payload = jsonify(resp.json())
        status = 200

    except requests.exceptions.Timeout:
        payload = jsonify({
            "service": SERVICE,
            "error": "Service A timed out",
            "upstream": SERVICE_A_URL,
        })
        status = 503

    except requests.exceptions.ConnectionError:
        payload = jsonify({
            "service": SERVICE,
            "error": "Service A is unreachable",
            "upstream": SERVICE_A_URL,
        })
        status = 503

    latency_ms = (time.time() - start) * 1000
    logging.info(
        "service=%s endpoint=/call-echo status=%d latency_ms=%.2f",
        SERVICE, status, latency_ms,
    )
    return payload, status


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081)
