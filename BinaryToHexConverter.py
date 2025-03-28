import tkinter as tk
from ctypes import windll

root = tk.Tk()
root.title("Binary to Hexadecimal Converter")
tk.Label(root, text="Binary to Hex", font=("consolas", 50)).pack()


def hexEdit(*args):
    """Updates the binary buttons when the hex value is edited"""
    global value
    
    if len(hex_StringVar.get()) != 8: #if hex value not 8 characters long
        hex_label["highlightcolor"] = "orange"
        ErrorLabel["text"] = f"Must be 8 characters long, not {len(hex_StringVar.get())}!"
        return
    
    try:
        binary = [i =='1' for i in f'{bin(int(hex_StringVar.get(), 16))[2:]:0>32}'] #convert hex to 32 bit binary array
        [buttons[i].setState(binary[i]) for i in range(32)]
        hex_label["highlightcolor"] = "green"
        ErrorLabel["text"] = ""
    except: #if invalud hex value entered
        hex_label["highlightcolor"] = "red"
        ErrorLabel["text"] = "Invalid hex value - only 0-9, a-f!"


class ToggleButton(tk.Button):
    """Sub class of Button to create a toggle button for binary values"""
    def __init__(self, index:int, **kw):
        super().__init__(command=self.toggle, **kw)
        self.index = index
    
    def getState(self):
        return value[self.index]
    
    def toggle(self):
        value[self.index] = not value[self.index]
        self.__change__()
    
    def setState(self, newState:bool):
        value[self.index] = newState
        self.__change__()
        
    def __change__(self):  #switch from 0 to 1 or 1 to 0
        if self.getState(): #if value = 1
            self["text"] = "1"
            self["background"] = "black"
            self["foreground"] = "white"
        else:
            self["text"] = "0"
            self["background"] = "white"
            self["foreground"] = "black"
        self.update()
        
        hex_num = f'{hex(int("".join(["1" if i else "0" for i in value]), 2))[2:]:0>8}' #convert binary value to 8-bit hex value
        hex_StringVar.set(hex_num) #update hex value in text box


value = [False for i in range(32)]  #Current binary value. Stored as array of boolean

#Frame for binary buttons and labels
table = tk.Frame(root)
table.pack()

#Multi-Flip buttons
d = tk.BooleanVar() #temp value to store state of first flip button in each group
[tk.Button(table, text="Flip", font=("consolas", 15), command=lambda i=i: (d.set(not buttons[i*8].getState()), [b.setState(d.get()) for b in buttons[i*8:(i+1)*8]]))
    .grid(column=i*8, row=0, columnspan=8, padx=(15,0)) for i in range(4)]
[tk.Button(table, text="Flip", font=("consolas", 15), command=lambda i=i: (d.set(not buttons[i*4].getState()), [b.setState(d.get()) for b in buttons[i*4:(i+1)*4]]))
    .grid(column=i*4, row=1, columnspan=4, padx=(15,0) if i%2==0 else 0) for i in range(8)]

#Labels from 31 to 0
[tk.Label(table, text=str(31-i), font=("consolas", 20)).grid(column=i, row=2, padx=(15,0) if i%8==0 else 0) for i in range(32)]

#Binary Buttons
buttons = [ToggleButton(master=table, text="0", font=("consolas", 20),  background= "white", foreground="black", index=i) for i in range(32)]
[button.grid(column=i, row=3, padx=(15,0) if i%8==0 else 0) for i, button in enumerate(buttons)]

#Copy binary value and clear binary value to 0
tk.Button(table, text="Copy", font=("consolas", 15), foreground='green', command=lambda: (hex_label.clipboard_clear(), hex_label.clipboard_append(''.join(['1' if i else '0' for i in value])))).grid(column=33, row=3, padx=(15,0))
tk.Button(table, text='Clear', font=("consolas", 15), foreground='red', command=lambda: [b.setState(False) for b in buttons]).grid(column=33, row=2, padx=(15,0))

#Frame for hex value
resultFrame = tk.Frame(root)
resultFrame.pack()
tk.Label(resultFrame, text="0x", font=("consolas", 40)).grid(column=0, row=0) #0x on front of entry

#Entry box for hex value
hex_StringVar = tk.StringVar(value="00000000")  #stores input from text box
hex_label = tk.Entry(resultFrame, textvariable=hex_StringVar, highlightcolor="green", font=("consolas", 40), highlightthickness=5, width=8, border=0, borderwidth=0) #text box for hex value
hex_label.bind('<KeyRelease>', hexEdit)
hex_label.grid(column=1, row=0, pady=10)

#Copy hex value
tk.Button(resultFrame, text="Copy", font=("consolas", 15), foreground='green', command=lambda: (hex_label.clipboard_clear(), hex_label.clipboard_append(f'0x{hex_StringVar.get()}'))).grid(column=2, row=0, padx=(15,0))

#Label to display errors in entered hex value
ErrorLabel = tk.Label(root, text="", font=("consolas", 15), foreground="red")
ErrorLabel.pack()


windll.shcore.SetProcessDpiAwareness(1) #Fixes blurry text
root.mainloop() #Starts the GUI