from screens import *
from keyvariables import *
from ui import *
from accountmanager import *
from board import *

screen_manager = ScreenManager()

# Logout function
def Logout():
    screen_manager.SwitchScreen("start_screen")
    ActiveAccount.current_account = None

# Defining the elements placed on each screen
def MainMenuElements():
    return [
        Frame( # Background
            width=window_width, height=window_height,
            bg_colour="#1F2421"
        ), Image( # Title
            x=window_width//2-255, y=-100, width=500, height=500,
            img_source="assets/title.png"
        ), Button( # Tutorial
            x=window_width//2-150, y=180, width=300, height=25,
            text="tutorial", text_size=24, font="gadugi", bg_colour="#216869",
            onclick=lambda : screen_manager.SwitchScreen("tutorial_screen")
        ), Frame(
            x=window_width//2-148, y=182, width=4, height=21,
            bg_colour="#49A078"
        ), Button( # Puzzle
            x=window_width//2-150, y=215, width=300, height=25,
            text="puzzle", text_size=24, font="gadugi", bg_colour="#216869",
            onclick=lambda : screen_manager.SwitchScreen("puzzle_screen")
        ), Frame(
            x=window_width//2-148, y=217, width=4, height=21,
            bg_colour="#49A078"
        ), Button( # AI
            x=window_width//2-150, y=250, width=300, height=25,
            text="ai", text_size=24, font="gadugi", bg_colour="#216869",
            onclick=lambda : screen_manager.SwitchScreen("ai_screen")
        ), Frame(
            x=window_width//2-148, y=252, width=4, height=21,
            bg_colour="#49A078"
        ), Button( # Account
            x=window_width//2-150, y=285, width=300, height=25,
            text="account", text_size=24, font="gadugi", bg_colour="#216869",
            onclick=lambda : screen_manager.SwitchScreen("account_screen")
        ), Frame(
            x=window_width//2-148, y=287, width=4, height=21,
            bg_colour="#49A078"
        ), Button( # Quit
            x=window_width//2-150, y=320, width=300, height=25,
            text="quit", text_size=24, font="gadugi", bg_colour="#216869",
            onclick=lambda : pygame.quit()
        ), Frame(
            x=window_width//2-148, y=322, width=4, height=21,
            bg_colour="#49A078",
        )
    ]

def StartScreenElements():
    return [
        Frame(
            width=window_width, height=window_height,
            bg_colour="#1F2421"
        ), Button( # Sign in
            x=window_width//2-150, y=210, width=300, height=35,
            bg_colour="#216869", text_colour="#DCE1DE",
            text="SIGN IN",
            onclick=lambda : screen_manager.SwitchScreen("signin_screen")
        ), Button( # Sign up
            x=window_width//2-150, y=255, width=300, height=35,
            bg_colour="#216869", text_colour="#DCE1DE",
            text="SIGN UP",
            onclick=lambda : screen_manager.SwitchScreen("signup_screen")
        ), Frame(
            x=window_width//2-150, y=243, width=300, height=2,
            bg_colour="#49A078"
        ), Frame(
            x=window_width//2-150, y=288, width=300, height=2,
            bg_colour="#49A078"
        )
    ]

def SignInScreenElements():
    return [
        Frame(
            width=window_width, height=window_height,
            bg_colour="#1F2421"
        ), Button(
            x=15, y=560, width=100, height=30,
            bg_colour="#2F3732", text="BACK", text_colour="#DCE1DE",
            onclick=lambda: screen_manager.SwitchScreen("start_screen")
        ), UsernameBox(
            x=window_width//2-150, y=225, width=300, height=40,
            bg_colour="#216869",
            text_size=30, text_colour="#DCE1DE",
            placeholder="username",
            id="userBox"
        ), PasswordBox(
            x=window_width//2-150, y=270, width=300, height=40,
            bg_colour="#216869",
            text_size=30, text_colour="#DCE1DE",
            placeholder="password",
            id="passBox"
        ), Button (
            x=window_width//2-150, y=315, width=300, height=35,
            bg_colour="#3A7E5E",
            text_size=28, text_colour="#DCE1DE",
            text="SIGN IN",
            onclick = lambda : screen_manager.screens["signin_screen"].InfoValidation()
        ), TextLabel(
            x=200, y=145, width=400, height=100,
            text_colour="#DCE1DE",
            text_size=35, font="aptosblack",
            id="messageLabel"
        )
    ]

