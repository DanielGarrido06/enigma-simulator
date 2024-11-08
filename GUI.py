'''
This is some serious spaghetti made for a live demo of the Enigma machine.
Don't worry about understanding it all, just know that it's a simple GUI that
allows you to input a message, key, swaps, and rotor order to encrypt a message,
or decrypt it if you have the parameters set correctly.
'''

import machine as m
import tkinter as tk
from tkinter import simpledialog
import unicodedata
import re

class InputDialog(simpledialog.Dialog):

    def body(self, master):
        tk.Label(master, text="Starting rotor position (e.g., 'AAA'):").grid(row=0)
        tk.Label(master, text="Current rotor position:").grid(row=1)
        tk.Label(master, text="Enter plugboard swaps (space-separated, commas between pairs e.g., 'A,Z B,C'):").grid(row=2)
        tk.Label(master, text="Enter rotor order (comma-separated, e.g., 'I,II,III'):").grid(row=3)
        tk.Label(master, text="").grid(row=4)  # Add a blank row
        tk.Label(master, text="Enter message to encrypt:").grid(row=5)
        
        self.key_entry = tk.Entry(master)
        self.current_key = tk.Entry(master)
        self.swap_entry = tk.Entry(master)
        self.rotor_order_entry = tk.Entry(master)
        self.message_entry = tk.Text(master, height=4, width=50)
        
        self.key_entry.grid(row=0, column=1)
        self.current_key.grid(row=1, column=1)
        self.swap_entry.grid(row=2, column=1)
        self.rotor_order_entry.grid(row=3, column=1)
        self.message_entry.grid(row=5, column=1)
        
        tk.Label(master, text="Output ciphered text:").grid(row=6)
        self.output_text = tk.Text(master, height=4, width=50, state='disabled')
        self.output_text.grid(row=6, column=1)

        tk.Label(master, text="").grid(row=7)  # Add a blank row

        self.encrypt_button = tk.Button(master, text="Encrypt", command=self.encrypt_message)
        self.encrypt_button.grid(row=8, columnspan=2)

        self.message_entry.bind('<KeyRelease>', self.live_encrypt_message)

    def buttonbox(self):
        # Override this method to remove the default "OK" and "Cancel" buttons
        pass

    @staticmethod
    def parse_string(input_str):
        if not input_str:
            return None
    
        pairs = input_str.split()
        result = [tuple(pair.split(',')) for pair in pairs]
        return result

    def set_output_text(self, text):
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state='disabled')

    def remove_special_characters(self,text):
        # Normalize the text to decompose special characters
        normalized_text = unicodedata.normalize('NFD', text)
        # Remove diacritics (accents) and special characters
        cleaned_text = ''.join(c for c in normalized_text if unicodedata.category(c) != 'Mn')
        # Remove any remaining non-alphanumeric characters
        cleaned_text = re.sub(r'[^A-Za-z0-9 ]+', '', cleaned_text)
        return cleaned_text    

    def encrypt_message(self):
        message = self.remove_special_characters(self.message_entry.get("1.0", tk.END).strip())
        key = self.key_entry.get()
        swap_array_input = self.swap_entry.get()
        rotor_oder_array = self.rotor_order_entry.get().split(',')
        swap_array = self.parse_string(swap_array_input)

        e = m.Enigma(key, swap_array, rotor_oder_array)
        cipher_text = e.encipher(message)
        self.set_output_text(cipher_text)


    def live_encrypt_message(self, event):

        # Ignore non-alphabetic characters
        if not event.char.isalpha():
            return
        
        message = self.remove_special_characters(self.message_entry.get("1.0", tk.END).strip())
        key = self.key_entry.get()
        swap_array_input = self.swap_entry.get()
        rotor_oder_array = self.rotor_order_entry.get().split(',')
        swap_array = self.parse_string(swap_array_input)

        e = m.Enigma(key, swap_array, rotor_oder_array)
        updated_output = e.encipher(message)
        self.set_output_text(updated_output)

        # Update the rotor position box
        new_key = e.l_rotor.window + e.m_rotor.window + e.r_rotor.window
        self.current_key.delete(0, tk.END)
        self.current_key.insert(0, new_key)



root = tk.Tk()
root.withdraw()  # Hide the root window

dialog = InputDialog(root, title="Enigma Machine Simulator")