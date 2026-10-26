import heapq
import random
import sys
import time


# different moves
# https://ruwix.com/online-puzzle-simulators/2x2x2-pocket-cube-simulator.php


MOVES = {
    "U":  [6,3,0,7,4,1,8,5,2,    45,46,47,12,13,14,15,16,17, 9,10,11,21,22,23,24,25,26,  27,28,29,30,31,32,33,34,35, 18,19,20,39,40,41,42,43,44, 36,37,38,48,49,50,51,52,53],
    "U'": [2,5,8,1,4,7,0,3,6,    18,19,20,12,13,14,15,16,17, 36,37,38,21,22,23,24,25,26, 27,28,29,30,31,32,33,34,35, 45,46,47,39,40,41,42,43,44, 9,10,11,48,49,50,51,52,53],
    "R":  [0,1,20,3,4,23,6,7,26, 15,12,9,16,13,10,17,14,11,  18,19,29,21,22,32,24,25,35, 27,28,51,30,31,48,33,34,45, 36,37,38,39,40,41,42,43,44, 8,46,47,5,49,50,2,52,53],
    "R'": [0,1,51,3,4,48,6,7,45, 11,14,17,10,13,16,9,12,15,  18,19,2,21,22,5,24,25,8,    27,28,20,30,31,23,33,34,26, 36,37,38,39,40,41,42,43,44, 35,46,47,32,49,50,29,52,53],
    "F":  [0,1,2,3,4,5,44,41,38, 6,10,11,7,13,14,8,16,17,    24,21,18,25,22,19,26,23,20, 15,12,9,30,31,32,33,34,35,  36,37,27,39,40,28,42,43,29, 45,46,47,48,49,50,51,52,53],
    "F'": [0,1,2,3,4,5,9,12,15,  29,10,11,28,13,14,27,16,17, 20,23,26,19,22,25,18,21,24, 38,41,44,30,31,32,33,34,35, 36,37,8,39,40,7,42,43,6,    45,46,47,48,49,50,51,52,53],
    "D":  [0,1,2,3,4,5,6,7,8,    9,10,11,12,13,14,24,25,26,  18,19,20,21,22,23,42,43,44, 33,30,27,34,31,28,35,32,29, 36,37,38,39,40,41,51,52,53, 45,46,47,48,49,50,15,16,17],
    "D'": [0,1,2,3,4,5,6,7,8,    9,10,11,12,13,14,51,52,53,  18,19,20,21,22,23,15,16,17, 29,32,35,28,31,34,27,30,33, 36,37,38,39,40,41,24,25,26, 45,46,47,48,49,50,42,43,44],
    "L":  [53,1,2,50,4,5,47,7,8, 9,10,11,12,13,14,15,16,17,  0,19,20,3,22,23,6,25,26,    18,28,29,21,31,32,24,34,35, 42,39,36,43,40,37,44,41,38, 45,46,33,48,49,30,51,52,27],
    "L'": [18,1,2,21,4,5,24,7,8, 9,10,11,12,13,14,15,16,17,  27,19,20,30,22,23,33,25,26, 53,28,29,50,31,32,47,34,35, 38,41,44,37,40,43,36,39,42, 45,46,6,48,49,3,51,52,0],
    "B":  [11,14,17,3,4,5,6,7,8, 9,10,35,12,13,34,15,16,33,  18,19,20,21,22,23,24,25,26, 27,28,29,30,31,32,36,39,42, 2,37,38,1,40,41,0,43,44,    51,48,45,52,49,46,53,50,47],
    "B'": [42,39,36,3,4,5,6,7,8, 9,10,0,12,13,1,15,16,2,     18,19,20,21,22,23,24,25,26, 27,28,29,30,31,32,17,14,11, 33,37,38,34,40,41,35,43,44, 47,50,53,46,49,52,45,48,51],
}

CORNERS_AND_EDGES = [ # all corners and edges
  (6, 18, 38),
  (8, 20, 9),
  (2, 11, 45),
  (0, 36, 47),
  (27, 24, 44),
  (29, 26, 15),
  (35, 17, 51),
  (33, 42, 53),
  (7, 19),
  (5, 10),
  (1, 46),
  (3, 37),
  (28, 25),
  (32, 16),
  (34, 52),
  (30, 43),
  (23, 12),
  (21, 41),
  (48, 14),
  (50, 39)
]

