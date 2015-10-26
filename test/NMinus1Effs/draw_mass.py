#!/usr/bin/env python

# (py draw.py >! plots/nminus1effs/out.draw) && tlp plots/nminus1effs

from pprint import pprint
import sys, os
from array import array
from SUSYBSMAnalysis.Zprime2muAnalysis.roottools import *
set_zp2mu_style()
ROOT.gStyle.SetPadTopMargin(0.02)
ROOT.gStyle.SetPadRightMargin(0.02)
ROOT.gStyle.SetTitleX(0.12)
#ROOT.gStyle.SetTitleH(0.07)
ROOT.TH1.AddDirectory(0)

outfile = ROOT.TFile("whargl.root","recreate")
iarp=0
do_tight = 'tight' in sys.argv
psn = 'plots/nminus1effs'
if do_tight:
    psn += '_tight'
ps = plot_saver(psn, size=(600,600), log=False, pdf=True)
ps.c.SetBottomMargin(0.2)


if do_tight:
    nminus1s = [
        #'TiPt',
        'TiDB',
        'TiGlbChi2',
        'TiIso',
        'TiTkLayers',
        'TiPxHits',
        'TiMuHits',
        'TiMuMatch',
        ]
else:
    nminus1s = [
        'NoPt',
        'NoDB',
        'NoIso',
        'NoTkLayers',
        'NoPxHits',
        'NoMuHits',
        'NoMuMatch',
        'NoVtxProb',
        'NoB2B',
        'NoDptPt',
                #'NoCosm',
        'NoTrgMtch',
        ]

