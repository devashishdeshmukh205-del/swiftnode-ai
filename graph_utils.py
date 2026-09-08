import networkx as nx
import matplotlib.pyplot as plt

def create_city_graph():
    G = nx.Graph()
    nodes = ["Library", "Dorm A", "Dorm B", "Cafeteria", "Science Block", "Admin", "Sports Complex"]
    G.add_nodes_from(nodes)
    
    edges = [
        ("Library", "Dorm A", 4, False),
        ("Library", "Cafeteria", 2, False),
        ("Dorm A", "Science Block", 5, True),
        ("Cafeteria", "Science Block", 1, False),
        ("Cafeteria", "Admin", 3, False),
        ("Science Block", "Sports Complex", 2, False),
        ("Admin", "Sports Complex", 4, False),
        ("Dorm B", "Library", 3, False),
        ("Dorm B", "Admin", 6, True)
    ]
    
    for u, v, weight, hazard in edges:
        G.add_edge(u, v, weight=weight, hazard=hazard)
        
    pos = {
        "Library": (0, 2),
        "Dorm A": (-2, 1),
        "Dorm B": (-1, 4),
        "Cafeteria": (1, 1),
        "Science Block": (2, 3),
        "Admin": (3, 1),
        "Sports Complex": (4, 3)
    }
    nx.set_node_attributes(G, pos, 'pos')
    return G

def draw_graph(G, path=None, current_node_idx=None):
    fig, ax = plt.subplots(figsize=(8, 6))
    pos = nx.get_node_attributes(G, 'pos')
    
    nx.draw_networkx_nodes(G, pos, node_color='#b85c96', node_size=700, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, font_color='white', font_weight='bold', ax=ax)
    
    edge_colors = ['red' if G[u][v].get('hazard', False) else '#ccc' for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2, ax=ax)
    
    edge_labels = {(u, v): f"{d['weight']}km" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
    
    if path and len(path) > 1:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='#2ecc71', width=4, ax=ax)
        
        if current_node_idx is not None and current_node_idx < len(path):
            current_node = path[current_node_idx]
            nx.draw_networkx_nodes(G, pos, nodelist=[current_node], node_color='#f1c40f', node_size=900, ax=ax)

    ax.axis('off')
    return fig