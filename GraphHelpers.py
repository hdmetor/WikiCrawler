class Link:
    def __init__(self, node, sons = None ,weight = None, depth = None):
        self.node = node
        self.weight = weight if weight is not None else 0
        self.sons = sons if sons is not None else []
        self.depth = depth if depth is not None else 0


def reduce_graph(graph, start, max_depth, max_links = None):
    """
    reduce_graph will return the a subgraph of \'graph\', obtained by start and following \'max_links\' up to depth \'max_depth\'
    """
    if start not in graph:
        return {}

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
                for link in links:
                    if link.node in visited:
                        link.weight = visited[link.node].weight
                        # we should update sons as well, but this information is not relevant here for now
                page.sons = links
                visited[page.node] = page
                to_visit.extend([l for l in links if l.node not in visited])

            except KeyError:
                # this node in not present in the original graph
                page.weight = 0
                visited[page.node] = page

    return visited


