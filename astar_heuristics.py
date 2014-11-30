# heuristics.py
# ----------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

""" This class contains heuristics which are used for the search procedures that
    you write in search_strategies.py.

    The first part of the file contains heuristics to be used with the algorithms
    that you will write in search_strategies.py.

    In the second part you will write a heuristic for Q4 to be used with a
    MultiplePositionSearchProblem.
"""

#-------------------------------------------------------------------------------
# A set of heuristics which are used with a PositionSearchProblem 
# You do not need to modify any of these.
#-------------------------------------------------------------------------------

def null_heuristic(pos, problem):
    """ The null heuristic. It is fast but uninformative. It always returns 0.
        (State, SearchProblem) -> int
    """
    return 0

def manhattan_heuristic(pos, problem):
  """ The Manhattan distance heuristic for a PositionSearchProblem.
      ((int, int), PositionSearchProblem) -> int
  """
  return abs(pos[0] - problem.goal_pos[0]) + abs(pos[1] - problem.goal_pos[1])

def euclidean_heuristic(pos, problem):
    """ The Euclidean distance heuristic for a PositionSearchProblem
        ((int, int), PositionSearchProblem) -> float
    """
    return ((pos[0] - problem.goal_pos[0]) ** 2 + (pos[1] - problem.goal_pos[1]) ** 2) ** 0.5

#Abbreviations
null = null_heuristic
manhattan = manhattan_heuristic
euclidean = euclidean_heuristic
 
#-------------------------------------------------------------------------------
# You have to implement the following heuristic for Q4 of the assignment.
# It is used with a MultiplePositionSearchProblem
#-------------------------------------------------------------------------------

