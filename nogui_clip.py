# two step hotkeys are broken so need to implement manually
# have first step hotkey trigger a function to create the second step hotkeys, then remove them when one is pressed



import keyboard
import pyperclip
import time

KEY_FUNCTIONS = {
                 's': r'sum({text})',
                 'c': r'coalesce({text}, 0)',
                 'n': r"nullif({text},'')",
                 'f': r"format_timestamp('%Y-%m', {text})",
                 }

def modify_text(entry_text):
    time.sleep(0.5)
    print('send copy cut')
    keyboard.send('ctrl+c, ctrl+x')

    clipboard_text = pyperclip.paste()
    print('clipboard text', clipboard_text)
    if entry_text.isdigit():
        limit = int(entry_text)
        number_range = ', '.join(map(str,range(1,limit + 1)))
        clipboard_text = f'GROUP BY {number_range}\nORDER BY {number_range}'
    else:

        # nodot = 
        # if not all digits then loop through all letters
        for letter in entry_text:
            if letter not in KEY_FUNCTIONS:
                continue # ignore things we don't recognize
            clipboard_text = KEY_FUNCTIONS[letter].format(text=clipboard_text)


    print('clipboard text mod', clipboard_text)
    # test show info
    # showinfo(title="Reply", message = f"entry text: {entry_text}, clipboard text: {clipboard_text}")

    pyperclip.copy(clipboard_text)
    keyboard.send('ctrl+v')


def activate():
    time.sleep(0.5)
    # send ctrl+c to copy just in case can't cut
    keyboard.send('ctrl+c, ctrl+x')
    # open small window
    # open_window()
    time.sleep(0.5)
    keyboard.send('ctrl+v')

# def open_window():
#     root = Tk()
    
#     # root.title("Echo")

#     Label(root, text="(s)um, (c)oalesce, (n)ullif, (f)ormat_timestamp:").pack(side=TOP)
#     ent = Entry(root)
#     ent.bind("<Return>", (lambda event: modify_text(ent.get(), root)))
#     ent.pack(side=TOP)
#     ent.focus_set()
#     # btn = Button(root,text="Submit", command=(lambda: reply(ent.get())))
#     # btn.pack(side=LEFT)

#     root.eval('tk::PlaceWindow . center')
#     root.mainloop()

def main():
    # time.sleep(10) # for testing because ctrl+c is keyboard interrupt
    # activate()

    keyboard.add_hotkey('alt+shift+s', modify_text, args=['scn'], trigger_on_release=False)
    # for letter in KEY_FUNCTIONS.keys():
    #     keyboard.add_hotkey(f'alt+shift+s, {letter}', modify_text, args=[letter])
    keyboard.wait()


# open_window()
if __name__ == "__main__":
    main()