# Project Overview

## CP1: NFA Simulator

Using graph algorithm to simulate NFAs.

Input: NFA file, target string

Output: Accept/Reject, path (if accepted)

### Example:

<img width="495" alt="截屏2024-05-27 16 23 22" src="https://github.com/Leoreoreo/SAT_Solver/assets/87118867/f676fc05-795b-45ec-a2c5-8af60de77fda">
<img width="232" alt="截屏2024-05-27 16 24 23" src="https://github.com/Leoreoreo/SAT_Solver/assets/87118867/a9f1abd3-888a-4675-9ac6-8a5bd12a1fcb">

### Usage:

<img width="281" alt="截屏2024-05-27 16 26 11" src="https://github.com/Leoreoreo/SAT_Solver/assets/87118867/c3df2bfa-680e-4a22-a875-1b55b0347545">

## CP2: Regular Expression Simulator

Parse regular expressions (only with '(', ')', '|', '*') with PDA, construct a tree. Then convert the tree into NFA.

Input: regexp, lines of strings

Output: strings that match the regexp

### Example: 

<img width="434" alt="截屏2024-05-27 16 37 13" src="https://github.com/Leoreoreo/SAT_Solver/assets/87118867/baf605a0-a3cf-4ef6-87bc-3b058164b2bb">

<img width="599" alt="截屏2024-05-27 16 38 48" src="https://github.com/Leoreoreo/SAT_Solver/assets/87118867/6d493d3e-23a1-4d88-a5c4-3b3830733d20">


## CP3: Sed Simulator

Add group to the regexp parser to simulate the mini-sed (msed).
Prove msed is Turing-Complete by implementing a translation from Turing machines to msed.

<img width="414" alt="截屏2024-05-28 12 02 40" src="https://github.com/Leoreoreo/SAT_Solver/assets/87118867/cfe9f137-2a6e-4fc6-8da5-75579e475fa6">

### Example: 

<img width="393" alt="截屏2024-05-28 12 24 43" src="https://github.com/Leoreoreo/SAT_Solver/assets/87118867/7c5160e3-df34-4fe6-9558-abb0e748c938">

### Usage:

<img width="563" alt="截屏2024-05-28 12 03 58" src="https://github.com/Leoreoreo/SAT_Solver/assets/87118867/08d69811-7f75-4b67-8a84-decde98bf4ce">

## CP4: Regular Expression Matcher with Backreferences

Add backreference to the regexp parser.

<img width="499" alt="截屏2024-05-28 12 28 30" src="https://github.com/Leoreoreo/SAT_Solver/assets/87118867/fdb0dc20-d172-4bb5-8be7-c5638ec2d440">
<img width="321" alt="截屏2024-05-28 12 29 12" src="https://github.com/Leoreoreo/SAT_Solver/assets/87118867/6dc495dc-0a03-407b-a65e-17737159eddf">

Prove regexp with backreferences is NP-Complete by reducing it into SAT problem in polynomial time

### Usage:

<img width="257" alt="截屏2024-05-28 12 32 41" src="https://github.com/Leoreoreo/SAT_Solver/assets/87118867/a1a1681e-9fc8-4099-9024-691ef531f169">


## Language and Libraries
- Language: Python
- Standard Libraries Used: All standard libraries except `re`

