#Realizado por:
#Daniver Franchesco Hernandez Acero 2240032
#Juan Manuel Nino Pina 2240040
#Juan Manuel Rivera Torres 2240046
#Luis Felipe Rueda Garcia 2240021
import math, random
import matplotlib.pyplot as plt
class Dron:
    def __init__(self,nombre,peso_maximo,ruta=None):
        self.nombre=nombre
        self.peso_maximo=peso_maximo
        self.ruta=ruta
        self.id_ruta=None
class Nodo:
    def __init__(self,peso,id,cantidad_paquetes,valor_mercancia,coordenada_x,coordenada_y,nombre):
        self.peso = peso
        self.nombre = nombre
        self.id = id
        self.cantidad_paquetes = cantidad_paquetes
        self.valor_mercancia = valor_mercancia
        self.coordenada_x = coordenada_x
        self.coordenada_y = coordenada_y
        self.siguiente = None

    def toString(self):
        return f"{self.id:3} | {self.nombre:21} | {self.peso:9} | {self.cantidad_paquetes:8} | {self.valor_mercancia:6} | ({self.coordenada_x},{self.coordenada_y})"
        
class LCSE:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.base_coordenada_x = 0
        self.base_coordenada_y = 0


    def validarVacia(self):
        if self.cabeza == None:
            return True
        else:
            return False
            
    def agregarInicio(self,peso,id=None,cantidad_paquetes=None,valor_mercancia=None,coordenada_x=None,coordenada_y=None,nombre=None):
        nuevo_Nodo = Nodo(peso,id,cantidad_paquetes,valor_mercancia,coordenada_x,coordenada_y,nombre)
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
            return 0
        else:
            contador = 1
            actual = self.cabeza
            while True:
                if actual.siguiente == self.cabeza:
                    break
                actual = actual.siguiente
                contador += 1
        return contador

    def pesoPaquetes(self):
        if self.validarVacia():
            return 0
        else:
            contador = 0
            actual = self.cabeza
            while True:
                contador += actual.peso
                if actual.siguiente == self.cabeza:
                    break
                actual = actual.siguiente
        return contador

    
    def toString(self):
        if self.validarVacia():
            return -1
        temp = self.cabeza
        string = " ID | Nombre                | Peso (kg) | Paquetes |  Valor | Coordenadas"
        while( True ):
            string = string + "\n" + temp.toString()
            if temp.siguiente == self.cabeza:
                return string
            temp = temp.siguiente
    
    def buscar(self,criterio,valor,valor2=None):
        if self.validarVacia():
            return -1
        else:
            if (criterio=="peso" or criterio == "id" or criterio == "cantidad_paquetes" or criterio =="valor_mercancia"  or criterio=="nombre"):
                actual = self.cabeza
                
                contador = 0
                while actual != self.cabeza or contador==0:

                    contador=contador+1
                    atributo=getattr(actual,criterio)
                    if atributo == valor:
                        return contador
                    actual = actual.siguiente
                return -1
            elif criterio == "coordenadas":
                actual = self.cabeza
                contador = 0
                while actual != self.cabeza or contador==0:

                    contador=contador+1
                    if actual.coordenada_x ==valor and actual.coordenada_y==valor2:
                        return contador
                    actual = actual.siguiente
                return -1

            else:
                #print("criterio de busqueda invalido, solo se admiten 'id','peso','cantidad_paquetes','valor_mercancia' o 'coordenadas'")
                return -1 
                

    def insertionSort(self,criterio):
        if self.validarVacia() or self.cabeza.siguiente == self.cabeza:
            return 0 # Si la lista esta vacia o tiene un solo elemento, no es necesario ordenar
        if (criterio=="peso" or criterio == "id" or criterio == "cantidad_paquetes" or criterio =="valor_mercancia"):

            ordenada = None  # La nueva lista ordenada

            actual = self.cabeza
            while True:
                siguiente = actual.siguiente
                if ordenada is None:  # Si la lista ordenada esta vacia, insertar el primer nodo
                    ordenada = actual
                    ordenada.siguiente = ordenada  
                else:
                    # Insertar el nodo en su posicion correcta en la lista ordenada
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
            return 1

        
        elif criterio == "coordenadas":    
            #buscando la cola
            #actual es el nodo que se esta examinando en cada recorrido, empezamos desde la cabeza
            actual =self.cabeza
            #mientras que el nodo siguente al nodo actual sea diferente de la cabeza, es decir mientras el nodo actual no sea la cola
            while actual.siguiente != self.cabeza:
                #guardamos en nuestra apuntador "actual" el nodo siguiente al actual
                actual=actual.siguiente
            #si se salio del bucle el valor de "actual" debe ser la cola de la lista, lo guardamos en la variable "cola"
            cola = actual

            #variable que almacena el nodo "mas cercano" a el ultimo nodo agregado a la ruta ordenada por distancia,pero EL MAS CERCANO ENCONTRADO HASTA EL MOMENTO es decir el nodo que almacena esta variable va cambiando en medio del recorrido segun se encuentre un nodo mas cercano, en este caso guardamos en el la cabeza mientras recorremos toda lista comparando hasta que quede uno mas cercano que ese
            mas_cercano = self.cabeza
            #al mover un nodo de una posicion para no romper la lista circular necesitamos que el anterior a ese nodo apunte a el siguiente de ese nodo, así cuando "quitemos" un nodo de una posicion la lista no se rompa, por eso nesecitamos esta variable
            anterior_al_mas_cercano = cola

            #encontramos el mas cercano a la base ( en este caso, coordenadas (0,0))
            #actual es el nodo que se esta examinando en cada recorrido, empezamos desde la cabeza
            actual =self.cabeza
            #variable cuyo valor aumenta dentro del bucle
            i=0
            #mientras que "actual" sea diferente de la cabeza (actual es igual a cabeza en la primera iteración o cuando ya se recorrio la lista por completo), o cuando i==0, esta segunda condicion sólo ocurre antes de entrar el bucle ya que una vez dentro el valor de i cambia, (esto es para que a pesar de que la primera vez que se axamina "actual" es igual a "cabeza" aun asi entre en el bucle pero la siguiente vez que esto ocurra ya no)
            while actual != self.cabeza or i==0:
                #cambiamos el valor de i
                i= i+1
                #si la distancia entre la base y el nodo siguiente al actual es menor a la distancia entre la base y mas cercano encontrado hasta el momento (en la primer iteración este más cercano sería el mismo "actual", por eso empezamos comparando con el siguiente al actual)
                if distancia(self.base_coordenada_x, self.base_coordenada_y,actual.siguiente.coordenada_x,actual.siguiente.coordenada_y) < distancia(self.base_coordenada_x,self.base_coordenada_y,mas_cercano.coordenada_x,mas_cercano.coordenada_y):
                    #actualizamos que el anterior al más cercano es ahora el actual pues en la comparación el siguiente al actual fue el máscercano
                    anterior_al_mas_cercano = actual
                    #se actualiza el nodo almacendo en la variable más cercano,
                    mas_cercano = actual.siguiente
                #sin importar si los valores de mascercano y anterioralmascercano se actualizaron o no, en la variable acutal ahora almacenamos el nodo siguiente al guardado en actual
                actual=actual.siguiente
            #si se salió del bucle es porque por segunda vez en nodo guardado en actual es la cabeza, es decir se recorrio toda la lista (sin alterarla)    
            
            #si el más cercano es la cabeza
            if mas_cercano==self.cabeza:
                #guardamos como cabeza de la lista al siguiente (como luego vamos a remover al nodo más cercano en este caso la cabeza de la lista, no queremos que self.cabeza a punte a un nodo que no está en la lista porque no tendríamos como acceder al resto de nodos de la lista a ordenar)
                self.cabeza=self.cabeza.siguiente
            #ahora hacemos que el nodo anterior al mascercano apunte al siguiente al nodo mascercano (para poder removerlo el mascercano de la lista sin romperla)
            anterior_al_mas_cercano.siguiente=mas_cercano.siguiente
            #guardamos en la variable primer_ordenado (la cabeza de la nueva lista ya ordenada) el más cercano
            primer_ordenado=mas_cercano
            #guardamos en la variable ultimo_ordenado el más cercano ("ultimo_ordenado" será siempre el último nodo agragado a la nueva lista ya ordenada)
            ultimo_ordenado=mas_cercano
            #cerramos la nueva lista circular haciendo que este nodo al que apunta ultimo_ordenado tenga como .siguiente a sí mismo
            ultimo_ordenado.siguiente=ultimo_ordenado

            #ahora encontramos el nodo más cercano al ultimo nodo agregado a la lista ya ordenada, (es deicir la siguiente parada más cercana a la parada actual en una ruta) y lo quitamos de la lista a ordenar, u original, y lo agregamos a la lista ya ordenada

            #mientras que el siguiente a la cabeza sea diferete a la cabeza, es decir la lista a ordenar se haya vaciado y sólo que un nodo por odernar
            while self.cabeza.siguiente!=self.cabeza:


                #encotramos la cola de la lista original
                actual =self.cabeza
                #mientras que el nodo siguente al nodo actual sea diferente de la cabeza, es decir mientras el nodo actual no sea la cola
                while actual.siguiente != self.cabeza:
                    #guardamos en nuestra apuntador "actual" el nodo siguiente al actual
                    actual=actual.siguiente
                #si se salió del bucle el valor de "actual" debe ser la cola de la lista, lo guardamos en la variable "cola"
                cola = actual

                #restauramos las valores de actual y máscercano para que sean la cabeza y empezar a recorrerla lista otra vez
                actual=self.cabeza
                mas_cercano=actual
                #restauramos el valor de anterior al mas cercano para que sea la cola
                anterior_al_mas_cercano = cola
                #volvemos a darle el valor de 0 a i para que se pueda ingresar en el siguiente bucle interno, aún con actual siendo igual a cabeza
                i=0
                #mientras que "actual" sea diferente de la cabeza (actual es igual a cabeza en la primera iteración o cuando ya se recorrió la lista por completo), o cuando i==0, esta segunda condición sólo ocurre antes de entrar el bucle ya que una vez dentro el valor de i cambia, (esto es para que a pesar de que la primera vez que se axamina "actual" es igual a "cabeza" aún así entre en el bucle pero la siguiente vez que esto ocurra ya no)
                while actual != self.cabeza or i==0:
                    #cambiamos el valor de i
                    i=i+1
                    #si la distancia entre el último nodo agregado a la lista ya ordenada y el nodo siguiente al actual es menor a la distancia entre ultimo_ordenado (el último nodo agregado a la lista ya ordenada) y mas_cercano (el más cercano encontrado hasta el momento), [en la primer iteración este más cercano sería el mismo "actual", por eso empezamos comparando con el siguiente al actual]
                    if distancia(ultimo_ordenado.coordenada_x,ultimo_ordenado.coordenada_y, actual.siguiente.coordenada_x,actual.siguiente.coordenada_y) < distancia(ultimo_ordenado.coordenada_x,ultimo_ordenado.coordenada_y,mas_cercano.coordenada_x,mas_cercano.coordenada_y):
                         #actualizamos que el anterior al más cercano es ahora el actual pues en la comparación el siguiente al actual fue el máscercano
                        anterior_al_mas_cercano = actual
                        #se actualiza el nodo almacendo en la variable más cercano
                        mas_cercano = actual.siguiente
                    #sin importar si los valores de mascercano y anterioralmascercano se actualizaron o no, en la variable acutal ahora almacenamos el nodo siguiente al guardado en actual
                    actual=actual.siguiente
            #si se salió de este bucle interno es porque por segunda vez en nodo guardado en actual es la cabeza, es decir se recorrio toda la lista (sin alterarla)    
            
            #si el más cercano es la cabeza
                if mas_cercano==self.cabeza:
                    #guardamos como cabeza de la lista al siguiente (como luego vamos a remover al nodo más cercano en este caso la cabeza de la lista, no queremos que self.cabeza a punte a un nodo que no está en la lista porque no tendríamos como acceder al resto de nodos de la lista a ordenar)
                    self.cabeza=self.cabeza.siguiente

                #ahora hacemos que el nodo anterior al mascercano apunte al siguiente al nodo mascercano (para poder removerlo el mascercano de la lista sin romperla)
                anterior_al_mas_cercano.siguiente=mas_cercano.siguiente
                #hacemos que el último en la lista ya ordenada apunte al más cercano (así lo agregamos a la lista ordenada)
                ultimo_ordenado.siguiente=mas_cercano
                #ahora el último en la lista ordenada es el más cercano encontrado en la última iteración
                ultimo_ordenado=mas_cercano
                #hacemos que el último agregado a la lista ordenada apunte a la cabeza para completar la lista cerrada
                ultimo_ordenado.siguiente=primer_ordenado

            #una vez se sale del ciclo externo la lista a orderar (original) ya  sólo tiene un elemento, la cabeza, agregamos este nodo a la lista ya ordenada, asiendo que el último en la lista ordenada ahora apunte a la cabeza
            ultimo_ordenado.siguiente=self.cabeza
            #ahora el último en la lista ordenada es la cabeza de la lista original
            ultimo_ordenado=self.cabeza
            #hacemos que el primer_ordenado (cabeza de la lista ordenada) sea la cabeza de nuestra lista original que ahora estará ya ordenada
            self.cabeza = primer_ordenado
            #hacemos que este último nodo agregado a la lista ya ordenada(anterior cabeza de la lista original) ahora apunte a la cabeza de la lista para cerrar la lista original ordenada
            ultimo_ordenado.siguiente=primer_ordenado
            return 1
        else:
            return -1
            

    def insertarOrdenado(self, ordenada, nuevo_nodo, criterio):
        if ordenada is None:
            nuevo_nodo.siguiente = nuevo_nodo
            return nuevo_nodo
        
        actual = ordenada

        # Caso 1: Insertar al inicio si el valor es menor que la cabeza de la lista ordenada

        nuevo_nodo_atributo=getattr(nuevo_nodo,criterio)
        ordenada_atributo=getattr(ordenada,criterio)

        if nuevo_nodo_atributo < ordenada_atributo:
            while actual.siguiente != ordenada:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = ordenada
            return nuevo_nodo

        # Caso 2: Insertar en cualquier otra parte de la lista ordenada
        actual_siguiente_atributo=getattr(actual.siguiente,criterio)

        while actual.siguiente != ordenada and actual_siguiente_atributo < nuevo_nodo_atributo:
            actual = actual.siguiente
            actual_siguiente_atributo=getattr(actual.siguiente,criterio)

        # Insertar el nodo en la posición adecuada
        nuevo_nodo.siguiente = actual.siguiente
        actual.siguiente = nuevo_nodo
        return ordenada
    
    def visualizarRuta(self):
            x_coords, y_coords, id = [], [], []
            actual = self.cabeza
            i=0
            x_coords.append(self.base_coordenada_x)
            y_coords.append(self.base_coordenada_y)
            id.append("Distribuidora")
            while actual !=self.cabeza or i==0:
                i=i+1
                x_coords.append(actual.coordenada_x)
                y_coords.append(actual.coordenada_y)
                id.append(actual.nombre)
                actual = actual.siguiente

            plt.figure(figsize=(8,6))
            plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='b')
            for i, label in enumerate(id):
                plt.annotate(f"{label}", (x_coords[i], y_coords[i]), textcoords="offset points", xytext=(0,10), ha='center')
            plt.title("Distribuidora De Medicamentos E Insumos Hospitalarios Ltda\nVisualizacion de la Ruta")
            plt.xlabel("Coordenada X")
            plt.ylabel("Coordenada Y")
            plt.grid(True)
            plt.show()
    
