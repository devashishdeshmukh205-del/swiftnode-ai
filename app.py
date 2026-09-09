import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="SwiftNode.ai", layout="wide")

st.title("Intelligent Campus Delivery Automation")
st.write("Automated Graph Orchestration & Pathfinding Platform")

# Sidebar Controls
st.sidebar.header("Dispatch Control Terminal")

# Algorithm Selection (Populates the dropdown selector)
algorithm_choice = st.sidebar.selectbox(
    "Select Routing Algorithm",
    options=["A* Search", "Dijkstra's Algorithm"]
)

# Binary search implementation for looking up campus entities
def binary_search_entity(sorted_list, target):
    low = 0
    high = len(sorted_list) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

# Campus buildings list (sorted for binary search demo)
campus_buildings = sorted(["Cafeteria", "Gym", "Home", "Hostel A", "Hostel B", "Lab", "Library"])

search_query = st.sidebar.text_input("Quick Lookup Building (Binary Search)", "Library")
if search_query:
    idx = binary_search_entity(campus_buildings, search_query)
    if idx != -1:
        st.sidebar.success(f"Found '{search_query}' at index {idx} using Binary Search.")
    else:
        st.sidebar.error("Building not found in registry.")

source = st.sidebar.selectbox("Source Node", campus_buildings, index=5)
target = st.sidebar.selectbox("Destination Node", campus_buildings, index=1)
payload = st.sidebar.selectbox("Active Payload", ["Midnight Pizza", "Medical Kit", "Document Packet"])

if st.sidebar.button("Dispatch Delivery Agent"):
    # Build Campus Graph with coordinates for A* heuristic
    G = nx.Graph()
    pos = {
        "Hostel A": (0, 0),
        "Library": (2, 1),
        "Hostel B": (1, 3),
        "Lab": (3, 2),
        "Cafeteria": (2, -1),
        "Home": (4, -1),
        "Gym": (4, 2)
    }
    
    for node, coords in pos.items():
        G.add_node(node, pos=coords)
        
    edges = [
        ("Hostel A", "Library", 4),
        ("Hostel A", "Cafeteria", 4),
        ("Hostel B", "Library", 3),
        ("Hostel B", "Lab", 6),
        ("Library", "Lab", 2),
        ("Library", "Cafeteria", 2),
        ("Cafeteria", "Home", 3),
        ("Lab", "Gym", 2),
        ("Lab", "Home", 1),
        ("Home", "Gym", 4)
    ]
    
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
        
    # Run selected search algorithm
    try:
        if algorithm_choice == "A* Search":
            def heuristic(u, v):
                p1 = pos[u]
                p2 = pos[v]
                return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5
            path = nx.astar_path(G, source, target, heuristic=heuristic, weight="weight")
        else:
            path = nx.dijkstra_path(G, source, target, weight="weight")
            
        st.success(f"Path Dispatched Successfully via {algorithm_choice}!")
        st.write(f"**Optimal Route Sequence:** {' → '.join(path)}")
        
        # Render Matplotlib Graph
        fig, ax = plt.subplots(figsize=(8, 5))
        node_positions = nx.get_node_attributes(G, 'pos')
        
        # Draw background elements
        nx.draw_networkx_nodes(G, node_positions, node_color="#e74c3c", node_size=700, ax=ax)
        nx.draw_networkx_labels(G, node_positions, font_color="white", font_weight="bold", ax=ax)
        nx.draw_networkx_edges(G, node_positions, edge_color="gray", width=2, ax=ax)
        
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, node_positions, edge_labels=edge_labels, ax=ax)
        
        # Highlight active path
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, node_positions, edgelist=path_edges, edge_color="#2c3e50", width=4, ax=ax)
        
        st.pyplot(fig)
        
    except nx.NetworkXNoPath:
        st.error("No valid path exists between the selected nodes.")
