from graph_io import *
from perm import *
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

    iteration(graph_list)  # color refinement algorithm
    result(graph_list)

    pass


def createPermutation(graphA, graphB):
    permutations = []

    for vertexA in graphA.vertices:
        for vertexB in graphB.vertices:
            if vertexA.colornum == vertexB.colornum:
                permutations.append([vertexA.label, vertexB.label])


    p = [None] * len(permutations)
    for i in range(len(permutations)):
        p[permutations[i][0]] = permutations[i][1]

    return p


def result(graph_list):
    checked = []
    print('Sets of possibly isomorphic graphs:')
    for i, graph1 in enumerate(graph_list):
        if graph1 in checked:
            continue

        this_set = [i]
        for j, graph2 in enumerate(graph_list[i + 1:]):
            if colors_in_graph(graph1) == colors_in_graph(graph2):  # check if balanced
                this_set += [i + j + 1]
                if len(set(colors_in_graph(graph1))) == len(graph1):  # check if discrete
                    print(f'{this_set} 1')
                if len(set(colors_in_graph(graph1))) != len(graph1):  # if not discrete
                    graphs = [graph_list[this_set[0]], graph_list[this_set[-1]]]
                    count = countIsomorphism(graphs, {})  # enter branching algorithm

                    if count != 0:  # a isomorphism is found
                        print(str(this_set) + " " + str(count))
                        checked.append(graph2)
                    else:  # no isomorphism found
                        del this_set[-1]

                    for graph in graph_list:  # initial coloring
                        for v in graph.vertices:
                            v.colornum = 0

                    iteration(graph_list)  # give graphs their original stable coloring again

    pass


def countIsomorphism(graphs, col):
    iteration(graphs)
    graph1, graph2 = graphs[0], graphs[1]

    if colors_in_graph(graph1) != colors_in_graph(graph2):  # if not balanced
        return 0
    if len(set(colors_in_graph(graph1))) == len(graph1):  # if bijection
        p = createPermutation(graph1, graph2)
        print_permutation(p)

        #with open('output/additional1.dot', 'w') as f:
        #    write_dot(graph1, f)

        #with open('output/additional2.dot', 'w') as f:
        #    write_dot(graph2, f)

        return 1

    graph_color = colors_in_graph(graph1)  # get current coloring
    color_class = max(graph_color, key=graph_color.count)  # pick color class with most occurrences
    x = list(filter(lambda v: v.colornum == color_class, graph1.vertices))[0]  # get vertex in color class from graph 1

    num = 0

    vertices = [v for v in graph2.vertices if v.colornum == color_class]  # all vertices in graph 2 with color class

    for y in vertices:
        # give new initial coloring
        col[color_class] = []
        col[color_class].append(x)
        col[color_class].append(y)

        for graph in graphs:
            for v in graph.vertices:
                v.colornum = 0  # not chosen vertices are given 0

        for color in col:
            for v in col[color]:
                v.colornum = color  # chosen vertex x and y get new color

        num += countIsomorphism(graphs, col)  # continue until bijection or not balanced
        col[color_class] = []  # clear list with special vertices for new choice

    return num


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


with open('testfiles/Trees11.grl') as f:
    L = load_graph(f, read_list=True)[0]

t1 = timeit.default_timer()
colorpartition(L)
t2 = timeit.default_timer()
print(t2 - t1)
