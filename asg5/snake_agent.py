import numpy as np
from numpy.core.fromnumeric import argmax
import helper
import random

#   This class has all the functions and variables necessary to implement snake game
#   We will be using Q learning to do this

class SnakeAgent:

    #   This is the constructor for the SnakeAgent class
    #   It initializes the actions that can be made,
    #   Ne which is a parameter helpful to perform exploration before deciding next action,
    #   LPC which ia parameter helpful in calculating learning rate (lr) 
    #   gamma which is another parameter helpful in calculating next move, in other words  
    #            gamma is used to blalance immediate and future reward
    #   Q is the q-table used in Q-learning
    #   N is the next state used to explore possible moves and decide the best one before updating
    #           the q-table
    def __init__(self, actions, Ne, LPC, gamma):
        self.actions = actions
        self.Ne = Ne
        self.LPC = LPC
        self.gamma = gamma
        self.reset()

        # Create the Q and N Table to work with
        self.Q = helper.initialize_q_as_zeros()
        self.N = helper.initialize_q_as_zeros()


    #   This function sets if the program is in training mode or testing mode.
    def set_train(self):
        self._train = True

     #   This function sets if the program is in training mode or testing mode.       
    def set_eval(self):
        self._train = False

    #   Calls the helper function to save the q-table after training
    def save_model(self):
        helper.save(self.Q)

    #   Calls the helper function to load the q-table when testing
    def load_model(self):
        self.Q = helper.load()

    #   resets the game state
    def reset(self):
        self.points = 0
        self.s = None
        self.a = None

    #   This is a function you should write. 
    #   Function Helper:IT gets the current state, and based on the 
    #   current snake head location, body and food location,
    #   determines which move(s) it can make by also using the 
    #   board variables to see if its near a wall or if  the
    #   moves it can make lead it into the snake body and so on. 
    #   This can return a list of variables that help you keep track of
    #   conditions mentioned above.
    
    # x values 0 = none or false, 1 = left or true, 2 = right
    # y value  0 = none, 1 = up, 2 = down
    #
    def helper_func(self, state):
        print("IN helper_func")
        # State = [0, 1, 2, 3, 4]
        # 0 snake_head_x
        # 1 snake_head_y
        # 2 snake_body = [body parts]
        # 3 food_x
        # 4 food_y 

        snake_head_x = state[0]
        snake_head_y = state[1]
        snake_body = state[2]
        food_x = state[3]
        food_y = state[4]
        q_table_index = []
        body_check = False

        #check snake x values
        if snake_head_x + 40 == 520: #check if wall on left
            q_table_index.append(1)
        elif snake_head_x - 40 == 0:  #check if wall on right
            q_table_index.append(2)
        else: # not touching wall on left or right
            q_table_index.append(0) 

        #check snake y values
        if snake_head_y - 40 == 0: #check if wall on top
            q_table_index.append(1)
        elif snake_head_y + 40 == 520: #check if wall on bottom
            q_table_index.append(2)
        else: # not touching wall on top or bottom
            q_table_index.append(0)
        
        #check food x value
        if snake_head_x > food_x: #if food < snake x, food on left
            q_table_index.append(1)
        elif snake_head_x < food_x: #if food > snake x, food on right
            q_table_index.append(2)
        else: #food in same column
            q_table_index.append(0)

        #check food y value
        if snake_head_y > food_y: #if food < snake y, food on top
            q_table_index.append(1)
        elif snake_head_y < food_y: #if food > snake x, food bellow
            q_table_index.append(2)
        else: #food in same row
            q_table_index.append(0)
        
        #check snake body above
        for i in snake_body: # loop through each body
            if snake_head_y - 40 == i[1]: #check if body above head
                body_check = True
                break
        if body_check: # if body above append 1, else append 0
            q_table_index.append(1)
            body_check = False
        else:
            q_table_index.append(0)

        #check snake body bottom
        for i in snake_body: # loop through each body
            if snake_head_y + 40 == i[1]: #check if body is bellow the head
                body_check = True
                break
        if body_check: # if body bellow append 1, else append 0
            q_table_index.append(1)
        else:
            q_table_index.append(0)

        #check snake body to left
        for i in snake_body: # loop through each body
            if snake_head_x - 40 == i[0]: #check if body is to the left of head
                body_check = True
                break
        if body_check: # if body left append 1, else append 0
            q_table_index.append(1)
        else:
            q_table_index.append(0)
        
        #check snake body to right
        for i in snake_body: # loop through each body
            if snake_head_x + 40 == i[0]: #check if body is to the right of head
                body_check = True
                break
        if body_check: # if body right append 1, else append 0
            q_table_index.append(1)
        else:
            q_table_index.append(0)

        return q_table_index # return list containing indexs of Q table for given state

    # Computing the reward, need not be changed.
    def compute_reward(self, points, dead):
        if dead:
            return -1
        elif points > self.points:
            return 1
        else:
            return -0.1

    #   This is the code you need to write. 
    #   This is the reinforcement learning agent
    #   use the helper_func you need to write above to
    #   decide which move is the best move that the snake needs to make 
    #   using the compute reward function defined above. 
    #   This function also keeps track of the fact that we are in 
    #   training state or testing state so that it can decide if it needs
    #   to update the Q variable. It can use the N variable to test outcomes
    #   of possible moves it can make. 
    #   the LPC variable can be used to determine the learning rate (lr), but if 
    #   you're stuck on how to do this, just use a learning rate of 0.7 first,
    #   get your code to work then work on this.
    #   gamma is another useful parameter to determine the learning rate.
    #   based on the lr, reward, and gamma values you can update the q-table.
    #   If you're not in training mode, use the q-table loaded (already done)
    #   to make moves based on that.
    #   the only thing this function should return is the best action to take
    #   ie. (0 or 1 or 2 or 3) respectively. 
    #   The parameters defined should be enough. If you want to describe more elaborate
    #   states as mentioned in helper_func, use the state variable to contain all that.
    def agent_action(self, state, points, dead):
        print("IN AGENT_ACTION")
       
        self.load_model() #load model
        self.N = np.copy(self.Q) # copy array into N to modify

        q_index = self.helper_func(state) #fetch q values of current state
        q_values = self.Q[q_index[0], q_index[1], q_index[2],q_index[3], q_index[4], q_index[5], q_index[6], q_index[7]]
        #print(q_values)
        #print(type(q_values))

        if self._train: # if training 
            #chekc up down left right
            
            for x in range(0, 4):
                new_state = np.copy(state) #create copy of state to modify

                if x == 0: # check up case
                    prev = (new_state[0], new_state[1]) # save head to then modify body parts
                    snake_body = new_state[2]
                    for i in range(len(snake_body)): # loop through each body part
                        temp = snake_body[i]
                        snake_body[i] = prev # set current body part to prev one
                        prev = temp
                    new_state[1] -= 40 #move snake_head_y up by 40
                    up_index = self.helper_func(new_state) #call helper func on state moved up
                    up_values = self.Q[up_index[0], up_index[1], up_index[2], up_index[3], up_index[4], up_index[5], up_index[6], up_index[7]]
                    
                    #check if dead after move
                    if new_state[1] == 0: #if up is wall, its dead
                        dead = True
                    else:
                        for j in new_state[2]: #check if up is a body, we die
                            if new_state[0] == j[0] and new_state[1] == j[1]:
                                dead = True

                    #check if food eaten when going up
                    if new_state[0] == new_state[3] and new_state[1] == new_state[4]:
                        points += 1
                        
                    #sample = reWARD(up) + gamma * max(up_values)
                    sample = self.compute_reward(points, dead) + (self.gamma * np.amax(up_values))

                    #set new q value for up move
                    q_values[x] = (1 - 0.7) * q_values[x] + 0.7 * sample

                if x == 1: # check down case
                    prev = (new_state[0], new_state[1]) # save head to then modify body parts
                    snake_body = new_state[2]
                    for i in range(len(snake_body)): # loop through each body part
                        temp = snake_body[i]
                        snake_body[i] = prev # set current body part to prev one
                        prev = temp
                    new_state[1] += 40 #move snake_head_y down by 40
                    up_index = self.helper_func(new_state) #call helper func on state moved down
                    up_values = self.Q[up_index[0], up_index[1], up_index[2], up_index[3], up_index[4], up_index[5], up_index[6], up_index[7]]
                    
                    #check if dead after move
                    if new_state[1] == 520: #if down is wall, its dead
                        dead = True
                    else:
                        for j in new_state[2]: #check if down is a body, we die
                            if new_state[0] == j[0] and new_state[1] == j[1]:
                                dead = True

                    #check if food eaten when going up
                    if new_state[0] == new_state[3] and new_state[1] == new_state[4]:
                        points += 1
                        
                    #sample = reWARD(up) + gamma * max(up_values)
                    sample = self.compute_reward(points, dead) + (self.gamma * np.amax(up_values))

                    #set new q value for up move
                    q_values[x] = (1 - 0.7) * q_values[x] + 0.7 * sample
                
                if x == 2: # check left case
                    prev = (new_state[0], new_state[1]) # save head to then modify body parts
                    snake_body = new_state[2]
                    for i in range(len(snake_body)): # loop through each body part
                        temp = snake_body[i]
                        snake_body[i] = prev # set current body part to prev one
                        prev = temp
                    new_state[0] -= 40 #move snake_head_x left by 40
                    up_index = self.helper_func(new_state) #call helper func on state moved down
                    up_values = self.Q[up_index[0], up_index[1], up_index[2], up_index[3], up_index[4], up_index[5], up_index[6], up_index[7]]
                    
                    #check if dead after move
                    if new_state[0] == 0: #if down is wall, its dead
                        dead = True
                    else:
                        for j in new_state[2]: #check if down is a body, we die
                            if new_state[0] == j[0] and new_state[1] == j[1]:
                                dead = True

                    #check if food eaten when going up
                    if new_state[0] == new_state[3] and new_state[1] == new_state[4]:
                        points += 1
                        
                    #sample = reWARD(up) + gamma * max(up_values)
                    sample = self.compute_reward(points, dead) + (self.gamma * np.amax(up_values))

                    #set new q value for up move
                    q_values[x] = (1 - 0.7) * q_values[x] + 0.7 * sample
                    
                if x == 3: # check right case
                    prev = (new_state[0], new_state[1]) # save head to then modify body parts
                    snake_body = new_state[2]
                    for i in range(len(snake_body)): # loop through each body part
                        temp = snake_body[i]
                        snake_body[i] = prev # set current body part to prev one
                        prev = temp
                    new_state[0] += 40 #move snake_head_x right by 40
                    up_index = self.helper_func(new_state) #call helper func on state moved down
                    up_values = self.Q[up_index[0], up_index[1], up_index[2], up_index[3], up_index[4], up_index[5], up_index[6], up_index[7]]
                    
                    #check if dead after move
                    if new_state[0] == 520: #if down is wall, its dead
                        dead = True
                    else:
                        for j in new_state[2]: #check if down is a body, we die
                            if new_state[0] == j[0] and new_state[1] == j[1]:
                                dead = True

                    #check if food eaten when going up
                    if new_state[0] == new_state[3] and new_state[1] == new_state[4]:
                        points += 1
                        
                    #sample = reWARD(up) + gamma * max(up_values)
                    sample = self.compute_reward(points, dead) + (self.gamma * np.amax(up_values))

                    #set new q value for up move
                    q_values[x] = (1 - 0.7) * q_values[x] + 0.7 * sample
            
            #save new q values into q table
            self.Q[q_index[0], q_index[1], q_index[2],q_index[3], q_index[4], q_index[5], q_index[6], q_index[7]] = q_values
            self.save_model()

        # get index of max of q_values to determine next action
        action = np.argmax(q_values)
        # call helper function to get current state indexs = [0, 0, 0, 0]
        #
        # 
        # if training 
        #         calculate new q values for up down left right
        #         update table with those values
        # else
        # select max from current state
        # return max

        #UNCOMMENT THIS TO RETURN THE REQUIRED ACTION.
        return action