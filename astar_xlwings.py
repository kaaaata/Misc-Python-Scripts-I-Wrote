import xlwings as xw

a = 'abcdefghijklmnopqrstuvwxyz'
maze_start = input('input start cell like "a10": ')
maze_end = input('input end cell like "t20": ')

# testing variables
y_max_bound = 40


                 
class Cell:
    def __init__(self,x,y):
        self.coordinates = x+str(y)
        self.x = x
        self.y = y
        self.color = xw.books('maze.xlsm').sheets(1).range(self.coordinates).color
        self.is_wall = True if self.color == (0,0,0) else False
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

class Astar:
    def __init__(self):
        self.openset = set()
        self.closedset = set()
        self.cells = []
        self.path = []

    def init_grid(self):
        print('cleaning map...')
        for i in a:
            for j in range(1,y_max_bound+1):
                self.cells.append(Cell(i,str(j)))
                # remove all previously drawn paths
                if self.cells[-1].color not in ((None),(0,0,0)):
                    xw.books('maze.xlsm').sheets(1).range(self.cells[-1].coordinates).color = None
        self.start = self.get_cell(maze_start)
        self.end = self.get_cell(maze_end)

    def get_cell(self,coordinates): # take coordinates, return Class object Cell
        x = a.index(coordinates[0])
        y = int(coordinates[1:])
        return self.cells[y_max_bound*x+y-1]
        
    def distance(self,start,end):
        x_distance = abs(a.index(end[0])-a.index(start[0]))
        y_distance = abs(int(end[1:])-int(start[1:]))
        return x_distance+y_distance

    def adj_cells(self,coordinates):
        # N/E/S/W
        x = coordinates[0]
        y = int(coordinates[1:])
        cells = []
        if y != 1:
            cells.append(self.get_cell(x+str(y-1)))
        if x != 'z':
            cells.append(self.get_cell(a[a.index(x)+1]+str(y)))
        if y != y_max_bound:
            cells.append(self.get_cell(x+str(y+1)))
        if x != 'a':
            cells.append(self.get_cell(a[a.index(x)-1]+str(y)))
        return cells

    def astar(self):
        self.init_grid()
        print('thinking...')
        current = self.start.coordinates
        self.openset.add(current)
        while self.openset:
            current = min(self.openset,key=lambda x:self.get_cell(x).f)
            self.openset.remove(current)
            self.closedset.add(current)
            # loop through children
            for i in self.adj_cells(current):
                if not i.is_wall and i.coordinates not in self.closedset:
                    # if the maze is solved
                    if current == self.end.coordinates:
                        while self.get_cell(current).parent != None:
                            self.path.append(current)
                            current = self.get_cell(current).parent
                        self.path.append(self.start.coordinates)
                        self.path.reverse()
                        return self.path
                    if i.coordinates in self.openset and i.g <= self.get_cell(current).g:
                        i.g = self.get_cell(current).g + 1
                        i.h = self.distance(i.coordinates,self.end.coordinates)
                        i.f = i.g + i.h
                        i.parent = current
                    else:
                        i.g = self.get_cell(current).g + 1
                        i.h = self.distance(i.coordinates,self.end.coordinates)
                        i.f = i.g + i.h
                        i.parent = current
                        self.openset.add(i.coordinates)
        # if the maze is not solvable
        return ['no solution']


def show(path):
    # color the path
    if path == ['no solution']:
        print(path)
        return
    else:
        print('path found!')
        for i in path:
            xw.books('maze.xlsm').sheets(1).range(i).color = (150,214,180)


astar = Astar()
path = astar.astar()
show(path)



