from collections import deque
import matplotlib
import networkx as nx
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')


# Function for searching for increasing flow (BFS) from source to sink
def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)  # The visited array keeps track of which vertices have already been visited to avoid loops.
    queue = deque([source])  # The queue stores vertices for further processing, starting with source, and then sequentially checking possible paths to sink.
    visited[source] = True

    while queue:
        current_node = queue.popleft()  # For each node get current_node from the queue
        for neighbor in range(len(capacity_matrix)):  # its neighbors are checked
            # If the neighbor has not yet been visited and there is residual capacity in the channel
            if not visited[neighbor] and capacity_matrix[current_node][neighbor] - flow_matrix[current_node][neighbor] > 0:
                parent[neighbor] = current_node  # neighbor is written to parent so that the path can be restored after BFS is terminated
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)  # Neighbor ID is added to the queue

    return False


# function for calculating maximum flow
def edmonds_karp(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]  # We initialize the flow matrix with zero
    parent = [-1] * num_nodes
    max_flow = 0  # will store the total flow passing from source to sink

    # As long as there is an increasing path, we add a flow
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):  # When there are no more new increasing paths, the algorithm terminates
        # We find the minimum throughput along the found path (bottleneck)
        min_path_flow = float("Inf")  # will be equal to the minimum remaining capacity on the path — that is how much can be added to the flow along the found path
        current_node = sink
        while current_node != source:  # Starting from sink, we move to source using parent
            previous_node = parent[current_node]
            min_path_flow = min(min_path_flow, capacity_matrix[previous_node][current_node] - flow_matrix[previous_node][current_node])
            current_node = previous_node

        # We update the flow along the path, taking into account the return flow
        current_node = sink
        # Starting from the sink, we update the flow_matrix by adding min_path_flow in the direction from source to sink and subtracting it in the opposite direction
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += min_path_flow  # from previous_node to current_node
            flow_matrix[current_node][previous_node] -= min_path_flow  # from current_node to previous_node
            current_node = previous_node

        max_flow += min_path_flow  # Increase the maximum flow by min_path_flow

    return max_flow


edges = [
    ("T1", "W1", 25),
    ("T1", "W2", 20),
    ("T1", "W3", 15),
    ("T2", "W3", 15),
    ("T2", "W4", 30),
    ("T2", "W2", 10),
    ("W1", "S1", 15),
    ("W1", "S2", 10),
    ("W1", "S3", 20),
    ("W2", "S4", 15),
    ("W2", "S5", 10),
    ("W2", "S6", 25),
    ("W3", "S7", 20),
    ("W3", "S8", 15),
    ("W3", "S9", 10),
    ("W4", "S10", 20),
    ("W4", "S11", 10),
    ("W4", "S12", 15),
    ("W4", "S13", 5),
    ("W4", "S14", 10)
]

pos = {
    "T1": (1, 2),
    "T2": (5, 2),
    "W1": (2, 3),
    "W2": (4, 3),
    "W3": (2, 1),
    "W4": (4, 1),
    "S1": (0, 4),
    "S2": (1, 4),
    "S3": (2, 4),
    "S4": (3, 4),
    "S5": (4, 4),
    "S6": (5, 4),
    "S7": (0, 0),
    "S8": (1, 0),
    "S9": (2, 0),
    "S10": (3, 0),
    "S11": (4, 0),
    "S12": (5, 0),
    "S13": (6, 0),
    "S14": (7, 0),
}

terminals = ["T1", "T2"]
stores = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "S11", "S12", "S13", "S14"]

G = nx.DiGraph()
G.add_weighted_edges_from(edges)

nodes = list(pos.keys())
node_index = {node: i for i, node in enumerate(nodes)}
n = len(nodes)
capacity_matrix = [[0] * n for _ in range(n)]
for src, dst, weight in edges:
    i = node_index[src]
    j = node_index[dst]
    capacity_matrix[i][j] = weight

for row in capacity_matrix:
    print(row)

table = f"| {'Terminal':<8} | {'Store':<8} | Max Flow |\n"
table += f"|{'-' * 10}|{'-' * 10}|{'-' * 10}|\n"
for src in terminals:
    for dst in stores:
        max_flow = edmonds_karp(capacity_matrix, node_index[src], node_index[dst])
        if max_flow > 0:
            table += f'| {src:<8} | {dst:<8} | {max_flow:>8} |\n'

print(table)

node_colors = []
for node in G.nodes():
    if node.startswith("T"):
        node_colors.append("lightcoral")
    elif node.startswith("W"):
        node_colors.append("mediumaquamarine")
    else:
        node_colors.append("skyblue")

plt.figure(figsize=(14, 8))
nx.draw(G, pos, with_labels=True, node_size=1500, node_color=node_colors, font_size=12, font_weight="bold", arrows=True)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()
