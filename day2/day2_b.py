#TODO: Refactor and clean up duplicate code

def read_data(in_file: str) -> list[list]:
    
    data = []
    
    with open(in_file, "r") as in_file:
        for line in in_file:
            data.append([int(x) for x in line.split()])
        
    return data

def _check_instability(curr_level: int, prev_level: int, ascending: bool) -> bool:
    
    """Check for violations in two conditions:
    1. Changes in direction / trend between two levels
    2. Significant changes (>3) or zero changes between levels"""
    
    unstable = False
    if curr_level == prev_level or abs(curr_level - prev_level) > 3:
        unstable = True
    if ((curr_level - prev_level) > 0 and not ascending) or ((curr_level - prev_level) < 0 and ascending):
        unstable = True
    return unstable

def _check_level_group(level_group: list[int], ascending: bool) -> bool:
    
    unstable = False
    
    if _check_instability(level_group[1], level_group[0], ascending):
        unstable = True
    
    return unstable

def get_num_safe_entries(in_file: str) -> int:
    data = read_data(in_file)
    
    num_safe = 0
    
    for report in data:
        is_safe = True
        buffer_check = True
        ascending = (report[1] - report[0]) > 0
        
        orig_report = report
        
        for level_idx in range(1, len(report)):
            unstable = _check_level_group(report[level_idx - 1: level_idx + 1], ascending)  
            if unstable:
                if buffer_check:
                    problematic_level = report.pop(level_idx)
                    buffer_check = False
                    break
                
        if not buffer_check:        
            for level_idx in range(1, len(report)):
                unstable = _check_level_group(report[level_idx - 1: level_idx + 1], ascending)  
                if unstable:
                    is_safe = False
                    break
                
        orig_report.pop(0)
                
        if not buffer_check:        
            for level_idx in range(1, len(orig_report)):
                unstable = _check_level_group(report[level_idx - 1: level_idx + 1], ascending)  
                if unstable:
                    is_safe = False
                    break
        
        if is_safe and buffer_check:
            num_safe += 1
            print(f"safe! on {report}")
        elif is_safe and not buffer_check:
            num_safe += 1
            print(f"safe! on {report} by removing problematic level: {problematic_level}")
    
    print(f"safe entries: {num_safe}")
    
    
    
get_num_safe_entries("day2/day2.txt")