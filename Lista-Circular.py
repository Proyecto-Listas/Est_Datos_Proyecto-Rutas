class Nodo:
    def __init__(self,data):
        self.data = data
        self.siguiente = None
        
class LCSE:
    def __init__(self):
        self.cabeza = None
        self.cola = None    
        
    def validarVacia(self):
        if self.cabeza == None:
            return True
        else:
            return False
            
    def aggInicio(self,data):
        nuevo_Nodo = Nodo(data)
        if self.validarVacia():
            nuevo_Nodo.siguiente = nuevo_Nodo
            self.cabeza = nuevo_Nodo
            self.cola = nuevo_Nodo              #No se si quitar cola, opiniones?
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
                print(actual.data)
                if actual.siguiente == self.cabeza:
                    break
                actual = actual.siguiente
    
    def Buscar(self,valor):
        if self.validarVacia():
            print("Lista vacia")
            return
        else:
            actual = self.cabeza
            while actual.siguiente != self.cabeza:
                if actual.data == valor:
                    print("Elemento Encontrado")
                    return
                actual = actual.siguiente
            print("Elemento no encontrado")  
                

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

lista.aggInicio(10)
lista.aggInicio(40)
lista.aggInicio(30)
lista.aggInicio(20)

lista.ContarElementos()
lista.insertionSort()
lista.imprimirLista()
lista.Buscar(10)
                
    