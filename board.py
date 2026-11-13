from keyvariables import *
from ui import *
from pieces import *
from piecetables import *

class Board:

    def __init__(self, game, **properties):
        default_properties = {"x":0, "y":0, "size":600}
        self.properties = {**default_properties, **properties}
        self.game = game
        self.rules = game.rules

        self.InitialiseBoardVariables()
        self.CreateBoard()
        self.LoadPosition()

    def InitialiseBoardVariables(self):
        self.ui_elements = []
        self.piece_map = [0 for i in range(64)]
        self.pieces = {"w": [], "b": []}
        self.selected_tile = None

    def MovePiece(self, piece, index):
        captured_piece = self.piece_map[index]

        self.piece_map[piece.properties["index"]] = 0
        self.piece_map[index] = piece
        piece.properties["index"] = index

        return captured_piece

    def LoadPosition(self):
        fen_string = self.properties["fen"]
        pointer_index = 0
        
        for char in fen_string:
            if char == " ":
                break
            elif char == "/":
                continue
            elif char.lower() in "prnbqk":
                self.CreatePiece(char, pointer_index)
            elif char.isdigit():
                pointer_index += int(char) - 1
            pointer_index += 1

        fen_parts = fen_string.split(" ") + [None] * 6
        fen_parts = fen_parts[:6]
        self.ParseFEN(fen_parts)
        
    def ParseFEN(self, fen_parts):
        self.game.turn = fen_parts[1] or "w"

        # Castling rights
        if fen_parts[2]:
            for colour, king in zip(["w", "b"], [self.GetKing("w"), self.GetKing("b")]):
                castling_rights = fen_parts[2][0:2] if colour == "w" else fen_parts[2][2:4]
                if king.GetKingSideRook() != None:
                    king.GetKingSideRook().moved = True if castling_rights[0:1] == "-" else False
                if king.GetQueenSideRook() != None:
                    king.GetQueenSideRook().moved = True if castling_rights[1:2] == "-" else False

        # Is there a possible en passant
        if fen_parts[3] and fen_parts[3] != "-":
            self.game.en_passant_target = self.AlgebraicToIndex(fen_parts[3])

    def CreatePiece(self, char, index):
        piece_class = {"P": Pawn, "R": Rook, "B": Bishop, "N": Knight, "Q": Queen, "K": King}
        piece_colour = "w" if char.isupper() else "b"
        new_piece = piece_class[char.upper()](
            size = self.properties["size"]//8,
            x = self.IndexToCoordinates(index)[0],
            y = self.IndexToCoordinates(index)[1],
            colour = piece_colour,
            board = self,
            index = index
        )
        self.piece_map[index] = new_piece
        self.pieces[piece_colour].append(new_piece)
        return new_piece

    def RemovePiece(self, piece):
        self.pieces[piece.properties["colour"]].remove(piece)
        piece.UpdateProperty(visible=False)

    def CreateBoard(self):
        # Creating 8 by 8 chess board
        for y in range(8):
            for x in range(8):
                self.ui_elements.append(self.CreateTile(x, y))

    def CreateTile(self, x, y):
        tile_size = self.properties["size"] // 8
        tile_id = x + (y * 8)
        tile = Tile(
            x = x * tile_size + self.properties["x"],
            y = y * tile_size + self.properties["y"],
            width = tile_size, height = tile_size,
            checkered = (x + y) % 2, id = tile_id
        )
        tile.properties["onclick"] = lambda id=tile_id: self.game.TileManager(id)
        return tile

    def UpdatePieceImage(self, piece):
        index = piece.properties["index"]
        x = self.IndexToCoordinates(index)[0]
        y = self.IndexToCoordinates(index)[1]
        piece.UpdateProperty(x=x, y=y)

    def IndexToCoordinates(self, index):
        tile_size = self.properties["size"] // 8
        x = (index % 8) * tile_size + self.properties["x"]
        y = (index // 8) * tile_size + self.properties["y"]
        return [x, y]

    def AlgebraicToIndex(self, algebraic):
        letter = algebraic[0:1]
        number = int(algebraic[1:2])
        index = "abcdefgh".index(letter) + (8-number) * 8
        return index

    def SelectTile(self, index):
        self.selected_tile = index
        self.GetElementById(index).SelectTile()

    def HighlightPotentialMoves(self, moves):
        for move in moves:
            self.GetElementById(move).HighlightTile()

    def ResetSelectedTile(self):
        if self.selected_tile == None:
            return
        self.selected_tile = None
        Tile.ResetAllTiles()

    def GetKing(self, colour):
        for _piece in self.pieces[colour]:
            if isinstance(_piece, King):
                return _piece

    def GetPieceAtIndex(self, index):
        for _piece in self.pieces["w"] + self.pieces["b"]:
            if index == _piece.properties["index"]:
                return _piece

    def GetElementById(self, id):
        for _element in self.ui_elements:
            if id == _element.properties["id"]:
                return _element

    def GetElements(self):
        piece_elements = []
        for _piece in self.pieces["w"] + self.pieces["b"]:
            piece_elements.append(_piece.GetImage())
        return self.ui_elements + piece_elements

class TutorialBoard(Board):

    def __init__(self, game, **properties):
        super().__init__(game, **properties)
    
    def UpdateNewPieceImage(self):
        for _piece in self.pieces["w"] + self.pieces["b"]:
            self.game.screen.ui_elements.append(_piece.GetImage())

class PuzzleBoard(Board):

    def __init__(self, game, **properties):
        super().__init__(game, **properties)

    def UpdateNewPieceImage(self):
        for _piece in self.pieces["w"] + self.pieces["b"]:
            self.game.screen.ui_elements.append(_piece.GetImage())

    def HighlightMovedTile(self, index, order=0):
        self.GetElementById(index).MovedTile(order)

    def HighlightGreenTile(self, index, order=0):
        self.GetElementById(index).GreenTile(order)

    def HighlightRedTile(self, index, order=0):
        self.GetElementById(index).RedTile(order)

class AIBoard(Board):
    
    def __init__(self, game, **properties):
        super().__init__(game, **properties)

    def EvaluateBoard(self):
        evaluation_score = 0
        
        # Adding material and positional value to the evaluation score
        evaluation_score += self.GetMaterialValue() + self.GetPositionValue()

        return evaluation_score

    def GetMaterialValue(self, absolute=False):
        material_score = 0

        # Evaluating the number of pieces and their values
        for _piece in self.pieces["w"]:
            material_score += material_value[_piece.piece_type]
        for _piece in self.pieces["b"]:
            if absolute:
                material_score += material_value[_piece.piece_type]
            else:
                material_score -= material_value[_piece.piece_type]
        return material_score
    
    def GetPositionValue(self):
        piece_tables = piece_table_dict
        position_score = 0

        # If it is end game then use a different king score table
        if self.IsEndGame():
            piece_tables.update({"k": king_end_game_table})

        # Adding the pieces position score to the total score and flipping the tables for black
        for _piece in self.pieces["w"]:
            table = piece_tables[_piece.piece_type]
            position_score += table[_piece.properties["index"]]
        for _piece in self.pieces["b"]:
            table = piece_tables[_piece.piece_type][::-1]
            position_score -= table[_piece.properties["index"]]

        return position_score

    def NoQueens(self):
        # Returns false if there are still queens left, true if not
        for _piece in self.pieces["w"] + self.pieces["b"]:
            if _piece.piece_type == "q":
                return False
        return True

    def IsEndGame(self):
        # Returns true if it is endgame, false if not
        if self.GetMaterialValue(True) <= 2600:
            return True
        return False

    def IndexToAlgebraic(self, index):
        index_file = index % 8
        index_rank = ((63 - index) // 8) + 1
        algebraic_file = "abcdefgh"[index_file:index_file+1]
        return algebraic_file + str(index_rank)

    def GetAllMoves(self, colour):
        moves = []

        for _piece in self.pieces[colour]:
            for move in _piece.GetSimulatedMoves():
                moves.append([_piece, move, 0])
        return moves

    def GetAllSortedMoves(self, colour):
        moves = []
        
        for _piece in self.pieces[colour]:
            origin_index = _piece.properties["index"]
            piece_colour = _piece.properties["colour"]
            for move in _piece.GetSimulatedMoves():
                captured_piece = self.piece_map[move]
                score = 0

                # Capture moves are deemed better
                if captured_piece:
                    piece_value = material_value[_piece.piece_type]
                    captured_piece_value = material_value[captured_piece.piece_type]
                    score += (captured_piece_value - piece_value) + 600

                # Check moves deemed better
                self.game.SimulateMove(_piece, move)
                if self.game.rules.IsInCheck("b" if piece_colour == "w" else "w"):
                    score += 300
                self.game.UndoSimulationMove(_piece, origin_index, captured_piece, move)

                # Moves that place pieces towards center deemed better
                file = move % 8
                rank = move // 8
                if 2 <= file <= 5 and 2 <= rank <= 5:
                    score += 100

                moves.append([_piece, move, score])
        # Sorting the list in descending order of score
        moves.sort(key=lambda result: result[2], reverse=True)
        return moves

    def GetNoisyMoves(self, colour):
        noisy_moves = []

        for move_list in self.GetAllMoves(colour):
            piece, move = move_list[0], move_list[1]
            
            # Capture moves added to noisy list
            target_piece = self.piece_map[move]
            if target_piece != 0 and target_piece.properties["colour"] != colour:
                noisy_moves.append(move_list)
                continue

            # If a pawn is promoting add to noisy list
            if isinstance(piece, Pawn) and self.game.rules.IsPromotionMove(piece, move):
                noisy_moves.append(move_list)
                continue
                
            origin_index = piece.properties["index"]
            captured_piece = self.game.SimulateMove(piece, move)

            if self.game.rules.IsInCheck("b" if colour == "w" else "w"):
                noisy_moves.append(move_list)
            
            self.game.UndoSimulationMove(piece, origin_index, captured_piece, move)
            
        return noisy_moves

    def HighlightMovedTile(self, index, order=0):
        self.GetElementById(index).MovedTile(order)

class Tile(Button):

    tile_instances = []
    
    def __init__(self, **properties):
        super().__init__(**properties)

        # Every other tile rank plus file equals one creating a checkered pattern
        self.checkered = properties.get("checkered", 0)
        self.ResetTileColour()
        Tile.tile_instances.append(self)

    def SelectTile(self):
        self.UpdateProperty(bg_colour="#66AA66")
    
    def CheckTile(self):
        self.UpdateProperty(bg_colour="#6162BB")

    def MovedTile(self, order):
        if order == 0:
            self.UpdateProperty(bg_colour="#B79FCD")
        else:
            self.UpdateProperty(bg_colour="#A08BB4")

    def GreenTile(self, order):
        if order == 0:
            self.UpdateProperty(bg_colour="#9FCDA1")
        else:
            self.UpdateProperty(bg_colour="#92B48B")

    def RedTile(self, order):
        if order == 0:
            self.UpdateProperty(bg_colour="#D17979")
        else:
            self.UpdateProperty(bg_colour="#B95E5E")

    def HighlightTile(self):
        if self.checkered == 0:
            self.UpdateProperty(bg_colour="#A8D1FF")
        else:
            self.UpdateProperty(bg_colour="#4F9FFA")

    def ResetTileColour(self):
        if self.checkered == 0:
            self.UpdateProperty(bg_colour="#FFD2A8")
        else:
            self.UpdateProperty(bg_colour="#FA6F4F")

    @staticmethod
    def ResetAllTiles():
        for _tile in Tile.tile_instances:
            _tile.ResetTileColour()