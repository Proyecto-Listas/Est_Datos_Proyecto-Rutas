import random
import math
import matplotlib.pyplot as plt

class Node:
    def __init__(self, id, x, y, package_weight=1.0, has_order=True):
        self.id = id
        self.x = x
        self.y = y
        self.package_weight = package_weight
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
                    dist = math.hypot(u.x - v.x, u.y - v.y)
                    #se están agregando todos los vertices dos veces :/
                    self.edges.add((u, v))
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
            print(i)
            print(tour[i])
            print(tour[i+1])
            total += self.get_weight(tour[i], tour[i+1])
        return total

    def adjust_route(self, tour, cancelled_node, start):
        idx = tour.index(cancelled_node)
        prev = tour[idx-1]
        tail = tour[idx+1:-1]
        remaining = [n for n in tail if n.has_order] #
        new_tour = tour[:idx]
        current = prev
        while remaining:
            next_node = min(remaining, key=lambda v: self.get_weight(current, v))
            if next_node == remaining[0]:
                new_tour+=remaining
                break
            elif next_node==remaining[-2]:
                new_tour+=reversed(remaining)
                break
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

    def plan_routes(self, start, max_distance=None, max_weight=None, max_volume=None):
        #active = [n for n in self.vertices if n.has_order]#
        total_weight=0
        total_volume=0
        dist=0
        unvisited=set()
        for v in self.vertices:
            if v.has_order:
                total_weight += v.package_weight
                total_volume +=1
                dist = self.tour_length(self.nearest_neighbor(start))
                unvisited.add(v)
        l_w = math.ceil(total_weight / max_weight) if max_weight else 1
        l_v = math.ceil(total_volume / max_volume) if max_volume else 1
        l_d = math.ceil(dist / max_distance) if max_distance else 1
        k = max(l_w, l_v, l_d)
        routes = []
        for _ in range(k):
            routes.append({'tour':[start], 'distance':0.0, 'weight':0.0, 'volume':0, 'current':start})
        for r in routes:
            if not unvisited: break
            first = min(unvisited, key=lambda n: self.get_weight(start, n))
            dist_to = self.get_weight(start, first)
            ret = self.get_weight(first, start)
            if ((not max_distance or dist_to + ret <= max_distance) and
                (not max_weight or first.package_weight <= max_weight) and
                (not max_volume or 1 <= max_volume)):
                r['tour'].append(first)
                r['distance'] += dist_to
                r['weight'] += first.package_weight
                r['volume'] += 1
                r['current'] = first
                unvisited.remove(first)
        idx = 0
        while unvisited:
            r = routes[idx % len(routes)]
            curr = r['current']
            feas = []
            for n in unvisited:
                d = self.get_weight(curr, n)
                ret = self.get_weight(n, start)
                if ((not max_distance or r['distance'] + d + ret <= max_distance) and
                    (not max_weight or r['weight'] + n.package_weight <= max_weight) and
                    (not max_volume or r['volume'] + 1 <= max_volume)):
                    feas.append((n, d))
            if feas:
                n, d = min(feas, key=lambda x: x[1])
                r['tour'].append(n)
                r['distance'] += d
                r['weight'] += n.package_weight
                r['volume'] += 1
                r['current'] = n
                unvisited.remove(n)
            else:
                r['tour'].append(start)
                r['distance'] += self.get_weight(r['current'], start)
                if all(
                    not any(
                        (not max_distance or other['distance'] + self.get_weight(other['current'], n) + self.get_weight(n,start) <= max_distance) and
                        (not max_weight or other['weight'] + n.package_weight <= max_weight) and
                        (not max_volume or other['volume'] + 1 <= max_volume)
                    for other in routes)
                    for n in unvisited
                ):
                    routes.append({'tour':[start], 'distance':0.0, 'weight':0.0, 'volume':0, 'current':start})
                idx += 1
                continue
            idx += 1
        for r in routes:
            if r['tour'][-1] != start:
                r['tour'].append(start)
                r['distance'] += self.get_weight(r['current'], start)
        return routes

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

    def plot_route(self, route, title):
        tour = route['tour']
        xs = [node.x for node in tour]
        ys = [node.y for node in tour]
        fig, ax = plt.subplots()
        ax.scatter([n.x for n in self.vertices if n.has_order],
                   [n.y for n in self.vertices if n.has_order], s=50, label='Activo')
        ax.scatter([n.x for n in self.vertices if not n.has_order],
                   [n.y for n in self.vertices if not n.has_order], s=50, label='Inactivo', alpha=0.3)
        for n in self.vertices:
            ax.text(n.x, n.y, n.id)
        ax.plot(xs, ys, linestyle='-', marker='o', label=title)
        ax.set_title(title)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.legend()
        plt.grid(True)
        plt.show()

    def plot_all_routes(self, routes):
        colors = plt.cm.get_cmap('tab10', len(routes))
        fig, ax = plt.subplots()
        ax.scatter([n.x for n in self.vertices if n.has_order],
                   [n.y for n in self.vertices if n.has_order], s=50, label='Activo')
        ax.scatter([n.x for n in self.vertices if not n.has_order],
                   [n.y for n in self.vertices if not n.has_order], s=50, label='Inactivo', alpha=0.3)
        for n in self.vertices:
            ax.text(n.x, n.y, n.id)
        for idx, r in enumerate(routes):
            tour = r['tour']
            xs = [node.x for node in tour]
            ys = [node.y for node in tour]
            ax.plot(xs, ys, linestyle='-', marker='o', color=colors(idx), label=f'Ruta {idx+1}')
        ax.set_title('Todas las Rutas en un Gráfico')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
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
        nodes.append(Node(str(i), x, y, package_weight=random.uniform(1,2)))

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
    print(new_tour)
    for node in new_tour:
        print(node.id)
    new_length = g.tour_length(new_tour)
    print('Ajustado:', [n.id for n in new_tour], new_length)
    g.plot_tour(new_tour, title_suffix=' (ajustada)')

    routes = g.plan_routes(start, max_distance=200, max_weight=10, max_volume=5)
    for idx, r in enumerate(routes,1):
        print(f"Ruta {idx}: {[n.id for n in r['tour']]} distancia={r['distance']:.1f} peso={r['weight']:.1f} vol={r['volume']}")
        g.plot_route(r, title=f"Ruta {idx}")

    g.plot_all_routes(routes)
