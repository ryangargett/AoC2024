#TODO: Significantly improve efficiency of search algorithm

import regex as re
import statistics as st

def validate_update(update: list, valid_rules: list) -> bool:
    
    """Validates a given update (checks to ensure all page ordering rules are being correctly followed)

    Returns:
        is_valid (bool): whether the update abides by all provided ordering rules
    """

    rule_exceptions = []
    is_valid = True

    for before, after in valid_rules:
        if before in update and after in update:
            if update.index(before) > update.index(after):
                rule_exceptions.append(f"{before}|{after}")

    if len(rule_exceptions) != 0:
         print(f"update {update} is not valid according to {len(rule_exceptions)} broken rule(s): {rule_exceptions}")
         is_valid = False
            
    return is_valid

def get_median_value(update: list) -> int:
    med_idx = int(len(update) / 2)
    return int(update[med_idx])

def get_page_value(data: dict) -> int:
    
    median_values = []
    
    for update in data["page_updates"]:
        is_valid = validate_update(update, data["ordering_rules"])
        if is_valid:
            median_values.append(get_median_value(update))
    
    print(median_values)        
            
    return sum(median_values)

def read_data(in_path: str) -> dict:
    parsed_data = {
        "ordering_rules": [],
        "page_updates": []
    }
    
    curr_section = "ordering_rules"
    
    with open(in_path, "r") as in_file:
        for line in in_file:
            cleaned_line = line.strip()
            if not cleaned_line:
                curr_section = "page_updates"
                
            processed_line = [entry for entry in re.split(r'[,\|]', cleaned_line) if entry]
            if processed_line:
                parsed_data[curr_section].append(processed_line)
        
        return parsed_data
    
data = read_data("./day5/day5.txt")
page_value = get_page_value(data)
print(f"\npage value for valid entries: {page_value}")


    