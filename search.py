# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import searchAgents
from game import Directions

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    
    current_location = problem.getStartState()
    #To remember which node has been visited
    visited = []
    visited.append(current_location)
    #location and direction means the pair of each move
    location = util.Stack()
    direction = util.Stack()
    #use to remeber the effective actions of each point, so we use dict structure to store
    remember_actions = {}
    #real_direction store every move
    #route strorethe sequence of visited nodes
    real_directions = []
    route = []
    while not problem.isGoalState(current_location):
        actions = problem.getSuccessors(current_location)
        remember_actions[current_location] = []
        for action in actions:
            if action[0] not in visited:
                '''
                if the vertex is not in the visited list, then add it to the Stack,
                Also remember to store the action of current point to this point
                in dfs we don't have to consider the cost so we can add the point to visited list now
                '''
                location.push(action[0])
                visited.append(current_location)
                remember_actions[current_location].append(action)
                direction.push(action[1])
        if not location.isEmpty():
            current_location = location.pop()
            current_direction = direction.pop()
            real_directions.append(current_direction)
            route.append(current_location)
    '''
    Here we traceback from the goal to see which one is real route
    If not then we delete the wrong route and direction move
    '''
    final = len(route)-2
    while final >=0:
        right_route = False
        actions = remember_actions[route[final]]
        for action in actions:
            if action[0]==route[final+1]:
                right_route = True
                break
        if not right_route:
            del route[final]
            del real_directions[final]
        final = final -1  
    return  real_directions

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST
    
    current_location = problem.getStartState()
    visited = []
    visited.append(current_location)
    location = util.Queue()
    direction = util.Queue()
    remember_actions = {}
    real_directions = []
    route = []
    
    while not problem.isGoalState(current_location):
        actions = problem.getSuccessors(current_location)
        remember_actions[current_location]=[]
        for action in actions:
            if action[0] not in visited:
                location.push(action[0])
                visited.append(action[0])
                remember_actions[current_location].append(action)
                direction.push(action[1])
        if not location.isEmpty():
            current_location = location.pop()
            current_direction = direction.pop()
            real_directions.append(current_direction)
            route.append(current_location)
    '''
    Here we traceback from the goal to see which one is real route
    If not then we delete the wrong route and direction move
    '''
    final = len(route)-2
    while final >=0:
        right_route = False
        actions = remember_actions[route[final]]
        for action in actions:
            if action[0]==route[final+1]:
                right_route = True
                break
        if not right_route:
            del route[final]
            del real_directions[final]
        final = final -1  
    #return [e,n,e,s]
    return  real_directions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    current_location = problem.getStartState()
    visited = []
    visited.append(current_location)
    location = util.PriorityQueue()
    direction = util.Queue()
    remember_actions = {}
    real_directions = []
    routes = {}
    routes[current_location]=[]
    costs = {}
    costs[current_location]=0
    cost = 0
    while not problem.isGoalState(current_location):
        actions = problem.getSuccessors(current_location)
        remember_actions[current_location]=[]
        for action in actions:
            if action[0] not in visited:
                location.update(action[0],action[2]+cost)
                remember_actions[current_location].append(action)
                if action[0] not in costs:
                    costs[action[0]] = action[2]+cost
                    routes[action[0]] = current_location
                elif action[2]+cost < costs[action[0]]:
                    costs[action[0]] = action[2]+cost
                    routes[action[0]] = current_location
        if not location.isEmpty():
            current_location = location.pop()
            visited.append(current_location)
            #route.append(current_location)
            cost = costs[current_location]
      
    '''
    Here we traceback from the goal to see which one is real route
    If not then we delete the wrong route and direction move
    '''
    real_directions=[]
    while current_location != problem.getStartState():
        previous = routes[current_location]
        actions = remember_actions[previous]
        for action in actions:
            if action[0]==current_location:
                real_directions.append(action[1])
                break
        current_location = previous
    real_directions.reverse()
    return  real_directions



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    current_location = problem.getStartState()
    visited = []
    visited.append(current_location)
    location = util.PriorityQueue()
    direction = util.Queue()
    remember_actions = {}
    real_directions = []
    routes = {}
    routes[current_location]=[]
    costs = {}
    costs[current_location]=0
    cost = 0
    while not problem.isGoalState(current_location):
        actions = problem.getSuccessors(current_location)
        #print actions
        remember_actions[current_location]=[]
        for action in actions:
            if action[0] not in visited:
                location.update(action[0],action[2]+cost+heuristic(action[0],problem))
                remember_actions[current_location].append(action)
                if action[0] not in costs:
                    costs[action[0]] = action[2]+cost
                    routes[action[0]] = current_location
                elif action[2]+cost+heuristic(action[0],problem) < costs[action[0]]:
                    costs[action[0]] = action[2]+cost+heuristic(action[0],problem)
                    routes[action[0]] = current_location
        if not location.isEmpty():
            current_location = location.pop()
            visited.append(current_location)
            #route.append(current_location)
            cost = costs[current_location]
    '''
    Here we traceback from the goal to see which one is real route
    If not then we delete the wrong route and direction move
    '''
    real_directions=[]
    while current_location != problem.getStartState():
        previous = routes[current_location]
        actions = remember_actions[previous]
        for action in actions:
            if action[0]==current_location:
                real_directions.append(action[1])
                break
        current_location = previous
    real_directions.reverse()
    return  real_directions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
