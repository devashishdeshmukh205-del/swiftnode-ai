import math
import heapq
from collections import deque
import networkx as nx

def euclidean_heuristic(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def bfs_search(G, start, goal):
    queue = deque([[start]])
    visited = set([start])
    
    while queue:
        path = queue.popleft()
        node = path[-1]
        
        if node == goal:
            return path
            
        for neighbor in G.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return None

def a_star_search(G, start, goal, ignore_hazards=False):
    pos = nx.get_node_attributes(G, 'pos')
    frontier = [(0, [start])]
    visited = {}
    
    while frontier:
        cost, path = heapq.heappop(frontier)
        current = path[-1]
        
        if current == goal:
            return path, cost
            
        if current in visited and visited[current] <= cost:
            continue
        visited[current] = cost
        
        for neighbor in G.neighbors(current):
            edge_data = G[current][neighbor]
            
            if not ignore_hazards and edge_data.get('hazard', False):
                continue
                
            weight = edge_data.get('distance', 1)
            new_cost = cost + weight
            h = euclidean_heuristic(pos[neighbor], pos[goal])
            priority = new_cost + h
            
            heapq.heappush(frontier, (priority, path + [neighbor]))
            
    return None, float('inf')