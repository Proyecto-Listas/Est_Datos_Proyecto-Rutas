#Realizado por:
#Daniver Franchesco Hernandez Acero 2240032
#Juan Manuel Nino Pina 2240040
#Juan Manuel Rivera Torres 2240046
#Luis Felipe Rueda Garcia 2240021
from operator import contains
import random
import math
from xml.etree.ElementTree import tostring
import matplotlib.pyplot as plt
class Dron:
    def __init__(self,nombre,peso_maximo,ruta=None):
        self.nombre=nombre
        self.peso_maximo=peso_maximo
        self.ruta=ruta
        self.id_ruta=None

class Node:
    def __init__(self, id, x, y, package_weight=1.0, has_order=True, cantidad_paquetes=None, valor_mercancia=None, nombre=None):
        self.id = id
        self.nombre = nombre
        self.x = x
        self.y = y
        self.package_weight = package_weight
        self.has_order = has_order
        self.cantidad_paquetes = cantidad_paquetes
        self.valor_mercancia = valor_mercancia
    def __str__(self):
        return self.toString()
    def __repr__(self):
        return self.toString()
    def __hash__(self):
        return hash(self.id)
    def __eq__(self, other):
        return isinstance(other, Node) and self.id == other.id
    def toString(self):
        nombre = self.nombre if self.nombre is not None else "N/A"
        cantidad = self.cantidad_paquetes if self.cantidad_paquetes is not None else 0
        valor = self.valor_mercancia if self.valor_mercancia is not None else 0
        peso = self.package_weight if self.package_weight is not None else 0.0
        return f"{self.id:3} | {nombre:21} | {peso:9.6f} | {cantidad:8} | {valor:7} | ({self.x},{self.y})"

