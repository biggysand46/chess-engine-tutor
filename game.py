from keyvariables import *
from board import *
from rules import *
class Game:

    def __init__(self, **properties):
        self.screen = properties["screen"]
        self.rules = Rules(self)
        self.board = Board(self, **properties)
        self.InitialiseGameVariables()

    def InitialiseGameVariables(self):
        self.turn = "w"
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.game_over = False

    def TileManager(self, index):
        piece = self.board.piece_map[index]

        # User has already selected a tile
        if self.board.selected_tile != None:
            # User clicks on a piece and piece is their piece
            if piece and piece.properties["colour"] == self.turn:
                self.board.ResetSelectedTile()
                self.board.SelectTile(index)
                self.board.HighlightPotentialMoves(piece.GetSimulatedMoves())
            # User clicks on the board -> could be the opponents piece
            else:
                current_piece = self.board.piece_map[self.board.selected_tile]
                potential_moves = []
                if current_piece != 0:
                    potential_moves = current_piece.GetSimulatedMoves()

                if index in potential_moves:
                    self.MakeMove(current_piece, index)
                else:
                    self.board.ResetSelectedTile()

        # User has not already selected a tile
        else:
            # User clicks on a piece and the piece is the user's
            if piece and piece.properties["colour"] == self.turn:
                self.board.SelectTile(index)
                self.board.HighlightPotentialMoves(piece.GetSimulatedMoves())

    def MakeMove(self, piece, index):
        # Checking for special moves
        self.rules.CastleCheck(piece, index)
        self.rules.EnPassantCheck(piece, index)
        self.rules.UpdateEnPassantTarget(piece, index)

        captured_piece = self.board.MovePiece(piece, index)
        piece.moved = True
        Tile.ResetAllTiles()
        self.board.UpdatePieceImage(piece)

        # Removing captured piece
        if captured_piece != 0:
            self.board.RemovePiece(captured_piece)

        self.rules.PawnPromotionCheck(piece, index)

        # Updating turn change
        self.ChangeTurn()
        self.rules.CheckForChecks()

    def SimulateMove(self, piece, index):
        self.ChangeTurn()
        previous_piece = self.board.MovePiece(piece, index)
        if previous_piece:
            self.board.pieces[previous_piece.properties["colour"]].remove(previous_piece)
            return previous_piece
    
    def UndoSimulationMove(self, first_piece, first_index, second_piece=None, second_index=None):
        self.ChangeTurn()
        self.board.MovePiece(first_piece, first_index)
        if second_piece != None and second_piece != 0:
            self.board.piece_map[second_index] = second_piece
            self.board.pieces[second_piece.properties["colour"]].append(second_piece)

    def ChangeTurn(self):
        if self.turn == "w":
            self.turn = "b"
        else:
            self.turn = "w"

class TutorialGame(Game):

    def __init__(self, **properties):
        super().__init__(**properties)
        self.board = TutorialBoard(self, **properties)
        self.rules = TutorialRules(self)
        self.active = True
        self.tutorial_stage = 0
        self.return_function = properties.get("function", None)

    def TileManager(self, index):
        if self.active:
            super().TileManager(index)

    def UpdateBoard(self, fen):
        # Removing old pieces
        for _piece in self.board.pieces["w"] + self.board.pieces["b"]:
            self.board.piece_map[_piece.properties["index"]] = 0
            self.board.RemovePiece(_piece)
        # Removing highlighted tiles
        Tile.ResetAllTiles()

        # Setting new pieces
        self.board.pieces = {"w" : [], "b" : []}
        self.board.properties["fen"] = fen
        self.board.LoadPosition()
        self.board.UpdateNewPieceImage()

    def MakeMove(self, piece, index):
        if self.tutorial_stage == 3:
            # Ensuring the user captures and doesn't move forward
            if index == 20:
                return
        elif self.tutorial_stage == 10:
            # Ensuring the user doesn't capture the king
            if index == 0:
                return
            
        # Piece moving dictionary for each stage of the scenario tutorial
        for tut_stage, piece_index in {3:19, 4:14, 5:19, 6:11, 7:49, 8:54}.items():
            if self.tutorial_stage == tut_stage and index == piece_index:
                super().MakeMove(piece, index)
                self.return_function()
                return
            
        # Castling scenarios
        for tut_stage, piece_index in {11:62, 12:58, 13:19}.items():
            if self.tutorial_stage == tut_stage:
                if index == piece_index:
                    super().MakeMove(piece, index)
                    self.return_function()
                return

        super().MakeMove(piece, index)

        pieces_moved = 0
        for _piece in self.board.pieces["w"]:
            if _piece.moved:
                pieces_moved += 1

        # (Checking bishop, knight and rook have all been moved) and (Checking both king and queen have been moved) and (Finishing the tutorial)
        if (self.tutorial_stage == 1 and pieces_moved == 3) or (self.tutorial_stage == 2 and pieces_moved == 2) or self.tutorial_stage == 14:
            self.return_function()
            return

        # Checking if the black king is in check for the king checks scenario
        if self.tutorial_stage == 9 and self.rules.IsInCheck("b"):
            Tile.tile_instances[4].CheckTile()
            self.return_function()
            return

        # Checking if the black king has been checkmated
        if self.tutorial_stage == 10:
            if self.rules.IsInCheck("b"):
                Tile.tile_instances[0].CheckTile()
            if self.rules.IsCheckmate("b"):
                self.return_function()
                return

    def ChangeTurn(self):
        return

    def ActivateBoard(self):
        self.active = True

    def DeactivateBoard(self):
        self.active = False

