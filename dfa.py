import tkinter as tk


class DFA:
    def __init__(self, states, start_state, final_states, alphabet, nfa):
        # inpute nga perdoruesi
        self.start_state = start_state
        self.nfa_finish_states = final_states
        self.alphabet = alphabet
        self.nfa = nfa
        # variablat e instances se DFA
        self.states = states
        self.dfa_states = None
        self.dfa_states2 = None
        self.dfa_finish_states = set()
        self.legend_of_dictionary = {}
        self.converted_dictionary = {}
        # self.dfa_keys = dfa.keys()

    def create_converted_dfa(self, dfa):
        dfa_keys = dfa.keys()
        i = 0
        for key in dfa_keys:
            k = str(i)
            self.legend_of_dictionary.update({key: str(i)})
            i += 1
        self.legend_of_dictionary.update({"-1": "-1"})
        # print("legend: {}".format(legend_of_dictionary))
        self.converted_dictionary = {}

        for key, value in dfa.items():
            k1 = self.legend_of_dictionary.get(key)
            l1 = list(value)
            # print("Po printohet value: {}".format(value))
            l2 = list()
            for item in l1:
                v = self.legend_of_dictionary.get(item)
                l2.append(v)
            # print("Po printohet l2: {}".format(l2))
            self.converted_dictionary.update({k1: l2})
        # print("Po printohet dic i ri: {}".format(converted_dictionary))
        ltmp = list()
        for item in self.dfa_finish_states:
            ltmp.append(self.legend_of_dictionary.get(item))
        self.dfa_finish_states = set(ltmp)

    def where_to_dfa(self, current):
        str_ls_cstate = str(current)
        tmp = set()
        sq = list()
        final_trans_states = list()
        for c in self.alphabet:
            for s in str_ls_cstate:
                sq.extend((self.nfa[c][int(s)]))
                for ch in sq:
                    tmp.add(ch)
            sq = list(tmp)
            sq.sort()
            if len(sq) != 1 and "-1" in sq:
                sq.remove("-1")
            s1 = "".join(sq)
            sq.clear()
            tmp.clear()
            final_trans_states.append(s1)
        return final_trans_states

    def convert_nfa_to_dfa(self):
        to_check = {str(self.states[0])}
        checked = set()
        dfa_transitions = {str(self.states[0]): []}
        while to_check:
            current = to_check.pop()
            tmp = self.where_to_dfa(current)
            for item in tmp:
                if item not in checked and item != "-1":
                    to_check.add(item)
            checked.add(str(current))
            for fs in self.nfa_finish_states:
                if str(fs) in str(current):
                    self.dfa_finish_states.add(current)
            dfa_transitions[current] = tmp
        return dfa_transitions

    def get_dfa_states(self, data):
        return list(data.keys())

    def visualize_DFA(self, data):
        window = tk.Tk()
        state = tk.Label(window, text="State")
        state.grid(row=0, column=0)
        alphabet_length = len(self.alphabet)
        for i in range(0, alphabet_length):
            char = tk.Label(window, text=self.alphabet[i])
            char.grid(row=0, column=i + 1)
        self.dfa_states = self.get_dfa_states(data)
        for i in range(0, len(self.dfa_states)):
            s = tk.Label(window, text=self.dfa_states[i])
            s.grid(row=(i + 1), column=0)
            for j in range(0, alphabet_length):
                m = self.dfa_states[i]
                w = tk.Label(window, text=str(data[m][j]))
                w.grid(row=i + 1, column=j + 1)
        l = tk.Label(window, text="DFA Start State: {}".format(self.start_state))
        l.grid(row=len(self.dfa_states) + 2)
        l = tk.Label(
            window, text="DFA Finish States: {}".format(self.dfa_finish_states)
        )
        l.grid(row=len(self.states) + 3)

    def visualize_DFA2(self, data, legend):
        window = tk.Tk()
        state = tk.Label(window, text="State")
        state.grid(row=0, column=0)
        alphabet_length = len(self.alphabet)
        for i in range(0, alphabet_length):
            char = tk.Label(window, text=self.alphabet[i])
            char.grid(row=0, column=i + 1)
        self.dfa_states2 = self.get_dfa_states(data)
        for i in range(0, len(self.dfa_states2)):
            s = tk.Label(window, text=self.dfa_states2[i])
            s.grid(row=(i + 1), column=0)
            for j in range(0, alphabet_length):
                m = self.dfa_states2[i]
                if m != "-1":
                    w = tk.Label(window, text=str(data[m][j]))
                    w.grid(row=i + 1, column=j + 1)
        l = tk.Label(window, text="DFA Start State: {}".format(self.start_state))
        l.grid(row=len(self.dfa_states) + 2)
        l = tk.Label(
            window, text="DFA Finish States: {}".format(self.dfa_finish_states)
        )
        l.grid(row=len(self.states) + 3)

        window2 = tk.Tk()
        state = tk.Label(window2, text="Legend")
        state.grid(row=0, column=0)
        i = 1
        j = 0
        for key, value in legend.items():
            l = tk.Label(window2, text=key)
            l.grid(row=i, column=j)
            l = tk.Label(window2, text=value)
            l.grid(row=i, column=j + 1)
            i += 1

