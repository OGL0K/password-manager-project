import os
import re
import gnupg
import customtkinter

from app_window import SafeMan
from tkinter import messagebox

#Global Variables
pwd = os.path.expanduser('~')

class KeyGen(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Initialise Vault")
        width = 430
        height = 180

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)

        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.resizable(False,False)
        self.protocol("WM_DELETE_WINDOW", self.disable_close)

        self.title_label = customtkinter.CTkLabel(self, text ="Key Generation - Name", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.place(x=80,y=10)

        self.input_label = customtkinter.CTkLabel(self, text ="Please put your real name.", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.input_label.place(x=80,y=35)

        self.enter_button = customtkinter.CTkButton(self, text="Enter", width=60, command=self.checkName)
        self.enter_button.place(x=110,y=110)

        self.cancel_button = customtkinter.CTkButton(self, text="Cancel Generation", width=60, command=self.cancelProcess)
        self.cancel_button.place(x=195,y=110)

        def validate(P):    
            if len(P) > 20:
                messagebox.showinfo('Character Limit', 'Your input should not be longer than 30 characters.', parent=self)
                return False
            elif len(P) <= 20:
                return True
        
        self.vcmd = (self.register(validate), '%P')
        self.input_entry = customtkinter.CTkEntry(self, width=270, validate="key", validatecommand=self.vcmd)
        self.input_entry.place(x=80,y=63)
        

    def checkPassphrase(self):
        special_characters = "!@#$%^&*()-+?_=,<>/"
        alphabet = "abcdefghijklmnopqrstuvwxyz"  
        numbers = "0123456789"
        passphrase = self.input_entry3.get()

        if passphrase == "":
            messagebox.showinfo('Invalid Passphrase', 'Passphrase should not be empty.', parent=self)

        else:
            if any(c in special_characters or c in numbers for c in passphrase) and any(c in alphabet.upper() or c in alphabet for c in passphrase) and len(passphrase) >=8:
                self.geometry("420x150")
                self.input_label.configure(text="Please re-enter your new passphrase")
                self.label.destroy()
                self.label2.destroy()
                self.input_entry3.destroy()
                self.input_entry5 = customtkinter.CTkEntry(self, show="*", width=270)
                self.input_entry5.place(x=80,y=63)
                self.enter_button.configure()
                self.enter_button.place(x=110,y=110)
                self.cancel_button.place(x=195,y=110)

            else:
                if messagebox.askyesno('Weak Passphrase', 'Your passphrase is not considered strong. Do you wish to use this one?', parent=self):
                    self.title("Passphrase Entry for GPG Key & Pass Storage Generation")
                    self.geometry("420x150")
                    self.input_label.configure(text="Please re-enter your new passphrase")
                    self.label.destroy()
                    self.label2.destroy()
                    self.input_entry3.destroy()
                    self.input_entry5 = customtkinter.CTkEntry(self, show="*", width=270)
                    self.input_entry5.place(x=80,y=63)
                    self.enter_button.configure()
                    self.enter_button.place(x=110,y=110)
                    self.cancel_button.place(x=195,y=110)


    def checkEamil(self):
        gtEmail = self.input_entry2.get()
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]{1,}\b"

        if re.fullmatch(regex, gtEmail):
            self.geometry("500x200")
            self.input_entry2.destroy()
            self.input_label.configure(text="Please create a passphrase.")

            self.label = customtkinter.CTkLabel(self, text ="To create a secure passphrase, it should be at least 8", font=customtkinter.CTkFont(size=12, weight="bold"))
            self.label.place(x=80,y=63)

            self.label2 = customtkinter.CTkLabel(self, text ="characters long and contain at least 1 digit or special character.", font=customtkinter.CTkFont(size=12, weight="bold"))
            self.label2.place(x=80,y=83)

            self.title_label.configure(text="Key Generation - Passphrase")
            self.input_entry3 = customtkinter.CTkEntry(self, show="*", width=270)
            self.input_entry3.place(x=80,y=118)
            self.enter_button.configure(command=self.checkPassphrase)
            self.enter_button.place(y=158)
            self.cancel_button.place(y=158)

        elif gtEmail.isascii() == False:
            messagebox.showinfo('Invalid Email', 'Email should not contain non-ascii characters.', parent=self)
        else:
            messagebox.showinfo('Invalid Email','The email address you put is not valid.', parent=self)



    def checkName(self):
        gtname = self.input_entry.get()
        if gtname == "":
            messagebox.showinfo('Invalid Name', 'Name should not be empty.', parent=self)
        elif gtname.isascii() == False:
            messagebox.showinfo('Invalid Name', 'Name should not contain non-ascii characters.', parent=self)
        else:
            self.title_label.configure(text="Key Generation - E-Mail")
            self.input_entry.destroy()
            self.input_label.configure(text="Please put your email address.", font=customtkinter.CTkFont(size=12, weight="bold"))
            self.input_entry2 = customtkinter.CTkEntry(self, width=270)
            self.input_entry2.place(x=80,y=63)
            self.enter_button.configure(command=self.checkEamil)




    def cancelProcess(self):
        if messagebox.askyesno('Cancel Process', 'Are you sure to cancel your vault initiation process?', parent=self):
            self.destroy()
            SafeMan.enable_button(SafeMan())


    def disable_close(self):
        pass


