from generate_sample import generate_regular_traffic, generate_ddos_attack
import numpy as np


MAX_NO_OF_FLOWS = 200
MAX_FLOW_THROUGHPUT = 100
MAX_LINK_CAPACITY = 1000
TOPOLOGY_JSON = "topologies\mesh3x3.json"
NO_OF_ATTACKERS = 8
NO_OF_SAMPLES = 10000

dataset = []

for i in range(NO_OF_SAMPLES):
    traffic_matrix = generate_regular_traffic(TOPOLOGY_JSON, MAX_NO_OF_FLOWS, MAX_FLOW_THROUGHPUT, MAX_LINK_CAPACITY)
    dataset.append(traffic_matrix)

X_train = np.array(dataset)      

np.save('traffic_data.npy', X_train)
print(f"File saved")
