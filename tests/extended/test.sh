#!/bin/bash

TASK=mka
EXTENSION=py
INTERPRETER="python3"

ok_count=0
count=0

red='\033[1;31m'
green='\033[1;32m'
NC='\033[0m'

LOCAL_IN_PATH="./test-in/" 	# (simple relative path)
LOCAL_OUT_PATH="./test-out/" # (simple relative path)

function run_test {
	((count++))

	printf ">>> %-7s %-59s " "Test $count:" "$4"

	printf ""|$INTERPRETER $TASK.$EXTENSION $3 1> "${LOCAL_OUT_PATH}test.out" 2> "${LOCAL_OUT_PATH}err.out"
	exit_code="$?"

	if [ "$1" = "" ]; then
		diffCode="0"; 
		diffout="";
	else
		diffout="Diff out "`diff "${LOCAL_OUT_PATH}test.out" "ref-out/$1"`""
		diffCode=$?
	fi

	if [ "$diffCode" = "0" ] && [ "$exit_code" = "$2" ]; then
		echo -e "[  ${green}OK${NC}  ]"
		((ok_count++))
	else
		echo -e "[ ${red}CHYBA${NC} ]"
		echo "$INTERPRETER" "$TASK.$EXTENSION" "$3"
		cat "${LOCAL_OUT_PATH}err.out"
		echo "Exit code: $exit_code"
		printf "%s" "$diffout"
		echo
	fi
	rm "${LOCAL_OUT_PATH}test.out"
	rm "${LOCAL_OUT_PATH}err.out"
}

function check_ref_test {
	((count++))
	if [ "$1" -lt "10" ]; then
		num="0$1"
	else
		num="$1"
	fi


	printf ">>> %-10s %-56s " "Referencni test $num" ""
	if [ -f ref-out/test$num.out ] && [ -s ref-out/test$num.out ]; then
		diffOut="Diff test$num.out: `diff "test-out/test$num.out" "ref-out/test$num.out"`\n"
		retOut=$?
	else
		retOut="0"
	fi
	diffRet="Diff test$num.!!!: `diff test-out/test$num'.!!!' ref-out/test$num'.!!!'`"
	retRet=$?
	if [ "$retOut" = "0" ] && [ "$retRet" = "0" ]; then
		echo -e "[  ${green}OK${NC}  ]"
		((ok_count++))
	else
		echo -e "[ ${red}CHYBA${NC} ]"
		tail test-out/test$num.err
		printf "\n%s\n" "$diffRet"
		printf "%s\n" "$diffOut"
		echo
	fi
}

################################################################################

echo
echo
echo -e "\t\t\t\t\t${green}IPP:MKA TESTY${NC}"

if [ ! -d "${LOCAL_OUT_PATH}" ]; then
	mkdir "${LOCAL_OUT_PATH}"
fi

# test01: velmi jednoducha minimalizace; Expected output: test01.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH}test01.in --output=${LOCAL_OUT_PATH}test01.out --minimize 2> ${LOCAL_OUT_PATH}test01.err
echo -n $? > ${LOCAL_OUT_PATH}test01.!!!
check_ref_test 1

# test02: slozitejsi minimalizace; Expected output: test02.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --output=${LOCAL_OUT_PATH}test02.out -m < ${LOCAL_IN_PATH}test02.in 2> ${LOCAL_OUT_PATH}test02.err
echo -n $? > ${LOCAL_OUT_PATH}test02.!!!
check_ref_test 2

# test03: slozitejsi formatovani vstupniho automatu (dia); Expected output: test03.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH}test03.in > ${LOCAL_OUT_PATH}test03.out 2> ${LOCAL_OUT_PATH}test03.err
echo -n $? > ${LOCAL_OUT_PATH}test03.!!!
check_ref_test 3

# test04: hledani neukoncujiciho stavu (past, trap); Expected output: test04.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --output=${LOCAL_OUT_PATH}test04.out --find-non-finishing < ${LOCAL_IN_PATH}test04.in 2> ${LOCAL_OUT_PATH}test04.err
echo -n $? > ${LOCAL_OUT_PATH}test04.!!!
check_ref_test 4

# test05: kontrola dobre specifikovanosti vstupniho automatu; Expected output: test05.out; Expected return code: 62
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH}test05.in --output=${LOCAL_OUT_PATH}test05.out 2> ${LOCAL_OUT_PATH}test05.err
echo -n $? > ${LOCAL_OUT_PATH}test05.!!!
check_ref_test 5

