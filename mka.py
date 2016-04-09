#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#MKA:xdudla00
#------------------------------------------------------------------------------
import re                           # to searching by regex
import os                           # to work with filesystem
import sys                          # to get arguments
import argparse
#------------------------------FUNCTIONS---------------------------------------
#------------------------------------------------------------------------------
def check_args(): # TODO fix duplicated params
    parser = argparse.ArgumentParser(add_help=False, 
                description='Script for processing finite state machines')
    parser.add_argument('--help', #help='show this help message and exit', 
                required=False, action="store_true")
    parser.add_argument('--input', required=False,
                #help='if not set it takes STDIN', 
                default=sys.stdin)
    parser.add_argument('--output', required=False,
                #help='if not set output will be at STDOUT', 
                default=sys.stdout)
    parser.add_argument('-m','--minimize', required=False,
                #help='minimizes finite state machine', 
                action="store_true")
    parser.add_argument('-f','--find-non-finishing', required=False,
                #help='find states and prints them otherwise \'0\'',
                action="store_true")
    parser.add_argument('-i','--case-insensitive', required=False, 
                #help='ignoring input states strings case', 
                action="store_true")
    try :
        args = parser.parse_args()
    except :
        exit(9)
    # if args.help : 
    #     print(parser.format_help())
    return args
#------------------------------------------------------------------------------
def read_input(input_file):
    if input_file != sys.stdin :
        try :
            input_file=open(input_file,'r')
        except :
            print_err("Can not open file",9)
    for line in input_file:
        print(line)
#------------------------------------------------------------------------------
def print_err(msg,code):
    print(msg)
    exit(code)
#------------------------------------------------------------------------------
#-----------------------------MAIN-FUNCTION------------------------------------
def main():
    args = check_args()
    read_input(args.input)
    return 0
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