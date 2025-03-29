#Finlay Robb CES - 2025/03/26 - Binary to Hex Converter
import tkinter as tk
from ctypes import windll

root = tk.Tk()
root.title("Binary to Hexadecimal Converter")
tk.Label(root, text="Binary to Hex", font=("consolas", 50)).pack()


class Value:
    def __init__(self):
        self.binary = "0"*32
        self.decimal = 0
        self.hexVal = "0"

    def binUpdate(self):
        print('binUpdate')
        self.binary = "".join(["1" if b.getValue() else "0" for b in buttons])
        self.decimal = int(self.binary, 2)
        dec_StringVar.set(str(self.decimal))
        self.hexVal = f'{hex(self.decimal)[2:]:0>8}'
        hex_StringVar.set(self.hexVal)
        

    def hexUpdate(self, newValue:str, *args):
        print(f'hexUpdate: "{newValue}"')

        try:
            if len(newValue) > 8: #if hex value not 8 characters long
                hex_entry["highlightcolor"] = "orange"
                hex_errorLabel["text"] = f"Must be less than or equal to 8 characters long, not {len(newValue)}!"
                return
            
            self.hexVal = newValue

            self.decimal = int(self.hexVal, 16) #convert hex to decimal
            dec_StringVar.set(str(self.decimal))

            self.binary = f'{bin(self.decimal)[2:]:0>32}'
            [buttons[i].setValue(self.binary[i] == '1', True) for i in range(32)] #update binary value

            hex_entry["highlightcolor"] = "green"
            hex_errorLabel["text"] = ""
        except: #if invalid hex value entered
            hex_entry["highlightcolor"] = "red"
            hex_errorLabel["text"] = "Invalid hex value - only 0-9, a-f!"
            

    def decUpdate(self, newValue:str, *args):
        print(f'decUpdate: "{str(newValue)}"')

        try:
            if int(newValue) < 0:
                dec_entry["highlightcolor"] = "orange"
                dec_errorLabel["text"] = f"Must be > 0!"
                return
            
            if int(newValue) > 2**32 -1:
                dec_entry["highlightcolor"] = "orange"
                dec_errorLabel["text"] = f"Number entered cant be greater than {2**32-1}"
                return
            
            self.decimal = int(newValue)

            self.hexVal = f'{hex(self.decimal)[2:]:0>8}'
            hex_StringVar.set(self.hexVal)

            self.binary = f'{bin(self.decimal)[2:]:0>32}'
            print(f'{self.binary=}')
            [buttons[i].setValue(self.binary[i] == '1', True) for i in range(32)] #update binary value

            dec_entry["highlightcolor"] = "green"
            dec_errorLabel["text"] = ""

        except: #if invalid hex value entered
            dec_entry["highlightcolor"] = "red"
            dec_errorLabel["text"] = "Invalid value - only 0-9"


class ToggleButton(tk.Button):
    """Sub class of Button to create a toggle button for binary values"""
    def __init__(self, index:int, **kw):
        super().__init__(command=self.toggleValue, **kw)
        self.index = index
        self.value = False
    
    def getValue(self):
        return self.value
    
    def toggleValue(self):
        self.value = not self.value
        self.__change__()
    
    def setValue(self, newValue:bool, dontUpdate=False):
        self.value = newValue
        self.__change__(dontUpdate)
        
    def __change__(self, dontUpdate=False):  #switch from 0 to 1 or 1 to 0
        if self.getValue(): #if value = 1
            self["text"] = "1"
            self["background"] = "black"
            self["foreground"] = "white"
        else:
            self["text"] = "0"
            self["background"] = "white"
            self["foreground"] = "black"
        self.update()

        if not dontUpdate:
            values.binUpdate()

values = Value()

#Frame for binary buttons and labels
table = tk.Frame(root)
table.pack()

#Multi-Flip buttons
d = tk.BooleanVar() #tempory value to store value of first flip button in each group
[tk.Button(table, text="Flip", font=("consolas", 15), command=lambda i=i: (d.set(not buttons[i*8].getValue()), [b.setValue(d.get()) for b in buttons[i*8:(i+1)*8]]))
    .grid(column=i*8, row=0, columnspan=8, padx=(15,0)) for i in range(4)]