pretty = {
    'NoPt': 'p_{T} > 53 GeV',
    'NoTkLayers': '# tk lay > 5',
    'NoPxHits': '# px hits > 0',
    'NoMuStns': '# mu segs > 1',
    'NoDB': '|dB| < 0.2',
    'NoGlbChi2': 'glb #chi^{2}/ndf < 10',
    'NoTkMuon': 'isTrackerMuon',
    'NoMuHits': '# mu hits > 0',
    'NoMuMatch': '# tk. #mu seg > 1',
    'NoCosm': 'anti-cosmic',
    'NoTrgMtch': 'HLT match',
    'NoB2B': 'back-to-back',
    'NoVtxProb': '#chi^{2} #mu#mu vtx < 20',
    'NoDptPt': 'dpT/pT',
    'NoIso': 'rel. tk. iso.',
    #'data': 'Data, %.1f fb^{-1}',
    'data': 'Data, %.1f fb^{-1}, MuonOnly',
    'dataB': 'Data RunB, %.1f fb^{-1}, MuonOnly',
    'dataCD': 'Data RunC+D, %.1f fb^{-1}, MuonOnly',
    'mcsum_lumi': 'Simulation',
    'mcsum_ref': 'Simulation',
    'mc50m120_lumi': 'Simulation 60 < M < 120 GeV',
    'mc50m120_ref': 'Simulation 60 < M < 120 GeV',
    'mc120m_lumi': 'Simulation M > 120 GeV',
    'mc120m_ref': 'Simulation M > 120 GeV',
    'mc800m2300_lumi': 'Simulation 800 < M < 2300 GeV',
    'mc800m2300_ref': 'Simulation 800 < M < 2300 GeV',
    'mc400m2300_lumi': 'Simulation 400 < M < 2300 GeV',
    'mc400m2300_ref': 'Simulation 400 < M < 2300 GeV',
    'zmumu': 'Z#rightarrow#mu#mu, 60 < M < 120 GeV',
    'dy120_c1': 'DY#rightarrow#mu#mu, M > 120 GeV',
    'dy200_c1': 'DY#rightarrow#mu#mu, M > 200 GeV',
    'dy500_c1': 'DY#rightarrow#mu#mu, M > 500 GeV',
    'dy1000_c1': 'DY#rightarrow#mu#mu, M > 1000 GeV',
    'dy50': 'DY#rightarrow#mu#mu madgraph',
#    'dy50': 'DY#rightarrow#mu#mu, M > 50 GeV',
    'dy50to120': 'DY#rightarrow#mu#mu powheg',
    'dy50_startup': 'DY#rightarrow#mu#mu startup',
    'ttbar': 't#bar{t}',
    'ttbar_pow': 't#bar{t} powheg',
    'ttbar_startup': 't#bar{t} startup',
    'ww_incl': 'WW',
    'zz_incl': 'ZZ',
    'wz' : 'WZ',
    'inclmu15': 'QCD',
    'zssm1000': 'Z\' SSM, M=1000 GeV',
    'zpsi5000': 'Z\'_{#psi}, M=5000 GeV',
    'zpsi5000_m1TeV': 'Z\'_{#psi}, M=5000 GeV',
    'zpsi5000_1m3TeV': 'Z\'_{#psi}, M=5000 GeV',
    'zpsi5000_3mTeV': 'Z\'_{#psi}, M=5000 GeV',
    '60m120_BCD': '60 < m < 120 GeV',
    '60m120_CD': '60 < m < 120 GeV',
    '60m120': '60 < m < 120 GeV',
    '70m110': '70 < m < 110 GeV',
    '120m200': '120 < m < 200 GeV', 
    '200m400': '200 < m < 400 GeV',
    '400m600': '400 < m < 600 GeV',
    '200m': 'm > 200 GeV',
    '50m': 'm > 50 GeV',
    '70m': 'm > 70 GeV',
    '120m_BCD': 'm > 120 GeV',
    '120m_CD': 'm > 120 GeV',
    '120m': 'm > 120 GeV',
    'DY120to200Powheg': 'DY#rightarrow#mu#mu 120 < m < 200 GeV',
    'DY200to400Powheg': 'DY#rightarrow#mu#mu 200 < m < 400 GeV',
    'DY400to800Powheg': 'DY#rightarrow#mu#mu 400 < m < 800 GeV',
    'DY800to1400Powheg': 'DY#rightarrow#mu#mu 800 < m < 1400 GeV',
    'dy1400to2300': 'DY#rightarrow#mu#mu 1400 < m < 2300 GeV',
    '400m800' : '400 < m < 800 GeV',
    '800m1400': '800 < m < 1400 GeV',
    '1400m2300':'1400 < m < 2300 GeV',
    '800m2300':'800 < m < 2300 GeV',
    '400m2300':'400 < m < 2300 GeV',
    'all_lumi':'Simulation M > 120 GeV',
    'all_ref':'Simulation M > 120 GeV',
    '120m1400':'120 < M < 1400 GeV',
    }

class nm1entry:
    def __init__(self, sample, is_data, lumi):
        if type(sample) == str:
            self.name = sample
            self.fn = self.make_fn(sample) if is_data else None
            self.lumi = lumi if is_data else None
        else:
            self.name = sample.name
            self.fn = self.make_fn(self.name)
        self.prepare_histos()
            
    def make_fn(self, name):
        return 'nminus1_histos/ana_nminus1_%s.root' % name
    
    def prepare_histos(self):
        self.histos = {}
        if self.fn is not None:
            f = ROOT.TFile(self.fn)
            for nminus1 in nminus1s + ['NoNo']:
                if 'wjets' in self.name:
                    self.histos[nminus1] = f.Get(nminus1).Get('DimuonMassVertexConstrainedWeight').Clone()#DileptonMass
                else:
                    self.histos[nminus1] = f.Get(nminus1).Get('DimuonMassVertexConstrained').Clone()#DileptonMass

    def prepare_histos_sum(self, samples, lumi):
        self.histos = {}
        for nminus1 in nminus1s + ['NoNo']:
            hs = []
            #print '%20s%20s%21s%20s%20s' % ('cut', 'sampe name', 'partial weight', 'scale(ref)','scale(lumi)')
            for sample in samples:
                f = ROOT.TFile(self.make_fn(sample.name))
                if 'wjets' in sample.name:
                    h = f.Get(nminus1).Get('DimuonMassVertexConstrainedWeight').Clone()
                else:
                    h = f.Get(nminus1).Get('DimuonMassVertexConstrained').Clone()
                #print '%20s%20s%20.15f%20f%20f' % (nminus1, sample.name, sample.partial_weight, refN/refXS, lumiCD)
                # partial_weight = cross_section * k_factor / Nevents
                if lumi>0:
                    # scale to luminosity for comparision of single dataset to MC
                    h.Scale(sample.partial_weight * lumi) 
                    #print nminus1, sample.name, sample.partial_weight*lumi
                    #print '%20s%20s%20.10f%20f' % (nminus1, sample.name, sample.partial_weight, lumi)
                if lumi<0:
                    # scale to reference cross section/Nevents for comparision of multiple datasets to MC
                    h.Scale(sample.partial_weight * refN / refXS)  
                    #print nminus1, sample.name, sample.partial_weight*refN/refXS
                    #print '%20s%20s%20.10f%20f' % (nminus1, sample.name, sample.partial_weight, refN/refXS)
                hs.append(h)
            hsum = hs[0].Clone()
            for h in hs[1:]:
                hsum.Add(h)
            self.histos[nminus1] = hsum

