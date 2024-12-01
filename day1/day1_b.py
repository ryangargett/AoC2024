import pandas as pd

data = pd.read_csv("./day1.txt", names = ["A", "B"], header = None, delimiter = "\s+")

list_a = data["A"].tolist()
list_b = data["B"].tolist()

list_a_sorted = sorted(list_a)
list_b_sorted = sorted(list_b)

total_sim = 0

for aa in list_a_sorted:

    sim = 0
    
    for bb in list_b_sorted:
        if aa == bb:
            sim += 1
            
        elif bb > aa:
            break # can stop checking early as the lists are already sorted
            
    total_sim += sim * aa
    
print(f"similarity: {total_sim}")