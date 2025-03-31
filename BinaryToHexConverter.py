#Finlay Robb CES - 2025/03/26 - Binary to Hex Converter
import tkinter as tk
from tkinter import ttk
from ctypes import windll

root = tk.Tk()
root.title("Binary to Hexadecimal Converter")

tk.Label(root, text="Binary to Hex", font=("consolas", 50)).pack()
bits = 32


class Value:
    def __init__(self):
        self.binary = "0"*bits
        self.decimal = 0
        self.hexVal = "0"

    def binUpdate(self):
        self.binary = "".join(["1" if b.getValue() else "0" for b in buttons])

        self.decimal = int(self.binary, 2) #convert binary to decimal
        
        self.hexVal = f'{hex(self.decimal)[2:]:0>{bits//4}}' #convert decimal to hex before possibly changing to negative
        hex_StringVar.set(self.hexVal)

        if signed.get() and self.binary[0] == '1': #if signed is checked, convert to signed decimal
            self.decimal = self.decimal - (1 << bits)
        dec_StringVar.set(str(self.decimal))
        

    def hexUpdate(self, newValue:str, *args):
        dec_errorLabel["text"] = "" #clear decimal error label
        try:
            if newValue[:2].lower() == '0x': #if 0x is in front of hex value then remove it
                self.hexVal = newValue[2:]; hex_StringVar.set(self.hexVal) #update hex value with removed 0x
            else:
                self.hexVal = newValue

            if len(newValue) > bits//4: #if hex value not correct length
                hex_entry["highlightcolor"] = "orange"
                hex_errorLabel["text"] = f"Must be less than or equal to {bits//4} characters long, not {len(newValue)}!"
                return
            if "-" in newValue: #negative hex value not allowed
                raise ValueError()
            
            self.decimal = int(self.hexVal, 16) #convert hex to decimal (unsigned)

            self.binary = f'{bin(self.decimal)[2:]:0>{bits}}' #convert decimal to binary, before possible negative conversion
            [buttons[i].setValue(self.binary[i] == '1', True) for i in range(bits)] #update binary value

            if signed.get() and self.hexVal[0] >= '8': #if signed is checked, convert to signed decimal
                self.decimal -= (1 << bits) #convert to signed decimal
            dec_StringVar.set(str(self.decimal))

            hex_entry["highlightcolor"] = "green"
            hex_errorLabel["text"] = ""

        except ValueError: #if invalid hex value entered
            hex_entry["highlightcolor"] = "red"
            hex_errorLabel["text"] = "Invalid hex value - only 0-9, a-f!"
            

    def decUpdate(self, newValue:str, *args):
        hex_errorLabel["text"] = "" #clear hex error label
        try:
            self.decimal = int(newValue)

            if self.decimal < 0 and not signed.get(): #error if decimal value is negative and signed is not checked
                dec_entry["highlightcolor"] = "orange"
                dec_errorLabel["text"] = f"Can't be less than zero unless in signed mode!"
                return
            if (self.decimal > 2**(bits-1) -1 and signed.get()) or (not signed.get() and self.decimal > 2**(bits) -1): #if decimal value is too high
                dec_entry["highlightcolor"] = "orange"
                dec_errorLabel["text"] = f"Number entered can't be greater than {2**(bits-1) -1 if signed.get() else 2**(bits) -1}!"
                return
            if self.decimal < -(2**(bits-1)) and signed.get(): #if decimal value is too low
                dec_entry["highlightcolor"] = "orange"
                dec_errorLabel["text"] = f"Number entered can't be less than {2**(bits-1)} in signed mode!"
                return

            if self.decimal < 0:
                self.binary = f'1{bin((2 ** (bits-1)) + self.decimal)[2:]:0>{bits-1}}' #convert to signed binary
            else:
                self.binary = f'{bin(self.decimal)[2:]:0>{bits}}' #convert to non signed binary
            [buttons[i].setValue(self.binary[i] == '1', True) for i in range(bits)] #update binary value

            self.hexVal = f'{hex(int(self.binary, 2))[2:]:0>{bits//4}}' #convert binary to hex
            hex_StringVar.set(self.hexVal)

            dec_entry["highlightcolor"] = "green"
            dec_errorLabel["text"] = ""

        except ValueError: #if invalid hex value entered
            dec_entry["highlightcolor"] = "red"
            dec_errorLabel["text"] = "Invalid decimal value - only 0-9"


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
    
    def setValue(self, newValue:bool, dontUpdate:bool=False):
        self.value = newValue
        self.__change__(dontUpdate)
        
    def __change__(self, dontUpdate:bool=False):  #switch button from 0 to 1 or 1 to 0
        if self.getValue(): #if value = 1
            self["text"] = "1"
            self["background"] = "black"
            self["foreground"] = "white"
        else:
            self["text"] = "0"
            self["background"] = "white"
            self["foreground"] = "black"
        self.update()

        if not dontUpdate:   #don't need to recalculate values if just done that
            values.binUpdate()


