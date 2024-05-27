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
        print("states are ", ' '.join(list(self.states)))
        print("alphabet is ", ' '.join(list(self.alphabet)))
        print("start state is ", self.start_state)
        print("accept states are ",' '.join(list(self.accept_states)))
        print("transitions are:------------------------------------------")
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

# get the k from k_OPEN or k_CLOSE or k_COPY
def getK(state):
    num = ""
    j = 0
    if state[-5:] == "_OPEN":
        j = len(state) - 5 - 1
    elif state[-6:] == "_CLOSE":
        j = len(state) - 6 - 1
    else:
        j = len(state) - 5 - 1
    # group_stack.append(num)
    # stack_dic[num] = ''     # create new key & overwrite original

    while j >= 0 and state[j].isdigit():  # for example, 16_OPEN
        num = state[j] + num
        j -= 1

    return int(num)


# real table: {fake: real}, use when I know eg. fake: (0, 2) -> real: (0, 2)
def match(M, w, real_table):
    # doing ***DFS***
    #M.print()
    frontier = [(M.start_state, 0, (1,), ((None, None),))]  # current state, current index, backreference keys, backreference values. Use tuple because tuple is hashable
    w_len = len(w)
    backreference_table = {}  # for example, {1: (0, 2)}
    graph = {}          # graph := { (q, cur_wd_len): [(last_q, last_wd_len)], }, used this to retrace the path

    while frontier:
        #print("----------------------------------------------------------------------")
        cur_state, cur_wd_len, keys, values = frontier.pop()
        if (cur_state, cur_wd_len, keys, values) not in graph:  # create new key in graph
            graph[(cur_state, cur_wd_len, keys, values)] = (None, None, None, None)
        
        #print("cur_state and cur_wd_len are ", cur_state, cur_wd_len)
        if len(cur_state) > 5 and cur_state[-5:] == '_OPEN':
            k = getK(cur_state)
            backreference_table[real_table[k]] = (cur_wd_len, None)
        
        if len(cur_state) > 6 and cur_state[-6:] == '_CLOSE':
            k = getK(cur_state)
            start = backreference_table[real_table[k]][0]
            backreference_table[real_table[k]] = (start, cur_wd_len)  # we get gk for reference k
        
        #print("table is ", backreference_table)

        if cur_wd_len < w_len:
            next_symbol = w[cur_wd_len]  # step to new symbol
            #print("next_symbol is ", next_symbol)
            try:
                next_states = M.transitions[cur_state][next_symbol]
                #print("next states are ", next_states)
                for next_state in next_states:
                    #print("next state is", next_state)
                    new_config = (next_state, cur_wd_len + 1, tuple(backreference_table.keys()), tuple(backreference_table.values()))
                    #print("new config is ", new_config)
                    #print("graph is ", graph)
                    if new_config not in graph:  # only consider new (state, wordlen)
                        graph[new_config] = (cur_state, cur_wd_len, keys, values)
                        frontier.append(new_config)
            except KeyError:
                pass
        try:
            next_states = M.transitions[cur_state]['&']
            for next_state in next_states:
                #print("next state when epsilon is", next_state)
                if len(next_state) > 5 and next_state[-5:] == "_COPY":
                    k = getK(next_state)
                    # check if w[i+|gk|] == gk
                    gk_range = backreference_table.get(k, None)
                    # gk_range may be not initialized yet. This can cause error
                    if gk_range == None:
                        continue
                    if gk_range[0] == None or gk_range[1] == None:
                        continue
                    if cur_wd_len + gk_range[1] - gk_range[0] <= len(w) and \
                        w[cur_wd_len: cur_wd_len + gk_range[1] - gk_range[0]] == w[gk_range[0]:gk_range[1]]:
                        #print(f"they are equal: {w[cur_wd_len: cur_wd_len + gk_range[1] - gk_range[0]]} and {w[gk_range[0]:gk_range[1]]}")
                        #print(cur_wd_len, gk_range)
                        new_config = (next_state, cur_wd_len + gk_range[1] - gk_range[0], tuple(backreference_table.keys()), tuple(backreference_table.values()))
                        if new_config not in graph:  # only consider new (state, wordlen)
                            graph[new_config] = (cur_state, cur_wd_len, keys, values)
                            frontier.append(new_config)
                else:
                    new_config = (next_state, cur_wd_len, tuple(backreference_table.keys()), tuple(backreference_table.values()))
                    #print("the string is not equal (epsilon), the new config is ", new_config)
                    if new_config not in graph:  # only consider new (state, wordlen)
                        graph[new_config] = (cur_state, cur_wd_len, keys, values)
                        frontier.append(new_config)
        except KeyError:
            pass

    
    
    # print(graph)
    accepting_configs = [(state, wd_len, k, v) for (state, wd_len, k, v) in graph.keys() if wd_len == w_len and state in M.accept_states]
    # print(graph)
    # print(len(accepting_configs))

    return len(accepting_configs) > 0



# this can return the path to you. not used in CP4
# def group_match(M, w):
#     # doing bfs
#     frontier = deque([(M.start_state, 0)])
#     w_len = len(w)
#     graph = {}          # graph := { (q, cur_wd_len): [(last_q, last_wd_len)], }, used this to retrace the path

#     while frontier:
#         cur_state, cur_wd_len = frontier.popleft()
#         if (cur_state, cur_wd_len) not in graph:  # create new key in graph
#             graph[(cur_state, cur_wd_len)] = (None, None)

#         if cur_wd_len < w_len:
#             next_symbol = w[cur_wd_len]  # step to new symbol
#             try:
#                 next_states = M.transitions[cur_state][next_symbol]
#                 for next_state in next_states:
#                     new_config = (next_state, cur_wd_len + 1)
#                     if new_config not in graph:  # only consider new (state, wordlen)
#                         graph[new_config] = (cur_state, cur_wd_len)
#                         frontier.append(new_config)
#             except KeyError:
#                 pass
#         try:
#             next_states = M.transitions[cur_state]['&']
#             for next_state in next_states:
#                 new_config = (next_state, cur_wd_len)
#                 if new_config not in graph:  # only consider new (state, wordlen)
#                     graph[new_config] = (cur_state, cur_wd_len)
#                     frontier.append(new_config)
#         except KeyError:
#             pass

#     accepting_configs = [(state, wd_len) for (state, wd_len) in graph.keys() if wd_len == w_len and state in M.accept_states]
#     if len(accepting_configs) > 0:  # word accepted
#         # Reconstruct path
#         path = []
#         accepting_config = accepting_configs[0]
#         while accepting_config[0]:
#             path.append(accepting_config)
#             accepting_config = graph.get(accepting_config, [])

#         return True, path[::-1]
#     else:
#         return False, []
        

         