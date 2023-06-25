# SMEFTsim_tutorial_June23
Basic SMEFTsim tutorial for a PhD course.

## Prerequisites
you can either have installed locally:
* Madgraph >=2.6.x
* pyROOT for python2

or use docker
[instructions to come]

## Tutorial instructions

### Setup
download material cloning this repository and move to this folder
```
https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23.git
cd Material
```

### Running MG and looking at diagrams
launch MadGraph 
[command TBC]

inside the MadGraph terminal, run
```
import model ./SMEFTsim_U35_MwScheme_UFO-massless_Hvlvl
```

SM process:
```
generate h > e- ve~ mu+ vm SMHLOOP=0 NP=0 NPprop=
display diagrams
output Hvlvl_SM
```

pure SMEFT process (quadratics):
```
generate h > e- ve~ mu+ vm SMHLOOP=0 NP==1 NPprop=0
display diagrams
output Hvlvl_SMEFT
```

check diagrams operator by operator (without exporting)
```
generate h > e- ve~ mu+ vm SMHLOOP=0 NP==1 NPcll1==1 NPprop=0
display diagrams
generate h > e- ve~ mu+ vm SMHLOOP=0 NP==1 NPcHl3==1 NPprop=0
display diagrams
generate h > e- ve~ mu+ vm SMHLOOP=0 NP==1 NPcHW==1 NPprop=0
display diagrams
generate h > e- ve~ mu+ vm SMHLOOP=0 NP==1 NPcHbox==1 NPprop=0
```

SM-SMEFT interference:
```
generate h > e- ve~ mu+ vm SMHLOOP=0 NP=1 NP^2==1 NPprop=0
output Hvlvl_SMEFT_linear
```

SM-SMEFT interference, propagator corrections:
```
generate h > e- ve~ mu+ vm SMHLOOP=0 NP=0 NPprop=2 NPprop^2==2
display diagrams
output Hvlvl_prop
```


### Direct event simulation
exit MG. in the main shell, copy the predefined cards in the folders just generated
```
cp param_card_Hvlvl.dat Hvlvl_SM/Cards/param_card.dat
cp param_card_Hvlvl.dat Hvlvl_SMEFT/Cards/param_card.dat
cp param_card_Hvlvl.dat Hvlvl_SMEFT_linear/Cards/param_card.dat
cp param_card_Hvlvl.dat Hvlvl_SMEFT_prop/Cards/param_card.dat

cp run_card_Hvlvl.dat Hvlvl_SM/Cards/run_card.dat
cp run_card_Hvlvl.dat Hvlvl_SMEFT/Cards/run_card.dat
cp run_card_Hvlvl.dat Hvlvl_SMEFT_linear/Cards/run_card.dat
cp run_card_Hvlvl.dat Hvlvl_SMEFT_prop/Cards/run_card.dat
```

launch the SM event generation
```
./Hvlvl_SM/bin/generate_events
```
when prompted, remove all optional tools (shower, delphes, analysis etc) and leave default cards

