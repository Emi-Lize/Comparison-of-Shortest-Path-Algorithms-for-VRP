import random
import tkinter as tk
import time
from string import ascii_uppercase, ascii_lowercase
import numpy as np


class Receiver:
    def __init__(self, place):
        self.x = random.randint(100, 1200)
        self.y = random.randint(100, 700)
        self.name = place
        self.id = 0

    def draw(self, canvas):
        r = 15
        x0 = self.x - r
        y0 = self.y - r
        x1 = self.x + r
        y1 = self.y + r
        self.id = canvas.create_rectangle(x0, y0, x1, y1, fill="red", width=2, tags=("person",))
        canvas.create_text(self.x, self.y, text=self.name, font="bold")

    def visited(self, canvas):
        canvas.itemconfig(self.id, fill="grey")


class Sender:
    def __init__(self, place):
        self.x = random.randint(100, 1200)
        self.y = random.randint(100, 700)
        self.name = place
        self.id = 0

    def draw(self, canvas):
        r = 15
        x0 = self.x - r
        y0 = self.y - r
        x1 = self.x + r
        y1 = self.y + r
        self.id = canvas.create_rectangle(x0, y0, x1, y1, fill="green", width=2, tags=("person",))
        canvas.create_text(self.x, self.y, text=self.name, font="bold")

    def visited(self, canvas):
        canvas.itemconfig(self.id, fill="grey")


class Parcel:
    def __init__(self, receiver, noOfNodes):
        self.distance = 0
        self.deadline = noOfNodes * 30
        self.receiver = receiver


class Driver:
    def __init__(self):
        self.x = random.randint(100, 1200)
        self.y = random.randint(100, 700)
        self.move_x = 0
        self.move_y = 0
        self.id = 0
        self.name = "Driver"
        self.move_id = 0

    def draw(self, canvas):
        r = 15
        x0 = self.x - r
        y0 = self.y - r
        x1 = self.x + r
        y1 = self.y + r
        self.id = canvas.create_oval(x0, y0, x1, y1, fill="yellow", width=2, tags=("driver",))

    def move(self, x, y, canvas):
        self.move_x = x
        self.move_y = y
        r = 15
        x0 = self.move_x - r
        y0 = self.move_y - r
        x1 = self.move_x + r
        y1 = self.move_y + r

        if self.move_id == 0:
            canvas.itemconfig(self.id, fill="black")
            self.move_id = canvas.create_oval(x0, y0, x1, y1, fill="yellow", width=2, tags=("move",))
        else:
            canvas.delete(self.move_id)
            self.move_id = canvas.create_oval(x0, y0, x1, y1, fill="yellow", width=2, tags=("move",))

    def redraw(self):
        self.move_id = 0
        self.move_x = 0
        self.move_y = 0


class Path:
    def __init__(self, startPoint, endPoint):
        self.start = startPoint
        self.end = endPoint
        self.distance = int(euclidean(startPoint, endPoint) / 10)

    def draw(self, canvas):
        canvas.create_line(self.start.x, self.start.y, self.end.x, self.end.y, width=1, tags=("path",))
        centre_x = (self.start.x + self.end.x) / 2
        centre_y = (self.start.y + self.end.y) / 2
        canvas.create_text(centre_x, centre_y, text=self.distance, tags=("distance",))
        canvas.tag_raise("distance")
        canvas.tag_lower("path")


class Text:
    def __init__(self):
        self.total = 0
        self.x = 50
        self.y = 10
        self.id = 0
        self.parcel = []

    def draw(self, canvas, total, jobs):
        self.total += total
        if self.id == 0:
            self.id = canvas.create_text(self.x, self.y, text="Total Distance: " + str(self.total), tags=("text",))
        else:
            canvas.itemconfig(self.id, text="Total Distance: " + str(self.total))
        if self.parcel:
            for x in range(len(jobs)):
                if canvas.itemcget(self.parcel[x], 'text') == ascii_lowercase[x] + ": " + str(jobs[x]):
                    canvas.itemconfig(self.parcel[x], text=ascii_lowercase[x] + ": " + str(jobs[x]), fill="grey")
                else:
                    canvas.itemconfig(self.parcel[x], text=ascii_lowercase[x] + ": " + str(jobs[x]), fill="red")
        else:
            for x in range(len(jobs)):
                self.parcel.append(self.draw_parcel(canvas, x, jobs[x]))

    def draw_parcel(self, canvas, idx, value):
        return canvas.create_text(self.x, self.y + (idx + 1) * 20, text=ascii_lowercase[idx] + ": " + str(value),
                                  fill="black", tags=("text",))


