#!/bin/bash

BASEX_DIR_BIN=../basex/bin/
BASEX_DIR=../basex/
OUTPUT_TEMP_FILE=../dictionnaryOutput/dicoSorted
OUTPUT_FILE=$1
export CLASSPATH=${BASEX_DIR}/icu4j-70_1.jar
echo $1
${BASEX_DIR_BIN}/basex -s "cdata-section-elements=def nature" ${BASEX_DIR}/query.xq  > ${OUTPUT_TEMP_FILE}
mv ${OUTPUT_TEMP_FILE} ${OUTPUT_FILE}
