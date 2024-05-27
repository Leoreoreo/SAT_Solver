#!/usr/bin/env python3

import sys
from nfa import NFA, read_nfa

def star_nfa(M):
    start_state = 'ST'
    # while start_state in M.states:
    #     start_state += '_ST'

    states = M.states | {start_state}
    alphabet = M.alphabet
    accept_states =  M.accept_states | {start_state} 

    transitions = M.transitions
    transitions[start_state] = {'&': {M.start_state}}
    for state in M.accept_states:
        if state in transitions:
            if '&' in transitions[state]: 
                transitions[state]['&'].add(M.start_state)
            else:
                transitions[state].update({'&': {M.start_state}})
        else:
            transitions[state] = {'&': {M.start_state}} 
    return NFA(states, alphabet, transitions, start_state, accept_states)

def main(arguments=sys.argv[1:]):

    M = read_nfa(arguments[0])
    nfa = star_nfa(M)
    nfa.print()

if __name__ == "__main__":
    main()
