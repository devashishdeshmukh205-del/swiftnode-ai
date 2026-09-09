import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from pathfinding import bfs_search, a_star_search

# 1. Page Config
st.set_page_config(page_title="SwiftNode.ai - Intelligent Logistics", layout="wide", initial_sidebar_state="collapsed")

# 2. Advanced Custom CSS
st.markdown("""
    <style>
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display: none !important;}
    
    .stApp {
        background-color: #fafbfa;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 1400px;
    }

    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 2rem;
        border-bottom: 1px solid #eee;
        margin-bottom: 3rem;
    }
    .logo-text {
        font-size: 28px;
        font-weight: 800;
        color: #000;
        letter-spacing: -1px;
    }
    .logo-accent {
        color: #b85c96;
    }
    .nav-button {
        background-color: #b85c96;
        color: white;
        padding: 10px 20px;
        border-radius: 30px;
        font-weight: bold;
        text-decoration: none;
        font-size: 14px;
    }

    .hero-title {
        font-size: 56px;
        font-weight: 800;
        line-height: 1.1;
        color: #111;
        margin-bottom: 10px;
        letter-spacing: -1.5px;
    }
    .hero-subtitle {
        font-size: 28px;
        font-weight: 600;
        color: #b85c96;
        margin-bottom: 30px;
    }
    
    .card-container {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-top: 50px;
        margin-bottom: 60px;
    }
    .value-card {
        background: white;
        padding: 30px 20px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.04);
        flex: 1;
        border-bottom: 4px solid #fdf5fa;
    }
    .card-icon {
        font-size: 40px;
        color: #333;
        margin-bottom: 15px;
    }
    .card-title {
        font-weight: 800;
        font-size: 18px;
        color: #111;
        margin-bottom: 8px;
    }
    .card-desc {
        font-size: 13px;
        color: #666;
        line-height: 1.4;
    }

    div.stButton > button {
        background-color: #b85c96;
        color: white;
        border-radius: 30px;
        font-weight: bold;
        border: none;
        padding: 0.75rem 2rem;
        box-shadow: 0 4px 14px rgba(184, 92, 150, 0.4);
    }
    
    .section-header {
        font-size: 32px;
        font-weight: 800;
        text-align: center;
        color: #b85c96;
        margin-bottom: 20px;
        margin-top: 40px;
    }
    .section-sub {
        text-align: center;
        color: #555;
        max-width: 800px;
        margin: 0 auto 40px auto;
        font-size: 16px;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Inline Graph Utilities with Label Background Bounding Box
def create_city_graph():
    G = nx.Graph()
    nodes = ["Library", "Hostel A", "Hostel B", "Cafeteria", "Lab", "Home", "Gym"]
    G.add_nodes_from(nodes)
    
    edges = [
        ("Library", "Hostel A", 4, False),
        ("Library", "Cafeteria", 2, False),
        ("Hostel A", "Lab", 5, True),
        ("Cafeteria", "Lab", 1, False),
        ("Cafeteria", "Home", 3, False),
        ("Lab", "Gym", 2, False),
        ("Home", "Gym", 4, False),
        ("Hostel B", "Library", 3, False),
        ("Hostel B", "Home", 6, True)
    ]
    
    for u, v, weight, hazard in edges:
        G.add_edge(u, v, weight=weight, hazard=hazard)
        
    pos = {
        "Library": (0, 2),
        "Hostel A": (-2, 1),
        "Hostel B": (-1, 4),
        "Cafeteria": (1, 1),
        "Lab": (2, 3),
        "Home": (3, 1),
        "Gym": (4, 3)
    }
    nx.set_node_attributes(G, pos, 'pos')
    return G

def draw_graph(G, path=None, highlight_start=True):
    fig, ax = plt.subplots(figsize=(10, 8))
    pos = nx.get_node_attributes(G, 'pos')
    
    # Draw background edges
    edge_colors = ['red' if G[u][v].get('hazard', False) else '#ccc' for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2, ax=ax)
    
    # Draw active path edges on top in GREEN if available
    if path and len(path) > 1:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='#2ecc71', width=4, ax=ax)

    # Draw nodes (names hidden to prevent text clutter)
    nx.draw_networkx_nodes(G, pos, node_color='#b85c96', node_size=2500, ax=ax)
    
    if path and len(path) > 0 and highlight_start:
        start_node = path[0]
        nx.draw_networkx_nodes(G, pos, nodelist=[start_node], node_color='#f1c40f', node_size=2800, ax=ax)

    # Draw edge labels LAST with a white background box and "km" unit so they are never hidden by lines
    edge_labels = {(u, v): f"{d['weight']} km" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(
        G, pos, 
        edge_labels=edge_labels, 
        ax=ax, 
        font_size=8,
        bbox=dict(boxstyle="round,pad=0.3", ec="none", fc="white", alpha=0.85)
    )

    ax.axis('off')
    return fig

# 4. Navbar & Hero
st.markdown("""
    <div class="navbar">
        <div class="logo-text">SwiftNode<span class="logo-accent">.ai</span></div>
        <a href="#demo-section" class="nav-button">Get Started</a>
    </div>
""", unsafe_allow_html=True)

col_text, col_img = st.columns([1.2, 1])
with col_text:
    st.markdown("""
        <div style="margin-top: 40px;">
            <div class="hero-title">Intelligent Campus<br>Delivery Automation</div>
            <div class="hero-subtitle">Maximize Efficiency, Minimize Delays</div>
            <p style="color: #555; font-size: 18px; margin-bottom: 30px; max-width: 90%;">
                An AI-powered graph orchestration platform that unifies routing nodes, network constraints, and live cargo workflows into a single intelligent system.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    b1, b2, _ = st.columns([1, 1, 2])
    with b1:
        st.button("Launch App", use_container_width=True)
    with b2:
        st.button("View Specs", type="secondary", use_container_width=True)

# 5. Cards Section
st.markdown("""
    <div class="section-header">Immediate Impact Across the Network</div>
    <div class="section-sub">SwiftNode.ai optimizes resource traversal across complex paths for fast and efficient delivery routing.</div>
    
    <div class="card-container">
        <div class="value-card">
            <div class="card-icon">🚀</div>
            <div class="card-title">X4 Throughput</div>
            <div class="card-desc">More deliveries, faster, and more predictable.</div>
        </div>
        <div class="value-card">
            <div class="card-icon">⚙️</div>
            <div class="card-title">60% Efficiency</div>
            <div class="card-desc">Optimized traversal states using Heuristic A*.</div>
        </div>
        <div class="value-card">
            <div class="card-icon">📉</div>
            <div class="card-title">X7.5 Cost Reduction</div>
            <div class="card-desc">Lower operational costs through graph minimization.</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border: none; border-top: 1px solid #eee; margin: 40px 0;'>", unsafe_allow_html=True)

# 6. Interactive Terminal
st.markdown('<div id="demo-section" class="section-header">📦 Live Complex Cargo Dispatch Terminal</div>', unsafe_allow_html=True)

G = create_city_graph()
nodes = list(G.nodes())

demo_col1, demo_col2 = st.columns([1, 2.5])

with demo_col1:
    st.markdown("### 🕹️ Mission Control")
    st.markdown("Configure your delivery cargo and route parameters:")
    
    start_node = st.selectbox("📍 Pick-up Terminal", nodes, index=0)
    goal_node = st.selectbox("🎯 Drop-off Hub", nodes, index=len(nodes)-1)
    
    # Fixed the empty options array bug by explicitly providing choice options
    algorithm = st.radio("🧠 Routing Algorithm", options=["A* Search (Optimal & Smart)", "Breadth-First Search (BFS)"])
    avoid_hazards = st.checkbox("🚧 Avoid Traffic/Hazard Zones", value=True)
    
    package_type = st.selectbox("🎁 Cargo Type", ["🍕 Midnight Pizza", "📚 Assignment Notes", "💻 Laptop Charger", "☕ Cold Coffee"])
    st.info(f"Active Payload: **{package_type}**")
    
    st.markdown("<br>", unsafe_allow_html=True)
    dispatch = st.button("🚀 Dispatch Delivery Agent", use_container_width=True)

with demo_col2:
    if dispatch:
        with st.spinner(f"🤖 AI agent routing cargo [{package_type}]..."):
            if "Breadth-First" in algorithm:
                path = bfs_search(G, start_node, goal_node)
                cost = "N/A"
            else:
                path, cost = a_star_search(G, start_node, goal_node, ignore_hazards=not avoid_hazards)
                
        if path:
            st.success(f"🎉 **Route Discovered for {package_type}:** {' ➔ '.join(path)}")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Nodes", len(path))
            m2.metric("Route Cost", f"{cost} km" if isinstance(cost, (int, float)) else cost)
            m3.metric("Status", "🛵 Agent Ready at Start")
            
            fig = draw_graph(G, path, highlight_start=True)
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.error("🚨 Mission Failed! No safe route found bypassing hazard zones.")
            fig = draw_graph(G, path=None)
            st.pyplot(fig)
            plt.close(fig)
    else:
        st.markdown("<div style='text-align:center; padding: 30px; background: white; border-radius: 10px; border: 1px solid #eee;'>Select your options on the left and click <b>Dispatch Delivery Agent</b> to view the optimal route and agent positioning.</div>", unsafe_allow_html=True)
        fig = draw_graph(G, path=None)
        st.pyplot(fig)
        plt.close(fig)
