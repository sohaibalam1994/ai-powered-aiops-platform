import pandas as pd
from datetime import datetime, timedelta
import random
import os

os.makedirs("data", exist_ok=True)

# Realistic service dependency chain
service_flow = [
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
    "high_cpu"
]

rows = []

start = datetime.now()

for i in range(100):

    current_time = start + timedelta(minutes=i)

    # Simulate flow through services
    for service in service_flow:

        rows.append({
            "timestamp": current_time,
            "service": service,
            "event": random.choice(events),
            "severity": random.choice(["low", "medium", "high"]),
            "response_time": random.randint(100, 2000)
        })

        # Small time difference
        current_time += timedelta(seconds=5)

df = pd.DataFrame(rows)

df.to_csv("data/logs.csv", index=False)

print("Realistic synthetic logs generated!")