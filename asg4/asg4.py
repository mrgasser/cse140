from hashlib import new
from itertools import count
from os import sched_get_priority_max
import sys
from ast import literal_eval
import random
import fileinput
import copy
import time

# This is the file in which you need to write code for assignment 4.
# Code is to be written in python3.
# This file has the general outline and functions required for assignment 4.
# There are a total of three classes and they are described in the asg4.pdf
# and in comments above the class/function.
# You are allowed to make changes to functions in ways mentioned in the comments
# above each function.
# You are not allowed to make changes to the input files. 

#Setting the seed; don't change.
random.seed(31)


# This class is supposed to handle the Travelling Salesperson Problem and it's associated functions. To implement TSP,
# for the start and end nodes use the first node. A solution or a globally optimal is not garunteed. 
class TSP_GRAPH():

    # This is the constructor initializes the graph to be 0 at first. The entire graph can be set by passing a graph to it.
    # The graph is stored as a list of lists. The V varialbe is to track the number of vertices in the graph. 
    # If two vertices are connected the value is not 0. A 0 value indicates no connection between two vertices.
    # Since this is a weighted graph, the non 0 values indicating an edge between two vertices is the weight of that edge.
    def __init__(self, vertices  = 1):
        self.V = vertices
        self.graph  = [[0 for column in range(vertices)]\
                              for row in range(vertices)]

    # This is a helper function used to get the graph from a file. It takes a Number "N" as a parameter and appends the number to 
    # the default file name "tsp_graph_N", opens that file reads it's contents and stores it in the graph along with the number 
    # of vertices.
    # You are allowed to make changes to this function but it shouldn't be necessary.
    def get_graph(self, N = None):
        if N is not None:
            default_file_name = 'tsp_graph_'
            file_name = default_file_name + str(N) + '.txt'
            print("OPENING ", file_name)
            file_object = open(file_name)
            count = 0
            output_list=[]
            for line in file_object:
                line=line.strip('\r\n')
                count = count + 1
                output_list.append(literal_eval(line))
            self.V = count
            self.graph = output_list
        else:
            print("NO FILE PROVIDED.")


    #### Helper functions for hill_climbing

    #function to get cost of path
    #follows path through graph adding up cost
    #returns total cost
    def get_cost(self, path):
        #print("geting cost")
        cost = 0

        #loop through all nodes of path - last node
        #add up the cost of each node
        for i in range(0, len(path) - 1):
            cost += self.graph[path[i]][path[i+1]]
        return cost 

    #function to check if valid swap is acheivable
    #a swap is valid if when swaping i and j, there is still a valid path
    def swap(self, path, i, j):
        #print("swaping")
        temp = copy.deepcopy(path)

        if self.graph[temp[i-1]][temp[j]] == 0:
            return False
        if self.graph[temp[j]][temp[i+1]] == 0:
            return False
        if self.graph[temp[j-1]][temp[i]] == 0:
            return False
        if self.graph[temp[i]][temp[j+1]] == 0:
            return False

        #now perform swap
        v = temp[i]
        temp[i] = temp[j]
        temp[j] = v
        return temp #return new path with swap
        
    #Starting functionm for recursively finding path
    #calls recursive function and returns path
    #if path doenst exists, it prints message and returns False
    # reference used
    # https://www.geeksforgeeks.org/hamiltonian-cycle-backtracking-6/
    def find_path(self):
        path = []
        path.append(0) # start at vertex 0
        path_count = 1

        ans = self.find_path_rec(path, path_count) #call recursive function

        # if false was returned print path doesnt exist, otherwise return the path
        if ans[0] == False:
            print("Path does not exist")
            return False
        else:
            ans[1].append(0)
            return ans[1] 

    #recursive function to find path
    def find_path_rec(self, path, path_count):

        if path_count == self.V:
            if self.graph[path[path_count-1]][path[0]] != 0: #check if last node is adj to fisrt node
                return (True, path)
            else:
                return (False, 0)

        for v in range(1, self.V): #loop through list of vertex
            if v not in path and self.graph[path[path_count-1]][v] > 0: #if vertex is not already in path, and is neighbor, add it to the path
                path.append(v)
                
                ret = self.find_path_rec(path, path_count+1) #recursive call to find next node in path
                if ret[0] == True: #if path doesnt exist remove last node
                    return ret
                
                path.pop()
        return (False, 0)        
    
    # This function implements the Travelling Salesperson Problem using hill-climbing. 
    # You are allowed to add parameters and helper functions to achieve this functionality.
    # For start and end nodes use the first node.
    def hill_climbing(self):
        print ("Hill-climbing implementation")
        #print(self.graph)

        path = self.find_path() #find path to use for hill climbing
        if path == False:
            return
        min_cost = self.get_cost(path)

        for i in range(1, len(path) - 1):
            for j in range(1, len(path) - 1):
                new_path = self.swap(path, i, j)
                if new_path == False:
                    continue
                else:
                    new_cost = self.get_cost(new_path)
                    if new_cost <= min_cost:
                        path = new_path
                        min_cost = new_cost

        return path

    ##### Helper functions for random_hill_climbing

    #function to find random path for random hill climbing
    def find_random_path(self):
        #print("finding random path")
        path = []
        path.append(0) # start at vertex 0
        path_count = 1

        ans = self.find_random_path_rec(path, path_count) #call recursive function

        # if false was returned print path doesnt exist, otherwise return the path
        if ans[0] == False:
            print("Path does not exist")
            return False
        else:
            ans[1].append(0)
            return ans[1]
    
    #function to recursively find a random path from start to end
    def find_random_path_rec(self, path, path_count):
        
        if path_count == self.V:
            if self.graph[path[path_count-1]][path[0]] != 0: #check if last node is adj to fisrt node
                return (True, path)
            else:
                return (False, 0)

        neighbors = self.create_adj_list(path, path_count) #get list of neighbors
        for v in range(1, self.V): #loop through list of vertex

            if len(neighbors) > 0:
                r_index = random.randint(0, len(neighbors) - 1) #generate random index
                vertex = neighbors[r_index] #get vertex using random index
                path.append(vertex) #add random vertex to path
            
                ret = self.find_random_path_rec(path, path_count+1) #recursive call to find next node in path
                if ret[0] == True: #if path exist return path
                    return ret
                
                path.pop()
                neighbors.pop(r_index)
        return (False, 0)    

    def create_adj_list(self, path, path_count):
        adj_list = []
        for v in range(1, self.V): #loop through list of vertexs and build list of neigbors
                if v not in path and self.graph[path[path_count-1]][v] > 0: #if vertex is not already in path, and is neighbor, add it to the path
                    adj_list.append(v)
        return adj_list

    # This function implements the Travelling Salesperson Problem using random restart hill-climbing. 
    # You are allowed to add parameters and helper functions to achieve this functionality.        
    # For start and end nodes use the first node.
    # use the imported random modules "randint()" or "random()" function to get the random value. 
    def random_hill_climbing(self):
        print ("Random restart hill-climbing implementation")

        # do 100 iterations of random
        # return best path from iterations
        min_path = self.find_path()

        for i in range(100):
            #generate random state
            #run HC on random state
            #save and returnlowest cost path
            rand_path = self.find_random_path()
            curr_cost = self.get_cost(rand_path)

            for i in range(1, len(rand_path) - 1):
                for j in range(1, len(rand_path) - 1):
                    new_path = self.swap(rand_path, i, j)
                if new_path == False:
                    continue
                else:
                    new_cost = self.get_cost(new_path)
                    if new_cost <= curr_cost:
                        rand_path = new_path
                        curr_cost = new_cost

            if self.get_cost(rand_path) <= self.get_cost(min_path):
                min_path = rand_path

        return min_path

    # This function implements the Travelling Salesperson Problem using stochastic hill-climbing. 
    # You are allowed to add parameters and helper functions to achieve this functionality.        
    # For start and end nodes use the first node.
    # Use the imported random modules "randint()" or "random()" function to get the random value. 
    def stoch_hill_climbing(self):
        print("Stochastic hill-climbing implementation")

        path = self.find_path() #find path to use for hill climbing
        if path == False:
            return
        print(path)
        min_cost = self.get_cost(path)

        for i in range(1, len(path) - 1):
            for j in range(1, len(path) - 1):
                new_path = self.swap(path, i, j)
                if new_path == False:
                    continue
                else:
                    new_cost = self.get_cost(new_path)
                    if new_cost <= min_cost:
                        p = ((min_cost - new_cost) / min_cost) * 100 #get percent decrease
                        move = random.randint(1, 100) #generate # between 1 and 100
                        if p >= move: #if the prob of the move is >= random number, make the move
                            path = new_path
                            min_cost = new_cost
        return path

