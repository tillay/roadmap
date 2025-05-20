from csvparser import make_roads, shorthand
import math
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
        return px, py
    return None

def get_node_endpoints(csv_file):
    endpoints = []
    nodes = make_roads(csv_file)
    for i in range(len(nodes)):
        endpoints.append((nodes[i][1],nodes[i][2]))
    return endpoints

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

def build_graph(segments):
    graph = defaultdict(list)
    all_points = set()
    for a, b in segments:
        all_points.add(a)
        all_points.add(b)
    new_segs = []

    for i, (a1, a2) in enumerate(segments):
        ipts = []
        for j, (b1, b2) in enumerate(segments):
            if i == j: continue
            ipt = intersection(a1, a2, b1, b2)
            if ipt: ipts.append(ipt)
        ipts = sorted(ipts + [a1, a2], key=lambda p: ((p[0]-a1[0])**2 + (p[1]-a1[1])**2))
        for x in range(len(ipts)-1):
            p1, p2 = ipts[x], ipts[x+1]
            if p1 != p2:
                new_segs.append((p1, p2))
                all_points.add(p1)
                all_points.add(p2)

    for a, b in new_segs:
        d = dist(a, b)
        graph[a].append((b, d))
        graph[b].append((a, d))

    return graph


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def dijkstra(graph, start, end):
    q, visited, dist_map, prev = [(0, start)], set(), {start: 0}, {}
    while q:
        d, node = q.pop(0)
        if node in visited: continue
        visited.add(node)
        if node == end: break
        for neighbor, weight in graph[node]:
            new_d = d + weight
            if new_d < dist_map.get(neighbor, float('inf')):
                dist_map[neighbor] = new_d
                prev[neighbor] = node
                q.append((new_d, neighbor))
        q.sort()
    path = []
    while end in prev:
        path.append(end)
        end = prev[end]
    if path: path.append(start)
    return path[::-1]

def find_path(segments, start, end):
    graph = build_graph(segments)
    return dijkstra(graph, start, end)