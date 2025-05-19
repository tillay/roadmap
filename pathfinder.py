from csvparser import make_roads, shorthand
import math, heapq
from collections import defaultdict, deque

def intersection(p1, p2, p3, p4):
    x1,y1 = p1
    x2,y2 = p2
    x3,y3 = p3
    x4,y4 = p4
    d = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
    if d == 0: return None
    px = ((x1*y2 - y1*x2)*(x3-x4)-(x1-x2)*(x3*y4 - y3*x4))/d
    py = ((x1*y2 - y1*x2)*(y3-y4)-(y1-y2)*(x3*y4 - y3*x4))/d
    if min(x1,x2)<=px<=max(x1,x2) and min(y1,y2)<=py<=max(y1,y2) and min(x3,x4)<=px<=max(x3,x4) and min(y3,y4)<=py<=max(y3,y4):
        return (px, py)
    return None

def are_same_points(p1, p2):
    return abs(p1[0]-p2[0])==0 and abs(p1[1]-p2[1])==0

def get_node_endpoints(csv_file):
    endpoints = []
    nodes = make_roads(csv_file)
    for i in range(len(nodes)):
        endpoints.append([nodes[i][1],nodes[i][2]])
    return endpoints

def splice_nodes(segments):
    intersections = []
    for i,(p1,p2) in enumerate(segments):
        for j in range(i+1,len(segments)):
            p3,p4 = segments[j]
            point = intersection(p1,p2,p3,p4)
            if point is None: continue
            is_endpoint = are_same_points(point,p1) or are_same_points(point,p2) or are_same_points(point,p3) or are_same_points(point,p4)
            if not is_endpoint: intersections.append((i,j,point))
    new_segments = []
    for i,(p1,p2) in enumerate(segments):
        pts = [p1,p2]
        for j,k,pt in intersections:
            if i==j or i==k: pts.append(pt)
        vertical = abs(p1[0]-p2[0])<1e-9
        pts.sort(key=lambda p: p[1] if vertical else p[0])
        for k in range(len(pts)-1):
            a,b=pts[k],pts[k+1]
            if not are_same_points(a,b): new_segments.append((a,b))
    return new_segments

def resplice(node_list, point):
    problem_node = closest_segment(node_list, point)
    separation_point = problem_node[2]
    problem_node = [problem_node[0],problem_node[1]]
    for i in range(len(node_list)):
        if node_list[i] == problem_node:
            print(node_list[i])
            node_list.pop(i)
    node_list.append([problem_node[0],separation_point])
    node_list.append([separation_point, problem_node[1]])
    node_list.append([point, separation_point])
    return node_list


def find_shortest_path(segments, start_point, end_point):
    graph = defaultdict(list)
    for a, b in segments:
        graph[a].append(b)
        graph[b].append(a)
    visited = set()
    queue = deque([(start_point, [start_point])])
    while queue:
        node, path = queue.popleft()
        if node == end_point:
            return path
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    return []

def find_closest_point(node_array, cursor_x, cursor_y, width=None):
    min_dist = float('inf')
    closest_point = None
    for node in node_array:
        points = node[1:]
        for x, z in points:
            dist = (x - cursor_x) ** 2 + (z - cursor_y) ** 2
            if dist < min_dist:
                min_dist = dist
                closest_point = (x, z)
    if width and math.sqrt(abs((cursor_x-closest_point[0])**2 + (cursor_y-closest_point[1])**2)) < width / 30:
        return closest_point
    else: return closest_segment(node_array,[cursor_x,cursor_y])[2]

def get_length(point_list):
    print(point_list)
    distance = 0
    for i in range(len(point_list)-1):
        distance += math.sqrt(abs((point_list[i][0]-point_list[i+1][0])**2 + (point_list[i+1][1]-point_list[i][1])**2))
    return distance

def closest_segment(nodes, point):
    min_dist = float('inf')
    closest = None
    px, py = point
    for a, b in nodes:
        x1, y1 = a
        x2, y2 = b
        dx, dy = x2 - x1, y2 - y1
        if dx == dy == 0:
            proj = (x1, y1)
        else:
            t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
            proj = (x1 + t * dx, y1 + t * dy)
        d = (proj[0] - px) ** 2 + (proj[1] - py) ** 2
        if d < min_dist:
            min_dist = d
            closest = (a, b, proj)
    return closest