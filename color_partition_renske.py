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
    else:   # Select a vertex for individualization reffinment
        print(create_color_groups(graph_list[0].vertices))

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

    result(graph_list)
    pass

def result(graph_list):
    checked = []
    print('Sets of possibly isomorphic graphs:')
    for i, graph1 in enumerate(graph_list):
        if graph1 in checked:
            continue
        discrete = (len(set(colors_in_graph(graph1))) == len(graph1))

        this_set = [i]
        for j, graph2 in enumerate(graph_list[i + 1:]):
            if colors_in_graph(graph1) == colors_in_graph(graph2):
                checked.append(graph2)
                this_set += [i + j + 1]

        if discrete:
            print(f'{this_set} discrete')
        else:
            graph_next_iteration = []
            for i in this_set:
                graph_next_iteration.append(graph_list[i])
            colorpartition(graph_next_iteration, True)
            print(this_set)
    pass


def create_color_groups(vertices):
    color_groups = {}
    for v in vertices:
        vertex_color = v.colornum
        if vertex_color in color_groups.keys():
            color_groups[vertex_color].append(v)
        else:
            color_groups[vertex_color] = [v]

    return color_groups


with open('testfiles/SignOffColRefFri1.grl') as f:
    L = load_graph(f, read_list=True)[0]
t1 = timeit.default_timer()
colorpartition(L)
t2 = timeit.default_timer()
print(t2-t1)