#data, lumi = nm1entry('data', True), 242.8 # lumi in pb
nolumi = -1
lumiB = 50.7 
lumiCD = 1052.24 
lumiD = 1004.99
dataB = nm1entry('dataB', True, lumiB)#lumiB )
dataCD = nm1entry('dataCD', True, lumiCD)#lumiCD )
#dataD = nm1entry('dataD', True, lumiD )
mcsum_lumi = nm1entry('mcsum_lumi',False,lumiCD)
mcsum_ref = nm1entry('mcsum_ref',False,nolumi)
DYmc = nm1entry('DYmc',False,lumiCD)
nonDYmc = nm1entry('nonDYmc',False,lumiCD)
#wjets = nm1entry('wjets',False,lumiCD)

from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import *
raw_samples = [dy50to120,DY120to200Powheg,DY200to400Powheg,DY400to800Powheg,DY800to1400Powheg,dy1400to2300,dy2300to3500,DY3500to4500Powheg,dy4500to6000,ttbar_pow,ww_incl,zz_incl,wz,tWtop,tWantitop,wjets]#inclmu15,
#DYmc_list = [dy50to120,DY120to200Powheg,DY200to400Powheg,DY400to800Powheg,DY800to1400Powheg,dy1400to2300,dy2300to3500,DY3500to4500Powheg,dy4500to6000]
#nonDYmc_list = [ttbar_pow,ww_incl,zz_incl,wz,wjets,tWtop,tWantitop]

refXS = dy50to120.cross_section
refN = dy50to120.nevents

# All MC samples
# lumi
mcsum_lumi.prepare_histos_sum(raw_samples,lumiCD)
mc_samples_lumi = [nm1entry(sample,False,lumiCD) for sample in raw_samples]
for mc_sample in mc_samples_lumi:
    exec '%s = mc_sample' % mc_sample.name
## ref
#mcsum_ref.prepare_histos_sum(raw_samples, nolumi) 
#mc_samples_ref = [nm1entry(sample,False,nolumi) for sample in raw_samples]
#for mc_sample in mc_samples_ref:
#    exec '%s = mc_sample' % mc_sample.name

#DYmc.prepare_histos_sum(DYmc_list,lumiCD)
#nonDYmc.prepare_histos_sum(nonDYmc_list,lumiCD)

mass_range = [60,120,200,400,800,1600]#,2300,3500,4500,6000]