[tk.Button(table, text="Flip", font=("consolas", 15), command=lambda i=i: (d.set(not buttons[i*4].getValue()), [b.setValue(d.get()) for b in buttons[i*4:(i+1)*4]]))
    .grid(column=i*4, row=1, columnspan=4, padx=(15,0) if i%2==0 else 0) for i in range(8)]

#Labels from 31 to 0
[tk.Label(table, text=str(31-i), font=("consolas", 20)).grid(column=i, row=2, padx=(15,0) if i%8==0 else 0) for i in range(32)]

#Binary Buttons
buttons = [ToggleButton(master=table, text="0", font=("consolas", 20),  background= "white", foreground="black", index=i) for i in range(32)]
[button.grid(column=i, row=3, padx=(15,0) if i%8==0 else 0) for i, button in enumerate(buttons)]

#Copy binary value and clear binary value to 0
tk.Button(table, text="Copy", font=("consolas", 15), foreground='green', command=lambda: (hex_entry.clipboard_clear(), hex_entry.clipboard_append(''.join(['1' if b.getValue() else '0' for b in buttons])))).grid(column=33, row=3, padx=(15,0))
tk.Button(table, text='Clear', font=("consolas", 15), foreground='red', command=lambda: [b.setValue(False) for b in buttons]).grid(column=33, row=2, padx=(15,0))

#Frame for hex value
hexFrame = tk.Frame(root)
hexFrame.pack()
tk.Label(hexFrame, text='Hex: ', font=("consolas", 20)).grid(column=0, row=0)
tk.Label(hexFrame, text="0x", font=("consolas", 40)).grid(column=1, row=0) #0x on front of entry

#Entry box for hex value
hex_StringVar = tk.StringVar(value="00000000")  #stores input from text box
hex_entry = tk.Entry(hexFrame, textvariable=hex_StringVar, highlightcolor="green", font=("consolas", 40), highlightthickness=5, width=8, border=0, borderwidth=0) #text box for hex value
hex_entry.bind('<KeyRelease>', func=lambda l: values.hexUpdate(hex_StringVar.get()))
hex_entry.grid(column=2, row=0, pady=10)

#Copy hex value
tk.Button(hexFrame, text="Copy", font=("consolas", 15), foreground='green', command=lambda: (hex_entry.clipboard_clear(), hex_entry.clipboard_append(f'0x{hex_StringVar.get()}'))).grid(column=3, row=0, padx=(15,0))

#Label to display errors in entered hex value
hex_errorLabel = tk.Label(root, text="", font=("consolas", 15), foreground="red")
hex_errorLabel.pack()


#Frame for hex value
decFrame = tk.Frame(root)
decFrame.pack()
tk.Label(decFrame, text="Decimal: ", font=("consolas", 20)).grid(column=0, row=0) #0x on front of entry

#Entry box for dec value
dec_StringVar = tk.StringVar(value='0')  #stores input from text box
dec_entry = tk.Entry(decFrame, textvariable=dec_StringVar, highlightcolor="green", font=("consolas", 40), highlightthickness=5, width=10, border=0, borderwidth=0) #text box for dec value
dec_entry.bind('<KeyRelease>', func= lambda l: values.decUpdate(dec_StringVar.get()))
dec_entry.grid(column=1, row=0, pady=10)

#Copy dec value
tk.Button(decFrame, text="Copy", font=("consolas", 15), foreground='green', command=lambda: (dec_entry.clipboard_clear(), dec_entry.clipboard_append(dec_StringVar.get()))).grid(column=2, row=0, padx=(15,0))

#Label to display errors in entered dec value
dec_errorLabel = tk.Label(root, text="", font=("consolas", 15), foreground="red")
dec_errorLabel.pack()



windll.shcore.SetProcessDpiAwareness(1) #Fixes blurry text
root.mainloop() #Starts the GUI