#!/usr/bin/env python3

import sys
from collections import defaultdict
from nfa import NFA

def string_nfa(w):
    states = {'q0'}
    alphabet = set(w)
    transitions = defaultdict(lambda: defaultdict(set))
    start_state = 'q0'
    accept_states = {f'q{len(w)}'}

    for i, char in enumerate(w):
        old_state = f'q{i}'
        new_state = f'q{i+1}'
        states.add(new_state)
        transitions[old_state][char].add(new_state)

    return NFA(states, alphabet, transitions, start_state, accept_states)

def main(arguments=sys.argv[1:]):

    w = arguments[0]
    nfa = string_nfa(w)
    nfa.print()

if __name__ == "__main__":
    main()
