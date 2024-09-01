import keyboard

in_chat = False
selection_index = 0
message_length = 0

def on_key_press(event:keyboard.KeyboardEvent):
    global in_chat, selection_index, message_length
    if event.name == "enter":
        in_chat = not in_chat
    elif in_chat and len(event.name) == 1 or event.name == "space":
        selection_index += 1
        message_length += 1
    elif event.name == "left":
        if selection_index > 0:
            selection_index -= 1
    elif event.name == "right":
        if selection_index < message_length:
            selection_index += 1
    elif event.name == "home":
        selection_index = 0
    elif event.name == "end":
        selection_index = message_length
    elif event.name == "backspace":
        if selection_index > 0:
            message_length -= 1
            selection_index -= 1
    elif event.name == "delete":
        if selection_index < message_length:
            message_length -= 1
    print(f"{message_length=}")
    print(f"{selection_index=}")

keyboard.on_press(on_key_press)
keyboard.wait()