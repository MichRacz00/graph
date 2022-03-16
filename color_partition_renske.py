from graph_io import *
import timeit


def color_nbs(vertex):  # COLOR_NeighBourS
    return sorted([v.colornum for v in vertex.neighbours])


def colors_in_graph(graph):  # Give all colors for a given graph
    return sorted([v.colornum for v in graph])


def identifier(v):  # Identifier for a vertex: its own color followed by its neighbours colors, sorted
    return tuple([v.colornum] + color_nbs(v))


def colorpartition(graph_list, initial_coloring=False):
    all_vertices = []
    for graph in graph_list:
        all_vertices += graph.vertices

    if not initial_coloring:  # Give every vertex the same color as the first iteration if no coloring is specified
        for vertex in all_vertices:
            vertex.colornum = 0
    iteration(graph_list)
    result(graph_list)

    pass


def result(graph_list):
    checked = []
    print('Sets of possibly isomorphic graphs:')
    for i, graph1 in enumerate(graph_list):
        if graph1 in checked:
            continue

        this_set = [i]
        for j, graph2 in enumerate(graph_list[i + 1:]):
            if colors_in_graph(graph1) == colors_in_graph(graph2): # check if balanced
                this_set += [i + j + 1]
                if len(set(colors_in_graph(graph1))) == len(graph1):
                    print(f'{this_set} 1')
                if len(set(colors_in_graph(graph1))) != len(graph1):
                    graphs = [graph_list[this_set[0]], graph_list[this_set[-1]]]
                    count = countIsomorphism(graphs, dict())

                    if count != 0:
                        print(str(this_set) + " " + str(count))
                        checked.append(graph2)
                    else:
                        del this_set[-1]

                    coloring([graph1, graph2], dict())
                    iteration([graph1, graph2])

    pass


def countIsomorphism(graphs, col):
    iteration(graphs)
    graph1, graph2 = graphs[0], graphs[1]

    if colors_in_graph(graph1) != colors_in_graph(graph2):
        return 0
    if len(set(colors_in_graph(graph1))) == len(graph1):
        return 1

    graph_color = colors_in_graph(graph1)
    color_class = max(graph_color, key=graph_color.count) # color class with most occurences
    x = list(filter(lambda v: v.colornum == color_class, graph1.vertices))[0] # get vertex in color class

    num = 0

    vertices = [v for v in graph2.vertices if v.colornum == color_class]

    for y in vertices:
        col[color_class] = []
        col[color_class].append(x)
        col[color_class].append(y)
        coloring(graphs, col)
        num += countIsomorphism(graphs, col)
        col[color_class] = []

    return num


def coloring(graphs, colors):
    for graph in graphs:
        for v in graph.vertices:
            v.colornum = 0

    for color in colors:
        for v in colors[color]:
            v.colornum = color


def iteration(graph_list):
    all_vertices = []
    for graph in graph_list:
        all_vertices += graph.vertices

    patterns = {}

    while True:  # Color refinement algorithm
        highest_color = 0
        new_patterns = {}
        for vertex in all_vertices:  # Check each vertex once every iteration
            neighbourhood = identifier(vertex)
            if neighbourhood in new_patterns:
                vertex.newcolor = new_patterns[neighbourhood]
            else:
                highest_color += 1
                new_patterns[neighbourhood] = highest_color
                vertex.newcolor = highest_color
        if patterns == new_patterns:
            break
        patterns = new_patterns
        for v in all_vertices:
            v.colornum = v.newcolor


with open('testfiles/products72.grl') as f:
    L = load_graph(f, read_list=True)[0]

t1 = timeit.default_timer()
colorpartition(L)
t2 = timeit.default_timer()
print(t2 - t1)
