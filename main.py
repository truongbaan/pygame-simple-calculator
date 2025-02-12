#Since this use constant number, it wont able to change base on the size of your device

import pygame 

WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (128,128,128)

#init
pygame.init()

#screen size
screen_width = 500
screen_length = 700

#create the window for pygame
win = pygame.display.set_mode((screen_width, screen_length))
pygame.display.set_caption('Calculator')
Icon = pygame.image.load('calculator.png')
pygame.display.set_icon(Icon)

#display screen info

display_length = 200
#button info
button_width, button_length = screen_width/4,(screen_length-display_length)/5

#function for restricting to only 1 operator at the same time
def check_valid(value):
    if value and value[-1] in "+-*X/.":
        value = value[:-1]
    return value


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.edge_color = BLACK

    def draw(self, surface):
        font_size = 20
        pygame.draw.rect(surface, self.edge_color, self.rect.inflate(2, 2))  # Inflate by 2 pixels for edge thickness
        pygame.draw.rect(surface, WHITE, self.rect)
        font = pygame.font.SysFont("comicsans", font_size)
        text = font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
            
# Create a list of buttons
buttons = [
    Button(0, display_length, button_width, button_length, "C"),
    Button(button_width, display_length, button_width, button_length, "CE"),
    Button(button_width*2, display_length, button_width, button_length, "Backward"),
    Button(button_width*3, display_length, button_width, button_length, "/"),
    Button(0, display_length+button_length, button_width, button_length, "7"),
    Button(button_width, display_length+button_length, button_width, button_length, "8"),
    Button(button_width*2, display_length+button_length, button_width, button_length, "9"),
    Button(button_width*3, display_length+button_length, button_width, button_length, "X"),
    Button(0, display_length+button_length*2, button_width, button_length, "4"),
    Button(button_width, display_length+button_length*2, button_width, button_length, "5"),
    Button(button_width*2, display_length+button_length*2, button_width, button_length, "6"),
    Button(button_width*3, display_length+button_length*2, button_width, button_length, "-"),
    Button(0, display_length+button_length*3, button_width, button_length, "1"),
    Button(button_width, display_length+button_length*3, button_width, button_length, "2"),
    Button(button_width*2, display_length+button_length*3, button_width, button_length, "3"),
    Button(button_width*3, display_length+button_length*3, button_width, button_length, "+"),
    Button(0, display_length+button_length*4, button_width, button_length, "0"),
    Button(button_width, display_length+button_length*4, button_width, button_length, "%"),
    Button(button_width*2, display_length+button_length*4, button_width, button_length, "."),
    Button(button_width*3, display_length+button_length*4, button_width, button_length, "="),
]

def calculation(value):
    try:
        value = value.replace('%', '/100')
        value = value.replace('X','*')
        # Check if value ends with an operator, and remove it
        while value and value[-1] in "+-*/%":
            value = value[:-1]  # Remove the last operator
        if value == "": # case nothing has been entered
            value = "0"
        # Evaluate the arithmetic expression
        # Use a safer evaluation method for mathematical expressions
        result = eval(value, {"__builtins__": None}, {}) # use ast.literal_eval() if you want to evaluate the code but not execute it
        #{"__builtins__": None}: restricted to python builtin function
        
        # Convert the result to a string
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero"
    except SyntaxError:
        return "Error: Syntax error in expression"
    except Exception as e:
        return f"Error: {e}"
    
def ReDrawScreen(value):
    #init value
    win.fill(BLACK, (0, 0, screen_width, display_length))
    font_size = 30
    SCORE_FONT = pygame.font.SysFont("comicsans", font_size)
    
    #get the result
    result = calculation(value)
    
    lines = []
    #write the calculation
    while len(value) > 0:
        lines.append(value[:27])  # Take the first 27 characters
        value = value[27:]        # Remove the first 27 characters from value

    y_pos = font_size/2
    for line in lines:
        value_surface = SCORE_FONT.render(line, True, WHITE)
        value_width = value_surface.get_width()
        value_position = (screen_width - value_width - 5, y_pos)
        y_pos += font_size
        
        win.blit(value_surface, value_position)
    
    #write the answer base on the result
    if "Error" in result and "Division" not in result:
        while value and value[-1] not in "+-*/%":
            value = value[:-1]
        if value and value[-1] in "+-*/%": # Remove the operator
            value = value[:-1]
        if value == "":
            answer_text = "0"
        else:
            answer_text = calculation(value)
    else:
        answer_text = f"{result}"
        if "Error" not in answer_text:
            if float(answer_text) > 999999999999999999999999999:
                answer_text = "Overload"
    answer_surface = SCORE_FONT.render(answer_text, True, WHITE)
    answer_width = answer_surface.get_width()
    answer_position = (screen_width - answer_width - 5, display_length - font_size*2)
    
    
    
    win.blit(answer_surface, answer_position)
        
    pygame.display.update()
    
