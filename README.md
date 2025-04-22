<<<<<<< HEAD
# Proyecto Rutas estructuras de Datos y Análisis de algorítmos

Integrantes:
Daniver Franchesco Hernandez Acero 2240032
Juan Manuel Niño Piña 2240040
Juan Manuel Rivera Torres 2240046
Luis Felipe Rueda Garcia 2240021

Sistema de Optimización de Rutas:
1. Implementación con Listas https://github.com/Proyecto-Listas/Est_Datos_Proyecto-Rutas/tree/main/Lista-Circular-Simple

2. Implementación con Árboles: https://github.com/Proyecto-Listas/Est_Datos_Proyecto-Rutas/tree/main/Diagrama-Arbol



Mayorista Farmacéutica
Sistema de Optimización de Rutas

Problema
Una mayorista farmacéutica con alta demanda necesita distribuir medicamentos y otros insumos críticos de forma rápida y eficiente a hospitales, clínicas y farmacias. Ante la necesidad de minimizar tiempos de entrega, reducir el consumo energético y responder a imprevistos (como cambios de demanda o condiciones climáticas adversas), se opta por utilizar drones que realicen entregas automáticas.
Los drones están programados para realizar una ruta semanal, en la que recorre la ciudad, yendo a cada punto de entrega en su base de datos, y entrega el paquete de farmacéuticos, correspondiente. 
El problema a resolver consiste en planificar y optimizar las rutas de vuelo de los drones, garantizando que cada entrega se realice en el menor tiempo y con el menor recorrido posible. Esto no solo permite mejorar la eficiencia logística, sino que también asegura la entrega oportuna de productos esenciales para la salud de la población.

Puesta en Contexto de Listas y Nodos
La estructura de datos Lista es usada para representar el camino que toma el dron cada vez que hace una ruta de entrega. Así pues, el Nodo representa cada punto al que el dron debe llevar un paquete, y el orden en el que esté la lista es el camino que toma el dron para realizar su ruta de entrega.
El tipo de Lista es: Lista Circular Simple. De acuerdo al contexto, este tipo ofrece varios beneficios y ventajas estratégicas, como:
Iteración Cíclica Natural:
 La naturaleza circular de la lista permite recorrer de forma continua la ruta, lo que resulta útil si el dron debe regresar a un punto de origen o realizar múltiples ciclos de entrega a lo largo del día. Se interpreta que el dron realiza la última entrega y, al volver a la cabeza de la lista, ha vuelto al punto de inicio de su ruta y empieza a recorrer el camino una vez más.


Flexibilidad y Dinamismo:
 La estructura facilita la incorporación, eliminación o actualización de nodos, permitiendo ajustes en tiempo real conforme cambian las necesidades logísticas o surgen imprevistos.

La clase Nodo
El nodo es fundamental porque encapsula toda la información necesaria para que el dron pueda realizar la entrega de manera precisa y segura. Al representar cada parada como un nodo, se facilita el cálculo de distancias, la optimización de la secuencia de entregas y la capacidad de adaptación ante cambios en la operación (por ejemplo, reordenar paradas según la prioridad o condiciones del entorno).
Cada nodo almacena los siguientes datos 
Un apuntador al siguiente nodo, o sea, el punto de la siguiente entrega
Identificador de la entrega (Código de tres números)
Nombre de la farmaceútica
Peso en KG del paquete
Cantidad de paquetes a entregar
Valor de los paquetes a entregar
Posición x del punto de entrega
Posición y (Coordenadas del punto de entrega)
La clase Lista
La lista es la representación virtual de la ruta que toma el dron,  pasando por cada punto de entrega (nodo).
La lista tiene los siguientes métodos:
Verificar si la lista está vacía: Para la farmaceútica y el dron, significa verificar si el dron tiene alguna entrega pendiente a realizar.
Insertar Nodo: Permite agregar un nuevo punto de entrega a la lista, pero solo al inicio, haciendo a este nuevo elemento cabeza de lista, es decir, la primera farmacia a la que el dron va desde la base.

Contar los elementos de la lista: para conocer la cantidad de entregas/ viajes que tiene que hacer el dron.
Imprimir en pantalla los elementos de la lista:  la ruta completa que el dron debe seguir. Cada elemento que se imprime en pantalla es un punto de entrega que el dron debe recorrer.
Buscar un elemento: Verificar si en la ruta se debe entregar: una carga del peso especificado, una carga del valor especificado. Verificar si debe entregar a la farmacia especificada o con la id especificada.
Optimizar ruta (Ordenar los nodos): Reorganizar la ruta a seguir por el dron al hacer las entregas. Se puede organizar por distancia, peso y valor de la mercancía. Al organizar por distancia, se asegura que toda la ruta es la más corta posible, es decir la distancia entre las farmacias (los puntos donde se entrega) son las más cortas posibles.
Mostrar la ruta (interfaz básica): Puede mostrarse la ruta en un gráfico en el que se unen los nodos adyacentes utilizando líneas, se parte desde el origen (0,0), donde el dron se aprovisiona, y se une con una línea el siguiente nodo, después se parte en ese nodo y se une con una línea al siguiente.
La clase Demo, interfaz gráfica de la ruta y prueba con datos reales
Contiene llamadas a todos los métodos de la clase lista con valores reales de Bucaramanga de manera que se pueda probar el correcto funcionamiento del sistema de rutas para cualquier caso.
En ese caso, la ruta sería empleada por la mayorista: Distribuidora De Medicamentos E Insumos Hospitalarios Ltda. En el punto de coordenadas, el origen del sistema coordenado representa la distribuidora, y cada uno de los diferentes puntos son los puntos correspondientes a las clínicas (medidos con google maps) fueron tomados con respecto al origen ya mencionado.
Las clínicas utilizadas para la ruta son:
Clínica Bucaramanga
Clínica Chicamocha
Clínica San Luis
Las Farmacias utilizadas en la ruta son:
Farmatodo
Drogas La Rebaja
Droguería Colsubsidio
Cruz Verde
Drogas paguealcosto
Drogas Ahorramás
Droguería Alemana


