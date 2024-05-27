#!/usr/bin/env python3

from collections import defaultdict, deque

class NFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states                # Set[str]
        self.alphabet = alphabet            # Set[str]
        self.transitions = transitions      # Dict[str, Dict[str, set[str]]]
        self.start_state = start_state      # str
        self.accept_states = accept_states  # Set[str]
    
    def print(self):
        print(' '.join(list(self.states)))
        print(' '.join(list(self.alphabet)))
        print(self.start_state)
        print(' '.join(list(self.accept_states)))
        for q, transition in self.transitions.items():
            for symbol, target in transition.items():
                for accept in target:
                    print(f'{q} {symbol} {accept}')

def read_nfa(file):
    with open(file, 'r') as f:
        lines = f.readlines()

    states = set(lines[0].split())
    alphabet = set(lines[1].split())
    start_state = lines[2].strip()
    accept_states = set(lines[3].split())

    transitions:dict[str,dict[str,list[str]]] = defaultdict(lambda: defaultdict(set))
    for line in lines[4:]:
        parts = line.split()
        transitions[parts[0]][parts[1]].add(parts[2])

    return NFA(states, alphabet, transitions, start_state, accept_states)

def match(M, w):
    # doing bfs
    frontier = deque([(M.start_state, 0)])
    w_len = len(w)
    graph = {}          # graph := { (q, cur_wd_len): [(last_q, last_wd_len)], }, used this to retrace the path

    while frontier:
        cur_state, cur_wd_len = frontier.popleft()
        if (cur_state, cur_wd_len) not in graph:  # create new key in graph
            graph[(cur_state, cur_wd_len)] = (None, None)

        if cur_wd_len < w_len:
            next_symbol = w[cur_wd_len]  # step to new symbol
            try:
                next_states = M.transitions[cur_state][next_symbol]
                for next_state in next_states:
                    new_config = (next_state, cur_wd_len + 1)
                    if new_config not in graph:  # only consider new (state, wordlen)
                        graph[new_config] = (cur_state, cur_wd_len)
                        frontier.append(new_config)
            except KeyError:
                pass
        try:
            next_states = M.transitions[cur_state]['&']
            for next_state in next_states:
                new_config = (next_state, cur_wd_len)
                if new_config not in graph:  # only consider new (state, wordlen)
                    graph[new_config] = (cur_state, cur_wd_len)
                    frontier.append(new_config)
        except KeyError:
            pass

    
    # print(graph)
    accepting_configs = [(state, wd_len) for (state, wd_len) in graph.keys() if wd_len == w_len and state in M.accept_states]

    return len(accepting_configs) > 0
        