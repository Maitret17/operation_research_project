from parser import parser
from algorithm import balashammer, northwest, acyclic, connected, fix_degeneracy
from display import print_matrix
import os

def menu():
    while True:
        print("transportation problems file list:")
        transp_list = os.listdir("data/")
        for filename in transp_list:
            if filename.endswith(".txt"):
                name = filename[:-4]
                transp_list[transp_list.index(filename)]=name
                print(name)
            else:
                transp_list.remove(filename)
        transp_selected = 0
        print("="*80)
        while not(transp_selected in transp_list):
            print("Select a transportation problem file or type 'q' to exit :")
            transp_selected = input()
            if transp_selected.lower() == "q":
                print("Goodbye")
                return
            if (transp_selected in transp_list):
                break
            print("The transporation problem file's name is incorrect")
        print("="*80)
        n, m, cost_matrix, cost_row, provision_column = parser(transp_selected)
        print("Select which algorithm to use :\n1 - northwest\n2 - balashammer \n3-stepping stone (not implemented yet)")
        matrix=0
        algo_selected = input()
        print("="*80)
        if algo_selected == "1":
            matrix = northwest(n, m, cost_row, provision_column)
        if algo_selected == "2":
            matrix = balashammer(n, m, cost_matrix,cost_row, provision_column)
        if algo_selected == "3":
            pass
            #matrix = stepping_stone(n, m, cost_row, provision_column)
        print(matrix)
        if matrix!=0:
            print_matrix(n, m, matrix, provision_column, cost_row)
            print("")
            acyclic(n, m, matrix)
            print("")
            connected(n, m, matrix)
        print("="*80)

if __name__ == "__main__":
    menu()