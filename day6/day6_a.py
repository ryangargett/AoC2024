class Node:
    def __init__(self, x_coord: int, y_coord: int, type: str):
        self.x_coord: int = x_coord
        self.y_coord: int = y_coord
        self.type: str = type
        self.visited: bool = False # required when tallying the total number of spaces moved (without overlaps)
        
    def set_visited(self, new_visited: bool):
        self.visited = new_visited
        
    def get_visited(self) -> bool:
        return self.visited
    
    def set_type(self, new_type: str) -> None:
        self.type = new_type
    
    def get_type(self) -> str:
        return self.type
        
        
class Lab:
    def __init__(self, raw_map: list[list]):
        self.start_x: int = 0
        self.start_y: int = 0
        self.map: list[list] = self.build(raw_map)
        self.legal_moves: list = [ # e.g. up, right, down, left (in ref. to a coord system starting at the topmost row)
            {
                "change": (-1, 0),
                "denotion": "^"
            },
            {
            
                "change": (0, 1),
                "denotion": ">"
            },
            {
        
                "change": (1, 0),
                "denotion": "v"
            },
            {
        
                "change": (0, -1),
                "denotion": "<"
            }
        ]
        
        
    def set_start_x(self, new_start_x: int) -> None:
        self.start_x = new_start_x
        
    def get_start_x(self) -> int:
        return self.start_x
    
    def set_start_y(self, new_start_y: int) -> None:
        self.start_y = new_start_y
        
    def get_start_y(self) -> int:
        return self.start_y
        
    def build(self, raw_map: list[list]) -> list[list]:
        
        processed_map = []
        
        for row_idx, row in enumerate(raw_map):
            processed_row = []
            if "^" in row: # check for predetermined starting position
                self.set_start_x(row.index("^"))
                self.set_start_y(row_idx)
            for cell_idx, cell in enumerate(row):
                processed_row.append(Node(row_idx, cell_idx, cell))
            
            processed_map.append(processed_row)
            
        return processed_map
            
    def display_map(self):
        
        print("\n")
        
        for row in self.map:
            print(''.join(node.type for node in row))
            
    def reset(self):
        for row in self.map:
            for cell in row:
                cell.set_visited(False)
                if cell.get_type() == "^":
                    cell.set_type(".")
                
                
    def has_escaped(self, curr_x: int, curr_y: int) -> bool:
        escaped = True
        
        if curr_x > 0 and curr_y > 0 and curr_x < (len(self.map) - 1)  and curr_y < (len(self.map[curr_y]) - 1):
            escaped = False
            
        return escaped
            
    def escape(self) -> None:
        
        """Check to see whether a given starting position allows a agent to escape the Lab using the predefined movement patterns.
        """
        
        self.reset()
        
        curr_x = self.start_x
        curr_y = self.start_y
        
        move_idx = 0
        
        num_spaces = 0
        not_escaped = True
        
        while not_escaped:
            
            movement = self.legal_moves[move_idx]
            
            new_y = curr_y + movement["change"][0]
            new_x = curr_x + movement["change"][1]
            
            if self.map[new_y][new_x].get_type() == "#":
                move_idx = (move_idx + 1) % len(self.legal_moves) # repeat movement list if end movement pattern is reached
                new_x = curr_x
                new_y = curr_y
                
            curr_x = new_x
            curr_y = new_y
                
            if self.map[curr_y][curr_x].get_visited() is False:
                self.map[curr_y][curr_x].set_visited(True)
                self.map[curr_y][curr_x].set_type(movement["denotion"])
                num_spaces += 1
                
                self.display_map()
            
            if self.has_escaped(curr_x, curr_y):
                not_escaped = False
                print(f"sucessfully escaped after covering {num_spaces} steps!")       
                        
def read_data(in_path: str) -> tuple[list[list], int, int]:
    
    raw_data = []
    
    with open(in_path, "r") as in_file:
        for line in in_file:
            processed_line = line.strip()
            raw_data.append(processed_line)
            
    return raw_data
                        
raw_map = read_data("./day6/day6.txt")

lab = Lab(raw_map)
lab.escape()