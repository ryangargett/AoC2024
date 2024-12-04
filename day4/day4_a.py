import numpy as np

def read_data(in_path: str) -> list[list]:
    full_data = []
    
    with open(in_path, "r") as in_file:
        for line in in_file:
            full_data.append(list(line.strip()))
        
        return full_data
    
def _transpose_data(data: list[list]) -> list[list]:
    return np.array(data).T.tolist()

def _flip_data(data: list[list]) -> list[list]:
    return np.fliplr(np.array(data)).tolist()

def _get_diags(data: list[list]) -> list:
    data = np.array(data)
    diags = []
    
    for offset in range(-data.shape[0] + 1, data.shape[1]):
        diag = data.diagonal(offset)
        diags.append("".join(diag))
        
    return diags
    
def get_num_matches(data: list[list]) -> int:
    num_matches = 0
    
    # 1. check for "XMAS" in rows
    
    for row in data:
        joined_row = "".join(row)
        num_matches += joined_row.count("XMAS")
        num_matches += joined_row[::-1].count("XMAS")
            
    # 2. check for "XMAS" in cols by transposing
    
    data_t = _transpose_data(data)
    
    for row in data_t:
        joined_row = "".join(row)
        num_matches += joined_row.count("XMAS")
        num_matches += joined_row[::-1].count("XMAS")       
    
    # 3. check for "XMAS" in diagonals
    
    top_diags = _get_diags(data)
    
    for diag in top_diags:
        num_matches += diag.count("XMAS")
        num_matches += diag[::-1].count("XMAS")
    
    data_flipped = _flip_data(data)
    bottom_diags = _get_diags(data_flipped)
    
    for diag in bottom_diags:
        num_matches += diag.count("XMAS")
        num_matches += diag[::-1].count("XMAS")
        
    return num_matches
    
full_data = read_data("./day4/day4.txt")
num_matches = get_num_matches(full_data)
print(f"Num hits: {num_matches}")