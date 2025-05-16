import csv

def shorthand(number):
    prefix = ""
    if number < 0:
        number = abs(number)
        prefix = "-"

    if number < 1000:
        return f"{prefix}{number}"
    elif 10 ** 3 <= number < 10 ** 6:
        number = number / 10 ** 3
        if number.is_integer(): number = int(number)
        return f"{prefix}{number}k"
    elif number >= 10 ** 6:
        number = number / 10 ** 6
        if number.is_integer(): number = int(number)
        return f"{prefix}{number}m"

def unshorthand(short):
    short = short.strip().lower()
    try:
        if short.endswith("k"):
            return int(float(short[:-1]) * 10**3)
        elif short.endswith("m"):
            return int(float(short[:-1]) * 10**6)
        else:
            return int(float(short))
    except ValueError:
        return None

def get_line(csv_filename, n):
    with open(csv_filename, newline='', encoding='utf-8') as f:
        for i, row in enumerate(csv.reader(f), 1):
            if i == n:
                return row
    return []

def csv_len(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return sum(1 for _ in file)

def make_roads(filename):
    node_list = []
    for i in range(csv_len(filename)):
        name = get_line(filename,i+1)[0]
        road_type = get_line(filename,i+1)[1]
        if road_type == "ringroad":
            radius = int(unshorthand(get_line(filename,i+1)[2]))
            node_list.append([(name, radius), (radius,radius), (radius,-radius)])
            node_list.append([(name, radius), (radius,-radius), (-radius,-radius)])
            node_list.append([(name, radius), (-radius,-radius), (-radius,radius)])
            node_list.append([(name, radius), (-radius,radius), (radius,radius)])
        elif road_type == "diamond":
            radius = int(unshorthand(get_line(filename,i+1)[2]))
            node_list.append([(name, radius), (0,radius), (radius,0)])
            node_list.append([(name, radius), (radius,0), (0,-radius)])
            node_list.append([(name, radius), (0,-radius), (-radius,0)])
            node_list.append([(name, radius), (-radius,0), (0,radius)])
        elif road_type == "grid":
            length = int(unshorthand(get_line(filename,i+1)[2]))
            offset = int(unshorthand(get_line(filename,i+1)[3]))
            node_list.append([(name, offset), (-offset,-length), (-offset,length)])
            node_list.append([(name, offset), (-length,offset), (length,offset)])
            node_list.append([(name, offset), (offset,length), (offset,-length)])
            node_list.append([(name, offset), (length,-offset), (-length,-offset)])
        elif road_type == "highway":
            length = int(unshorthand(get_line(filename,i+1)[4]))
            cases = {'-': -1, '+': 1, '0': 0}
            x_end = cases.get(get_line(filename,i+1)[2])*length
            z_end = cases.get(get_line(filename,i+1)[3])*length
            node_list.append([(name, length), (0,0), (x_end, z_end)])
    return node_list