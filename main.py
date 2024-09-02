from PIL import ImageFont, ImageDraw, Image
import keyboard, os

font = ImageFont.truetype("malgun.ttf", 16.5)

image = Image.new('RGB', (1, 1))
draw = ImageDraw.Draw(image)

in_chat = False
selection_index = 0
message = ""

def calc_width(text):
    text = "At least I dont need to spell to dominate"
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    return width,height

def remove_char_at_index(s, index):
    return s[:index] + s[index+1:]

def insert_char_at_index(s, index, char):
    return s[:index] + char + s[index:]

def on_key_press(event:keyboard.KeyboardEvent):
    global in_chat, selection_index, message
    if event.name == "escape":
        in_chat = False
        message = ""
        selection_index = 0
    elif event.name == "enter":
        in_chat = not in_chat
        if not in_chat:
            message = ""
            selection_index = 0
    elif in_chat and len(event.name) == 1 or event.name == "space":
        message = insert_char_at_index(message, selection_index, event.name if event.name != "space" else " ")
        selection_index += 1
    elif event.name == "left":
        if selection_index > 0:
            selection_index -= 1
    elif event.name == "right":
        if selection_index < len(message):
            selection_index += 1
    elif event.name == "home":
        selection_index = 0
    elif event.name == "end":
        selection_index = len(message)
    elif event.name == "backspace":
        if selection_index > 0:
            selection_index -= 1
            message = remove_char_at_index(message, selection_index)
    elif event.name == "delete":
        if selection_index < len(message):
            message = remove_char_at_index(message, selection_index)
    if in_chat:
        os.system("cls")
        print(insert_char_at_index(message,selection_index,"|"))

keyboard.on_press(on_key_press)
keyboard.wait()