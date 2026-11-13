from keyvariables import *
from ui import *
from screens import *
from screensettings import *
from accountmanager import *

# Creating the user data table
CreateUserTable()

# Adding each UI element to its screen class
for screen, elements in screen_elements.items():
    screen_manager.screens[screen].InitiateElements(elements)

running = True
while running:
    mouse_position = pygame.mouse.get_pos()
    mouse_button = pygame.mouse.get_pressed()

    # Draw the active window
    screen_manager.active_screen.DrawScreen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            screen_manager.active_screen.EventHandler(event, mouse_position, mouse_button)

    pygame.display.flip()
    clock.tick(24)

# Safely closes pygame
pygame.quit()