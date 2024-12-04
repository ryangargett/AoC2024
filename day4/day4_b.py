import numpy as np

def read_data(in_path: str) -> list[list]:
    full_data = []
    
    with open(in_path, "r") as in_file:
        for line in in_file:
            full_data.append(list(line.strip()))
        
        return full_data
    
def get_num_matches(data: list[list]) -> int:
    num_matches = 0
    
    valid_seeds = []
    
    # 1. find any potential "A" seeds (don't exist in outermost row / col)
    
    n_rows = len(data)
    
    for row in range(1, n_rows - 1):
        n_cols = len(data[row])
        for col in range(1, n_cols - 1):
            if data[row][col] == "A":
                valid_seeds.append([row, col])

    # 2. check diagonals, if both are valid, increment num matches                
                
    for seed in valid_seeds:
        if data[seed[0] - 1][seed[1] - 1] in ["M", "S"] and data[seed[0] + 1][seed[1] + 1] in ["M", "S"] and data[seed[0] - 1][seed[1] - 1] != data[seed[0] + 1][seed[1] + 1]:
            if data[seed[0] - 1][seed[1] + 1] in ["M", "S"] and data[seed[0] + 1][seed[1] - 1] in ["M", "S"] and data[seed[0] - 1][seed[1] + 1] != data[seed[0] + 1][seed[1] - 1]:
                num_matches += 1
        
    return num_matches    
    
full_data = read_data("./day4/day4.txt")
num_matches = get_num_matches(full_data)
print(f"Num hits: {num_matches}")