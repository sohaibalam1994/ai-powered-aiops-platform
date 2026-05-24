import pandas as pd
import random
import time
from datetime import datetime

services = [
    "auth-service",
    "payment-service",
    "order-service",
    "inventory-service",
    "notification-service",
    "database"
]

events = [
    "request_received",
    "processing",
    "success",
    "timeout",
    "high_cpu",
    "memory_spike",
    "connection_error"
]

severities = [
    "low",
    "medium",
    "high"
]

while True:

    log = {
        "timestamp": datetime.now(),
        "service": random.choice(services),
        "event": random.choice(events),
        "severity": random.choice(severities),
        "response_time": random.randint(100, 3000)
    }

    df = pd.DataFrame([log])

    df.to_csv(
        "data/logs.csv",
        mode='a',
        header=False,
        index=False
    )

    print(f"Generated log: {log}")

    time.sleep(2)