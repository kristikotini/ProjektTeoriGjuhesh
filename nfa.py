import read_states as rs
import tkinter as tk

# shiko rastin e rekursioni!!!
class NFA:
    def __init__(self, start_state, final_states, alphabet, filename):
        # inpute nga perdoruesi
        self.start_state = start_state
        self.final_states = final_states.split(",")
        self.alphabet = alphabet.split(",")
        self.filename = filename
        # variabla instance te klases NFA
        self.dataset = rs.get_dataset(self.filename)
        self.tf = self.create_transition_dictionary_for_ENFA()
        self.nfa_finish_states = set()
        self.states = rs.get_states(self.filename)

    def create_dictionary(self):
        diction = {k: [] for k in self.alphabet}
        return diction

    def create_transition_dictionary_for_ENFA(self):
        dataset = self.dataset
        epsilon_alphabet = ["epsilon"] + self.alphabet
        transition_functions = {}
        i = 1
        for char in epsilon_alphabet:
            transition_functions[char] = dataset.iloc[:, i].values
            i += 1
        return transition_functions

    def where_to_nfa(self, c, s, tf, seen_states):
        tmp = set()
        tmp.add(str(s))
        if c == "epsilon":
            seen_states_copy = seen_states.copy()
            seen_states_copy.add(str(s))
            sq = set(str(tf[c][s]).split(","))
            for st in sq:
                if st != str(s) and st not in seen_states:

                    tmp.update(
                        self.where_to_nfa("epsilon", int(st), tf, seen_states_copy)
                    )
            return tmp
        else:
            sq = set(str(tf[c][s]).split(","))
            return sq

    def convert_enfa_to_nfa(self):
        to_check = {}
        nfa_dictionary = self.create_dictionary()
        finale = set()
        seen_states = set()
        for state in self.states:
            for c in self.alphabet:
                finale.update(set(str(state)))
                to_check = finale.copy()
                finale.clear()
                for st in to_check:
                    finale.update(
                        self.where_to_nfa("epsilon", int(st), self.tf, seen_states)
                    )
                for i in finale:
                    if str(i) in self.final_states:
                        self.nfa_finish_states.add(str(state))
                        break
                to_check = finale.copy()
                finale.clear()
                for st in to_check:
                    finale.update(self.where_to_nfa(c, int(st), self.tf, seen_states))
                to_check = finale.copy()
                finale.clear()
                for st in to_check:
                    finale.update(
                        self.where_to_nfa("epsilon", int(st), self.tf, seen_states)
                    )
                if len(finale) != 1 and "-1" in finale:
                    finale.remove("-1")

                nfa_dictionary[c].append(list(finale))
                finale.clear()
        return nfa_dictionary

    def visualize_NFA(self, root, data):
        window = tk.Tk()
        state = tk.Label(window, text="State")
        state.grid(row=0, column=0)
        alphabet_length = len(self.alphabet)
        for i in range(0, alphabet_length):
            char = tk.Label(window, text=self.alphabet[i])
            char.grid(row=0, column=i + 1)
        for i in range(0, len(self.states)):
            s = tk.Label(window, text=self.states[i])
            s.grid(row=(i + 1), column=0)
            for j in range(0, alphabet_length):
                m = self.alphabet[j]
                w = tk.Label(window, text=str(data[m][i]))
                w.grid(row=i + 1, column=j + 1)
        l = tk.Label(window, text="NFA Start State: {}".format(self.start_state))
        l.grid(row=len(self.states) + 2)
        l = tk.Label(
            window, text="NFA Finish States: {}".format(self.nfa_finish_states)
        )
        l.grid(row=len(self.states) + 3)

