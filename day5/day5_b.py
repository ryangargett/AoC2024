import regex as re
import statistics as st

def validate_update(update: list, valid_rules: list) -> list:
    
    """Validates a given update, updating it continuously until all rules are satisfied. If a rule is not satisfied, the list is mutated and all rules are checked
    again for violations. Checks until either rules are completely satisfied.

    Returns:
        update (list): successfully mutated list of page updates to satisfy all given ordering rules
    """

    rule_exceptions = []
    update_mutated = True

    # Create a dictionary to store the index of each element in the update
    index_map = {update_value: update_idx for update_idx, update_value in enumerate(update)}

    old_update = update.copy()
    
    while update_mutated:
        update_mutated = False
        for before, after in valid_rules:
            if before in index_map and after in index_map:
                if index_map[before] > index_map[after]:
            
                    update.remove(before)
                    update.insert(index_map[after], before)
                    
                    # update the index mapping to mutate the list
                    index_map = {update_value: update_idx for update_idx, update_value in enumerate(update)}
                    rule_exceptions.append(f"{before}|{after}")
                    
                    update_mutated = True
                    

    if rule_exceptions:
        print(f"update {old_update} is not valid according to {len(rule_exceptions)} broken rule(s): {rule_exceptions} -> successfully updated to: {update}")
        
    return update

def get_median_value(update: list) -> int:
    med_idx = int(len(update) / 2)
    return int(update[med_idx])

def get_page_value(data: dict) -> int:
    
    median_values = []
    
    for update in data["page_updates"]:
        old_update = update.copy()
        validated_update = validate_update(update, data["ordering_rules"])
        if validated_update != old_update:
            median_values.append(get_median_value(validated_update))
    
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
print(f"\npage value for corrected entries: {page_value}")


    