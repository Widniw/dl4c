import networkx as nx
import pandas as pd
from utils import json2networkx
import random


def generate_regular_traffic(topology_json, max_no_of_flows, max_flow_throughput, max_link_capacity):
    no_of_flows = random.randrange(1, max_no_of_flows)

    G = json2networkx(topology_json)

    flows = {}

    for flow in range(no_of_flows):
        src, dst = random.sample(range(1, 10), 2)
        flow_throughput = random.randrange(1, max_flow_throughput)

        shortest_path = nx.dijkstra_path(G, source=str(src), target=str(dst), weight='weight')

        links = list(zip(shortest_path, shortest_path[1:]))

        least_link_available_capacity = max_link_capacity

        for u, v in links:
            sum_throughput = 0
            for flow_id in G[u][v]['flows']:
                sum_throughput += flows[flow_id]["throughput"]
            
            link_available_capacity = max_link_capacity - sum_throughput
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

    return traffic_matrix

def generate_ddos_attack(topology_json, max_no_of_flows, max_flow_throughput, max_link_capacity, no_of_attackers):
    no_of_flows = random.randrange(1, max_no_of_flows)

    G = json2networkx(topology_json)

    flows = {}

    for flow in range(no_of_flows):
        src, dst = random.sample(range(1, 10), 2)
        flow_throughput = random.randrange(1, max_flow_throughput)

        shortest_path = nx.dijkstra_path(G, source=str(src), target=str(dst), weight='weight')

        links = list(zip(shortest_path, shortest_path[1:]))

        least_link_available_capacity = max_link_capacity

        for u, v in links:
            sum_throughput = 0
            for flow_id in G[u][v]['flows']:
                sum_throughput += flows[flow_id]["throughput"]
            
            link_available_capacity = max_link_capacity - sum_throughput
            if link_available_capacity < least_link_available_capacity:
                least_link_available_capacity = link_available_capacity 
        
        flow_throughput = min(flow_throughput, least_link_available_capacity)

        flows[flow] = {"src": str(src), "dst": str(dst), "throughput": flow_throughput}

        for u, v in links:
            G[u][v]['flows'].append(flow)
    
    no_of_ddos_victims = 1
    no_of_ddos_actors = no_of_attackers + no_of_ddos_victims

    ddos_actors_ids = random.sample(range(1,10), no_of_ddos_actors)

    ddos_attackers_ids = ddos_actors_ids[:-1]
    ddos_victim_id = ddos_actors_ids[-1]

    for attacker in ddos_attackers_ids:
        shortest_path = nx.dijkstra_path(G, source=str(attacker), target=str(ddos_victim_id), weight='weight')

        links = list(zip(shortest_path, shortest_path[1:]))

        least_link_available_capacity = max_link_capacity

        for u, v in links:
            sum_throughput = 0
            for flow_id in G[u][v]['flows']:
                sum_throughput += flows[flow_id]["throughput"]
            
            link_available_capacity = max_link_capacity - sum_throughput
            if link_available_capacity < least_link_available_capacity:
                least_link_available_capacity = link_available_capacity 
        
        flow_throughput = least_link_available_capacity

        flows[str(attacker)] = {"src": str(attacker), "dst": str(ddos_victim_id), "throughput": flow_throughput}

        for u, v in links:
            G[u][v]['flows'].append(str(attacker))


    nodes = sorted(G.nodes())
    traffic_matrix = pd.DataFrame(0.0, index=nodes, columns=nodes)

    for u, v, data in G.edges(data=True):
        
        current_link_flows = data.get('flows')
        total_throughput = 0
        
        for flow_id in current_link_flows:
            total_throughput += flows[flow_id]['throughput']

        traffic_matrix.loc[u, v] = total_throughput

    return traffic_matrix
