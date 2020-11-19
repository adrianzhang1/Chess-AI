import random
import chess
import time

class Player:
    def __init__(self, board, color, t):
        self.color=color
        if self.color==chess.BLACK:
            print("I AM BLACK")
        else:
            print("I AM WHITE")
        self.depth = 2
        #self.mateval = {"P": 10, "N": 30, "B": 30, "R": 50, "Q": 90, "K": 900, "p": -10, "n": -30, "b": -30, "r": -50, "q": -90, "k": -900}
        self.mateval = [0,10,30,30,50,90,900]

        self.poseval = {"P":[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5, 0.5, -0.5, 1.0, 0.0, 0.0, -1.0, -0.5, 0.5, 0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0, 0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5, 1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 
            "N":[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0, -4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0, -3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0, -3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0, -3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0, -3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0, -4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0, -5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0], 
            "B":[-2, -1, -1, -1, -1, -1, -1, -2, -1, 0.5, 0, 0, 0, 0, 0.5, -1,  -1, 1, 1, 1, 1, 1, 1, -1, -1, 0, 1, 1, 1, 1, 0, -1, -1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1, -1, 0, 0.5, 1, 1, 0.5, 0, -1, -1, 0, 0, 0, 0, 0, 0, -1, -2, -1, -1, -1, -1, -1, -1, -2],
            "R":[0, 0, 0, 0.5, 0.5, 0, 0, 0, -.5, 0, 0, 0, 0, 0, 0, -.5,-.5, 0, 0, 0, 0, 0, 0, -.5,-.5, 0, 0, 0, 0, 0, 0, -.5,-.5, 0, 0, 0, 0, 0, 0, -.5,-.5, 0, 0, 0, 0, 0, 0, -.5, .5, 1, 1, 1, 1, 1, 1, .5, 0, 0, 0, 0, 0, 0, 0, 0 ],
            "Q":[-2, -1, -1, -.5, -.5, -1, -1, -2, -1, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1, -1, .5, .5, .5, .5, .5, 0.0, -1, 0, 0, 0.5, .5, .5, .5, 0.0, -.5, -.5, 0, .5, .5, .5, .5, 0, -.5, -1, 0, .5, .5, .5, .5, 0, -1, -1, 0, 0, 0, 0, 0, 0, -1, -2, -1, -1, -.5, -.5, -1, -1, -2],
            "K":[2, 3, 1, 0, 0, 1, 3, 2, 2, 2, 0, 0, 0, 0, 2, 2, -1, -2, -2, -2, -2, -2, -2, -1,-2, -3, -3, -4, -4, -3, -3, -2, -3, -4, -4, -5, -5, -4, -4, -3,-3, -4, -4, -5, -5, -4, -4, -3,-3, -4, -4, -5, -5, -4, -4, -3,-3, -4, -4, -5, -5, -4, -4, -3]}
        
    def eval(self,boardd):
        score=0
        temp=boardd
        
        if (temp.is_game_over()):
            if (temp.is_variant_draw()):
                return 0
            if (temp.turn == self.color):
                return float("inf")
            else:
                return -float("inf")

        for x in range(8):
            for y in range(8):
                piece=temp.piece_at(chess.SQUARES[x + 8*y])
                if not(piece == None):
                    p=piece.symbol()
                    if (piece.color==self.color):
                        #print(piece.piece_type)
                        score += self.mateval[piece.piece_type] + self.poseval[p.upper()][x + 8*y]
                    else:
                        #print(piece.piece_type)

                        score -= self.mateval[piece.piece_type]
        
        if (temp.is_check()):
            if (temp.turn == self.color):
                score+=20
            else:
                score -=20
            #print("someone can check!")
        
        return score
    def smartEval(self,oldBoard,move,prevEval):

        oldBoard.push(move)
        
        if (oldBoard.is_game_over()):
            if (oldBoard.is_variant_draw()):
                return 0
            if (oldBoard.turn == self.color):
                return float("inf")
            else:
                return -float("inf")

        if (oldBoard.is_check() and ( oldBoard.turn == self.color)):
            score+=1000
            print("i can check!")
        
        oldBoard.pop()

        score=0
        p = oldBoard.piece_at(move.from_square)
        score -= self.poseval[p][chess.parse_square(move.from_square)]
        score += self.poseval[p][chess.parse_square(move.to_square)]

        ep= oldBoard.piece_at(move.to_square)
        if not ep==None:
            score+=self.mateval[p]
        
        if (self.color == chess.BLACK):
            score = -1 * score

        score+=prevEval
        return score
    def move(self, board, t):
        if (self.color==chess.BLACK):
            board.mirror()
        action=self.moveHelper(board,self.color, 0,-float('inf'),float('inf'))
        #print(action)
        return action
        
    def moveHelper(self, board, col, curDepth, alpha, beta):
        
        if (curDepth == self.depth or board.is_game_over()):
            return self.eval(board)
        actionList = dict()
        oldAgentIndex = col
        oldCurDepth = curDepth
        
        if col==chess.BLACK:
            col=chess.WHITE
        else:
            col=chess.BLACK

        if col==self.color:
            curDepth += 1
        
        legals = list(board.legal_moves)

        for i in legals:
            board.push(i)
            actionList[i] = self.moveHelper(board, col, curDepth,alpha,beta)
            board.pop()
            if not col==self.color:
                if actionList[i]>beta: return actionList.get(i)
                alpha=max(alpha,actionList.get(i))
            else:
                if actionList[i]<alpha: return actionList.get(i)
                beta=min(beta,actionList.get(i))

        if not col==self.color:
            if oldCurDepth == 0:
                #print("FLAG")
                #print(curDepth)
                return max(actionList, key=actionList.get)
            return max(actionList.values())
        return min(actionList.values())