to_use = {
    #'NoPt':[DYmc,nonDYmc,dataCD],
    #'NoDB':[DYmc,nonDYmc,dataCD],
    #'NoIso':[DYmc,nonDYmc,dataCD],
    #'NoTkLayers':[DYmc,nonDYmc,dataCD],
    #'NoPxHits':[DYmc,nonDYmc,dataCD],
    #'NoMuHits':[DYmc,nonDYmc,dataCD],
    #'NoMuMatch':[DYmc,nonDYmc,dataCD],
    #'NoVtxProb':[DYmc,nonDYmc,dataCD],
    #'NoB2B':[DYmc,nonDYmc,dataCD],
    #'NoDptPt':[DYmc,nonDYmc,dataCD],
    #'NoTrgMtch':[DYmc,nonDYmc,dataCD],
    'NoPt':[mcsum_lumi,dataCD],
    'NoDB':[mcsum_lumi,dataCD],
    'NoIso':[mcsum_lumi,dataCD],
#    'NoIso':[wjets],
    'NoTkLayers':[mcsum_lumi,dataCD],
    'NoPxHits':[mcsum_lumi,dataCD],
    'NoMuHits':[mcsum_lumi,dataCD],
    'NoMuMatch':[mcsum_lumi,dataCD],
#    'NoMuMatch':[wjets],
    'NoVtxProb':[mcsum_lumi,dataCD],
    'NoB2B':[mcsum_lumi,dataCD],
    'NoDptPt':[mcsum_lumi,dataCD],
    'NoTrgMtch':[mcsum_lumi,dataCD],
    }

styles = {
#    'data':      (ROOT.kBlack,     -1),
    'dataB':      (ROOT.kBlack,     -1),
    'dataCD':      (ROOT.kBlack,     -1),
#    'zmumu':     (ROOT.kRed,     3001),
#    'dy50':      (ROOT.kBlue,     1001),
#    'dy50_startup':      (ROOT.kViolet+2,     3001),
#    'dy200_c1':  (ROOT.kRed,     1001),
#    'dy500_c1':  (ROOT.kRed,     1001),
#    'dy1000_c1': (ROOT.kBlue,    1001),
#    'ttbar':     (ROOT.kGreen+2, 3005),
#    'ttbar_startup':     (ROOT.kGreen+2, 3005),
#    'ww_incl':    (ROOT.kBlue,    3004),
#    'zz_incl':    (62,            3006),
#    'wz' :       (64,            3007),
#    'inclmu15':  (28,            3002),
    'mc50m120_lumi':     (ROOT.kGreen+2, 1001),
    'mc50m120_ref':     (ROOT.kGreen+2, 1001),
    'mc120m_lumi':     (ROOT.kGreen+2, 1001),
    'mc120m_ref':     (ROOT.kGreen+2, 1001),
    'mc800m2300_lumi':     (ROOT.kGreen+2, 1001),
    'mc800m2300_ref':     (ROOT.kGreen+2, 1001),
    'mc400m2300_lumi':     (ROOT.kGreen+2, 1001),
    'mc400m2300_ref':     (ROOT.kGreen+2, 1001),
    'dy50to120':      (ROOT.kGreen+2,     1001),
    'DY120to200Powheg':  (ROOT.kGreen+2, 1001),
    'DY200to400Powheg':  (ROOT.kGreen+2, 1001),
    'DY400to800Powheg':  (ROOT.kGreen+2, 1001),
    'DY800to1400Powheg': (ROOT.kGreen+2, 1001),
    'dy1400to2300':      (ROOT.kGreen+2, 1001),
    'ttbar_pow':     (ROOT.kGreen+2, 1001),
    'mcsum_lumi':    (ROOT.kGreen+2, 1001),
    'mcsum_ref':    (ROOT.kGreen+2, 1001),
    'zpsi5000':    (ROOT.kBlue, 1001),
    'zpsi5000_m1TeV':    (ROOT.kBlue, 1001),
    'zpsi5000_1m3TeV':    (ROOT.kBlue, 1001),
    'zpsi5000_3mTeV':    (ROOT.kBlue, 1001),
    'DYmc': (ROOT.kGreen, 3001),
    'nonDYmc': (ROOT.kRed, 1001),
    }

ymin = {
    'NoPt': 0.0,
    'NoDB': 0.7,
    'NoIso': 0.4,
    'NoTkLayers':0.7,
    'NoPxHits':0.7,
    'NoMuHits':0.7,
    'NoMuMatch':0.7,
    'NoVtxProb':0.7,
    'NoB2B':0.7,
    'NoDptPt':0.7,
    'NoTrgMtch':0.7,
    }
