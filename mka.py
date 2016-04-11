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
COMM_REX = '#.*'
COMA_REX = ','
WHTC_REX = '\s+'
COMB_REX = '[\s+,]'
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
    try :       # not working still on stderr
        args = parser.parse_args()
    except :
        exit(ARGS_ERR)
    if args.find_non_finishing == args.minimize and args.minimize == True :
        print_err("Wrong combination of arguments", ARGS_ERR)
    if args.help : # fix help
        print(parser.format_help())
        exit(PROG_OK)
    return args
#------------------------------------------------------------------------------
def read_input(input_file):
    if input_file != sys.stdin :
        try:
            with open(input_file,'r') as file :
                input_file = file.read()
        except:
            print_err("Can not open file", READ_ERR)
    else:
        input_file = input_file.read()
    # Replacing any comments with space
    input_file=re.sub(COMM_REX,SP,input_file)
    return input_file
#------------------------------------------------------------------------------
def parse_rules(rules,states):
    output = OrderedDict()
    for rule in rules:
        state = ""
        part = rule.split('->') # fix bad rule
        if (len(part[0]) == len(rule)):
            print_err("Invalid rule in rules",FORM_ERR) 
        left = part[0]
        dest = part[1]
        for i in range(0,len(left)):
            state += left[i]
            if state in states:               
                alpha = left[i+1:]
                output.update({state : {alpha : dest}})
                break
            if (len(state)==len(left)):
                print_err("Invalid rule in rules",FORM_ERR)    
    #print (output)
    return output
#------------------------------------------------------------------------------
def cut(tmp,rex,rep,split):
    tmp = re.sub(COMB_REX,SP,tmp) # maybe there
    tmp = tmp.split()
    return tmp
#------------------------------------------------------------------------------
def scan(string,separator=COMA_REX):
    result = []
    #separator = COMB_REX # :-( Dont want to !!!!
    string = "({start,finish,banany,jablka},{'a','b','e','c','e','d','a'},{start'c'->finish},start,{finish})"
    i = 0

    part = re.sub(WHTC_REX,' ',string)
    REX = r'\s*\((\s*\{(.+?)\}\s*\,)(\s*\{(.+?)\}\s*\,)(\s*\{(.+?)\}\s*\,)(.*)\,(\s*\{(.+?)\}\s*)\)\s*'
    part = re.match(REX,part)
    # all states
    #print (part.group(2))
    result.append(cut(part.group(2),WHTC_REX,EMPTY,separator))
    # alphabet
    #print (part.group(4))
    result.append(cut(part.group(4),WHTC_REX,EMPTY,separator))
    # all rules
    #print (part.group(6))    
    result.append(cut(part.group(6),WHTC_REX,EMPTY,separator))
    # starting state
    #print (part.group(7))
    result.append(cut(part.group(7),WHTC_REX,EMPTY,separator))
    # all finishing states
    #print (part.group(9))
    result.append(cut(part.group(9),WHTC_REX,EMPTY,separator))

    result[RULES] = parse_rules(result[RULES],result[STATES])
    #print (result)
    return result
#------------------------------------------------------------------------------
def empty_alphabet(alphabet):
    chars = ""
    for char in alphabet:
        chars += char
    return (len(chars) == 0)
#------------------------------------------------------------------------------
def invalid_rules(rules,states,alphabet): 
    for r in rules:
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
    if (empty_alphabet(M[ALPHA])):
        return False
    if (invalid_rules(M[RULES],M[STATES],M[ALPHA])):
        return False
    if (not in_states(M[START],M[STATES])):
        return False
    if (not in_states(M[FINISH],M[STATES])):
        return False
    return True
#------------------------------------------------------------------------------
def is_dska(M): #TODO 
# Pokud vstup nereprezentuje dobře specifikovaný konečný automat, skončí skript
# s chybou a vrátí návratový kód 62
    return True
#------------------------------------------------------------------------------
def print_err(msg,code):
    print(msg,file=sys.stderr)
    exit(code)
#------------------------------------------------------------------------------
#-----------------------------MAIN-FUNCTION------------------------------------
def main():
    args = check_args()
    M = scan(read_input(args.input)) 
    if (not valid_format(M)):
        print_err("Input file is not in valid format", FORM_ERR)
    if (not True):
        pass

    for item in M:
        print ("-----")
        print (item) 
    print ("-----")
    return PROG_OK
#------------------------------------------------------------------------------
if __name__ == "__main__":
    exit(main())    
#------------------------------------------------------------------------------

# -f, --find-non-finishing -> hledá neukončující stav zadaného dobře specifikovaného
# konečného automatu (automat se nevypisuje). Nalezne-li jej, bez odřádkování jej vypíše na
# výstup; jinak vypíše pouze číslici 0. (Před hledáním se provede validace na dobrou specifiko-
# vanost automatu.) Parametr nelze kombinovat s parametrem -m (resp. --minimize).

# -m, --minimize -> provede minimalizaci dobře specifikovaného konečného automatu (viz algo-
# ritmus IFJ, přednáška 11, snímek 23/35). Parametr nelze kombinovat s parametrem -f (resp.
# --find-non-finishing).

# -i, --case-insensitive -> nebude brán ohled na velikost znaků při porovnávání symbolů či
# stavů (tj. a = A, ahoj = AhOj nebo A b = a B); ve výstupu potom budou všechna velká písmena
# převedena na malá.

# bonus 
# -w, --white-char
# -r, --rules-only
# --analyze-string="retezec"
# --wsfa