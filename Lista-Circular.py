import math, random
import matplotlib.pyplot as plt
class Nodo:
    def __init__(self,peso,id,cantidad_paquetes,valor_mercancia,coordenadas,nombre):
        self.peso = peso
        self.nombre = nombre
        self.id = id
        self.cantidad_paquetes = cantidad_paquetes
        self.valor_mercancia = valor_mercancia
        self.coordenadas = coordenadas
        self.siguiente = None

    def toString(self):
        return f"{self.id:3} | {self.nombre:20} | {self.peso:9} | {self.cantidad_paquetes:8} | {self.valor_mercancia:6}"
        
class LCSE:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.base_coordenadas = (0,0)


    def validarVacia(self):
        if self.cabeza == None:
            return True
        else:
            return False
            
    def agregarInicio(self,peso,id=None,cantidad_paquetes=None,valor_mercancia=None,coordenadas=None,nombre=None):
        nuevo_Nodo = Nodo(peso,id,cantidad_paquetes,valor_mercancia,coordenadas,nombre)
        if self.validarVacia():
            nuevo_Nodo.siguiente = nuevo_Nodo
            self.cabeza = nuevo_Nodo
            self.cola = nuevo_Nodo            
            return
        else:
            nuevo_Nodo.siguiente = self.cabeza
            self.cola.siguiente = nuevo_Nodo   
            self.cabeza = nuevo_Nodo
    
    def ContarElementos(self):
        if self.validarVacia():
            print("No hay ruta establecida")
            return
        else:
            contador = 1
            actual = self.cabeza
            while True:
                if actual.siguiente == self.cabeza:
                    break
                actual = actual.siguiente
                contador += 1
            print (f"La ruta contiene {contador} paradas\n")
    
    def toString(self):
        if self.validarVacia():
            return "No hay ruta establecida"
        temp = self.cabeza
        string = " ID | Nombre               | Peso (kg) | Paquetes |  Valor"
        while( True ):
            string = string + "\n" + temp.toString()
            if temp.siguiente == self.cabeza:
                return string
            temp = temp.siguiente
    
    def buscar(self,valor,criterio):
        if self.validarVacia():
            print("No hay ruta establecida")
            return
        else:
            if (criterio=="peso" or criterio == "id" or criterio == "cantidad_paquetes" or criterio =="valor_mercancia" or criterio=="coordenadas"):
                actual = self.cabeza
                
                contador = 0
                while actual != self.cabeza or contador==0:

                    contador=contador+1
                    atributo=getattr(actual,criterio)
                    if atributo == valor:
                        print(f"Elemento Encontrado en posicion {contador}")
                        return contador
                    actual = actual.siguiente
                print("Elemento no encontrado")
            else:
                print("criterio de búsqueda inválido, sólo se admiten 'id','peso','cantidad_paquetes','valor_mercancia' o 'coordenadas'")
            
            return -1 
                

    def insertionSort(self,criterio,ascendente=True):
        if self.validarVacia() or self.cabeza.siguiente == self.cabeza:
            return  # Si la lista está vacía o tiene un solo elemento, no es necesario ordenar
        if (criterio=="peso" or criterio == "id" or criterio == "cantidad_paquetes" or criterio =="valor_mercancia" or criterio=="coordenadas"):

            ordenada = None  # La nueva lista ordenada

            actual = self.cabeza
            while True:
                siguiente = actual.siguiente
                if ordenada is None:  # Si la lista ordenada está vacía, insertar el primer nodo
                    ordenada = actual
                    ordenada.siguiente = ordenada  
                else:
                    # Insertar el nodo en su posición correcta en la lista ordenada
                    ordenada = self.insertarOrdenado(ordenada, actual,criterio)
                
                actual = siguiente
                if actual == self.cabeza:
                    break

            # Establecer la cabeza y la cola de la lista ordenada
            self.cabeza = ordenada
            actual = self.cabeza
            while actual.siguiente != self.cabeza:
                actual = actual.siguiente
            self.cola = actual
        else:
            print("criterio de búsqueda inválido, sólo se admiten 'id','peso','cantidad_paquetes','valor_mercancia' o 'coordenadas'")
            

    def insertarOrdenado(self, ordenada, nuevo_nodo, criterio):
        if ordenada is None:
            nuevo_nodo.siguiente = nuevo_nodo
            return nuevo_nodo
        
        actual = ordenada

        # Caso 1: Insertar al inicio si el valor es menor que la cabeza de la lista ordenada

        if criterio=="coordenadas":
            if distancia(self.base_coordenadas, nuevo_nodo.coordenadas) < distancia(self.base_coordenadas,ordenada.coordenadas):
                while actual.siguiente != ordenada:
                    actual = actual.siguiente
                actual.siguiente = nuevo_nodo
                nuevo_nodo.siguiente = ordenada
                return nuevo_nodo
        else:
            nuevo_nodo_atributo=getattr(nuevo_nodo,criterio)
            ordenada_atributo=getattr(ordenada,criterio)

            if nuevo_nodo_atributo < ordenada_atributo:
                while actual.siguiente != ordenada:
                    actual = actual.siguiente
                actual.siguiente = nuevo_nodo
                nuevo_nodo.siguiente = ordenada
                return nuevo_nodo

        # Caso 2: Insertar en cualquier otra parte de la lista ordenada
        if criterio=="coordenadas":
            if distancia(self.base_coordenadas, nuevo_nodo.coordenadas) < distancia(self.base_coordenadas,ordenada.coordenadas):
                while actual.siguiente != ordenada and distancia(actual.coordenadas,actual.siguiente.coordenadas) < distancia(actual.coordenadas,nuevo_nodo.coordenadas):
                    actual = actual.siguiente
                    actual_siguiente_atributo=getattr(actual.siguiente,criterio)
        else:
            actual_siguiente_atributo=getattr(actual.siguiente,criterio)

            while actual.siguiente != ordenada and actual_siguiente_atributo < nuevo_nodo_atributo:
                actual = actual.siguiente
                actual_siguiente_atributo=getattr(actual.siguiente,criterio)

        # Insertar el nodo en la posición adecuada
        nuevo_nodo.siguiente = actual.siguiente
        actual.siguiente = nuevo_nodo
        return ordenada
    
    
    
