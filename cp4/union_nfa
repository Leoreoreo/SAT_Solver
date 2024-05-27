#!/usr/bin/env python3

import sys
from nfa import NFA, read_nfa

def union_nfa(M1, M2):
    start_state = 'q0'
    states = {f'M1_{s}' for s in M1.states} | {f'M2_{s}' for s in M2.states} | {start_state}
    alphabet = M1.alphabet | M2.alphabet

    transitions = {start_state: {'&': {f'M1_{M1.start_state}', f'M2_{M2.start_state}'}}}
    for state, transition in M1.transitions.items():
        new_state = f'M1_{state}'
        transitions[new_state] = {symbol: {f'M1_{s}' for s in targets} for symbol, targets in transition.items()}
    for state, transition in M2.transitions.items():
        new_state = f'M2_{state}'
        transitions[new_state] = {symbol: {f'M2_{s}' for s in targets} for symbol, targets in transition.items()} 

    accept_states =  {f'M1_{s}' for s in M1.accept_states} | {f'M2_{s}' for s in M2.accept_states} 

    return NFA(states, alphabet, transitions, start_state, accept_states)

def main(arguments=sys.argv[1:]):

    if len(arguments) < 2:
        return
    
    M1 = read_nfa(arguments[0])
    M2 = read_nfa(arguments[1])
    nfa = union_nfa(M1, M2)
    nfa.print()

if __name__ == "__main__":
    main()
