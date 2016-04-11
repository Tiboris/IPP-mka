#!/usr/bin/env bash

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# IPP - mka - doplňkové testy - 2015/2016
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Činnost: 
# - vytvoří výstupy studentovy úlohy v daném interpretu na základě sady testů
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Popis (README):
#
# Struktura skriptu _stud_tests.sh (v kódování UTF-8):
# Každý test zahrnuje až 4 soubory (vstupní soubor, případný druhý vstupní 
# soubor, výstupní soubor, soubor logující chybové výstupy *.err vypisované na 
# standardní chybový výstup (pro ilustraci) a soubor logující návratový kód 
# skriptu *.!!!). Pro spuštění testů je nutné do stejného adresáře zkopírovat i 
# váš skript. V komentářích u jednotlivých testů jsou uvedeny dodatečné 
# informace jako očekávaný návratový kód. 
# Tyto doplňující testy obsahují i několik testů rozšíření (viz konec skriptu).
#
# Proměnné ve skriptu _stud_tests.sh pro konfiguraci testů:
#  INTERPRETER - využívaný interpret 
#  EXTENSION - přípona souboru s vaším skriptem (jméno skriptu je dáno úlohou) 
#  LOCAL_IN_PATH/LOCAL_OUT_PATH - testování různých cest ke vstupním/výstupním
#    souborům
#  
# Další soubory archivu s doplňujícími testy:
# V adresáři ref-out najdete referenční soubory pro výstup (*.out nebo *.xml), 
# referenční soubory s návratovým kódem (*.!!!) a pro ukázku i soubory s 
# logovaným výstupem ze standardního chybového výstupu (*.err). Pokud některé 
# testy nevypisují nic na standardní výstup nebo na standardní chybový výstup, 
# tak může odpovídající soubor v adresáři chybět nebo mít nulovou velikost.
#
# Doporučení a poznámky k testování:
# Tento skript neobsahuje mechanismy pro automatické porovnávání výsledků vašeho 
# skriptu a výsledků referenčních (viz adresář ref-out). Pokud byste rádi 
# využili tohoto skriptu jako základ pro váš testovací rámec, tak doporučujeme 
# tento mechanismus doplnit.
# Dále doporučujeme testovat různé varianty relativních a absolutních cest 
# vstupních a výstupních souborů, k čemuž poslouží proměnné začínající 
# LOCAL_IN_PATH a LOCAL_OUT_PATH (neomezujte se pouze na zde uvedené triviální 
# varianty). 
# Výstupní soubory mohou při spouštění vašeho skriptu již existovat a pokud není 
# u zadání specifikováno jinak, tak se bez milosti přepíší!           
# Výstupní soubory nemusí existovat a pak je třeba je vytvořit!
# Pokud běh skriptu skončí s návratovou hodnotou různou od nuly, tak není 
# vytvoření souboru zadaného parametrem --output nutné, protože jeho obsah 
# stejně nelze považovat za validní.
# V testech se jako pokaždé určitě najdou nějaké chyby nebo nepřesnosti, takže 
# pokud nějakou chybu najdete, tak na ni prosím upozorněte ve fóru příslušné 
# úlohy (konstruktivní kritika bude pozitivně ohodnocena). Vyhrazujeme si také 
# právo testy měnit, opravovat a případně rozšiřovat, na což samozřejmě 
# upozorníme na fóru dané úlohy.
#
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

TASK=mka
# INTERPRETER="php -d open_basedir=\"\""
# EXTENSION=php
INTERPRETER=python3
EXTENSION=py

# cesty ke vstupním a výstupním souborům
LOCAL_IN_PATH="./" # (simple relative path)
LOCAL_IN_PATH2="" #Alternative 1 (primitive relative path)
LOCAL_IN_PATH3=`pwd`"/" #Alternative 2 (absolute path)
LOCAL_OUT_PATH="./" # (simple relative path)
LOCAL_OUT_PATH2="" #Alternative 1 (primitive relative path)
LOCAL_OUT_PATH3=`pwd`"/" #Alternative 2 (absolute path)
# cesta pro ukládání chybového výstupu studentského skriptu
LOG_PATH="./"


# test01: velmi jednoducha minimalizace; Expected output: test01.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH}test01.in --output=${LOCAL_OUT_PATH}test01.out --minimize 2> ${LOG_PATH}test01.err
echo -n $? > test01.!!!

# test02: slozitejsi minimalizace; Expected output: test02.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --output=${LOCAL_OUT_PATH}test02.out -m < ${LOCAL_IN_PATH}test02.in 2> ${LOG_PATH}test02.err
echo -n $? > test02.!!!

