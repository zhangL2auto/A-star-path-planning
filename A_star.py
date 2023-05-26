from matplotlib import pyplot as plt
import numpy as np
import itertools

class Map:
    def __init__(self, map_data, start_x, start_y, end_x, end_y):
        self.map_data = map_data
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

class Node:
    def __init__(self, x, y, g, h, father):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.father = father

    def get_neighbors(self, map):
        x = self.x
        y = self.y
        result = []
    #上
        if (x !=0 and map.map_data[x-1][y] != 0):
            up_node = Node(x-1,y,self.g+10,(abs(x-1-map.end_x)+abs(y-map.end_y))*10,self)
            result.append(up_node)
    #下
        if(x!=len(map.map_data)-1 and map.map_data[x+1][y]!=0):
            downNode = Node(x+1,y,self.g+10,(abs(x+1-map.end_x)+abs(y-map.end_y))*10,self)
            result.append(downNode)
    #左
        if(y!=0 and map.map_data[x][y-1]!=0):
            leftNode = Node(x,y-1,self.g+10,(abs(x-map.end_x)+abs(y-1-map.end_y))*10,self)
            result.append(leftNode)
    #右
        if(y!=len(map.map_data[0])-1 and map.map_data[x][y+1]!=0):
            rightNode = Node(x,y+1,self.g+10,(abs(x-map.end_x)+abs(y+1-map.end_y))*10,self)
            result.append(rightNode)
    #西北  14
        if(x!=0 and y!=0 and map.map_data[x-1][y-1]!=0 ):
            wnNode = Node(x-1,y-1,self.g+14,(abs(x-1-map.end_x)+abs(y-1-map.end_y))*10,self)
            result.append(wnNode)
    #东北
        if(x!=0 and y!=len(map.map_data[0])-1 and map.map_data[x-1][y+1]!=0 ):
            enNode = Node(x-1,y+1,self.g+14,(abs(x-1-map.end_x)+abs(y+1-map.end_y))*10,self)
            result.append(enNode)
    #西南
        if(x!=len(map.map_data)-1 and y!=0 and map.map_data[x+1][y-1]!=0 ):
            wsNode = Node(x+1,y-1,self.g+14,(abs(x+1-map.end_x)+abs(y-1-map.end_y))*10,self)
            result.append(wsNode)
    #东南
        if(x!=len(map.map_data)-1 and y!=len(map.map_data[0])-1 and map.map_data[x+1][y+1]!=0 ):
            esNode = Node(x+1,y+1,self.g+14,(abs(x+1-map.end_x)+abs(y+1-map.end_y))*10,self)
            result.append(esNode)
        return result
    
    def has_node(self, work_list):
        return any((n.x == self.x and n.y == self.y) for n in work_list)
    
    def change_g(self, work_list):
        for n in work_list:
            if n.x == self.x and n.y == self.y and n.g > self.g:
                n.g == self.g

class Astar:
    def __init__(self, map:Map):
        self.map = map

    def get_key_for_sort(self, element:Node):
        return element.g #element#不应该+element.h，否则会穿墙
    
    def solve_star(self):
        start_node = Node(self.map.start_x, self.map.start_y, 0, 0, None)
        open_list = []
        closed_list = [start_node]
        current_node = start_node

        while((self.map.end_x, self.map.end_y) != (current_node.x, current_node.y)):
            work_list = current_node.get_neighbors(self.map)
            for n in work_list:
                if n not in closed_list:
                    if(n.has_node(open_list)):
                        n.change_g(open_list)
                    else:
                        open_list.append(n)
            open_list.sort(key = self.get_key_for_sort)
            current_node = open_list.pop(0)
            closed_list.append(current_node)

        return current_node
    
    def save_path(self, current_node):
        path = []
        while(current_node.father != None):
            path.append((current_node.x, current_node.y))
            current_node = current_node.father

        path.append((current_node.x, current_node.y))
        path.reverse()

        return path
    
    def plot_path(self, path):
        # Plot
        plt.figure("Path")
        plt.xlim(0, len(my_map))
        plt.ylim(0, len(my_map[0]))
        plt.grid(True, axis='both')
        plt.xticks(np.arange(-1,len(my_map),1))
        plt.yticks(np.arange(-1,len(my_map[0]),1))

        for x, y in itertools.product(range(len(my_map)-1), range(len(my_map[0])-1)):
            if my_map[x][y] == 0:
                plt.scatter(x, y, c = 'b')
                plt.pause(0.1)
        plt.plot([self.map.start_x, self.map.end_x], [self.map.start_y, self.map.end_y], 'o', color='red')
        for v in path:
            plt.pause(1)   
            plt.plot(v[0], v[1], 'o', color='green')
        plt.plot([v[0] for v in path], [v[1] for v in path], color = 'red')
        plt.show()
    
if __name__ == "__main__":
    my_map = [
    [1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1]
    ]
    start_x , start_y = 0, 0
    end_x, end_y = 8, 15
    map = Map(my_map,start_x, start_y, end_x, end_y)

    a_star = Astar(map)
    node = a_star.solve_star()
    path = a_star.save_path(node)
    a_star.plot_path(path)