def heuristic(node, join_list):
    h = {}
    for x in join_list:
        h[x] = int(euclidean(node, x) / 10)
    return h


def a_star(path_list, receiver_list, sender_list, driver):
    start = time.time()
    waiting_time = 0
    sequence = [driver]
    node_list = []
    parcel_list = []
    job_text = [0] * len(receiver_list)
    job_text_list = [job_text.copy()]
    text_list = [0]
    sent = []
    join_list = sender_list + receiver_list + [driver]
    job_list = sender_list.copy()
    job_distance = {}
    current = driver
    while job_list:
        initial = current
        path_travel = {}
        for goal_node in job_list:
            current = initial
            visited = [current]
            unvisited = join_list.copy()
            unvisited.remove(current)
            h = heuristic(goal_node, join_list)
            path_travel[goal_node] = []
            g = {current: 0}
            f = {}
            previous = {}
            while unvisited:
                neighbours = []
                for x in path_list:
                    if x.start == current:
                        neighbours.append([x.end, x.distance])
                    elif x.end == current:
                        neighbours.append([x.start, x.distance])
                for (node, dist) in neighbours:
                    if node in unvisited:
                        if node not in g:
                            g[node] = dist + g[current]
                            f[node] = g[node] + h[node]
                            previous[node] = current
                        else:
                            if dist + g[current] < g[node]:
                                g[node] = dist + g[current]
                                f[node] = g[node] + h[node]
                                previous[node] = current
                sorted_f = sorted(f.items(), key=lambda item: item[1])
                for x in sorted_f:
                    if x[0] in unvisited:
                        current = x[0]
                        break
                visited.append(current)
                unvisited.remove(current)
                if current == goal_node:
                    break
            visited.reverse()
            node = visited[0]
            while node != initial:
                idx = [i for i, x in enumerate(visited) if x == previous[node]][0]
                for path in path_list:
                    if (path.start == node and path.end == visited[idx]) or (
                            path.end == node and path.start == visited[idx]):
                        path_travel[goal_node].append(path)
                        break
                node = previous[node]
            job_distance[goal_node] = g[goal_node]
        sorted_job = dict(sorted(job_distance.items(), key=lambda item: item[1]))
        current = next(iter(sorted_job))
        parcel_list.sort(key=lambda x: x.deadline)
        for parcel in parcel_list:
            if parcel.distance + sorted_job[parcel.receiver] >= parcel.deadline:
                current = parcel.receiver
                break
        else:
            if parcel_list:
                dict_list = list(sorted_job.items())
                for i in range(len(dict_list) - 1):
                    if dict_list[i][1] == dict_list[i + 1][1]:
                        if any(x.receiver == dict_list[i + 1][0] for x in parcel_list):
                            if isinstance(dict_list[i][0], Sender):
                                dict_list[i], dict_list[i + 1] = dict_list[i + 1], dict_list[i]
                            elif any(x.receiver == dict_list[i][0] for x in parcel_list):
                                node1 = [node for node in parcel_list if node.receiver == dict_list[i][0]][0]
                                node2 = [node for node in parcel_list if node.receiver == dict_list[i + 1][0]][0]
                                if (node1.deadline - node1.distance) > (node2.deadline - node2.distance):
                                    dict_list[i], dict_list[i + 1] = dict_list[i + 1], dict_list[i]
                sorted_job = dict(dict_list)
            for i in sorted_job:
                if isinstance(i, Receiver) or isinstance(i, Sender):
                    if i in job_list:
                        current = i
                        break
        sent.append(0)
        if len(path_travel[current]) > 1:
            for path in path_travel[current]:
                if path.start == initial:
                    current = path.end
                    text_list.append(path.distance)
                    break
                elif path.end == initial:
                    current = path.start
                    text_list.append(path.distance)
                    break
        else:
            text_list.append(path_travel[current][0].distance)
        node_list.append(current)
        if isinstance(current, Sender) and current in job_list:
            job_list.remove(current)
            job_list.append(receiver_list[sender_list.index(current)])
            parcel = Parcel(receiver_list[sender_list.index(current)], len(receiver_list))
            parcel_list.append(parcel)
        if parcel_list:
            for parcel in parcel_list:
                i = [i for i, node in enumerate(receiver_list) if node == parcel.receiver][0]
                job_text[i] = int(parcel.deadline - parcel.distance)
                parcel.distance += text_list[-1]
        job_text_list.append(job_text.copy())
        if current in job_list and isinstance(current, Receiver):
            job_list.remove(current)
            idx = [i for i, x in enumerate(parcel_list) if x.receiver == current][0]
            waiting_time += parcel_list[idx].distance
            del parcel_list[idx]
            sent.pop()
            sent.append(1)
    for i, node in enumerate(node_list):
        if sent[i] == 1:
            sequence.append([node, True])
        else:
            sequence.append(node)
    print("Runtime:", (time.time() - start) * 1000)
    return sequence, text_list, job_text_list, waiting_time