# test06: příklad konečného automatu ve vstupním formátu úlohy MKA (není dobře specifikovaný); Expected output: test06.out; Expected return code: 62
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH}test06.in --output=${LOCAL_OUT_PATH}test06.out 2> ${LOCAL_OUT_PATH}test06.err
echo -n $? > ${LOCAL_OUT_PATH}test06.!!!
check_ref_test 6

# test07: ukazka case-insensitive; Expected output: test07.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --case-insensitive -m < ${LOCAL_IN_PATH}test07.in > ${LOCAL_OUT_PATH}test07.out 2> ${LOCAL_OUT_PATH}test07.err
echo -n $? > ${LOCAL_OUT_PATH}test07.!!!
check_ref_test 7

# test08: chybna kombinace parametru -m a -f; Expected output: test08.out; Expected return code: 1
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH}test08.in --output=${LOCAL_OUT_PATH}test08.out --minimize -f 2> ${LOCAL_OUT_PATH}test08.err
echo -n $? > ${LOCAL_OUT_PATH}test08.!!!
check_ref_test 8

# test09: syntakticka chyba vstupniho formatu; Expected output: test09.out; Expected return code: 60
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH}test09.in --output=${LOCAL_OUT_PATH}test09.out --minimize 2> ${LOCAL_OUT_PATH}test09.err
echo -n $? > ${LOCAL_OUT_PATH}test09.!!!
check_ref_test 9

# test10: semanticka chyba vstupniho formatu (stav neni v mnozine stavu); Expected output: test10.out; Expected return code: 61
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH}test10.in --output=${LOCAL_OUT_PATH}test10.out 2> ${LOCAL_OUT_PATH}test10.err
echo -n $? > ${LOCAL_OUT_PATH}test10.!!!
check_ref_test 10

# test90: Bonus RLO - na vstupu pouze pravidla (bez rozsireni vraci chybu 1); Expected output: test90.out; Expected return code: 0
#$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH}test90.in --output=${LOCAL_OUT_PATH}test90.out --rules-only 2> ${LOCAL_OUT_PATH}test90.err
#echo -n $? > ${LOCAL_OUT_PATH}test90.!!!
#check_ref_test 90

# test91: Bonus WHT - oddeleni elementu nejen carkami, ale i bilymi znaky, symboly nemusi byt v apostrofech (bez rozsireni vraci chybu 1); Expected output: test91.out; Expected return code: 0
#$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH}test91.in --output=${LOCAL_OUT_PATH}test91.out -w 2> ${LOCAL_OUT_PATH}test91.err
#echo -n $? > ${LOCAL_OUT_PATH}test91.!!!
#check_ref_test 91

# test92: Bonus RLO - konecny automat neni dobre specifikovany (bez rozsireni vraci chybu 1); Expected output: test92.out; Expected return code: 62
#$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH}test92.in --output=${LOCAL_OUT_PATH}test92.out -r 2> ${LOCAL_OUT_PATH}test92.err
#echo -n $? > ${LOCAL_OUT_PATH}test92.!!!
#check_ref_test 92

# test93: Bonus WHT a RLO - kombinace parametru (bez rozsireni vraci chybu 1); Expected output: test93.out; Expected return code: 0
#$INTERPRETER $TASK.$EXTENSION -r -m --white-char --input=${LOCAL_IN_PATH}test93.in --output=${LOCAL_OUT_PATH}test93.out 2> ${LOCAL_OUT_PATH}test93.err
#echo -n $? > ${LOCAL_OUT_PATH}test93.!!!
#check_ref_test 93


echo
echo -e "${green}Testy parametrů${NC}"
echo

#run_test   <vyst. soub>	<e> 	<argumenty programu> 						<popis spusteneho testu>
#--------------------------------------------------------------------------------------------------------------------------- 					
run_test 	""		60 	""									"Prázdný vstup - exit 60"
run_test 	""		1 	"--bla"									"Neexistujici parametr - exit 1"
run_test	"" 		1 	"--input" 								"Parametr bez hodnoty - exit 1"
run_test 	""		1 	"--input=${LOCAL_IN_PATH}test01.in --input=${LOCAL_IN_PATH}test01.in" 	"Duplicitni parametr - exit 1"
run_test 	""		1 	"--minimize -m"								"Duplicitni prepinac - exit 1"
run_test 	""		1 	"-f -m"									"Nepovolena kombinace - exit 1"
run_test	""		2 	"--input=bla"								"Neexistujici input - exit 2"
run_test	""		3 	"--input=${LOCAL_IN_PATH}test01.in --output=./blaablla/test01.out"	"Neexistujici output - exit 3"
run_test 	""		0 	"--input=${LOCAL_IN_PATH}test01.in --output=${LOCAL_OUT_PATH}test01.out" 	"Vstup ok"

