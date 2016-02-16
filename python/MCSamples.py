#!/usr/bin/env python

import os
from SUSYBSMAnalysis.Zprime2muAnalysis.tools import big_warn, files_from_dbs
from SUSYBSMAnalysis.Zprime2muAnalysis.crabtools import dataset_from_publish_log

class sample(object):
    def __init__(self, name, nice_name, dataset, nevents, color, syst_frac, cross_section, k_factor=1, filenames=None, scheduler='condor', hlt_process_name='HLT', ana_dataset=None, is_madgraph=False, is_zprime=False):
        self.name = name
        self.nice_name = nice_name
        self.dataset = dataset
        self.nevents = nevents
        self.color = color
        self.syst_frac = syst_frac
        self.cross_section = cross_section
        self.k_factor = k_factor
        self.filenames_ = filenames
        self.scheduler = scheduler
        self.hlt_process_name = hlt_process_name
        self.ana_dataset = ana_dataset
        self.is_madgraph = is_madgraph
        self.is_zprime = is_zprime

    @property
    def partial_weight(self):
        return self.cross_section / float(self.nevents) * self.k_factor # the total weight is partial_weight * integrated_luminosity

    @property
    def filenames(self):
        # Return a list of filenames for running the histogrammer not
        # using crab.
        if self.filenames_ is not None:
            return self.filenames_
        return files_from_dbs(self.ana_dataset, ana02=True)

    def __getitem__(self, key):
        return getattr(self, key)

    def _dump(self, redump_existing=False):
        dst = os.path.join('/uscmst1b_scratch/lpc1/3DayLifetime/tucker', self.name) 
        os.system('mkdir ' + dst)
        for fn in self.filenames:
            print fn
            if redump_existing or not os.path.isfile(os.path.join(dst, os.path.basename(fn))):
                os.system('dccp ~%s %s/' % (fn,dst))

class tupleonlysample(sample):
    def __init__(self, name, dataset, scheduler='condor', hlt_process_name='HLT'):
        super(tupleonlysample, self).__init__(name, 'dummy', dataset, 1, 1, 1, 1, scheduler=scheduler, hlt_process_name=hlt_process_name)

