import pandas as pd
import networkx as nx

# Load logs
df = pd.read_csv("data/logs.csv")

# Create graph
G = nx.DiGraph()

# Add dependencies
for i in range(len(df) - 1):

    current_service = df.iloc[i]["service"]
    next_service = df.iloc[i + 1]["service"]

    # Ignore circular restart
    if current_service == "database" and next_service == "auth-service":
        continue

    if current_service != next_service:
        G.add_edge(current_service, next_service)

print("\nDetected Dependencies:\n")

for edge in G.edges():
    print(f"{edge[0]} --> {edge[1]}")