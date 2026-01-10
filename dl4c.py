import networkx as nx
import pandas as pd
from utils import json2networkx
import random

MAX_NO_OF_FLOWS = 300
MAX_FLOW_THROUGHPUT = 100
MAX_LINK_CAPACITY = 1000

NO_OF_FLOWS = random.randrange(1, MAX_NO_OF_FLOWS)

G = json2networkx("topologies\mesh3x3.json")

flows = {}

for flow in range(NO_OF_FLOWS):
    src, dst = random.sample(range(1, 10), 2)
    flow_throughput = random.randrange(1, MAX_FLOW_THROUGHPUT)

    shortest_path = nx.dijkstra_path(G, source=str(src), target=str(dst), weight='weight')

    links = list(zip(shortest_path, shortest_path[1:]))

    least_link_available_capacity = 1000

    for u, v in links:
        sum_throughput = 0
        for flow_id in G[u][v]['flows']:
            sum_throughput += flows[flow_id]["throughput"]
        
        link_available_capacity = MAX_LINK_CAPACITY - sum_throughput
        if link_available_capacity < least_link_available_capacity:
            least_link_available_capacity = link_available_capacity 
    
    flow_throughput = min(flow_throughput, least_link_available_capacity)

    flows[flow] = {"src": str(src), "dst": str(dst), "throughput": flow_throughput}

    for u, v in links:
        G[u][v]['flows'].append(flow)


nodes = sorted(G.nodes())
traffic_matrix = pd.DataFrame(0.0, index=nodes, columns=nodes)

for u, v, data in G.edges(data=True):
    
    current_link_flows = data.get('flows')
    total_throughput = 0
    
    for flow_id in current_link_flows:
        total_throughput += flows[flow_id]['throughput']

    traffic_matrix.loc[u, v] = total_throughput

print("Traffic Matrix (Mbps):")
print(traffic_matrix)

# plt.figure(figsize=(10, 8))

# # Create the heatmap
# # annot=True writes the numbers in the cells
# # cmap='viridis' is a color map (Yellow = High, Purple = Low)
# # fmt='g' prevents scientific notation (like 3e+02)
# sns.heatmap(traffic_matrix, annot=True, cmap='viridis', fmt='g', linewidths=0.5)

# plt.title("Network Traffic Matrix (Throughput in Mbps)")
# plt.xlabel("Destination Switch")
# plt.ylabel("Source Switch")

# plt.show()