import pygame, sys, random, time
pygame.init()

size = width, height = 800, 800
screen = pygame.display.set_mode(size, pygame.RESIZABLE)

pygame.display.set_caption("Maze Generator")

black = 0, 0, 0
green = 0, 255, 0
red = 255, 0, 0
white = 255, 255, 255
col_num, row_num = 100, 100
row = [0 for i in range(col_num)]
grid = {}
w, h = 800/col_num, 800/row_num

class cell():
    def __init__(self, j, i):
        self.x = i
        self.y = j
        self.visited = False
        self.done = False
        self.upperleft = self.x * w, self.y * h 
        self.upperright = (self.x+1) * w, self.y * h
        self.lowerleft = self.x * w, (self.y+1) * h
        self.lowerright = (self.x+1) * w, (self.y+1) * h

    def show(self, color):
        pygame.draw.rect(screen, color, (self.x * w + 1, self.y * h + 1, w - 1, h - 1), 0)
        pygame.display.update()

    '''
    Code To Destroy Walls:
        UP - pygame.draw.line(screen, color, (self.x * w + 1, self.y * h), ((self.x+1) * w - 1, self.y * h))
        DOWN - pygame.draw.line(screen, color, (self.x * w + 1, (self.y+1) * h), ((self.x+1) * w - 1, (self.y+1) * h))
        LEFT - pygame.draw.line(screen, color, (self.x * w, self.y * h + 1), (self.x * w, (self.y+1) * h - 1))
        RIGHT - pygame.draw.line(screen, color, ((self.x+1) * w, self.y * h + 1), ((self.x+1) * w, (self.y+1) * h - 1))
    '''


    def destroyup(self, visited):
        if visited:
            color = white
        else: 
            color = green
        pygame.draw.line(screen, color, (self.x * w + 1, self.y * h), ((self.x+1) * w - 1, self.y * h)) #Destroy UP

    def destroydown(self, visited):
        if visited:
            color = white
        else: 
            color = green
        pygame.draw.line(screen, color, (self.x * w + 1, (self.y+1) * h), ((self.x+1) * w - 1, (self.y+1) * h))

    def destroyleft(self, visited):
        if visited:
            color = white
        else: 
            color = green
        pygame.draw.line(screen, color, (self.x * w, self.y * h + 1), (self.x * w, (self.y+1) * h - 1))

    def destroyright(self, visited):
        if visited:
            color = white
        else: 
            color = green
        pygame.draw.line(screen, color, ((self.x+1) * w, self.y * h + 1), ((self.x+1) * w, (self.y+1) * h - 1))

class generator():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.backtrack = False
        self.stack = []
        self.complete = False

    def test(self):
        self.current_cell_x, self.current_cell_y = input().split()
        grid[self.current_cell_x][self.current_cell_y].show(red)    

    #Same For all Directions!
    def goup(self, visited):
        #Destroy Wall
        grid[self.x, self.y].destroyup(visited)
        #Move Gen
        self.y -= 1


    def godown(self, visited):
        grid[self.x, self.y].destroydown(visited)
        self.y += 1

    def goleft(self, visited):
        grid[self.x, self.y].destroyleft(visited)
        self.x -= 1

    def goright(self, visited):
        grid[self.x, self.y].destroyright(visited)
        self.x += 1

    def stay(self):
        pass


    def search_neighbors(self):
        #Check None Visited Cells
        neighbors = []
        if self.x > 0:
            lcell = grid[self.x - 1, self.y]
            neighbors.append(lcell)
        if self.x < col_num - 1:
            rcell = grid[self.x + 1, self.y]
            neighbors.append(rcell)
        if self.y > 0:
            ucell = grid[self.x, self.y - 1]
            neighbors.append(ucell)
        if self.y < row_num - 1:
            dcell = grid[self.x, self.y + 1]
            neighbors.append(dcell)
        return [cell for cell in neighbors if cell.visited == False]
    
    def investigate_cell(self):
        if grid[self.x, self.y].visited == True and self.search_neighbors() == []:
            grid[self.x, self.y].done = True
            grid[self.x, self.y].show(white)
        else:
            if grid[self.x, self.y].visited == False:
                grid[self.x, self.y].visited = True
                grid[self.x, self.y].show(green)
            self.stack.append(grid[self.x, self.y])

    def mainstream(self):
        visited0 = self.search_neighbors()
        if visited0:
            #Prioritize Breaking Walls
            return random.choice(visited0)
        if grid[self.x, self.y].visited == True and visited0 == []:
            try:
                return self.stack.pop()
            except:
                self.complete = True



for i in range(row_num):
    for j in range(col_num):
        grid[(j, i)] = cell(i, j)
        grid[j, i].show(black)

gen = generator(50, 50)

def main():
    if gen.complete == False:
        try:
            gen.investigate_cell()
            next_cell = gen.mainstream()

            lcell, rcell, ucell, dcell = None, None, None, None
            if gen.x > 0:
                lcell = grid[gen.x - 1, gen.y]
            if gen.x < col_num - 1:
                rcell = grid[gen.x + 1, gen.y]
            if gen.y > 0:
                ucell = grid[gen.x, gen.y - 1]
            if gen.y < row_num - 1:
                dcell = grid[gen.x, gen.y + 1]

            visited = next_cell.visited
            if next_cell == lcell:
                gen.goleft(visited)
            elif next_cell == rcell:
                gen.goright(visited)
            elif next_cell == ucell:
                gen.goup(visited)
            elif next_cell == dcell:
                gen.godown(visited)
            else:
                gen.stay()
            time.sleep(0.001)
        except:
            pass


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.update()
    main()