import pandas as pd
import numpy as np
#shiko dhe shembullin e klejdit rekursioni i pafund...
#filename = "rekursion.csv"
#filename = "prova_rekursion_pafund.csv"
#filename = "prova1.csv"  # duhet marr input nga perdoruesi punoi deri ne fund 
#filename = "prova2.csv"  #punoi deri ne fund
#filename = "prova3.csv"  #punoi deri ne fund
#filename = "prova4.csv"  #punoi deri ne fund
filename = "Machine_States.csv" #punoi deri ne fund
dataset = pd.read_csv(filename)
alphabet = ["a", "b"]  # input nga perdoruesi
start_state = "0"  # input nga perdoruesi
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
    seen_states = set()
    for state in states:
        for c in alphabet:
            finale.update(set(str(state)))
            to_check = finale.copy()
            finale.clear()
            for st in to_check:
                finale.update(where_to_nfa("epsilon", int(st), tf,seen_states))
            for i in finale:
                if str(i) in finish_states:
                    nfa_final_states.add(str(state))
                    break
            to_check = finale.copy()
            finale.clear()
            #print("JASHT {}:".format(seen_states))
            for st in to_check:
                finale.update(where_to_nfa(c, int(st), tf,seen_states))
            to_check = finale.copy()
            finale.clear()
            for st in to_check:
                finale.update(where_to_nfa("epsilon", int(st), tf,seen_states))
            if len(finale) != 1 and "-1" in finale:
                finale.remove("-1")

            nfa_dictionary[c].append(list(finale))
            finale.clear()
    return nfa_dictionary


def where_to_nfa(c, s, tf,seen_states):
    tmp = set()
    tmp.add(str(s))
    if c == "epsilon":
        #print("seen_states I PARI i thirrur nga funksioni me s {}: {}".format(s,seen_states))
        seen_states_copy = seen_states.copy()
        seen_states_copy.add(str(s))
        sq = set(str(tf[c][s]).split(","))
        #print(sq)
        for st in sq:
            #print("seen_states pasi u shtua s: {}".format(seen_states))
            if st != str(s) and st not in seen_states:
                
                tmp.update(where_to_nfa("epsilon", int(st), tf,seen_states_copy))
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

all_states = set(dfa.keys())
finish_states_with_error = final_states_dfa
non_final_states = all_states - finish_states_with_error
finish_states_with_error.add("-1")
#print(all_states)
#print(all_states2)
#print(non_final_states)

tmp_states_list = list(all_states)
tmp_states_list.sort()
#print(tmp_for_states_list)

nr_states = len(tmp_states_list)

the_2d_table = a = [[0 for x in range(nr_states)] for y in range(nr_states)]
#print(the_2d_table)
set_with_marked_couples = set()
for i in range(1, nr_states):
    for j in range(0, i):
        #print("State 1: {} ---- State 2: {}".format(tmp_states_list[i],tmp_states_list[j]))
        if(tmp_states_list[i] in non_final_states and tmp_states_list[j]  in finish_states_with_error or tmp_states_list[i] in finish_states_with_error and tmp_states_list[j]  in  non_final_states):
            the_2d_table [i][j] = 1
            marked_couple = (tmp_states_list[i],tmp_states_list[j])
            set_with_marked_couples.add(marked_couple)

set_with_marked_couples.add("-1")
print(the_2d_table)
print(set_with_marked_couples)


def look_for_marking(i,j,alphabet,dfa):
    for ind in range(len(alphabet)):
        s1 = tmp_states_list[i]
        s2 = tmp_states_list[j]
        t1= dfa[s1][ind]
        t2= dfa[s2][ind]
        print("Funksioni look for marking")
        for couple in set_with_marked_couples:
            print("S1: {} --- S2: {}".format(s1, s2))
            print("T1: {} --- T2: {}".format(t1, t2))
            print("Couple: {}".format(couple))
            if {t1,t2} == set(couple) or "-1" in {t1,t2}:
                print("u be if")
                set_with_marked_couples.add(tuple({t1,t2}))
                return 1
    return 0

def marking_states():
    flag = 1 
    while(flag):
        flag = 0
        for i in range(1, nr_states):
    
            for j in range(0, i):
                
                if(the_2d_table[i][j] == 0):
                    tmpflag = look_for_marking(i,j,alphabet,dfa) 
                    print("tmp: {}".format(tmpflag))
                    if tmpflag ==1:
                        the_2d_table[i][j] = 1
                        flag = 1
                        #print("u be ")
                        
final_automate_states = set()

def merge_states():
    states_to_be_merged = set()
    for i in range(1, nr_states):
        for j in range(0, i):
            if the_2d_table[i][j] == 0:
                states_to_be_merged.add((tmp_states_list[i],tmp_states_list[j]))
                
    print("statet qe do behen merge: {}".format(states_to_be_merged))
    final_merged_states = set()
    tmp_merged_states =set()
    while(states_to_be_merged):
        pairs_to_remove = list()
        tmp = states_to_be_merged.pop()
        for pair in states_to_be_merged:
                #def common_member(a, b): 
            a_set = set(tmp) 
            b_set = set(pair) 
            if (a_set & b_set): 
                tmp = a_set|b_set
                pairs_to_remove.extend(pair)
        tmp_merged_states.add(tuple(tmp))
        
        for i,k in zip(pairs_to_remove[0::2], pairs_to_remove[1::2]):
            states_to_be_merged.remove(tuple((i,k)))
    print(tmp_merged_states)
    for item in tmp_merged_states:
       #print("item : {}".format(item))
        s = "".join(list(item))
        s = "".join(set(s))
        final_merged_states.add(s)
    print("finale merged states: {}".format(final_merged_states))
    
    final_automate_states.update(final_merged_states)
    for item in all_states:
        print("item : {}".format(item))
        print("final_merged_states")
        for it in final_merged_states:
            print("it : {}".format(it))
            if set(it).isdisjoint(set(item)):
                final_automate_states.add(item)
    print(final_automate_states)
    
def minimization_of_dfa():
    marking_states()
    merge_states()

minimization_of_dfa()









        














