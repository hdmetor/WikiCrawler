

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


