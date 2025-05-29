## Estructuras de Datos y Análisis de Algoritmos
# Proyecto: Optimización de Rutas

Integrantes:
Daniver Franchesco Hernandez Acero 2240032
Juan Manuel Niño Piña 2240040
Juan Manuel Rivera Torres 2240046
Luis Felipe Rueda Garcia 2240021

## Resumen del Problema:
Una mayorista farmacéutica, con alta demanda, necesita distribuir medicamentos e insumos críticos de forma rápida y eficiente a hospitales, clínicas y farmacias. Para minimizar los tiempos de entrega, reducir el consumo energético y adaptarse a imprevistos como cambios en la demanda o el clima, se decide utilizar un dron para realizar entregas automáticas.

El dron realiza una única ruta semanal, planificada a partir de una base de datos que contiene las zonas de entrega. Esta ruta se genera según criterios definidos por las características de los paquetes. Solo se incluyen en la ruta los puntos de entrega que cumplen con dichos criterios.

El principal reto consiste en planificar y optimizar la ruta del dron, ordenando las entregas de forma geográficamente eficiente para reducir el tiempo y la distancia de vuelo. La solución debe garantizar entregas oportunas y eficientes, mejorando la logística y asegurando el suministro de productos esenciales de salud.

## Etapas de Desarrollo:
1. Implementación con Listas: https://github.com/Proyecto-Listas/Est_Datos_Proyecto-Rutas/tree/main/Lista-Circular-Simple
Se adapto el problema a una lista enlazada simple, donde cada nodo era un lugar de entrega y se reordenaba la lista de acuerdo a la menor distancia cubierta total. Se disminuyó un pco el alcance del problema para adaptarlo.

![Grafico de la ruta con LCSE](/Lista-Circular-Simple/lista.png)

3. Implementación con Árboles: https://github.com/Proyecto-Listas/Est_Datos_Proyecto-Rutas/tree/main/Diagrama-Arbol
Se hizo el cambio de centrar el origen de los drones en (0,0), y tomar los 4 cuadrantes del plano cartesiano, donde por cada cuadrante se recorre una ruta distinta. El mayor cambio fue que hay 4 drones, uno por cada cuadrante y cada uno con su propia ruta.

![Grafico de la ruta con Árboles](/Diagrama-Arbol/arbol.png)


4. Implementación con Grafos: [https://github.com/Proyecto-Listas/Est_Datos_Proyecto-Rutas/tree/main/Diagrama-Arbol](https://github.com/Proyecto-Listas/Est_Datos_Proyecto-Rutas/tree/main/Grafo)
Se tomo el problema en su totalidad, y cada punto de entrega se conecta con todos los demas puntos y con el origen de los drones, así se pueden evaluar todas las posibles rutas con cualquier criterio de selección. Se definió que puede haber mútiples drones, y pueden ser asignados a distintas rutas.

![Grafico de la ruta con Grafos](/Grafo/fullruta.png)