def distancia(ubicacion_a, ubicacion_b):
    return math.sqrt((ubicacion_b[0] - ubicacion_a[0])**2 + (ubicacion_b[1] - ubicacion_a[1])**2)

class Demo ():
    def __init__(self):
        print("test")
    def test():
        lista = LCSE()
        i = 0
        print("El programa crea un sistema de rutas con 15 entradas de prueba totalmente aleatorias\n")
        while i<15:
            i=i+1
            lista.agregarInicio(random.randint(0,10),random.randint(0,1000),random.randint(0,5),random.randint(0,200000),(random.randint(-20,20),random.randint(-20,20)),f"Farmacia{i}")
        lista.ContarElementos()
        print(lista.toString())
        lista.insertionSort("peso")
        print("\nRuta ordenada por peso\n")
        print(lista.toString())

        lista.insertionSort("valor_mercancia")
        print("\nRuta ordenada por el valor de la mercancia\n")
        print(lista.toString())

        lista.insertionSort("coordenadas")
        print("\nRuta ordenada por distancia\n")
        print(lista.toString())


        lista.buscar(3,"peso")
        lista.buscar((2,2),"coordenadas")

        def visualizarRuta(ruta):
            x_coords, y_coords, id = [], [], []
            actual = ruta.cabeza
            i=0
            x_coords.append(lista.base_coordenadas[0])
            y_coords.append(lista.base_coordenadas[1])
            id.append("base")
            while actual !=ruta.cabeza or i==0:
                i=i+1
                x_coords.append(actual.coordenadas[0])
                y_coords.append(actual.coordenadas[1])
                id.append(actual.id)
                actual = actual.siguiente

            plt.figure(figsize=(8,6))
            plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='b')
            for i, label in enumerate(id):
                plt.annotate(f"{label}", (x_coords[i], y_coords[i]), textcoords="offset points", xytext=(0,10), ha='center')
            plt.title("Visualización de la Ruta")
            plt.xlabel("Coordenada X")
            plt.ylabel("Coordenada Y")
            plt.grid(True)
            plt.show()

        visualizarRuta(lista)
                
Demo.test()
