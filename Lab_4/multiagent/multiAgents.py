# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # Minimizar la distancia a la comida y maximizar la distancia a los fantasmas
        min_food_distance = min(util.manhattanDistance(newPos, food) for food in newFood.asList()) if newFood.asList() else 0 # Evitar que falle cuando se coma la última comida
        min_ghost_distance = min(util.manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates)
        if min_ghost_distance <= 2:
            return -1e9
        #para 2 * min_ghost_distance gana 9/10, igual con 3
        return successorGameState.getScore() + 10 / (min_food_distance + 1) - 4 * min_ghost_distance 

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    
    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        super().__init__(evalFn, depth)

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        def min_value(gameState: GameState, index, depth):
            num_agents = gameState.getNumAgents()
            next_index = (index + 1) % num_agents 
            
            actions = gameState.getLegalActions(index)
            v = 1e9
            for action in actions:     
                if next_index == 0:
                    v = min(v, value(gameState.generateSuccessor(index, action), 0, depth + 1))  # Es el pacman, se aumenta la profundidad
                else:
                    v = min(v, value(gameState.generateSuccessor(index, action), next_index, depth))
            return v

        def max_value(gameState: GameState, index, depth):
            # Como el max value solo lo llama el pacman, se llama entonces al índice 1 como el sucesor 
            actions = gameState.getLegalActions(index)
            v = -1e9
            for action in actions:
                v = max(v, value(gameState.generateSuccessor(index, action), 1, depth))
            return v
        
        def value(gameState: GameState, index, depth):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

            if index == 0:
                return max_value(gameState, index, depth)
            else:
                return min_value(gameState, index, depth)

        #Inicializamos en el pacman
        ans = None
        best_val = -1e9
        
        for action in gameState.getLegalActions(0):
            suc = gameState.generateSuccessor(0, action)
            val = value(suc, 1, 0)
            if val > best_val:
                best_val = val
                ans = action

        return ans


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        super().__init__(evalFn, depth)

    def getAction(self, gameState: GameState):
        """
        Returns the best action using alpha-beta pruning.
        """ 
        
        "*** YOUR CODE HERE ***"
        
        def min_value(gameState: GameState, index, depth, alpha, beta):
            num_agents = gameState.getNumAgents()
            next_index = (index + 1) % num_agents 
            
            actions = gameState.getLegalActions(index)
            v = 1e9
            for action in actions:     
                if next_index == 0:
                    v = min(v, value(gameState.generateSuccessor(index, action), 0, depth + 1, alpha, beta))  # Es el pacman, se aumenta la profundidad

                    # Version profe
                    beta = min(beta, v)
                    if beta < alpha:
                        break
                    
                    # Version berkley 
                    # if v <= alpha:
                    #     return v
                    # beta = min(beta, v)
                    
                    # Version Wikipedia
                    # if v <= alpha:
                    #     break
                    # beta = min(beta, v)
                else:
                    v = min(v, value(gameState.generateSuccessor(index, action), next_index, depth, alpha, beta))
                    
                    # Version profe
                    beta = min(beta, v)
                    if beta < alpha:
                        break
                    
                    # Version berkley
                    # if v <= alpha:
                    #     return v
                    # beta = min(beta, v)
                    
                    # Version Wikipedia
                    # if v <= alpha:
                    #     break
                    # beta = min(beta, v)
            return v

        def max_value(gameState: GameState, index, depth, alpha, beta):
            # Como el max value solo lo llama el pacman, se llama entonces al índice 1 como el sucesor 
            actions = gameState.getLegalActions(index)
            v = -1e9
            for action in actions:
                v = max(v, value(gameState.generateSuccessor(index, action), 1, depth, alpha, beta))
                
                # Version profe
                alpha = max(alpha, v)
                if beta < alpha:
                    break
                
                # Version berkley
                # if v >= beta:
                #     return v
                # alpha = max(alpha, v)
                
                # Version Wikipedia
                # if v >= beta:
                #     break
                # alpha = max(alpha, v)
                
            return v
        
        def value(gameState: GameState, index, depth, alpha, beta):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

            if index == 0:
                return max_value(gameState, index, depth, alpha, beta)
            else:
                return min_value(gameState, index, depth, alpha, beta)

        #Inicializamos en el pacman
        ans = None
        best_val = -1e9
        alpha = -1e9
        beta = 1e9
        
        for action in gameState.getLegalActions(0):
            suc = gameState.generateSuccessor(0, action)
            val = value(suc, 1, 0, alpha, beta)
            if val > best_val:
                best_val = val
                ans = action
            alpha = max(alpha, best_val) # Se debe actualizar la mejor ruta encontrada hasta el momento
        return ans

class ExpectimaxAgent(MultiAgentSearchAgent):
    
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
