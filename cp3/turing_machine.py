#!/usr/bin/env python3

from collections import defaultdict, deque
import sys

class TM:
    def __init__(self, states, alphabet, tape_symbols, transitions, start_state, accept_state, reject_state):
        self.states = states                # Set[str]
        self.alphabet = alphabet            # Set[str]
        self.tape_symbols = tape_symbols 
        self.transitions = transitions      # Dict[str, Dict[str: set[(str, str, str)]]]
                                            # {'q1' : {'0' : {('q2', '_', 'R')}, '1':...}, 'q2':{...}}
        self.start_state = start_state      # str
        self.accept_state = accept_state  # Set[str]
        self.reject_state = reject_state
    
    def print(self):
        print(' '.join(list(self.states)))
        print(' '.join(list(self.alphabet))) 
        print(' '.join(list(self.tape_symbols))) 
        print(self.start_state)
        print(' '.join(list(self.accept_state)))
        print(' '.join(list(self.reject_state)))

        for q, transition in self.transitions.items():
            for symbol, target in transition.items():
                print(f'{q} {symbol} {target[0]} {target[1]} {target[2]}')

def read_TM(file):
    with open(file, 'r') as f:
        lines = f.readlines()

    states = set(lines[0].split())
    alphabet = set(lines[1].split())
    tape_symbols = set(lines[2].split()) 
    start_state = lines[3].strip()
    accept_state = lines[4].strip()
    reject_state = lines[5].strip()

    transitions:dict[str,dict[str,tuple[str, str, str]]] = defaultdict(lambda: defaultdict(tuple))
    for line in lines[6:]:
        if line:
            parts = line.split()
            transitions[parts[0]][parts[1]] = tuple(parts[2:])
    return TM(states, alphabet, tape_symbols, transitions, start_state, accept_state, reject_state)

def match(M, w):
    pass
    # # doing bfs
    # frontier = deque([(M.start_state, 0)])
    # w_len = len(w)
    # graph = {}          # graph := { (q, cur_wd_len): [(last_q, last_wd_len)], }, used this to retrace the path

    # while frontier:
    #     cur_state, cur_wd_len = frontier.popleft()
    #     if (cur_state, cur_wd_len) not in graph:  # create new key in graph
    #         graph[(cur_state, cur_wd_len)] = (None, None)

    #     if cur_wd_len < w_len:
    #         next_symbol = w[cur_wd_len]  # step to new symbol
    #         try:
    #             next_states = M.transitions[cur_state][next_symbol]
    #             for next_state in next_states:
    #                 new_config = (next_state, cur_wd_len + 1)
    #                 if new_config not in graph:  # only consider new (state, wordlen)
    #                     graph[new_config] = (cur_state, cur_wd_len)
    #                     frontier.append(new_config)
    #         except KeyError:
    #             pass
    #     try:
    #         next_states = M.transitions[cur_state]['&']
    #         for next_state in next_states:
    #             new_config = (next_state, cur_wd_len)
    #             if new_config not in graph:  # only consider new (state, wordlen)
    #                 graph[new_config] = (cur_state, cur_wd_len)
    #                 frontier.append(new_config)
    #     except KeyError:
    #         pass

    
    # # print(graph)
    # accepting_configs = [(state, wd_len) for (state, wd_len) in graph.keys() if wd_len == w_len and state in M.accept_states]

    # return len(accepting_configs) > 0


def main(arguments=sys.argv[1:]):
    tm_file = arguments[0]
    tm = read_TM(tm_file)
    tm.print()
    pass

if __name__ == '__main__':
    main()

         