import chess
import random

class Evaluation:
    """
        This class calculates useful information to use in th evaluation function.
    """

    # Calculates the piece difference of both sides with weights that calculated, assigned, and adjusted to fit in a 0 to 1 scale.
    def pieceDifference(self, board, color):
        score = 0
        for (piece, value) in [(chess.PAWN, 0.004448), (chess.BISHOP, 0.01468), (chess.KING, 0.88968),\
                            (chess.QUEEN, 0.040036), (chess.KNIGHT, 0.014235), (chess.ROOK, 0.022242)]:
            score += (len(board.pieces(piece, color)) - len(board.pieces(piece, not color))) * value
        return score

    def pawnStructure(self, board, color):
        ourPawns = list(board.pieces(chess.PAWN, color))
        enemyPawns = list(board.pieces(chess.PAWN, not color))
        ourPawnIslands = 1
        enemyPawnIslands = 1
        if len(ourPawns) > 0:
            firstSquare = ourPawns[0]
            for square in ourPawns:
                if chess.square_distance(firstSquare, square) > 1:
                    ourPawnIslands += 1
                firstSquare = square
        if len(enemyPawns) > 0:
            firstSquare = enemyPawns[0]
            for square in enemyPawns:
                if chess.square_distance(firstSquare, square) > 1:
                    enemyPawnIslands += 1
                firstSquare = square
        return enemyPawnIslands - ourPawnIslands
        
    # Calculates the difference between piece development of each piece at its respective square of both sides with weights that calculated, assigned, and adjusted to fit in a 0 to 1 scale.
    def pieceDevelopment(self, board, color):
        king_developmentTable = [[-0.03, -0.04, -0.04, -0.05, -0.05, -0.04, -0.04, -0.03], 
                                 [-0.03, -0.04, -0.04, -0.05, -0.05, -0.04, -0.04, -0.03], 
                                 [-0.03, -0.04, -0.04, -0.05, -0.05, -0.04, -0.04, -0.03], 
                                 [-0.03, -0.04, -0.04, -0.05, -0.05, -0.04, -0.04, -0.03], 
                                 [-0.02, -0.03, -0.03, -0.04, -0.04, -0.03, -0.03, -0.02], 
                                 [-0.01, -0.02, -0.02, -0.02, -0.02, -0.02, -0.02, -0.01], 
                                 [0.02, 0.02, 0.00, 0.00, 0.00, 0.00, 0.02, 0.02], 
                                 [0.02, 0.03, 0.01, 0.00, 0.00, 0.01, 0.03, 0.02]]

        queen_developmentTable = [[-0.02, -0.01, -0.01, -0.005, -0.005, -0.01, -0.01, -0.02], 
                                 [-0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, -0.01], 
                                 [-0.01, 0.00, 0.005, 0.01, 0.01, 0.005, 0.00, -0.01], 
                                 [-0.005, 0.00, 0.01, 0.015, 0.015, 0.01, 0.00, -0.005], 
                                 [-0.005, 0.00, 0.01, 0.015, 0.015, 0.01, 0.00, -0.005], 
                                 [-0.01, 0.00, 0.005, 0.01, 0.01, 0.005, 0.00, -0.01], 
                                 [-0.01, 0.00, 0.000, 0.00, 0.00, 0.00, 0.00, -0.01], 
                                 [-0.02, -0.01, -0.01, -0.005, -0.005, -0.01, -0.01, -0.02]]

        rook_developmentTable = [[-0.02, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.02], 
                                 [-0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, -0.01], 
                                 [-0.01, 0.005, 0.01, 0.01, 0.01, 0.01, 0.005, -0.01], 
                                 [-0.01, 0.01, 0.01, 0.015, 0.015, 0.01, 0.01, -0.01], 
                                 [-0.01, 0.01, 0.01, 0.015, 0.015, 0.01, 0.01, -0.01], 
                                 [-0.01, 0.005, 0.01, 0.01, 0.01, 0.01, 0.005, -0.01], 
                                 [-0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, -0.01], 
                                 [-0.02, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.02]]

        bishop_developmentTable = [[-0.02, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.02], 
                                   [-0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, -0.01], 
                                   [-0.01, 0.00, 0.005, 0.01, 0.01, 0.005, 0.00, -0.01], 
                                   [-0.01, 0.005, 0.005, 0.015, 0.015, 0.005, 0.005, -0.01], 
                                   [-0.01, 0.00, 0.01, 0.015, 0.015, 0.01, 0.00, -0.01], 
                                   [-0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, -0.01], 
                                   [-0.01, 0.005, 0.00, 0.00, 0.00, 0.00, 0.005, -0.01], 
                                   [-0.02, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.02]]

        knight_developmentTable = [[-0.05, -0.04, -0.03, -0.03, -0.03, -0.03, -0.04, -0.05], 
                                   [-0.04, -0.02, 0.00, 0.00, 0.00, 0.00, -0.02, -0.04], 
                                   [-0.03, 0.00, 0.01, 0.015, 0.015, 0.01, 0.00, -0.03], 
                                   [-0.03, 0.005, 0.015, 0.02, 0.02, 0.015, 0.005, -0.03], 
                                   [-0.03, 0.00, 0.015, 0.02, 0.02, 0.015, 0.00, -0.03], 
                                   [-0.03, 0.005, -0.01, 0.015, 0.015, -0.01, 0.005, -0.03], 
                                   [-0.04, -0.02, 0.00, 0.005, 0.005, 0.00, -0.02, -0.04], 
                                   [-0.05, -0.04, -0.03, -0.03, -0.03, -0.03, -0.04, -0.05]]

        pawn_developmentTable =  [[0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00], 
                                  [0.015, 0.015, 0.015, 0.015, 0.015, 0.015, 0.015, 0.015], 
                                  [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], 
                                  [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], 
                                  [0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005], 
                                  [0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005], 
                                  [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00], 
                                  [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]]

        developmentTables = [king_developmentTable, queen_developmentTable, rook_developmentTable, \
                             bishop_developmentTable, knight_developmentTable, pawn_developmentTable]
        ourDevelopment = 0
        enemyDevelopment = 0
        for square in range(64):
            if board.color_at(square) == color:
                ourDevelopment += developmentTables[6 - board.piece_type_at(square)][7 - int((square - square % 8)/8)][square % 8]
            elif board.color_at(square) and board.color_at(square) != color:
                enemyDevelopment += developmentTables[6 - board.piece_type_at(square)][int((square - square % 8)/8)][square % 8]
        return ourDevelopment - enemyDevelopment

    # Calculates a integer of the difference of center control of both sides
    def centerControl(self, board, color):
        oppositeControl = 0
        ownControl = 0
        center = [(chess.D5, chess.BB_D5), (chess.E5, chess.BB_E5), (chess.D4, chess.BB_D4), (chess.E4, chess.BB_E4)]
        for num, square in center:
            ownControl += len(list(board.attackers(color, num)))
            oppositeControl += len(list(board.attackers(not color, num)))
        return ownControl - oppositeControl

    # Adds up all features to calculate a final evaluation
    def finalEvaluation(self, board, color):
        weights = [1.00, 1.00, 0.05, 0.05]
        result = weights[0] * self.pieceDifference(board, color) + weights[1] * self.pieceDevelopment(board, color) + \
                 weights[2] * self.centerControl(board, color) + weights[3] * self.pawnStructure(board, color)
        return result