#You can make helper functions here, if you need them
def every_bird_heuristic(state, problem):
    """ Q4: Find Every Yellow Bird (4 marks)
        
        This heuristic is used for solving a MultiplePositionSearchProblem.
        It should return an estimate of the cost of reaching a goal state in
        problem, from the given state.

        To ensure correctness, this heuristic must be admissible. This means that
        it must not overestimate the cost of reaching the goal. Inadmissible
        heuristics may still find optimal solutions, so be careful.

        The state is a tuple (pos, yellow_birds) where:
            - pos is a tuple (int, int) indicating the red bird's current position;
            - yellow_birds is a tuple ((int, int), (int, int), ...) containing
              tuples representing the positions of the remaining yellow birds.
              
        You have access to the following information directly from problem:
            
            - problem.maze_distance(pos1, pos2)
                (MultiplePositionSearchProblem, (int, int), (int, int)) -> int
            
                This will return the shortest distance between the given positions.
                Do not use this information to for earlier parts of the assignment.
                We will actually look at your code!
                
            - problem.get_width() 
                (MultiplePositionSearchProblem) -> int
                
                This will return the width of the board.
            
            - problem.get_height()
                (MultiplePositionSearchProblem) -> int
                
                This will return the height of the board.
            
            - problem.get_walls()
                (MultiplePositionSearchProblem) -> [[bool]]
                
                This will return lists representing a 2D array of the wall positions.

        If you want to *store* information to be reused in other calls to the heuristic,
        there is a dictionary called problem.heuristic_info that you can use.
        
        You need to be able to explain your heuristic to us -- i.e. what's the
        intuition behind it?
        
        You should comment your heuristic.
        
        Feel free to make helper functions above this one.
        
        (((int, int), ((int, int))), MultiplePositionSearchProblem) -> number
    """
    position, yellow_birds = state
    heuristic_value = 0
    """ *** YOUR CODE HERE *** """
    # originally, I used the total weight of the minimum spanning tree (MST) 
    # constructed from all the yellow birds and the red bird itself as the heuristic. 
    # it is apparently admissible, and it seems to me that
    # it should also be consistent if Manhattan distance is used to measure the distance between two birds,
    # but somehow I could not find a way to prove that.
    # so I change the heuristic a little to make it easier to proved its consistency, 
    # though it is not required.
    
    # this is the original piece of code:
    # heuristic_value = compute_mst(list(yellow_birds)+[position],problem)
    # it expands exactly 698 nodes as mentioned in the description.
    
    # the new heuristic is calculated by the sum of:
    # 1.1 the distance between the red bird and its nearest yellow bird
    # 1.2 the total weight of the MST that constructed from all the yellow birds, but not including the red bird
    # and it is admissible and consistent.
    
    # first prove its admissibility,
    # the shortest path can be divided into two parts:
    # 2.1 the edge between the red bird and the first yellow bird it gets to
    # 2.2 the rest of the path connects all the yellow birds
    #  
    # it is obvious that 1.1 is always less than or equal to 2.1, because 1.1 is the nearest.
    # 2.2 could also be viewed as a tree where all the nodes has exactly one child.
    # because a MST is a tree connects all of the vertices and whose total weight is minimized.
    # thus, the total weight of MST (1.2) is always less than or equal to the length of the rest of the path (2.2),
    # 
    # therefore we have 1.1+1.2 <= 2.1+2.2 hence it is a admissible estimation of this problem.
    
    # now we are going to prove its consistency.
    # suppose we take a step from node n0 to n1,
    # then h(n0) = 1.1(n0) + 1.2(n0), h(n1) = 1.1(n1) + 1.2(n1)
    #
    # if there is no yellow bird at n1, 
    # then 1.2(n1) is the same as 1.2(n0),
    # and 1.1(n1) + cost(n0,n1) is greater than or equal to 1.1(n0), because of the triangle inequality.
    # so we have h(n1) + cost(n0,n1) >= h(n0)
    # 
    # if there is a yellow bird at n1,
    # then 1.1(n0) is smaller than or equal to 1.1(n1) + 1.2(n1),
    # because 1.1(n1) + 1.2(n1) could also be view the as a tree that constructed from exactly the same 
    # nodes as we have in 1.1(n0), since we moved to the same place where the yellow bird used to be.
    # we know 1.1(n0) is MST, so 1.1(n1) + 1.2(n1) >= 1.1(n0).
    # because we reached a yellow bird with one step, so 1.2(n0) = 1 = cost(n0,n1).
    # hence we have h(n1) + cost(n0,n1) = 1.1(n1) + 1.2(n1) + cost(n0,n1) >= 1.1(n0) + 1.2(n0) = h(n0)
    #
    # Therefore, our heuristic is consistent.
    
    # actually it turns out to be a better estimation than the original MST heuristic,
    # because it always holds MST <= 1.1+1.2 <= shortest_path
    # and the number of nodes it expand is 474. ;]
    if len(yellow_birds)==0:
        heuristic_value = 0
    else: 
        heuristic_value = compute_mst(list(yellow_birds),problem)+select_shortest(position,list(yellow_birds),problem)
        
    return heuristic_value

import sys, frontiers

def compute_mst(vertices,problem):
    key = {}
    pred = {}
    for v in vertices:
        key[v] = sys.maxint
        pred[v] = None
    key[vertices[0]] = 0
    pq = frontiers.PriorityQueue()
    for v in vertices:
        pq.push(v, key[v])
    while not pq.is_empty():
        u = pq.pop()
        for v in vertices:
            if v != u:
                item = pq.find(lambda x: x == v)
                if item != None:
                    w = problem.maze_distance(u, v)
                    if w<key[v]:
                        pred[v] = u
                        key[v] = w
                        pq.change_priority(item, w)
    # return the sum of weight of all edges in the tree
    return sum(key.values())

''' return the nearest yellow bird ''' 
def select_shortest(src, yellow_birds, problem):
    min_val = sys.maxint
    for pos in yellow_birds:
        min_val = min(min_val,problem.maze_distance(src, pos))
    return min_val 
    
