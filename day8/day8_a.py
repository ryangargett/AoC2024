import random

import matplotlib.pyplot as plt

from itertools import combinations
from colorama import Fore, Style, init

class RadioTower:
    def __init__(self, x_pos: int, y_pos: int, type: str):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.type = type
        
    def get_x_pos(self) -> int:
        return self.x_pos
    
    def get_y_pos(self) -> int:
        return self.y_pos
    
    def get_type(self) -> str:
        return self.type
        
    def distance_to_neighbour(self, neighbour_tower: "RadioTower") -> tuple[int]:
        return (self.x_pos - neighbour_tower.get_x_pos(), self.y_pos - neighbour_tower.get_y_pos())
    
class Map:
    def __init__(self, processed_data: list[list]):
        self.region = processed_data
        self.towers, self.tower_types = self.find_towers()
        self.antinodes = set()
        self.cmap = self.assign_cmap() 
        
    def get_towers(self) -> dict:
        return self.towers

    def find_towers(self) -> tuple[set, dict]:
        towers = set()
        tower_types = {}
        
        for row_idx, row in enumerate(self.region):
            for col_idx, col in enumerate(row):
                if col != ".":
                    if col not in tower_types:
                        tower_types[col] = [] # create new tower type
                    
                    tower_types[col].append(RadioTower(col_idx, row_idx, col))
                    towers.add((col_idx, row_idx))
                          
        return towers, tower_types
    
    def assign_cmap(self) -> dict:
        num_colours = len(self.tower_types.items())
        cmap = plt.get_cmap("viridis", num_colours)  # Use a colormap with distinct colors
        colours = {}
        
        for idx, tower_type in enumerate(self.tower_types):
            colour = cmap(idx % cmap.N)
            r, g, b = int(colour[0] * 255), int(colour[1] * 255), int(colour[2] * 255)
            colours[tower_type] = f"\033[38;2;{r};{g};{b}m"
        
        return colours
    
    def display(self) -> None:
        print("\033[H", end="")
        print("\n")
        
        for y, row in enumerate(self.region):
            for x, cell in enumerate(row):
                if (x, y) in self.antinodes:
                    if (x, y) in self.towers:
                        print(f"{self.cmap[tower_type]}{cell}{Style.RESET_ALL}", end="")
                    else:
                        tower_type = self.region[y][x]
                        print(f"{self.cmap[tower_type]}#{Style.RESET_ALL}", end="")
                else:
                    print(cell, end="")
            print()
            
    def find_antinodes(self) -> int:
        
        for tower_type, tower_list in self.tower_types.items():
            for tower_a, tower_b in combinations(tower_list, 2): # check all combinations inside each list, and see if any antinodes exist within the bounds of the map, in which case, add them to the list of antinodes
        
                dx, dy = tower_a.distance_to_neighbour(tower_b)
                
                antinode_x = tower_b.get_x_pos() + (2 * dx)
                antinode_y = tower_b.get_y_pos() + (2 * dy)
                                
                if 0 <= antinode_x < len(self.region[0]) and 0 <= antinode_y < len(self.region):
                    self.antinodes.add((antinode_x, antinode_y))
                    if (antinode_x, antinode_y) not in self.towers:
                        self.region[antinode_y][antinode_x] = tower_type
                        
                    self.display()
                    
                dx, dy = -dx, -dy
                
                antinode_x = tower_a.get_x_pos() + (2 * dx)
                antinode_y = tower_a.get_y_pos() + (2 * dy)
                
                if 0 <= antinode_x < len(self.region[0]) and 0 <= antinode_y < len(self.region):
                    self.antinodes.add((antinode_x, antinode_y))
                    antinode = (antinode_x, antinode_y)
                    if antinode not in self.towers:
                        self.region[antinode_y][antinode_x] = tower_type
                        
                    self.display()
                    
        self.print_legend()
        return len(self.antinodes)
    
    def print_legend(self) -> None:
        print("\nMapping:")
        for tower_type, color in self.cmap.items():
            print(f"{color}#{Style.RESET_ALL} - {tower_type}")
    
def read_data(in_path: str) -> list[list]:
    
    processed_data = []
    
    with open(in_path, "r") as in_file:
        for line in in_file:
            processed_line = list(line.strip())
            processed_data.append(processed_line)
            
    return processed_data

if __name__ == "__main__":
    processed_data = read_data("./day8/day8.txt")
    map = Map(processed_data)
    num_antinodes = map.find_antinodes()
    
    print(f"discovered {num_antinodes} distinct antinodes!")