# read in text file
import pandas as pd

data = pd.read_csv("./day1.txt", names = ["A", "B"], header = None, delimiter = "\s+")

list_a = data["A"].tolist()
list_b = data["B"].tolist()

list_a_sorted = sorted(list_a)
list_b_sorted = sorted(list_b)

list_diff = sum([abs(a - b) for a,b in zip(list_a_sorted, list_b_sorted)])
print(f"list diff: {list_diff}")