# Open Port Scanner

![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)

A fast, asynchronous IPv4 port scanner. It probes standard, registered, and private port ranges with high concurrency. Useful for network auditing, identifying exposed services on remote machines, or checking local listeners.

## Tech Stack

- **Python 3.12** (Core language)
- **`asyncio`** (Built-in concurrency)
- **Docker** (Containerized execution)

## Run In Docker

Best for scanning remote targets or getting an external network perspective.

> [!NOTE]
> Docker uses a separate network namespace and the host firewall rules apply differently.
> When scanning your own host from inside a container, results can differ
> from running locally.

```bash
# Build the image
docker build -t open-port-scanner .

# Run container in interactive mode
docker run -it --rm open-port-scanner:latest
```

## Run Locally

Best for scanning the local machine (full visibility on local listeners).

```bash
python main.py
```
