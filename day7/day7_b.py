import itertools

def read_data(in_path: str) -> list[list]:
    
    processed_data = []
     
    with open(in_path, "r") as in_file:
        for line in in_file:
            lhs, rhs = line.strip().split(":")
            lhs = int(lhs)
            rhs = [int(val) for val in rhs.split()]
            processed_data.append((lhs, rhs))
            
    return processed_data

def add(num1: int, num2: int) -> int:
    return num1 + num2

def product(num1: int, num2: int) -> int:
    return num1 * num2

def concat(num1: int, num2: int) -> int:
    return int(f"{num1}{num2}")

def eval_equation(operands: list, rhs: list):
    result = rhs[0]
    for operand, value in zip(operands, rhs[1:]):
        result = operand(result, value)
        
    return result

def get_valid_total(equations: list) -> int:
    
    valid_total = 0
    valid_operands = [add, product, concat]
    
    operand_text_conversion = {
        add: "+",
        product: "*",
        concat: "||"
    }
    
    for lhs, rhs in equations:
        for operands in itertools.product(valid_operands, repeat = len(rhs) - 1):
            if eval_equation(operands, rhs) == lhs:
                equation_text = str(rhs[0])
                for operand, value in zip(operands, rhs[1:]):
                    equation_text += f" {operand_text_conversion[operand]} {value}"
                print(f"Solution found: {lhs} = {equation_text}")
                valid_total += lhs
                break
            
    return valid_total
        
if __name__ == "__main__":
    processed_data = read_data("./day7/day7.txt")
    print(processed_data)
    valid_total = get_valid_total(processed_data)
    print(f"final valid total: {valid_total}")