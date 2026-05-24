import pandas as pd
import networkx as nx

# Load logs
df = pd.read_csv("data/logs.csv")

# Create graph
G = nx.DiGraph()

# Build dependencies
for i in range(len(df) - 1):

    current_service = df.iloc[i]["service"]
    next_service = df.iloc[i + 1]["service"]

    if current_service == "database" and next_service == "auth-service":
        continue

    if current_service != next_service:
        G.add_edge(current_service, next_service)

# Simulate service failure
failed_service = "payment-service"

# Find impacted services
impacted = list(nx.descendants(G, failed_service))

print(f"\nService Failure: {failed_service}\n")

print("Blast Radius Impact:\n")

for service in impacted:
    print(f"- {service}")