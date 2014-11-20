class Link:
    def __init__(self, node, sons = None ,weight = None, depth = None):
        self.node = node
        self.weight = weight if weight is not None else 0
        self.sons = sons if sons is not None else []
        self.depth = depth if depth is not None else 0


def new_reduce_graph(graph, start, max_depth, max_links = None):
    """
    reduce_graph will return the a subgraph of \'graph\', obtained by start and following \'max_links\' up to depth \'max_depth\'
    """
    if start not in graph:
        return None
    to_visit = [Link(start, depth = 0)]
    #reduced = {}
    visited = []
    #i = 0
    while to_visit: #and i <=10:
        #i+=1
        page = to_visit.pop(0)
        #print ('page is ',page.node)#,'and to visit is ',[(l.node, l.depth) for l in to_visit])
        #print('visited ',[n.node for n in visited])
        #print('  reduced is: ',reduced)

        if page.depth >= max_depth:
            #print (page.node, "is too deep")
            try:
                page.weight = len(graph[page.node])
            except KeyError:
                page.weight = 0
            #print('**** appending and then continue ',page.node)
            #if page.node in [n.node for n in visited]:
            #    print ("\n",page.node,"\n")
            visited.append(page)
            continue

        elif page.node in [name.node for name in visited]:
            #i +=1
            #print(page.node,"already visited")
            pass
            #print("not continued in if")
        else:
            #print("not continued in else")
            #print('\tvisting page:', page.node)
            try:
                #Putting str(l) to ensure compatibility with imported json files
                links = [Link(str(l), depth = page.depth + 1) for l in graph[page.node][:max_links]]
                weight = len(graph[page.node])
                page.weight = weight
                page.sons = links
                page.weight = len(graph[page.node])
                #print ('\tweight is ', page.weight)
                #print('\tlinks are:', [(l.node, l.depth) for l in links])
                #reduced[page.node] = [l.node for l in links]
                #print('\treduced is:', reduced)
                to_visit.extend(links)
                #print('**** appending in try ',page.node)
                #if page.node in [n.node for n in visited]:
                #    print ("\n",page.node,"\n")
                visited.append(page)
                #print('\tto visit are:', [(l.node, l.depth) for l in to_visit])

            except KeyError:
                #print('passing',i)
                #i +=1
                page.weight = 0
                #print('**** appending in except ',page.node)
                #if page.node in [n.node for n in visited]:
                #    print ("\n",page.node,"\n")
                visited.append(page)
                #reduced[page.node] = []
    return visited


def new_reduce_graph_2(graph, start, max_depth, max_links = None):

    if start not in graph:
        return None

    to_visit = [Link(start, depth = 0)]
    visited = {}
    while to_visit:
        page = to_visit.pop(0)

        if page.depth >= max_depth:
            # we don't need to traverse this node, just save the number of links
            # in the original graph, if any
            try:
                page.weight = len(graph[page.node])
            except KeyError:
                page.weight = 0

            # let's make sure we will not visit this node again
            visited[page.node] = page
            continue

        else:
            # we are visiting a new node
            try:
                # str(l) to ensure compatibility with imported json files
                # saving tops max_links links
                links = [Link(str(l), depth = page.depth + 1) for l in graph[page.node][:max_links]]
                # number of links in the original graph
                page.weight = len(graph[page.node])
                page.sons = links
                visited[page.node] = page
                to_visit.extend([l for l in links if l.node not in visited])


            except KeyError:
                # this node in not present in the original graph
                page.weight = 0
                visited[page.node] = page

    return visited



def find_all_links(graph,start):
    to_visit = [start]
    visited = []
    i = 0
    while to_visit:
        page = to_visit.pop(0)
        if page in visited:
            #print(page,"already visited")
            pass
        else:
            #print('visting page:', page)
            try:
                links = graph[page]
                #print('links are:', links)
                visited.append(page)
                #print('visited are:', visited)
                to_visit.extend(links)
                #print('to visit are:', to_visit)

            except KeyError:
                visited.append(page)
    return visited





def find_links(graph, start, max_depth, max_links = None):
    to_visit = [[start,0]]
    visited = []
    i = 0
    while to_visit:
        page,i = to_visit.pop(0)
        #print('at the beginning i: ',i)

        if page in visited or i > max_depth:
            #print(page,"already visited")
            pass
        else:
            #print('\tvisting page:', page)
            try:

                links = [[l,i+1] for l in graph[page][:max_links]]
                #print('\tlinks are:', links)
                visited.append(page)
                #print('\tvisited are:', visited)
                to_visit.extend(links)
                #print('to visit are:', to_visit)

            except KeyError:
                #print('passing',i)
                visited.append(page)
    return visited





def find_path(graph, first, last, max_depth):
    to_visit = [[first]]
    visited = []
    if first not in graph:
        print (first,'is not in the graph')
        return None
    if last not in graph:
        print (last,'is not in the graph')
        return None
    while to_visit:
        path = to_visit.pop(0)
        current = path[-1]
        if len(path) > max_depth:
            return None
        elif current in visited:
            pass
        elif current == last:
            return path
        else:
            visited.append(current)
            for link in graph.get(current,[]):
                new_path = path[:]
                new_path.append(link)
                to_visit.append(new_path)


def reduce_graph(graph, start, max_depth, max_links = None):
    """
    reduce_graph will return the a subgraph of \'graph\', obtained by start and following \'max_links\' up to depth \'max_depth\'
    """
    to_visit = [[start,0]]
    reduced = {}
    i = 0
    while to_visit:
        page,i = to_visit.pop(0)
        #print('at the beginning i: ',i)
        if page in reduced or i > max_depth-1:
            #print(page,"already visited")
            pass
        else:
            #print('\tvisting page:', page)
            try:
                links = [[l,i+1] for l in graph[page][:max_links]]
                #print('\tlinks are:', links)
                reduced[page] = [link[0] for link in links]
                #print('reduced is:', reduced)
                to_visit.extend(links)
                #print('to visit are:', to_visit)

            except KeyError:
                #print('passing',i)
                reduced[page] = []
    return reduced



if __name__ == '__main__':

    graph = {
        '1': ['2', '3', '4'],
        '2': ['5', '6'],
        '5': ['9', '10','1'],
        '4': ['7', '8'],
        '7': ['11', '12']
        }



    graph2 = {
        '1': ['2', '3', '4'],
        '2': ['5','11','12','13','14','15'],
        '3' : ['6','7'],
        '5': ['6', '8'],
        '4': ['7'],
        '7': ['9', '10']
        }

    graph3 = {
        '1': ['2', '3', '4'],
        '2': ['5','11','12','13','14','15'],
        '3' : ['6','7','66','77'],
        '5': ['6', '8','66','77'],
        '4': ['7','66','77'],
        '7': ['9', '10']
        }

    print()
    print('visit all link starting at 1 ',find_all_links(graph,'1'))
    print()
    print('visit all link at depth 2 starting at 1 ',find_links(graph2,'1',2, max_links=10))
    print()
    print('find path between 1 and 6 ',find_path(graph2,'1','6',5))
    print()
    print('reducing graph', reduce_graph(graph3, '1',2,max_links=2))

"""

from functools import wraps

def memo(f):
     Memoizing decorator for dynamic programming.
    @wraps(f)
    def func(*args):
        if args not in func.cache:
            func.cache[args] = f(*args)
        return func.cache[args]
    func.cache = {}
    return func

@memo
def factorial(num):
    Recursively calculate num!.
    if num < 0:
        raise ValueError("Negative numbers have no factorial.")
    elif num == 0:
        return 1
    return num * factorial(num-1)


"""

