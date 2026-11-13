from keyvariables import pygame, window

class BaseUI:
    ui_instances = []

    def __init__(self, **properties):
        # Setting up properties in a dictionary
        self.properties = {
            "x": properties.get("x", 0),
            "y": properties.get("y", 0),
            "width": properties.get("width", 0),
            "height": properties.get("height", 0),
            "id": properties.get("id", None)
        }

        BaseUI.ui_instances.append(self)

    def UpdateProperty(self, **properties):
        self.properties.update(**properties)

    @staticmethod
    def GetElementById(id):
        for _element in BaseUI.ui_instances:
            if _element.properties["id"] == id:
                return _element

class TextLabel(BaseUI):

    def __init__(self, **properties):
        super().__init__(**properties)

        # Adding text properties
        self.properties["text"] = properties.get("text", "")
        self.properties["font"] = properties.get("font", "freesansbold")
        self.properties["text_size"] = properties.get("text_size", 36)
        self.properties["text_colour"] = properties.get("text_colour", "#FFFFFF")

    def DrawText(self):
        x, y = self.properties["x"], self.properties["y"]
        width, height = self.properties["width"], self.properties["height"]

        # Setting up the text font and size
        font = pygame.font.Font(
            pygame.font.match_font(self.properties["font"]),
            self.properties["text_size"]
        )
        text_to_render = font.render(
            self.properties["text"],
            True, 
            self.properties["text_colour"]
        )
        text_rect = text_to_render.get_rect()
        rect = (x, y)

        if width + height > 0:
            # Centering the text if it has a width and height property
            rect = (x + (width - text_rect.width) / 2, y + (height - text_rect.height) / 2)

        # Rendering text to the window
        window.blit(
            text_to_render,
            rect
        )

    def Draw(self):
        self.DrawText()

class MultiLineText(BaseUI):

    def __init__(self, **properties):
        super().__init__(**properties)

        # Adding text properties
        self.properties["text"] = properties.get("text", "")
        self.properties["font"] = properties.get("font", "freesansbold")
        self.properties["text_size"] = properties.get("text_size", 36)
        self.properties["text_colour"] = properties.get("text_colour", "#FFFFFF")

        # Creating a new text label for each line of text
        self.labels = []
        self.CreateLabels(properties.get("text", "").split("\n"))
        
    def CreateLabels(self, lines_of_text):

        for index in range(len(lines_of_text)):
            _text = lines_of_text[index]
            increment = (self.properties["text_size"]//1) * index

            self.labels.append(
                TextLabel(
                    x=self.properties["x"], y=self.properties["y"]+increment,
                    text=_text, text_colour=self.properties["text_colour"],
                    font=self.properties["font"], text_size=self.properties["text_size"]
                )
            )

    def Draw(self):
        for _label in self.labels:
            _label.DrawText()

class Frame(BaseUI):

    def __init__(self, **properties):
        super().__init__(**properties)
    
        # Adding the background colour property and setting the default colour
        self.properties["bg_colour"] = properties.get("bg_colour", "#000000")

        # Creating a rect and storing it in the frame's properties
        self.frame_rect = pygame.Rect(
            self.properties["x"], 
            self.properties["y"], 
            self.properties["width"], 
            self.properties["height"]
        )

    def DrawFrame(self):
        pygame.draw.rect(
            window, 
            self.properties["bg_colour"], 
            self.frame_rect
        )

    def Draw(self):
        self.DrawFrame()

    def UpdateProperty(self, **properties):
        super().UpdateProperty(**properties)

        self.frame_rect.x = self.properties["x"]
        self.frame_rect.y = self.properties["y"]
        self.frame_rect.width = self.properties["width"]
        self.frame_rect.height = self.properties["height"]

class Button(Frame):

    def __init__(self, **properties):
        super().__init__(**properties)

        # Adding text label
        self.text_label = TextLabel(**properties)
        # Adding mouse functionality 
        self.properties["onclick"] = properties.get("onclick", None)

    def Draw(self):
        self.DrawFrame()
        self.text_label.DrawText()

    def OnClick(self, mouse_position):
        if self.frame_rect.collidepoint(mouse_position):
            button_function = self.properties.get("onclick", None)
            if button_function:
                button_function()
            return True

class Image(BaseUI):

    def __init__(self, **properties):
        super().__init__(**properties)

        self.properties["img_source"] = properties.get("img_source", "")
        self.properties["visible"] = properties.get("visible", True)
    
    def DrawImage(self):
        if not self.properties["visible"]:
            return
        x, y = self.properties["x"], self.properties["y"]
        width, height = self.properties["width"], self.properties["height"]

        image = pygame.image.load(self.properties["img_source"]).convert_alpha()
        image = pygame.transform.smoothscale(image, (width, height))

        window.blit(image, (x, y))

    def Draw(self):
        self.DrawImage()

class TextBox(Frame):

    def __init__(self, **properties):
        super().__init__(**properties)

        self.text_label = TextLabel(**properties)

        # Adding placeholder text to the text box
        self.properties["placeholder"] = properties.get("placeholder", "")
        self.text_label.properties["text"] = self.properties["placeholder"]

    def Draw(self):
        self.DrawFrame()
        self.text_label.Draw()

    def OnClick(self, mouse_position):
        mouse_x, mouse_y = mouse_position[0], mouse_position[1]
        x, y = self.properties["x"], self.properties["y"]
        width, height = self.properties["width"], self.properties["height"]

        # Checking if the mouse position falls within the button position
        if x <= mouse_x < x + width and y <= mouse_y <= y + height:
            return True
        return False
    
    def SetPlaceholder(self):
        self.text_label.properties["text"] = self.properties["placeholder"]
    
    def UpdateText(self, event):
        text_label = self.text_label
        text = text_label.properties["text"]

        if event.key == pygame.K_BACKSPACE:
            if len(text) != 0:
                text_label.properties["text"] = text[0:len(text)-1]
        else:
            text_label.properties["text"] += event.unicode

class UsernameBox(TextBox):

    def __init__(self, **properties):
        super().__init__(**properties)
        self.username = ""
    
    def SetPlaceholder(self):
        self.text_label.properties["text"] = self.properties["placeholder"]
        self.username = ""

    def UpdateText(self, event):
        text_label = self.text_label
        text = text_label.properties["text"]

        if event.key == pygame.K_BACKSPACE:
            if len(text) != 0:
                text_label.properties["text"] = text[0:len(text)-1]
                self.username = self.username[0:len(self.username)-1]
        else:
            # Ensuring the key typed is in the alphabet and limiting username to 12 characters
            if event.unicode.isalnum() and len(text) < 12:
                self.username += event.unicode
                text_label.properties["text"] += event.unicode

class PasswordBox(TextBox):
    
    def __init__(self, **properties):
        super().__init__(**properties)
        self.password = ""

    def SetPlaceholder(self):
        self.text_label.properties["text"] = self.properties["placeholder"]
        self.password = ""
    
    def UpdateText(self, event):
        text_label = self.text_label
        text = text_label.properties["text"]

        if event.key == pygame.K_BACKSPACE:
            if len(text) != 0:
                text_label.properties["text"] = text[0:len(text)-1]
                self.password = self.password[0:len(self.password)-1]
        else:
            # Ensuring the key typed is in the alphabet and limiting username to 12 characters
            if event.unicode.isalnum() and len(text) < 12:
                self.password += event.unicode
                text_label.properties["text"] += "*"