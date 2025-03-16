class Nodo:
    def __init__(self,data):
        self.data = data
        self.siguiente = None

    def __init__(self,data,id,cantidad_paquetes,valor_mercancia,coordenadas):
        self.data = data
        self.id = id
        self.cantidad_paquetes = cantidad_paquetes
        self.valor_mercancia = valor_mercancia
        self.coordenadas = coordenadas
        self.siguiente = None
        
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
            
    def agregarInicio(self,data,id=None,cantidad_paquetes=None,valor_mercancia=None,coordenadas=None):
        nuevo_Nodo = Nodo(data,id,cantidad_paquetes,valor_mercancia,coordenadas)
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
            print("Lista Vacia")
            return
        else:
            contador = 1
            actual = self.cabeza
            while True:
                if actual.siguiente == self.cabeza:
                    break
                actual = actual.siguiente
                contador += 1
            print (f"Lista tiene {contador} elementos")
    
    def imprimirLista(self):
        if self.validarVacia():
            print("Lista Vacia")
            return
        else:
            actual = self.cabeza
            while True:
                print(f"data:{actual.data}, id:{actual.id}, cantidad_paquetes:{actual.cantidad_paquetes}, vavlor_paquete:{actual.valor_mercancia}, coordenadas:{actual.coordenadas}")
                if actual.siguiente == self.cabeza:
                    break
                actual = actual.siguiente
    
    def buscar(self,valor,criterio):
        if self.validarVacia():
            print("Lista vacia")
            return
        else:
            if (criterio=="data" or criterio == "id" or criterio == "cantidad_paquetes" or criterio =="valor_mercancia" or criterio=="coordenadas"):
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
                print("criterio de búsqueda inválido, sólo se admiten 'id','data','cantidad_paquetes','valor_mercancia' o 'coordenadas'")
            
            return -1 
                

    def insertionSort(self):
        if self.validarVacia() or self.cabeza.siguiente == self.cabeza:
            return  # Si la lista está vacía o tiene un solo elemento, no es necesario ordenar
        
        ordenada = None  # La nueva lista ordenada

        actual = self.cabeza
        while True:
            siguiente = actual.siguiente
            if ordenada is None:  # Si la lista ordenada está vacía, insertar el primer nodo
                ordenada = actual
                ordenada.siguiente = ordenada  
            else:
                # Insertar el nodo en su posición correcta en la lista ordenada
                ordenada = self.insertarOrdenado(ordenada, actual)
            
            actual = siguiente
            if actual == self.cabeza:
                break

        # Establecer la cabeza y la cola de la lista ordenada
        self.cabeza = ordenada
        actual = self.cabeza
        while actual.siguiente != self.cabeza:
            actual = actual.siguiente
        self.cola = actual

    def insertarOrdenado(self, ordenada, nuevo_nodo):
        if ordenada is None:
            nuevo_nodo.siguiente = nuevo_nodo
            return nuevo_nodo
        
        actual = ordenada

        # Caso 1: Insertar al inicio si el valor es menor que la cabeza de la lista ordenada
        if nuevo_nodo.data < ordenada.data:
            while actual.siguiente != ordenada:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = ordenada
            return nuevo_nodo

        # Caso 2: Insertar en cualquier otra parte de la lista ordenada
        while actual.siguiente != ordenada and actual.siguiente.data < nuevo_nodo.data:
            actual = actual.siguiente

        # Insertar el nodo en la posición adecuada
        nuevo_nodo.siguiente = actual.siguiente
        actual.siguiente = nuevo_nodo

        return ordenada
    
    
    

lista = LCSE()

lista.agregarInicio(1,11,111,1111,(1,1))
lista.agregarInicio(4,44,444,4444,(4,4))
lista.agregarInicio(3,33,333,3333,(3,3))
lista.agregarInicio(2,22,222,2222,(2,2))

lista.ContarElementos()
lista.insertionSort()
lista.imprimirLista()
lista.buscar(3,"data")
lista.buscar((2,2),"coordenadas")
                
    