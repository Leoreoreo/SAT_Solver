#/usr/bin/env python3

import sys
from collections import defaultdict
from nfa import NFA, read_nfa

def backreference_nfa(k):
    start_state = f"{k}_COPY"  # M2_1_COPY, M1_M2_1_COPY
    alphabet = set()
    transitions = defaultdict(lambda: defaultdict(set))
    states = {f"{k}_COPY"}
    accept_states = {f"{k}_COPY"}
    return NFA(states, alphabet, transitions, start_state, accept_states)
    