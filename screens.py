from keyvariables import *
from ui import *
from accountmanager import *
from game import *

class ScreenManager():
    instance = None
    def __init__(self):
        self.screens = {
            "main_menu": MainMenu(),
            "start_screen": StartScreen(),
            "signin_screen": SignIn(),
            "signup_screen": SignUpScreen(),
            "tutorial_screen": TutorialScreen(),
            "puzzle_screen": PuzzleScreen(),
            "account_screen": AccountScreen(),
            "ai_screen": AIScreen()
        }
        self.active_screen = self.screens["start_screen"]
        ScreenManager.instance = self

    def SwitchScreen(self, new_screen):
        self.active_screen = self.screens[new_screen]
        self.active_screen.ResetTextBox()
        self.active_screen.OnSwitch()

class BaseScreen():
    def __init__(self):
        self.ui_elements = []
        self.active_element = None
        self.click_used = False

    def InitiateElements(self, elements):
        self.ui_elements = elements

    def DrawScreen(self):
        for _ui in self.ui_elements:
            _ui.Draw()

    def EventHandler(self, event, mouse_position, mouse_button):
        # Recieves events from the main pygame file
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.ClickElements(mouse_position)
        elif event.type == pygame.KEYDOWN:
            if self.active_element:
                self.ActiveElementHandler(event)
                
    def ActiveElementHandler(self, event):
        # Updates active text box
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
            self.active_element = None
        else:
            self.active_element.UpdateText(event)

    def ClickElements(self, mouse_position):
        # Deactivating text boxes
        self.active_element = None

        for _ui in reversed(self.ui_elements):
            if isinstance(_ui, Button) and not self.click_used:
                # Checking all active buttins for a click
                if _ui.OnClick(mouse_position):
                    self.click_used = True

            if isinstance(_ui, TextBox):
                if _ui.OnClick(mouse_position):
                    self.active_element = _ui
                    # Removing previous username and password values
                    _ui.SetPlaceholder()
                    # Clearing placeholder text
                    _ui.text_label.properties["text"] = ""
        self.click_used = False

    def ResetTextBox(self):
        for _ui in self.ui_elements:
            if isinstance(_ui, TextBox):
                _ui.SetPlaceholder()

    def Get(self, id):
        for _ui in self.ui_elements:
            if _ui.properties["id"] == id:
                return _ui
            
    def OnSwitch(self):
        pass

class MainMenu(BaseScreen):

    def __init__(self):
        super().__init__()

class StartScreen(BaseScreen):

    def __init__(self):
        super().__init__()

class SignIn(BaseScreen):

    def __init__(self):
        super().__init__()

    def OnSwitch(self):
        self.ChangeMessageLabel("")

    def InfoValidation(self):
        username = self.Get("userBox").username
        password = self.Get("passBox").password

        login_result = VerifyAccount(username, password)
        if login_result:
            # Login failed
            self.ChangeMessageLabel(login_result)
        else:
            # Successful login
            ScreenManager.instance.SwitchScreen("main_menu")
        
    def ChangeMessageLabel(self, text):
        self.Get("messageLabel").properties["text"] = text

class SignUpScreen(BaseScreen):

    def __init__(self):
        super().__init__()

    def OnSwitch(self):
        self.ChangeMessageLabel("")

    def InfoValidation(self):
        username = self.Get("userBox").username
        password = self.Get("passBox").password
        verifypass = self.Get("verifypassBox").password

        result = self.InvalidInfo(username, password, verifypass)

        # Changes message label based on the outcome of the account creation
        if result:
            self.ChangeMessageLabel(result)
        else:
            if CreateAccount(username, password):
                self.ChangeMessageLabel("Account successfully created")
            else:
                self.ChangeMessageLabel("Username already exists")

    def InvalidInfo(self, username, password, verifypass):
        # Validating user info
        if len(username) < 3:
            return "Username must be atleast 3 characters"
        if password != verifypass:
            return "Passwords do not match"
        if len(password) < 3:
            return "Password must be atleast 3 characters"
        return
    
    def ChangeMessageLabel(self, text):
        self.Get("messageLabel").properties["text"] = text