def distancia(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

class NodoRaiz():
    def __init__(self,data,x,y):
        self.data=data
        self.coordenada_x=x
        self.coordenada_y=y
        self.hijos_Xpos_YPos=LCSE()
        self.hijos_Xpos_YNeg=LCSE()
        self.hijos_XNeg_YPos=LCSE()
        self.hijos_XNeg_YNeg=LCSE()   

class Tree():
    def __init__(self,raiz):
        self.raiz=raiz
        self.rutas=["Xpositivo YPositivo","Xpositivo YNegativo","XNegativo YPositivo","XNegativo YNegativo"]

    def agregarNodo(self,peso,id=None,cantidad_paquetes=None,valor_mercancia=None,coordenada_x=None,coordenada_y=None,nombre=None):
        if coordenada_x>=0 and coordenada_y>=0:
            self.raiz.hijos_Xpos_YPos.agregarInicio(peso,id,cantidad_paquetes,valor_mercancia,coordenada_x,coordenada_y,nombre)
        elif coordenada_x>=0 and coordenada_y<0:
            self.raiz.hijos_Xpos_YNeg.agregarInicio(peso,id,cantidad_paquetes,valor_mercancia,coordenada_x,coordenada_y,nombre)
        elif coordenada_x<0 and coordenada_y>=0:
            self.raiz.hijos_XNeg_YPos.agregarInicio(peso,id,cantidad_paquetes,valor_mercancia,coordenada_x,coordenada_y,nombre)
        elif coordenada_x<0 and coordenada_y<0:
            self.raiz.hijos_XNeg_YNeg.agregarInicio(peso,id,cantidad_paquetes,valor_mercancia,coordenada_x,coordenada_y,nombre)

    def peso(self):
        i=0
        peso=1
        contador=self.raiz.hijos_Xpos_YPos.ContarElementos()
        peso=peso+contador
        print (f"La ruta {self.rutas[i]} contiene {contador} paradas\n")
        i=i+1
        contador=self.raiz.hijos_Xpos_YNeg.ContarElementos()
        peso=peso+contador
        print (f"La ruta {self.rutas[i]} contiene {contador} paradas\n")
        i=i+1
        contador=self.raiz.hijos_XNeg_YPos.ContarElementos()
        peso=peso+contador
        print (f"La ruta {self.rutas[i]} contiene {contador} paradas\n")
        i=i+1
        contador=self.raiz.hijos_XNeg_YNeg.ContarElementos()
        peso=peso+contador
        print (f"La ruta {self.rutas[i]} contiene {contador} paradas\n")

        print(f"el arbol tiene un peso de {peso}")
        return peso 
        
    def buscar(self,criterio,valor,valor2=None):
        position=self.raiz.hijos_Xpos_YPos.buscar(criterio,valor,valor2=None)
        if position>=0:
            return (0,position)
        position=self.raiz.hijos_Xpos_YNeg.buscar(criterio,valor,valor2=None)
        if position>=0:
            return (1,position)
        position=self.raiz.hijos_XNeg_YPos.buscar(criterio,valor,valor2=None)
        if position>=0:
            return (2,position)
        position=self.raiz.hijos_XNeg_YNeg.buscar(criterio,valor,valor2=None)
        if position>=0:
            return (3,position)
        return (-1,-1)

    def toString(self):
        i=0
        string=""
        string=string+("\n\n\nRuta"+self.rutas[i]+".\n")
        string=string+self.raiz.hijos_Xpos_YPos.toString()
        i=i+1
        string=string+("\n\n\nRuta"+self.rutas[i]+".\n")
        string=string+self.raiz.hijos_Xpos_YNeg.toString()
        i=i+1
        string=string+("\n\n\nRuta"+self.rutas[i]+".\n")
        string=string+self.raiz.hijos_XNeg_YPos.toString()
        i=i+1
        string=string+("\n\n\nRuta"+self.rutas[i]+".\n")
        string=string+self.raiz.hijos_XNeg_YNeg.toString()
        return string

    def insertionSort(self,criterio):
        i=0
        rutaOrdena= self.raiz.hijos_Xpos_YPos.insertionSort(criterio)
        if rutaOrdena<0:
            print("criterio de ordenamiento invalido, solo se admiten 'id','peso','cantidad_paquetes','valor_mercancia' o 'coordenadas'")
        else:
            i=i+1
            self.raiz.hijos_Xpos_YNeg.insertionSort(criterio)
            i=i+1
            self.raiz.hijos_XNeg_YPos.insertionSort(criterio)
            i=i+1
            self.raiz.hijos_XNeg_YNeg.insertionSort(criterio)


    def visualizarRuta(self):
            plt.figure(figsize=(8,6))
            
            def aux(list,colour):
                x_coords, y_coords, id = [], [], []
                x_coords.append(self.raiz.coordenada_x)
                y_coords.append(self.raiz.coordenada_y)
                id.append(self.raiz.data)
                actual=list.cabeza
                i=0
                while actual !=list.cabeza or i==0:
                    i=i+1
                    x_coords.append(actual.coordenada_x)
                    y_coords.append(actual.coordenada_y)
                    id.append(actual.nombre)
                    actual = actual.siguiente
                plt.plot(x_coords, y_coords, marker='o', linestyle='-', color=colour)
                for i, label in enumerate(id):
                    plt.annotate(f"{label}", (x_coords[i], y_coords[i]), textcoords="offset points", xytext=(0,10), ha='center')

                   
            route=self.raiz.hijos_Xpos_YPos
            aux(route,"b")
            route=self.raiz.hijos_Xpos_YNeg
            aux(route,"g")
            route=self.raiz.hijos_XNeg_YPos
            aux(route,"r")
            route=self.raiz.hijos_XNeg_YNeg
            aux(route,"m")


            plt.title("Distribuidora De Medicamentos E Insumos Hospitalarios Ltda\nVisualizacion de las Rutas")
            plt.xlabel("Coordenada X")
            plt.ylabel("Coordenada Y")
            plt.grid(True)
            plt.show()


        

class NodoRaiz2():
    def __init__(self,data,x,y):
        self.data=data
        self.coordenada_x=x
        self.coordenada_y=y
        self.hijos2=[ (hijos_Xpos_YPos:=LCSE()) , (hijos_Xpos_YNeg:=LCSE()) , (hijos_XNeg_YPos:=LCSE()) , (hijos_XNeg_YNeg:=LCSE()) ]

class Tree2():
    def __init__(self,raiz):
        self.raiz=raiz
        self.rutas=["0. Primer cuadrante","1. Cuarto cuadrante","2. Segundo cuadrante","3. Tercer cuadrante"]


    def agregarNodo(self,peso,id=None,cantidad_paquetes=None,valor_mercancia=None,coordenada_x=None,coordenada_y=None,nombre=None):
        if coordenada_x>=0 and coordenada_y>=0:
            self.raiz.hijos2[0].agregarInicio(peso,id,cantidad_paquetes,valor_mercancia,coordenada_x,coordenada_y,nombre)
        elif coordenada_x>=0 and coordenada_y<0:
            self.raiz.hijos2[1].agregarInicio(peso,id,cantidad_paquetes,valor_mercancia,coordenada_x,coordenada_y,nombre)
        elif coordenada_x<0 and coordenada_y>=0:
            self.raiz.hijos2[2].agregarInicio(peso,id,cantidad_paquetes,valor_mercancia,coordenada_x,coordenada_y,nombre)
        elif coordenada_x<0 and coordenada_y<0:
            self.raiz.hijos2[3].agregarInicio(peso,id,cantidad_paquetes,valor_mercancia,coordenada_x,coordenada_y,nombre)

    def peso(self):
        i=0
        peso=1
        for hijo in self.raiz.hijos2:
            contador=hijo.ContarElementos()
            peso=peso+contador
            print (f"La ruta {self.rutas[i]} contiene {contador} paradas\n")
            i=i+1
        print(f"el arbol tiene un peso de {peso}")
        return peso 
        

    def buscar(self,criterio,valor,valor2=None):
        i=0
        for hijo in self.raiz.hijos2:
            position=hijo.buscar(criterio,valor,valor2=None)
            if position>0:
                return (i,position)
            i=i+1
        return (-1,-1)

    def toString(self):
        i=0
        string=""
        for hijo in self.raiz.hijos2:
            string=string+("\n\n\nRuta "+self.rutas[i]+".\n")
            string=string+hijo.toString()
            i=i+1
        return string

    def insertionSort(self,criterio):
        for hijo in self.raiz.hijos2:
            rutaOrdena=hijo.insertionSort(criterio)
            if rutaOrdena<0:
                print("Criterio de ordenamiento invalido, solo se admiten 'id','peso','cantidad_paquetes','valor_mercancia' o 'coordenadas'")
                return -1

    def visualizarRuta(self):
        plt.figure(figsize=(8,6))
        
        colours=["b","g","r","m"]
        j=0
        for route in self.raiz.hijos2:
            x_coords, y_coords, id = [], [], []
            x_coords.append(self.raiz.coordenada_x)
            y_coords.append(self.raiz.coordenada_y)
            id.append(self.raiz.data)
            actual=route.cabeza
            i=0
            while actual !=route.cabeza or i==0:
                i=i+1
                x_coords.append(actual.coordenada_x)
                y_coords.append(actual.coordenada_y)
                id.append(actual.nombre)
                actual = actual.siguiente
            plt.plot(x_coords, y_coords, marker='o', linestyle='-', color=colours[j])
            for i, label in enumerate(id):
                plt.annotate(f"{label}", (x_coords[i], y_coords[i]), textcoords="offset points", xytext=(0,10), ha='center')
            j=j+1        

        plt.title("Distribuidora De Medicamentos E Insumos Hospitalarios Ltda\nVisualizacion de las Rutas")
        plt.xlabel("Coordenada X")
        plt.ylabel("Coordenada Y")
        plt.grid(True)
        plt.show()

raiz1=NodoRaiz("Distribuidora",0,0)
raiz2=NodoRaiz2("Distribuidora",0,0)
arbol1=Tree(raiz1)
arbol2=Tree2(raiz2)

class Demo ():
    def __init__(self):
        print("test")
    def test(arbol):
        print("Inicializando prueba de la clase demo:")
        i = 0
        stay=True
        while(stay):
            TypeOfSimulation = input("\nIngrese 0 para probar con datos reales\nIngrese 1 para probar con datos aleatorios\n")
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
            while i<15:
                i=i+1
                arbol.agregarNodo(random.randint(1,10),random.randint(1,1000),random.randint(1,5),random.randint(1,200000),random.randint(-20,20),random.randint(-20,20),f"Farmacia{i}")
        else:
            print("Se crea un sistema de rutas con 10 entradas de prueba reales\n")

            
            arbol.agregarNodo(random.randint(1,10),random.randint(1,1000),random.randint(1,5),random.randint(1,200000),165.59,-281.63,"Clinica Bucaramanga")
            arbol.agregarNodo(random.randint(1,10),random.randint(1,1000),random.randint(1,5),random.randint(1,200000),-50.58,-471.17,"Clinica Chicamocha")
            arbol.agregarNodo(random.randint(1,10),random.randint(1,1000),random.randint(1,5),random.randint(1,200000),196.66,242.43,"Drogueria Colsubsidio")
            arbol.agregarNodo(random.randint(1,10),random.randint(1,1000),random.randint(1,5),random.randint(1,200000),-250.1,-116.22,"Farmatodo")
            arbol.agregarNodo(random.randint(1,10),random.randint(1,1000),random.randint(1,5),random.randint(1,200000),-436.03,607.43,"Farmacia La rebaja")
            arbol.agregarNodo(random.randint(1,10),random.randint(1,1000),random.randint(1,5),random.randint(1,200000),360.21,795.22,"Drogueria Alemana")
            arbol.agregarNodo(random.randint(1,10),random.randint(1,1000),random.randint(1,5),random.randint(1,200000),-483.81,303.81,"Clinica San Luis")
            arbol.agregarNodo(random.randint(1,10),random.randint(1,1000),random.randint(1,5),random.randint(1,200000),-239.04,833.36,"Drogueria Ahorremas")
            arbol.agregarNodo(random.randint(1,10),random.randint(1,1000),random.randint(1,5),random.randint(1,200000),271.23,47.15,"Cruz verde")
            arbol.agregarNodo(random.randint(1,10),random.randint(1,1000),random.randint(1,5),random.randint(1,200000),25.06,-360.52,"Drogas Paguealcosto")
        arbol.peso()
        print(arbol.toString())
        arbol.insertionSort("peso")
        print("\nRutas ordenada por peso\n")
        print(arbol.toString())

        arbol.insertionSort("valor_mercancia")
        print("\nRutas ordenada por el valor de la mercancia\n")
        print(arbol.toString())

        arbol.insertionSort("coordenadas")
        print("\nRutas ordenada por distancia\n")
        print(arbol.toString())

        def printencontrado(encontrado):
            if encontrado[0]<1:
                print("elemento no encontrado")
            else:
                print(f"elememto encontrado en la ruta {arbol.rutas[encontrado[0]]} posicion {encontrado[1]}")

        print("Buscando un envio con peso 3")
        printencontrado( arbol.buscar("peso",3) )
        print("Buscando un envio con coordenadas (2,2)")
        printencontrado( arbol.buscar("coordenadas",2,2))
        print("Buscando un envio con coordenadas (-50.58,-471.17)")
        printencontrado( arbol.buscar("coordenadas",-50.58,-471.17) )
        print("Buscando una farmacia de nombre Farmacia11")
        printencontrado( arbol.buscar("nombre","Farmacia11") )      
        print("Buscando una farmacia de nombre Farmatodo")
        printencontrado( arbol.buscar("nombre","Farmatodo") )

        print("\nLas rutas se mostraran ordenadas por distancia")
        arbol.visualizarRuta()

        
                
#Demo.test(arbol1)
drones=[]
# Demo.test(arbol2)
print("Bienvenido al sistema de rutas de la distribuidora De Medicamentos E Insumos Hospitalarios Ltda\n")
menu = "\n------------------------ Menu -----------------------------\nA continuacion, ingrese:\n\n 1. Para agregar una drogueria a la ruta. \n 2. Para ordenar el arbol. \n 3. Para visualizar las rutas \n 4. Para agregar un dron.\n 5. Para asignar ruta a un dron.\n 6. Para mostrar este menu. \n 7. Para salir del programa. \n 8. Para generar demostracion de rutas del sistema.\n-----------------------------------------------------------\n"
print(menu)
while True:
    op=int(input("Su opcion es: "))
    if op==1:
        print("\n------------------ Agregar una drogueria ----------------------\n")
        print("\nSe ha agregado correctamente a la ruta", arbol2.agregarNodo(float(input("Ingrese el peso de la carga: ")),int(input("Ingrese una id para la entrega: ")),int(input("Ingrese la cantidad de paquetes")),int(input("Ingrese un valor para la mercancia: ")),float(input("Ingrese la coordenada x con respecto a la distribuidora: ")),float(input("Ingrese la coordenada y con respecto a la distribuidora: ")),input("Ingrese el nombre de la farmacia: ")))
        print("---------------------------------------------------------------\n")
    elif op==2:
        print("\n--------------------------- Ordenar las rutas -----------------------------\n")
        eleccion = input("\nA continuacion, ingrese:\n\n 1. Para ordenar por peso.\n 2. Para ordenar por valor de mercancia.\n 3. Para ordenar por distancia.\n\nSu opcion es: ")
        if eleccion == "1":
            arbol2.insertionSort("peso")
            print("El arbol se ha ordenado por peso")
        elif eleccion == "2":
            arbol2.insertionSort("valor_mercancia")
            print("El arbol se ha ordenado por valor de mercancia")
        elif eleccion == "3":
            arbol2.insertionSort("coordenadas")
            print("El arbol se ha ordenado por distancia")
        else:
            print("No se ha ejecutado ninguna operacion")
        print("---------------------------------------------------------------------------\n")
    elif op==3:
        print("\n--------------------------- Visualizar las rutas -----------------------------\n")
        print("\n Visualizando las siguientes rutas :", arbol2.toString())
        arbol2.visualizarRuta()
        print("------------------------------------------------------------------------------\n")
    elif op==4:
        print("\n--------------------------- Agregar un dron -----------------------------\n")
        dron = Dron(input("Ingrese el nombre del dron: "),float(input("Ingrese el peso maximo en kg que soporta el dron: ")))
        drones.append(dron)
        print(f"Se ha agregado correctamente el dron\n")
        print("----------------------------------------------------------------------------\n")
    elif op==5:
        print("\n----------------------------------------------- Asignar ruta a dron -------------------------------------------------\n")
        print("Drones actualmente agregados: ")
        cont=0
        for dron in drones:
            cont+=1
            print(f"{cont}. {dron.nombre}, soporta un maximo de {dron.peso_maximo} kg, y tiene ruta asignada: {dron.id_ruta}")
        eleccion_dron = int(input("\nElija un dron: "))
        cont=0
        for dron in drones:
            cont+=1
            if eleccion_dron == cont:
                dron_selec=dron
                break
        print("\nRutas actualmente disponibles:\n",arbol2.toString())
        while True:
            eleccion_ruta = int(input("\nElija una ruta: "))
            if eleccion_ruta > 3:
                print("Cancelo la operacion, saliendo...")
                break
            elif dron_selec.peso_maximo >= arbol2.raiz.hijos2[eleccion_ruta].pesoPaquetes():
                dron_selec.ruta=arbol2.raiz.hijos2[eleccion_ruta]
                dron_selec.id_ruta=eleccion_ruta
                break
            else:
                print(f"La ruta de peso {arbol2.raiz.hijos2[eleccion_ruta].pesoPaquetes()} kg excede el peso maximo del dron: {dron_selec.peso_maximo} kg")
                print("Elija otra ruta o 4 para cancelar")

        print("--------------------------------------------------------------------------------------------------------------\n")
    elif op==6:
        print(menu)
    elif op==7:
        print("Gracias por usar el programa\nSaliendo...")
        break
    elif op==8:
        Demo.test(arbol2)
    else:
        print("Opcion no valida. Por favor ingresar una de las opciones del menu: ")
        print(menu)