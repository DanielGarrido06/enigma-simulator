'''
This is some serious spaghetti made for a live demo of the Enigma machine.
Don't worry about understanding it all, just know that it's a simple GUI that
allows you to input a message, key, swaps, and rotor order to encrypt a message,
or decrypt it if you have the parameters set correctly.
'''


import machine as m
import tkinter as tk
from tkinter import simpledialog

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
        tk.Label(master, text="Output ciphered text:").grid(row=4)

        self.message_entry = tk.Entry(master)
        self.key_entry = tk.Entry(master)
        self.swap_entry = tk.Entry(master)
        self.rotor_order_entry = tk.Entry(master)
        self.output_text = tk.Text(master, height=4, width=50, state='disabled')

        self.message_entry.grid(row=0, column=1)
        self.key_entry.grid(row=1, column=1)
        self.swap_entry.grid(row=2, column=1)
        self.rotor_order_entry.grid(row=3, column=1)
        self.output_text.grid(row=4, column=1)

        self.encrypt_button = tk.Button(master, text="Encrypt", command=self.encrypt_message)
        self.encrypt_button.grid(row=5, columnspan=2)

    def buttonbox(self):
        # Override this method to remove the default "OK" and "Cancel" buttons
        pass

    def set_output_text(self, text):
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state='disabled')

    def encrypt_message(self):
        message = self.message_entry.get()
        key = self.key_entry.get()
        swap_array_input = self.swap_entry.get()
        rotor_oder_array = self.rotor_order_entry.get().split(',')
        swap_array = parse_string(swap_array_input)

        e = m.Enigma(key, swap_array, rotor_oder_array)
        e.set_rotor_position(key)
        cipher_text = e.encipher(message)
        self.set_output_text(cipher_text)

root = tk.Tk()
root.withdraw()  # Hide the root window

dialog = InputDialog(root)