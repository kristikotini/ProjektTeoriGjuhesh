import tkinter as tk


class minim_dfa:
    def __init__(
        self, dfa_o, converted_dictionary, legend_of_dictionary, final_states_dfa
    ):
        self.dfa_o = dfa_o
        self.converted_dictionary = converted_dictionary
        self.legend_of_dictionary = legend_of_dictionary
        self.final_states_dfa = final_states_dfa
        self.all_states = set(converted_dictionary.keys())
        self.non_final_states = self.all_states - self.final_states_dfa
        self.tmp_states_list = list(self.all_states)
        self.tmp_states_list.sort()
        self.nr_states = len(self.tmp_states_list)
        self.the_2d_table = a = [
            [0 for x in range(self.nr_states)] for y in range(self.nr_states)
        ]
        self.set_with_marked_couples = set()
        self.final_automate_states = set()

    def fill_table(self):
        for i in range(1, self.nr_states):
            for j in range(0, i):
                if (
                    self.tmp_states_list[i] in self.non_final_states
                    and self.tmp_states_list[j] in self.final_states_dfa
                    or self.tmp_states_list[i] in self.final_states_dfa
                    and self.tmp_states_list[j] in self.non_final_states
                ):
                    self.the_2d_table[i][j] = 1
                    marked_couple = (self.tmp_states_list[i], self.tmp_states_list[j])
                    self.set_with_marked_couples.add(marked_couple)
                if (
                    self.set_with_marked_couples == set()
                    and "-1" in self.legend_of_dictionary.keys()
                ):
                    for item in self.final_states_dfa:
                        self.set_with_marked_couples.add(tuple({"-1", item}))

    def look_for_marking(self, i, j, alphabet, dfa):
        for ind in range(len(alphabet)):
            s1 = self.tmp_states_list[i]
            s2 = self.tmp_states_list[j]
            t1 = self.converted_dictionary[s1][ind]
            t2 = self.converted_dictionary[s2][ind]
            for couple in self.set_with_marked_couples:
                if {t1, t2} == set(couple) or (
                    ("-1" == t1 and t2 in self.final_states_dfa)
                    or ("-1" == t2 and t1 in self.final_states_dfa)
                ):
                    self.set_with_marked_couples.add(tuple({s1, s2}))
                    return 1
        return 0

    def marking_states(self):
        flag = 1
        while flag:
            flag = 0
            for i in range(1, self.nr_states):

                for j in range(0, i):

                    if self.the_2d_table[i][j] == 0:
                        tmpflag = self.look_for_marking(
                            i, j, self.dfa_o.alphabet, self.converted_dictionary
                        )
                        if tmpflag == 1:
                            self.the_2d_table[i][j] = 1
                            flag = 1

    def merge_states(self):
        states_to_be_merged = set()
        for i in range(1, self.nr_states):
            for j in range(0, i):
                if self.the_2d_table[i][j] == 0:
                    states_to_be_merged.add(
                        (self.tmp_states_list[i], self.tmp_states_list[j])
                    )
        final_merged_states = set()
        tmp_merged_states = set()
        while states_to_be_merged:
            pairs_to_remove = list()
            tmp = states_to_be_merged.pop()
            for pair in states_to_be_merged:
                a_set = set(tmp)
                b_set = set(pair)
                if a_set & b_set:
                    tmp = a_set | b_set
                    pairs_to_remove.extend(pair)
            tmp_merged_states.add(tuple(tmp))

            for i, k in zip(pairs_to_remove[0::2], pairs_to_remove[1::2]):
                states_to_be_merged.remove(tuple((i, k)))
        for item in tmp_merged_states:
            s = "".join(list(item))
            s = "".join(set(s))
            final_merged_states.add(s)
        self.final_automate_states.update(final_merged_states)
        for item in self.all_states:
            for it in final_merged_states:
                if set(it).isdisjoint(set(item)):
                    self.final_automate_states.add(item)
        if self.final_automate_states == set():
            self.final_automate_states.update(self.all_states)
        return self.final_automate_states

    def get_minimazed_dfa(self, final_states):
        for item in final_states:
            if len(item) > 1:
                statechar = item[0]
                tmp1 = self.converted_dictionary.get(statechar)
                for i in range(0, len(item)):
                    del self.converted_dictionary[item[i]]
                self.converted_dictionary.update({item: tmp1})
                for key in self.converted_dictionary.keys():
                    self.converted_dictionary[key] = [
                        item if x in item else x for x in self.converted_dictionary[key]
                    ]
        return self.converted_dictionary

    def minimization_of_dfa(self):
        self.fill_table()
        self.marking_states()
        final_states = self.merge_states()
        mDFA = self.get_minimazed_dfa(final_states)
        return mDFA

    def vizualize(self, data):
        window = tk.Tk()
        state = tk.Label(window, text="State")
        state.grid(row=0, column=0)
        alphabet_length = len(self.dfa_o.alphabet)
        for i in range(0, alphabet_length):
            char = tk.Label(window, text=self.dfa_o.alphabet[i])
            char.grid(row=0, column=i + 1)
        dfa_states = list(data.keys())
        for i in range(0, len(dfa_states)):
            s = tk.Label(window, text=dfa_states[i])
            s.grid(row=(i + 1), column=0)
            for j in range(0, alphabet_length):
                m = dfa_states[i]
                w = tk.Label(window, text=str(data[m][j]))
                w.grid(row=i + 1, column=j + 1)
        l = tk.Label(window, text="DFA Start State: {}".format(self.dfa_o.start_state))
        l.grid(row=len(dfa_states) + 2)
        gjendjet_fundore = list()
        d = self.dfa_o.dfa_finish_states
        for item in self.final_automate_states:
            for each in d:
                if each in item:
                    gjendjet_fundore.append(item)
                    break
        l = tk.Label(
            window, text="DFA MINIM Finish States: {}".format(gjendjet_fundore),
        )
        l.grid(row=len(dfa_states) + 3)

