#!/usr/bin/env python3

import sys
import string
import re
import time
from nfa import NFA, read_nfa
from string_nfa import string_nfa
from union_nfa import union_nfa
from concat_nfa import concat_nfa
from star_nfa import star_nfa
from group_nfa import group_nfa
from backreference_nfa import backreference_nfa

U = {chr(i) for i in range(0, 9000)} 
exclude_character = {'⊣', "\\"}

T = U | {'\\k', '\\g<k>'} # note: k should be greater than or equal to 1

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
    ("&", "P"): {"below": Γ, "next": T - {"*"}, "push": ('F', None)},
    ("&", "a"): {"below": Γ, "next": T | {"⊣"}, "push": ('P', 'symbol')},
    ("&", "(E)"): {"below": Γ, "next": T | {"⊣"}, "push": ('P', 'group')},
    ("\\k", "&"): {"below": {"$", "(", "|", "T"}, "next": T | {"⊣"}, "push": ('\\k', None)},
    ("\\g<k>", "&"): {"below": {"$", "(", "|", "T"}, "next": T | {"⊣"}, "push": ('\\g<k>', None)},
    ("&", "\\k"): {"below": Γ, "next": T | {"⊣"}, "push": ('P', 'backref')},
    ("&", "\\g<k>"): {"below": Γ, "next": T | {"⊣"}, "push": ('P', 'backref')},
}

# from CP3wq
def rearrange_group_numbers(s):
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

# convert "ab\1c" into ["a", "b", "\1", "c"]
def create_string_list(s):
    #edge case when s is ""
    if len(s) == 0:
        return []
    index = 0
    string_list = []
    while index < len(s):
        # process the case that start with "\"
        if s[index] == "\\":
            num = ""
            if s[index:index+2] == "\\g":
        # the situation when \g<01>
                if s[index+3] == "0" :
                    return None
                
                index += 3 # the first three characters are \g<
                while s[index].isdigit():
                    num += s[index]
                    index += 1
                index += 1
                string_list.append(f"\\g<{num}>")

            else:
                # the situation when \01
                if s[index+1] == "0":
                    return None
                    
                index += 1
                while index < len(s) and s[index].isdigit():
                    num += s[index]
                    index += 1
                string_list.append(f"\\{num}")

        else:
            string_list.append(s[index])
            index += 1
            

    return string_list

# get the k value from backreference \k or \g<k>
def getK(backreference):
    #edge case when the string is empty string:
    if len(backreference) == 0:
        return 0
    
    # if this is not a backreference, return 0
    if backreference[0] != "\\":
        return 0

    i = 0
    num = ""
    if backreference[:2] == "\\g":       
        i += 3 # the first three characters are \g<
        while backreference[i].isdigit():
            num += backreference[i]
            i += 1
    else:    
        i += 1
        while i < len(backreference) and backreference[i].isdigit():
            num += backreference[i]
            i += 1
    return int(num)