class PuzzleGame(Game):

    def __init__(self, **properties):
        super().__init__(**properties)
        self.board = PuzzleBoard(self, **properties)
        self.rules = PuzzleRules(self)
        self.turn_function = properties["turn_function"]
        self.return_function = properties["return_function"]
        self.failed_function = properties["failed_function"]
        self.puzzle_stage = 0
        self.active = True

    def UpdateBoard(self, fen):
        # Removing old pieces
        for _piece in self.board.pieces["w"] + self.board.pieces["b"]:
            self.board.piece_map[_piece.properties["index"]] = 0
            self.board.RemovePiece(_piece)
        # Removing highlighted tiles
        Tile.ResetAllTiles()

        # Setting new pieces
        self.board.pieces = {"w" : [], "b" : []}
        self.board.properties["fen"] = fen
        self.board.LoadPosition()
        self.board.UpdateNewPieceImage()

    def TileManager(self, index):
        if self.puzzle_stage % 2 == 0 or not self.active:
            return
        super().TileManager(index)

    def MakeMove(self, piece, index):
        origin_index = piece.properties["index"]
        super().MakeMove(piece, index)

        # Highlighting tiles based on move
        if self.puzzle_stage % 2 == 1:
            start, end = self.screen.moves[self.puzzle_stage][0:2], self.screen.moves[self.puzzle_stage][2:4]
            start, end = self.board.AlgebraicToIndex(start), self.board.AlgebraicToIndex(end)
            
            # They didn't make the correct move
            if origin_index != start or index != end:
                self.board.HighlightRedTile(origin_index)
                self.board.HighlightRedTile(index, 1)
                self.failed_function()
                return
            self.board.HighlightGreenTile(origin_index)
            self.board.HighlightGreenTile(index, 1)
        else:
            self.board.HighlightMovedTile(origin_index)
            self.board.HighlightMovedTile(index, 1)
        self.return_function()

    def MakeFirstMove(self, move):
        self.screen.DrawScreen()
        pygame.display.flip()
        pygame.time.wait(500)
        start, end = move[0:2], move[2:4]
        start, end = self.board.AlgebraicToIndex(start), self.board.AlgebraicToIndex(end)
        piece_to_move = self.board.piece_map[start]
        self.MakeMove(piece_to_move, end)

    def ChangeTurn(self):
        super().ChangeTurn()
        self.turn_function()

    def ActivateBoard(self):
        self.active = True

    def DeactivateBoard(self):
        self.active = False