def SignUpScreenElements():
    return [
        Frame(
            width=window_width, height=window_height,
            bg_colour="#1F2421"
        ), Button(
            x=15, y=560, width=100, height=30,
            bg_colour="#2F3732", text="BACK", text_colour="#DCE1DE",
            onclick=lambda: screen_manager.SwitchScreen("start_screen")
        ), UsernameBox(
            x=window_width//2-150, y=180, width=300, height=40,
            bg_colour="#216869", text_colour="#DCE1DE",
            text_size=30, placeholder="username",
            id="userBox"
        ), PasswordBox(
            x=window_width//2-150, y=225, width=300, height=40,
            bg_colour="#216869", text_colour="#DCE1DE",
            text_size=30, placeholder="password",
            id="passBox"
        ), PasswordBox(
            x=window_width//2-150, y=270, width=300, height=40,
            bg_colour="#216869", text_colour="#DCE1DE",
            text_size=30, placeholder="verify password",
            id="verifypassBox"
        ), Button (
            x=window_width//2-150, y=315, width=300, height=35,
            bg_colour="#3A7E5E",
            text_size=28, text_colour="#DCE1DE",
            text="CREATE ACCOUNT",
            onclick = lambda : screen_manager.screens["signup_screen"].InfoValidation()
        ), TextLabel(
            x=200, y=105, width=400, height=100,
            text_colour="#DCE1DE",
            text_size=35, font="aptosblack",
            id="messageLabel"
        )
    ]

def PuzzleScreenElements():
    return [
        Frame(
            width=window_width, height=window_height,
            bg_colour="#B99675"
        ), Frame( # Side Frame
            x=600, y=8, width=192, height=584, bg_colour="#77614C"
        ), Frame( # Top Bar
            x=600, y=8, width=192, height=38, bg_colour="#584838"
        ), TextLabel( # Turn Text
            x=600, y=8, width=192, height=40, font="twcen", text_colour="#FFD2A8", 
            text_size=24, text="WHITES TURN", id="turnLabel"
        ), TextLabel( # Puzzle difficulty Text
            x=605, y=52, font="twcen", text_colour="#FFD2A8", 
            text_size=20, text="difficulty: placeholder", id="difficultyLabel"
        ), TextLabel( # Puzzle rating Text
            x=605, y=74, font="twcen", text_colour="#FFD2A8", 
            text_size=20, text="rating: 0000", id="ratingLabel"
        ), TextLabel( # User rating Text
            x=605, y=96, font="twcen", text_colour="#FFD2A8", 
            text_size=20, text="your rating: 0000", id="userRatingLabel"
        ), Button( # Exit to main menu
            x=603, y=559, width=186, height=30, bg_colour="#665341",
            text_size=24, font="twcen", text_colour="#FFD2A8", text="exit to main menu",
            onclick=lambda : screen_manager.SwitchScreen("main_menu")
        )
    ]

def AIScreenElements():
    return [
        Frame(
            width=window_width, height=window_height,
            bg_colour="#B99675"
        ), Frame( # Side Frame
            x=600, y=8, width=192, height=584, bg_colour="#77614C"
        ), Frame( # Top Bar
            x=600, y=8, width=192, height=38, bg_colour="#584838"
        ), TextLabel( # Turn Text
            x=600, y=8, width=192, height=40, font="twcen", text_colour="#FFD2A8", 
            text_size=24, text="WHITES TURN", id="turnLabel"
        ), Button( # Exit to main menu
            x=603, y=559, width=186, height=30, bg_colour="#665341",
            text_size=24, font="twcen", text_colour="#FFD2A8", text="exit to main menu",
            onclick=lambda : screen_manager.active_screen.OpenMenu(2)
        ), Frame ( # AI Icon
            x=82, y=5, width=30, height=30, bg_colour="#77614C", id="aiIcon"
        ), TextLabel( # AI Name
            x=120, y=10, font="twcen", text_colour="#000000",
            text_size=18, text="AI", id="aiName"
        ), Frame ( # User Icon
            x=82, y=565, width=30, height=30, bg_colour="#77614C"
        ), Image ( # User Image
            x=82, y=565, width=30, height=30, img_source="assets/user.png"
        ), TextLabel( # User Name
            x=120, y=570, font="twcen", text_colour="#000000",
            text_size=18, text="USER", id="userName"
        ), Frame( # Evaluation bar background frame
            x=16, y=40, width=40, height=520, bg_colour="#DCE1DE"
        ), Frame( # Evaluation bar black frame
            x=16, y=40, width=40, height=260, bg_colour="#333333", id="evaluationBar"
        )
    ]

