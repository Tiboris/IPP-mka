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
def read_input(input_file,rules=False):
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
    if (rules):
        input_file = input_file.split(COMA)
    return input_file
#------------------------------------------------------------------------------
def prt(M):
    A=M[RULES]
    for item in A:
        print ("-----")
        print (A[item]) 
    print ("-----")
#------------------------------------------------------------------------------
def parse_rules(rules,states):
    output = OrderedDict()
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
        # hack ','
        if alph == '°':
            alph = ','
        if state in output:
            output[state].update({alph : dest})
        else:
            output.update({state : {alph : dest}})                      
    return output
#------------------------------------------------------------------------------
def convert(string,hack=False):
    output = ord(string[1])
    if hack:
        for char in range(0,len(string)):
            if string[char] == '°':
                string[char] = ','
        return string
    return output
#------------------------------------------------------------------------------
def scan(string,separator=COMA):
    result = []
    hack = False
    #string = "({start,finish,banany,jablka},{'a',',','b','e','c','e','d','a'},{start','->finish},start,{finish})"
    i = 0
    component = 1
    while((i < len(string)) and (component < 6)):
        if string[i] == '(' :
            i += 1
            while (string[i] != ')'):
                if (component == 4):
                    tmp = ""
                    while (re.match(separator,string[i]) == None):
                        tmp += string[i]
                        i += 1
                    tmp = re.sub(WHTC_REX,'',tmp)
                    tmp = tmp.split(separator)
                    result.append(tmp)
                if (string[i] == '{'):  
                    i += 1
                    tmp = ""
                    while (string[i] != '}'): # problem with space in ->
                        if ((component == 3) and (string[i] == '>') and (string[i-1] != '-')):
                            return None
                        if (string[i]=='\''):
                            char = ""
                            for x in range(0,3):
                                if ((x == 2) and (string[i]!= '\'')):
                                    print_err("Input File is not in valid format", FORM_ERR)
                                char += string[i]
                                i += 1
                            char = convert(char)
                            # hack ','
                            if (char == 44):
                                #print (ord('°'))
                                hack = True
                                char = 176
                            if (char == 39) and (string[i]!='\''):
                                print_err("Input file is not in valid Format", FORM_ERR)
                            elif (char == 39):
                                i += 1
                            char = chr(char)
                            tmp += char
                        elif (re.match(WHTC_REX,string[i]) != None): # checking bonus
                            i += 1
                        else:
                            tmp += string[i]
                            i += 1
                    tmp = tmp.split(separator)
                    result.append(tmp)
                    i += 1
                elif (re.match(WHTC_REX,string[i]) != None): # checking bonus
                    i += 1
                elif (re.match(separator,string[i]) != None):
                    component += 1
                    if (component > 5):
                        return None
                    i += 1
                else :
                    return None  
            i += 1
        elif( re.match(r'[\s]',string[i]) != None):
            i += 1
        else :
            return None 
    #print(result)
    if hack:
        result[ALPHA] = convert(result[ALPHA],hack)
    result[RULES] = parse_rules(result[RULES],result[STATES])
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
    if not args.rules_only:
        M = scan(read_input(args.input)) 
    else :
        M = read_input(args.input,args.rules_only)
        print (M)
    if (not valid_format(M)):
        print_err("Input file is not in valid format", FORM_ERR)
    if (not True):
        pass
    
    prt(M)
    
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