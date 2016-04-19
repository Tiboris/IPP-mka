#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#MKA:xdudla00
#------------------------------------------------------------------------------
import re                           # to searching by regex
import os                           # to work with filesystem
import sys                          # to get arguments
import argparse                     # to parse arguments
from collections import OrderedDict # 
#------------------------------------------------------------------------------
STATES   = 0
ALPHA    = 1 
RULES    = 2
START    = 3
FINISH   = 4
PROG_OK  = 0
ARGS_ERR = 1
READ_ERR = 2
WRIT_ERR = 3
FORM_ERR = 60
SEMS_ERR = 61
DSKA_ERR = 62
COMM_REX = r'#.*'
COMA     = ','
WHTC_REX = r'\s+'
COMB_REX = r'[\s+,]'
EMPTY    = ''
REX = r'\s*\((\s*\{(.+?)\}\s*\,)(\s*\{(.+?)\}\s*\,)(\s*\{(.+?)\}\s*\,)(.*)\,(\s*\{(.+?)\}\s*)\)\s*'
SP       = ' '
#------------------------------FUNCTIONS---------------------------------------
#------------------------------------------------------------------------------
def check_args(): # TODO fix duplicated params
    parser = argparse.ArgumentParser(add_help=False, 
                description='Script for processing finite state machines')
    parser.add_argument('--help', help='show this help message and exit', 
                required=False, action="store_true")
    parser.add_argument('--input', required=False,
                help='if not set it takes STDIN', 
                default=sys.stdin)
    parser.add_argument('--output', required=False,
                help='if not set output will be at STDOUT', 
                default=sys.stdout)
    parser.add_argument('-m','--minimize', required=False,
                help='minimizes finite state machine', 
                action="store_true")
    parser.add_argument('-f','--find-non-finishing', required=False,
                help='find states and prints them otherwise \'0\'',
                action="store_true")
    parser.add_argument('-i','--case-insensitive', required=False, 
                help='ignoring input states strings case', 
                action="store_true")
    parser.add_argument('-r','--rules-only', required=False, 
                help='input is in format rules only', 
                action="store_true")
    parser.add_argument('--analyse-string', required=False, 
                help='analysing string passed as parameter')
    try :   # not working still on stderr
        args = parser.parse_args()
    except :
        exit(ARGS_ERR)
    if args.find_non_finishing == args.minimize and args.minimize == True :
        print_err("Wrong combination of arguments", ARGS_ERR)
    if (args.help):
        if (len(sys.argv) == 2):
            print(parser.format_help())
            exit(PROG_OK)
        else :
            print_err("Wrong combination of arguments", ARGS_ERR)
    return args
#------------------------------------------------------------------------------
def read_input(input_file,case_insensitive):
    if (input_file != sys.stdin):
        try:
            with open(input_file,'r') as file:
                input_file = file.read()
        except:
            print_err("Can not open file", READ_ERR)
    else:
        input_file = input_file.read()
    # Replacing any comments with space
    input_file = re.sub(COMM_REX,SP,input_file)
    if case_insensitive:
        return input_file.lower()
    return input_file
#------------------------------------------------------------------------------
def prt(M): # to delete
    A=M#[RULES]
    for item in A:
        print ("-----")
        print (item) #(item)#
    print ("-----")
#------------------------------------------------------------------------------
def parse_rules(M,rules_only=False):
    output = OrderedDict()
    if (rules_only):
        rules = M# TODO if rules only
        print(rules)
    else :
        rules = M[RULES] 
    for rule in rules:
        part = rule.split('->') # fix bad rule
        if (len(part[0]) == len(rule)):
            print_err("Invalid rule in rules",FORM_ERR) 
        left = part[0]
        dest = part[1]
        state = left[0:-1]
        alph = left[-1]  
        if (len(state) * len(alph) * len(dest) == 0):
            print_err("Invalid rule in rules",FORM_ERR)
        # hack
        alph = xchange(alph)
        if alph not in M[ALPHA]:
            print_err("Invalid terminal in rules",SEMS_ERR)
        if state not in M[STATES]:
            print_err("Invalid state in rules",SEMS_ERR)
        if dest not in M[STATES]:
            print_err("Invalid state in rules",SEMS_ERR)
        if state in output:
            if alph in output[state]:
                print_err("Autoamata is not deterministic",DSKA_ERR)
            output[state].update({alph : dest})
        else:
            output.update({state : {alph : dest}})                      
    return output
#------------------------------------------------------------------------------
def xchange(char):
    if ord(char) == 172:
        return ' '  #32
    if ord(char) == 174:
        return ','  #34
    return char
#------------------------------------------------------------------------------
def convert(string,hack=False):
    output = ord(string[1])
    if hack:
        for char in range(0,len(string)):
            string[char]=xchange(string[char])
        return string
    return output
