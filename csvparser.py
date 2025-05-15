import csv

def shorthand(number):
    if int(number) != number:
        return None
    if number < 1000:
        return number
    elif number >= 10**3:
        number = number / 10**3
        if number.is_integer(): number = int(number)
        return f"{number}k"
    elif number >= (10**6):
        number = number / 10**6
        if number.is_integer(): number = int(number)
        return f"{number}m"


def unshorthand(shorthand):
    shorthand = shorthand.strip().lower()
    try:
        if shorthand.endswith("k"):
            return int(float(shorthand[:-1]) * 10**3)
        elif shorthand.endswith("m"):
            return int(float(shorthand[:-1]) * 10**6)
        else:
            return int(float(shorthand))
    except ValueError:
        return None

def get_line(csv_filename, n):
    with open(csv_filename, newline='', encoding='utf-8') as f:
        for i, row in enumerate(csv.reader(f), 1):
            if i == n:
                return row
    return []

def csv_len(filename):
    count = 0
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            count += 1
    return count

def sign_to_int(sign):
    return {'-': -1, '+': 1, '0': 0}.get(sign)

def make_nodes(filename):
    node_list = []
    for i in range(csv_len(filename)):
        name = get_line(filename,i+1)[0]
        if get_line(filename,i+1)[1] == "ringroad":
            radius = int(unshorthand(get_line(filename,i+1)[2]))
            node_list.append([(name, radius), (radius,radius), (radius,-radius)])
            node_list.append([(name, radius), (radius,-radius), (-radius,-radius)])
            node_list.append([(name, radius), (-radius,-radius), (-radius,radius)])
            node_list.append([(name, radius), (-radius,radius), (radius,radius)])
        elif get_line(filename,i+1)[1] == "diamond":
            radius = int(unshorthand(get_line(filename,i+1)[2]))
            node_list.append([(name, radius), (0,radius), (radius,0)])
            node_list.append([(name, radius), (radius,0), (0,-radius)])
            node_list.append([(name, radius), (0,-radius), (-radius,0)])
            node_list.append([(name, radius), (-radius,0), (0,radius)])
        elif get_line(filename,i+1)[1] == "grid":
            length = int(unshorthand(get_line(filename,i+1)[2]))
            offset = int(unshorthand(get_line(filename,i+1)[3]))
            node_list.append([(name, offset), (-offset,-length), (-offset,length)])
            node_list.append([(name, offset), (-length,offset), (length,offset)])
            node_list.append([(name, offset), (offset,length), (offset,-length)])
            node_list.append([(name, offset), (length,-offset), (-length,-offset)])
        elif get_line(filename,i+1)[1] == "highway":
            length = int(unshorthand(get_line(filename,i+1)[4]))
            x_end = sign_to_int(get_line(filename,i+1)[2])*length
            z_end = sign_to_int(get_line(filename,i+1)[3])*length
            node_list.append([(name, length), (0,0), (x_end, z_end)])
    return node_list