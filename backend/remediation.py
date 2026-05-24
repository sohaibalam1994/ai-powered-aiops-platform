def recommend_fix(event):

    fixes = {
        "timeout": "Increase timeout threshold",
        "high_cpu": "Scale service horizontally",
        "memory_spike": "Restart container",
        "db_failure": "Check DB connections"
    }

    return fixes.get(event, "Investigate manually")