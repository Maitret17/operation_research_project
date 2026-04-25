from copy import deepcopy

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
            total += cost_matrix[i][j] * transport_matrix[i][j]
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
