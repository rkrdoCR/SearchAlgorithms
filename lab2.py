

Skip to content
Using Gmail with screen readers
rkrdo.a.v@gmail.com 

Conversations

Ricardo Alfaro
rkrdo.a.v@gmail.com
Some messages in Trash or Spam match your search. View messages.
15.27 GB (89%) of 17 GB used
Manage
Terms · Privacy · Program Policies
Last account activity: 3 minutes ago
Details

#
# Sus respuestas para las preguntas falso y verdadero deben tener la siguiente forma.
# Sus respuestas deben verse como las dos siguientes:
#ANSWER1 = True
#ANSWER1 = False

# 1: Falso o Verdadero - busqueda Hill Climbing garantiza encontrar una respuesta
#    si es que la hay
ANSWER1 = False

# 2: Falso o Verdadero - busqueda Best-first encontrara una ruta optima
#    (camino mas corto).
ANSWER2 = False

# 3: Falso o Verdadero - Best-first y Hill climbing hacen uso de el
#    valor de la heuristica de los nodos.
ANSWER3 = True

# 4: Falso o Verdadero - A* utiliza un conjunto extendido de nodos
ANSWER4 = True

# 5: Falso o Verdadero - Anchura primero esta garantizado a encontrar un
#    camino con el minimo numero de nodos posible
ANSWER5 = True

# 6: Falso o Verdadero - El Branch and bound regular utiliza valores de
#    la heuristica para acelerar la busqueda de un camino optimo
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph


# Retorna las extensiones para los nodos adjacentes
def get_extensions(graph, path):
    return (path + [adjacent_node] for adjacent_node in graph.get_connected_nodes(path[-1]))

# Retorna los nodos del siguiente nivel ordenados por el valor de la heuristica
def sort_sublevel_by_heuristic(graph, goal, path, sublevel_sorted):
    return sorted(sublevel_sorted, key = lambda path: graph.get_heuristic(path[-1], goal))


# Implemente estos y los puede revisar con el modulo tester
def bfs(graph, start, goal):
    firstPath = [start]
    agenda = [firstPath]
    extended = set()
    result = []		

    while agenda:
		temp_agenda = agenda[:]
		for path in agenda:
			temp_agenda.remove(path)
			extended.add(path[-1])
			if path[-1] == goal:
				result = path
				break
			all_extensions = get_extensions(graph, path)
			for n in all_extensions:
				if n[-1] not in extended:
					temp_agenda.append(n)
		else:
			agenda = temp_agenda
		if not result == []:
			break

    return result



## Si hizo el anterior el siguiente debe ser muy sencillo
def dfs(graph, start, goal):
    firstPath = [start]
    agenda = [firstPath]
    extended = set()
    result = []

    while agenda:
        path = agenda.pop()
        extended.add(path[-1])
        if path[-1] == goal:
            result = path
            break

        all_extensions = get_extensions(graph, path)
        for n in all_extensions:
            if n[-1] not in extended:
                agenda.append(n)

    return result



## Ahora agregue heuristica a su busqueda
## Hill-climbing puede verse como un tipo de busqueda a profundidad primero
## La busqueda debe ser hacia los valores mas bajos que indica la heuristica
def hill_climbing(graph, start, goal):
    firstPath = [start]
    agenda = [firstPath]
    result = []

    while agenda:
        path = agenda[0]
        agenda.remove(path)

        if path[-1] == goal:
            result = path
            break

        sublevel_sorted = []
        all_extensions = get_extensions(graph, path)
        for extension in all_extensions:
            if extension[-1] not in extension[:-1]:
                sublevel_sorted.append(extension)

        sublevel_sorted = sort_sublevel_by_heuristic(graph, goal, path, sublevel_sorted)

        sublevel_sorted.extend(agenda)
        agenda = sublevel_sorted

    return result

    

## Ahora implementamos beam search, una variante de BFS
## que acota la cantidad de memoria utilizada para guardar los caminos
## Mantenemos solo k caminos candidatos de tamano n en nuestra agenda en todo momento.
## Los k candidatos deben ser determinados utilizando la
## funcion (valor) de heuristica del grafo, utilizando los valores mas bajos como los mejores
def beam_search(graph, start, goal, beam_width):
    firstPath = [start]
    agenda = [firstPath]
    result = []

    while agenda:
		temp_agenda = agenda[:]
		for path in agenda:
			temp_agenda.remove(path)

			if path[-1] == goal:
				result = path
				break

			all_extensions = get_extensions(graph, path)
			for extension in all_extensions:
				if extension[-1] not in extension[:-1]:
					temp_agenda.append(extension)
		else:
			temp_agenda = sorted(temp_agenda, key= lambda path: graph.get_heuristic(path[-1], goal))
			agenda = temp_agenda[:beam_width]

		if not result == []:
			break

    return result

## Ahora se implemente busqueda optima, Las anteriores NO utilizan
## las distancias entre los nodos en sus calculos

## Esta funcion toma un grafo y una lista de nombres de nodos y retorna
## la suma de los largos de las aristas a lo largo del camino -- la distancia total del camino.
def path_length(graph, node_names):
	length = 0
	for n1, n2 in zip(node_names[:-1], node_names[1:]):
		length += (graph.get_edge(n1, n2)).length
	return length


def branch_and_bound(graph, start, goal):
    firstPath = [start]
    agenda = [firstPath]
    result = []

    while agenda:
		path = min(agenda, key = lambda possible_path: path_length(graph, possible_path))
		agenda.remove(path)

		if path[-1] == goal:
			result = path
			break

		all_extensions = get_extensions(graph, path)
		for extension in all_extensions:
			if extension[-1] not in extension[:-1]:
				agenda.append(extension)

    return result

def a_star(graph, start, goal):
    firstPath = [start]
    agenda = [firstPath]
    result = []
    extended = set()

    while agenda:
		path = min(agenda, key= lambda candidate: path_length(graph, candidate) +
            graph.get_heuristic(candidate[-1], goal))
		agenda.remove(path)
		extended.add(path[-1])

		if path[-1] == goal:
			result = path
			break

		all_extensions = get_extensions(graph, path)
		for extension in all_extensions:
			if extension[-1] not in extended:
				agenda.append(extension)

    return result


## Es util determinar si un grafo tiene una heuristica admisible y consistente
## puede dar ejemplos de grafos con heuristica admisible pero no consistente
## consistente pero no admisible?

def is_admissible(graph, goal):
    for node in graph.nodes:
        if path_length(graph, branch_and_bound(graph,node,goal))<graph.get_heuristic(node, goal):
            return False
    return True

def is_consistent(graph, goal):
    if not is_admissible(graph,goal):
        return False
    for edge in graph.edges:
        if graph.get_heuristic(edge.node1,goal)>edge.length+graph.get_heuristic(edge.node2,goal):
            return False
        if graph.get_heuristic(edge.node2,goal)>edge.length+graph.get_heuristic(edge.node1,goal):
            return False
    if graph.get_heuristic(goal,goal) !=0:
        return False
    return True

HOW_MANY_HOURS_THIS_PSET_TOOK = 20
WHAT_I_FOUND_INTERESTING = """Todo en realidad, previamente habia implementado BFS y DFS para casos triviales, 
    los otros algoritmos no los conocia, ademas no tengo experiencia en Phyton por lo que fue bastante retador"""
WHAT_I_FOUND_BORING = 'Nada, todo estuvo entretenido.'
lab2.py
Displaying lab2.py.