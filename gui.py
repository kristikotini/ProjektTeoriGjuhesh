from tkinter import Label, Button, Entry, Frame, Toplevel, messagebox
from tkinter import filedialog as fd
from nfa import NFA
from dfa import DFA
from minim import minim_dfa


class GUI:
    def __init__(self, root):
        self.root = root
        self.frame = Frame(root)
        self.frame.pack()
        self.alphabet_label = self.create_label("Vendos alfabetin", self.frame, 0, 0)
        self.first_label = self.create_label(
            "Vendos gjendjen e fillimit", self.frame, 1, 0
        )
        self.finalStates_label = self.create_label(
            "Vendos gjendjet perfundimtare", self.frame, 2, 0
        )
        self.alphabet_input = self.create_input_field(self.frame, 0, 1)
        self.alphabet_input.grid(columnspan=2, sticky="we")
        self.start_input = self.create_input_field(self.frame, 1, 1)
        self.start_input.grid(columnspan=2, sticky="we")
        self.finalStates_input = self.create_input_field(self.frame, 2, 1)
        self.finalStates_input.grid(columnspan=2, sticky="we")
        self.filename = ""
        self.buton_1 = Button(
            self.frame,
            text="Konverto ne NFA",
            padx=20,
            pady=10,
            command=self.convert_to_NFA,
        )
        self.buton_1.grid(row=4, column=1, rowspan=2)
        self.buton_2 = Button(
            self.frame,
            text="Konverto ne DFA",
            padx=20,
            pady=10,
            state="disabled",
            command=self.convert_to_DFA,
        )
        self.buton_2.grid(row=4, column=2, rowspan=2)
        self.buton_3 = Button(
            self.frame,
            text="Minimizo",
            padx=20,
            pady=10,
            state="disabled",
            command=self.minimize_dfa,
        )
        self.buton_3.grid(row=4, column=3, rowspan=2)
        self.upload_enfa = Button(
            self.frame, text="Choose E-NFA", command=self.UploadAction
        )
        self.upload_enfa.grid(row=4, column=0)
        ##### Objects we create after pressing buttons #####
        self.nfa_o = None
        self.nfa_data = None
        self.dfa_o = None
        self.dfa_data = None
        self.converted_dictionary_DFA = None
        self.minim_dfa = None

    def create_input_field(self, frame, p1, p2):
        myEntry = Entry(frame, width=35, borderwidth=5)
        myEntry.grid(row=p1, column=p2, sticky="e")
        return myEntry

    def create_label(self, text, frame, p1, p2):
        myLabel = Label(frame, text=text)
        myLabel.grid(row=p1, column=p2)
        return myLabel

    def UploadAction(self, event=None):
        self.filename = fd.askopenfilename()

    def convert_to_NFA(self):
        alphabet = self.alphabet_input.get()
        start_state = self.start_input.get()
        end_states = self.finalStates_input.get()
        filename = self.filename

        try:
            self.nfa_o = NFA(start_state, end_states, alphabet, filename)
            self.nfa_data = self.nfa_o.convert_enfa_to_nfa()
            self.nfa_o.visualize_NFA(self.root, self.nfa_data)
            self.buton_2.config(state="normal")
        except Exception:
            messagebox.showerror("Error", "Kontrollo Vendsojen e Te dhenave (file csv)")

    def convert_to_DFA(self):
        self.dfa_o = DFA(
            self.nfa_o.states,
            self.nfa_o.start_state,
            self.nfa_o.nfa_finish_states,
            self.nfa_o.alphabet,
            self.nfa_data,
        )
        self.dfa_data = self.dfa_o.convert_nfa_to_dfa()
        self.dfa_o.visualize_DFA(self.dfa_data)
        self.dfa_o.create_converted_dfa(self.dfa_data)
        legend_of_dictionary = self.dfa_o.legend_of_dictionary
        converted_dictionary = self.dfa_o.converted_dictionary
        self.dfa_o.visualize_DFA2(converted_dictionary, legend_of_dictionary)
        self.buton_3.config(state="normal")

    def minimize_dfa(self):
        self.minim_dfa = minim_dfa(
            self.dfa_o,
            self.dfa_o.converted_dictionary,
            self.dfa_o.legend_of_dictionary,
            self.dfa_o.dfa_finish_states,
        )
        DFA_I_MINIM = self.minim_dfa.minimization_of_dfa()
        self.minim_dfa.vizualize(DFA_I_MINIM)
        self.buton_3.config(state="disabled")

