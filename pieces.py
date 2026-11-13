from keyvariables import *
from ui import *

class BasePiece:

    def __init__(self, **properties):
        default_properties = {"x":0, "y":0, "colour":"w", "index":None}
        self.properties = {**default_properties, **properties}
        self.InitalisePieceVariables(**properties)
        self.CreatePieceImage()

    def InitalisePieceVariables(self, **properties):
        self.board = properties["board"]
        self.moved = False
    
    def CreatePieceImage(self):
        self.image = Image(
            x=self.properties["x"], y=self.properties["y"],
            width=self.properties["size"], height=self.properties["size"],
            img_source=f"assets/{self.properties["colour"]}{self.piece_type}.png"
        )

    def GetImage(self):
        return self.image
    
    def UpdateProperty(self, **properties):
        self.image.properties.update(**properties) 

    def SimulatePieceMoves(self, moves):
        legal_moves = []

        for move in moves:
            piece_index = self.properties["index"]
            captured_piece = self.board.game.SimulateMove(self, move)
            captured_index = captured_piece.properties["index"] if captured_piece != None else None

            # Checking whether the king is in check
            if not self.board.game.rules.IsInCheck(self.properties["colour"]):
                legal_moves.append(move)

            self.board.game.UndoSimulationMove(self, piece_index, captured_piece, captured_index)
        return legal_moves

    def GetSimulatedMoves(self):
        moves = self.GetUnsimulatedMoves()
        moves = self.SimulatePieceMoves(moves)
        return moves

class SlidingPiece(BasePiece):
    
    def __init__(self, **properties):
        super().__init__(**properties)

    def PotentialMoves(self):
        moves = []

        for move in self.direction_moves:
            current_index = self.properties["index"]

            while True:
                file = current_index % 8
                # Prevents moves from wrapping round the edge of the board
                if move in [1, 9, -7] and file == 7:
                    break
                if move in [7, -1, -9] and file == 0:
                    break

                new_index = current_index + move
                if new_index < 0 or new_index > 63:
                    break

                obstructing_piece = self.board.piece_map[new_index]
                if obstructing_piece:
                    if obstructing_piece.properties["colour"] != self.properties["colour"]:
                        moves.append(new_index)
                    break
                else:
                    moves.append(new_index)
                    current_index = new_index

        return moves  

class Pawn(BasePiece):

    def __init__(self, **properties):
        self.piece_type = "p"
        super().__init__(**properties)
        self.multiplier = -1 if self.properties["colour"] == "w" else 1
        if self.properties["index"] // 8 != 1 and self.properties["index"] // 8 != 6:
            self.moved = True

    def PotentialForwardMoves(self):
        # Pawn can move two tiles if they haven't yet moved
        index = self.properties["index"]
        moves = []
        potential_moves = [8 * self.multiplier] if self.moved else [8 * self.multiplier, 16 * self.multiplier]
        for move in potential_moves:
            if index + move < 0 or index + move > 63:
                continue
            if self.board.piece_map[index + move]:
                break
            moves.append(index + move)
        return moves
    
    def PotentialCaptureMoves(self):
        potential_moves = []
        for move in [7 * self.multiplier, 9 * self.multiplier]:
            if self.properties["index"] + move > 63 or self.properties["index"] + move < 0:
                continue
            potential_piece = self.board.piece_map[self.properties["index"] + move]
            if potential_piece:
                if potential_piece.properties["colour"] != self.properties["colour"]:
                    potential_moves.append(self.properties["index"] + move)
        return potential_moves
    
    def PotentialEnPassantMoves(self):
        moves = []
        if self.board.game.en_passant_target is not None:
            for move in [7, 9]:
                target = self.properties["index"] + (move * self.multiplier)
                if target == self.board.game.en_passant_target:
                    moves.append(target)
        return moves

    def VerifyMoves(self, moves):
        piece_file = self.properties["index"] % 8
        piece_rank = self.properties["index"] // 8
        verified_moves = []

        for move in moves:
            new_file, new_rank = move % 8, move // 8
            if abs(piece_file - new_file) in (0, 1, 2) and abs(piece_rank - new_rank) in (1, 2):
                verified_moves.append(move)
        return verified_moves

    def GetUnsimulatedMoves(self):
        moves = self.PotentialForwardMoves() + self.PotentialCaptureMoves() + self.PotentialEnPassantMoves()
        moves = self.VerifyMoves(moves)
        return moves

class Rook(SlidingPiece):

    def __init__(self, **properties):
        self.piece_type = "r"
        super().__init__(**properties)
        self.direction_moves = [1, 8, -1, -8] 

    def GetUnsimulatedMoves(self):
        return self.PotentialMoves()

class Bishop(SlidingPiece):

    def __init__(self, **properties):
        self.piece_type = "b"
        super().__init__(**properties)
        self.direction_moves = [7, -7, 9, -9]
    
    def GetUnsimulatedMoves(self):
        return self.PotentialMoves()