#------------------------------------------------------------------------------
def scan(string,separator=COMA,rules_only=False):
    i = 0 

    if (rules_only):
        m_start = string[i]
        m_end = "\0"
        b_start = string[i]
        b_end = '\0'
        component = 3
    else:
        m_start = '('
        m_end = ')'
        b_start = '{'
        b_end = '}'
        component = 1
    result = []
    hack = False

    #string = "({start,finish,banany,jablka},{'a',',','b','e','c','e','d','a'},{start','->finish},start,{finish})"
    while((i < len(string)) and (component < 6)):
        if (string[i] == m_start) :
            if (not rules_only):
                i += 1
            while ((i < len(string)) and (string[i] != m_end)):
                if (component == 4):
                    tmp = ""
                    while (re.match(separator,string[i]) == None):
                        tmp += string[i]
                        i += 1
                    tmp = re.sub(WHTC_REX,'',tmp)
                    tmp = tmp.split(separator)
                    result.append(tmp)
                if (string[i] == b_start):  
                    if (not rules_only):
                        i += 1
                    tmp = ""
                    while ((i < len(string)) and (string[i] != b_end) ): # problem with space in ->
                    ##################################################
                        if ((component == 3) and (string[i] == '>')):
                            if ((i==0) or (string[i-1] != '-')):
                                return None
                        if (string[i]=='\''):
                            char = ""
                            for x in range(0,3):
                                if ((x == 2) and (string[i]!= '\'')):
                                    if string[i-1] == '\'':
                                        print_err("Autoamata is not deterministic",DSKA_ERR)
                                    print_err("Input File is not in valid format", FORM_ERR)
                                char += string[i]
                                i += 1
                            char = convert(char)
                            # hack ','
                            if (char == 44):
                                hack = True
                                char = 174
                            # hack ' '
                            if (char == 32):
                                hack = True
                                char = 172
                            # jump over ''''
                            if (char == 39) and (string[i]!='\''):
                                print_err("Input file is not in valid Format", FORM_ERR)
                            elif (char == 39):
                                i += 1 #may be problem, will see
                            char = chr(char)
                            tmp += char
                        elif (re.match(WHTC_REX,string[i]) != None):
                            i += 1
                        else:
                            tmp += string[i]
                            i += 1
                    tmp = tmp.split(separator)
                    result.append(tmp)
                    i += 1
                elif (re.match(WHTC_REX,string[i]) != None):
                    i += 1
                elif (re.match(separator,string[i]) != None):
                    component += 1
                    i += 1
                else :
                    return None  
            i += 1
        elif( re.match(WHTC_REX,string[i]) != None):
            i += 1
        else :
            return None 
    if (component != 5 and not rules_only):
        return None
    if hack:
        result[ALPHA] = convert(result[ALPHA],hack)
    if rules_only:
        result = parse_rules(result[0],True)
    else :
        result[RULES] = parse_rules(result)
    return result
#------------------------------------------------------------------------------
def size_alphabet(alphabet):
    chars = ""
    for char in alphabet:
        if char in chars:
            continue
        chars += char    
    return len(chars)
#------------------------------------------------------------------------------
def invalid_rules(rules,states,alphabet): 
    for r in rules:
        if (r not in states):
            return True
        rule = rules[r]
        for a in rule:
            if (a not in alphabet):
                return True
            if (rule[a] not in states):
                return True
    return False
#------------------------------------------------------------------------------
def in_states(to_search,all_states): 
    for q in to_search:
        if (q not in all_states):
            return False
    return True
#------------------------------------------------------------------------------
def valid_format(M):
    if (M == None):
        return False
    if (size_alphabet(M[ALPHA]) == 0):
        return False
    if (invalid_rules(M[RULES],M[STATES],M[ALPHA])):
        return False
    if (not in_states(M[START],M[STATES])):
        return False
    if (not in_states(M[FINISH],M[STATES])):
        return False
    return True
#------------------------------------------------------------------------------
def size_of_alph(alphabet):
    for c in alphabet:
        pass
#------------------------------------------------------------------------------
def is_dska(M,non_fin): #TODO 

    rules = M[RULES]
    accessible = [M[START]]
    candidates = []
    non_finishing = []
    alph_size = size_alphabet(M[ALPHA])
    for from_state in rules:
        rule = rules[from_state]
        for by in rule:
            to_state = rule[by]
            #print (from_state,by,to_state)
            if (to_state != from_state):
                accessible.append(to_state)
            else:
                candidates.append(to_state)
    for state in M[STATES]:
        count = 0
        if (state not in accessible):
            return False
        for item in candidates:
            if (item == state) :
                count+=1
        if (count == alph_size):
            non_finishing.append(state)
    if (len(non_finishing) > 1):
        return True
    if non_fin :
        #vypis na vystup
        if len(non_finishing) == 1:
            print(non_finishing[0])
        else:
            print(0)
    return True
#------------------------------------------------------------------------------
def print_err(msg,code):
    print(msg,file=sys.stderr)
    exit(code)
#------------------------------------------------------------------------------
#-----------------------------MAIN-FUNCTION------------------------------------
def main():
    args = check_args()

    if not args.rules_only:
        M = scan(read_input(args.input, args.case_insensitive)) 
    else :
        M = scan(read_input(args.input, args.case_insensitive),COMA,args.rules_only)
    if (not valid_format(M)): # here argument for rules only
        print_err("Input file is not in valid format", FORM_ERR)
    if (not is_dska(M,args.find_non_finishing)):
        print_err("Autoamata is not deterministic",DSKA_ERR)
    prt(M)

    return PROG_OK
#------------------------------------------------------------------------------
if __name__ == "__main__":
    exit(main())    
#------------------------------------------------------------------------------