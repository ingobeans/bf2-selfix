from PIL import ImageFont, ImageDraw, Image
from screeninfo import get_monitors
import keyboard, os, yaml, sys, pydirectinput
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QApplication, QWidget

font = ImageFont.truetype("malgun.ttf", 16.5)
image = Image.new('RGB', (1, 1))
draw = ImageDraw.Draw(image)

if not os.path.isfile("config.yaml"):
    print("no config.yaml file!")
    quit()

with open("config.yaml","r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

monitor_index = config["monitor index"]
character_data = config["character data"]
color = config["color"]

monitor = get_monitors()[monitor_index]
chat_start_x = int(monitor.width * 0.714062)
chat_start_y = int(monitor.height * 0.221296)

in_chat = False
selection_index = 0
message = ""

app = QApplication(sys.argv)

class TransparentLine(QWidget):
    def __init__(self):
        super().__init__()
        self.start_point = QPoint(0, 0)
        self.end_point = QPoint(0, 0)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showFullScreen()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor("#"+color), 2)
        painter.setPen(pen)
        painter.drawLine(self.start_point, self.end_point)

    def move_line(self, x1, y1, x2, y2):
        self.start_point = QPoint(x1,y1)
        self.end_point = QPoint(x2,y2)
        self.update()

window = TransparentLine()
window.show()

def calc_width(text):
    width = 0
    for char in text:
        char_width = 7
        if char in character_data:
            char_width = character_data[char]
        width += char_width
    return width

def remove_char_at_index(s, index):
    return s[:index] + s[index+1:]

def insert_char_at_index(s, index, char):
    return s[:index] + char + s[index:]

def handle_command(command):
    args = command.split(" ")
    keyword = args.pop(0)
    match keyword:
        case "help":
            print("test command!")
        case _:
            return

def on_enter(event:keyboard.KeyboardEvent):
    global in_chat, selection_index, message
    in_chat = not in_chat
    if not in_chat:
        if message.startswith("/"):
            command = message.removeprefix("/")
            pydirectinput.press("esc")
            handle_command(command)
            message = ""
            selection_index = 0
            window.move_line(0,0,0,0)
            return False
        message = ""
        selection_index = 0
        window.move_line(0,0,0,0)
    return True

def on_key_press(event:keyboard.KeyboardEvent):
    global in_chat, selection_index, message
    if event.name == "esc":
        in_chat = False
        message = ""
        selection_index = 0
        window.move_line(0,0,0,0)
    elif event.name == "enter":
        pass
    elif in_chat and (len(event.name) == 1 or event.name == "space"):
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
        #os.system("cls")
        #print(insert_char_at_index(message,selection_index,"|"))
        x_offset = calc_width(message[:selection_index])
        
        window.move_line(chat_start_x + x_offset, chat_start_y, chat_start_x + x_offset, chat_start_y - 10)

keyboard.on_press_key("enter",on_enter,True)
keyboard.on_press(on_key_press)
sys.exit(app.exec_())
