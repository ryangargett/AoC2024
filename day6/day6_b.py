from day6_a import Lab, Node
class InfiniteLab(Lab):
    def __init__(self, raw_map: list[list]):
        self.obstacles = []
        self.valid_starts = []
        super().__init__(raw_map)
        
        self.legal_moves: list = [ # e.g. up, right, down, left (in ref. to a coord system starting at the topmost row)
            {
                "change": (-1, 0),
                "denotion": "|"
            },
            {
            
                "change": (0, 1),
                "denotion": "-"
            },
            {
        
                "change": (1, 0),
                "denotion": "|"
            },
            {
        
                "change": (0, -1),
                "denotion": "-"
            }
        ]
        
        print(self.obstacles)
        #self.valid_starts = self.get_valid_starts() 

    def build(self, raw_map: list[list]) -> list[list]:
        
        processed_map = []
        
        for row_idx, row in enumerate(raw_map):
            processed_row = []
            if "^" in row: # check for predetermined starting position
                self.valid_starts.append((row.index("^"), row_idx))
            for cell_idx, cell in enumerate(row):
                if cell == "#":
                    self.obstacles.append((cell_idx, row_idx))
                processed_row.append(Node(row_idx, cell_idx, cell))
            
            processed_map.append(processed_row)
            
        return processed_map
    
    def reset(self):
        
        for row in self.map:
            for cell in row:
                cell.set_visited(False)
                if cell.get_type() != "#":
                    cell.set_type(".")
                    
    def _move_player(self, curr_x: int, curr_y: int, move_idx: int) -> tuple[int, int]:
        
        movement = self.legal_moves[move_idx]
        
        new_y = curr_y + movement["change"][0]
        new_x = curr_x + movement["change"][1]
        
        return (new_x, new_y)
    
    def _filter_route(self, curr_x: int, curr_y: int, move_idx: int) -> bool:
 
        valid_route = False
        
        for obstacle in self.obstacles:
            if ((move_idx == 0 and curr_y == obstacle[1] and curr_x < obstacle[0]) or
                (move_idx == 1 and curr_x == obstacle[0] and curr_y < obstacle[1]) or
                (move_idx == 2 and curr_y == obstacle[1] and curr_x > obstacle[0]) or
                (move_idx == 3 and curr_x == obstacle[0] and curr_y > obstacle[1])):
                
                valid_route = True
                break        
                
        return valid_route
    
    def find_loops(self) -> None:
        
        for start_pos in self.valid_starts:
            
            self.reset()
            
            route = []
            valid_placements = []
            obstacle_placements = set()
            
            curr_x = start_pos[0]
            curr_y = start_pos[1]
            
            move_idx = 0
            loop_check = True
            append_to_route = True
            
            if self._filter_route(curr_x, curr_y, move_idx) is True:
                valid_placements.append((curr_x, curr_y, move_idx))
            
            num_loops = 0
            
            self.map[curr_y][curr_x].set_visited(True)
            self.map[curr_y][curr_x].set_type(f"\033[32m{'|'}\033[0m")
            
            self.display_map(in_place = False)
            
            while loop_check:
                
                new_x, new_y = self._move_player(curr_x, curr_y, move_idx)
                
                if self.has_escaped(new_x, new_y):
                    
                    # if we escape, we need to incrementally check along the path we just took whether adding a new obstacle results in a loop
                    
                    print(f"escaped bounds, retrying route....")
                    self.reset()

                    new_x = start_pos[0]
                    new_y = start_pos[1]
                    move_idx = 0
                                        
                    append_to_route = False
                    not_valid = True
                    
                    while not_valid and len(valid_placements) != 0:
                        
                        pos = valid_placements.pop()
                        obstacle_x, obstacle_y = self._move_player(pos[0], pos[1], pos[2])
                        
                        if not self.has_escaped(obstacle_x, obstacle_y) and self.map[obstacle_y][obstacle_x].get_type() != "#" and (obstacle_x, obstacle_y) not in obstacle_placements:
                            not_valid = False
                            
                    if len(valid_placements) == 0:
                        print(f"exhausted all routes, resetting....")
                        self.reset()
                        break
 
                    self.map[obstacle_y][obstacle_x].set_type("O")
                    route = []
                
                if self.map[new_y][new_x].get_type() in ["#", "O"]:
                    move_idx = (move_idx + 1) % len(self.legal_moves) # repeat movement list if end movement pattern is reached
                    new_x = curr_x
                    new_y = curr_y
                    
                else:
                    
                    if (new_x, new_y, move_idx) in route and (obstacle_x, obstacle_y) not in obstacle_placements:
                        
                        num_loops += 1 
                        
                        print(f"found infinite loop ({num_loops} total)!")
                        self.display_map(in_place = False)
                        self.reset()
                        obstacle_placements.add((obstacle_x, obstacle_y))
                                    
                        new_x = -1
                        new_y = start_pos[1]
                        move_idx = 0
                        route = []
                    
                curr_x = new_x
                curr_y = new_y
                
                if append_to_route:
                    if self._filter_route(curr_x, curr_y, move_idx) is True:
                        valid_placements.append((curr_x, curr_y, move_idx))
                        
                route.append((curr_x, curr_y, move_idx))
                    
                if self.map[curr_y][curr_x].get_visited() is False:
                    self.map[curr_y][curr_x].set_visited(True)
                    
                    if self.map[curr_y][curr_x].get_type() not in ["#"]:
                        
                        if curr_x == start_pos[0] and curr_y == start_pos[1]:
                            move_type = f"\033[32m{'|'}\033[0m"
                        else:
                            move_type = self.legal_moves[move_idx]["denotion"]
                        
                        self.map[curr_y][curr_x].set_type(move_type)
                        
                #self.display_map(in_place=False)
                    
        print(f"discovered {len(obstacle_placements)} unique solutions")
                        
def read_data(in_path: str) -> tuple[list[list], int, int]:
    
    raw_data = []
    
    with open(in_path, "r") as in_file:
        for line in in_file:
            processed_line = line.strip()
            raw_data.append(processed_line)
            
    return raw_data

if __name__ == "__main__":
    raw_mapping = read_data("./day6/day6.txt")
    lab = InfiniteLab(raw_mapping)
    lab.display_map()
    lab.find_loops()