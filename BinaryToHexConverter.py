import tkinter as tk
from ctypes import windll

root = tk.Tk()

tk.Label(root, text="Binary to hex", font=("consolas", 50)).pack()
table = tk.Frame(root)
table.pack()

root.title("Binary to Hexadecimal Converter")

def hexEdit(*args):
    global value
    if len(hex_StringVar.get()) != 8:
        hex_label["highlightcolor"] = "orange"
        return
    try:
        value = list(f'{bin(int(hex_StringVar.get(), 16))[2:]:0>32}')
        [buttons[i].set(value[i]=="1") for i in range(32)]
        hex_label["highlightcolor"] = "green"
    except:
        hex_label["highlightcolor"] = "red"
    

class ToggleButton(tk.Button):
    def __init__(self, index, **kw):
        super().__init__(command=self.toggle, **kw)
        self.state = False
        self.index = index
    
    def toggle(self):
        self.state = not self.state
        self.__change__()
    
    def set(self, newState:bool):
        self.state = newState
        value[self.index] = newState
        self.__change__()
        
    def __change__(self):
        if self.state:
            self["text"] = "1"
            self["background"] = "black"
            self["foreground"] = "white"
            value[self.index] = "1"
        else:
            self["text"] = "0"
            self["background"] = "white"
            self["foreground"] = "black"
            value[self.index] = "0"
        self.update()

        hex_num = f'{hex(int("".join(value), 2))[2:]:0>8}'
        hex_StringVar.set(hex_num)
        
d = tk.BooleanVar()
[tk.Button(table, text="Flip", font=("consolas", 15), command=lambda i=i: (d.set(not buttons[i*8].state), [b.set(d.get()) for b in buttons[i*8:(i+1)*8]])).grid(column=i*8, row=0, columnspan=8) for i in range(4)]

value = ["0" for i in range(32)]
[tk.Label(table, text=str(31-i), font=("consolas", 20)).grid(column=i, row=1) for i in range(32)]

buttons = [ToggleButton(master=table, text="0", font=("consolas", 20),  background= "white", foreground="black", index=i) for i in range(32)]
[button.grid(column=i, row=2, padx=(15,0) if i%8==0 else 0) for i, button in enumerate(buttons)]

resultFrame = tk.Frame(root)
resultFrame.pack()
hex_StringVar = tk.StringVar(value="00000000")
hex_StringVar.trace_add(mode='write', callback=hexEdit)
hex_label = tk.Entry(resultFrame, textvariable=hex_StringVar, highlightcolor="green", font=("consolas", 40), highlightthickness=5, width=8, border=0, borderwidth=0)

hex_label.grid(column=1, row=0)
tk.Label(resultFrame, text="0x", font=("consolas", 40)).grid(column=0, row=0)

tk.Button(resultFrame, text="Copy", font=("consolas", 15), foreground='green', command=lambda: (hex_label.clipboard_clear(), hex_label.clipboard_append(f'0x{hex_StringVar.get()}'))).grid(column=2, row=0, padx=(15,0))
tk.Button(table, text="Copy", font=("consolas", 15), foreground='green', command=lambda: (hex_label.clipboard_clear(), hex_label.clipboard_append(''.join(value)))).grid(column=33, row=2, padx=(15,0))
tk.Button(root, text='Clear', font=("consolas", 15), foreground='red', command=lambda: [b.set(False) for b in buttons]).pack()


windll.shcore.SetProcessDpiAwareness(1)
root.mainloop()