class Knight(BasePiece):

    def __init__(self, **properties):
        self.piece_type = "n"
        super().__init__(**properties)
        self.potential_moves = [6, -6, 10, -10, 15, -15, 17, -17]

    def GetPotentialMoves(self):
        index = self.properties["index"]
        index_file = index % 8
        index_rank = index // 8
        moves = []

        for move in self.potential_moves:
            new_index = index + move

            # Checking piece remains within board
            if new_index < 0 or new_index > 63:
                continue

            new_file = new_index % 8
            new_rank = new_index // 8

            # Prevents moves from wrapping round the edge of the board
            if abs(new_file - index_file) in [1, 2] and abs(new_rank - index_rank) in [1, 2]:
                obstructing_piece = self.board.piece_map[new_index]

                if obstructing_piece:
                    if obstructing_piece.properties["colour"] == self.properties["colour"]:
                        continue
                moves.append(new_index)
        
        return moves
    
    def GetUnsimulatedMoves(self):
        return self.GetPotentialMoves()

class Queen(SlidingPiece):

    def __init__(self, **properties):
        self.piece_type = "q"
        super().__init__(**properties)
        self.direction_moves = [1, 8, -1, -8, 7, -7, 9, -9]

    def GetUnsimulatedMoves(self):
        return self.PotentialMoves()

class King(BasePiece):

    def __init__(self, **properties):
        self.piece_type = "k"
        super().__init__(**properties)
        self.potential_moves = [1, -1, 7, -7, 8, -8, 9, -9]

    def GetPotentialMoves(self):
        index = self.properties["index"]
        index_file = index % 8
        index_rank = index // 8
        moves = []

        for move in self.potential_moves:
            new_index = index + move

            # Checking piece remains within board
            if new_index < 0 or new_index > 63:
                continue

            new_file = new_index % 8
            new_rank = new_index // 8

            # Prevents moves from wrapping round the edge of the board
            if abs(new_file - index_file) <= 1 and abs(new_rank - index_rank) <= 1:
                obstructing_piece = self.board.piece_map[new_index]

                if obstructing_piece:
                    if obstructing_piece.properties["colour"] == self.properties["colour"]:
                        continue
                moves.append(new_index)

        return moves
    
    def GetCastlingMoves(self):
        return self.CheckKingSideCastle() + self.CheckQueenSideCastle()

    def CheckKingSideCastle(self):
        index = self.properties["index"]
        board = self.board
        moves = []

        king_side_rook = self.GetKingSideRook()
        if (king_side_rook
            and not king_side_rook.moved
            and board.piece_map[index + 1] == 0
            and board.piece_map[index + 2] == 0):

            # Simulating and gathering check result for adjacent squares
            board.game.SimulateMove(self, index + 1)
            first_square_check = board.game.rules.IsInCheck(self.properties["colour"])
            board.game.UndoSimulationMove(self, index)


            board.game.SimulateMove(self, index + 2)
            second_square_check = board.game.rules.IsInCheck(self.properties["colour"])
            board.game.UndoSimulationMove(self, index)

            if not first_square_check and not second_square_check:
                moves.append(index + 2)
        return moves

    def CheckQueenSideCastle(self):
        index = self.properties["index"]
        board = self.board
        moves = []

        queen_side_roook = self.GetQueenSideRook()
        if (queen_side_roook
            and not queen_side_roook.moved
            and board.piece_map[index - 1] == 0
            and board.piece_map[index - 2] == 0
            and board.piece_map[index - 3] == 0):

            # Simulating and gathering check result for adjacent squares
            board.game.SimulateMove(self, index - 1)
            first_square_check = board.game.rules.IsInCheck(self.properties["colour"])
            board.game.UndoSimulationMove(self, index)

            board.game.SimulateMove(self, index - 2)
            second_square_check = board.game.rules.IsInCheck(self.properties["colour"])
            board.game.UndoSimulationMove(self, index)

            if not first_square_check and not second_square_check:
                moves.append(index - 2)
        return moves
    
    def GetKingSideRook(self):
        rank = self.properties["index"] // 8
        king_side_rook = self.board.piece_map[rank * 8 + 7]

        if isinstance(king_side_rook, Rook):
            return king_side_rook
        return None

    def GetQueenSideRook(self):
        rank = self.properties["index"] // 8
        queen_side_rook = self.board.piece_map[rank * 8]

        if isinstance(queen_side_rook, Rook):
            return queen_side_rook
        return None
    
    def GetUnsimulatedMoves(self):
        moves = self.GetPotentialMoves()
        return moves
    
    def GetSimulatedMoves(self):
        moves = self.GetUnsimulatedMoves()
        moves = self.SimulatePieceMoves(moves)
        if not self.moved and not self.board.game.rules.IsInCheck(self.properties["colour"]):
            moves = moves + self.GetCastlingMoves()
        return moves