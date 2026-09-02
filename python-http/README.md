# CMPE 273 – Week 1 Lab 1: Two-Service HTTP Communication

A minimal distributed-systems lab demonstrating two independent HTTP services
that communicate over the network using Flask and the `requests` library.

---

## Project Structure

```
python-http/
├── service-a/
│   ├── app.py            # Flask application – runs on port 8080
│   └── requirements.txt
└── service-b/
    ├── app.py            # Flask application – runs on port 8081
    └── requirements.txt
```

---

## What Makes This Distributed?

Service A and Service B are **two completely independent processes** — each has
its own Python interpreter, its own network socket, and its own lifecycle.
They communicate exclusively over **HTTP** (the same mechanism used across
servers on the internet). Neither service shares memory, global state, or a
function call with the other; the only coupling is the network interface.
This mirrors how real-world microservices are deployed: they can run on
different machines, be restarted independently, and fail without immediately
crashing the rest of the system. Service B demonstrates this by staying alive
and returning a graceful `503` error when Service A is stopped — a key
property of distributed fault isolation.

---

## Prerequisites

- Python 3.9+
- `pip`

---

## Setup and Run

Each service needs its **own terminal window** and its own virtual environment.

### Terminal 1 – Service A (port 8080)

```bash
cd python-http/service-a
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 app.py
```

Expected startup output:
```
 * Running on http://127.0.0.1:8080
```

### Terminal 2 – Service B (port 8081)

```bash
cd python-http/service-b
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 app.py
```

Expected startup output:
```
 * Running on http://127.0.0.1:8081
```

---

## API Reference

### Service A – port 8080

| Method | Endpoint         | Description                        |
|--------|------------------|------------------------------------|
| GET    | `/health`        | Returns service health status      |
| GET    | `/echo?msg=...`  | Echoes the `msg` query parameter   |

### Service B – port 8081

| Method | Endpoint              | Description                                      |
|--------|-----------------------|--------------------------------------------------|
| GET    | `/health`             | Returns service health status                    |
| GET    | `/call-echo?msg=...`  | Calls Service A's `/echo` and returns its reply  |

---

## Testing

### Service A health check
```bash
curl http://127.0.0.1:8080/health
```
Expected response:
```json
{"service": "A", "status": "ok"}
```

### Service A echo
```bash
curl "http://127.0.0.1:8080/echo?msg=hello"
```
Expected response:
```json
{"service": "A", "echo": "hello"}
```

### Service B health check
```bash
curl http://127.0.0.1:8081/health
```
Expected response:
```json
{"service": "B", "status": "ok"}
```

### Service B calls Service A (success path)
```bash
curl "http://127.0.0.1:8081/call-echo?msg=hello"
```
Expected response (Service A is running):
```json
{"service": "A", "echo": "hello"}
```

### Service B with Service A stopped (failure path)

Stop Service A (Ctrl+C in Terminal 1), then:

```bash
curl -i "http://127.0.0.1:8081/call-echo?msg=hello"
```

Expected response (HTTP 503):
```
HTTP/1.1 503 SERVICE UNAVAILABLE

{"service": "B", "error": "Service A is unreachable", "upstream": "http://127.0.0.1:8080"}
```

Service B continues running and handles every subsequent request.

---

## Log Format

Every request is logged to stdout in the following format:

```
YYYY-MM-DD HH:MM:SS,mmm service=<A|B> endpoint=<path> status=<code> latency_ms=<ms>
```

Example:
```
2024-09-02 10:30:01,452 service=A endpoint=/echo status=200 latency_ms=0.42
2024-09-02 10:30:01,523 service=B endpoint=/call-echo status=200 latency_ms=4.71
```

---

## Lab Requirement Checklist

- [x] Service A runs on port 8080
- [x] Service A `GET /health` returns JSON
- [x] Service A `GET /echo?msg=...` returns JSON
- [x] Service B runs on port 8081
- [x] Service B `GET /health` returns JSON
- [x] Service B `GET /call-echo?msg=...` calls Service A and returns its response
- [x] Both services run as independent processes
- [x] Both services log every request
- [x] Logs include service name, endpoint, HTTP status, and latency
- [x] Both services return clean JSON responses
- [x] Service B uses an explicit timeout (2 s) when calling Service A
- [x] Service B catches `Timeout` and `ConnectionError` exceptions
- [x] Service B returns HTTP 503 with a JSON error when Service A is unavailable
- [x] Service B continues running when Service A is stopped
