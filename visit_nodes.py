graph = {
        '1': ['2', '3', '4'],
        '2': ['5', '6'],
        '5': ['9', '10','1'],
        '4': ['7', '8'],
        '7': ['11', '12']
        }



graph2 = {
        '1': ['2', '3', '4'],
        '2': ['5'],
        '3' : ['6','7'],
        '5': ['6', '8'],
        '4': ['7'],
        '7': ['9', '10']
        } 
        

def find_all_links(start):
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





def find_links(start, max_depth):
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
                
                links = [[l,i+1] for l in graph2[page]]
                #print('\tlinks are:', links)
                visited.append(page)
                #print('\tvisited are:', visited)
                to_visit.extend(links)
                #print('to visit are:', to_visit)
    
            except KeyError:
                #print('passing',i)
                visited.append(page)
    return visited





def find_path(first, last, max_depth):
    to_visit = [[first]]
    visited = []
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
            for link in graph2.get(current,[]):
                new_path = path[:]
                new_path.append(link)
                to_visit.append(new_path)

print('visit all link starting at 1 ',find_all_links('1'))
print()
print('visit all link at depth 2 starting at 1 ',find_links('1',2))
print()
print('find path between 1 and 6 ',find_path('1','6',5))


