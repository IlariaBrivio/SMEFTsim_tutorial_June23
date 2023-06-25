#!/usr/bin/env python
import os, sys, math, ROOT, array, numpy

def KILL(log):
    print '\n@@@ FATAL -- '+log+'\n'
    raise SystemExit


### main
if __name__ == '__main__':

    if len(sys.argv)-1 != 1:
        KILL(' command-line arguments required: [1] list of input .root file')

    ifile = ROOT.TFile.Open(sys.argv[1])

    main_dir = os.path.abspath(os.getcwd())

    default_wgt = 'direct_sim' # this name is chosen in the lhe_analyzer.py
    weights_to_plot = [
           default_wgt   
#          ,'cHbox'
          ,'cHW'
          ,'cHl3'
          ,'cll1'
#          ,'cHbox_sq'
          ,'cHW_sq'
          ,'cHl3_sq'
          ,'cll1_sq'
#          ,'cHbox_cHW'
#          ,'cHbox_cHl3'
#          ,'cHbox_cll1'
#          ,'cHW_cHl3'
#          ,'cHW_cll1'
#          ,'cHl3_cll1'
          ,'cHl3_propW'
#          ,'cHq3_propW'
#          ,'cll1_propW'
    ]



    # histograms settings

    histo_dc = {

      'mll': ['m_{ll} [GeV]',                # x label
              "d#sigma/dm_{ll} [pb/5 GeV]",  # y label
              1e-9, 3e-6, 'log',             # ymin, ymax, log/lin scale
              .68, 1.25,                       # ymin, ymax lower panel
              #.95, 1.05,                       # ymin, ymax lower panel
              []],                           # weights labels NOT to plot

      'mmv': ['m_{#mu#nu_{#mu}} [GeV]',                # x label
              "d#sigma/dm_{#mu#nu_{#mu}} [pb/5 GeV]",  # y label
              1e-9, 5e-6, 'log',             # ymin, ymax, log/lin scale
              .68, 1.25,                       # ymin, ymax lower panel
              #.95, 1.05,                       # ymin, ymax lower panel
              []],                           # weights labels NOT to plot

      'pTl1': ['p_{T}^{l1} [GeV]',
               "d#sigma/dp_{T}^{l1} [pb/4 GeV]",
               1e-9, 5e-6, 'log',
               #.68, 1.25, 
               .95, 1.05, 
               []],

      'pTmu': ['p_T^{$mu} [GeV]',
               "d#sigma/dp_{T}^{#mu} [pb/4 GeV]",
               5e-8, 3e-6, 'log',
               0.68,1.25,
               []]
      
    }

    # lines setting for each weight

    color = {
    default_wgt : 1,   # black
    'cHbox'      :862,
    'cHW'        :800,
    'cHl3'       :633,
    'cll1'       :429,
    'cHbox_sq'   :862,
    'cHW_sq'     :800,
    'cHl3_sq'    :633,
    'cll1_sq'    :429,
    'cHbox_cHW'  :807,
    'cHbox_cHl3' :418,
    'cHbox_cll1' :456,
    'cHW_cHl3'   :429,
    'cHW_cll1'   :437,
    'cHl3_cll1'  :418,
    'cHl3_propW' :633,
    'cHq3_propW' :879,
    'cll1_propW' :429
    }

    style = {
    default_wgt  :1, 
    'cHbox'      :2,
    'cHW'        :2,
    'cHl3'       :2,
    'cll1'       :2,
    'cHbox_sq'   :1, 
    'cHW_sq'     :1, 
    'cHl3_sq'    :1,
    'cll1_sq'    :1,
    'cHbox_cHW'  :1,
    'cHbox_cHl3' :1,
    'cHbox_cll1' :1,
    'cHW_cHl3'   :1, 
    'cHW_cll1'   :1, 
    'cHl3_cll1'  :1, 
    'cHl3_propW' :3,  
    'cHq3_propW' :3,  
    'cll1_propW' :3 
    }


    ROOT.gROOT.SetBatch()
 
    histos = {}

    # get list of weighted histos
    for key in ifile.GetListOfKeys():
        key_name = key.GetTitle()
        histos[key_name] = ifile.Get(key_name)


    for histo_key in histo_dc:

        canvas = ROOT.TCanvas(histo_key, histo_key, 800, 725)

	# histograms pad
	 
        pad1 = ROOT.TPad("histo_pos","histo_pos",0., 0.45, 1, 1)
        pad1.SetTopMargin(0.05)
        pad1.SetBottomMargin(0)
        pad1.SetLeftMargin(0.15)
	pad1.SetGridx()
        if histo_dc[histo_key][4] == 'log':
  	    pad1.SetLogy()
	pad1.Draw()
	pad1.cd()

        #leg = ROOT.TLegend(.18,.55,.35,.95)
        leg = ROOT.TLegend(.8,.55,.95,.95)
        
        h_toPlot = {}

        for hk in histos.keys():
            coef = "_".join(hk.split("_")[1:])
            if hk.startswith(histo_key):
                h_toPlot[hk] = histos[hk].Clone()
                h_toPlot[hk].SetName("sum " + hk)
                if not coef == default_wgt:
                    h_toPlot[hk].Add(histos[histo_key + '_' + default_wgt])


        first_h = True
        for hk in histos.keys():
            coef = "_".join(hk.split("_")[1:])
            if hk.startswith(histo_key) and coef in weights_to_plot and coef not in histo_dc[histo_key][-1]:
                if first_h:
                   h_toPlot[hk].Draw('hist')
                   h_toPlot[hk].GetYaxis().SetRangeUser(histo_dc[histo_key][2],histo_dc[histo_key][3])
                   h_toPlot[hk].GetYaxis().SetLabelSize(0.05)
                   h_toPlot[hk].GetXaxis().SetTitle(histo_dc[histo_key][0])
                   h_toPlot[hk].GetXaxis().SetTitleSize(0.05)
                   h_toPlot[hk].GetYaxis().SetTitle(histo_dc[histo_key][1])
                   h_toPlot[hk].GetYaxis().SetTitleSize(0.05)

	           h_toPlot[hk].SetTitle("")
                   first_h = False

                else:

                    h_toPlot[hk].Draw('hist,same')

                h_toPlot[hk].SetStats(0)
                h_toPlot[hk].SetLineColor(color[coef])
                h_toPlot[hk].SetLineStyle(style[coef])
                h_toPlot[hk].SetLineWidth(3)
                
                if coef.startswith("c"):
                    leg.AddEntry(h_toPlot[hk],coef )
                else:
                    leg.AddEntry(h_toPlot[hk],coef)


        leg.SetTextSize(.035)
        leg.Draw()

        canvas.cd()


        ratio = {}

        for hk in histos.keys():
            coef = "_".join(hk.split("_")[1:])
            if hk.startswith(histo_key) and not coef == default_wgt:
                ratio[hk] = h_toPlot[hk].Clone()
                ratio[hk].SetName("ratio " + hk)

                # 'ratio' means just normalize to SM
                ratio[hk].Divide(h_toPlot[histo_key +"_" + default_wgt])

        # lower pad: ratio to SM
        pad2 = ROOT.TPad("histo_ratio","histo_ratio",0., 0.0 , 1, 0.45)
        pad2.SetTopMargin(0.0)
        pad2.SetLeftMargin(0.15)
        pad2.SetBottomMargin(0.27)
        pad2.SetGridx()
        pad2.SetGridy()
        pad2.Draw()
        pad2.cd()


        leg2 = ROOT.TLegend(.6,.3,.9,.65)
        
        first_h = True
        for hk in histos.keys():
            coef = "_".join(hk.split("_")[1:])
            if hk.startswith(histo_key) and coef in weights_to_plot[1:] and coef not in histo_dc[histo_key][-1] :  
                if first_h:

                    ratio[hk].Draw('hist')
                    ratio[hk].GetYaxis().SetRangeUser(histo_dc[histo_key][5],histo_dc[histo_key][6])
                    ratio[hk].GetXaxis().SetLabelSize(0.05)
                    ratio[hk].GetXaxis().SetLabelOffset(0.015)
                    ratio[hk].GetYaxis().SetLabelSize(0.05)
                    ratio[hk].GetYaxis().SetLabelOffset(0.015)
	            ratio[hk].GetXaxis().SetTitle(histo_dc[histo_key][0])
                    ratio[hk].GetXaxis().SetTitleSize(0.075)
	            
	            ratio[hk].GetYaxis().SetTitle("(SM + SMEFT) / SM")
                    ratio[hk].GetYaxis().SetTitleSize(0.07)
                    ratio[hk].GetYaxis().SetTitleOffset(0.7)

                    ratio[hk].SetTitle("")
                    first_h=False

                else:
                    ratio[hk].Draw('hist,same')

                ratio[hk].SetStats(0)
                ratio[hk].SetLineColor(color[coef])    
                ratio[hk].SetLineStyle(style[coef])
                ratio[hk].SetLineWidth(3)
              
                leg2.AddEntry(ratio[hk], hk,"l")



        leg2.SetTextSize(0.065)

        canvas.cd()

	
	canvas.SaveAs("plot_" + histo_key + ".pdf")


