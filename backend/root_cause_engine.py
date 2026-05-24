import random

def analyze_root_cause(failed_service):

    root_causes = {

        "payment-service": {
            "cause": "Database connection saturation",
            "confidence": random.randint(85, 98),
            "reason":
                "Spike in transaction latency detected "
                "between payment-service and database."
        },

        "order-service": {
            "cause": "Queue backlog overflow",
            "confidence": random.randint(80, 95),
            "reason":
                "Message processing delay observed "
                "in order pipeline."
        },

        "inventory-service": {
            "cause": "High CPU utilization",
            "confidence": random.randint(75, 92),
            "reason":
                "Inventory workers exceeded CPU threshold."
        },

        "notification-service": {
            "cause": "SMTP gateway timeout",
            "confidence": random.randint(70, 90),
            "reason":
                "External notification provider latency detected."
        },

        "database": {
            "cause": "Replication lag",
            "confidence": random.randint(88, 99),
            "reason":
                "Primary database replication falling behind."
        },

        "auth-service": {
            "cause": "Token validation bottleneck",
            "confidence": random.randint(78, 94),
            "reason":
                "Authentication token requests exceeded limit."
        }
    }

    return root_causes.get(
        failed_service,
        {
            "cause": "Unknown issue",
            "confidence": 50,
            "reason": "Insufficient telemetry data."
        }
    )