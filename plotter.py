import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import mplcursors
from csvparser import make_nodes

bounds = 50000

def plot_roads(nodes_list=None, csv_file=None):
    if nodes_list is None and csv_file is None:
        csv_file = "2b2t.csv"

    fig, ax = plt.subplots(figsize=(12, 12))

    if csv_file:
        nodes_list = make_nodes(csv_file)

    roads_by_name = {}

    for node in nodes_list:
        name, radius = node[0]
        if name not in roads_by_name:
            roads_by_name[name] = []

        points = node[1:]
        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points]

        line, = ax.plot(x_coords, [-y for y in y_coords], color="black", linewidth=1)

        line.road_info = {
            'name': name,
        }

    plt.title('2B2T ROADMAP')
    plt.grid(True)
    ax.set_aspect('equal')

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{int(-y):,}'))

    cursor = mplcursors.cursor(ax.lines)

    @cursor.connect("add")
    def on_add(sel):
        road_info = sel.artist.road_info
        sel.annotation.set(text=f"Road: {road_info['name']}")
        sel.annotation.get_bbox_patch().set(fc="white", alpha=0.8)

    plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    plt.axvline(x=0, color='gray', linestyle='--', alpha=0.5)

    plt.axis([-bounds, bounds, -bounds, bounds])
    plt.show()

if __name__ == "__main__":
    plot_roads(csv_file="2b2t.csv")