# This class is supposed to handle the Travelling Salesperson Problem and it's associated functions. To implement TSP,
# for the start and end nodes use the first node. A solution or a globally optimal is not garunteed. 
class JOB_GRAPH():

    # This function is the constructor for the JOB_GRAPH class.
    # It initializes the following varialbes
    # NJ - Number of Jobs
    # NM - Number of Machines
    # jobs -  a list of lists of sets where the first inner lists represents the first job, second inner list represents the second job
    # and so on. The values stored are in the form of a tuple/set (machineID, processingTime) for each step of the job.
    # It is initialized to all zeros.
    def __init__(self):
        self.NJ = 0
        self.NM = 0
        self.jobs = []

    # This function is used to read a file and save the total jobs, total machines, and the parameters for the jobs (machineID, processingTime)
    # and store it in the self.NJ, self.NM, and self.jobs variables in the format descrived above.    
    def get_jobs(self, N = 0):
        default_file_name = 'job_graph_'        
        file_name = default_file_name + str(N) + '.txt'
        print("OPENING ", file_name)
        file_object = open(file_name)
        count = 0  
        for f in file_object:
            jobss = []  
            if count == 0:
                self.NJ, self.NM = f.split(" ", 1)
                count = count + 1
            else:
                jobss = [(int(machine), int(time)) for machine, time in zip(*[iter(f.split())]*2)] 
                self.jobs.append(jobss)

    # Helper functions for sim_anneal

    def schedule_time():
        print("generating schedule time")

    #function creates a schedule from a jobs list 
    def create_schedule(self, job_list):
        print("creating schedule from job list")
        schedule = []
        for i in range(len(job_list)): #loop through each job
            mk = []
            for b in range(len(job_list)):

                for j in job_list[i]: #for each job loop through and find the ith job, at it to the ith schedule
                    if j[0] == i:
                        mk.append(j)
                schedule.append(mk) #add ith machine 
        return schedule


    # This function implements the simulted annealing version of the job-shop problem. Use a starting temperature of 500.
    # Decrease the temperature in increments of  0.5. This algorithm is not time limited but is limited stagnation (no improvement)
    # after 10,000 steps. Use appropriate values for other values. 
    # You are allowed to add parametetrs and helper functions to achieve the described functionality.  
    def sim_anneal(self):
        print(self.NJ)
        print(self.NM)
        #print(self.jobs)
        for i in self.jobs:
            print(i)

        print("SIMULATED ANNEALING")
        schedule = self.create_schedule(self.jobs)
        for i in schedule:
            print(i)


    # This function implements the genetic algorithm version of the job-shop problem.
    # Use random selection select the parents. Use the "random" or "randint" function to get the value for this purpose.
    # The stopping condition based on the number of generations: 10,000 generations.  
    # Use random mutation probalility of 0.75 and use the "random" function to get a real random value for this purpose.
    # Use appropriate values for other parameters if necessary.
    # You are allowed to add parametetrs and helper functions to achieve the described functionality.
    def genetic(self):
        print("GENETIC ALGORITHM")         

