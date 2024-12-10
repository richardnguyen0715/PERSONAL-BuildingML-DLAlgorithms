from PL_Solution import *
import os
import sys

def read_file(filepath):
    KB = []
    elements = []
    with open(filepath, "r") as file:
        lines = file.readlines()
        for line in lines:
            elements.append(line)
    alpha = elements[0]
    num = elements[1]
    KB = elements[2:]
    return alpha, num, KB

def input_processed(alpha, num, KB):
    
    alpha = set(alpha.strip().replace(' ','').split('OR'))
    num = int(num)
    new_KB = [set(kb.strip().replace(' ', '').split('OR')) for kb in KB]
    
    # -A, -B, -C, A, B, C, ...
    def sort_literals(literals):
        return sorted(literals, key=lambda x: (x.lstrip('-'), '-' not in x))
    
    alpha_sorted = sort_literals(alpha)
    new_KB_sorted = [sort_literals(kb_clause) for kb_clause in new_KB]
    
    alpha_sorted = lit_cleaned(alpha_sorted)
    new_KB_sorted = clauses_cleaned(new_KB_sorted)
    
    return alpha_sorted, num, new_KB_sorted

def print_input(alpha, num, KB):
    print(alpha)
    print(num)
    print(KB)


def menu():
    base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_directory = os.path.join(base_directory, 'Input')
    output_directory = os.path.join(base_directory, 'Output')

    input_files = [f'input_{i}.txt' for i in range(1, 11)]
    output_files = [f'output_{i}.txt' for i in range(1, 11)]
    
    print("Select input file from the following list:")
    for idx, file_name in enumerate(input_files, start=1):
        print(f"{idx}. {file_name}")
    
    while True:
        try:
            choice = int(input("Enter the file number (1-10): "))
            if 1 <= choice <= 10:
                selected_file = os.path.join(input_directory, input_files[choice - 1])
                output_selected_file = os.path.join(output_directory, output_files[choice - 1])
                
                if not os.path.isfile(selected_file):
                    print(f"File '{selected_file}' does not exist. Please double check the path and file name.")
                    return None
                
                break
            else:
                print("Please select a number from 1 to 10.")
        except ValueError:
            print("Please enter a valid number.")
    
    alpha, num, KB = read_file(selected_file)
    
    alpha, num, KB = input_processed(alpha, num, KB)
    
    print(f"\nSelected file: {input_files[choice - 1]}")
    print(f"Alpha: {alpha}")
    print(f"The number of sentences in KB: {num}")
    print(f"KB: {KB}")


    PL_resolution_ouput(alpha, KB, output_selected_file)
