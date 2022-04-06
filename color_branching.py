from graph_io import *
from permv2 import *
from basicpermutationgroup import *
import timeit

permutations = []


def color_nbs(vertex):  # COLOR_NeighBourS
    return sorted([v.colornum for v in vertex.neighbours])


def colors_in_graph(graph):  # Give all colors for a given graph
    return sorted([v.colornum for v in graph])


def identifier(v):  # Identifier for a vertex: its own color followed by its neighbours colors, sorted
    return tuple([v.colornum] + color_nbs(v))


def colorpartition(graph_list, counting, initial_coloring=False):
    all_vertices = []
    for graph in graph_list:
        all_vertices += graph.vertices

    if not initial_coloring:  # Give every vertex the same color as the first iteration if no coloring is specified
        for vertex in all_vertices:
            vertex.colornum = 0

    iteration(graph_list)  # color refinement algorithm
    result(graph_list, counting)

    pass


def createPermutation(graphA, graphB):
    perm = []

    for vertexA in graphA.vertices:
        for vertexB in graphB.vertices:
            if vertexA.colornum == vertexB.colornum:
                perm.append([vertexA.label, vertexB.label])

    p = [None] * len(perm)
    for i in range(len(perm)):
        p[perm[i][0]] = perm[i][1]

    return p


def result(graph_list, counting):
    global permutations
    checked = []
    print(f'Sets of isomorphic graphs:   {"Number of automorphisms: " if counting else ""}')
    for i, graph1 in enumerate(graph_list):
        if graph1 in checked:
            continue

        this_set = [i]
        discrete = False
        for j, graph2 in enumerate(graph_list[i + 1:]):
            if colors_in_graph(graph1) == colors_in_graph(graph2):  # check if balanced
                if len(set(colors_in_graph(graph1))) == len(graph1):  # check if discrete
                    this_set += [i + j + 1]
                    checked.append(graph2)
                    discrete = True
                if len(set(colors_in_graph(graph1))) != len(graph1):  # if not discrete
                    graphs = [graph1, graph2]
                    isomorphic = isomorphism(graphs, {})  # enter branching algorithm

                    for graph in graph_list:
                        for v in graph.vertices:
                            v.colornum = 0

                    iteration(graph_list)  # give graphs their original stable coloring again

                    if isomorphic:  # an isomorphism is found
                        this_set += [i + j + 1]
                        checked.append(graph2)
        if not counting:
            print(this_set)
            continue

        if discrete:
            print(f'{str(this_set):<29}1')
            permutations = []
            continue

        automorphism([graph1, graph1.copy()], {})
        perm_objects = []
        for p in permutations:
            perm_objects.append(permutation(len(p), mapping=p))
        perm_objects = Reduce(perm_objects)
        # print(perm_objects)
        count = order(perm_objects)
        permutations = []
        print(f'{str(this_set):<29}{count}')


def automorphism(graphs, col, explore=True):
    global permutations
    iteration(graphs)
    graph1, graph2 = graphs[0], graphs[1]

    if colors_in_graph(graph1) != colors_in_graph(graph2):  # if not balanced
        return 0
    if len(set(colors_in_graph(graph1))) == len(graph1):  # if bijection
        p = createPermutation(graph1, graph2)
        permutations.append(p)
        return 1

    graph_color = colors_in_graph(graph1)  # get current coloring
    color_class = max(graph_color, key=graph_color.count)  # pick color class with most occurrences
    x = list(filter(lambda v: v.colornum == color_class, graph1.vertices))[0]  # get vertex in color class from graph 1

    num = 0

    vertices = [v for v in graph2.vertices if v.colornum == color_class]  # all vertices in graph 2 with color class

    for i, y in enumerate(vertices):
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

        # TODO: clean this section

        num += automorphism(graphs, col, explore)  # continue until bijection or not balanced
        if not explore and i == 0:
            col[color_class] = []
            return 0

        explore = False
        col[color_class] = []  # clear list with special vertices for new choice

    return num


def isomorphism(graphs, col):
    iteration(graphs)
    graph1, graph2 = graphs[0], graphs[1]

    if colors_in_graph(graph1) != colors_in_graph(graph2):  # if not balanced
        return False
    if len(set(colors_in_graph(graph1))) == len(graph1):  # if bijection
        return True

    graph_color = colors_in_graph(graph1)  # get current coloring
    color_class = max(graph_color, key=graph_color.count)  # pick color class with most occurrences
    x = list(filter(lambda v: v.colornum == color_class, graph1.vertices))[0]  # get vertex in color class from graph 1

    vertices = [v for v in graph2.vertices if v.colornum == color_class]  # all vertices in graph 2 with color class
    col[color_class] = []

    for y in vertices:
        # give new initial coloring
        col[color_class].append(x)
        col[color_class].append(y)

        for graph in graphs:
            for v in graph.vertices:
                v.colornum = 0  # not chosen vertices are given 0

        for color in col:
            for v in col[color]:
                v.colornum = color  # chosen vertex x and y get new color

        if isomorphism(graphs, col):
            return True  # continue until bijection or not balanced

        col[color_class] = []  # clear list with special vertices for new choice

    return False


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


def order(H):
    if len(H) == 0:
        return 1
    if len(H) == 1:
        return len(H[0].cycles()[0])
    alpha = 0
    orbit = Orbit(H, alpha)
    while orbit == [alpha]:
        alpha += 1
        orbit = Orbit(H, alpha)
    # print(orbit, alpha, H)
    return len(orbit) * order(Stabilizer(H, alpha))

filename = str(input('What is the filename: '))
with open(filename) as f:
    L = load_graph(f, read_list=True)[0]

t1 = timeit.default_timer()
colorpartition(L, counting = True)
t2 = timeit.default_timer()
print(t2 - t1)
