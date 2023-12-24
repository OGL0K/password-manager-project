import os
import subprocess
import customtkinter

from tkinter import messagebox
import app_window

#Global Variables
passpEntry = 3
pwd = os.path.expanduser("~")

class UnlockPsw(customtkinter.CTkToplevel):
    def __init__(self, pswPath, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Passphrase Entry for Password Decryption")
        width = 500
        height = 190
        
        self.grab_set()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)

        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.resizable(False,False)
        self.protocol("WM_DELETE_WINDOW", self.disable_close)
        self.get_path = pswPath
        
        label2 = customtkinter.CTkLabel(self, text="Passphrase Entry for Decryption", font=customtkinter.CTkFont(size=20, weight="bold"))
        label2.place(x=40,y=10)

        label3 = customtkinter.CTkLabel(self,text ="Your passwords are asymmetrically encrypted inside the pass storage.")
        label3.place(x=40,y=35)

        label_extra = customtkinter.CTkLabel(self,text ="Please enter your existing passphrase to decrypt your passwords.")
        label_extra.place(x=40,y=60)
        
        self.passp_entry = customtkinter.CTkEntry(self, show="*", width=320)
        self.passp_entry.place(x=70,y=100)

        enter_button = customtkinter.CTkButton(self, text='Enter', width=60, command=self.encrptPsw)
        enter_button.place(x=140,y=140)

        exit_button = customtkinter.CTkButton(self, text="Cancel Backup", width=60, command= self.cancelProcess)
        exit_button.place(x=225,y=140)

        
    def encrptPsw(self):
        if self.passp_entry:
            try:
                command1 = ["gpg", "-d", "--quiet", "--yes", "--pinentry-mode=loopback", f"--passphrase={self.passp_entry.get()}", f'{self.get_path}']
                out = subprocess.check_output(command1, universal_newlines=False, shell=False, stderr=subprocess.DEVNULL)

                messagebox.showinfo("Success", f"Your password is {str(out)}")
                kill_command = ["gpgconf", "--kill", "gpg-agent"]
                kill_out = subprocess.check_output(kill_command, universal_newlines=False, shell=False, stderr=subprocess.DEVNULL)
                self.destroy()
                self.passphrase = ""

            except subprocess.CalledProcessError:
                    global passpEntry
                    passpEntry -= 1
                    if passpEntry <= 0:
                        messagebox.showinfo('Failed Unlock', 
                                            'Files could not be unlocked due to the incorrect passphrase.', parent=self)
                        self.destroy()
                        passpEntry = 3
                    else:
                        messagebox.showinfo('Bad Passphrase', 
                                            f'Bad passphrase (try {passpEntry} out of 3)', parent=self)
    

    def cancelProcess(self):
        if messagebox.askyesno('Cancel Process', 'Are you sure to cancel your process?', parent=self):
            try:
                self.destroy()
                self.passphrase = ""
            except AttributeError:
                pass


    def disable_close(self):
        pass

        

