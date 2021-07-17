import sys
from ast import literal_eval
import random
import fileinput

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
    
    # This function implements the Travelling Salesperson Problem using hill-climbing. 
    # You are allowed to add parameters and helper functions to achieve this functionality.
    # For start and end nodes use the first node.
    def hill_climbing(self):
        print ("Hill-climbing implementation")
        #print(self.graph)

        path = self.find_path() #find path to use for hill climbing
        if path == False:
            return
        print(path)
        


        #for i in range(len(self.graph)): #loop to find the path, maxmum loop should = # of nodes
         #   max = current.index(min(current)) #start max as min of current
        #    for j in range(len(current)): # loop through neighbors to find max
         #       next = current[j] # get neighbor
         #       if next > current[max] and j not in visited: #if neighbor > then current max and not yet visited, set new max value
         #           max = j
         #   visited.append(max)
         #   current = self.graph[max]
        # return visited

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
            return ans[1] 

    #recursive function to find path
    def find_path_rec(self, path, path_count):

        print(path)
        print(path_count, self.V)

        if path_count == self.V:
            print("sane size")
            print(self.graph[path[path_count-1]][path[0]])
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



    # This function implements the Travelling Salesperson Problem using random restart hill-climbing. 
    # You are allowed to add parameters and helper functions to achieve this functionality.        
    # For start and end nodes use the first node.
    # use the imported random modules "randint()" or "random()" function to get the random value. 
    def random_hill_climbing(self):
        print ("Random restart hill-climbing implementation")

    # This function implements the Travelling Salesperson Problem using stochastic hill-climbing. 
    # You are allowed to add parameters and helper functions to achieve this functionality.        
    # For start and end nodes use the first node.
    # Use the imported random modules "randint()" or "random()" function to get the random value. 
    # You can use any values for bounds and step size (please choose values that make senes) as long
    # as you use 10,000 total number of steps. 
    def stoch_hill_climbing(self):
        print("Stochastic hill-climbing implementation")



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

    # This function implements the simulted annealing version of the job-shop problem. Use a starting temperature of 500.
    # Decrease the temperature in increments of  0.5. This algorithm is not time limited but is limited stagnation (no improvement)
    # after 10,000 steps. Use appropriate values for other values. 
    # You are allowed to add parametetrs and helper functions to achieve the described functionality.  
    def sim_anneal(self):
        print(self.NJ)
        print(self.NM)
        print(self.jobs)
        print("SIMULATED ANNEALING")

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

    # This is the fucntion where you're supposed to implement the graph coloring algorithm. Right now it only prints the graph.
    # You are allowed to add parameters and define helper functions to achieve this functionality.
    def do_color(self):
        print (self.graph)
 
# This is the __main__ for this program. The program starts here. You are allowed to make changes as needed.
# Right now it just calls all the functions in the different classes defined above.
# For the assignment's final output, call the graph coloring first and based on the result generated, call the TSP and JOB-SHOP functions as described 
# in the pdf. 
if __name__ == "__main__":
    
    
    # Testing TSP_GRAPH file reading and printing and functions.
    print ("\nTesting TSP_GRAPH functions.")
    g1 = TSP_GRAPH()
    g1.get_graph(0)
    g1.hill_climbing()
    #g1.random_hill_climbing()
    #g1.stoch_hill_climbing()

    # Testing the Job-shop class functions.
    #print ("\nTesting JOB_GRAPH functions.")
    #g2 = JOB_GRAPH()
    #g2.get_jobs(0)
    #g2.sim_anneal()
    #g2.genetic()

    # Testing COLOR_GRAPH functions.
    #print ("\nTesting COLOR_GRAPH functions.")
    #g3 = COLOR_GRAPH()
    #g3.get_graph('color_graph.txt')
    #g3.do_color()
