import os
import customtkinter
from tkinter import messagebox

#Global Variables
pwd = os.path.expanduser('~')

class RadioButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.radiobutton_list = []

        self.all_items = []
        for main_path, sub_directories, files in os.walk(f"{pwd}/.safeman-psw"):
            for file_name in sorted(files):
                if file_name.endswith('.txt'):
                    self.replaced = file_name.replace(".txt", "")
                    self.all_items.append(self.replaced)
                    self.item_add(f"{self.replaced}")
        
    #Adds radiobutton item
    def item_add(self, item):
        radiobutton = customtkinter.CTkRadioButton(self, text=item, value=item, variable=self.radiobutton_variable)
        if self.command is not None:
            radiobutton.configure(command=self.command)
        radiobutton.grid(row=len(self.radiobutton_list), pady=(0, 12))
        self.radiobutton_list.append(radiobutton)

    #Removes radiobutton item
    def item_remove(self, item):
        for radiobutton in self.radiobutton_list:
            if item == radiobutton.cget("text"):
                radiobutton.destroy()
                self.radiobutton_list.remove(radiobutton)
                return
    
    def get_checked_item(self):
        return self.radiobutton_variable.get()


class SafeMan(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("SafeMan")
        self._set_appearance_mode("System")

        #Centering the application
        width = 750
        height = 350 
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.resizable(False,False)
        self.protocol("WM_DELETE_WINDOW", self.quit_app)

        self.toolbar = customtkinter.CTkFrame(self, width=750, height=65, corner_radius=5)
        self.toolbar.place(x=0, y=0)

        self.maintitle = customtkinter.CTkLabel(self.toolbar, text="Welcome to SafeMan", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.maintitle.place(x=65, y=16)

        self.rfrshbtn = customtkinter.CTkButton(self.toolbar, text="Refresh Vault", height=40, width=120, command=self.refresh)
        self.rfrshbtn.place(x=387, y=12)

        self.chngbtn = customtkinter.CTkButton(self.toolbar, text="Ecnrypt Vault with New Key", height=40, width=180)
        self.chngbtn.place(x=527, y=12)

        self.mainbarright = customtkinter.CTkFrame(self, width=220, height=240, corner_radius=20)
        self.mainbarright.place(x=490, y=90)

        self.addpassbtn = customtkinter.CTkButton(self.mainbarright, text="Add Password", height=40, width=170)
        self.addpassbtn.place(x=25, y=30)

        self.rempassbtn = customtkinter.CTkButton(self.mainbarright, text="Delete Password", height=40, width=170, command=self.deletepsw)
        self.rempassbtn.place(x=25, y=100)

        self.seepassbtn = customtkinter.CTkButton(self.mainbarright, text="See Password", height=40, width=170)
        self.seepassbtn.place(x=25, y=170)

        self.radiobutton_frame = RadioButtonFrame(self, width=390, corner_radius=20, command=self.radiobutton_frame_event)
        self.radiobutton_frame.place(x=30, y=90)

    def radiobutton_frame_event(self):
        print(f"radiobutton frame modified: {pwd}/.safeman-psw/{self.radiobutton_frame.get_checked_item()}.txt")

    #Refreshes the password vault.
    def refresh(self):
        if os.path.exists(f"{pwd}/.safeman-psw"):
            self.subdir_file_arr = []
            for i in range (0, len(self.radiobutton_frame.radiobutton_list)):
                self.radiobutton_frame.item_remove(self.radiobutton_frame.all_items[i])

            for main_path, sub_directories, files in os.walk(f"{pwd}/.safeman-psw"):
                for file_name in sorted(files):
                    if file_name.endswith('.txt'):
                        self.radiobutton_frame.replaced = file_name.replace(".txt", "")
                        self.radiobutton_frame.all_items.append(self.radiobutton_frame.replaced)
                        self.radiobutton_frame.item_add(f"{self.radiobutton_frame.replaced}")
            
            messagebox.showinfo('Refreshed', 'Your password vault has been refreshed.', parent=self)
        else:
            messagebox.showinfo('No Vault', 'No vault could not be found on your machine.', parent=self)

    #Deletes password from the vault.
    def deletepsw(self):
        deletepss_question = messagebox.askquestion("Delete Password", f"{self.radiobutton_frame.get_checked_item()} will be deleted. Do you want to continue this process?", parent=self).upper()
        if (deletepss_question[0]== "Y"):
            self.radiobutton_frame.item_remove(self.radiobutton_frame.get_checked_item())
            os.remove(f"{pwd}/.safeman-psw/{self.radiobutton_frame.get_checked_item()}.txt")
            deleted_info = messagebox.showinfo("Password Deleted", f"{self.radiobutton_frame.get_checked_item()}  deleted successfulfy.", parent=self)
        else:
            return None

    def disable_button(self):
        self.rfrshbtn.configure(state= customtkinter.DISABLED)
        self.chngbtn.configure(state= customtkinter.DISABLED)
        self.addpassbtn.configure(state= customtkinter.DISABLED)
        self.rempassbtn.configure(state= customtkinter.DISABLED)
        self.seepassbtn.configure(state= customtkinter.DISABLED)
    

    def enable_button(self):
        self.rfrshbtn.configure(state= customtkinter.NORMAL)
        self.chngbtn.configure(state= customtkinter.NORMAL)
        self.addpassbtn.configure(state= customtkinter.NORMAL)
        self.rempassbtn.configure(state= customtkinter.NORMAL)
        self.seepassbtn.configure(state= customtkinter.NORMAL)


    def disable_close(self):
        pass


    def quit_app(self):
        quit_question = messagebox.askquestion('Exit App', 'Are you sure exitting the applicaiton?', parent=self).upper()
        if quit_question[0] == 'Y':
            self.quit()
        else:
            return None


if __name__ == "__main__":
    app = SafeMan()
    app.mainloop()