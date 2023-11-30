from queue import PriorityQueue
import pygame
from os.path import exists

pygame.init()

WIDTH = 600
HEIGHT= 600

RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (15, 10, 222)
GREY = (128, 128, 128)
IRISBLUE = (0, 181, 204)
PINK = (255, 105, 180)
LIGHTGREEN = (208,242,136)
LIGHTPUR = (255,245,194)

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move your step")
font = pygame.font.Font('freesansbold.ttf', 18)
key_image = pygame.image.load("./images/key.png")
tile_font = pygame.font.Font('freesansbold.ttf', 10)

class Button:
    def __init__(self, x, y, text, click):
        self.x = x
        self.y = y
        self.text = text
        self.click = click
        self.draw()
        
    def draw(self):
        text_button = font.render(self.text, True, BLACK)
        button = pygame.rect.Rect((self.x, self.y), (120, 50))
        if self.click:
            pygame.draw.rect(window, GREEN, button, 0,5)
        else:
            pygame.draw.rect(window, IRISBLUE, button, 0,5)
        window.blit(text_button,(self.x +20, self.y + 15))
    
    def is_click(self) -> bool:
        mouse = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button = pygame.rect.Rect(self.x, self.y, 120, 50)
        if(left_click and button.collidepoint(mouse)):
            return True
        else:
            return False
        
    def set_click(self):
        self.click = True
        
    def remove_click(self):
        self.click = False
        
    def return_click(self) -> bool:
        return self.click

