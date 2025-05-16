import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import mplcursors
from csvparser import make_roads, shorthand
from pathfinder import *

bounds = 30 * 10 ** 6 / 8

def plot(csv_file, start_point, end_point):
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='#37474F')
    ax.set_facecolor("#6e0000")
    roads_by_name = {}
    all_segments = []

    for node in make_roads(csv_file):
        name, radius = node[0]
        if name not in roads_by_name:
            roads_by_name[name] = []

        points = node[1:]
        x_coords = [p[0] for p in points]
        z_coords = [p[1] for p in points]

        line, = ax.plot(x_coords, [-z for z in z_coords], color="black", linewidth=1)
        line.road_info = {
            'name': name,
        }

        for i in range(len(points) - 1):
            all_segments.append((points[i], points[i + 1]))

    segments = resplice(resplice(splice_nodes(all_segments), start_point), end_point)
    path = find_shortest_path(segments, start_point, end_point)

    if path:
        path_x = [p[0] for p in path]
        path_z = [-p[1] for p in path]
        ax.plot(path_x, path_z, color="blue", linewidth=2, zorder=10)

        ax.scatter([start_point[0]], [-start_point[1]], color="green", s=50, zorder=20)
        ax.scatter([end_point[0]], [-end_point[1]], color="red", s=50, zorder=20)

    ax.set_aspect('equal')
    ax.tick_params(colors='#B0BEC5')

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{shorthand(int(x))}'))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{shorthand(int(-y))}'))

    cursor = mplcursors.cursor(ax.lines)

    @cursor.connect("add")
    def on_add(sel):
        if hasattr(sel.artist, 'road_info'):
            road_info = sel.artist.road_info
            x, y = sel.target[0], -sel.target[1]
            closest = find_closest_point(segments, x, -y, width=2*int(plt.gca().get_xlim()[1]))
            sel.annotation.set(text=f"Road: {road_info['name']}\n{shorthand(int(closest[0]))}, {shorthand(int(closest[1]))}")
            sel.annotation.get_bbox_patch().set(fc="white", alpha=0.8)

    plt.axis([-bounds, bounds, -bounds, bounds])

    fig.canvas.mpl_connect('scroll_event', lambda event: zoom_with_mouse(event, ax))
    plt.get_current_fig_manager().toolbar.pan()
    plt.show()

def zoom_with_mouse(event, ax):
    factor = 0.95 if event.button == 'up' else 1.05
    cur_xlim = ax.get_xlim()
    cur_ylim = ax.get_ylim()
    x_data = event.xdata
    y_data = event.ydata
    x_left = x_data - factor * (x_data - cur_xlim[0])
    x_right = x_data + factor * (cur_xlim[1] - x_data)
    y_bottom = y_data - factor * (y_data - cur_ylim[0])
    y_top = y_data + factor * (cur_ylim[1] - y_data)
    ax.set_xlim([x_left, x_right])
    ax.set_ylim([y_bottom, y_top])
    ax.figure.canvas.draw_idle()

if __name__ == "__main__":
    start_point = (423456, 2860000)
    end_point = (-98743, 1230000)
    plot("2b2t.csv", start_point, end_point)