def dijkstra_min_distance(name, distance, distance_list, path_sum):
    replace = False
    idx = [i for i, node in enumerate(distance_list) if node[0].name == name][0]
    possible = distance + path_sum
    if possible < distance_list[idx][1]:
        distance_list[idx][1] = possible
        replace = True
    return distance_list, replace, idx


def dijkstra(path_list, receiver_list, sender_list, driver):
    start = time.time()
    waiting_time = 0
    sequence = [driver]
    sent = []
    join_list = sender_list + receiver_list + [driver]
    job_list = sender_list.copy()
    current = driver
    parcel_list = []
    node_list = []
    text_list = [0]
    job_text = [0] * len(receiver_list)
    job_text_list = [job_text.copy()]
    while job_list:
        initial = current
        unvisited = join_list.copy()
        distance_list = np.full((len(join_list), 2), np.inf, dtype=object)
        for x in range(len(receiver_list)):
            distance_list[x][0] = sender_list[x]
            distance_list[len(sender_list) + x][0] = receiver_list[x]
        distance_list[-1][0] = driver
        unvisited.remove(current)
        path_sum = 0
        path_checked = np.copy(distance_list)
        for i in path_checked:
            i[1] = []
        current_path = []
        while unvisited:
            for path in path_list:
                replace = False
                if path.start == current:
                    distance_list, replace, idx = dijkstra_min_distance(path.end.name, path.distance,
                                                                        distance_list,
                                                                        path_sum)
                elif path.end == current:
                    distance_list, replace, idx = dijkstra_min_distance(path.start.name, path.distance,
                                                                        distance_list,
                                                                        path_sum)
                if replace:
                    path_checked[idx][1].clear()
                    if current_path:
                        path_checked[idx][1] = current_path + [path]
                    else:
                        path_checked[idx][1].append(path)

            minimum = sorted(distance_list, key=lambda x: x[1])
            for i in minimum:
                if i[0] in unvisited:
                    current = i[0]
                    path_sum = i[1]
                    unvisited.remove(current)
                    idx = [i for i, node in enumerate(path_checked) if node[0] == current][0]
                    current_path = path_checked[idx][1]
                    break
        parcel_list.sort(key=lambda x: x.deadline)
        for parcel in parcel_list:
            idx = [i for i, node in enumerate(distance_list) if node[0] == parcel.receiver][0]
            if parcel.distance + distance_list[idx][1] >= parcel.deadline:
                current = parcel.receiver
                break
        else:
            if parcel_list:
                for i in range(len(minimum) - 1):
                    if minimum[i][1] == minimum[i + 1][1]:
                        if any(x.receiver == minimum[i + 1][0] for x in parcel_list):
                            if isinstance(minimum[i][0], Sender):
                                minimum[i], minimum[i + 1] = minimum[i + 1], minimum[i]
                            elif any(x.receiver == minimum[i][0] for x in parcel_list):
                                node1 = [node for node in parcel_list if node.receiver == minimum[i][0]][0]
                                node2 = [node for node in parcel_list if node.receiver == minimum[i + 1][0]][0]
                                if (node1.deadline - node1.distance) > (node2.deadline - node2.distance):
                                    minimum[i], minimum[i + 1] = minimum[i + 1], minimum[i]
            for i in minimum:
                if isinstance(i[0], Receiver) or isinstance(i[0], Sender):
                    if i[0] in job_list:
                        current = i[0]
                        break
        sent.append(0)
        idx = [i for i, node in enumerate(path_checked) if node[0] == current][0]
        if len(path_checked[idx][1]) > 1:
            for path in path_checked[idx][1]:
                if path.start == initial:
                    current = path.end
                    text_list.append(path.distance)
                    break
                elif path.end == initial:
                    current = path.start
                    text_list.append(path.distance)
                    break
        else:
            text_list.append(path_checked[idx][1][0].distance)

        node_list.append(current)
        if isinstance(current, Sender) and current in job_list:
            job_list.remove(current)
            job_list.append(receiver_list[sender_list.index(current)])
            parcel = Parcel(receiver_list[sender_list.index(current)], len(receiver_list))
            parcel_list.append(parcel)
        idx = [i for i, node in enumerate(distance_list) if node[0] == current][0]
        if parcel_list:
            for parcel in parcel_list:
                i = [i for i, node in enumerate(receiver_list) if node == parcel.receiver][0]
                job_text[i] = int(parcel.deadline - parcel.distance)
                parcel.distance += distance_list[idx][1]
        job_text_list.append(job_text.copy())
        if current in job_list and isinstance(current, Receiver):
            job_list.remove(current)
            idx = [i for i, x in enumerate(parcel_list) if x.receiver == current][0]
            waiting_time += parcel_list[idx].distance
            del parcel_list[idx]
            sent.pop()
            sent.append(1)

    for i, node in enumerate(node_list):
        if sent[i] == 1:
            sequence.append([node, True])
        else:
            sequence.append(node)
    print("Runtime:", (time.time() - start) * 1000)
    return sequence, text_list, job_text_list, waiting_time


