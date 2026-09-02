import logging
import time
from flask import Flask, jsonify, request

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)

app = Flask(__name__)

SERVICE = "A"


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


@app.route("/echo")
def echo():
    start = time.time()
    msg = request.args.get("msg", "")
    payload = jsonify({"service": SERVICE, "echo": msg})
    latency_ms = (time.time() - start) * 1000
    logging.info(
        "service=%s endpoint=/echo status=200 latency_ms=%.2f",
        SERVICE, latency_ms,
    )
    return payload, 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
