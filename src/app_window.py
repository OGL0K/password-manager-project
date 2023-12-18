import customtkinter

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

        self.toolbar = customtkinter.CTkFrame(self, width=750, height=65, corner_radius=5)
        self.toolbar.place(x=0, y=0)

        self.maintitle = customtkinter.CTkLabel(self.toolbar, text="Welcome to SafeMan", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.maintitle.place(x=65, y=16)

        self.chngbtn = customtkinter.CTkButton(self.toolbar, text="Ecnrypt Vault with New Key", height=40, width=180)
        self.chngbtn.place(x=507, y=12)

        self.passlist = customtkinter.CTkScrollableFrame(self, width=390, height=120, corner_radius=20)
        self.passlist.place(x=30, y=90)

        self.mainbarright = customtkinter.CTkFrame(self, width=220, height=240, corner_radius=20)
        self.mainbarright.place(x=490, y=90)

        self.addpassbtn = customtkinter.CTkButton(self.mainbarright, text="Add Password", height=40, width=170)
        self.addpassbtn.place(x=25, y=30)

        self.addpassbtn = customtkinter.CTkButton(self.mainbarright, text="Remove Password", height=40, width=170)
        self.addpassbtn.place(x=25, y=100)

        self.addpassbtn = customtkinter.CTkButton(self.mainbarright, text="See Password", height=40, width=170)
        self.addpassbtn.place(x=25, y=170)


        


if __name__ == "__main__":
    app = SafeMan()
    app.mainloop()