class AIGame(Game):

    def __init__(self, **properties):
        super().__init__(**properties)
        self.board = AIBoard(self, **properties)
        self.rules = AIRules(self)
        self.checkmate_function = properties["checkmate_function"]
        self.turn_function = properties["turn_function"]
        self.eval_function = properties["eval_function"]
        self.winner = None
        self.active = True
        self.difficulty = None

    def TileManager(self, index):
        if not self.active:
            return
        if not self.game_over:
            super().TileManager(index)

    def MakeMove(self, piece, index):
        origin_index = piece.properties["index"]
        super().MakeMove(piece, index)
        self.board.HighlightMovedTile(origin_index)
        self.board.HighlightMovedTile(index, 1)

        self.screen.DrawScreen()
        pygame.display.flip()

        if self.turn == "b":
            self.AIMove(self.difficulty + 1, "b")

        if self.rules.IsCheckmate(self.turn) and not self.game_over:
            self.FinishGame()
        
        # Updating the evaluation bar
        self.eval_function(self.board.EvaluateBoard())

    def AIMove(self, depth, colour):
        result = self.MinMax(depth, colour)

        if result[0] == None or self.rules.IsCheckmate("b"):
            if not self.game_over:
                self.FinishGame()
        else:
            piece, move, score = result
            self.MakeMove(piece, move)
    
    def QuiescenceSearch(self, colour, alpha, beta):
        maximising = True if colour == "w" else False
        evaluation = self.board.EvaluateBoard()
        best_score = evaluation
        
        if maximising:
            if evaluation >= beta:
                return [None, None, beta]
            alpha = max(alpha, evaluation)
        else: # Minimizing
            if evaluation <= alpha:
                return [None, None, alpha]
            beta = min(beta, evaluation)

        noisy_moves = self.board.GetNoisyMoves(colour) 
        
        for move_list in noisy_moves:
            piece, move = move_list[0], move_list[1]
            origin_index = piece.properties["index"]
            
            captured_piece = self.SimulateMove(piece, move)
            result = self.QuiescenceSearch("b" if maximising else "w", alpha, beta)
            score = result[2]
            self.UndoSimulationMove(piece, origin_index, captured_piece, move)

            if maximising:
                if score > best_score:
                    best_score = score
                alpha = max(alpha, best_score)
            else:
                if score < best_score:
                    best_score = score
                beta = min(beta, best_score)

            if beta <= alpha:
                break

        return [None, None, best_score]

    def MinMax(self, depth, colour, alpha=float("-inf"), beta=float("inf")):
        result = self.IsGameOver()
        if result != None:
            return {
                "w": [None, None, 9999999999],
                "b": [None, None, -9999999999],
                "draw": [None, None, 0]
            }[result]
            
        if depth == 0:
            # If Hard AI selected
            if self.difficulty == 2:
                return self.QuiescenceSearch(colour, alpha, beta)
            else:
                return [None, None, self.board.EvaluateBoard()]
        
        maximising = True if colour == "w" else False
        best_score = float("-inf") if maximising else float("inf")
        best_piece, best_move = None, None
        
        all_moves = self.board.GetAllSortedMoves(colour)

        if not all_moves:
            return [None, None, self.board.EvaluateBoard()]

        for move_list in all_moves:
            _piece, move = move_list[0], move_list[1]
            origin_index = _piece.properties["index"]
            captured_piece = self.SimulateMove(_piece, move)

            # Recursively calling the function
            result = self.MinMax(depth - 1, "b" if maximising else "w", alpha, beta)
            score = result[2]
            
            self.UndoSimulationMove(_piece, origin_index, captured_piece, move)

            if maximising:
                if score > best_score:
                    best_score, best_piece, best_move = score, _piece, move
                alpha = max(alpha, best_score)
            else:
                if score < best_score:
                    best_score, best_piece, best_move = score, _piece, move
                beta = min(beta, best_score)

            if beta <= alpha:
                break

        return [best_piece, best_move, best_score]

    def ChangeTurn(self):
        super().ChangeTurn()
        self.turn_function()
       
    def IsGameOver(self):
        if self.rules.IsCheckmate("w"):
            return "b" # Black wins
        if self.rules.IsCheckmate("b"):
            return "w" # White wins
        # if self.stalemate job for later
        return None
    
    def FinishGame(self):
        self.winner = "w" if self.turn == "b" else "b"
        self.game_over = True
        self.checkmate_function(self.winner)

    def ActivateBoard(self):
        self.active = True

    def DeactivateBoard(self):
        self.active = False