def main():
    backup = ""
    value = ""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                # Handle numeric keypad numbers
                if event.key == pygame.K_KP0 or event.key == pygame.K_0:
                    value += "0"
                elif event.key == pygame.K_KP1 or event.key == pygame.K_1:
                    value += "1"
                elif event.key == pygame.K_KP2 or event.key == pygame.K_2:
                    value += "2"
                elif event.key == pygame.K_KP3 or event.key == pygame.K_3:
                    value += "3"
                elif event.key == pygame.K_KP4 or event.key == pygame.K_4:
                    value += "4"
                elif event.key == pygame.K_KP5 or event.key == pygame.K_5:
                    value += "5"
                elif event.key == pygame.K_KP6 or event.key == pygame.K_6:
                    value += "6"
                elif event.key == pygame.K_KP7 or event.key == pygame.K_7:
                    value += "7"
                elif event.key == pygame.K_KP8 or event.key == pygame.K_8 and not(pygame.key.get_mods() & pygame.KMOD_SHIFT):
                    value += "8"
                elif event.key == pygame.K_KP9 or event.key == pygame.K_9:
                    value += "9"
                elif event.key == pygame.K_PERIOD:
                    value = check_valid(value)
                    value += "."
                elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    backup = value
                    value = calculation(value)
                    
                # Handle other numpad keys
                elif event.key == pygame.K_KP_PLUS:
                    value = check_valid(value)
                    value += "+"
                elif event.key == pygame.K_KP_MINUS:
                    value = check_valid(value)
                    value += "-"
                elif event.key == pygame.K_KP_MULTIPLY:
                    value = check_valid(value)
                    value += "*"
                elif event.key == pygame.K_KP_DIVIDE:
                    value = check_valid(value)
                    value += "/"
                ##handle for main keyboard and mod keys
                elif event.key == pygame.K_SLASH:
                    value = check_valid(value)
                    value += "/"
                elif event.key == pygame.K_MINUS:
                    value = check_valid(value)
                    value += "-"
                elif event.key == pygame.K_8 and (pygame.key.get_mods() & pygame.KMOD_SHIFT):  # Shift + 8
                    value = check_valid(value)
                    value += "X"
                elif event.key == pygame.K_EQUALS and (pygame.key.get_mods() & pygame.KMOD_SHIFT):  # Shift + =
                    value = check_valid(value)
                    value += "+"
                elif event.key == pygame.K_c:
                    value = ""
                #Removes the last character with backspace button
                elif event.key == pygame.K_BACKSPACE:
                    if "Error" in value:
                        value = backup
                    else:
                        value = value[:-1]
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.is_clicked(mouse_pos):
                        if button.text == "C": # delete all
                            value = ""
                        elif button.text == "CE": # delete until encounter a operator or %
                                while value and value[-1] not in "+-*/X%":
                                    value = value[:-1]
                                if value and value[-1] in "+-*/X%": # Remove the operator
                                    value = value[:-1]
                        elif button.text == "Backward": # delete the last character
                            if "Error" in value:
                                value = backup
                            else:
                                value = value[:-1] 
                        elif button.text == ".":  # Only add a decimal if the current number doesn't already have one
                            # Split by operators to check the last number segment
                            last_number_segment = value.split('+')[-1].split('-')[-1].split('*')[-1].split('/')[-1].split('X')[-1].split('%')[-1]
                            if '.' not in last_number_segment:
                                value += "."
                        elif button.text in "+-*/X%":  # For operators and decimal point, run check_valid
                            value = check_valid(value)
                            value += button.text
                        elif button.text == "=": # the formula change to the last result
                            backup = value
                            value = calculation(value)
                        else:
                            value += button.text
                        
        # Draw the buttons
        for button in buttons:
            button.draw(win)
        result = calculation(value)
            
        print(f"Current calculation: {value}, result = {result}") # this line only use for checking, will be remove when completed
        
        ReDrawScreen(value)
        
    pygame.quit()
    
#start the program 
main()
                
