#!/bin/bash 

PROCNAMES=(Hvlvl_SM Hvlvl_SMEFT Hvlvl_SMEFT_linear Hvlvl_SMEFT_prop)
RUNNAME=run_01

mkdir -p Root_files

for proc in ${PROCNAMES[*]}; do
    	
  EVENTS="$proc/Events/$RUNNAME/unweighted_events.lhe"
  gunzip "$EVENTS.gz"
  python lhe_analyzer.py $EVENTS "Root_files/${proc}_${RUNNAME}.root"
  gzip $EVENTS

done

