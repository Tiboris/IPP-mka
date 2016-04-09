#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#MKA:xdudla00
#------------------------------------------------------------------------------
import re 							# to searching by regex
import os 							# to work with filesystem
import sys							# to get arguments
import argparse
#------------------------------FUNCTIONS---------------------------------------
def check_args(argv):
	parser = argparse.ArgumentParser()
	parser.add_argument('--foo', help='foo help')
	args = parser.parse_args()
	return args

def do_something(a):
	print(a)

#-----------------------------MAIN-FUNCTION------------------------------------
def main(argv):

	if ( check_args(argv) ):
		do_something("asdf")
	else:
		print("Invalid option or their combination")		
#------------------------------------------------------------------------------
if __name__ == "__main__":
    main(sys.argv)	
#------------------------------------------------------------------------------
#help
#input
#output

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