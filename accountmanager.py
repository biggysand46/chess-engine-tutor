from keyvariables import *

tutorial_progress = {0:False,1:False,2:False,3:False,4:False,5:False,6:False,7:False,8:False}
ai_progress = {0:False,1:False,2:False}

def ProducePasswordHash(password):
    hash_value = 0
    multiplier = 31
    # Large prime number to reduce the chance of collisions
    mod_value = int(1e9 + 7)
    # Ensures different orders of the same password doesn't result in the same hash value e.g "abc" "cba"
    rolling_multiplier = 1

    for character in password:
        # Each character is given a hash value using its ascii value
        hash_value = (hash_value + (ord(character) - ord("a") + 1) * rolling_multiplier) % mod_value
        rolling_multiplier = (rolling_multiplier * multiplier) % mod_value
    return hash_value

def CreateUserTable():
    # Opening connection to the database
    connection = sqlite3.connect("userinformation.db")
    cursor = connection.cursor()

    # Creating the user data table
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            puzzle_rating INTEGER DEFAULT 1000,
            puzzles_completed INTEGER DEFAULT 0
        )""")
    
    # Creating tutorial table
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_tutorial (
            id INTEGER PRIMARY KEY, 
            progress TEXT,
            FOREIGN KEY (id) references users(id)
        )""")

    # Creating ai table
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_ai (
            id INTEGER PRIMARY KEY, 
            progress TEXT,
            FOREIGN KEY (id) references users(id)
        )""")


    # Saving changes made to the database and closing connection
    connection.commit()
    connection.close()

def CreateAccount(username, password):
    # Opening connection to the database
    connection = sqlite3.connect('userinformation.db')
    cursor = connection.cursor()

    # Creating hash of password
    password_hash = ProducePasswordHash(password)
    
    try:
        # Safe way of inserting data into the database to avoid SQL injections
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hash))
        user_id = cursor.lastrowid
        cursor.execute("INSERT INTO user_tutorial (id, progress) VALUES (?, ?)", (user_id, json.dumps(tutorial_progress)))
        cursor.execute("INSERT INTO user_ai (id, progress) VALUES (?, ?)", (user_id, json.dumps(ai_progress)))
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        # Returns False if username already exists
        return False
    finally:
        # Closing connection to the database
        connection.close()
    
def VerifyAccount(username, password):
    # Opening connection to the database
    connection = sqlite3.connect("userinformation.db")
    cursor = connection.cursor()

    # Creating hash of password
    password_hash = ProducePasswordHash(password)

    # Fetching the users hashed password using their username
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    fetched_password = cursor.fetchone()
    connection.close()

    if fetched_password:
        user_password = int(fetched_password[0])
        
        if password_hash == user_password:
            # Successful login attempt
            ActiveAccount.SetActiveUser(username)
            return False
        else:
            return "Incorrect Password"
    else:
        return "Username Not Found"   
    
class ActiveAccount():
    current_account = None

    @staticmethod
    def SetActiveUser(username):
        ActiveAccount.current_account = username

    @staticmethod
    def RemoveActiveUser():
        ActiveAccount.current_account = None

    @staticmethod
    def GetActiveUser():
        return ActiveAccount.current_account
    
    @staticmethod
    def GetTutorialProgress():
        connection = sqlite3.connect("userinformation.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT user_tutorial.progress
            FROM user_tutorial
            JOIN users ON user_tutorial.id = users.id
            WHERE users.username = ?
        """, (ActiveAccount.current_account,))
        
        result = cursor.fetchone()
        connection.close()

        if result:
            return json.loads(result[0])
        return None
    
    @staticmethod
    def UpdateTutorialProgress(progress):
        connection = sqlite3.connect("userinformation.db")
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE user_tutorial
            SET progress = ?
            WHERE id = (SELECT id FROM users WHERE username = ?)
        """, (json.dumps(progress), ActiveAccount.current_account,))
        
        connection.commit()
        connection.close()

    @staticmethod
    def GetPuzzleRating():
        connection = sqlite3.connect("userinformation.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT users.puzzle_rating
            FROM users
            WHERE users.username = ?
        """, (ActiveAccount.current_account,))
        
        result = cursor.fetchone()
        connection.close()

        if result is not None:
            return result[0]
        return 0
    
    @staticmethod
    def UpdatePuzzleRating(rating):
        connection = sqlite3.connect("userinformation.db")
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE users
            SET puzzle_rating = ?
            WHERE username = ?
        """, (rating, ActiveAccount.current_account))

        connection.commit()
        cursor = connection.cursor()

    @staticmethod
    def GetPuzzlesComplete():
        connection = sqlite3.connect("userinformation.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT users.puzzles_completed
            FROM users
            WHERE users.username = ?
        """, (ActiveAccount.current_account,))
        
        result = cursor.fetchone()
        connection.close()

        if result is not None:
            return result[0]
        return 0

    @staticmethod
    def UpdatePuzzlesComplete():
        connection = sqlite3.connect("userinformation.db")
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE users
            SET puzzles_completed = puzzles_completed + 1
            WHERE username = ?
        """, (ActiveAccount.current_account,))

        connection.commit()
        cursor = connection.cursor()

    @staticmethod
    def GetAIProgress():
        connection = sqlite3.connect("userinformation.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT user_ai.progress
            FROM user_ai
            JOIN users ON user_ai.id = users.id
            WHERE users.username = ?
        """, (ActiveAccount.current_account,))
        
        result = cursor.fetchone()
        connection.close()

        if result:
            return json.loads(result[0])
        return None
    
    @staticmethod
    def UpdateAIProgress(progress):
        connection = sqlite3.connect("userinformation.db")
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE user_ai
            SET progress = ?
            WHERE id = (SELECT id FROM users WHERE username = ?)
        """, (json.dumps(progress), ActiveAccount.current_account,))
        
        connection.commit()
        connection.close()