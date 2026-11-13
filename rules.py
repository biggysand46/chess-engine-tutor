from keyvariables import *
from pieces import *

class Rules:

    def __init__(self, game):
        self.game = game

    def IsInCheck(self, colour):
        king = self.game.board.GetKing(colour)

        if king == None:
            return False

        king_index = king.properties["index"]
        opponent_colour = "w" if colour == "b" else "b"
        
        # Checking if the king is in the opponents possible moves
        for _piece in self.game.board.pieces[opponent_colour]:
            moves = _piece.GetUnsimulatedMoves()
            if king_index in moves:
                return True
        return False
    
    def IsCheckmate(self, colour):
        if not self.IsInCheck(colour):
            return False
        
        for piece in self.game.board.pieces[colour]:
            if piece.GetSimulatedMoves():
                return False
            
        return True
    
    def IsPromotionMove(self, piece, index):
        target_rank = 0 if piece.properties["colour"] == "w" else 7
        if index // 8 == target_rank:
            return True
        return False

    def CheckForChecks(self):
        if self.IsInCheck(self.game.turn):
            king_index = self.game.board.GetKing(self.game.turn).properties["index"]
            self.game.board.GetElementById(king_index).CheckTile()

    def CastleCheck(self, piece, index):
        start_index = piece.properties["index"]
        # Checking for castling
        if isinstance(piece, King) and abs(index - start_index) == 2:
            # Castling on the king's side
            if index > start_index:
                rook_original = start_index + 3
                rook_destination = start_index + 1
            # Castling on the queen's side
            else:
                rook_original = start_index - 4
                rook_destination = start_index - 1

            rook = self.game.board.piece_map[rook_original]
            if rook:
                self.game.board.MovePiece(rook, rook_destination)
                self.game.board.UpdatePieceImage(rook)
                rook.moved = True
                return True
        return False
    
    def PawnPromotionCheck(self, piece, index):
        if isinstance(piece, Pawn):
            rank = index // 8
            if ((piece.properties["colour"] == "w" and rank == 0)
                or (piece.properties["colour"] == "b" and rank == 7)):
                self.PromotePawn(piece)
    
    def EnPassantCheck(self, piece, index):
        # En passant move
        if isinstance(piece, Pawn) and self.game.en_passant_target is not None:
            if index == self.game.en_passant_target:
                captured_index = (self.game.en_passant_target + 8
                                if piece.properties["colour"] == "w"
                                else self.game.en_passant_target - 8)
                self.game.board.RemovePiece(self.game.board.piece_map[captured_index])
                self.game.board.piece_map[captured_index] = 0

    def UpdateEnPassantTarget(self, piece, index):
        start_index = piece.properties["index"]
        self.game.en_passant_target = None
        if isinstance(piece, Pawn) and abs(index - start_index) == 16:
            self.game.en_passant_target = (start_index + index) // 2

    def PromotePawn(self, piece):
        pawn_index = piece.properties["index"]
        pawn_colour = piece.properties["colour"]

        # Removing the pawn from the board
        self.game.board.RemovePiece(piece)
        self.game.board.piece_map[pawn_index] = 0

        promoted_piece = self.game.board.CreatePiece("q" if pawn_colour == "b" else "Q", pawn_index)
        self.game.board.pieces[pawn_colour].append(promoted_piece)
        self.game.board.UpdatePieceImage(promoted_piece)
        self.game.screen.ui_elements.append(promoted_piece.GetImage())

class TutorialRules(Rules):

    def __init__(self, game):
        super().__init__(game)

    def PromotePawn(self, piece):
        super().PromotePawn(piece)

        # Going to next stage in tutorial
        if self.game.tutorial_stage == 0:
            self.game.return_function()

class PuzzleRules(Rules):

    def __init__(self, game):
        super().__init__(game)

class AIRules(Rules):

    def __init__(self, game):
        super().__init__(game)