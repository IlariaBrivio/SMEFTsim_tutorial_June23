#!/usr/bin/env python
import sys, math, ROOT, copy

def KILL(log):
    print '\n@@@ FATAL -- '+log+'\n'
    raise SystemExit

def lhep_pdgID  (line): return int  (line.split()[ 0])
def lhep_status (line): return int  (line.split()[ 1])
def lhep_mother1(line): return int  (line.split()[ 2])
def lhep_mother2(line): return int  (line.split()[ 3])
def lhep_px     (line): return float(line.split()[ 6])
def lhep_py     (line): return float(line.split()[ 7])
def lhep_pz     (line): return float(line.split()[ 8])
def lhep_E      (line): return float(line.split()[ 9])
def lhep_M      (line): return float(line.split()[10])

def print_lhep(l):
    print lhep_pdgID  (l),
    print lhep_status (l),
    print lhep_mother1(l),
    print lhep_mother2(l),
    print lhep_px     (l),
    print lhep_py     (l),
    print lhep_pz     (l),
    print lhep_E      (l),
    print lhep_M      (l)

    return

### main
if __name__ == '__main__':

    if len(sys.argv)-1 != 2:
        KILL('two command-line arguments required: [1] input .lhe file, [2] output .root file')

    ifile = file      (sys.argv[1], 'r')
    ofile = ROOT.TFile(sys.argv[2], 'recreate')

    ###

    event_num_max = -1

    # find number of weights. begin with initial weight

    orig_wgt_label = 'direct_sim'
    Nwgts = 1
    wgt_id = [orig_wgt_label]

    for line in ifile:
        if line.startswith('<weight id'):
            Nwgts+=1
            wgt_id.append(line.split("'")[1])
        if line.startswith('</weightgroup>'):
            break
    else:
        print "end of file reached. no new weights found"



    ## define relevant histograms
    h_mll = {}
    h_pTl1 = {}
    h_pTmu = {}

    for k in wgt_id: # one histo per weight class
        label = k

        h_mll[k]   = ROOT.TH1F('mll_'+label  , 'mll_'+label , 25, 0, 125)
        h_pTl1[k]  = ROOT.TH1F('pTl1_'+label , 'pTl1_'+label ,16, 0, 64)
        h_pTmu[k]  = ROOT.TH1F('pTmu_'+label , 'pTmu_'+label ,16, 0, 64)

        h_mll[k].Sumw2()
        h_pTl1[k].Sumw2()
        h_pTmu[k].Sumw2()
  
    event_num, in_event = 0, False
 

    ifile.seek(0)

    # reads the lhe and looks into the events
    for line in ifile:
        if line[:1] == '#': continue
        if line.startswith('<scales'): continue

            
        if event_num_max > 0:
            if event_num > event_num_max: continue

        if line.startswith('<event>'):
            event_num += 1
            genp_ls = []
            weight = {}
            in_event = True
            continue

        if in_event:

            if not line.startswith('</event>'):
                l0 = line.strip('\n')
                
                if l0.startswith('<wgt'):
                    l1 = l0.split()
                    weight[l1[1].split("=")[1].strip("'>")] = float(l1[2])
                    continue

                if l0.startswith('<'): continue
                if len(l0.split()) == 6: 
                    weight[orig_wgt_label] = float(l0.split()[2])
                    continue

                genp_ls.append(l0)

            else:
                ### event analysis

	        # define the four momentum of the dilepton pair. 

		ll_p4 = ROOT.TLorentzVector(0, 0, 0, 0)
                e_p4 = ROOT.TLorentzVector(0, 0, 0, 0)
                m_p4 = ROOT.TLorentzVector(0, 0, 0, 0)

                for p in genp_ls:

		    # for each particle in an event: extract four momentum
                    i_p4 = ROOT.TLorentzVector(lhep_px(p), lhep_py(p), lhep_pz(p), lhep_E(p))
		   
		    if lhep_status(p) == 1: 

			# e or mu
                        if abs(lhep_pdgID(p)) == 11: 
                           ll_p4 += i_p4
                           e_p4 = i_p4

                        if abs(lhep_pdgID(p)) == 13: 
                           ll_p4 += i_p4
                           m_p4 = i_p4


                # for each event: store the observables in the histograms
                for k in wgt_id:
                        h_mll[k].Fill(ll_p4.M(), weight[k]) 
                        h_pTl1[k].Fill(max(e_p4.Pt(), m_p4.Pt()), weight[k]) 
                        h_pTmu[k].Fill(m_p4.Pt(), weight[k]) 
                    

                in_event = False
                continue

    # output a root file
    ofile.cd()

    print("processed %i events" %event_num)


    xsec = {}
    print event_num
    for k in wgt_id:
        h_mll[k].Scale(1./event_num)
        h_pTl1[k].Scale(1./event_num)
        h_pTmu[k].Scale(1./event_num)
        

        xsec[k] = float(h_mll[k].GetSumOfWeights())
        print("integrated weight %s: %.3e" %(k, xsec[k]))        



        h_mll[k].Write()
        h_pTl1[k].Write()
        h_pTmu[k].Write()

    ofile.Close()
    print("file %s produced" %sys.argv[2])                                 