# test03: slozitejsi formatovani vstupniho automatu (diakritika); Expected output: test03.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH}test03.in > ${LOCAL_OUT_PATH}test03.out 2> ${LOG_PATH}test03.err
echo -n $? > test03.!!!

# test04: hledani neukoncujiciho stavu (past, trap); Expected output: test04.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --output=${LOCAL_OUT_PATH3}test04.out --find-non-finishing < ${LOCAL_IN_PATH}test04.in 2> ${LOG_PATH}test04.err
echo -n $? > test04.!!!

# test05: kontrola dobre specifikovanosti vstupniho automatu; Expected output: test05.out; Expected return code: 62
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH}test05.in --output=${LOCAL_OUT_PATH}test05.out 2> ${LOG_PATH}test05.err
echo -n $? > test05.!!!

# test06: příklad konečného automatu ve vstupním formátu úlohy MKA (není dobře specifikovaný); Expected output: test06.out; Expected return code: 62
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH2}test06.in --output=${LOCAL_OUT_PATH2}test06.out 2> ${LOG_PATH}test06.err
echo -n $? > test06.!!!

# test07: ukazka case-insensitive; Expected output: test07.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --case-insensitive -m < ${LOCAL_IN_PATH}test07.in > ${LOCAL_OUT_PATH}test07.out 2> ${LOG_PATH}test07.err
echo -n $? > test07.!!!

# test08: chybna kombinace parametru -m a -f; Expected output: test08.out; Expected return code: 1
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH3}test08.in --output=${LOCAL_OUT_PATH2}test08.out --minimize -f 2> ${LOG_PATH}test08.err
echo -n $? > test08.!!!

# test09: syntakticka chyba vstupniho formatu; Expected output: test09.out; Expected return code: 60
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH2}test09.in --output=${LOCAL_OUT_PATH}test09.out --minimize 2> ${LOG_PATH}test09.err
echo -n $? > test09.!!!

# test10: semanticka chyba vstupniho formatu (stav neni v mnozine stavu); Expected output: test10.out; Expected return code: 61
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH3}test10.in --output=${LOCAL_OUT_PATH3}test10.out 2> ${LOG_PATH}test10.err
echo -n $? > test10.!!!

# test90: Bonus RLO - na vstupu pouze pravidla (bez rozsireni vraci chybu 1); Expected output: test90.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH}test90.in --output=${LOCAL_OUT_PATH3}test90.out --rules-only 2> ${LOG_PATH}test90.err
echo -n $? > test90.!!!

# test91: Bonus WHT - oddeleni elementu nejen carkami, ale i bilymi znaky, symboly nemusi byt v apostrofech (bez rozsireni vraci chybu 1); Expected output: test91.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH}test91.in --output=${LOCAL_OUT_PATH2}test91.out -w 2> ${LOG_PATH}test91.err
echo -n $? > test91.!!!

# test92: Bonus RLO - konecny automat neni dobre specifikovany (bez rozsireni vraci chybu 1); Expected output: test92.out; Expected return code: 62
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH2}test92.in --output=${LOCAL_OUT_PATH}test92.out -r 2> ${LOG_PATH}test92.err
echo -n $? > test92.!!!

# test93: Bonus WHT a RLO - kombinace parametru (bez rozsireni vraci chybu 1); Expected output: test93.out; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION -r -m --white-char --input=${LOCAL_IN_PATH}test93.in --output=${LOCAL_OUT_PATH}test93.out 2> ${LOG_PATH}test93.err
echo -n $? > test93.!!!

for i in `seq -w 1 93` ; do
    t="test$i";
    retval=`cat ${LOG_PATH}$t".!!!"`;
    exp=`cat "ref-out/"$t".!!!"`;
    ((total++))
    if [ $exp = $retval  ];then
        if [ ! -e ${LOG_PATH}$t".out" ] || diff ${LOG_PATH}$t".out" "ref-out/"$t".out" >/dev/null ; then
            ((succ++))
            echo $t" -> SUCCESS"
        else
            echo $t" -> FAILED (OUTPUTS DO NOT MATCH)\n"
#            echo `diff $t".out" "ref-out/"$t".out"`; 
        fi
    else
        expmsg=`cat "ref-out/"$t".err"`;
        retmsg=`cat ${LOG_PATH}$t".err"`;
        echo $t" -> FAILED (WRONG RETVAL: $retval $retmsg | EXPECTED $exp $expmsg )"
    fi
done
 
 
printf "\n== TESTS SUCCEEDED: $succ/$total ==\n\n"
