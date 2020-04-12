import keyboard
import time
import datetime
import pyperclip
from tkinter import *

HOTKEY = 'ctrl+space'

KEY_FUNCTIONS = {
    "s": {"string": r"sum({text})", "description": r"(s)um"},
    "c": {"string": r"coalesce({text}, 0)", "description": r"(c)oalesce"},
    "n": {"string": r"nullif({text},'')", "description": r"(n)ullif"},
    "f": {"string": r"format_timestamp('%Y-%m', {text})", "description": r"(f)ormat_timestamp"},
}
def preview(clipboard_text,entry_text):
    if len(entry_text) < 1:
        return clipboard_text
    print("clipboard text", clipboard_text)
    if entry_text.isdigit():
        limit = int(entry_text)
        number_range = ", ".join(map(str, range(1, limit + 1)))
        clipboard_text = f"GROUP BY {number_range}\nORDER BY {number_range}"
    else:

        nodot = clipboard_text.replace(".", "_")
        # if not all digits then loop through all letters
        for letter in entry_text:
            if letter not in KEY_FUNCTIONS:
                continue  # ignore things we don't recognize
            clipboard_text = KEY_FUNCTIONS[letter]['string'].format(text=clipboard_text)
        clipboard_text = clipboard_text + " as " + nodot
    return clipboard_text


def modify_text(clipboard_text,entry_text, tk_root):
    tk_root.destroy()
    modified_text = preview(clipboard_text,entry_text)

    print("clipboard text", modified_text)

    pyperclip.copy(modified_text)


def activate():
    while keyboard.is_pressed(HOTKEY):
        print("still pressed, sleeping")
        time.sleep(0.05)
    # send ctrl+c to copy just in case can't cut
    keyboard.send("ctrl+c, ctrl+x")
    clipboard_text = pyperclip.paste()
    print("clipboard text from send", clipboard_text)
    # open small window
    open_window(clipboard_text=clipboard_text)
    time.sleep(0.1)
    keyboard.send("ctrl+v")


def open_window(clipboard_text):
    root = Tk()

    root.title(clipboard_text)

    function_descriptions = []
    for k, v in KEY_FUNCTIONS.items():
        function_descriptions.append(v['description'])

    Label(root, text=', '.join(function_descriptions)).pack(side=TOP)
    # Label(root, text="(s)um, (c)oalesce, (n)ullif, (f)ormat_timestamp:").pack(side=TOP)
    ent = Entry(root)
    ent.bind("<Return>", (lambda event: modify_text(clipboard_text, ent.get(), root)))
    ent.bind("<Escape>", (lambda event: root.destroy()))
    ent.pack(side=TOP)
    ent.focus_set()
    label = Label(root, text="placeholder")
    label.pack()
    def set_label():
        label['text'] = preview(clipboard_text, ent.get())
        root.after(100, set_label)


    root.eval("tk::PlaceWindow . center")
    set_label()
    root.mainloop()


def main():
    keyboard.add_hotkey(HOTKEY, activate)
    keyboard.wait()


# open_window()
if __name__ == "__main__":
    main()