#global_ymin = 0.
global_ymin = None

def table(entry,nminus1, mass_range):
    print entry.name
    hnum = entry.histos['NoNo']
    hden = entry.histos[nminus1]
    print '%20s%27s%23s%20s%20s%22s' % ('cut', 'mass range', 'numerator', 'denominator', 'efficiency', '68% CL')
    for mbin in range(len(mass_range)):
        if mbin == (len(mass_range)-1): break
        #print mass_range[mbin], mass_range[mbin+1]
        mlow = mass_range[mbin]
        mhigh = mass_range[mbin+1] 
        num = get_integral(hnum, mlow, mhigh, integral_only=True, include_last_bin=False)
        den = get_integral(hden, mlow, mhigh, integral_only=True, include_last_bin=False)
        e,l,h = clopper_pearson(num, den)
        print '%20s%15i%15i%20f%20f%20f%15f%15f' % (nminus1, mlow, mhigh, num, den, e, l, h)

ROOT.gStyle.SetTitleX(0.25)
ROOT.gStyle.SetTitleY(0.50)

for nminus1 in nminus1s:
    pretty_name = pretty[nminus1]
    print nminus1, pretty_name
    lg = ROOT.TLegend(0.25, 0.21, 0.81, 0.44)
    lg.SetTextSize(0.03)
    lg.SetFillColor(0)
    lg.SetBorderSize(1)
    
    same = 'A'
    effs = []


    for entry in to_use[nminus1]: #,mass_range 

        table(entry,nminus1, mass_range)
        color, fill = styles[entry.name]

        l = len(mass_range)-1
        nminus1_num = ROOT.TH1F('num', '', l, array('f',mass_range))
        nminus1_den = ROOT.TH1F('den', '', l, array('f',mass_range))
    
        hnum = entry.histos['NoNo']
        hden = entry.histos[nminus1]

        for mbin in range(len(mass_range)):
            if mbin == (len(mass_range)-1): continue
            mlow = mass_range[mbin]
            mhigh = mass_range[mbin+1]
            num = get_integral(hnum, mlow, mhigh, integral_only=True, include_last_bin=False)
            den = get_integral(hden, mlow, mhigh, integral_only=True, include_last_bin=False)
            nminus1_num.SetBinContent(mbin+1, num)
            nminus1_den.SetBinContent(mbin+1, den)
        eff = binomial_divide(nminus1_num, nminus1_den)
 
        eff.SetTitle(pretty_name)
        eff.GetYaxis().SetRangeUser(global_ymin if global_ymin is not None else ymin[nminus1], 1.01)
        eff.GetXaxis().SetTitle('m(#mu#mu) [GeV]')
        eff.GetYaxis().SetLabelSize(0.027)
        eff.GetYaxis().SetTitle('n-1 efficiency')
        if 'data' in entry.name:
            draw = 'P'
            eff.SetLineColor(color)
            eff.SetMarkerStyle(20)
            eff.SetMarkerSize(1.05)
            eff.SetMarkerColor(color)
            #lg.AddEntry(eff, pretty.get(entry.name, entry.name) % (lumi/1000.), 'LP')
            lg.AddEntry(eff, pretty.get(entry.name, entry.name) % (entry.lumi/1000.), 'LP')
        else:
            draw = '2'
            eff.SetLineColor(color)
            eff.SetFillColor(color)
            eff.SetFillStyle(fill)
            lg.AddEntry(eff, pretty.get(entry.name, entry.name), 'LF')
        draw += same
        eff.Draw(draw)
        effs.append(eff)
        same = ' same'
        outfile.cd()
        eff.Write("arp%d"%iarp)
        iarp+=1
    # end for entry in to_use[name]: # entry is a specific sample
    lg.Draw()
    ps.save(nminus1)
    print
# end for name, mass_range in mass_bins:
