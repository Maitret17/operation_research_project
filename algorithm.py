from copy import deepcopy
from utils import is_degenerate

INF = 1*10**20

def northwest(n: int, m: int, cost_row: list[int], provision_column: list[int]) -> list[list[int]]:
    transport_matrix = [[0] * m for _ in range(n)]
    i, j = 0, 0
    temp_cost_row, temp_provision_column = list(cost_row), list(provision_column)

    while i < n and j < m:
        allocation = min(temp_provision_column[i], temp_cost_row[j])
        transport_matrix[i][j] = allocation
        temp_provision_column[i] -= allocation
        temp_cost_row[j] -= allocation
        if temp_provision_column[i] == 0:
            i += 1
        if temp_cost_row[j] == 0:
            j += 1

    return transport_matrix


def total_cost(cost_matrix: list[list[int]], transport_matrix: list[list[int]]) -> int: # Takes the transport matrix and its cost_matrix to find the total cost of the proposed transport solution
    total = 0
    for i in range(len(cost_matrix)):
        for j in range(len(cost_matrix[0])):
            quantity = transport_matrix[i][j]
            if quantity == -1:
                quantity = 0
            total += cost_matrix[i][j] * quantity
    return total

def balashammer(n: int, m: int, cost_matrix: list[list[int]], cost_row: list[int], provision_column: list[int]) -> list[list[int]]:
    transport_matrix = [[0] * m for _ in range(n)]
    mat = deepcopy(cost_matrix)
    cost = deepcopy(cost_row)
    provision = deepcopy(provision_column)
    for i in range(n):
        mat[i].extend([0])
    mat.extend([[0]*(m+1)])

    def regret(l: list[int]) -> int:
        sl = set(l)
        min1 = min(sl)
        if l.count(min1)<=1 and len(l)>=2:
            sl.remove(min1)
            min2 = min(sl)
        elif len(l)<=1:
            min2 = 0
        else:
            min2 = min1
        return min2-min1

    searchinglist_n = [i for i in range(n)]
    searchinglist_m = [i for i in range(m)]

    while sum(provision) > 0 and sum(cost) > 0:
        # lines regrets
        for i in searchinglist_n:
            mat[i][m] = regret([mat[i][j] for j in searchinglist_m])
        # columns regrets
        for i in searchinglist_m:
            mat[n][i] = regret([mat[j][i] for j in searchinglist_n])

        maxindex = (searchinglist_n[0],m)
        
        for i in searchinglist_n:
            if mat[i][m] > mat[maxindex[0]][maxindex[1]]:
                maxindex = (i,m)
        for j in searchinglist_m:
            if mat[n][j] > mat[maxindex[0]][maxindex[1]]:
                maxindex = (n,j)

        def minindexlist(l:list) -> int:
            minimum = min(l)
            for i in range(len(l)):
                if l[i] == minimum:
                    return i
                    

        if maxindex[0] == n:  # largest penalty is a column one
            minindex = searchinglist_n[minindexlist([mat[i][maxindex[1]] for i in searchinglist_n])]
            transport_matrix[minindex][maxindex[1]] = min(cost[maxindex[1]],provision[minindex])
            cost[maxindex[1]] -= transport_matrix[minindex][maxindex[1]]
            provision[minindex] -= transport_matrix[minindex][maxindex[1]]
            if cost[maxindex[1]] == 0:
                for i in searchinglist_n:
                    if i != minindex:
                        transport_matrix[i][maxindex[1]] = 0
                    mat[i][maxindex[1]] = INF
                searchinglist_m.remove(maxindex[1])
            if provision[minindex] == 0:
                for i in searchinglist_m:
                    if i != maxindex[1]:
                        transport_matrix[minindex][i] = 0
                    mat[minindex][i] = INF
                searchinglist_n.remove(minindex)

        elif maxindex[1] == m:  # largest penalty is a line one
            minindex = searchinglist_m[minindexlist([mat[maxindex[0]][j] for j in searchinglist_m])]
            transport_matrix[maxindex[0]][minindex] = min(provision[maxindex[0]],cost[minindex])
            provision[maxindex[0]] -= transport_matrix[maxindex[0]][minindex]
            cost[minindex] -= transport_matrix[maxindex[0]][minindex]
            if provision[maxindex[0]] == 0:
                for i in searchinglist_m:
                    if i != minindex:
                        transport_matrix[maxindex[0]][i] = 0
                    mat[maxindex[0]][i] = INF 
                searchinglist_n.remove(maxindex[0])
            if cost[minindex] == 0:
                for i in searchinglist_n:
                    if i != maxindex[0]:
                        transport_matrix[i][minindex] = 0
                    mat[i][minindex] = INF 
                searchinglist_m.remove(minindex)

    return transport_matrix


def acyclic(n: int, m: int, transport_matrix: list[list[int]]) -> (bool):
    visited_names : list[str] =[] # To display in case of a cycle
    queue : list[tuple] = [] # Is formated as such that each element of the list takes the following form : (B,i) 
                        # - B is either a binary number that tell if the "vertice" is a provision (0) or an order (1)    
                        # - i refers to the index of the "vertice" in the cost_row or provision_column
    finished = False
    is_acyclic = True
    last_visited = [-1]
    visited_provisions = [False]*n
    visited_orders = [False]*m # These two list exist in case of a disconnected graph 

    queue.append((0,0))
    
    while is_acyclic and not(finished) and len(queue) > 0:
        if queue[0][0] == 0: # We have a "provision" vertice
            for i in range(m):
                if transport_matrix[queue[0][1]][i] != 0 and i != last_visited[0]:
                    queue.append((1,i))
                    last_visited.append(queue[0][1])
            
            name = "P" + str(queue[0][1]+1)
            if visited_provisions[queue[0][1]]:
                is_acyclic = False
            else:
                visited_provisions[queue[0][1]] = True
            visited_names.append(name)
            last_visited.pop(0)
            queue.pop(0)
        
        else: # We have an "order" vertice
            for i in range(n):
                if transport_matrix[i][queue[0][1]] != 0 and i != last_visited[0]:
                    queue.append((0,i))
                    last_visited.append(queue[0][1])
            
            name = "C" + str(queue[0][1]+1)
            if visited_orders[queue[0][1]]:
                is_acyclic = False
            else:
                visited_orders[queue[0][1]] = True
            visited_names.append(name)
            last_visited.pop(0)
            queue.pop(0)

        if len(queue) == 0:
            if len(visited_names) == m+n:
                finished = True
            else: # The graph is discontinued and we need to continue from a non visited vertice
                for i in range(n):
                    if not visited_provisions[i]:
                        queue.append((0,i))
                        break
                if len(queue) == 0:
                    for i in range(m):
                        if not visited_orders[i]:
                            queue.append((1,i))
                            break
                last_visited.append(-1)
        
    if is_acyclic:
        print("The graph is acyclic and has the following path:")
        print(visited_names)
    else:
        print("The graph has the following cycle:")
        print(visited_names)
    return is_acyclic

    
def connected(n: int, m: int, transport_matrix: list[list[int]]) -> (bool):
    subgraphs : list[list[str]] =[] # To display in case of a cycle
    queue : list[tuple] = [] # Is formated as such that each element of the list takes the following form : (B,i) 
                        # - B is either a binary number that tell if the "vertice" is a provision (0) or an order (1)    
                        # - i refers to the index of the "vertice" in the cost_row or provision_column
    finished = False
    
    last_visited = [-1]
    visited_provisions = [False]*n
    visited_orders = [False]*m # These two list exist in case of a disconnected graph 

    
    while not(finished):
        visited_names : list[str] = []
        is_complete = True

        for i in range(n):
            if not visited_provisions[i]:
                queue.append((0,i))
                break
        if len(queue) == 0:
            for i in range(m):
                if not visited_orders[i]:
                    queue.append((1,i))
                    break
        if len(queue) == 0:
            finished = True
        else : 
            last_visited.append(-1)
        
        while is_complete and len(queue) > 0:
            if queue[0][0] == 0: # We have a "provision" vertice
                for i in range(m):
                    if transport_matrix[queue[0][1]][i] != 0 and not visited_orders[i]:
                        queue.append((1,i))
                        last_visited.append(queue[0][1])
                
                name = "P" + str(queue[0][1]+1)
                visited_provisions[queue[0][1]] = True
                visited_names.append(name)
                last_visited.pop(0)
                queue.pop(0)
            
            else: # We have an "order" vertice
                for i in range(n):
                    if transport_matrix[i][queue[0][1]] != 0 and not visited_provisions[i]:
                        queue.append((0,i))
                        last_visited.append(queue[0][1])
                
                name = "C" + str(queue[0][1]+1)
                visited_orders[queue[0][1]] = True
                visited_names.append(name)
                last_visited.pop(0)
                queue.pop(0)

            if len(queue) == 0:
                if len(visited_names) == m+n:
                    finished = True
                else: # The graph is discontinued and we need to restart a new subgraph
                    is_complete = False
        subgraphs.append(visited_names)
        
    if len(subgraphs) == 1:
        print("The graph is connected and has the following path:")
        print(subgraphs[0])
    else:
        print("The graph is unconnected and is composed of the following subgraphs:")
        for i in subgraphs:
            print(i)
    return len(subgraphs) == 1


def fix_degeneracy(n: int, m: int, cost_matrix: list[list[int]], transport_matrix: list[list[int]]) -> list[list[int]]:
    while is_degenerate(n, m, transport_matrix):
        candidates = []

        for i in range(n):
            for j in range(m):
                if transport_matrix[i][j] == 0:
                    candidates.append((cost_matrix[i][j], i, j))

        candidates.sort()
        edge_add = False
        for cost, i, j in candidates:
            test_matrix = deepcopy(transport_matrix)
            test_matrix[i][j] = -1

            if acyclic(n, m, test_matrix):
                transport_matrix[i][j] = -1
                print(f"One basic edge was added at row {i+1} column {j+1}")
                edge_add = True
                break

        if not edge_add:
            raise ValueError("Could not fix degeneracy without creating a cycle")
    return transport_matrix
