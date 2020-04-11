import keyboard
import time
import pyperclip
from tkinter import *

KEY_FUNCTIONS = {
    "s": r"sum({text})",
    "c": r"coalesce({text}, 0)",
    "n": r"nullif({text},'')",
    "f": r"format_timestamp('%Y-%m', {text})",
}


def modify_text(entry_text, tk_root):
    tk_root.destroy()

    clipboard_text = pyperclip.paste()
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
            clipboard_text = KEY_FUNCTIONS[letter].format(text=clipboard_text)
        clipboard_text = clipboard_text + " as " + nodot)

    # test show info
    print("clipboard text", clipboard_text)
    # showinfo(title="Reply", message = f"entry text: {entry_text}, clipboard text: {clipboard_text}")

    pyperclip.copy(clipboard_text)


def activate():
    while keyboard.is_pressed("alt+shift+s"):
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

    # root.title("Echo")

    Label(root, text="(s)um, (c)oalesce, (n)ullif, (f)ormat_timestamp:").pack(side=TOP)
    ent = Entry(root)
    ent.bind("<Return>", (lambda event: modify_text(ent.get(), root)))
    ent.pack(side=TOP)
    ent.focus_set()
    # btn = Button(root,text="Submit", command=(lambda: reply(ent.get())))
    # btn.pack(side=LEFT)

    root.eval("tk::PlaceWindow . center")
    root.mainloop()


def main():
    # time.sleep(10) # for testing because ctrl+c is keyboard interrupt
    # activate()

    # keyboard.add_hotkey('alt+shift+s', activate, trigger_on_release=True)
    keyboard.add_hotkey("alt+shift+s", activate)
    keyboard.wait()


# open_window()
if __name__ == "__main__":
    main()
