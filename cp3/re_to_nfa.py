#!/usr/bin/env python3

import sys
import string

from nfa import NFA, read_nfa
from string_nfa import string_nfa
from union_nfa import union_nfa
from concat_nfa import concat_nfa
from star_nfa import star_nfa
from group_nfa import group_nfa


U = {chr(i) for i in range(0, 9000)} 
exclude_character = '⊣'
T = U - {exclude_character}
exclude_set = {'(', ')', '*', '|', '\\'}
Σ = set(string.ascii_lowercase) | set(string.digits) | {'[', '_', ']', '^', '#'}
V = {"E", "M", "T", "F", "P"}
Γ = V | T | {"$"}

transitions = {
    ("a", "&"): {"below": {"$", "(", "|", "T"}, "next": T | {"⊣"}, "push": ("a", None)},
    ("(", "&"): {"below": {"$", "(", "|", "T"}, "next": T | {"⊣"}, "push": ("(", None)},
    (")", "&"): {"below": {"E"}, "next": T | {"⊣"}, "push": (")", None)},
    ("|", "&"): {"below": {"E"}, "next": T | {"⊣"}, "push": ("|", None)},
    ("*", "&"): {"below": {"P"}, "next": T | {"⊣"}, "push": ("*", None)},
    ("&", "E|M"): {"below": Γ, "next": T | {"⊣"}, "push": ("E", "union")},
    ("&", "M"): {"below": {"$", "("}, "next": T | {"⊣"}, "push": ("E", None)},
    ("&", "&"): {"below": {"$", "(", "|"}, "next": {"|", ")", "⊣"}, "push": ("M", "epsilon")},
    ("&", "T"): {"below": Γ, "next": {'|', ')', '⊣'}, "push": ('M', None)},
    ("&", "TF"): {"below": Γ, "next": T | {"⊣"}, "push": ('T', 'concat')},
    ("&", "F"): {"below": {"$", "(", "|"}, "next": T | {"⊣"}, "push": ('T', None)},
    ("&", "P*"): {"below": Γ, "next": T | {"⊣"}, "push": ('F', 'star')},
    ("&", "P"): {"below": Γ, "next": U - {"*"}, "push": ('F', None)},
    ("&", "a"): {"below": Γ, "next": T | {"⊣"}, "push": ('P', 'symbol')},
    ("&", "(E)"): {"below": Γ, "next": T | {"⊣"}, "push": ('P', 'group')},
}

def rearrange_group_numbers(s, group_num):
    real_k_table = {}
    i = 0
    cur_num = 0
    while (i + 7 < len(s)):
        if s[i:i+6] == "group(":
            num = ""
            i += 6
            while s[i].isdigit():
                num += s[i]
                i += 1
            real_k_table[int(num)] = cur_num + 1
            cur_num += 1
        else:
            i += 1

    return real_k_table

def re_to_nfa(s):
    s = s + "⊣"
    stack_symbol = ["$"]
    
    stack_str = []
    fake_k = 0
    # stack_result should now be list[nfa]
    stack_result = []
    index = 0
    while index < len(s):
        inputs = ["&", s[index]]
        pops = ["&"]
        if len(stack_symbol) > 3:
            pops.append(stack_symbol[-3] + stack_symbol[-2] + stack_symbol[-1])
        if len(stack_symbol) > 2:
            pops.append(stack_symbol[-2] + stack_symbol[-1])
        if len(stack_symbol) > 1:
            pops.append(stack_symbol[-1])

        reject = True
        found = False
        # check which transition is the correct one, or no transition at all
        for input in inputs:
            for pop in pops:
                transitions_input = input
                transitions_pop = pop
                if transitions_input in Σ:
                    transitions_input = "a"
                if transitions_pop in Σ:
                    transitions_pop = "a"

                if not transitions.get((transitions_input, transitions_pop), None):
                    continue

                if stack_symbol[-1 if transitions_pop == "&" else -len(transitions_pop) - 1] in \
                        transitions[(transitions_input, transitions_pop)]["below"] and s[index] in \
                        transitions[(transitions_input, transitions_pop)]["next"]:
                    reject = False
                    if transitions_input != "&":
                        index += 1
                    if transitions_pop != "&":
                        for _ in range(len(transitions_pop)):
                            stack_symbol.pop()

                    if transitions_input in Σ:
                        stack_symbol += input
                    else:
                        stack_symbol.append(transitions[(transitions_input, transitions_pop)]["push"][0])

                    subscript = transitions[(transitions_input, transitions_pop)]["push"][1]
                    if subscript:
                        if subscript == "union":
                            beta = stack_result.pop()
                            alpha = stack_result.pop()
                            stack_result.append(union_nfa(alpha, beta))
                            beta = stack_str.pop()
                            alpha = stack_str.pop()
                            stack_str.append(f"union({alpha},{beta})")
                        elif subscript == "concat":
                            beta = stack_result.pop()
                            alpha = stack_result.pop()
                            stack_result.append(concat_nfa(alpha, beta))
                            beta = stack_str.pop()
                            alpha = stack_str.pop()
                            stack_str.append(f"concat({alpha},{beta})")
                        elif subscript == "epsilon":
                            stack_result.append(string_nfa('')) 
                            stack_str.append("epsilon()")
                        elif subscript == "star":
                            alpha = stack_result.pop()
                            stack_result.append(star_nfa(alpha))
                            alpha = stack_str.pop()
                            stack_str.append(f"star({alpha})")
                        elif subscript == "group":
                            fake_k += 1
                            alpha = stack_result.pop()
                            stack_result.append(group_nfa(alpha, fake_k))
                            alpha = stack_str.pop()
                            stack_str.append(f"group({fake_k},{alpha})")
                        else:
                            stack_result.append(string_nfa(pop))
                            stack_str.append(f"symbol(\"{pop}\")")
                    found = True
                    break
                else:
                    continue
            if found:
                break

        if reject:
            return False, None, None

        if s[index] == "⊣" and len(stack_symbol) == 2 and stack_symbol[0] == "$" and stack_symbol[1] == "E":
            return True, stack_result[0], rearrange_group_numbers(stack_str[0], fake_k)  # return the accept, nfa result, and real table


def main(arguments=sys.argv[1:]):
    accept, result, _ = re_to_nfa(arguments[0])
    if accept:
        result.print()
    else:
        print('reject')

if __name__ == '__main__':
    main()