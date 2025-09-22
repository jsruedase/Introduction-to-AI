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
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    
    if problem.isGoalState(problem.getStartState()):
        return []
    
    directions = []
    marked = []
    stack = util.Stack()
    stack.push(problem.getStartState())
    father = {}
    
    while not stack.isEmpty():
        current_state = stack.pop()
        if current_state in marked:
            continue
        marked.append(current_state)
        
        if problem.isGoalState(current_state):
            while current_state != problem.getStartState():
                 directions.append(father[current_state][1])
                 current_state = father[current_state][0]
            return directions[::-1]
        successors = problem.getSuccessors(current_state)
        
        for suc in successors:
            if suc[0] in marked:
                continue
            father[suc[0]] = (current_state , suc[1])
            stack.push(suc[0])
    return []

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    if problem.isGoalState(problem.getStartState()):
        return []
    
    directions = []
    marked = []
    queue = util.Queue()
    queue.push(problem.getStartState())
    father = {}
    
    while not queue.isEmpty():
        current_state = queue.pop()
        if current_state in marked:
            continue
        marked.append(current_state)
        
        if problem.isGoalState(current_state):
            while current_state != problem.getStartState():
                 directions.append(father[current_state][1])
                 current_state = father[current_state][0]
            return directions[::-1]
        successors = problem.getSuccessors(current_state)
        
        for suc in successors:
            try: 
                if suc[0] in marked or father[suc[0]] != None:
                    continue
                father[suc[0]] = (current_state , suc[1])
                queue.push(suc[0])
            except:
                if suc[0] in marked:
                    continue
                father[suc[0]] = (current_state , suc[1])
                queue.push(suc[0])
    return []

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    if problem.isGoalState(problem.getStartState()):
        return []
    
    directions = []
    marked = []
    queue = util.PriorityQueue()
    queue.push(problem.getStartState(), 0)
    father = {}
    cost = {}
    cost[problem.getStartState()] = 0
    
    while not queue.isEmpty():
        current_state = queue.pop()
        if current_state in marked:
            continue
        marked.append(current_state)
        
        if problem.isGoalState(current_state):
            while current_state != problem.getStartState():
                 directions.append(father[current_state][1])
                 current_state = father[current_state][0]
            return directions[::-1]
        successors = problem.getSuccessors(current_state)
        
        for suc in successors:
            cost_suc = cost[current_state] + suc[2]
            # try: 
            #     if suc[0] in marked or father[suc[0]] != None or cost[suc[0]] <= cost_suc:
            #         continue
            #     cost[suc[0]] = cost_suc
            #     father[suc[0]] = (current_state , suc[1])
            #     queue.push(suc[0], cost_suc)
            # except:
            #     if suc[0] in marked or (suc[0] in cost and cost[suc[0]] <= cost_suc):
            #         continue
            #     cost[suc[0]] = cost_suc
            #     father[suc[0]] = (current_state , suc[1])
            #     queue.push(suc[0], cost_suc)
            if suc[0] not in cost or cost_suc < cost[suc[0]]:
                cost[suc[0]] = cost_suc
                father[suc[0]] = (current_state , suc[1])
                queue.push(suc[0], cost_suc)
    return []
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    if problem.isGoalState(problem.getStartState()):
        return []
    
    directions = []
    marked = []
    queue = util.PriorityQueue()
    queue.push(problem.getStartState(), 0)
    father = {}
    cost = {}
    cost[problem.getStartState()] = 0
    
    while not queue.isEmpty():
        current_state = queue.pop()
        if current_state in marked:
            continue
        marked.append(current_state)
        
        if problem.isGoalState(current_state):
            while current_state != problem.getStartState():
                 directions.append(father[current_state][1])
                 current_state = father[current_state][0]
            return directions[::-1]
        successors = problem.getSuccessors(current_state)
        
        for suc in successors:
            cost_suc = cost[current_state] + suc[2] + heuristic(suc[0], problem)
            if suc[0] not in cost or cost_suc < cost[suc[0]]:
                cost[suc[0]] = cost_suc - heuristic(suc[0], problem)
                father[suc[0]] = (current_state , suc[1])
                queue.push(suc[0], cost_suc)
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