class TutorialScreen(BaseScreen):

    def __init__(self):
        super().__init__()

        self.sub_screen_elements = []
        self.active_sub_screen = None
        self.screen_stage = 0
        self.tutorial_stages = [0, 1, 2, 8, 9, 10, 12, 13, 14]
        self.corresponding_stage = {1:0, 3:1, 7:2, 10:3, 17:9, 19:10, 21:11, 24:13, 26:14}

    def OnSwitch(self): 
        # Creating an instance of a board
        self.game = TutorialGame(screen=self, size=584, x=208, y=8, fen="", function=self.TutorialStageChanged)

        for _element in self.game.board.GetElements():
            self.ui_elements.append(_element)

        # Block Completed tutorial sections if logged in
        if ActiveAccount.current_account != None:
            self.BlockCompletedStages()

        # Never played the tutorial or finished tutorial
        section_index = self.GetFirstTutorial()
        if section_index == None:
            self.OpenMenu(0)
        # Has played the tutorial -> Open on incomplete section
        else:
            current_stage = list(self.corresponding_stage.keys())[int(section_index)]
            self.OpenMenu(current_stage)

    def TutorialStageChanged(self):
        # Updating tutorial completions to the user_tutorial data table
        if self.game.tutorial_stage in self.tutorial_stages and ActiveAccount.current_account != None:
            self.UpdateAccountInfo()
            self.BlockCompletedStages()

        self.game.tutorial_stage += 1
        self.screen_stage += 1
        self.OpenMenu(self.screen_stage)
        
    def PlayMenu(self, fen):
        self.CloseMenu()
        self.game.UpdateBoard(fen)

        for _element in self.game.board.GetElements():
            if not _element in self.ui_elements:
                self.ui_elements.append(_element)

    def OpenMenu(self, menu_number):
        self.screen_stage = menu_number
        self.CloseMenu()
        self.game.DeactivateBoard()

        if menu_number in self.corresponding_stage:
            self.game.tutorial_stage = self.corresponding_stage[menu_number]

        self.active_sub_screen = self.sub_screen_elements[menu_number]
        for _element in self.active_sub_screen:
            self.ui_elements.append(_element)

    def CloseMenu(self):
        self.game.ActivateBoard()
        if self.active_sub_screen == None:
            return
        for _element in self.active_sub_screen:
            if _element in self.ui_elements:
                self.ui_elements.remove(_element)
        self.active_sub_screen = None

    def ChangeMenu(self, amount=1):
        self.CloseMenu()
        self.screen_stage += amount
        self.OpenMenu(self.screen_stage)

    def UpdateAccountInfo(self):
        tutorial_index = self.tutorial_stages.index(self.game.tutorial_stage)
        updated_progress = ActiveAccount.GetTutorialProgress()
        updated_progress[tutorial_index] = True
        ActiveAccount.UpdateTutorialProgress(updated_progress)

    def BlockCompletedStages(self):
        self.ClearBlockingFrames()
        
        for index, value in ActiveAccount.GetTutorialProgress().items():
            if value:
                self.ui_elements.append(
                    Frame(
                        x=11, y=25+(int(index)*33), width=186, height=3, bg_colour="#FA6F4F", id="blocking"
                    )
                )

    def ClearBlockingFrames(self):
        for _element in self.ui_elements:
            if _element.properties["id"] == "blocking":
                self.ui_elements.remove(_element)

    def GetFirstTutorial(self):
        for index, value in ActiveAccount.GetTutorialProgress().items():
            if not value:
                return index
        return None

class PuzzleScreen(BaseScreen):

    def __init__(self):
        super().__init__()
        self.sub_screen_elements = []
        self.current_puzzle = None
        self.active_screen = None
        self.moves = []

    def OnSwitch(self):
        # Creating an instance of a board
        self.game = PuzzleGame(
            screen=self,
            turn_function=self.ChangeTurnLabel,
            return_function=self.ReturnFunction,
            failed_function=self.FailedPuzzle,
            size=584, x=8, y=8,
            fen=""
        )
        for _element in self.game.board.GetElements():
            self.ui_elements.append(_element)

        self.LoadRandomPuzzle()
        
    def LoadRandomPuzzle(self):
        with open('chess_puzzles.json', 'r') as file:
            puzzle_list = json.load(file)

        filtered_puzzles = [puzzle for puzzle in puzzle_list if abs(puzzle["rating"] - ActiveAccount.GetPuzzleRating()) <= 100]

        if not filtered_puzzles:
            self.current_puzzle = random.choice(filtered_puzzles)
        else:
            self.current_puzzle = random.choice(filtered_puzzles)

        self.game.UpdateBoard(self.current_puzzle["fen"])
        self.moves = self.current_puzzle["moves"]

        self.SetInfoLabels()
        self.ChangeTurnLabel()
        self.game.MakeFirstMove(self.moves[0])

    def NextPuzzle(self):
        self.CloseMenu()
        self.game.puzzle_stage = 0
        self.LoadRandomPuzzle()
    
    def CompletedPuzzle(self):
        self.OpenMenu(0)
        ActiveAccount.UpdatePuzzlesComplete()
        ActiveAccount.UpdatePuzzleRating(ActiveAccount.GetPuzzleRating() + 10)

    def FailedPuzzle(self):
        self.OpenMenu(1)
        ActiveAccount.UpdatePuzzleRating(ActiveAccount.GetPuzzleRating() - 12)

    def ReturnFunction(self):
        self.game.puzzle_stage += 1

        if self.game.puzzle_stage < len(self.moves) and self.game.puzzle_stage % 2 == 0:
            self.game.MakeFirstMove(self.moves[self.game.puzzle_stage])
        elif self.game.puzzle_stage >= len(self.moves):
            self.CompletedPuzzle()

    def OpenMenu(self, index):
        self.game.DeactivateBoard()
        self.active_screen = index
        for _element in self.sub_screen_elements[index]:
            self.ui_elements.append(_element)

    def CloseMenu(self):
        self.game.ActivateBoard()
        for _element in self.sub_screen_elements[self.active_screen]:
            if _element in self.ui_elements:
                self.ui_elements.remove(_element)

    def SetInfoLabels(self):
        self.Get("difficultyLabel").properties["text"] = "difficulty: " + self.current_puzzle["difficulty"]
        self.Get("ratingLabel").properties["text"] = "rating: " + str(self.current_puzzle["rating"])
        self.Get("userRatingLabel").properties["text"] = "your rating: " + str(ActiveAccount.GetPuzzleRating())

    def ChangeTurnLabel(self):
        label_text = "WHITES TURN" if self.game.turn == "w" else "BLACKS TURN"
        self.Get("turnLabel").properties["text"] = label_text