XYZ_CORNERS_AND_EDGES = { # coords in 3d space for each combination
  (6, 18, 38): (0,2,2),
  (8, 20, 9): (2,2,2),
  (2, 11, 45): (2,0,2),
  (0, 36, 47): (0,0,2),
  (27, 24, 44): (0,2,0),
  (29, 26, 15): (2,2,0),
  (35, 17, 51): (2,0,0),
  (33, 42, 53): (0,0,0),
  (7, 19): (1,2,2),
  (5, 10): (2,1,2),
  (1, 46): (1,0,2),
  (3, 37): (0,1,2),
  (28, 25): (1,2,0),
  (32, 16): (2,1,0),
  (34, 52): (1,0,0),
  (30, 43): (0,1,0),
  (23, 12): (2,2,1),
  (21, 41): (0,2,1),
  (48, 14): (2,0,1),
  (50, 39): (0,0,1)
}

PIECE_COLORS = [ # list of all piece colors
  ('G', 'O', 'W'), 
  ('G', 'R', 'W'), 
  ('B', 'R', 'W'), 
  ('B', 'O', 'W'), 
  ('G', 'O', 'Y'), 
  ('G', 'R', 'Y'), 
  ('B', 'R', 'Y'), 
  ('B', 'O', 'Y'), 
  ('G', 'W'), 
  ('R', 'W'), 
  ('B', 'W'), 
  ('O', 'W'), 
  ('G', 'Y'), 
  ('R', 'Y'), 
  ('B', 'Y'), 
  ('O', 'Y'), 
  ('G', 'R'), 
  ('G', 'O'), 
  ('B', 'R'), 
  ('B', 'O')
]

COLORS_COORS_NORM_GOAL = { # these are the correct coords for the norm goal state with the keys being the sorted colors
  ('G', 'O', 'W'): (0, 2, 2), 
  ('G', 'R', 'W'): (2, 2, 2), 
  ('B', 'R', 'W'): (2, 0, 2), 
  ('B', 'O', 'W'): (0, 0, 2), 
  ('G', 'O', 'Y'): (0, 2, 0), 
  ('G', 'R', 'Y'): (2, 2, 0), 
  ('B', 'R', 'Y'): (2, 0, 0), 
  ('B', 'O', 'Y'): (0, 0, 0), 
  ('G', 'W'): (1, 2, 2), 
  ('R', 'W'): (2, 1, 2), 
  ('B', 'W'): (1, 0, 2), 
  ('O', 'W'): (0, 1, 2), 
  ('G', 'Y'): (1, 2, 0), 
  ('R', 'Y'): (2, 1, 0), 
  ('B', 'Y'): (1, 0, 0), 
  ('O', 'Y'): (0, 1, 0), 
  ('G', 'R'): (2, 2, 1), 
  ('G', 'O'): (0, 2, 1), 
  ('B', 'R'): (2, 0, 1), 
  ('B', 'O'): (0, 0, 1)
} # dict coords returns this for a cube, i saved this one bc it is a known one I will always need

'''
sticker indices:

      
                00 01 02
                03 04 05
                06 07 08

     36 37 38   18 19 20    09 10 11   45 46 47
     39 40 41   21 22 23    12 13 14   48 49 50
     42 43 44   24 25 26    15 16 17   51 52 53

                27 28 29
                30 31 32
                33 34 35

face colors:

    0
  4 2 1 5
    3

moves:
[ U , U', R , R', F , F', D , D', L , L', B , B']

Initial state = "WWWWWWWWW RRRRRRRRR GGGGGGGGG YYYYYYYYY OOOOOOOOO BBBBBBBBB"
'''