# https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV for xsecs (all below in pb)
# Single-top cross sections are from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
# K factor for Drell-Yan samples is the ratio of the NNLO to POWHEG cross sections for M > 20 GeV bin, 1915/1871=1.024
samples = [
    sample('zpsi5000',  'Z\'_{#psi} (5 TeV) #rightarrow #mu^{+}#mu^{-}',  '/ZprimeToMuMu_M-5000_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 99320, 48, 1., 0.0369,  k_factor=1, is_zprime=True),
    #sample('zpsi2250',  'Z\'_{#psi} (2.25 TeV) #rightarrow #mu^{+}#mu^{-}', '/RelValZpMM_13/CMSSW_7_4_0-MCRUN2_74_V7_gensim_740pre7-v1/GEN-SIM-RECO',      9000,  48, 1.,  0.0369,  k_factor=1.3, is_zprime=True),
           
#    sample('dy50',          'DY50', '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/AODSIM', 13344402, 209 , 1., 6025.2,    k_factor=1., is_madgraph=True), #19917018 events without weight. -N*fraction of neg + N*(1-frac) frac=16.5%
##    sample('dy50_startup',          'DY50', '/RelValZMM_13/CMSSW_7_4_6_patch6-74X_mcRun2_startup_realistic50ns_v0_trackPog2015Jul24-v1/GEN-SIM-RECO', 8619, 8 , 1., 6025.2,    k_factor=1.),
           
           ####POWHEG
#    sample('dy50to120','DY50to120', '/ZToMuMu_NNPDF30_13TeV-powheg_M_50_120/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM', 2895638, 209 , 1., 1975,    k_factor=1.), # cross sect by Benj
#    sample('DY120to200Powheg','DY120to200', '/ZToMuMu_NNPDF30_13TeV-powheg_M_120_200/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 100000, 210, 1., 19.32, k_factor=1.),#mcm 19.32
#    sample('DY200to400Powheg','DY200to400', '/ZToMuMu_NNPDF30_13TeV-powheg_M_200_400/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 100000, 211, 1., 2.731, k_factor=1.),#mcm 2.731
#    sample('DY400to800Powheg','DY400to800', '/ZToMuMu_NNPDF30_13TeV-powheg_M_400_800/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 100000, 212, 1., 0.241, k_factor=1.),
#    sample('DY800to1400Powheg','DY800to1400', '/ZToMuMu_NNPDF30_13TeV-powheg_M_800_1400/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 100000, 72, 1., 0.01678, k_factor=1.),
#    sample('dy1400to2300','DY1400to2300', '/ZToMuMu_NNPDF30_13TeV-powheg_M_1400_2300/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM', 99600, 70 , 1., 0.00139,    k_factor=1.),
#    sample('dy2300to3500','DY2300to3500', '/ZToMuMu_NNPDF30_13TeV-powheg_M_2300_3500/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM', 100000, 70 , 1., 0.00139,    k_factor=1.),
#    sample('DY3500to4500Powheg','DY3500to4500', '/ZToMuMu_NNPDF30_13TeV-powheg_M_3500_4500/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 100000, 30, 1., 0.0000041, k_factor=1.),
#    sample('dy4500to6000','DY4500to6000', '/ZToMuMu_NNPDF30_13TeV-powheg_M_4500_6000/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 100000, 31 , 1., 0.00139,    k_factor=1.),
#    sample('dy50to120','DY50', '/ZToMuMu_NNPDF30_13TeV-powheg_M_50_120/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM', 19917018, 8 , 1., 6025.2,    k_factor=1.),

           ####POWHEG STARTUP 50ns
#    sample('dy50to120_s',          'DY50to120', '/ZToMuMu_NNPDF30_13TeV-powheg_M_50_120/RunIISpring15DR74-Startup_EXOReReco_74X_Spring15_mcRun2_startup_v0-v1/AODSIM', 2898838, 209 , 1., 1975,    k_factor=1.), # cross sect by Benj
#    sample('dy120to200_s',     'DY120to200', '/ZToMuMu_NNPDF30_13TeV-powheg_M_120_200/RunIISpring15DR74-Startup_EXOReReco_74X_Spring15_mcRun2_startup_v0-v1/AODSIM', 100000, 210, 1., 19.32, k_factor=1.),#mcm 19.32
#    sample('dy200to400_s',  'DY200to400', '/ZToMuMu_NNPDF30_13TeV-powheg_M_200_400/RunIISpring15DR74-Startup_EXOReReco_74X_Spring15_mcRun2_startup_v0-v1/AODSIM', 100000, 211, 1., 2.731, k_factor=1.),#mcm 2.731
#    sample('dy400to800_s',  'DY400to800', '/ZToMuMu_NNPDF30_13TeV-powheg_M_400_800/RunIISpring15DR74-Startup_EXOReReco_74X_Spring15_mcRun2_startup_v0-v1/AODSIM', 100000, 212, 1., 0.241, k_factor=1.),
#    sample('dy800to1400_s',     'DY800to1400', '/ZToMuMu_NNPDF30_13TeV-powheg_M_800_1400/RunIISpring15DR74-Startup_EXOReReco_74X_Spring15_mcRun2_startup_v0-v1/AODSIM', 100000, 72, 1., 0.01678, k_factor=1.),
#    sample('dy1400to2300_s',          'DY1400to2300', '/ZToMuMu_NNPDF30_13TeV-powheg_M_1400_2300/RunIISpring15DR74-Startup_EXOReReco_74X_Spring15_mcRun2_startup_v0-v1/AODSIM', 99600, 71 , 1., 0.00139,    k_factor=1.),
#    sample('dy2300to3500_s',          'DY2300to3500', '/ZToMuMu_NNPDF30_13TeV-powheg_M_2300_3500/RunIISpring15DR74-Startup_EXOReReco_74X_Spring15_mcRun2_startup_v0-v1/AODSIM', 100000, 70 , 1., 0.00008948,    k_factor=1.),
#    sample('dy3500to4500_s',  'DY3500to4500', '/ZToMuMu_NNPDF30_13TeV-powheg_M_3500_4500/RunIISpring15DR74-Startup_EXOReReco_74X_Spring15_mcRun2_startup_v0-v1/AODSIM', 100000, 30, 1., 0.0000041, k_factor=1.),
#    sample('dy4500to6000_s',          'DY4500to6000', '/ZToMuMu_NNPDF30_13TeV-powheg_M_4500_6000/RunIISpring15DR74-Startup_EXOReReco_74X_Spring15_mcRun2_startup_v0-v1/AODSIM', 100000, 31 , 1., 4.56E-7,    k_factor=1.),
#    sample('dy6000_s',          'DY6000', '/ZToMuMu_NNPDF30_13TeV-powheg_M_6000_Inf/RunIISpring15DR74-Startup_EXOReReco_74X_Spring15_mcRun2_startup_v0-v1/AODSIM', 100000, 31 , 1., 2.066E-8,    k_factor=1.),

#           #####aMC@NLO
#    sample('dy100to200',    'DY100-200', '/DYJetsToLL_M-100to200_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM', 66471, 210 , 1., 226,    k_factor=1., is_madgraph=True), #initial 101638 frac 17.3
#    sample('dy200to400',    'DY200-400', '/DYJetsToLL_M-200to400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM', 55741,  211, 1., 7.67,    k_factor=1., is_madgraph=True), #initial 97111 frac 21.3
#    sample('dy400to500',    'DY400-500', '/DYJetsToLL_M-400to500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM', 52853,  212, 1., 0.423,    k_factor=1., is_madgraph=True), #initial 99722 frac 23.5
#    sample('dy500to700',    'DY500-700', '/DYJetsToLL_M-500to700_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM', 52131,  72, 1., 0.24,    k_factor=1., is_madgraph=True), #initial 101029 frac 24.2
#    sample('dy700to800',    'DY700-800', '/DYJetsToLL_M-700to800_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM', 48005,  70, 1., 0.035,   k_factor=1., is_madgraph=True), #initial 96011 frac 25.
#    sample('dy800to1000',   'DY800-1000', '/DYJetsToLL_M-800to1000_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM', 44073,  30, 1., 0.03,   k_factor=1., is_madgraph=True), #initial 89216 frac 25.3
#    sample('dy1000to1500',  'DY1000-1500', '/DYJetsToLL_M-1000to1500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM', 42151,  43, 1., 0.016,    k_factor=1., is_madgraph=True), #initial 90067 26.6
#           #######
#    sample('dy1500to2000',  'DY1500-2000', '/DYJetsToLL_M-1500to2000_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM', 41895,  44, 1., 0.002,    k_factor=1., is_madgraph=True),#initil 95217 fraction 28
#    sample('dy2000to3000',  'DY2000-3000', '/DYJetsToLL_M-2000to3000_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM', 38080,  45, 1., 0.00054,    k_factor=1., is_madgraph=True),#initial 95200 fraction 30
           
    sample('tW'   ,'tW',       '/T_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM',    986100,  1, 1., 35.6, k_factor=1.),
    sample('tbarW','tbarW',    '/Tbar_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM', 971800, 12, 1., 35.6, k_factor=1.),

    sample('wz',        'WZ', '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/AODSIM', 996920, 98, 1., 66.1, k_factor=1.),# 40.2 cross section from aidan
##    sample('zz',       'ZZ', '/ZZTo4L_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM',  6621404, 7, 1., 0.157, k_factor=1.),# 0.157 pb sasha 1.256 McM
#    sample('ww',       'WW', '/WWTo2L2Nu_13TeV-powheg/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/AODSIM', 499926,   5, 1., 12.59 , k_factor=1. ),
    sample('zz_incl',   'ZZ', '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/AODSIM', 998848, 94, 1., 15.4, k_factor=1.),# 0.157 pb sasha 1.256 McM
    sample('ww_incl',   'WW', '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM', 994416,   91, 1., 118.7 , k_factor=1. ),

    sample('wjets',     'W+jets', '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM', 16430759, 52, 1., 61500, k_factor=1., is_madgraph=True), #without weights:24162881 ratio negative 16%
    sample('inclmu15', 'QCD',  '/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/AODSIM', 4767935, 801, 1., 867000000, k_factor=1.),
    sample('ttbar_pow',     't#bar{t}', '/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v4/AODSIM', 19699896, 4 , 1., 815.96, k_factor=1.),
#    sample('ttbar',     't#bar{t}', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM', 4995842, 4 , 1., 815.96, k_factor=1.),
#    sample('ttbar_startup',     't#bar{t}', '/RelValTTbar_13/CMSSW_7_4_6_patch6-74X_mcRun2_startup_realistic50ns_v0_trackPog2015Jul24-v1/GEN-SIM-RECO', 9000, 4 , 1., 815.96, k_factor=1.),
#
    sample('tWantitop', 'tWantiTop', '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/AODSIM',1000000,63 , 1., 35.85,k_factor=1.),#aidan 35.6*0.1086
    sample('tWtop',     'tWTop', '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM',998400,66 , 1., 35.85,k_factor=1.),#aidan 35.6*0.1086
#qcd
    sample('qcd50to80', 'QCD50to80', '/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM', 4914020,  43, 1., 19204300,k_factor=1.),
    sample('qcd80to120', 'QCD80to120', '/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 3459761, 43, 1., 2762530,k_factor=1.),
#    sample('qcd120to170', 'QCD120to170', '/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 3448504,  43, 1., 471100,    k_factor=1.),
    sample('qcd170to300', 'QCD170to300', '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM', 3354480,  43, 1., 117276,k_factor=1.),
    sample('qcd300to470', 'QCD300to470', '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 2935633,  43, 1., 7823,k_factor=1.),
    sample('qcd470to600', 'QCD470to600', '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM', 1937537,  43, 1., 648.2,k_factor=1.),
    sample('qcd600to800', 'QCD600to800', '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 90067,  43, 1., 186.9,k_factor=1.),
    sample('qcd800to1000', 'QCD800to1000', '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM', 1937216,  43, 1., 32.293,k_factor=1.),
    sample('qcd1000to1400', 'QCD1000to1400', '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 1487136,  43, 1., 9.4183,k_factor=1.),
    sample('qcd1400to1800', 'QCD1400to1800', '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 197959,  43, 1., 0.84265,k_factor=1.),
    sample('qcd1800to2400', 'QCD1800to2400', '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 193603,  43, 1., 0.114943,k_factor=1.),
#    sample('qcd2400to3200', 'QCD2400to3200', 'QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 90067,  43, 1., 0.00682981,k_factor=1.),
    sample('qcd3200', 'QCD3200', '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 192944,  43, 1., 0.000165445,k_factor=1.),
           
####
#### Powheg 25ns Startup
####
    sample('zpsi5000_s',  'Z\'_{#psi} (5 TeV) #rightarrow #mu^{+}#mu^{-}',  '/ZprimeToMuMu_M-5000_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Startup_EXOReReco_74X_Spring15_mcRun2_startup_v0-v1/AODSIM', 100000, 48, 1., 0.0369,  k_factor=1, is_zprime=True), #McM 0.000052
    sample('dy50to120_s','DY50to120', '/ZToMuMu_NNPDF30_13TeV-powheg_M_50_120/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM', 2901238, 209 , 1., 1975,    k_factor=1.), # cross sect by Benj
    sample('dy120to200_s','DY120to200', '/ZToMuMu_NNPDF30_13TeV-powheg_M_120_200/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM', 100000, 210, 1., 19.32, k_factor=1.),#mcm 19.32
    sample('dy200to400_s','DY200to400', '/ZToMuMu_NNPDF30_13TeV-powheg_M_200_400/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM', 100000, 211, 1., 2.731, k_factor=1.),#mcm 2.731
    sample('dy400to800_s','DY400to800', '/ZToMuMu_NNPDF30_13TeV-powheg_M_400_800/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM', 100000, 212, 1., 0.241, k_factor=1.),
    sample('dy800to1400_s','DY800to1400', '/ZToMuMu_NNPDF30_13TeV-powheg_M_800_1400/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM', 100000, 72, 1., 0.01678, k_factor=1.),
    sample('dy1400to2300_s','DY1400to2300', '/ZToMuMu_NNPDF30_13TeV-powheg_M_1400_2300/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM', 99600, 71 , 1., 0.00139,    k_factor=1.),
    sample('dy2300to3500_s','DY2300to3500', '/ZToMuMu_NNPDF30_13TeV-powheg_M_2300_3500/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM', 100000, 70 , 1., 0.00008948,    k_factor=1.),
    sample('dy3500to4500_s','DY3500to4500', '/ZToMuMu_NNPDF30_13TeV-powheg_M_3500_4500/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM', 100000, 30, 1., 0.0000041, k_factor=1.),
    sample('dy4500to6000_s','DY4500to6000', '/ZToMuMu_NNPDF30_13TeV-powheg_M_4500_6000/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM', 100000, 31 , 1., 4.56E-7,    k_factor=1.),
    sample('dy6000_s','DY6000', '/ZToMuMu_NNPDF30_13TeV-powheg_M_6000_Inf/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM', 100000, 31 , 1., 2.066E-8,    k_factor=1.),
    sample('wz_s',        'WZ', '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM', 996920, 98, 1., 66.1, k_factor=1.),# 40.2 cross section from aidan
    sample('zz_incl_s',   'ZZ', '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM', 998848, 94, 1., 15.4, k_factor=1.),# 0.157 pb sasha 1.256 McM
    sample('ww_incl_s',   'WW', '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM', 994416,   91, 1., 118.7 , k_factor=1. ),
    sample('wjets_s',     'W+jets', '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM', 16430759, 52, 1., 61500, k_factor=1., is_madgraph=True), #without weights:24162881 ratio negative 16%
    sample('ttbar_pow_s',     't#bar{t}', '/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM', 19699896, 4 , 1., 815.96, k_factor=1.),
    sample('tWantitop_s', 'tWantiTop', '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM',1000000,63 , 1., 35.85,k_factor=1.),#aidan 35.6*0.1086
    sample('tWtop_s',     'tWTop', '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM',998400,66 , 1., 35.85,k_factor=1.),#aidan 35.6*0.1086
    sample('inclmu15_s', 'QCD',  '/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM', 4767935, 801, 1., 867000000, k_factor=1.),

#    sample('DYJetsToLL_HT-100to200', 'DY_HT-100to200', '/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM', 2725655, 209, 1., 147.4, k_factor=1.),
#    sample('DYJetsToLL_HT-200to400', 'DY_HT-200to400', '/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM', 973937, 210, 1., 40.99, k_factor=1.),
#    sample('DYJetsToLL_HT-400to600', 'DY_HT-400to600', '/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM', 1067758, 211, 1., 5.678, k_factor=1.),
#    sample('DYJetsToLL_HT-600toInf', 'DY_HT-600toInf', '/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM', 998912, 212, 1., 2.21, k_factor=1.),
#    sample('DYJetsToLL_Zpt-150toInf', 'DY_Zpt-150toInf', '/DYJetsToLL_M-50_Zpt-150toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 2325189, 209, 1., 19.53, k_factor=1.),

    ]

samples.reverse()

for sample in samples:
    exec '%s = sample' % sample.name
    #if '_c' in sample.name:
    #if 'Zprime' in sample.dataset:
#    sample.ana_dataset = '/%s/federica-%s-f646da20575c2cb2b2eda7b4413fb91e/USER'  % (sample.dataset.split('/')[1], sample.name)
#    if sample.name == 'dy100-200':
#        sample.ana_dataset = '/%s/federica-%s-7a0d7047a2104d11a44d5593620f154b/USER'% (sample.dataset.split('/')[1], sample.name)
#    elif sample.name == 'dy200-400' or sample.name == 'dy400-500' or sample.name == 'dy500-700' or sample.name == 'dy700-800':
#        sample.ana_dataset = '/%s/federica-%s-f646da20575c2cb2b2eda7b4413fb91e/USER'% (sample.dataset.split('/')[1], sample.name)
#    else:
    sample.ana_dataset = '/%s/rradogna-datamc_%s-c4b4ec8fa143ea00cec443e9d0afb38f/USER'  % (sample.dataset.split('/')[1], sample.name)

        #else:
            #sample.ana_dataset = '/%s/federica-%s-02dba98b5abbcd2765544ae02b3dcc74/USER'  % (sample.dataset.split('/')[1], sample.name) # this is actually wrong
#dy100to200.ana_dataset = '/DYJetsToLL_M-100to200_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_dy100to200-1e36332d8badf10b79a5027340f46eb1/USER'
#dy200to400.ana_dataset = '/DYJetsToLL_M-200to400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_dy200to400-1e36332d8badf10b79a5027340f46eb1/USER'
#dy400to500.ana_dataset = '/DYJetsToLL_M-400to500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_dy400to500-1e36332d8badf10b79a5027340f46eb1/USER'
#dy500to700.ana_dataset = '/DYJetsToLL_M-500to700_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_dy500to700-1e36332d8badf10b79a5027340f46eb1/USER'
#dy700to800.ana_dataset = '/DYJetsToLL_M-700to800_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_dy700to800-1e36332d8badf10b79a5027340f46eb1/USER'
#dy800to1000.ana_dataset = '/DYJetsToLL_M-800to1000_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_dy800to1000-1e36332d8badf10b79a5027340f46eb1/USER'
#dy1000to1500.ana_dataset = '/DYJetsToLL_M-1000to1500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_dy1000to1500-1e36332d8badf10b79a5027340f46eb1/USER'
#dy1500to2000.ana_dataset = '/DYJetsToLL_M-1500to2000_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_dy1500to2000-1e36332d8badf10b79a5027340f46eb1/USER'
#dy2000to3000.ana_dataset = '/DYJetsToLL_M-2000to3000_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_dy2000to3000-1e36332d8badf10b79a5027340f46eb1/USER'

#zpsi5000.ana_dataset = '/ZprimeToMuMu_M-5000_TuneCUETP8M1_13TeV-pythia8/rradogna-datamc_zpsi5000-1e36332d8badf10b79a5027340f46eb1/USER'
#zpsi5000.ana_dataset = '/ZprimeToMuMu_M-5000_TuneCUETP8M1_13TeV-pythia8/federica-Zprime5000-bd8368177ad37334caf3ba3ccf63ed1c/USER'
#dy50_startup.ana_dataset = '/RelValZMM_13/rradogna-datamc_dy50_startup-8b577364235a1c7c11f4fb31512a2917/USER'
#dy50to120.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_50_120/rradogna-datamc_dy50to120-1e36332d8badf10b79a5027340f46eb1/USER' # 50ns
#dy1400to2300.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_1400_2300/rradogna-datamc_dy1400to2300-1e36332d8badf10b79a5027340f46eb1/USER' 50ns

#dy50to120.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_50_120/rradogna-datamc_dy50to120-586c586423adca66870850e07fce764e/USER' # 25ns
#DY120to200Powheg.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_120_200/alfloren-DY120to200Powheg-ea459820ba8ecaf0b251c44e2defe317/USER'
#DY200to400Powheg.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_200_400/alfloren-DY200to400Powheg-ea459820ba8ecaf0b251c44e2defe317/USER'
#DY400to800Powheg.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_400_800/alfloren-DY400to800Powheg-ea459820ba8ecaf0b251c44e2defe317/USER'
#DY800to1400Powheg.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_800_1400/alfloren-DY800to1400Powheg-d361b004739dfc1dad40e50368455d7a/USER'
#dy1400to2300.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_1400_2300/rradogna-datamc_dy1400to2300-586c586423adca66870850e07fce764e/USER'#25ns
#dy2300to3500.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_2300_3500/rradogna-datamc_dy2300to3500-586c586423adca66870850e07fce764e/USER'
#DY3500to4500Powheg.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_3500_4500/alfloren-DY3500to4500Powheg-ea459820ba8ecaf0b251c44e2defe317/USER'
#dy4500to6000.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_4500_6000/rradogna-datamc_dy4500to6000-586c586423adca66870850e07fce764e/USER'

#ww_incl.ana_dataset = '/WW_TuneCUETP8M1_13TeV-pythia8/rradogna-datamc_ww_incl-1e36332d8badf10b79a5027340f46eb1/USER'
#zz_incl.ana_dataset = '/ZZ_TuneCUETP8M1_13TeV-pythia8/rradogna-datamc_zz_incl-1e36332d8badf10b79a5027340f46eb1/USER'
###wjets.ana_datasetOLD = '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_wjets-1e36332d8badf10b79a5027340f46eb1/USER'
###ttbar.ana_dataset = '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_ttbar-1e36332d8badf10b79a5027340f46eb1/USER'
#wjets.ana_dataset = '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_wjets-d2059c7d2b57376da41472544da161fa/USER'
#ttbar_pow.ana_dataset = '/TT_TuneCUETP8M1_13TeV-powheg-pythia8/rradogna-datamc_ttbar_pow-1e36332d8badf10b79a5027340f46eb1/USER'
##ttbar_startup.ana_dataset = '/RelValTTbar_13/rradogna-datamc_ttbar_startup-8b577364235a1c7c11f4fb31512a2917/USER'
#tWantitop.ana_dataset = '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/alfloren-tWantitop-728a04705e311faf7e2183c346d6b42c/USER'
#tWtop.ana_dataset = '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/alfloren-tWtop-728a04705e311faf7e2183c346d6b42c/USER'
#inclmu15.ana_dataset = '/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/rradogna-datamc_inclmu15-c4b4ec8fa143ea00cec443e9d0afb38f/USER'

#STARTUP 50ns
#zpsi5000_s.ana_dataset = '/ZprimeToMuMu_M-5000_TuneCUETP8M1_13TeV-pythia8/rradogna-datamc_zpsi5000_s-0b6bcee552194577bc9cd7f37ddb97e3/USER'
#dy50to120_s.ana_dataset ='/ZToMuMu_NNPDF30_13TeV-powheg_M_50_120/rradogna-datamc_dy50to120_s-0b6bcee552194577bc9cd7f37ddb97e3/USER'
#dy120to200_s.ana_dataset ='/ZToMuMu_NNPDF30_13TeV-powheg_M_120_200/rradogna-datamc_dy120to200_s-0b6bcee552194577bc9cd7f37ddb97e3/USER'
#dy200to400_s.ana_dataset ='/ZToMuMu_NNPDF30_13TeV-powheg_M_200_400/rradogna-datamc_dy200to400_s-0b6bcee552194577bc9cd7f37ddb97e3/USER'
#dy400to800_s.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_400_800/rradogna-datamc_dy400to800_s-0b6bcee552194577bc9cd7f37ddb97e3/USER'
#dy800to1400_s.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_800_1400/rradogna-datamc_dy800to1400_s-0b6bcee552194577bc9cd7f37ddb97e3/USER'
#dy1400to2300_s.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_1400_2300/rradogna-datamc_dy1400to2300_s-0b6bcee552194577bc9cd7f37ddb97e3/USER'
#dy2300to3500_s.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_2300_3500/rradogna-datamc_dy2300to3500_s-0b6bcee552194577bc9cd7f37ddb97e3/USER'
#dy3500to4500_s.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_3500_4500/rradogna-datamc_dy3500to4500_s-0b6bcee552194577bc9cd7f37ddb97e3/USER'
#dy4500to6000_s.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_4500_6000/rradogna-datamc_dy4500to6000_s-0b6bcee552194577bc9cd7f37ddb97e3/USER'
#dy6000_s.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_6000_Inf/rradogna-datamc_dy6000_s-0b6bcee552194577bc9cd7f37ddb97e3/USER'

#STARTUP 25ns
zpsi5000_s.ana_dataset = '/ZprimeToMuMu_M-5000_TuneCUETP8M1_13TeV-pythia8/alfloren-zpsi5000_25s-b0e04885c346d1c92030034d13dbe060/USER'
dy50to120_s.ana_dataset ='/ZToMuMu_NNPDF30_13TeV-powheg_M_50_120/alfloren-dy50to120_25s-b0e04885c346d1c92030034d13dbe060/USER'
dy120to200_s.ana_dataset ='/ZToMuMu_NNPDF30_13TeV-powheg_M_120_200/alfloren-dy120to200_25s-b0e04885c346d1c92030034d13dbe060/USER'
dy200to400_s.ana_dataset ='/ZToMuMu_NNPDF30_13TeV-powheg_M_200_400/alfloren-dy200to400_25s-b0e04885c346d1c92030034d13dbe060/USER'
dy400to800_s.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_400_800/alfloren-dy400to800_25s-b0e04885c346d1c92030034d13dbe060/USER'
dy800to1400_s.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_800_1400/alfloren-dy800to1400_25s-b0e04885c346d1c92030034d13dbe060/USER'
dy1400to2300_s.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_1400_2300/alfloren-dy1400to2300_25s-b0e04885c346d1c92030034d13dbe060/USER'
dy2300to3500_s.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_2300_3500/alfloren-dy2300to3500_25s-b0e04885c346d1c92030034d13dbe060/USER'
dy3500to4500_s.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_3500_4500/alfloren-dy3500to4500_25s-b0e04885c346d1c92030034d13dbe060/USER'
dy4500to6000_s.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_4500_6000/alfloren-dy4500to6000_25s-b0e04885c346d1c92030034d13dbe060/USER'
#dy6000_s.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_6000_Inf/
ttbar_pow_s.ana_dataset = '/TT_TuneCUETP8M1_13TeV-powheg-pythia8/federica-datamc_ttbar_pow_s-204edf19ee7c76836afdfe3976e9bde0/USER'
wjets_s.ana_dataset = '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/federica-datamc_wjets_s-204edf19ee7c76836afdfe3976e9bde0/USER'
# wmunu_m1000.ana_dataset = '/WToMuNu_M-1000_TuneCUETP8M1_13TeV-pythia8/federica-datamc_w1000_s-0b6bcee552194577bc9cd7f37ddb97e3/USER'
# wmunu_m3000.ana_dataset = '/WToMuNu_M-3000_TuneCUETP8M1_13TeV-pythia8/federica-datamc_w3000_s-0b6bcee552194577bc9cd7f37ddb97e3/USER'
ww_incl_s.ana_dataset = '/WW_TuneCUETP8M1_13TeV-pythia8/federica-datamc_ww_incl_s-204edf19ee7c76836afdfe3976e9bde0/USER'
wz_s.ana_dataset = '/WZ_TuneCUETP8M1_13TeV-pythia8/federica-datamc_wz_s-0b6bcee552194577bc9cd7f37ddb97e3/USER'
zz_incl_s.ana_dataset = '/ZZ_TuneCUETP8M1_13TeV-pythia8/federica-datamc_zz_incl_s-0b6bcee552194577bc9cd7f37ddb97e3/USER'
tWantitop_s.ana_dataset = '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/federica-datamc_tWantitop_s-0b6bcee552194577bc9cd7f37ddb97e3/USER'
tWtop_s.ana_dataset = '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/federica-datamc_tWtop_s-0b6bcee552194577bc9cd7f37ddb97e3/USER'

# QCD
qcd50to80.ana_dataset = '/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/alfloren-qcd50to80-728a04705e311faf7e2183c346d6b42c/USER'
qcd80to120.ana_dataset = '/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/alfloren-qcd80to120-728a04705e311faf7e2183c346d6b42c/USER'
#qcd120to170.ana_dataset = '/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/alfloren-qcd120to170-728a04705e311faf7e2183c346d6b42c/USER'
qcd170to300.ana_dataset = '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/alfloren-qcd170to300-728a04705e311faf7e2183c346d6b42c/USER'
qcd300to470.ana_dataset = '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/alfloren-qcd300to470-728a04705e311faf7e2183c346d6b42c/USER'
qcd470to600.ana_dataset = '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/alfloren-qcd470to600-728a04705e311faf7e2183c346d6b42c/USER'
qcd800to1000.ana_dataset = '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/alfloren-qcd800to1000-728a04705e311faf7e2183c346d6b42c/USER'
qcd1000to1400.ana_dataset = '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/alfloren-qcd1000to1400-728a04705e311faf7e2183c346d6b42c/USER'
qcd1400to1800.ana_dataset = '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/alfloren-qcd1400to1800-728a04705e311faf7e2183c346d6b42c/USER'
qcd1800to2400.ana_dataset = '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/alfloren-qcd1800to2400-728a04705e311faf7e2183c346d6b42c/USER'
qcd3200.ana_dataset = '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/alfloren-qcd3200-728a04705e311faf7e2183c346d6b42c/USER'

__all__ = ['samples'] + [s.name for s in samples]


if __name__ == '__main__':
    if False:
        from dbstools import dbsparents
        for s in samples:
            print s.dataset
            parents = dbsparents(s.dataset)
            for parent in parents:
                for line in os.popen('dbss rel %s' % parent):
                    if 'CMSSW' in line:
                        print parent, line,
            print

    if False:
        import os
        from dbstools import dbsparents
        for s in [ww,wz,zz]:
            print s.dataset
            parents = dbsparents(s.dataset)
            print parents
            os.system('dbsconfig %s > %s' % (parents[-1], s.name))

        os.system('dbss nevents %s' % x.replace('RECO','RAW'))
        os.system('dbss nevents %s' % x)

    if False:
        import os
        from dbstools import dbsparents
        for s in samples:
            print s.dataset
            def fuf(y):
                x = os.popen(y).read()
                for line in x.split('\n'):
                    try:
                        print int(line)
                    except ValueError:
                        pass
            fuf('dbss nevents %s' % s.dataset)
            fuf('dbss nevents %s' % s.dataset.replace('AODSIM','GEN-SIM-RECO'))

    if False:
        for s in samples:
            print s.name
            os.system('grep "total events" ~/nobackup/crab_dirs/384p3/publish_logs/publish.crab_datamc_%s' % s.name)
            os.system('grep "total events" ~/nobackup/crab_dirs/413p2/publish_logs/publish.crab_datamc_%s' % s.name)
            print

    if False:
        os.system('mkdir ~/scratch/wjets')
        for fn in wjets.filenames:
            assert fn.startswith('/store')
            fn = '/pnfs/cms/WAX/11' + fn
            cmd = 'dccp %s ~/scratch/wjets/' % fn
            print cmd
            os.system(cmd)

    if False:
        for s in samples:
            print s.name
            os.system('dbss site %s' % s.dataset)
            print

    if False:
        for s in samples:
            if s.ana_dataset is None:
                continue
            c = []
            for line in os.popen('dbss ana02 find file.numevents where dataset=%s' % s.ana_dataset):
                try:
                    n = int(line)
                except ValueError:
                    continue
                c.append(n)
            c.sort()
            print s.name, c
