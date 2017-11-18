# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True


# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def path_to_goal(path, goal):
    return path[-1] == goal

def search(graph, start, goal, strategy):
    agenda = [[start]]
    extended_list = set()
    while len(agenda) != 0:
        path = agenda.pop(0)
        if path_to_goal(path, goal):
            return path
        current = path[-1]
        if current not in extended_list:
            extended_list.add(current)
            paths = []
            for node in [n for n in graph.get_connected_nodes(current) if n not in path]:
                paths.append(path + [node])
            agenda = strategy(agenda, paths)

    return []

identity = lambda x: x

def bfs(graph, start, goal):
    return search(graph, start, goal, lambda a, p: a + p)

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    return search(graph, start, goal, lambda a, p: p + a)

sort_by_heuristic = lambda p, g, graph: sorted(p, key=lambda x: graph.get_heuristic(x[-1], g))

## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    return search(
        graph,
        start,
        goal,
        lambda a, p: sort_by_heuristic(p, goal, graph) + a
    )


## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    return search(
        graph,
        start,
        goal,
        lambda a, p: (a + sort_by_heuristic(p, goal, graph))[:beam_width]
    )

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    length = 0
    for i in range(len(node_names) - 1):
        length += graph.get_edge(node_names[i], node_names[i+1]).length
    return length

sort_by_cost = lambda p, graph: sorted(p, key=lambda x: path_length(graph, x))

def branch_and_bound(graph, start, goal):
    return search(
        graph,
        start,
        goal,
        lambda a, p: sort_by_cost(a + p, graph)
    )

sort_by_cost_plus_heurestic = lambda p, g, graph: sorted(
    p,
    key=lambda x: path_length(graph, x) + graph.get_heuristic(x[-1], g)
)

def a_star(graph, start, goal):
    return search(
        graph,
        start,
        goal,
        lambda a, p: sort_by_cost_plus_heurestic(a + p, goal, graph)
    )


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    for node in graph.nodes:
        if graph.get_heuristic(node, goal) > path_length(
            graph,
            branch_and_bound(graph, node, goal)
        ):
            return False

    return True

def is_consistent(graph, goal):
    for edge in graph.edges:
        h1 = graph.get_heuristic(edge.node1, goal)
        h2 = graph.get_heuristic(edge.node2, goal)
        if edge.length < abs(h1 - h2):
            return False

    return True

HOW_MANY_HOURS_THIS_PSET_TOOK = '5'
WHAT_I_FOUND_INTERESTING = 'the way different sorts can be implemented using most of single function'
WHAT_I_FOUND_BORING = 'moving hacky bits around due to Python 2 vs 3 - exp_graph'