def AccountScreenElements():
    return [
        Frame(
            width=window_width, height=window_height,
            bg_colour="#1F2421"
        ), Frame(
            x=window_width//2-200, y=70, width=400, height=425,
            bg_colour="#216869"
        ), Frame(
            x=window_width//2-200, y=70, width=400, height=25,
            bg_colour="#49A078"
        ), TextLabel( # Username label
            x=window_width//2-200, y=72, width=400, height=25,
            text_size=26, font="bahnschrift",
            text="USERNAME", text_colour="#000000",
            id="usernameLabel"
        ), TextLabel( # Tutorial info
            x=window_width//2-180, y=115,
            text_size=22,
            text="TUTORIAL SECTIONS: 0/9 COMPLETE", text_colour="#DCE1DE", id="tutorialInfo"
        ), Frame(
            x=window_width//2-180, y=145, width=360, height=1,
            bg_colour="#FFFFFF"
        ), TextLabel( # Puzzle info
            x=window_width//2-180, y=165,
            text_size=22, text_colour="#DCE1DE",
            text="PUZZLE RATING: 1000", id="ratingLabel"
        ), TextLabel(
            x=window_width//2-180, y=185,
            text_size=22, text_colour="#DCE1DE",
            text="PUZZLES SOLVED: 0", id="puzzlesSolvedLabel"
        ), Frame(
            x=window_width//2-180, y=215, width=360, height=1,
            bg_colour="#FFFFFF"
        ), TextLabel( # AI info
            x=window_width//2-180, y=235,
            text_size=22,
            text="EASY AI: UNBEATEN", text_colour="#DCE1DE", id="easyAI"
        ), TextLabel(
            x=window_width//2-180, y=255,
            text_size=22,
            text="MEDIUM AI: UNBEATEN", text_colour="#DCE1DE", id="mediumAI"
        ), TextLabel(
            x=window_width//2-180, y=275,
            text_size=22,
            text="HARD AI: UNBEATEN", text_colour="#DCE1DE", id="hardAI"
        ), Frame(
            x=window_width//2-180, y=305, width=360, height=1,
            bg_colour="#FFFFFF"
        ), Button( # Logout Button
            x=window_width//2-195, y=465, width=390, height=25,
            text="logout", text_size=26, bg_colour="#1D5B5D",
            onclick=lambda : Logout()
        ), Button(
            x=15, y=560, width=100, height=30,
            bg_colour="#2F3732", text="BACK", text_colour="#DCE1DE",
            onclick=lambda: screen_manager.SwitchScreen("main_menu")
        )
    ]

def TutorialScreenElements():
    return [
        Frame(
            width=window_width, height=window_height,
            bg_colour="#B99675"
        ), Frame(
            x=8, y=8, width=192, height=584,
            bg_colour="#77614C"
        ), Button( # Pawn Button
            x=11, y=11, width=186, height=30,
            bg_colour="#574738",
            onclick=lambda : screen_manager.active_screen.OpenMenu(1)
        ), TextLabel( # Pawn Label
            x=14, y=12, font="twcen",
            text_colour="#FFD2A8", text_size=24,
            text="Pawn Movement"
        ), Button( # Bishop Knight and Rook Button
            x=11, y=44, width=186, height=30,
            bg_colour="#574738",
            onclick=lambda : screen_manager.active_screen.OpenMenu(3)
        ), TextLabel( # Bishop Knight and Rook Label
            x=14, y=45, font="twcen",
            text_colour="#FFD2A8", text_size=24,
            text="Bishop Knight Rook"
        ), Button( # King and Queen Button
            x=11, y=77, width=186, height=30,
            bg_colour="#574738",
            onclick=lambda : screen_manager.active_screen.OpenMenu(7)
        ), TextLabel( # King and Queen Label
            x=14, y=78, font="twcen",
            text_colour="#FFD2A8", text_size=24,
            text="King and Queen"
        ), Button( # Capturing Pieces Button
            x=11, y=110, width=186, height=30,
            bg_colour="#574738",
            onclick=lambda : screen_manager.active_screen.OpenMenu(10)
        ), TextLabel( # Capturing Pieces Label
            x=14, y=111, font="twcen",
            text_colour="#FFD2A8", text_size=24,
            text="Capturing Pieces"
        ), Button( # King Checks Button
            x=11, y=143, width=186, height=30,
            bg_colour="#574738",
            onclick=lambda : screen_manager.active_screen.OpenMenu(17)
        ), TextLabel( # King Checks Label
            x=14, y=143, font="twcen",
            text_colour="#FFD2A8", text_size=24,
            text="King Checks"
        ), Button( # Checkmates Button
            x=11, y=176, width=186, height=30,
            bg_colour="#574738",
            onclick=lambda : screen_manager.active_screen.OpenMenu(19)
        ), TextLabel( # Checkmates Label
            x=14, y=177, font="twcen",
            text_colour="#FFD2A8", text_size=24,
            text="Checkmates"
        ), Button( # Castling Button
            x=11, y=209, width=186, height=30,
            bg_colour="#574738",
            onclick=lambda : screen_manager.active_screen.OpenMenu(21)
        ), TextLabel( # Castling Label
            x=14, y=210, font="twcen",
            text_colour="#FFD2A8", text_size=24,
            text="Castling"
        ), Button( # En Passant Button
            x=11, y=242, width=186, height=30,
            bg_colour="#574738",
            onclick=lambda : screen_manager.active_screen.OpenMenu(24)
        ), TextLabel( # En Passant Label
            x=14, y=243, font="twcen",
            text_colour="#FFD2A8", text_size=24,
            text="En Passant"
        ), Button( # Playing Chess Button
            x=11, y=275, width=186, height=30,
            bg_colour="#574738",
            onclick=lambda : screen_manager.active_screen.OpenMenu(26)
        ), TextLabel( # Playing Chess Label
            x=14, y=276, font="twcen",
            text_colour="#FFD2A8", text_size=24,
            text="Playing Chess"
        ), Button( # Main Menu Button
            x=11, y=559, width=186, height=30,
            bg_colour="#574738", text_colour="#FFD2A8", text_size=24,
            text="main menu",onclick=lambda : screen_manager.SwitchScreen("main_menu")
        )
    ]

def StartTutorialElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=230,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="Tutorial", text_size=18
        ), MultiLineText( # Info
            x=window_width//2-245, y=130, text_colour="#DCE1DE", font="twcen",
            text_size=20, text="Welcome to the chess tutorial. On the left, you'll see a set of\nbuttons labeled with each part of the tutorial. When a\nsection is completed, its button will be crossed off. You can\nclick any button to skip directly to that part of the tutorial. On\nthe right is the chess baord, which will be used to make the\ntutorial interactive. During the tutorial you will play as the\nwhite pieces, while the black pieces will remain stationary.\nYou can make multiple moves in a row."
        ), Button(
            x=window_width//2-245, y=300, width=490, height=25, text_size=26,
            bg_colour="#2F3732", text="begin tutorial", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.OpenMenu(1)
        )
    ]

def PawnMovementElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=230,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="Pawn Movement", text_size=18
        ), Frame(
            x=window_width//2-240, y=130, width=80, height=80,
            bg_colour="#49A078"
        ), Image( # Piece image
            x=window_width//2-250, y=112, width=100, height=100,
            img_source="assets/wp.png"
        ), MultiLineText( # Info
            x=window_width//2-155, y=130, text_colour="#DCE1DE", font="twcen",
            text_size=20, text="Pawns have a piece value of 1. They can move\nforward only 1 square at a time unless it is their\nfirst go where they can move forward 2 squares.\nIf a pawn reaches the end it becomes a queen."
        ), TextLabel(
            x=window_width//2-250, y=260, width=500, height=20,
            text_size=20, font="twcen",
            text="Try moving the pawn to the end of the board."
        ), Button(
            x=window_width//2-245, y=300, width=490, height=25, text_size=26,
            bg_colour="#2F3732", text="close", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.PlayMenu("8/8/8/8/8/8/4P3/8")
        )
    ]

def FinishedPawnMovementElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=150,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="Pawn Movement", text_size=18
        ), TextLabel(
            x=window_width//2-250, y=160, width=500, height=20,
            text_size=20, font="twcen",
            text="Well done! You have successfully promoted the pawn."
        ), Button(
            x=window_width//2-245, y=220, width=490, height=25, text_size=26,
            bg_colour="#2F3732", text="next", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.ChangeMenu()
        )
    ]

def BishopInfoElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=180,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="Bishop Movement", text_size=18
        ), Frame(
            x=window_width//2-240, y=130, width=80, height=80,
            bg_colour="#49A078"
        ), Image( # Piece image
            x=window_width//2-245, y=125, width=90, height=90,
            img_source="assets/wb.png"
        ), MultiLineText( # Info
            x=window_width//2-155, y=130, text_colour="#DCE1DE", font="twcen",
            text_size=20, text="Bishops have a piece value of 3. They can move\nacross their diagonal lanes as far as you want."
        ), Button(
            x=window_width//2-245, y=250, width=490, height=25, text_size=26,
            bg_colour="#2F3732", text="next", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.ChangeMenu()
        )
    ]

def KnightInfoElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=180,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="Knight Movement", text_size=18
        ), Frame(
            x=window_width//2-240, y=130, width=80, height=80,
            bg_colour="#49A078"
        ), Image( # Piece image
            x=window_width//2-245, y=125, width=90, height=90,
            img_source="assets/wn.png"
        ), MultiLineText( # Info
            x=window_width//2-155, y=130, text_colour="#DCE1DE", font="twcen",
            text_size=20, text="Knights have a piece value of 3. They can move\nin L shapes in any direction. For example, they\ncan move 2 up and 1 across or they can move 2\nacross and 1 up."
        ), Button( # Previous button
            x=window_width//2-245, y=250, width=242, height=25, text_size=26,
            bg_colour="#2F3732", text="previous", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.ChangeMenu(-1)
        ), Button( # Next button
            x=window_width//2+3, y=250, width=242, height=25, text_size=26,
            bg_colour="#2F3732", text="next", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.ChangeMenu()
        )
    ]

def RookInfoElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=200,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="Rook Movement", text_size=18
        ), Frame(
            x=window_width//2-240, y=130, width=80, height=80,
            bg_colour="#49A078"
        ), Image( # Piece image
            x=window_width//2-245, y=125, width=90, height=90,
            img_source="assets/wr.png"
        ), MultiLineText( # Info
            x=window_width//2-155, y=130, text_colour="#DCE1DE", font="twcen",
            text_size=20, text="Rooks have a piece value of 5. They can move\nboth horizontally and vertically as far as you\nwant."
        ), TextLabel(
            x=window_width//2-250, y=225, width=500, height=20,
            text_size=20, font="twcen",
            text="Try moving each piece on the board."
        ), Button( # Previous button
            x=window_width//2-245, y=270, width=242, height=25, text_size=26,
            bg_colour="#2F3732", text="previous", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.ChangeMenu(-1)
        ), Button( # Close button
            x=window_width//2+3, y=270, width=242, height=25, text_size=26,
            bg_colour="#2F3732", text="close", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.PlayMenu("8/8/2B5/8/5N2/3R4/8/8")
        )
    ]

def FinishedBKRElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=150,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="Bishop, Knight and Rook", text_size=18
        ), TextLabel(
            x=window_width//2-250, y=160, width=500, height=20,
            text_size=20, font="twcen",
            text="Well done! You have successfully moved each piece."
        ), Button(
            x=window_width//2-245, y=220, width=490, height=25, text_size=26,
            bg_colour="#2F3732", text="next", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.ChangeMenu()
        )
    ]

def KingInfoElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=200,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="King Movement", text_size=18
        ), Frame(
            x=window_width//2-240, y=130, width=80, height=80,
            bg_colour="#49A078"
        ), Image( # Piece image
            x=window_width//2-242, y=127, width=84, height=84,
            img_source="assets/wk.png"
        ), MultiLineText( # Info
            x=window_width//2-155, y=130, text_colour="#DCE1DE", font="twcen",
            text_size=20, text="The king is the most important piece on the board.\nThe king can move to any of its adjacent squares.\nIf the king is in an enemy pieces' attack line then\nthe king is in check and must move or block the\nattack. If the king is in check and cannot move\nthen the game is lost."
        ), Button( # Next button
            x=window_width//2-245, y=270, width=490, height=25, text_size=26,
            bg_colour="#2F3732", text="next", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.ChangeMenu()
        )
    ]

def QueenInfoElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=200,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="Queen Movement", text_size=18
        ), Frame(
            x=window_width//2-240, y=130, width=80, height=80,
            bg_colour="#49A078"
        ), Image( # Piece image
            x=window_width//2-242, y=127, width=84, height=84,
            img_source="assets/wq.png"
        ), MultiLineText( # Info
            x=window_width//2-155, y=130, text_colour="#DCE1DE", font="twcen",
            text_size=20, text="The queen has a piece value of 9. The queen\ncan move along the diagonals, horizontals and\nverticals. The queen is the most powerful piece\non the board."
        ), TextLabel(
            x=window_width//2-250, y=225, width=500, height=20,
            text_size=20, font="twcen",
            text="Try moving the king and the queen."
        ), Button( # Previous button
            x=window_width//2-245, y=270, width=242, height=25, text_size=26,
            bg_colour="#2F3732", text="previous", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.ChangeMenu(-1)
        ), Button( # Close button
            x=window_width//2+3, y=270, width=242, height=25, text_size=26,
            bg_colour="#2F3732", text="close", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.PlayMenu("8/8/8/3QK3/8/8/8/8")
        )
    ]

def FinishedKAQElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=150,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="King and Queen", text_size=18
        ), TextLabel(
            x=window_width//2-250, y=160, width=500, height=20,
            text_size=20, font="twcen",
            text="Well done! You have successfully moved the king and queen."
        ), Button(
            x=window_width//2-245, y=220, width=490, height=25, text_size=26,
            bg_colour="#2F3732", text="next", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.ChangeMenu()
        )
    ]

def CapturingPiecesElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=255,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="Capturing Pieces", text_size=18
        ), MultiLineText( # Info
            x=window_width//2-245, y=130, text_colour="#DCE1DE", font="twcen",
            text_size=20, text="Capturing is how you remove an opponent's piece from the\nboard. A capture occurs when you move one of your pieces\nonto a tile that is currently occupied by an opponent's piece.\nEach piece captures in the way it moves except for the pawn\nwhich captures diagonally."
        ), MultiLineText(
            x=window_width//2-140, y=255, width=500, height=20,
            text_size=20, font="twcen",
            text="  Next will be a series of scenarios\nTry capturing the opponent's pieces."
        ), Button(
            x=window_width//2-245, y=325, width=490, height=25, text_size=26,
            bg_colour="#2F3732", text="close", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.PlayMenu("8/8/3p4/8/8/8/4P3/8")
        )
    ]

def FinishedScenarioElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=150,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="Capturing Pieces", text_size=18
        ), TextLabel(
            x=window_width//2-250, y=160, width=500, height=20,
            text_size=20, font="twcen",
            text="Well done! You have successfully captured the piece."
        ), Button(
            x=window_width//2-245, y=220, width=490, height=25, text_size=26,
            bg_colour="#2F3732", text="next", text_colour="#DCE1DE"
        )
    ]

def CheckInfoElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=230,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="King Checks", text_size=18
        ), MultiLineText( # Info
            x=window_width//2-245, y=130, text_colour="#DCE1DE", font="twcen",
            text_size=20, text="A check occurs when the king is in an enemy pieces line of\nattack. When your king is in check, you must make a move\nthat gets your king out of the line of attack. This can be\nachieved either by moving the king, blocking the attack or\ncapturing the attacking piece."
        ), TextLabel(
            x=window_width//2-250, y=250, width=500, height=20,
            text_size=20, font="twcen",
            text="Try placing the opponent's king in check"
        ), Button(
            x=window_width//2-245, y=300, width=490, height=25, text_size=26,
            bg_colour="#2F3732", text="close", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.PlayMenu("4k3/3p1p2/4p3/8/8/8/2B2R2/8")
        )
    ]

def FinishedCheckElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=150,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="King Checks", text_size=18
        ), TextLabel(
            x=window_width//2-250, y=160, width=500, height=20,
            text_size=20, font="twcen",
            text="Well done! You have successfully placed the king in check."
        ), Button(
            x=window_width//2-245, y=220, width=490, height=25, text_size=26,
            bg_colour="#2F3732", text="next", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.ChangeMenu()
        )
    ]

def CheckmatesInfoElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=230,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="Checkmates", text_size=18
        ), MultiLineText( # Info
            x=window_width//2-245, y=130, text_colour="#DCE1DE", font="twcen",
            text_size=20, text="A checkmate happens when the king is in check and there\nare no legal moves to escape the attack. This means the king\ncannot move to a safe square, no piece can block the attack\nand the attacking piece can not be captured. When a\ncheckmate occurs the game is over."
        ), TextLabel(
            x=window_width//2-250, y=255, width=500, height=20,
            text_size=20, font="twcen",
            text="Try to checkmate the opponent"
        ), Button(
            x=window_width//2-245, y=300, width=490, height=25, text_size=26,
            bg_colour="#2F3732", text="close", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.PlayMenu("kb6/pp6/7R/8/8/8/1Q6/5B2")
        )
    ]

def FinishedCheckmateElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=150,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="Checkmates", text_size=18
        ), TextLabel(
            x=window_width//2-250, y=160, width=500, height=20,
            text_size=20, font="twcen",
            text="Well done! You have checkmated the opponent."
        ), Button(
            x=window_width//2-245, y=220, width=490, height=25, text_size=26,
            bg_colour="#2F3732", text="next", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.ChangeMenu()
        )
    ]

def CastlingInfoElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=270,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="Castling", text_size=18
        ), MultiLineText( # Info
            x=window_width//2-245, y=130, text_colour="#DCE1DE", font="twcen",
            text_size=20, text="Castling is a special move using the king and the rooks. It is\nthe only move in chess where two pieces move at the same\ntime. To castle, the path between the king and the rook must\nbe clear of both pieces and also of attacking lines from\nenemy pieces. You can castle on both the king and the\nqueens side."
        ), MultiLineText(
            x=window_width//2-150, y=270, width=500, height=20,
            text_size=20, font="twcen",
            text="   Try to castle by selecting the king\nthen selecting the tile closest to the rook."
        ), Button(
            x=window_width//2-245, y=340, width=490, height=25, text_size=26,
            bg_colour="#2F3732", text="close", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.PlayMenu("8/8/8/8/8/8/PPPPPPPP/RNBQK2R")
        )
    ]

def FinishedKingSideElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=150,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="Castling", text_size=18
        ), MultiLineText(
            x=window_width//2-235, y=150, width=500, height=20,
            text_size=20, font="twcen",
            text="Well done! You have successfully castled on the kings side.\n               Now try castling on the queens side."
        ), Button(
            x=window_width//2-245, y=220, width=490, height=25, text_size=26,
            bg_colour="#2F3732", text="close", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.PlayMenu("8/8/8/8/8/8/PPPPPPPP/R3KBNR")
        )
    ]

def FinishedQueenSideElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=150,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="Castling", text_size=18
        ), TextLabel(
            x=window_width//2-250, y=150, width=500, height=20,
            text_size=20, font="twcen",
            text="Well done! You have successfully castled on the Queens side."
        ), Button(
            x=window_width//2-245, y=220, width=490, height=25, text_size=26,
            bg_colour="#2F3732", text="next", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.ChangeMenu()
        )
    ]

def EnPassantElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=240,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="En Passant", text_size=18
        ), MultiLineText( # Info
            x=window_width//2-245, y=130, text_colour="#DCE1DE", font="twcen",
            text_size=20, text="En Passant is a special pawn capture that only happens\nimmediately after an opponent moves a pawn two squares\nforward from its starting position. If the move places the\npawn next to your pawn, your pawn has the opportunity to\ncapture it."
        ), TextLabel(
            x=window_width//2-250, y=260, width=500, height=20,
            text_size=20, font="twcen",
            text="Try an en passant."
        ), Button(
            x=window_width//2-245, y=310, width=490, height=25, text_size=26,
            bg_colour="#2F3732", text="close", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.PlayMenu("r1bqkbnr/ppp1pppp/2n5/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 1")
        )
    ]

def FinishedEnPassantElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=150,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="En Passant", text_size=18
        ), TextLabel(
            x=window_width//2-250, y=150, width=500, height=20,
            text_size=20, font="twcen",
            text="Well done! You have successfully performed an en passant."
        ), Button(
            x=window_width//2-245, y=220, width=490, height=25, text_size=26,
            bg_colour="#2F3732", text="next", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.ChangeMenu()
        )
    ]

def PlayChessElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=300,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="Play Chess", text_size=18
        ), MultiLineText( # Info
            x=window_width//2-245, y=130, text_colour="#DCE1DE", font="twcen",
            text_size=20, text="In chess, white always moves first and players take turns\nmoving one at a time. You win the game by checkmating the\nopponent. A game can also end in a draw as a result of any\nof the following reasons: Stalemate (A player has no legal\nmoves but isn't in check), Threefold-repetition (When the\nsame position occurs three times), Fifty-move rule (When 50\nmoves have passed without pawn movement or capture),\nInsufficient material (When neither side has the material to\nperform a checkmate)"
        ), TextLabel(
            x=window_width//2-250, y=330, width=500, height=20,
            text_size=20, font="twcen",
            text="Move a piece to end the tutorial."
        ), Button(
            x=window_width//2-245, y=370, width=490, height=25, text_size=26,
            bg_colour="#2F3732", text="see the starting position", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.PlayMenu("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        )
    ]

def FinishedTutorialElements():
    return [
        Frame( # Background
            x=window_width//2-250, y=100, width=500, height=150,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-250, y=100, width=500, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-240, y=102,
            font="twcen", text_colour="#000000",
            text="Playing Chess", text_size=18
        ), TextLabel(
            x=window_width//2-250, y=150, width=500, height=20,
            text_size=20, font="twcen",
            text="You can now play chess."
        ), Button(
            x=window_width//2-245, y=220, width=490, height=25, text_size=26,
            bg_colour="#2F3732", text="return to the menu", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.SwitchScreen("main_menu")
        )
    ]

def ChooseAILevelElements():
    return [
        Frame( # Background
            x=window_width//2-150, y=200, width=300, height=150,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-150, y=200, width=300, height=30,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-150, y=207, width=300, height=20,
            font="twcen", text_colour="#DCE1DE",
            text="Choose AI Difficulty", text_size=28
        ), Button( # Easy button
            x=window_width//2-125, y=250, width=75, height=75,
            bg_colour="#6EAE6E", text="EASY",
            onclick=lambda : screen_manager.active_screen.SelectAIDifficulty(0)
        ), Button( # Medium button
            x=window_width//2-37, y=250, width=75, height=75,
            bg_colour="#6E97B9", text="MID",
            onclick=lambda : screen_manager.active_screen.SelectAIDifficulty(1)
        ), Button( # Hard button
            x=window_width//2+50, y=250, width=75, height=75,
            bg_colour="#B04040", text="HARD",
            onclick=lambda : screen_manager.active_screen.SelectAIDifficulty(2)
        )
    ]

def CheckmateScreenElements():
    return [
        Frame( # Background
            x=window_width//2-150, y=200, width=300, height=150,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-150, y=200, width=300, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-150, y=200, width=300, height=20,
            font="twcen", text_colour="#000000",
            text="CHECKMATE", text_size=18
        ), TextLabel(
            x=window_width//2-150, y=250, width=300, height=20,
            text_size=20, font="twcen", id="winner",
            text="BLACK WINS"
        ), Button(
            x=window_width//2-145, y=290, width=290, height=25, text_size=26,
            bg_colour="#2F3732", text="return to main menu", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.SwitchScreen("main_menu")
        ), Button(
            x=window_width//2-145, y=320, width=290, height=25, text_size=26,
            bg_colour="#2F3732", text="close", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.CloseMenu()
        )
    ]

def ExitToMainMenuElements():
    return [
        Frame( # Background
            x=window_width//2-150, y=200, width=300, height=150,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-150, y=200, width=300, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-145, y=202,
            font="twcen", text_colour="#000000",
            text="Return to Main Menu", text_size=18
        ), TextLabel(
            x=window_width//2-150, y=250, width=300, height=20,
            text_size=20, font="twcen", id="winner",
            text="All progress will be lost."
        ), Button(
            x=window_width//2-145, y=290, width=290, height=25, text_size=26,
            bg_colour="#2F3732", text="cancel", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.CloseMenu()
        ), Button(
            x=window_width//2-145, y=320, width=290, height=25, text_size=26,
            bg_colour="#2F3732", text="continue", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.SwitchScreen("main_menu")
        )
    ]

def PuzzleComplete():
    return [
        Frame( # Background
            x=window_width//2-165, y=200, width=330, height=150,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-165, y=200, width=330, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-160, y=202,
            font="twcen", text_colour="#000000",
            text="Completed Puzzle", text_size=18
        ), TextLabel(
            x=window_width//2-165, y=250, width=330, height=20,
            text_size=20, font="twcen", id="winner",
            text="Well done! You completed the puzzle."
        ), Button(
            x=window_width//2-160, y=290, width=320, height=25, text_size=26,
            bg_colour="#2F3732", text="return to main menu", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.SwitchScreen("main_menu")
        ), Button(
            x=window_width//2-160, y=320, width=320, height=25, text_size=26,
            bg_colour="#2F3732", text="play another puzzle", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.NextPuzzle()
        )
    ]

def PuzzleFailed():
    return [
        Frame( # Background
            x=window_width//2-165, y=200, width=330, height=150,
            bg_colour="#1F2421"
        ), Frame( # Top bar
            x=window_width//2-165, y=200, width=330, height=20,
            bg_colour="#216869"
        ), TextLabel( # Title
            x=window_width//2-160, y=202,
            font="twcen", text_colour="#000000",
            text="Failed Puzzle", text_size=18
        ), TextLabel(
            x=window_width//2-165, y=250, width=330, height=20,
            text_size=20, font="twcen", id="winner",
            text="Incorrect move"
        ), Button(
            x=window_width//2-160, y=290, width=320, height=25, text_size=26,
            bg_colour="#2F3732", text="return to main menu", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.SwitchScreen("main_menu")
        ), Button(
            x=window_width//2-160, y=320, width=320, height=25, text_size=26,
            bg_colour="#2F3732", text="try another puzzle", text_colour="#DCE1DE",
            onclick=lambda : screen_manager.active_screen.NextPuzzle()
        )
    ]

screen_elements = {
    "main_menu": MainMenuElements(),
    "start_screen": StartScreenElements(),
    "signin_screen": SignInScreenElements(),
    "signup_screen": SignUpScreenElements(),
    "tutorial_screen": TutorialScreenElements(),
    "puzzle_screen": PuzzleScreenElements(),
    "account_screen": AccountScreenElements(),
    "ai_screen": AIScreenElements()
}

tutorial_sub_screen_elements = [
    StartTutorialElements(),
    PawnMovementElements(), 
    FinishedPawnMovementElements(), 
    BishopInfoElements(),
    KnightInfoElements(),
    RookInfoElements(),
    FinishedBKRElements(),
    KingInfoElements(),
    QueenInfoElements(),
    FinishedKAQElements(),
    CapturingPiecesElements(),
    FinishedScenarioElements(), 
    FinishedScenarioElements(),
    FinishedScenarioElements(),
    FinishedScenarioElements(),
    FinishedScenarioElements(),
    FinishedScenarioElements(),
    CheckInfoElements(),
    FinishedCheckElements(),
    CheckmatesInfoElements(),
    FinishedCheckmateElements(),
    CastlingInfoElements(),
    FinishedKingSideElements(),
    FinishedQueenSideElements(),
    EnPassantElements(),
    FinishedEnPassantElements(),
    PlayChessElements(),
    FinishedTutorialElements()
]

puzzle_sub_screen_elements = [
    PuzzleComplete(),
    PuzzleFailed()
]

ai_sub_screen_elements = [
    ChooseAILevelElements(),
    CheckmateScreenElements(),
    ExitToMainMenuElements()
]

# Sub screen elements
tutorial_sub_screen_elements[11][-1].UpdateProperty(onclick=lambda : screen_manager.active_screen.PlayMenu("8/6p1/8/8/8/8/1R6/8"))
tutorial_sub_screen_elements[12][-1].UpdateProperty(onclick=lambda : screen_manager.active_screen.PlayMenu("8/8/3p4/8/8/8/4N3/8"))
tutorial_sub_screen_elements[13][-1].UpdateProperty(onclick=lambda : screen_manager.active_screen.PlayMenu("8/3p4/8/8/8/8/6B1/8"))
tutorial_sub_screen_elements[14][-1].UpdateProperty(onclick=lambda : screen_manager.active_screen.PlayMenu("8/5Q2/8/8/8/8/1p6/8"))
tutorial_sub_screen_elements[15][-1].UpdateProperty(onclick=lambda : screen_manager.active_screen.PlayMenu("8/1K6/8/8/8/8/6p1/8"))
tutorial_sub_screen_elements[16][-1].UpdateProperty(onclick=lambda : screen_manager.active_screen.ChangeMenu())
screen_manager.screens["tutorial_screen"].sub_screen_elements = tutorial_sub_screen_elements
screen_manager.screens["puzzle_screen"].sub_screen_elements = puzzle_sub_screen_elements
screen_manager.screens["ai_screen"].sub_screen_elements = ai_sub_screen_elements