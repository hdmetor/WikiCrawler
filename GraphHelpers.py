class Node:
    def __init__(self, key, sons = None, weight = None, depth = None, time_start = None, time_stop = None):
        self.key = key
        self.weight = weight if weight is not None else 0
        self.sons = sons #if sons is not None else []
        self.depth = depth #if depth is not None else 0
        self.time_start = time_start
        self.time_stop = time_stop


def reduce_graph(graph, start, max_depth, max_links = None):
    """
    reduce_graph will return the a subgraph of \'graph\', obtained by start and following \'max_links\' up to depth \'max_depth\'
    """
    if start not in graph:
        return {}

    to_visit = [Node(start, depth = 0)]
    visited = {}
    while to_visit:
        page = to_visit.pop(0)

        # check if a page was already visited
        if page.key in visited:
            continue

        if page.depth >= max_depth:
            # we don't need to traverse this node, just save the number of links
            # in the original graph, if any
            try:
                page.weight = len(graph[page.key])
            except KeyError:
                page.weight = 0

            # let's make sure we will not visit this node again
            visited[page.key] = page
            continue

        else:
            # we are visiting a new node
            try:
                # str(l) to ensure compatibility with imported json files
                # saving tops max_links links
                links = [Node(str(l), depth = page.depth + 1) for l in graph[page.key][:max_links]]
                # number of links in the original graph
                page.weight = len(graph[page.key])
                for link in links:
                    if link.key in visited:
                        link.weight = visited[link.key].weight
                        # we should update sons as well, but this information is not relevant here for now
                page.sons = links
                visited[page.key] = page
                to_visit.extend(links)

            except KeyError:
                # this node in not present in the original graph
                page.weight = 0
                visited[page.key] = page

    return visited

def find_path(graph, first, last, max_depth = None):

    # this is a list of paths
    to_visit = [[first]]
    visited = []
    if first not in graph:
        print (first,' is not in the graph')
        return None
    if last not in graph:
        print (last,' is not in the graph')
        return None
    while to_visit:
        path = to_visit.pop(0)
        current = path[-1]
        if len(path) > max_depth:
            print (' no path found within the desired depth')
            return None
        elif current in visited:
            # the sons of this node have been already added to the queue
            # so there is no need to create another path to reach them
            pass
        elif current == last:
            return path
        else:
            visited.append(current)
            # need a default case for nodes without children
            for link in graph.get(current,[]):
                # copy the current path
                new_path = path[:]
                # add each son of the current node
                new_path.append(link)
                # append (current path + son)
                to_visit.append(new_path)


def BFS(graph, start, visited, max_depth = None, depth = None):
    global time
    global nodes
    #if visited == None:
    #    visited = set()

    if depth == None:
        depth = 0

    time += 1

    visited.add(start)
    print("inside bfs ", start)
    node = Node(start, depth = depth, time_start = time)

    try:
        for son in graph[start]:
            if son not in visited:
                BFS(graph, son, visited = visited, depth = depth +1)
    except KeyError:
        # the node has no sons
        pass

    time += 1
    node.time_stop = time
    nodes.append(node)
    return visited

def BFS_general(graph):
    visited = set()
    for key in graph:
        if key not in visited:
            BFS(graph, key, visited)


def reverse_dic(original):
    from collections import defaultdict
    rev = defaultdict(list)
    for key in original:
        for el in original[key]:
            rev[el].append(key)

    return rev

def topological_sort(graph):
    global nodes
    nodes = []
    BFS_general(graph)
    print ([node.key for node in nodes])
    return reversed(nodes)


graph = {
    'a' : ["c", "b"],
    'b' : ["d", "e"],
    'c' : ["f"],
    'd' : [],
    'e' : ['f']
}


nodes = []
time = 0
#print(BFS_general(graph))
#BFS(graph,"a",set())
#print([(node.key, node.depth, node.time_start, node.time_stop) for node in nodes])
#print("now top sort ")
print([(node.key, node.depth, node.time_start, node.time_stop) for node in topological_sort(graph)])
