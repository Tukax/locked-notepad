import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
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
            with open(PASSWORD_FILE, 'r') as password_file:
                return password_file.read().strip()
        return None

    def save_password(self):
        try:
            password = simpledialog.askstring("Create Password", "Create a password for the application:", show='*')
            if password:
                with open(PASSWORD_FILE, "w") as file:
                    file.write(password)
                messagebox.showinfo("Success", "Password saved successfully.")
                return password
            else:
                messagebox.showerror("Error", "Invalid password!")
                return None
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the password: {e}")
            return None

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                text_content = self.text_area.get(1.0, tk.END)
                with open(file_path, "w") as file:
                    file.write(text_content)
                messagebox.showinfo("Success", "File saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

    def open_file(self):
        while True:
            password = simpledialog.askstring("Password Entry", "Enter the password to open the file:", show='*')
            if password == self.password:
                file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
                if file_path:
                    try:
                        with open(file_path, "r") as file:
                            text_content = file.read()
                        self.text_area.delete(1.0, tk.END)
                        self.text_area.insert(tk.END, text_content)
                        messagebox.showinfo("Success", "File opened successfully.")
                    except Exception as e:
                        messagebox.showerror("Error", f"An error occurred while opening the file: {e}")
                break  # Parola doğruysa döngüden çık
            elif password is None:  # Kullanıcı iptal ederse
                break  # Döngüden çık
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
