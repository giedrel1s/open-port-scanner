# Open Port Scanner

Scans for open ports.

# How To Use

Couple options to run the script/tool.

## Docker

Best for scanning remote targets or getting an external network perspective.
Note: when scanning your own host from inside a container, results can differ
from running locally because Docker uses a separate network namespace and the
host firewall rules apply differently.

```bash
# Build the image
docker build -t py-port-scanner .

# Run container in interactive mode
docker run -it py-port-scanner
```

## Local

Best for scanning the local machine (full visibility on local listeners).
Can run locally (needs python):

```bash
python main.py
```

<!-- Usecase / purpose -->
