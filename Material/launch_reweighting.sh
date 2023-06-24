#!/bin/bash 

PROCNAME=Hvlvl_SM
RUNNAME=run_01

cp reweight_card_int.dat $PROCNAME/Cards/reweight_card.dat
./${PROCNAME}/bin/madevent reweight ${RUNNAME} -f

cp reweight_card_squares.dat $PROCNAME/Cards/reweight_card.dat
./${PROCNAME}/bin/madevent reweight ${RUNNAME} -f

cp reweight_card_propW.dat $PROCNAME/Cards/reweight_card.dat
./${PROCNAME}/bin/madevent reweight ${RUNNAME} -f


MIXED=("cHbox_cHW" "cHbox_cHl3" "cHbox_cll1" "cHW_cHl3" "cHW_cll1" "cHl3_cll1" )

for mix in ${MIXED[*]}; do
  cp "reweight_card_mix_${mix}.dat" $PROCNAME/Cards/reweight_card.dat
  ./${PROCNAME}/bin/madevent reweight ${RUNNAME} -f
done





