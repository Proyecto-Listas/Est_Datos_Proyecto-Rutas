import random
import math
import matplotlib.pyplot as plt

class Node:
    def __init__(self, id, x, y, has_order=True):
        self.id = id
        self.x = x
        self.y = y
        self.has_order = has_order
    def __hash__(self):
        return hash(self.id)
    def __eq__(self, other):
        return isinstance(other, Node) and self.id == other.id

class Graph:
    def __init__(self, vertices=None):
        self.vertices = set(vertices) if vertices else set()
        self.edges = set()
        self.weight = set()
        if vertices:
            self._build_full_graph()

    def _build_full_graph(self):
        self.edges.clear()
        self.weight.clear()
        for u in self.vertices:
            for v in self.vertices:
                if u != v:
                    self.edges.add((u, v))
                    dx = u.x - v.x
                    dy = u.y - v.y
                    dist = math.hypot(dx, dy)
                    self.weight.add(((u, v), dist))

    def add_node(self, node):
        for u in self.vertices:
            self.edges.add((u, node))
            self.edges.add((node, u))
            dx = u.x - node.x
            dy = u.y - node.y
            dist = math.hypot(dx, dy)
            self.weight.add(((u, node), dist))
            self.weight.add(((node, u), dist))
        self.vertices.add(node)

    def remove_node(self, node):
        if node in self.vertices:
            self.vertices.remove(node)
            to_remove = {e for e in self.edges if node in e}
            self.edges -= to_remove
            self.weight = {w for w in self.weight if w[0][0] != node and w[0][1] != node}

    def get_weight(self, u, v):
        for (edge, w) in self.weight:
            if edge == (u, v):
                return w
        raise KeyError(f"Weight for edge {(u, v)} not found")

    def nearest_neighbor(self, start):
        unvisited = {n for n in self.vertices if n.has_order}
        if start not in unvisited:
            unvisited.add(start)
        tour = [start]
        current = start
        unvisited.remove(start)
        while unvisited:
            next_node = min(unvisited, key=lambda v: self.get_weight(current, v))
            tour.append(next_node)
            unvisited.remove(next_node)
            current = next_node
        tour.append(start)
        return tour

    def tour_length(self, tour):
        total = 0
        for i in range(len(tour) - 1):
            total += self.get_weight(tour[i], tour[i+1])
        return total

    def adjust_route(self, tour, cancelled_node, start):
        idx = tour.index(cancelled_node)
        prev = tour[idx-1]
        tail = tour[idx+1:-1]
        remaining = [n for n in tail if n.has_order]
        new_tour = tour[:idx]
        current = prev
        while remaining:
            next_node = min(remaining, key=lambda v: self.get_weight(current, v))
            new_tour.append(next_node)
            remaining.remove(next_node)
            current = next_node
        new_tour.append(start)
        return new_tour

    def plot_tour(self, tour, title_suffix=''):
        xs = [node.x for node in tour]
        ys = [node.y for node in tour]
        fig, ax = plt.subplots()
        ax.scatter([n.x for n in self.vertices if n.has_order],
                   [n.y for n in self.vertices if n.has_order], s=50, label='Activo')
        ax.scatter([n.x for n in self.vertices if not n.has_order],
                   [n.y for n in self.vertices if not n.has_order], s=50, label='Inactivo', alpha=0.3)
        for n in self.vertices:
            ax.text(n.x, n.y, n.id)
        ax.plot(xs, ys, linestyle='-', marker='o', label='Ruta')
        ax.set_title(f'Ruta del Dron (NN){title_suffix}')
        ax.set_xlabel('Coordenada X')
        ax.set_ylabel('Coordenada Y')
        ax.legend()
        plt.grid(True)
        plt.show()

    def plot_full_graph(self):
        fig, ax = plt.subplots()
        for (u, v) in self.edges:
            ax.plot([u.x, v.x], [u.y, v.y], color='lightgray', linewidth=0.5)
        ax.scatter([n.x for n in self.vertices if n.has_order],
                   [n.y for n in self.vertices if n.has_order], s=50, label='Activo')
        ax.scatter([n.x for n in self.vertices if not n.has_order],
                   [n.y for n in self.vertices if not n.has_order], s=50, label='Inactivo', alpha=0.3)
        for n in self.vertices:
            ax.text(n.x, n.y, n.id)
        ax.set_title('Grafo Completo')
        ax.set_xlabel('Coordenada X')
        ax.set_ylabel('Coordenada Y')
        ax.legend()
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    nodes = []
    base = Node("0", 0, 0, has_order=False)
    nodes.append(base)
    for i in range(1, 15):
        x = random.randint(-20, 20)
        y = random.randint(-20, 20)
        nodes.append(Node(str(i), x, y))

    g = Graph(nodes)
    start = base

    g.plot_full_graph()

    tour = g.nearest_neighbor(start)
    length = g.tour_length(tour)
    print('Inicial:', [n.id for n in tour], length)
    g.plot_tour(tour)

    cancelled = random.choice([n for n in nodes if n != base])
    cancelled.has_order = False
    print('Cancelado:', cancelled.id)

    new_tour = g.adjust_route(tour, cancelled, start)
    new_length = g.tour_length(new_tour)
    print('Ajustado:', [n.id for n in new_tour], new_length)
    g.plot_tour(new_tour, title_suffix=' (ajustada)')