def parser(s):
    input_list = create_string_list(s)
    if input_list == None:
        return False, None, None
    input_list.append("⊣")

    stack_symbol = ["$"]
    stack_str = []
    stack_result = []
    index = 0
    fake_k = 0
    while index < len(input_list):
        # print("stack_symbol is ",stack_symbol)
        # print("stack_str is ", stack_str)
        # print(index)
        #time.sleep(1)
        inputs = ["&", input_list[index]]
        pops = [("&",)]
        if len(stack_symbol) > 3:
            #append tuple, this helps to keep track the number to pop
            pops.append((stack_symbol[-3], stack_symbol[-2], stack_symbol[-1]))  
        if len(stack_symbol) > 2:
            pops.append((stack_symbol[-2], stack_symbol[-1]))
        if len(stack_symbol) > 1:
            pops.append((stack_symbol[-1],))

        reject = True
        found = False
        # check which transition is the correct one, or no transition at all
        for input in inputs:
            for pop in pops:
                k: int
                transitions_input = input
                transitions_pop = "".join(pop)  # convert ("a", "\1", "c") to "a\1c" temporarily
                if transitions_input in Σ:
                    transitions_input = "a"
                if transitions_pop in Σ:
                    transitions_pop = "a"
                if getK(transitions_input):
                    k = getK(transitions_input)
                    transitions_input = "\\g<k>" #faking the input to get the correct transition
                if getK(transitions_pop):
                    k = getK(transitions_pop) # k will be used later
                    transitions_pop = "\\g<k>" 

                if not transitions.get((transitions_input, transitions_pop), None):
                    continue

                # print(transitions_input, transitions_pop)

                next_symbol = input_list[index]
                if getK(input_list[index]):
                    next_symbol = "\\g<k>"  # faking the backreference so that it matches the key in the table

                # print(stack_symbol[-1 if transitions_pop == "&" else -len(pop) - 1] in transitions[(transitions_input, transitions_pop)]["below"])
                # print("input_list[index] is ", input_list[index])
                # print("next symbol is ", next_symbol)
                # print(next_symbol in transitions[(transitions_input, transitions_pop)]["next"])
                

                if stack_symbol[-1 if transitions_pop == "&" else -len(pop) - 1] in \
                        transitions[(transitions_input, transitions_pop)]["below"] and next_symbol in \
                        transitions[(transitions_input, transitions_pop)]["next"]:
                    
                    #print("correct transitions: ", transitions_input, transitions_pop)

                    reject = False
                    if transitions_input != "&":
                        index += 1
                    if transitions_pop != "&":
                        for _ in range(len(pop)):
                            stack_symbol.pop()

                    if transitions_input in Σ:
                        stack_symbol.append(input)
                    elif getK(input): # this indicates the input is a backreference, instead of the pop symbol
                        stack_symbol.append(f"\\g<{k}>")
                    else:
                        stack_symbol.append(transitions[(transitions_input, transitions_pop)]["push"][0])

                    subscript = transitions[(transitions_input, transitions_pop)]["push"][1]
                    if subscript:
                        if subscript == "union":
                            beta = stack_str.pop()
                            alpha = stack_str.pop()
                            stack_str.append(f"union({alpha},{beta})")
                            beta = stack_result.pop()
                            alpha = stack_result.pop()
                            stack_result.append(union_nfa(alpha, beta))
                        elif subscript == "concat":
                            beta = stack_str.pop()
                            alpha = stack_str.pop()
                            stack_str.append(f"concat({alpha},{beta})")
                            beta = stack_result.pop()
                            alpha = stack_result.pop()
                            stack_result.append(concat_nfa(alpha, beta))
                        elif subscript == "epsilon":
                            stack_str.append("epsilon()")
                            stack_result.append(string_nfa(""))
                        elif subscript == "star":
                            alpha = stack_str.pop()
                            stack_str.append(f"star({alpha})")
                            alpha = stack_result.pop()
                            stack_result.append(star_nfa(alpha))
                        elif subscript == "group":
                            fake_k += 1
                            alpha = stack_str.pop()
                            stack_str.append(f"group({fake_k},{alpha})")
                            alpha = stack_result.pop()
                            stack_result.append(group_nfa(alpha, fake_k))
                        elif subscript == "backref":
                            stack_str.append(f"backref({k})")
                            stack_result.append(backreference_nfa(k))
                        else:
                            symbol = "".join(pop)
                            stack_str.append(f"symbol(\"{symbol}\")")
                            stack_result.append(string_nfa(symbol))
                    found = True
                    break
                else:
                    continue
            if found:
                break
            

        if reject:
            return False, None, None

        if input_list[index] == "⊣" and len(stack_symbol) == 2 and stack_symbol[0] == "$" and stack_symbol[1] == "E":
            return True, stack_result[0], rearrange_group_numbers(stack_str[0]) 
            # res = stack_result[0]
            # i = 1
            # cur_num = 1
            # while (i < len(res)):
            #     if res[i] == ',' and res[i-1] == '(':
            #         res = res[:i] + str(cur_num) + res[i:]
            #         cur_num += 1
            #     i += 1
            # return True, res


def main(arguments=sys.argv[1:]):
    # result = create_string_list(arguments[0])
    # for i in result:
    #     print(i)
    accept, nfa, _ = parser(arguments[0])
    if accept:
        nfa.print()

if __name__ == '__main__':
    main()