# SMEFTsim_tutorial_June23
Basic SMEFTsim tutorial for a PhD course.

## Prerequisites
you will need:
* Madgraph >=2.6.x
* pyROOT for python2

## Tutorial instructions

### Setup
download material cloning this repository and move to this folder
```
https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23.git
cd Material
```

### Running MG and looking at diagrams
launch MadGraph 
```
./MGDIR/bin/mg5_aMC
```

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
* exit MG. in the main shell, copy the predefined cards in the folders just generated
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

* launch the SM event generation
```
./Hvlvl_SM/bin/generate_events
```
when prompted, remove all optional tools (shower, delphes, analysis etc) 
leave default param and run cards

* launch the generation for quadratic terms. We will check only the operator `cHl3`
```
./Hvlvl_SMEFT/bin/generate_events
```
when prompted, remove all optional tools (shower, delphes, analysis etc) 
modify param_card setting  `cHl3=1`

* launch the generation for interference terms.
```
./Hvlvl_SMEFT_linear/bin/generate_events
```
when prompted, remove all optional tools (shower, delphes, analysis etc) 
modify param_card setting  `cHl3=1`

* launch the generation for propagator corrections
```
./Hvlvl_SMEFT_prop/bin/generate_events
```
when prompted, remove all optional tools (shower, delphes, analysis etc) 
modify param_card setting  `cHl3=1`


### Simulation via reweighting of the SM sample
reweight cards and a script to run them are provided in the material folder. if needed, change hte name of the SM directory or run in the `launch_reweughting.sh` script and then launch it
```
./launch_reweighting.sh
```
when prompted, leave all reweight cards unchanged

### Event analysis and plotting
run
```
./make_rootfiles.sh
```
to run automatically `lhe_analyzer.py` over all the generated lhe files. This produces a root file for each generation, that contains 4 histograms, corresponding to differential distributions of
$m_{e\mu}$, $m_{\mu\nu_\mu}$, $p_T^{l_1}$ (leading lepton), $p_T^\mu$

The `make_rootfiles.sh` script assumes that the directories are named as in the previous steps, and stores root files in a directory called `Root_files`. Modify it if needed.

* for the direct generations, check out the histogram shapes from ROOT, eg.
  ```
  root
  new TBrowser()
  ```
* for the reweighted samples, create pdf plots for each distributions by running
  ```
  python plot_histos.py Root_files/Hvlvl_SM_run_01.root
  ```
  modifying the script `plot_histos.py` it is possible to select which EFT contributions to plot and to adjust the plot ranges.
