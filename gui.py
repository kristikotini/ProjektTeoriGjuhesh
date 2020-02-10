
from tkinter import Label,Button,Entry,Frame
from tkinter import filedialog as fd


class GUI:
    def __init__(self,root):
        self.root = root
        self.frame = Frame(root)
        self.frame.pack()
        self.alphabet_label = self.create_label("Vendos alfabetin",self.frame, 0, 0)
        self.first_label = self.create_label("Vendos gjendjen e fillimit",self.frame, 1, 0)
        self.finalStates_label= self.create_label("Vendos gjendjet perfundimtare",self.frame, 2, 0)
        self.alphabet_input = self.create_input_field(self.frame, 0, 1)
        self.alphabet_input.grid(columnspan=2,sticky='we')
        self.start_input = self.create_input_field(self.frame, 1, 1)
        self.start_input.grid(columnspan=2,sticky='we')
        self.finalStates_input = self.create_input_field(self.frame, 2, 1)
        self.finalStates_input.grid(columnspan=2,sticky='we')
        self.buton_1 = Button(self.frame, text="Konverto ne NFA", padx=20, pady= 10)
        self.buton_1.grid(row = 4, column = 1,rowspan = 2)
        self.buton_2 = Button(self.frame, text="Konverto ne DFA", padx=20, pady= 10)
        self.buton_2.grid(row = 4, column = 2, rowspan = 2)
        self.upload_enfa = Button(self.frame, text='Choose E-NFA', command=self.UploadAction)
        self.upload_enfa.grid(row = 4, column = 0)
        self.upload_nfa = Button(self.frame, text='Choose NFA', command=self.UploadAction)
        self.upload_nfa.grid(row = 5, column = 0)
    
    def create_input_field(self,frame,p1,p2):
        myEntry = Entry(frame, width=35, borderwidth=5)
        myEntry.grid(row=p1,column=p2, sticky = 'e')
        return myEntry

    def create_label(self,text,frame,p1,p2):
        myLabel = Label(frame,text=text)
        myLabel.grid(row=p1,column=p2)
        return myLabel

    def UploadAction(self,event=None):
        filename = fd.askopenfilename()
        return filename

