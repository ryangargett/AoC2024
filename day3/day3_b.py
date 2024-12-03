import regex as re

def extract_valid_ops(in_string: str) -> list[list]:
    search_pattern = r"mul\((\d+),(\d+)\)"
    
    enable_flag = "do()"
    disable_flag = "don't()"
    
    sections = re.split(f"({re.escape(enable_flag)}|{re.escape(disable_flag)})", in_string)

    process_section = True
    matches = []
    
    for section in sections:
        if "don't()" in section:
            process_section = False
        elif "do()" in section:
            process_section = True
            
        if process_section:
            section_matches = re.findall(search_pattern, section)
            matches.extend([[int(num1), int(num2)] for num1, num2 in section_matches])
            
    return matches

def execute_mul(inputs: list[list]) -> int:
    result = 0
    for op in inputs:
        result += op[0] * op[1]
    
    return result
def read_data(in_path: str) -> str:
    with open(in_path, "r") as in_file:
        encoded_ops = in_file.read()
        
        return encoded_ops

encoded_ops = read_data("./day3/day3.txt")    
matches = extract_valid_ops(encoded_ops)
result = execute_mul(matches)

print(matches)
print(result)