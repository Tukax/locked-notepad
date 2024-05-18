import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from cryptography.fernet import Fernet
import os

KEY_DIR = os.path.join(os.path.expanduser("~"), ".notepad_app")
KEY_FILE = os.path.join(KEY_DIR, 'key.key')
PASSWORD_FILE = os.path.join(KEY_DIR, 'password.txt')

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Notepad")
        self.root.geometry("600x400")

        # Check the password file
        self.password = self.load_password()

        # If there is no password file or it's corrupted, prompt the user to create a password
        if not self.password:
            self.password = self.save_password()

        # Load the key file
        self.cipher_suite = self.load_key()

        self.text_area = tk.Text(self.root, wrap='word')
        self.text_area.pack(expand=1, fill='both')

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Key File Location", command=self.show_key_location)
        self.file_menu.add_command(label="Exit", command=self.root.quit)

    def load_password(self):
        if os.path.exists(PASSWORD_FILE):
            with open(PASSWORD_FILE, 'rb') as password_file:
                return password_file.read().strip()
        return None

    def save_password(self):
        try:
            password = simpledialog.askstring("Create Password", "Create a password for the application:", show='*')
            if password:
                with open(PASSWORD_FILE, "wb") as file:
                    file.write(password.encode())
                messagebox.showinfo("Success", "Password saved successfully.")
                return password.encode()
            else:
                messagebox.showerror("Error", "Invalid password!")
                return None
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the password: {e}")
            return None

    def load_key(self):
        if not os.path.exists(KEY_DIR):
            os.makedirs(KEY_DIR)
        
        if os.path.exists(KEY_FILE):
            with open(KEY_FILE, 'rb') as key_file:
                key = key_file.read()
        else:
            key = Fernet.generate_key()
            with open(KEY_FILE, 'wb') as key_file:
                key_file.write(key)
        return Fernet(key)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                text_content = self.text_area.get(1.0, tk.END)
                encrypted_text = self.cipher_suite.encrypt(text_content.encode())
                with open(file_path, "wb") as file:
                    file.write(encrypted_text)
                messagebox.showinfo("Success", "File saved and encrypted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

    def open_file(self):
        while True:
            password = simpledialog.askstring("Password Entry", "Enter the password to open the file:", show='*')
            if password == self.password.decode():
                file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
                if file_path:
                    try:
                        with open(file_path, "rb") as file:
                            encrypted_text = file.read()
                        decrypted_text = self.cipher_suite.decrypt(encrypted_text).decode()
                        self.text_area.delete(1.0, tk.END)
                        self.text_area.insert(tk.END, decrypted_text)
                        messagebox.showinfo("Success", "File opened and decrypted successfully.")
                    except Exception as e:
                        messagebox.showerror("Error", f"An error occurred while opening the file: {e}")
                break  
            elif password is None:  
                break  
            else:
                messagebox.showerror("Incorrect Password", "Incorrect password!")
    def show_key_location(self):
        password = simpledialog.askstring("Password Entry", "Enter the password to view the key file location:", show='*')
        if password == self.password:
            messagebox.showinfo("Key File Location", f"The key file is stored here:\n{KEY_FILE}")
        else:
            messagebox.showerror("Incorrect Password", "Incorrect password!")

if __name__ == "__main__":
    root = tk.Tk()
    app = Notepad(root)
    root.mainloop()