def generateButtons(newBits:int, table:tk.Frame):
    """Generates the buttons for the binary values"""
    global bits, buttons
    bits = newBits #update bits value
    [i.destroy() for i in table.winfo_children()] #remove old buttons

    #Multi-Flip buttons
    d = tk.BooleanVar() #tempory value to store value of first flip button in each group
    [tk.Button(table, text="Flip", font=("consolas", 15), command=lambda i=i: (d.set(not buttons[i*8].getValue()), [b.setValue(d.get()) for b in buttons[i*8:(i+1)*8]]))
        .grid(column=i*8, row=0, columnspan=8, padx=(15,0)) for i in range(bits//8)] #multi flip buttons for each group of 8
    [tk.Button(table, text="Flip", font=("consolas", 15), command=lambda i=i: (d.set(not buttons[i*4].getValue()), [b.setValue(d.get()) for b in buttons[i*4:(i+1)*4]]))
        .grid(column=i*4, row=1, columnspan=4, padx=(15,0) if i%2==0 else 0) for i in range((bits//4))] #multi flip buttons for each group of 4
    
    [tk.Label(table, text=str(bits-1-i), font=("consolas", 20)).grid(column=i, row=2, padx=(15,0) if i%8==0 else 0) for i in range(bits)] #Labels from bits to 0
    buttons = [ToggleButton(master=table, text="0", font=("consolas", 20),  background= "white", foreground="black", index=i) for i in range(bits)] #Binary Buttons
    [b.grid(column=i, row=3, padx=(15,0) if i%8==0 else 0) for i, b in enumerate(buttons)] #add the buttons


values = Value()

options_Frame = tk.Frame(root) #Frame for options
options_Frame.pack(pady=(0,10))
signed = tk.BooleanVar(value=False) #tempory value to store value of signed checkbox
tk.Checkbutton(options_Frame, text="Signed", variable=signed, font=("consolas", 20), command=values.binUpdate).grid(column=0, row=0) #checkbox to set signed or unsigned

bits_StringVar = tk.IntVar(value=32) #stores value of bits dropdown menu
bits_OptionMenu = tk.OptionMenu(options_Frame, bits_StringVar, *(4, 8, 16, 32), command=lambda l: [generateButtons(int(l), table), values.binUpdate()])
bits_OptionMenu.config(font=("consolas", 20))
root.nametowidget(bits_OptionMenu.menuname).config(font=("consolas", 20))  # Set font for the menu items.
bits_OptionMenu.grid(column=1, row=0, padx=(20,0)) #dropdown menu to select bit length
tk.Label(options_Frame, text="bits", font=("consolas", 20)).grid(column=2, row=0) #Label for bits dropdown menu


#Frame for binary buttons and labels
table = tk.Frame(root); table.pack()

buttons: list[ToggleButton] = []
generateButtons(32, table) #generate buttons for binary values

#Copy binary value and clear binary value to 0
tk.Button(table, text="Copy", font=("consolas", 15), foreground='green', command=lambda: (hex_entry.clipboard_clear(), hex_entry.clipboard_append(''.join(['1' if b.getValue() else '0' for b in buttons])))).grid(column=33, row=3, padx=(15,0))
tk.Button(table, text='Clear', font=("consolas", 15), foreground='red', command=lambda: [b.setValue(False) for b in buttons]).grid(column=33, row=2, padx=(15,0))


#Frame for hex value
hexFrame = tk.Frame(root)
hexFrame.pack()
tk.Label(hexFrame, text='Hex: ', font=("consolas", 20)).grid(column=0, row=0)
tk.Label(hexFrame, text="0x", font=("consolas", 40)).grid(column=1, row=0) #0x on front of entry

#Entry box for hex value
hex_StringVar = tk.StringVar(value="0"*(bits//4))  #stores input from text box
hex_entry = tk.Entry(hexFrame, textvariable=hex_StringVar, highlightcolor="green", font=("consolas", 40), highlightthickness=5, width=8, border=0, borderwidth=0) #text box for hex value
hex_entry.bind('<KeyRelease>', func=lambda l: values.hexUpdate(hex_StringVar.get()))
hex_entry.grid(column=2, row=0, pady=(10,0))

#Copy hex value
tk.Button(hexFrame, text="Copy", font=("consolas", 15), foreground='green', command=lambda: (hex_entry.clipboard_clear(), hex_entry.clipboard_append(f'0x{hex_StringVar.get()}'))).grid(column=3, row=0, padx=(15,0))

#Label to display errors in entered hex value
hex_errorLabel = tk.Label(root, text="", font=("consolas", 15), foreground="red")
hex_errorLabel.pack(pady=(0,10))


#Frame for decimal value
decFrame = tk.Frame(root)
decFrame.pack()
tk.Label(decFrame, text="Decimal: ", font=("consolas", 20)).grid(column=0, row=0) #Decimal lable on front of entry

#Entry box for decimal value
dec_StringVar = tk.StringVar(value='0')  #stores input from text box
dec_entry = tk.Entry(decFrame, textvariable=dec_StringVar, highlightcolor="green", font=("consolas", 40), highlightthickness=5, width=11, border=0, borderwidth=0) #text box for dec value
dec_entry.bind('<KeyRelease>', func= lambda l: values.decUpdate(dec_StringVar.get()))
dec_entry.grid(column=1, row=0, pady=0)

#Copy decimal value
tk.Button(decFrame, text="Copy", font=("consolas", 15), foreground='green', command=lambda: (dec_entry.clipboard_clear(), dec_entry.clipboard_append(dec_StringVar.get()))).grid(column=2, row=0, padx=(15,0))

#Label to display errors in entered decimal value
dec_errorLabel = tk.Label(root, text="", font=("consolas", 15), foreground="red")
dec_errorLabel.pack(pady=0)


windll.shcore.SetProcessDpiAwareness(1) #Fixes blurry text
root.mainloop() #Starts the GUI