# This class is supposed to handle the graph coloring algorithm and it's associated functions.
class COLOR_GRAPH():
 
    # This constructor initializes the graph to be 0 at first. The entire graph can be set by passing the graph to it.
    # The graph is stored as a list of lists. The V variable is to track the number of vertices in the graph.
    # If two vertices are connected, value is not 0. A 0 value indicats no connection between the two vertices. 
    def __init__(self, vertices = 1):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]\
                              for row in range(vertices)]
    
    # This helper function is used to get the graph from a file. It takes a file name as a parameter and reads the file
    # sets the graph and number of veritces after reading the file. You are allowed to make changes, but no changes
    # should be necessary. 
    def get_graph(self, file = None):
        if file is not None:
            file_object= open(file)
            count = 0
            output_list=[]
            for line in file_object:
                line=line.strip('\r\n')
                count = count + 1
                output_list.append(literal_eval(line))
            self.V = count
            self.graph = output_list
        else:
            print("NO FILE PROVIDED.")

    # Helper functions for do_color

    #backtracking fo
    def backtracking(self):
        color = [0] * self.V #solution list
        n = 3 #number of colors

        ans = self.backtracking_rec(n, color, 0) #call recursive function

        # if false was returned print path doesnt exist, otherwise return the path
        if ans[0] == False:
            print("Graph cannot be colored")
            return False
        else:
            return ans[1] 

    #recursive function to find path
    def backtracking_rec(self, n, color, counter):

        if counter == self.V:
            return (True, color)

        for v in range(1, n + 1): #loop through domain
            if self.Safe(counter, color, v):
                color[counter] = v

                ret = self.backtracking_rec(n, color, counter+1) #recursive call to find next color of next node
                if ret[0] == True: #if path doesnt exist remove last node
                    return ret
                
                color[counter] = 0
        return (False, 0)    

    #determine if solution is valid
    #compares all edges of graph and check if each one is valid
    def Safe(self, counter, color, v):
        for i in range(self.V):
            if self.graph[counter][i] == 1 and color[i] == v:
                return False
        return True
        
    # This is the fucntion where you're supposed to implement the graph coloring algorithm. Right now it only prints the graph.
    # You are allowed to add parameters and define helper functions to achieve this functionality.
    def do_color(self):

        sol = self.backtracking()

        for i in range(0, len(sol)):
            if sol[i] == 1: # if color 1 print tsp for ith file
                print("color 1")
                print("vertex:", i)
                graph = TSP_GRAPH()
                graph.get_graph(i)
                p = graph.hill_climbing()
                print_path(p)
                p = graph.random_hill_climbing()
                print_path(p)
                p = graph.stoch_hill_climbing()
                print_path(p)
            if sol[i] == 2: #if color 2 do job scheduling
                print("color 2")
                print("vertex:", i)
                continue # wasnt able to complete, therefore continue
            if sol[i] == 3:
                print("color 3")
                print("vertex:", i)
                graph = TSP_GRAPH()
                graph.get_graph(i)

                start_time = time.time()
                p = graph.hill_climbing()
                end_time = time.time()
                print("Run time of Hill Climbing:", end_time - start_time)
                print_path(p)

                start_time = time.time()
                p = graph.random_hill_climbing()
                end_time = time.time()
                print("Run time of Random Hill Climbing:", end_time - start_time)
                print_path(p)
            
                start_time = time.time()
                p = graph.stoch_hill_climbing()
                end_time = time.time()
                print("Run time of Stochastic Hill Climbing:", end_time - start_time)
                print_path(p)

def print_path(path):
    s = ""
    for i in range(0, len(path)):
        s += str(path[i])
        if i < len(path) - 1:
            s += "->"
    print(s)

# This is the __main__ for this program. The program starts here. You are allowed to make changes as needed.
# Right now it just calls all the functions in the different classes defined above.
# For the assignment's final output, call the graph coloring first and based on the result generated, call the TSP and JOB-SHOP functions as described 
# in the pdf. 
if __name__ == "__main__":
    
    g3 = COLOR_GRAPH()
    g3.get_graph('color_graph.txt')
    g3.do_color()
