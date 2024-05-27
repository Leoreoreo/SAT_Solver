#!/usr/bin/env python3

import sys
from nfa import NFA, read_nfa

def group_nfa(M, fake_k):
    start_state = f'{fake_k}_OPEN'
    alphabet = M.alphabet
    accept_states =  {f'{fake_k}_CLOSE'} 
    states = M.states | {start_state} | accept_states 
    transitions = M.transitions
    
    transitions[start_state] = {'&': {M.start_state}}
    for state in M.accept_states:
        if state in transitions:
            if '&' in transitions[state]: 
                transitions[state]['&'] |= accept_states 
            else:
                transitions[state].update({'&': accept_states})
        else:
            transitions[state] = {'&': accept_states} 
    return NFA(states, alphabet, transitions, start_state, accept_states)

def main(arguments=sys.argv[1:]):

    M = read_nfa(arguments[0])
    nfa = group_nfa(M, 1)
    nfa.print()

if __name__ == "__main__":
    main()