echo
echo -e "${green}Testy konkretnich parametru${NC}"
echo

run_test  "test01.out" 	0 	"--input=${LOCAL_IN_PATH}test01.in -m"				"Parametr -m"
run_test  "test01.out" 	0 	"--input=${LOCAL_IN_PATH}test01.in --minimize"			"Parametr --minimize"
run_test  "test04.out" 	0 	"--input=${LOCAL_IN_PATH}test04.in -f"				"Parametr -f"
run_test  "test04.out" 	0 	"--input=${LOCAL_IN_PATH}test04.in --find-non-finishing"	"Parametr --find-non-finishing"
run_test  "test07.out" 	0 	"--input=${LOCAL_IN_PATH}test07.in -i -m"			"Parametr -i"	
run_test  "test07.out" 	0 	"--input=${LOCAL_IN_PATH}test07.in --case-insensitive -m"   	"Parametr --case-insensitive"	

echo
echo -e "${green}Testy chyb${NC}"
echo

# 	Epsilon nesmi byt ve vstupni abecede - bere se jako chybejici znak mezi apostrofy
run_test  	"" 		60 	"--input=${LOCAL_IN_PATH}test01a.in -m"			"Epsilon ve vstupni abecede - exit 60"
# 	Pokud je epsilon prechod, nejedna se o deterministicky automat
run_test  	"" 		62 	"--input=${LOCAL_IN_PATH}test01b.in -m"			"Epsilon prechod - exit 62"
run_test  	"" 		60 	"--input=${LOCAL_IN_PATH}test15a.in -m"			"Chybne apostrofy - exit 60"
run_test  	"" 		60 	"--input=${LOCAL_IN_PATH}test14a.in -m"			"Vice znaku v symbolu - exit 60"
run_test  	"" 		61 	"--input=${LOCAL_IN_PATH}test07.in -m"			"Neexistujici stav - exit 61"
run_test  	"" 		61 	"--input=${LOCAL_IN_PATH}test01c.in"			"Neexistujici symbol - exit 61"
run_test  	"" 		62 	"--input=${LOCAL_IN_PATH}test16.in"			"Nedeterministicky automat - exit 62"
run_test  	"" 		60 	"--input=${LOCAL_IN_PATH}test01e.in"			"Chybne nazvy stavu (stav zacina cislem) - exit 60"
run_test  	"" 		60 	"--input=${LOCAL_IN_PATH}test01f.in"			"Chybne nazvy stavu (stav zacina _) - exit 60"
run_test  	"" 		60 	"--input=${LOCAL_IN_PATH}test01g.in"			"Chybne nazvy stavu (stav konci _) - exit 60"
run_test  	"" 		61 	"--input=${LOCAL_IN_PATH}test01h.in"			"Prazdna vstupni abeceda - exit 61"
run_test  	"" 		61 	"--input=${LOCAL_IN_PATH}test01i.in"			"Prazdna mnozina stavu - exit 61"
run_test  	"" 		62 	"--input=${LOCAL_IN_PATH}test01j.in"			"Zadne koncove stavy - exit 62"

echo
echo -e "${green}Testy minimalizace${NC}"
echo

run_test  "test11.out" 	0 	"--input=${LOCAL_IN_PATH}test11.in -m"			"DSKA 1"
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH}test11.in -m 2> ${LOCAL_OUT_PATH}test11.err 1> "${LOCAL_OUT_PATH}test11.out"
run_test  "test11.out" 	0 	"--input=${LOCAL_OUT_PATH}test11.out -m"		"Znovunacteni DSKA 1 a minimalizace"
run_test  "test12.out" 	0 	"--input=${LOCAL_IN_PATH}test12.in -m"			"DSKA 2"
run_test  "test13.out" 	0 	"--input=${LOCAL_IN_PATH}test13.in -m -i"		"DSKA 3"
run_test  "test14.out" 	0 	"--input=${LOCAL_IN_PATH}test14.in -m"			"Symboly jsou znaky \t a \n"
run_test  "test15.out" 	0 	"--input=${LOCAL_IN_PATH}test15.in -m"			"Symboly apostrofy a uvozovky"
run_test  "test01.out" 	0 	"--input=${LOCAL_IN_PATH}test01d.in -m"			"Opakujici se stavy, symboly a pravidla"

color=${red}
if [ "$ok_count" = "$count" ]; then
	color=${green}
fi

echo
echo "--------------------------------------------------------------------------------"
echo -e "Proslo ${color}$ok_count${NC} testu z $count"
echo "--------------------------------------------------------------------------------"
