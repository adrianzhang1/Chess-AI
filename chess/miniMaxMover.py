import random
import chess
import time
from chess import polyglot

class Player:
    def __init__(self, board, color, t):
        self.color=color
        if self.color==chess.BLACK:
            print("I AM BLACK")
        else:
            print("I AM WHITE")
        self.depth = 1
        #self.mateval = {"P": 10, "N": 30, "B": 30, "R": 50, "Q": 90, "K": 900, "p": -10, "n": -30, "b": -30, "r": -50, "q": -90, "k": -900}
        self.mateval = [0,10,30,30,50,90,900]
        self.reader=chess.polyglot.open_reader("opening.bin")

        self.poseval = {"P":[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5, 0.5, -0.5, 1.0, 0.0, 0.0, -1.0, -0.5, 0.5, 0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0, 0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5, 1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 
            "N":[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0, -4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0, -3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0, -3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0, -3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0, -3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0, -4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0, -5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0], 
            "B":[-2, -1, -1, -1, -1, -1, -1, -2, -1, 0.5, 0, 0, 0, 0, 0.5, -1,  -1, 1, 1, 1, 1, 1, 1, -1, -1, 0, 1, 1, 1, 1, 0, -1, -1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1, -1, 0, 0.5, 1, 1, 0.5, 0, -1, -1, 0, 0, 0, 0, 0, 0, -1, -2, -1, -1, -1, -1, -1, -1, -2],
            "R":[0, 0, 0, 0.5, 0.5, 0, 0, 0, -.5, 0, 0, 0, 0, 0, 0, -.5,-.5, 0, 0, 0, 0, 0, 0, -.5,-.5, 0, 0, 0, 0, 0, 0, -.5,-.5, 0, 0, 0, 0, 0, 0, -.5,-.5, 0, 0, 0, 0, 0, 0, -.5, .5, 1, 1, 1, 1, 1, 1, .5, 0, 0, 0, 0, 0, 0, 0, 0 ],
            "Q":[-2, -1, -1, -.5, -.5, -1, -1, -2, -1, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1, -1, .5, .5, .5, .5, .5, 0.0, -1, 0, 0, 0.5, .5, .5, .5, 0.0, -.5, -.5, 0, .5, .5, .5, .5, 0, -.5, -1, 0, .5, .5, .5, .5, 0, -1, -1, 0, 0, 0, 0, 0, 0, -1, -2, -1, -1, -.5, -.5, -1, -1, -2],
            "K":[2, 3, 1, 0, 0, 1, 3, 2, 2, 2, 0, 0, 0, 0, 2, 2, -1, -2, -2, -2, -2, -2, -2, -1,-2, -3, -3, -4, -4, -3, -3, -2, -3, -4, -4, -5, -5, -4, -4, -3,-3, -4, -4, -5, -5, -4, -4, -3,-3, -4, -4, -5, -5, -4, -4, -3,-3, -4, -4, -5, -5, -4, -4, -3]}
        
        if self.color==chess.BLACK: #change piece tables
            for key in self.poseval.keys():
                table=[[]]
                for y in range(8):
                    row=[]
                    for x in range(8):
                        row.append(self.poseval[key][y*8+x])
                    table.append(row)
                table=table[::-1]
                for i in range(8):
                    table[i]=table[i][::-1]

                out=[]
                for r in table:
                    out+=r
                self.poseval[key]=out
        

    def eval(self,boardd):
        score=0
        temp=boardd
        
        if (temp.is_game_over()):
            if (temp.is_variant_draw()):
                return 0
            if (temp.turn == self.color):
                return -float("inf")
            else:
                return float("inf")

        for x in range(8):
            for y in range(8):
                piece=temp.piece_at(chess.SQUARES[x + 8*y])
                if not(piece == None):
                    p=piece.symbol()
                    if (piece.color==self.color):
                        score += self.mateval[piece.piece_type] + self.poseval[p.upper()][x + 8*y]
                    else:
                        score -= self.mateval[piece.piece_type]
        
        if (temp.is_check()): #checking bonus
            if (temp.turn == self.color):
                score+=1
            else:
                score-=1
        
        return score
    def incrEval(self,oldBoard,newBoard,move,prevEval):
        incr = 0

        if (newBoard.is_game_over()):
            if (newBoard.is_variant_draw()):
                return 0
            if (newBoard.turn == self.color):
                return -float("inf")
            else:
                return float("inf")

        fromPiece = oldBoard.piece_at(move.from_square)
        toPiece=oldBoard.piece_at(move.to_square)
        if fromPiece.color==self.color:
            if toPiece: #enemy piece was taken, add mateval
                incr += self.mateval[toPiece.piece_type]

            #subtract previous piece poseval and add new poseval
            incr -= self.poseval[fromPiece.symbol().upper()][move.from_square]
            incr += self.poseval[fromPiece.symbol().upper()][move.to_square]

            if move.promotion: # a friendly promotion happened
                incr += self.mateval[move.promotion]
        else:
            if toPiece: #friendly piece taken, subtract mateval and poseval
                incr -= self.mateval[toPiece.piece_type]
                incr -= self.poseval[toPiece.symbol().upper()][move.to_square]
            
            if move.promotion: # an enemy promotion happened
                incr -= self.mateval[move.promotion]
        return prevEval+incr
        
    
    def move(self, board, t):
        eval=self.eval(board)
        legals = list(board.legal_moves)
        length=len(legals)
        
        if length<22:
            self.depth=2
        else:
            self.depth=1

        action=None
        max = -float("inf")
        for entry in self.reader.find_all(board):
            if (max < entry.weight):
                max = entry.weight
                action = entry.move
        
        if action==None:
            action=self.moveHelper(board, self.color, eval, 0,-float('inf'),float('inf'))
        
            
        return action
        
    def moveHelper(self, board, col, prevEval, curDepth, alpha, beta):
        
        if (curDepth == self.depth or board.is_game_over()):
            return prevEval
            #return self.eval(board)
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
        
        #legals = self.moveOrder(legals,board)

        for i in legals:
            oldBoard=board.copy()
            board.push(i)
            nextPrevEval=self.incrEval(oldBoard,board,i,prevEval)
            actionList[i] = self.moveHelper(board, col, nextPrevEval, curDepth, alpha, beta)
            board.pop()
            if not col==self.color:
                if actionList[i]>beta: return actionList.get(i)
                alpha=max(alpha,actionList.get(i))
            else:
                if actionList[i]<alpha: return actionList.get(i)
                beta=min(beta,actionList.get(i))

        if not col==self.color:
            if oldCurDepth == 0:
                return max(actionList, key=actionList.get)
            return max(actionList.values())
        return min(actionList.values())

    def moveOrder(self, moves, board):
        out=[]
        sortedList=[[]]*7

        for move in moves:
            sortedList[board.piece_at(move.from_square).piece_type].append(move)
        
        for lst in sortedList:
            out+=lst
        return out
        