def random_walk(path_list, receiver_list, sender_list, driver):
    waiting_time = 0
    parcel_list = []
    sent = []
    node_list = []
    job_list = sender_list.copy()
    current = driver
    sequence = [driver]
    text_list = [0]
    job_text = [0] * len(receiver_list)
    job_text_list = [job_text.copy()]
    while job_list:
        neighbours = []
        for x in path_list:
            if x.start == current:
                neighbours.append([x.end, x.distance])
            elif x.end == current:
                neighbours.append([x.start, x.distance])
        neighbour_job = [x for x in neighbours if x[0] in job_list]
        if neighbour_job:
            job = random.choice(neighbour_job)
        else:
            job = random.choice(neighbours)

        sent.append(0)
        current = job[0]
        text_list.append(job[1])

        node_list.append(current)
        if isinstance(current, Sender) and current in job_list:
            job_list.remove(current)
            job_list.append(receiver_list[sender_list.index(current)])
            parcel = Parcel(receiver_list[sender_list.index(current)], len(receiver_list))
            parcel_list.append(parcel)
        if parcel_list:
            for parcel in parcel_list:
                i = [i for i, node in enumerate(receiver_list) if node == parcel.receiver][0]
                job_text[i] = int(parcel.deadline - parcel.distance)
                parcel.distance += job[1]
        job_text_list.append(job_text.copy())
        if current in job_list and isinstance(current, Receiver):
            job_list.remove(current)
            idx = [i for i, x in enumerate(parcel_list) if x.receiver == current][0]
            waiting_time += parcel_list[idx].distance
            del parcel_list[idx]
            sent.pop()
            sent.append(1)

    for i, node in enumerate(node_list):
        if sent[i] == 1:
            sequence.append([node, True])
        else:
            sequence.append(node)
    return sequence, text_list, job_text_list, waiting_time


def create(canvas, noOfNodes):
    receiver_list = []
    sender_list = []
    for x in range(noOfNodes):
        receiver = Receiver(ascii_lowercase[x])
        receiver.draw(canvas)
        receiver_list.append(receiver)
    for x in range(noOfNodes):
        sender = Sender(ascii_uppercase[x])
        sender.draw(canvas)
        sender_list.append(sender)
    driver = Driver()
    driver.draw(canvas)
    place_list = receiver_list + sender_list
    place_list.append(driver)
    path_list = create_main_path(place_list, canvas)
    text = Text()
    return path_list, receiver_list, sender_list, driver, text


def create_main_path(join_list, canvas):
    path_list = []
    start = join_list[random.randint(0, len(join_list) - 1)]
    while True:
        object_id = []
        end = join_list[random.randint(0, len(join_list) - 1)]
        if start != end:
            if not any(x.start == start and x.end == end for x in path_list) and not any(
                    x.start == end and x.end == start for x in path_list):
                objects = canvas.find_overlapping(start.x, start.y, end.x, end.y)
                for i in objects:
                    if canvas.itemcget(i, "tags") == "person" or canvas.itemcget(i, "tags") == "driver":
                        if i == start.id or i == end.id:
                            pass
                        else:
                            object_id.append(i)
                if not object_id:
                    path = Path(start, end)
                    path.draw(canvas)
                    path_list.append(path)
                else:
                    object_id.append(end.id)
                    object_list = (x for x in join_list if x.id in object_id)
                    object_list = sorted(object_list, key=lambda e: euclidean(e, start))
                    for i in object_list:
                        if path_list:
                            if any(x.start == start and x.end == i for x in path_list) or any(
                                    x.start == i and x.end == start for x in path_list):
                                pass
                            else:
                                path = Path(start, i)
                                path.draw(canvas)
                                path_list.append(path)
                        else:
                            path = Path(start, i)
                            path.draw(canvas)
                            path_list.append(path)
                        start = i
        path_node = []
        next_list = [start]
        hold = next_list.copy()
        for node in hold:
            if node not in path_node:
                path_node.append(node)
                for x in path_list:
                    if x.start == node:
                        hold.append(x.end)
                    elif x.end == node:
                        hold.append(x.start)
        if len(path_node) == len(join_list):
            break
        nodes_left = [x for x in join_list if x not in path_node]
        start = nodes_left[random.randint(0, len(nodes_left) - 1)]

    return create_sub_path(join_list, path_list, canvas)