class AIScreen(BaseScreen):

    def __init__(self):
        super().__init__()
        self.sub_screen_elements = []
        self.active_screen = None

    def OnSwitch(self):
        self.game = AIGame(
            screen=self,
            size=520, x=72, y=40,
            turn_function=self.ChangeTurnLabel,
            eval_function=self.UpdateEvalBar,
            checkmate_function=self.OpenCheckmateScreen, 
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        )

        for _element in self.game.board.GetElements():
            self.ui_elements.append(_element)

        self.UpdateUserName()
        self.OpenMenu(0)

    def UpdateEvalBar(self, evaluation):
        start_bar_height = 260
        max_evaluation = 3000
        
        if evaluation > max_evaluation:
            evaluation = max_evaluation - 100
        if evaluation < -max_evaluation:
            evaluation = -max_evaluation + 100

        if abs(max_evaluation) > 999999:
            if evaluation > 0:
                evaluation = max_evaluation
            else:
                evaluation = -max_evaluation
            
        bar_height = int((evaluation/max_evaluation)*260)
        self.Get("evaluationBar").UpdateProperty(height = start_bar_height - bar_height)

    def UpdateUserName(self):
        if ActiveAccount.current_account != None:
            self.Get("userName").properties["text"] = ActiveAccount.current_account.upper()

    def SelectAIDifficulty(self, difficulty):
        self.game.difficulty = difficulty

        # Updating AI display icon and label
        difficulty_text = {0:"EASY", 1:"MEDIUM", 2:"HARD"}
        difficulty_colour = {0:"#6EAE6E", 1:"#6E97B9", 2:"#B04040"}

        self.Get("aiName").properties["text"] = f"{difficulty_text[difficulty]} AI"
        self.Get("aiIcon").properties["bg_colour"] = difficulty_colour[difficulty]

        self.CloseMenu()

    def OpenCheckmateScreen(self, winner="w"):
        winner_colour = "WHITE" if winner == "w" else "BLACK"
        self.OpenMenu(1)
        for _element in self.ui_elements:
            if _element.properties["id"] == "winner":
                _element.properties["text"] = winner_colour + " WINS"
        if winner == "w":
            self.UpdateAccountInfo()

    def OpenMenu(self, index):
        self.game.DeactivateBoard()
        self.active_screen = index
        for _element in self.sub_screen_elements[index]:
            self.ui_elements.append(_element)

    def CloseMenu(self):
        self.game.ActivateBoard()
        for _element in self.sub_screen_elements[self.active_screen]:
            if _element in self.ui_elements:
                self.ui_elements.remove(_element)

    def ChangeTurnLabel(self):
        label_text = "WHITES TURN" if self.game.turn == "w" else "BLACKS TURN"
        self.Get("turnLabel").properties["text"] = label_text

    def UpdateAccountInfo(self):
        ai_progress = ActiveAccount.GetAIProgress()
        ai_progress[self.game.difficulty] = True
        ActiveAccount.UpdateAIProgress(ai_progress)

class AccountScreen(BaseScreen):

    def __init__(self):
        super().__init__()

    def OnSwitch(self):
        self.Get("usernameLabel").properties["text"] = ActiveAccount.current_account
        self.Get("tutorialInfo").properties["text"] = f"TUTORIAL SECTIONS: {self.CountTutorialsComplete()}/9 COMPLETE"
        self.Get("ratingLabel").properties["text"] = f"PUZZLE RATING: {ActiveAccount.GetPuzzleRating()}"
        self.Get("puzzlesSolvedLabel").properties["text"] = f"PUZZLES SOLVED: {ActiveAccount.GetPuzzlesComplete()}"
        self.SetAILabels()

    def CountTutorialsComplete(self):
        progress_dict = ActiveAccount.GetTutorialProgress()
        tut_completed = 0

        for key, value in progress_dict.items():
            if value:
                tut_completed += 1

        return tut_completed

    def SetAILabels(self):
        label_ids = {0:"easyAI", 1:"mediumAI", 2:"hardAI"}
        level = {0:"EASY", 1:"MEDIUM", 2:"HARD"}
        ai_progress = ActiveAccount.GetAIProgress()

        for ai_level, value in ai_progress.items():
            if value:
                self.Get(label_ids[int(ai_level)]).properties["text"] = f"{level[int(ai_level)]} AI: BEATEN"