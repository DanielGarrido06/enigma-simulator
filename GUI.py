'''
This is some serious spaghetti made for a live demo of the Enigma machine.
Don't worry about understanding it all, just know that it's a simple GUI that
allows you to input a message, key, swaps, and rotor order to encrypt a message,
or decrypt it if you have the parameters set correctly.
'''


import machine as m
import tkinter as tk
from tkinter import simpledialog

def get_user_input(prompt):
    return simpledialog.askstring("Input", prompt)

def parse_string(input_str):
    if not input_str:
        return None
    
    pairs = input_str.split()
    result = [tuple(pair.split(',')) for pair in pairs]
    return result

class InputDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Enter message to encrypt:").grid(row=0)
        tk.Label(master, text="Enter rotor position (e.g., 'AAA'):").grid(row=1)
        tk.Label(master, text="Enter plugboard swaps (space-separated, commas between pairs e.g., 'A,Z B,C'):").grid(row=2)
        tk.Label(master, text="Enter rotor order (comma-separated, e.g., 'I,II,III'):").grid(row=3)

        self.message_entry = tk.Entry(master)
        self.key_entry = tk.Entry(master)
        self.swap_entry = tk.Entry(master)
        self.rotor_order_entry = tk.Entry(master)

        self.message_entry.grid(row=0, column=1)
        self.key_entry.grid(row=1, column=1)
        self.swap_entry.grid(row=2, column=1)
        self.rotor_order_entry.grid(row=3, column=1)
        return self.message_entry

    def apply(self):
        self.result = {
            "message": self.message_entry.get(),
            "key": self.key_entry.get(),
            "swapArrayInput": self.swap_entry.get(),
            "rotorOderArray": self.rotor_order_entry.get()
        }

root = tk.Tk()
root.withdraw()  # Hide the root window

dialog = InputDialog(root)
inputs = dialog.result

message = inputs["message"]
key = inputs["key"]
swapArrayInput = inputs["swapArrayInput"]
rotorOderArray = inputs["rotorOderArray"].split(',')
swapArray = parse_string(swapArrayInput)

root.destroy()

e = m.Enigma(key, swapArray, rotorOderArray)

# Set the Enigma machine rotor position so that you are sure it is initialized for encryption. 
e.set_rotor_position(key)
# Now encrypt.
cipher_text = e.encipher(message)
print(cipher_text)