import pandas as pd
import numpy as np
#shiko dhe shembullin e klejdit rekursioni i pafund...
#filename = "prova1.csv"  # duhet marr input nga perdoruesi punoi
#filename = "prova2.csv"  #punoi
#filename = "prova3.csv"  #punoi
filename = "prova4.csv"  #punoi
#filename = "Machine_States.csv"
dataset = pd.read_csv(filename)
alphabet = ["a", "b"]  # input nga perdoruesi
start_state = 1  # input nga perdoruesi
finish_states = ["2"]  # input nga perdoruesi
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
final_states_dfa = set()

def where_to_dfa(current, alphabet, tf):
    str_ls_cstate = str(current)
    tmp = set()
    sq = list()
    final_trans_states = list()
    #print("gjendja aktuale ne shqyrtim: " +str_ls_cstate)
    for c in alphabet:
        for s in str_ls_cstate:
            #print("s as str: " +s)
            #print(int(s))
            sq.extend((tf[c][int(s)]))
            #print(sq)
            for ch in sq:
                tmp.add(ch)
        sq = list(tmp)
        sq.sort()
        if len(sq) != 1 and "-1" in sq:
                 sq.remove("-1")
        s1 = "".join(sq)
        sq.clear()
        tmp.clear()
        #print("s1 " + s1)
        final_trans_states.append(s1)
    return final_trans_states


def convert_nfa_to_dfa(states, alphabet, tf):
    to_check = {str(states[0])}
    checked = set()
    dfa_transitions = {str(states[0]): []}
    while to_check:
        current = to_check.pop()
        tmp = where_to_dfa(current, alphabet,tf)
        for item in tmp:
            if item not in checked and item != '-1':
                to_check.add(item)
        checked.add(str(current))
        for fs in nfa_final_states:
            if str(fs) in str(current):
                final_states_dfa.add(current)
        dfa_transitions[current] = tmp
    return dfa_transitions
dfa = convert_nfa_to_dfa(states, alphabet, prova)
#print(dfa)

""" Minimization NFA """

all_states = dfa.keys()
all_states2 = set(all_states)
non_final_states = all_states2 - final_states_dfa
#print(all_states)
#print(all_states2)
#print(non_final_states)

tmp_for_states_list = list(all_states2)
tmp_for_states_list.sort()
#print(tmp_for_states_list)

nr_states = len(tmp_for_states_list)

the_2d_table = a = [[-1 for x in range(nr_states)] for y in range(nr_states)]
#print(the_2d_table)


for i in range(1, nr_states):
    print("i : {}".format(i))
    for j in range(0, i):
        print("j : {}".format(j))

