def create_sub_path(join_list, path_list, canvas):
    for x in range(random.randint(0, len(join_list))):
        object_id = []
        start = join_list[random.randint(0, len(join_list) - 1)]
        end = join_list[random.randint(0, len(join_list) - 1)]
        if start != end:
            if not any(x.start == start and x.end == end for x in path_list) and not any(
                    x.start == end and x.end == start for x in path_list):
                objects = canvas.find_overlapping(start.x, start.y, end.x, end.y)
                for i in objects:
                    if canvas.itemcget(i, "tags") == "person" or canvas.itemcget(i, "tags") == "driver":
                        if i == start.id or i == end.id:
                            pass
                        else:
                            object_id.append(i)
                if not object_id:
                    path = Path(start, end)
                    path.draw(canvas)
                    path_list.append(path)
                    start = end

                else:
                    object_id.append(end.id)
                    object_list = (x for x in join_list if x.id in object_id)
                    object_list = sorted(object_list, key=lambda e: euclidean(e, start))
                    for i in object_list:
                        if any(x.start == start and x.end == i for x in path_list) or any(
                                x.start == i and x.end == start for x in path_list):
                            pass
                        else:
                            path = Path(start, i)
                            path.draw(canvas)
                            path_list.append(path)
                        start = i

    return path_list


def euclidean(p1, p2):
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5


def redraw(canvas, receiver_list, sender_list, driver):
    for receiver in receiver_list:
        receiver.draw(canvas)
    for sender in sender_list:
        sender.draw(canvas)
    driver.redraw()
    driver.draw(canvas)
    text = Text()
    return text


def run(algorithm, driver, canvas, text, nodes):
    sequence, text_list, job_text, waiting = algorithm
    avg_waiting = waiting / nodes
    animate(driver, sequence, canvas, text, text_list, job_text)
    print("\nTotal distance travelled:", text.total)
    print("Average waiting time:", avg_waiting)


def animate(driver, sequence, canvas, text, text_list, job_text):
    i = 0
    print("Order:", end=' ')
    for node in sequence:
        if node != driver:
            if isinstance(node, list):
                node[0].visited(canvas)
            elif isinstance(node, Sender):
                node.visited(canvas)
        if isinstance(node, list):
            driver.move(node[0].x, node[0].y, canvas)
            print(node[0].name, end=' ')
        else:
            driver.move(node.x, node.y, canvas)
            print(node.name, end=' ')
        text.draw(canvas, text_list[i], job_text[i])
        canvas.update()
        canvas.after(250)
        i += 1
    calculate_result(text, canvas)
    canvas.delete("person", "text", "move")


def calculate_result(text, canvas):
    print("\nDeadline left:")
    for i in range(len(text.parcel)):
        print(canvas.itemcget(text.parcel[i], 'text'))


def main():
    window = tk.Tk()
    canvas = tk.Canvas(window, height=800, width=1300)
    noOfNodes = 5
    path_list, receiver_list, sender_list, driver, text = create(canvas, noOfNodes)
    canvas.pack()

    print("Dijkstra")
    run(dijkstra(path_list, receiver_list, sender_list, driver), driver, canvas, text, noOfNodes)

    print("\nA* Search")
    text = redraw(canvas, receiver_list, sender_list, driver)
    run(a_star(path_list, receiver_list, sender_list, driver), driver, canvas, text, noOfNodes)

    print("\nRandom Walk")
    text = redraw(canvas, receiver_list, sender_list, driver)
    run(random_walk(path_list, receiver_list, sender_list, driver), driver, canvas, text, noOfNodes)

    window.destroy()
    window.mainloop()


noOfRun = 10
for x in range(noOfRun):
    print("Run", x + 1)
    main()
    print("\n")
