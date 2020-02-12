import pandas as pd
import numpy as np

filename = "Machine_States.csv"  # duhet marr input nga perdoruesi

dataset = pd.read_csv(filename)
alphabet = ["a", "b"]  # input nga perdoruesi
start_state = 1  # input nga perdoruesi
finish_states = ["3"]  # input nga perdoruesi
nfa_final_states = set()


def get_states():
    states = dataset.iloc[:, 0].values
    states = states[states != -1]
    return states


# nr_rows, nr_columns = dataset.shape


def create_transition_dictionary_for_ENFA():
    epsilon_alphabet = ["epsilon"] + alphabet
    transition_functions = {}
    i = 1
    for char in epsilon_alphabet:
        transition_functions[char] = dataset.iloc[:, i].values
        i += 1
    return transition_functions


def create_dictionary():
    diction = {k: [] for k in alphabet}
    return diction


states = get_states()
tf = create_transition_dictionary_for_ENFA()


def convert_enfa_to_nfa(states, alphabet, tf):
    #print(type(states))
    to_check = {}
    nfa_dictionary = create_dictionary()
    finale = set()
    for state in states:
        for c in alphabet:
            finale.update(set(str(state)))
            to_check = finale.copy()
            finale.clear()
            for st in to_check:
                finale.update(where_to_nfa("epsilon", int(st), tf))
            for i in finale:
                if str(i) in finish_states:
                    nfa_final_states.add(str(state))
                    break
            to_check = finale.copy()
            finale.clear()
            for st in to_check:
                finale.update(where_to_nfa(c, int(st), tf))
            to_check = finale.copy()
            finale.clear()
            for st in to_check:
                finale.update(where_to_nfa("epsilon", int(st), tf))
            if len(finale) != 1 and "-1" in finale:
                finale.remove("-1")

            nfa_dictionary[c].append(list(finale))
            finale.clear()
    return nfa_dictionary


def where_to_nfa(c, s, tf):
    tmp = set()
    tmp.add(str(s))
    if c == "epsilon":
        sq = set(str(tf[c][s]).split(","))
        for st in sq:
            if st != str(s):
                tmp.update(where_to_nfa("epsilon", int(st), tf))
        return tmp
    else:
        sq = set(str(tf[c][s]).split(","))
        return sq


prova = convert_enfa_to_nfa(states, alphabet, tf)
#print(prova)
#print(nfa_final_states)

""" NFA to DFA """


def where_to_dfa(current, alphabet, tf):
    str_ls_cstate = [current]
    tmp = set()
    sq = list()
    final_trans_states = list()
    for c in alphabet:
        for s in str_ls_cstate:
            print(int(s))
            sq.append(str(tf[c][int(current)]))
            print(sq)
            for ch in sq:
                tmp.add(ch)
        sq = list(tmp)
        sq.sort()
        s1 = "".join(sq)
        final_trans_states.append(s1)
        print(final_trans_states)
    return final_trans_states


def convert_nfa_to_dfa(states, alphabet, tf):
    s0 = states.reshape(-1)[0]
    to_check = {int(s0)}
    checked = set()
    dfa_transitions = {states[0]: []}
    while to_check:
        current = to_check.pop()
        tmp = where_to_dfa(current, alphabet,tf)
        for item in tmp:
            if item not in checked:
                to_check.add(item)
        checked.add(current)
        dfa_transitions[current] = tmp
    
dfa = convert_nfa_to_dfa(states, alphabet, prova)
print(dfa)