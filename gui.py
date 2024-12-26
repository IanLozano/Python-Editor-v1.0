# Importing tkinter and its dialog modules
import tkinter as tk
from tkinter import (filedialog, messagebox, simpledialog)  # For file, message, and input dialogs
import subprocess  # For running external processes, such as executing Python code

# Creating the main application window
root = tk.Tk()
root.title("Python Editor v1.0")  # Sets the title of the window
root.geometry("+250+340")  # Sets the window's position on the screen
root.iconbitmap("python_icon.ico")  # Sets the icon for the window (requires a valid .ico file)

# FUNCTIONS
# Opens a file, reads its contents, and displays it in the text editor
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])  # File selection dialog
    if file_path:
        with open(file_path, "r") as file:
            code = file.read()
            code_text.delete("1.0", "end")  # Clears the text area
            code_text.insert("1.0", code)  # Inserts the file's content into the text area
            
# Saves the current content of the text editor to a file
def save_file():
    code = code_text.get("1.0", "end-1c")  # Retrieves all text from the text editor
    file_path = filedialog.asksaveasfilename(defaultextension=".py")  # File save dialog
    if file_path:
        with open(file_path, "w") as file:
            file.write(code)  # Writes the text to the file

# EDIT BUTTONS
# Cuts selected text
def cut_text():
    code_text.event_generate("<<Cut>>")
    
# Copies selected text
def copy_text():
    code_text.event_generate("<<Copy>>")
    
# Pastes text from the clipboard
def paste_text():
    code_text.event_generate("<<Paste>>")
    
# Finds a specific text in the editor and highlights it
def find_text():
    target = simpledialog.askstring("Find", "Enter text to find: ")  # Input dialog for text to find
    if target:
        start_index = code_text.search(target, "1.0", stopindex="end", nocase=True)  # Searches for the text
        if start_index:
            end_index = f"{start_index}+{len(target)}c"
            code_text.tag_remove("search", "1.0", "end")  # Clears previous highlights
            code_text.tag_add("search", start_index, end_index)  # Highlights the text
            code_text.tag_config("search", background="red")  # Sets highlight color
            code_text.mark_set("insert", start_index)  # Moves the cursor to the found text
            code_text.see("insert")  # Scrolls to the text

# Replaces occurrences of specific text in the editor
def replace_text():
    target = simpledialog.askstring("Find and Replace", "Enter text to find:")
    if target:
        replace_with = simpledialog.askstring("Find and Replace", "Replace with:")
        if replace_with:
            start_index = code_text.search(target, "1.0", stopindex="end", nocase=True)
            while start_index:  # Loops to replace all occurrences
                end_index = f"{start_index}+{len(target)}c"
                code_text.delete(start_index, end_index)  # Deletes the found text
                code_text.insert(start_index, replace_with)  # Inserts the replacement text
                start_index = code_text.search(target, start_index, stopindex="end", nocase=True)

# Clears all text in the editor
def clear_text():
    code_text.delete("1.0", "end")

# Displays an "About" dialog
def about():
    about_text = "This is an about section"
    messagebox.showinfo("About", about_text)

# Displays a "Help" dialog
def help():
    help_text = "This is a help section"
    messagebox.showinfo("Help", help_text)

# RUN CODE FUNCTIONS
# Runs the Python code written in the editor
def run_code():
    code = code_text.get("1.0", "end-1c")  # Retrieves all text from the editor
    with open(".temp_file.py", "w") as file:  # Creates a temporary Python file
        file.write(code)
    result = subprocess.run(["python", ".temp_file.py"], capture_output=True)  # Executes the file
    terminal_text.insert("end", result.stdout.decode())  # Displays standard output
    terminal_text.insert("end", result.stderr.decode())  # Displays error output

# Clears the terminal output
def clear_code():
    terminal_text.delete("1.0", "end")

# NAVBAR
navbar = tk.Frame(root)
navbar.pack(fill=tk.X)

# DROPDOWN MENU
menu = tk.Menu(navbar)

# FILE MENU
file_menu = tk.Menu(menu, tearoff=False)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu.add_cascade(label="File", menu=file_menu)

# EDIT MENU
edit_menu = tk.Menu(menu, tearoff=False)
edit_menu.add_command(label="Cut", command=cut_text)
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_command(label="Paste", command=paste_text)
edit_menu.add_command(label="Find", command=find_text)
edit_menu.add_command(label="Replace", command=replace_text)
edit_menu.add_command(label="Clear", command=clear_text)
menu.add_cascade(label="Edit", menu=edit_menu)

# ABOUT MENU
about_menu = tk.Menu(menu, tearoff=False)
about_menu.add_command(label="About", command=about)
menu.add_cascade(label="About", menu=about_menu)

# HELP MENU
help_menu = tk.Menu(menu, tearoff=False)
help_menu.add_command(label="Help", command=help)
menu.add_cascade(label="Help", menu=help_menu)

# RUN MENU
run_menu = tk.Menu(menu, tearoff=False)
run_menu.add_command(label="Run", command=run_code)
run_menu.add_command(label="Clear", command=clear_code)
menu.add_cascade(label="Run", menu=run_menu)

# TEXT AREA FOR CODE
text_frame = tk.Frame(root)
text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

code_text = tk.Text(text_frame, undo=True, maxundo=-1)  # Editor with unlimited undo
code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# SCROLLBAR FOR CODE
text_scroll = tk.Scrollbar(text_frame, command=code_text.yview, orient=tk.VERTICAL)
text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
code_text.config(yscrollcommand=text_scroll.set)

# TEXT AREA FOR TERMINAL OUTPUT
terminal_frame = tk.Frame(root)
terminal_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

terminal_text = tk.Text(terminal_frame, bg="black", fg="white", insertbackground="white")  # Terminal-style text
terminal_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# SCROLLBAR FOR TERMINAL
terminal_scroll = tk.Scrollbar(terminal_frame, command=terminal_text.yview, orient=tk.VERTICAL)
terminal_scroll.pack(side=tk.RIGHT, fill=tk.Y)
terminal_text.config(yscrollcommand=terminal_scroll.set)

# Configure the menu bar
root.config(menu=menu)

# Start the application
root.mainloop()