class Graph:
    def __init__(self, vertices=None):
        self.vertices = set(vertices) if vertices else set()
        self.edges = set()
        self.weight = set()
        if vertices:
            self._build_full_graph()

    def toString(self, route):
        if not route or len(route) == 0:
            return "-1"
        output = "ID  | Nombre                | Peso (kg) | Paquetes |  Valor  | Coordenadas"
        for node in route:
            output += "\n" + node.toString()
        return output


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
            ax.text(n.x, n.y, n.nombre if n.nombre else n.id)
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
            ax.text(n.x, n.y, n.nombre if n.nombre else n.id)
        ax.set_title('Grafo Completo')
        ax.set_xlabel('Coordenada X')
        ax.set_ylabel('Coordenada Y')
        ax.legend()
        plt.grid(True)
        plt.show()
    def toStringFullGraph(self):
        output = "ID  | Nombre                | Peso (kg) | Paquetes |  Valor  | Coordenadas"
        for node in self.vertices:
            output += "\n" + node.toString()
        return output

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
            ax.text(n.x, n.y, n.nombre if n.nombre else n.id)
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
            ax.text(n.x, n.y, n.nombre if n.nombre else n.id)
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
    drones = []
    nodes = []
    base = Node("0", 0, 0, has_order=False)

    print("Bienvenido al sistema de rutas de la distribuidora De Medicamentos E Insumos Hospitalarios Ltda\n")
    menu = """
    ------------------------ Menú -----------------------------
    A continuación, ingrese:
    
    1. Para agregar un nodo a la lista.
    2. Para generar un nuevo grafo.
    3. Para generar las subrutas según criterios.
    4. Para visualizar las rutas.
    5. Para agregar un dron.
    6. Para asignar ruta a un dron.
    7. Para mostrar este menú.
    8. Para salir del programa.
    9. Para generar demostración de rutas del sistema.
    -------------------------------------------------------------
    """
    print(menu)

    while True:
        op = int(input("Su opción es: "))

        if op == 1:
            print("\n------------------ Agregar un nodo ----------------------\n")
            id = input("Ingrese la ID del nodo: ")
            x = float(input("Ingrese la coordenada x: "))
            y = float(input("Ingrese la coordenada y: "))
            peso = float(input("Ingrese el peso del pedido: "))
            volumen = float(input("Ingrese la cantidad de paquetes del pedido: "))
            valor = int(input("Ingrese el valor del pedido: "))
            nombre = input("Ingrese el nombre de la droguería: ")
            nodes.append(Node(id, x, y, package_weight=peso, has_order=True, cantidad_paquetes=volumen, valor_mercancia=valor, nombre=nombre))
            print("Nodo agregado exitosamente.\n")
            print("--------------------------------------------------------\n")

        elif op == 2:
            print("\n------------------ Generar nuevo grafo ------------------\n")
            if len(nodes) > 1:
                if not contains(nodes,base):
                    nodes.append(base)
                g = None
                g = Graph(nodes)
                start = base
                print(g.toStringFullGraph())
                g.plot_full_graph()
                tour = g.nearest_neighbor(start)
                length = g.tour_length(tour)
                print('Inicial:', [n.id for n in tour], length)
                print(f"\n\n{g.toString(tour)}")
                g.plot_tour(tour)

                cancelled = random.choice([n for n in nodes if n != base])
                cancelled.has_order = False
                print('Cancelado:', cancelled.id)

                new_tour = g.adjust_route(tour, cancelled, start)
                new_length = g.tour_length(new_tour)
                print('Ajustado:', [n.id for n in new_tour], new_length)
                g.plot_tour(new_tour, title_suffix=' (ajustada)')
                print(f"\n\n{g.toString(new_tour)}")
                print("--------------------------------------------------------\n")
            else:
                print("Por favor, primero agregue otro nodo al grafo")
                print("--------------------------------------------------------\n")
        elif op == 3:
            print("\n----------- Generar subrutas según criterios -----------\n")
            while True:
                try:
                    max_distance=input("Distancia máxima por ruta (enter para sin límite): ")
                    max_distance = None if max_distance.strip() == "" else float(max_distance)
                    max_distance_to_origin = max((n.x**2 + n.y**2)**0.5 for n in nodes)
                    if max_distance is not None:
                        if max_distance < max_distance_to_origin:
                            print(f"No es posible generar subrutas con una distancia entre nodos menor a la distancia máxima entre nodos, usando el menor valor posible: {max_distance_to_origin+1}")
                            max_distance = max_distance_to_origin+1
                    peso_max = input("Peso máximo por ruta (enter para sin límite): ")
                    peso_max = None if peso_max.strip() == "" else float(peso_max)
                    max_package_weight = max(n.package_weight for n in nodes)
                    if peso_max is not None:
                        if peso_max < max_package_weight:
                            print(f"No es posible generar subrutas con un peso menor al máximo de algún nodo, usando el menor valor posible: {max_package_weight+1}")
                            peso_max = max_package_weight+1
                    vol_max = input("Cantidad de nodos máxima por ruta (enter para sin límite): ")
                    vol_max = None if vol_max.strip() == "" else float(vol_max)



                
                    routes = g.plan_routes(start, max_distance=max_distance, max_weight=peso_max, max_volume=vol_max)
                    if routes is None:
                        print("Criterios no válidos, intente de nuevo.\n")
                        continue
                    break
                except ValueError:
                    print("Entrada inválida. Intente de nuevo.\n")
        
            print("Subrutas generadas:\n")
            for idx, r in enumerate(routes,1):
                print(f"Ruta {idx}: {[n.id for n in r['tour']]} distancia={r['distance']:.1f} peso={r['weight']:.1f} vol={r['volume']}")
                print(f"\n\n{g.toString(r['tour'])}")
                g.plot_route(r, title=f"Ruta {idx}")

            g.plot_all_routes(routes)
            print("--------------------------------------------------------\n")

        elif op == 4:
            print("\n------------------ Visualizar rutas ------------------\n")
            g.plot_full_graph()
            for idx, r in enumerate(routes,1):
                print(f"Ruta {idx}: {[n.id for n in r['tour']]} distancia={r['distance']:.1f} peso={r['weight']:.1f} vol={r['volume']}")
                print(f"\n\n{g.toString(r['tour'])}")
                g.plot_route(r, title=f"Ruta {idx}")

            g.plot_all_routes(routes)
            print("-----------------------------------------------------\n")

        elif op == 5:
            print("\n------------------ Agregar dron ------------------\n")
            nombre = input("Nombre del dron: ")
            peso_max = float(input("Peso máximo soportado (kg): "))
            dron = Dron(nombre, peso_max)
            drones.append(dron)
            print("Dron agregado exitosamente.\n")

        elif op == 6:
            print("\n-------------- Asignar ruta a dron --------------\n")
            if not routes:
                print("No hay rutas disponibles. Genere rutas primero.\n")
                continue

            print("Drones disponibles:")
            for i, dron in enumerate(drones, 1):
                print(f"{i}. {dron.nombre} (peso máximo: {dron.peso_maximo} kg, ruta asignada: {dron.id_ruta})")

            idx_dron = int(input("Seleccione el número de dron: ")) - 1
            if not (0 <= idx_dron < len(drones)):
                print("Opción inválida.\n")
                continue
            dron = drones[idx_dron]

            for i, r in enumerate(routes, 1):
                print(f"{i}. Ruta con peso total {r['weight']:.1f} kg")

            idx_ruta = int(input("Seleccione el número de ruta: ")) - 1
            if not (0 <= idx_ruta < len(routes)):
                print("Opción inválida.\n")
                continue

            if routes[idx_ruta]['weight'] > dron.peso_maximo:
                print("La ruta excede el peso máximo del dron.\n")
            else:
                dron.ruta=routes[idx_ruta]
                dron.id_ruta=idx_ruta+1
                print("Ruta asignada exitosamente.\n")
        elif op==7:
            print(menu)
        elif op==8:
            print("Gracias por usar el programa\nSaliendo...")
            break
        elif op==9:
            print("Inicializando prueba de la clase demo:")
            i = 0
            stay=True
            while(stay):
                TypeOfSimulation = input("\nIngrese 0 para probar con datos reales\nIngrese 1 para probar con datos aleatorios\n\nSu eleccion: ")
                if TypeOfSimulation.isnumeric():
                    TypeOfSimulation = int(TypeOfSimulation)
                    if TypeOfSimulation==1:
                        print("Ha elegido la opcion 0, los datos se generaran aleatoriamente")
                        stay=False
                    elif TypeOfSimulation==0:
                        print("Ha elegido la opcion 1, se usaran los datos reales")
                        stay=False
                else:
                    print(f"La opcion ingresada solo puede ser 0 o 1.\n {TypeOfSimulation} no es un tipo de opcion valida \n")
            if TypeOfSimulation==1:
                print("Se crea un sistema de rutas con 15 entradas de prueba\n")
                nodes = None
                nodes = []
                if not contains(nodes,base):
                    nodes.append(base)
                for i in range(1, 15):
                    x = random.randint(-20, 20)
                    y = random.randint(-20, 20)
                    nodes.append(Node(str(i), x, y, package_weight=random.uniform(1,2), has_order=True, cantidad_paquetes=random.randint(1,20), valor_mercancia=random.randint(100,10000)*100, nombre=f"Farmaceutica{i}"))
                g = None
                g = Graph(nodes)
                start = base
                print(g.toStringFullGraph())
                g.plot_full_graph()
                tour = g.nearest_neighbor(start)
                length = g.tour_length(tour)
                print('Inicial:', [n.id for n in tour], length)
                print(f"\n\n{g.toString(tour)}")
                g.plot_tour(tour)

                cancelled = random.choice([n for n in nodes if n != base])
                cancelled.has_order = False
                print('Cancelado:', cancelled.id)

                new_tour = g.adjust_route(tour, cancelled, start)
                new_length = g.tour_length(new_tour)
                print('Ajustado:', [n.id for n in new_tour], new_length)
                g.plot_tour(new_tour, title_suffix=' (ajustada)')
                print(f"\n\n{g.toString(new_tour)}")

                routes = g.plan_routes(start, max_distance=None, max_weight=15, max_volume=None)
                for idx, r in enumerate(routes,1):
                    print(f"Ruta {idx}: {[n.id for n in r['tour']]} distancia={r['distance']:.1f} peso={r['weight']:.1f} vol={r['volume']}")
                    print(f"\n\n{g.toString(r['tour'])}")
                    g.plot_route(r, title=f"Ruta {idx}")

                g.plot_all_routes(routes)
            else:
                print("Se crea un sistema de rutas con 10 entradas de prueba reales\n")
                nodes = None
                nodes = []
                if not contains(nodes,base):
                    nodes.append(base)
                nodes.append(Node("1",165.59,-281.63,package_weight=random.uniform(1,2),has_order=True,cantidad_paquetes=random.randint(1,20),valor_mercancia=random.randint(100,10000)*100,nombre="Clinica Bucaramanga"))
                nodes.append(Node("2",-50.58,-471.17,package_weight=random.uniform(1,2),has_order=True,cantidad_paquetes=random.randint(1,20),valor_mercancia=random.randint(100,10000)*100,nombre="Clinica Chicamocha"))
                nodes.append(Node("3",196.66,242.43,package_weight=random.uniform(1,2),has_order=True,cantidad_paquetes=random.randint(1,20),valor_mercancia=random.randint(100,10000)*100,nombre="Drogueria Colsubsidio"))
                nodes.append(Node("4",-250.1,-116.22,package_weight=random.uniform(1,2),has_order=True,cantidad_paquetes=random.randint(1,20),valor_mercancia=random.randint(100,10000)*100,nombre="Farmatodo"))
                nodes.append(Node("5",-436.03,607.43,package_weight=random.uniform(1,2),has_order=True,cantidad_paquetes=random.randint(1,20),valor_mercancia=random.randint(100,10000)*100,nombre="Farmacia La rebaja"))
                nodes.append(Node("6",360.21,795.22,package_weight=random.uniform(1,2),has_order=True,cantidad_paquetes=random.randint(1,20),valor_mercancia=random.randint(100,10000)*100,nombre="Drogueria Alemana"))
                nodes.append(Node("7",-483.81,303.81,package_weight=random.uniform(1,2),has_order=True,cantidad_paquetes=random.randint(1,20),valor_mercancia=random.randint(100,10000)*100,nombre="Clinica San Luis"))
                nodes.append(Node("8",-239.04,833.36,package_weight=random.uniform(1,2),has_order=True,cantidad_paquetes=random.randint(1,20),valor_mercancia=random.randint(100,10000)*100,nombre="Drogueria Ahorremas"))
                nodes.append(Node("9",271.23,47.15,package_weight=random.uniform(1,2),has_order=True,cantidad_paquetes=random.randint(1,20),valor_mercancia=random.randint(100,10000)*100,nombre="Cruz verde"))
                nodes.append(Node("10",25.06,-360.52,package_weight=random.uniform(1,2),has_order=True,cantidad_paquetes=random.randint(1,20),valor_mercancia=random.randint(100,10000)*100,nombre="Drogas Paguealcosto"))
                g = Graph(nodes)
                start = base
                print(g.toStringFullGraph())
                g.plot_full_graph()
                tour = g.nearest_neighbor(start)
                length = g.tour_length(tour)
                print('Inicial:', [n.id for n in tour], length)
                print(f"\n\n{g.toString(tour)}")
                g.plot_tour(tour)

                cancelled = random.choice([n for n in nodes if n != base])
                cancelled.has_order = False
                print('Cancelado:', cancelled.id)

                new_tour = g.adjust_route(tour, cancelled, start)
                new_length = g.tour_length(new_tour)
                print('Ajustado:', [n.id for n in new_tour], new_length)
                g.plot_tour(new_tour, title_suffix=' (ajustada)')
                print(f"\n\n{g.toString(new_tour)}")

                routes = g.plan_routes(start, max_distance=None, max_weight=5, max_volume=None)
                for idx, r in enumerate(routes,1):
                    print(f"Ruta {idx}: {[n.id for n in r['tour']]} distancia={r['distance']:.1f} peso={r['weight']:.1f} vol={r['volume']}")
                    print(f"\n\n{g.toString(r['tour'])}")
                    g.plot_route(r, title=f"Ruta {idx}")

                g.plot_all_routes(routes)