class Node:
    def __init__(self, irow, jcol, width, height, total_row, total_col,floor: int) -> None:
        self.color = WHITE
        self.neighbor=[]
        self.total_row = total_row
        self.x = irow
        self.y = jcol
        self.width = width
        self.height = height
        self.visited =[]
        self.total_col = total_col
        self.text = ""
        self.floor = floor
        self.is_door = False
    
    def get_floor(self):
        return self.floor
    
    def set_floor(self, f):
        self.floor = f
    
    def get_pos(self):
        return self.x, self.y
        
    def draw(self, window,cur_floor):
        if(self.floor == cur_floor):
            pygame.draw.rect(window, self.color, (self.y * self.width, self.x * self.height + 100, self.width, self.height + 100))
            text_surface = tile_font.render(self.text, True, BLACK)
            text_rect = text_surface.get_rect(center=((self.y * self.width) + self.width // 2, (self.x * self.height + 100) + self.height // 2))
            window.blit(text_surface, text_rect)

    def set_barrier_color(self):
        self.color = BLACK
    
    def set_end_color(self):
        self.color = BLUE
        
    def set_start_color(self):
        self.color = RED
    
    def set_nodeOpen_color(self):
        self.color = GREEN
        
    def set_nodeVisited_color(self):
        self.color = YELLOW
        
    def set_path_color(self):
        self.color = RED
    
    def set_unvisible(self):
        self.color =IRISBLUE

    def set_key(self):
        self.color = PINK

    def set_door(self):
        self.color = GREY
        self.is_door = True
        
    def set_UP(self):
        self.color = LIGHTGREEN
    
    def set_DO(self):
        self.color = LIGHTPUR
        
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == RED
    
    def is_end(self):
        return self.color == BLUE
    
    def is_UP(self):
        return self.color == LIGHTGREEN
    
    def is_DO(self):
        return self.color == LIGHTPUR
    
    def searchUP(self,grid,fl):
        for i in grid[fl+1]:
            for node in i:
                if(node.is_DO()):
                    print("find DO")
                    return node
    
    def searchDO(self,grid,fl):
        for i in grid[fl-1]:
            for node in i:
                if(node.is_UP()):
                    return node
    
    def neighbors(self, grid, collected_key, check_door):
        cur_floor = self.floor
        self.neighbor = []
        direct = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dir in direct:
            new_x = self.x + dir[0]
            new_y = self.y + dir[1]
            check = True
            
            if (0 <= new_x < self.total_row and 0 <= new_y < self.total_col):
                if abs(dir[0]) == abs(dir[1]):
                    if grid[cur_floor][self.x][new_y].is_barrier() or grid[cur_floor][new_x][self.y].is_barrier() or grid[cur_floor][new_x][new_y].is_barrier():
                        check = False                   
                    
                    if check_door ==True:
                        if grid[cur_floor][new_x][self.y].is_door:
                            key = "K" + str(grid[cur_floor][new_x][self.y].text[1])
                            if key not in collected_key:
                                check = False

                        if grid[cur_floor][self.x][new_y].is_door:
                            key = "K" + str(grid[cur_floor][self.x][new_y].text[1])
                            if key not in collected_key:
                                check = False
                        
                        if grid[cur_floor][new_x][new_y].is_door:
                            key = "K" + str(grid[cur_floor][new_x][new_y].text[1])
                            if key not in collected_key:
                                check = False

                else:
                    if grid[cur_floor][new_x][new_y].is_barrier():
                        check = False
                    
                    if check_door == True:
                        if grid[cur_floor][new_x][new_y].is_door:
                            key = "K" + str(grid[cur_floor][new_x][new_y].text[1])
                            if key not in collected_key:
                                check = False

            else: check = False

            if check == True:
                if grid[cur_floor][new_x][new_y] not in self.neighbor:
                    #self.neighbor.append(grid[cur_floor][new_x][new_y])
                    if(grid[cur_floor][new_x][new_y].is_UP()):
                        temp_node = self.searchUP(grid,cur_floor)
                        if temp_node not in self.neighbor:
                            self.neighbor.append(temp_node)
                    elif grid[cur_floor][new_x][new_y].is_DO():
                        temp_node = self.searchDO(grid,cur_floor)
                        if temp_node not in self.neighbor:
                            self.neighbor.append(temp_node)
                    else:
                        self.neighbor.append(grid[cur_floor][new_x][new_y])

    def __lt__(self, other):
        return False


def read_grid_from_file():
    i =0
    grid = []
    row ={}
    column = {}
    
    while i>=0:
        file = 'gridd'+str(i+1)+'.txt' 
        print(file)
    
        if exists(file) == False:
            print("File does not exist")
            break
    
        with open(file,'r') as file:
            row[i] , column[i] = map(int, file.readline().strip().split(','))
            floor = file.readline().strip().split(',')
            
            grid.append([[0] * column[i] for _ in range(row[i])])
            
            for j in range(row[i]):
                data = file.readline().strip().split(',')
                grid[i][j] = data
        i += 1
    return row, column, i, grid

def make_grid_color(row, col, width, height, grid,floor):
    grid_color = []
    start = None
    end = None
    for k in range(floor):
        nrow = row[k]
        ncol = col[k]
        grid_color.append([[0] * ncol for _ in range(nrow)])
        for i in range(nrow):
            for j in range(ncol):
                node = Node(i, j, width // ncol, height // nrow, nrow, ncol,k)

                if(grid[k][i][j] == "A1"):
                    node.set_start_color()
                    start = node

                if(grid[k][i][j] == "T1"):
                    node.set_end_color()
                    end = node

                if(grid[k][i][j] == "-1"):
                    node.set_barrier_color()

                if(grid[k][i][j].startswith("K")):
                    node.set_key()
                    node.text = str(grid[k][i][j])
                if(grid[k][i][j].startswith("UP")):
                    node.set_UP()
                    node.text = str(grid[k][i][j])
                if(grid[k][i][j].startswith("OW")):
                    node.set_DO()
                    node.text = str(grid[k][i][j])
                if(grid[k][i][j].startswith("D")):
                    node.set_door()
                    node.text = str(grid[k][i][j])
                    
                grid_color[k][i][j]=node
                   
    return grid_color, start, end 

def draw_grid_line(window, rows, cols, width, height):
    gap1 = height // rows
    gap2 = width // cols
 
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * gap1 + 100), (width-(width-cols*gap2), i * gap1 +100))
        for j in range(cols):
            pygame.draw.line(window, GREY, (j * gap2, 100), (j * gap2, height+100))
    
    pygame.draw.line(window, GREY, (cols * gap2, 100), (cols * gap2, height+100))

def draw_update(window, grid, rows, cols, width, height,cur_floor): 
    for i in grid[cur_floor]:
        for node in i:
            node.draw(window,cur_floor)
            
    draw_grid_line(window, rows[cur_floor], cols[cur_floor], width, height)
    pygame.display.update()

def draw_solution(come, current, draw,row, col, width, height, start, grid,floor):
    path = {}
    print("t")
    while current in come:   
        path[come[current]] = current
        current = come[current]

    while start in path:
        if(start.get_floor() != floor):
            draw_update(window,grid,row, col, width, height,start.get_floor())
        pygame.time.delay(5000)
        start.set_unvisible()
        start = path[start]
        start.set_path_color()
        draw()

def heuristic(start, end, start_floor, end_floor):
    x1, y1 = start
    x2, y2 = end
    return abs(x1 - x2) + abs(y1 - y2) + abs(start_floor-end_floor)^2

def astar_algorithm(draw,row, col, width, height, grid, start, end, floor):
    count = 0
    frontier = PriorityQueue()
    frontier.put((0, count, start))
    come = {}
    g_cost ={node: float("inf") for k in range(floor) for i in grid[k] for node in i}
    g_cost[start] =0
    f_cost = {node: float("inf") for k in range(floor) for i in grid[k] for node in i}
    f_cost[start] = heuristic(start.get_pos(), end.get_pos(), start.get_floor(), end.get_floor())
    explored = {start}

    while not frontier.empty():
        current_node = frontier.get()[2]
        
        explored.remove(current_node)

        if current_node == end:

            draw_solution(come,end,draw,row, col, width, height,start,grid,start.get_floor())
            # path = {}
            # while end in come:   
            #     path[come[end]] = end
            #     end = come[end]
            # return path
        for neighbor in current_node.neighbor:
            temp_g_cost = g_cost[current_node]+1
            if temp_g_cost < g_cost[neighbor]:
                come[neighbor] = current_node
                
                g_cost[neighbor] = temp_g_cost
                f_cost[neighbor] = temp_g_cost + heuristic(neighbor.get_pos(), end.get_pos(),neighbor.get_floor(),end.get_floor())
                if neighbor not in explored:
                    count += 1
                    frontier.put((f_cost[neighbor], count, neighbor))
                    explored.add(neighbor)
                    #neighbor.set_nodeOpen_color()
        #draw()
        #if(current_node != start):
        #    current_node.set_nodeVisited_color()

    return False

def astar_algorithm_with_checkpoints(draw,  row, col, width, height, grid, checklist, collected_key,floor):
    collected_key.clear()
    for i in range(len(checklist) - 1):
        start = checklist[i]
        end = checklist[i + 1]
        count = 0
        frontier = PriorityQueue()
        frontier.put((0, count, start))
        come = {}

        g_cost ={node: float("inf") for i in grid[floor] for node in i}
        g_cost[start] =0
        f_cost = {node: float("inf") for i in grid[floor] for node in i}
        f_cost[start] = heuristic(start.get_pos(), end.get_pos(), start.get_floor(), end.get_floor())
        
        explored = {start}
        
        while not frontier.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current_node = frontier.get()[2]

            if current_node == start and current_node.text.startswith("K"):
                key = "K" + str(current_node.text[1])
                collected_key.add(key)
            explored.remove(current_node)  
            current_node.neighbors(grid, collected_key, True)
                
            if current_node == end:
                draw_solution(come, end,row, col, width, height, start,grid,start.get_floor())
                path = {}
                while end in come:   
                    path[come[end]] = end
                    end = come[end]
                continue
     
            for neighbor in current_node.neighbor:
                temp_g_cost = g_cost[current_node] + 1
                
                if temp_g_cost < g_cost[neighbor]:
                    come[neighbor] = current_node
                    
                    g_cost[neighbor] = temp_g_cost
                    f_cost[neighbor] = temp_g_cost + heuristic(neighbor.get_pos(), end.get_pos(),neighbor.get_floor(),end.get_floor())
                    if neighbor not in explored:
                        count += 1
                        frontier.put((f_cost[neighbor], count, neighbor))
                        explored.add(neighbor)
            #draw()

def recursive (draw, grid, start, end, goal_list, all_keys,floor):
    path = astar_algorithm (draw, grid, start, end,floor)
    if(path):
        for step in path:
            if step.text.startswith("D"):
                goal_list.append(step)
                key = "K" + str(step.text)[1]
                for node in all_keys:
                    if node.text == key:
                        goal_list.append(node)
                        return recursive (draw, grid, start, node, goal_list, all_keys,node.get_floor())


def main(window, width, height):
    row, col, floor, temp_grid = read_grid_from_file() 
    grid, start, end = make_grid_color(row,col,width,height,temp_grid,floor)
    goal_list = []
    all_keys = []
    click1 = False
    click4 = False
    one_press = True
    collected_key = set()
    current_floor = start.get_floor()
    run = True
    while run:
        window.fill(WHITE)
        
        astar_button = Button(10, 10, "Go", click1)
        clear_button = Button(400, 10, "Clear", click4)
        draw_update(window,grid,row,col,width,height,current_floor)
        for k in range(floor):
            for i in grid[k]:
                for node in i:
                    node.neighbors(grid,collected_key,False)     
        astar_algorithm(lambda: draw_update(window, grid, row, col, width, height,current_floor),row, col, width, height, grid,start,end,floor)
        # if(pygame.mouse.get_pressed()[0]) and one_press:
        #     one_press = False             
        #     if(astar_button.is_click()):
        #         click1 = True
        #         click4 = False
        #         clear_button.remove_click()
        #         clear_button.draw()
                
                
        #     if(clear_button.is_click()):
        #         click4 = True
        #         click1 = False
        #         # goal_list.clear()
        #         # astar_button.remove_click()
        #         # astar_button.draw()
        #         # all_keys.clear()
        #         # collected_key.clear()
        #         grid, start, end = make_grid_color(row, col, width, height, temp_grid,floor)
            
        #     if((click1)):
        #         # for tfloor in range(floor):
        #         #     for i in grid[tfloor]:
        #         #         for node in i:
        #         #             node.neighbors(grid, collected_key, False)
        #         #             if node.text.startswith("K") or node.text =="UP" or node.text =="DO" :
        #         #                 all_keys.append(node)
                
        #         # astar_button.set_click()
        #         # astar_button.draw()
        #         # recursive(lambda: draw_update(window, grid, row, col, width, height,current_floor), grid, start, end, goal_list, all_keys,floor)
                
        #         # goal_list.reverse() 
        #         # goal_list.insert(0, start)
        #         # goal_list.append(end)
        #         # for i in goal_list:
        #         #     print (i.text, end = " ")
        #         # astar_algorithm_with_checkpoints(lambda: draw_update(window, grid, row, col, width, height),  row, col, width, height, grid, goal_list, collected_key,current_floor)
        #         astar_algorithm(lambda: draw_update(window, grid, row, col, width, height,current_floor), grid,start,end,floor)
          
        # if(not pygame.mouse.get_pressed()[0]) and not one_press:
        #     one_press = True
             
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
    pygame.quit()
    
if __name__ == "__main__":
    main(window, WIDTH,HEIGHT-100)