class cube:

  def __init__(self, string="WWWWWWWWW RRRRRRRRR GGGGGGGGG YYYYYYYYY OOOOOOOOO BBBBBBBBB"):
    self.cubeString = string.replace(" ", "")

    if len(self.cubeString) != 54: # if string is not length 24 then it is invalid
      print("Error: Cube string has invalid length.")
      sys.exit(1)
    for letter in ["W", "R", "G", "Y", "O", "B"]: # if 4 of each color is not present it is not valid, this would also exclude invalid colors
      if self.cubeString.count(letter) != 9:
        print("Error: Cube string has invalid colors.")
        sys.exit(1)
    return

  # print state of the cube
  def print(self):
    for i in range(3): # prints the different faces at the correct positions
      print("    " + self.cubeString[i*3] + self.cubeString[i*3+1] + self.cubeString[i*3+2])
    for i in range(3):
      print(self.cubeString[36+i*3] + self.cubeString[37+i*3] + self.cubeString[38+i*3] + " " + self.cubeString[18+i*3] + self.cubeString[19+i*3] + self.cubeString[20+i*3] + " " + self.cubeString[9+i*3] + self.cubeString[10+i*3] + self.cubeString[11+i*3] + " " + self.cubeString[45+i*3] + self.cubeString[46+i*3] + self.cubeString[47+i*3])
    for i in range(3):
      print("    " + self.cubeString[27+i*3] + self.cubeString[28+i*3] + self.cubeString[29+i*3])
    return

  def print3(self, cube1, cube2=None, cube3=None): #prints up to 3 cubes
    if cube3:
      iterations = 2
    elif cube2:
      iterations = 1
    else:
      iterations = 0

    for i in range(3): # prints the different faces at the correct positions
      string = "    " + cube1.cubeString[i*3] + cube1.cubeString[i*3+1] + cube1.cubeString[i*3+2]
      if cube2:
        string += "              " + cube2.cubeString[i*3] + cube2.cubeString[i*3+1] + cube2.cubeString[i*3+2]
      if cube3:
        string += "              " + cube3.cubeString[i*3] + cube3.cubeString[i*3+1] + cube3.cubeString[i*3+2]
      print(string)
    for i in range(3):
      string = cube1.cubeString[36+i*3] + cube1.cubeString[37+i*3] + cube1.cubeString[38+i*3] + " " + cube1.cubeString[18+i*3] + cube1.cubeString[19+i*3] + cube1.cubeString[20+i*3] + " " + cube1.cubeString[9+i*3] + cube1.cubeString[10+i*3] + cube1.cubeString[11+i*3] + " " + cube1.cubeString[45+i*3] + cube1.cubeString[46+i*3] + cube1.cubeString[47+i*3]
      if cube2:
        string += "  " + cube2.cubeString[36+i*3] + cube2.cubeString[37+i*3] + cube2.cubeString[38+i*3] + " " + cube2.cubeString[18+i*3] + cube2.cubeString[19+i*3] + cube2.cubeString[20+i*3] + " " + cube2.cubeString[9+i*3] + cube2.cubeString[10+i*3] + cube2.cubeString[11+i*3] + " " + cube2.cubeString[45+i*3] + cube2.cubeString[46+i*3] + cube2.cubeString[47+i*3]
      if cube3:
        string += "  " + cube3.cubeString[36+i*3] + cube3.cubeString[37+i*3] + cube3.cubeString[38+i*3] + " " + cube3.cubeString[18+i*3] + cube3.cubeString[19+i*3] + cube3.cubeString[20+i*3] + " " + cube3.cubeString[9+i*3] + cube3.cubeString[10+i*3] + cube3.cubeString[11+i*3] + " " + cube3.cubeString[45+i*3] + cube3.cubeString[46+i*3] + cube3.cubeString[47+i*3]
      print(string)
    for i in range(3):
      string = "    " + cube1.cubeString[27+i*3] + cube1.cubeString[28+i*3] + cube1.cubeString[29+i*3]
      if cube2:
        string += "              " + cube2.cubeString[27+i*3] + cube2.cubeString[28+i*3] + cube2.cubeString[29+i*3]
      if cube3:
        string += "              " + cube3.cubeString[27+i*3] + cube3.cubeString[28+i*3] + cube3.cubeString[29+i*3]
      print(string)
    return

  def printThreeCubes(self, cubeList):
    for i in range(0, len(cubeList), 3): # print states to 3 per line
      self.print3(cubeList[i], cubeList[i+1] if i+1 < len(cubeList) else None, cubeList[i+2] if i+2 < len(cubeList) else None)
      print()

  def norm(self): # normalizes cube based on the center colors
    cubeString = self.cubeString
    centers = [4, 13, 22, 31, 40, 49] # each center
    centerColors  = ["W", "R", "G", "Y", "O", "B"] # colors i want at center
    mapping = {}

    for i in range(6): # makes dict of color changes
      mapping[cubeString[centers[i]]] = centerColors[i]

    newCubeString = ""
    for i in range(54): # make new string with color changes
      newCubeString += mapping[cubeString[i]]
    return cube(newCubeString)

  # check if state is solved
  def isSolved(self): # using norm to directly compare to completed string
    return self.equals(cube("WWWWWWWWWRRRRRRRRRGGGGGGGGGYYYYYYYYYOOOOOOOOOBBBBBBBBB"))
  
  def equals(self, cube): # using norm to simplify comparison
    c1 = self.norm().cubeString
    c2 = cube.norm().cubeString

    for i in range(54): # direct comparison of each index of strings
      if c1[i] != c2[i]:
        return False
    return True

  def clone(self): # returns clone of current cube
    return cube(self.cubeString)

  # apply a move to a state
  def applyMove(self, move):
    if move not in MOVES: #check for valid moves
      print("Error: Invalid move provided.")
      sys.exit(1)

    newCubeString = ""
    for index in range(54): #append the value at the position from t he dictionary to the new string
      newCubeString += self.cubeString[MOVES[move][index]]
    
    self.cubeString = newCubeString
    return

  # apply a string sequence of moves to a state
  def applyMovesStr(self, alg, sexy=None): #sexy is used to recreate the direct applyMoveStr, that prints all cube positions from the example
    cloneCube = self.clone()
    if sexy: cubeList = [cloneCube.clone()]
    for move in alg.split(): # run for each move in alg, split to get each move individually
      cloneCube.applyMove(move)
      if sexy:  cubeList.append(cloneCube.clone())

    if sexy: self.printThreeCubes(cubeList)
    return cloneCube

  def shuffle(self, n, sexy1=None): #sexy1 is used for direct calls of shuffle to print nicely
    if not n.isdigit(): # insure valid input
      print("Error: Invalid number of moves.")
      sys.exit(1)

    potentialMoves = [ "U" , "U'", "R" , "R'", "F" , "F'", "D" , "D'", "L" , "L'", "B" , "B'"]

    moves = []
    for i in range(int(n)):
      moves.append(random.choice(potentialMoves)) # add a random move

    moves_str = " ".join(moves) # make the list into a string

    if sexy1: print(moves_str)
    newCube = self.applyMovesStr(moves_str, sexy=sexy1) # apply moves to cube
    return newCube

  def dict_coords(self): # returns a dicitonary of positions/coords
    cstring = self.cubeString
    tupleList = []
    for thing in CORNERS_AND_EDGES: # loops for each corner/edge location of cube
      if len(thing) == 3: # if corner
        tempList = [ cstring[thing[0]], cstring[thing[1]], cstring[thing[2]]  ]
        tempList.sort()# extracts colors into a list, sorts it, and makes a tuple
        tempTuple = (tempList[0], tempList[1], tempList[2])
      elif len(thing) == 2: # if edge
        tempList = [ cstring[thing[0]], cstring[thing[1]]  ]
        tempList.sort()# extracts colors into a list, sorts it, and makes a tuple
        tempTuple = (tempList[0], tempList[1])
      tupleList.append(tempTuple) # add tuple to list
    mapping = {}
    for thing in range(len(CORNERS_AND_EDGES)): # for each corner and edge
      mapping[tupleList[thing]] = XYZ_CORNERS_AND_EDGES[CORNERS_AND_EDGES[thing]] # make a dictionary with key being color of piece and value being its coords
    return mapping

  def heuristic(self, goalDict): # heuristic is the max of corner and edge distance
    selfDict = self.dict_coords() # makes a dict of colors/coords
    cornerDistance = 0
    edgeDistance = 0


    for piece in PIECE_COLORS:
      coords1 = selfDict[piece] # get distances for both pieces
      coords2 = goalDict[piece]
      distance = abs(coords1[0] - coords2[0]) + abs(coords1[1] - coords2[1]) + abs(coords1[2] - coords2[2])
      if len(piece) == 3: # if its len 3 its a corner
        cornerDistance += distance
      else:# otherwise its an edge
        edgeDistance += distance


    return max( (cornerDistance + 7) // 8, (edgeDistance + 7) // 8 ) # take max

  def moves(self, priorMoveList):
    moveList = [ "U" , "U'", "R" , "R'", "F" , "F'", "D" , "D'", "L" , "L'", "B" , "B'"]
    lenList = len(priorMoveList)
    if lenList > 0:
      move1 = priorMoveList[-1]
      if len(move1) == 2:
        moveList.remove(move1[0])
      else:
        moveList.remove(str(move1 + "'"))
    if lenList > 1:
      move1 = priorMoveList[-1]
      move2 = priorMoveList[-2]
      if move1 == move2:
        moveList.remove(move1)

    return moveList

  def bi_astar(self, alg):
    initialStateForward = self.applyMovesStr(alg).norm()
    initialStateBackward = cube()
    nodesExplored = 0 #saving nodes explored
    startTime = time.time() #saving time
    found = False

    forwardHeap = [ ] # each state will be a list including the current state plus moves made to create that state from the initial state
    backwardHeap = [ ]
    counter = 0 # using heap bc lists are really slow
    backwardCoords = initialStateForward.dict_coords()

    #heaps for better runtime
    heapq.heappush(forwardHeap, (initialStateForward.heuristic(COLORS_COORS_NORM_GOAL), 0, counter, initialStateForward.clone(), []))
    heapq.heappush(backwardHeap, (initialStateBackward.heuristic(backwardCoords), 0, counter, initialStateBackward.clone(), []))

    #dict to know repeat states AND to check if both directions met
    forwardRepeatedDict = { initialStateForward.cubeString: [] }
    backwardRepeatedDict = { initialStateBackward.cubeString: [] }

    while(forwardHeap and backwardHeap):
      #forward states
      currentForwardState = heapq.heappop(forwardHeap)
      nodesExplored+= 1 # get new node and increment coutner
      tempStateForward = currentForwardState[3]

      # checking for goal states
      if tempStateForward.isSolved(): # if goal is somehow directly found
        goalList = currentForwardState[4] # set it current list
        break
      elif tempStateForward.cubeString in backwardRepeatedDict: # if match is found on other side
        backwardGoalList = backwardRepeatedDict[tempStateForward.cubeString]
        backwardGoalList.reverse() # get other side list and reverse it
        goalList = currentForwardState[4]
        for item in backwardGoalList:
          if len(item) == 2:
            goalList.append(item[0]) # append opposite moves to goal list
          else:
            goalList.append(item[0] + "'")
        break

      # generate all possible non-redundant moves
      moves = tempStateForward.moves(currentForwardState[4])
      prevMoves = currentForwardState[4]
      lenMoves = len(prevMoves) + 1
      for move in moves: # for each move generated
        newForwardState = tempStateForward.clone() #create new state and apply move
        newForwardState.applyMove(move)
        if (newForwardState.cubeString in forwardRepeatedDict and lenMoves < len(forwardRepeatedDict[newForwardState.cubeString])) or newForwardState.cubeString not in forwardRepeatedDict:
          tempForwardList = prevMoves + [move] # if the move is either shorter than old OR new

          if newForwardState.cubeString in backwardRepeatedDict:
            backwardGoalList = backwardRepeatedDict[newForwardState.cubeString]
            backwardGoalList.reverse() # get other side list and reverse it
            goalList = tempForwardList
            for item in backwardGoalList:
              if len(item) == 2:
                goalList.append(item[0]) # append opposite moves to goal list
              else:
                goalList.append(item[0] + "'")
            found = True
            break

          forwardRepeatedDict[newForwardState.cubeString] = tempForwardList # add to dict

          counter += 1 # push to heap
          heapq.heappush(forwardHeap, (newForwardState.heuristic(COLORS_COORS_NORM_GOAL) + currentForwardState[1] + 1, currentForwardState[1] + 1, counter, newForwardState, tempForwardList))
      if found:
        break

      #backward states
      currentBackwardState = heapq.heappop(backwardHeap)
      nodesExplored+= 1 # get new node and increment coutner
      tempStateBackward = currentBackwardState[3]

      # checking for goal states
      if tempStateBackward.equals(initialStateForward): # if goal is somehow directly found
        goalList = currentBackwardState[4] # set it current list
        break
      elif tempStateBackward.cubeString in forwardRepeatedDict: # if match is found on other side
        backwardGoalList = currentBackwardState[4]
        backwardGoalList.reverse() # get other side list and reverse it
        goalList = forwardRepeatedDict[tempStateBackward.cubeString]
        for item in backwardGoalList:
          if len(item) == 2:
            goalList.append(item[0]) # append opposite moves to goal list
          else:
            goalList.append(item[0] + "'")
        break

      # generate all possible non-redundant moves
      moves = tempStateBackward.moves(currentBackwardState[4])
      prevMoves = currentBackwardState[4]
      lenMoves = len(prevMoves) + 1
      for move in moves: # for each move generated
        newBackwardState = tempStateBackward.clone() #create new state and apply move
        newBackwardState.applyMove(move)
        if (newBackwardState.cubeString in backwardRepeatedDict and lenMoves < len(backwardRepeatedDict[newBackwardState.cubeString])) or newBackwardState.cubeString not in backwardRepeatedDict:
          tempBackwardList = prevMoves + [move] # if the move is either shorter than old OR new
          
          if newBackwardState.cubeString in forwardRepeatedDict:
            backwardGoalList = tempBackwardList
            backwardGoalList.reverse() # get other side list and reverse it
            goalList = forwardRepeatedDict[newBackwardState.cubeString]
            for item in backwardGoalList:
              if len(item) == 2:
                goalList.append(item[0]) # append opposite moves to goal list
              else:
                goalList.append(item[0] + "'")
            found = True
            break
          
          backwardRepeatedDict[newBackwardState.cubeString] = tempBackwardList # add to dict

          counter += 1 # push to heap
          heapq.heappush(backwardHeap, (newBackwardState.heuristic(backwardCoords) + currentBackwardState[1] + 1, currentBackwardState[1] + 1, counter, newBackwardState, tempBackwardList))
      if found:
        break
    timeVal = round((time.time() - startTime),4)
    print(" ".join(goalList))
    c = initialStateForward.clone()
    c.applyMovesStr(" ".join(goalList),sexy=1)
    print(nodesExplored)
    print(timeVal)
    return

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Error: Too few arguments provided.")
    sys.exit(1)
  elif len(sys.argv) > 5:
    print("Error: Too many arguments provided.")
    sys.exit(1)

  command = sys.argv[1]

  if command == "print":
    if len(sys.argv) > 3: # cleans input
      print("Error: Invalid number of arguments for print command.")
      sys.exit(1)
    elif len(sys.argv) == 3: # checks for if cube string was provided
      c = cube(sys.argv[2])
    else:
      c = cube()
    c.print()

  elif command == "goal":
    if len(sys.argv) > 3: # cleans input
      print("Error: Invalid number of arguments for goal command.")
      sys.exit(1)

    if len(sys.argv) == 3: # checks for if cube string was provided
      c = cube(sys.argv[2])
    else: # generate default cube
      c = cube()
  
    if c.isSolved(): # check for solved
      print("True")
    else:
      print("False")

  elif command == "applyMovesStr":
    if len(sys.argv) > 4 or len(sys.argv) < 3: # cleans input
      print("Error: Invalid number of arguments for applyMovesStr command.")
      sys.exit(1)
    elif len(sys.argv) == 4: # pass arg if cube string was given
      c = cube(sys.argv[3])
    else: #generate default cube otherwise
      c = cube()
    c2 = c.applyMovesStr(sys.argv[2], sexy=1)

  elif command == "shuffle":
    if len(sys.argv) != 3: # cleans input
      print("Error: Invalid number of arguments for shuffle command.")
      sys.exit(1)

    c = cube()
    c2 = c.shuffle(sys.argv[2], sexy1=1)

  elif command == "bi_astar":
    if len(sys.argv) != 3: # cleans input
      print("Error: Invalid number of arguments for bi_astar command.")
      sys.exit(1)

    c=cube()
    c.bi_astar(sys.argv[2])

  else:
    print("Error: Invalid command")
    exit(1)