import os
import subprocess
import customtkinter

from tkinter import messagebox

#Global Variables
passpEntry = 3
pswEntry = 3
pwd = os.path.expanduser("~")

class PswAdd(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Add Password to Vault")
        width = 430
        height = 180
        
        self.grab_set()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)

        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.resizable(False,False)
        self.protocol("WM_DELETE_WINDOW", self.disable_close)
        self.bind('<Return>', self.AuthUser)

        self.instructions_label = customtkinter.CTkLabel(self, text ="Authentication", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.instructions_label.place(x=30,y=20)

        self.input_label = customtkinter.CTkLabel(self, text ="Please put your passphrase before you add a new password.")
        self.input_label.place(x=30,y=45)

        self.input_entry = customtkinter.CTkEntry(self, show="*", width=300)
        self.input_entry.place(x=60,y=83)

        self.enter_button = customtkinter.CTkButton(self, text="Enter", width=60, command=self.AuthUser)
        self.enter_button.place(x=120,y=130)

        cancel_button = customtkinter.CTkButton(self, text="Cancel Process", command=self.cancelProcess, width=60)
        cancel_button.place(x=205,y=130)

    #Checks the entered passwords, encrypts the password and stores to the vault.
    def checkPassword(self, event):
        self.re_password = self.input_entry4.get()
        if self.password == self.re_password :
            self.re_password = ""
            byte_password = self.password.encode('utf-8')
            self.password = ""
            command2 = ["gpg", "--batch", "--quiet", "--yes", "--encrypt", "-r", self.gpg_key_id, "-o" ,f"{pwd}/.safeman-psw/{self.file_name}.gpg"]
            out2 = subprocess.check_output(command2, input=byte_password, universal_newlines=False, shell=False, stderr=subprocess.DEVNULL)
            self.file_name = ""
            byte_password = ""
            messagebox.showinfo("Success", "Your password has been successfully added to your vault. Please click to refresh button to refresh your password vault.", parent=self)
            self.destroy()
        
        else:
            global pswEntry
            pswEntry -= 1
            if pswEntry <= 0:
                messagebox.showinfo('', 'Password could not be added due to incorrent password input.', parent=self)
                self.file_name = ""
                self.password = ""
                self.re_password = ""
                self.destroy()
            else:
                messagebox.showinfo('Bad Password', f'Passwords do not match (try {pswEntry} out of 3)', parent=self)

    #Receives the re-typed password.
    def getRePassword(self, event):
        self.bind('<Return>', self.checkPassword)
        if messagebox.askyesno("Question", "Are you sure to add this password?", parent=self):
            self.password = self.input_entry3.get()
            self.instructions_label.configure(text="Password")
            self.input_label.configure(text="Please re-enter your password.")
            self.input_entry3.destroy()
            self.input_entry4 = customtkinter.CTkEntry(self, show="*", width=300)
            self.input_entry4.place(x=60,y=83)
            self.enter_button.configure(command=lambda: self.checkPassword(self.bind()))

    #Receives the password.
    def getPassword(self, event):
        self.bind('<Return>', self.getRePassword)
        self.file_name = self.input_entry2.get()
        self.instructions_label.configure(text="Password")
        self.input_label.configure(text="Please enter your password.")
        self.input_entry2.destroy()
        self.input_entry3 = customtkinter.CTkEntry(self, show="*", width=300)
        self.input_entry3.place(x=60,y=83)
        self.enter_button.configure(command=lambda: self.getRePassword(self.bind()))

    #Receives and checks the file name of the password.
    def getFileName(self, event):
         self.bind('<Return>', self.getPassword)
         self.instructions_label.configure(text="File Name")
         self.input_label.configure(text="Please write the name of your password file.")
         self.input_entry.destroy()

         def validate(P):    
            if len(P) > 20:
                messagebox.showinfo('Character Limit', 'Your input should not be longer than 20 characters.', parent=self)
                return False
            elif len(P) <= 20:
                return True
            
         self.vcmd = (self.register(validate), '%P')
         self.input_entry2 = customtkinter.CTkEntry(self, width=300, validate="key", validatecommand=self.vcmd)
         self.input_entry2.place(x=60,y=83)
         self.enter_button.configure(command=lambda:self.getPassword(self.bind()))

    #Authenticates the user with passphrase.    
    def AuthUser(self, event):
        self.bind('<Return>', self.getFileName)
        passp = self.input_entry.get()
        with open(f'{pwd}/.safeman-psw/.key_id', 'r') as id_file:
                    self.gpg_key_id = str(id_file.read()).strip()

        try:
            kill_command = ["gpgconf", "--kill", "gpg-agent"]
            kill_out = subprocess.check_output(kill_command, universal_newlines=False, shell=False, stderr=subprocess.DEVNULL)
            command1 = ["gpg", "--dry-run", "--passwd", "--quiet", "--yes", "--pinentry-mode=loopback", f"--passphrase={passp}", self.gpg_key_id]
            out = subprocess.check_output(command1, universal_newlines=False, shell=False, stderr=subprocess.DEVNULL)
            self.getFileName(self.bind())
                    

        except subprocess.CalledProcessError:
            global passpEntry
            passpEntry -= 1
            if passpEntry <= 0:
                messagebox.showinfo('Authentication Error', 
                                    'Add Password process terminated due to incorrect passphrase entries.', parent=self)
                self.destroy()
                passpEntry = 3
            else:
                messagebox.showinfo('Bad Passphrase', 
                                    f'Bad passphrase (try {passpEntry} out of 3)', parent=self)
                

    def cancelProcess(self):
        if messagebox.askyesno('Cancel Process', 'Are you sure to cancel your process?', parent=self):
            try:
                self.destroy()
                self.file_name = ""
                self.password = ""
                self.re_password = ""
                self.passphrase = ""
            except AttributeError:
                pass


    def disable_close(self):
        pass
