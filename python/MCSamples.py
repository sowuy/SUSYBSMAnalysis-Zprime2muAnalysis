#!/usr/bin/env python

import os
from SUSYBSMAnalysis.Zprime2muAnalysis.tools import big_warn, files_from_dbs
from SUSYBSMAnalysis.Zprime2muAnalysis.crabtools import dataset_from_publish_log

class sample(object):
    def __init__(self, name, nice_name, dataset, nevents, color, syst_frac, cross_section, k_factor=1, filenames=None, scheduler='condor', hlt_process_name='HLT', ana_dataset=None, is_zprime=False):
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

# https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV for xsecs (all below in pb)
# Single-top cross sections are from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma8TeV
# K factor for Drell-Yan samples is the ratio of the NNLO to POWHEG cross sections for M > 20 GeV bin, 1915/1871=1.024
samples = [
    ##sample('zpsi5000',  'Z\'_{#psi} (5 TeV) #rightarrow #mu^{+}#mu^{-}',  '/ZprimeToMuMu_M-5000_Tune4C_13TeV-pythia8/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v1/AODSIM',      97890,  48, 1.,  0.0369,  k_factor=1.3, is_zprime=True),
  # sample('dy50', 'DY50', '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/AODSIM',  9000,  37, 1., 6104,    k_factor=1.), ## another quoted value for XS 5943.2
   # sample('dy100-200', 'DY100-200', '/DYJetsToLL_M-100to200_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM',   101638,  38, 1., 226,    k_factor=1.),
   # sample('dy200-400', 'DY200-400', '/DYJetsToLL_M-200to400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM',   96310,  39, 1., 7.67,    k_factor=1.),
   # sample('dy400-500', 'DY400-500', '/DYJetsToLL_M-400to500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM',   98441,  40, 1., 0.423,    k_factor=1.),
   # sample('dy500-700', 'DY500-700', '/DYJetsToLL_M-500to700_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM',   101029,  41, 1., 0.24,    k_factor=1.),
   # sample('dy700-800', 'DY700-800', '/DYJetsToLL_M-700to800_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM',   96011,  42, 1., 0.035,   k_factor=1.),
   # sample('dy1000-1500', 'DY1000-1500', '/DYJetsToLL_M-1000to1500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 90067,  43, 1., 0.016,    k_factor=1.),
   # sample('dy1500-2000', 'DY1500-2000', '/DYJetsToLL_M-1500to2000_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 95217,  44, 1., 0.002,    k_factor=1.),
   # sample('dy2000-3000', 'DY2000-3000', '/DYJetsToLL_M-2000to3000_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 95200,  45, 1., 0.00054,    k_factor=1.),
   # sample('ttbar','t#bar{t}', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM',    9000,  2,  1., 832,     k_factor=1.),
   # sample('WW', 'Inclusive-WW', '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM',     697656,  3, 1., 63.21,   k_factor=1.),
   # sample('WZ', 'Inclusive-WZ', '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM',     0,  2, 1., 22.82,   k_factor=1.),
    #sample('ZZ', 'Inclusive-ZZ', '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/AODSIM',     996944,  4, 1., 10.32,   k_factor=1.)
    #sample('qcd1000to1400', 'QCD1000to1400', '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 90067,  43, 1., 0.016,    k_factor=1.),
    #sample('qcd120to170', 'QCD120to170', '/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 90067,  43, 1., 0.016,    k_factor=1.),
   # sample('qcd1400to1800', 'QCD1400to1800', '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 90067,  43, 1., 0.016,    k_factor=1.),
    #sample('qcd170to300', 'QCD170to300', '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM', 90067,  43, 1., 0.016,    k_factor=1.),
    #sample('qcd1800to2400', 'QCD1800to2400', '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 90067,  43, 1., 0.016,    k_factor=1.),
    #sample('qcd2400to3200', 'QCD2400to3200', 'QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 90067,  43, 1., 0.016,    k_factor=1.),
    #sample('qcd300to470', 'QCD300to470', '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 90067,  43, 1., 0.016,    k_factor=1.),
   # sample('qcd470to600', 'QCD470to600', '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM', 90067,  43, 1., 0.016,    k_factor=1.),
    #sample('qcd3200', 'QCD3200', '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 90067,  43, 1., 0.016,    k_factor=1.),
    #sample('qcd50to80', 'QCD50to80', '/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM', 90067,  43, 1., 0.016,    k_factor=1.),
   # sample('qcd600to800', 'QCD600to800', '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 90067,  43, 1., 0.016,    k_factor=1.),
    #sample('qcd800to1000', 'QCD800to1000', '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM', 90067,  43, 1., 0.016,    k_factor=1.),
    #sample('qcd80to120', 'QCD80to120', '/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 90067,  43, 1., 0.016,    k_factor=1.)
    #sample('tWtop', 'tWTop', '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM', 90067,  43, 1., 0.016,    k_factor=1.),
    #sample('tWantitop', 'tWantiTop', '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/AODSIM', 90067,  43, 1., 0.016,    k_factor=1.)
    #sample('dy50',          'DY50', '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/AODSIM', 13543572, 8 , 1., 6025.2,    k_factor=1.),
    #sample('ttbar',     't#bar{t}', '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM', 1598670, 4 , 1., 815.96, k_factor=1.),
    #sample('ttbar_pow',     't#bar{t}', '/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v4/AODSIM', 19699896, 4 , 1., 815.96, k_factor=1.),
    #sample('zz_incl',   'ZZ', '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/AODSIM', 998848, 7, 1., 15.4, k_factor=1.), # 0.157 pb sasha 1.256 McM
    #sample('ww_incl',   'WW', '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM', 994416,   5, 1., 118.7 , k_factor=1. ),
    #sample('wz',        'WZ', '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/AODSIM', 996920, 6, 1., 66.1, k_factor=1.),# 40.2 cross section from aidan
    #sample('tWantitop', 'tWantiTop', '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/AODSIM',1000000,63 , 1., 35.6*0.1086, k_factor=1.),
    #sample('tWtop',     'tWTop', '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM',998400,66 , 1., 35.6*0.1086, k_factor=1.)
    #sample('wjets',     'W+jets', '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM', 24073076, 52, 1., 61500, k_factor=1.),
    #sample('dy50_startup',          'DY50', '/RelValZMM_13/CMSSW_7_4_6_patch6-74X_mcRun2_startup_realistic50ns_v0_trackPog2015Jul24-v1/GEN-SIM-RECO', 8619, 8 , 1., 6025.2,    k_factor=1.),
    #sample('DY800to1400Powheg',     'DY800to1400Powheg', '/ZToMuMu_NNPDF30_13TeV-powheg_M_800_1400/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 24073076, 52, 1., 0.01678, k_factor=1.),
    #sample('DY120to200Powheg',     'DY120to200Powheg', '/ZToMuMu_NNPDF30_13TeV-powheg_M_120_200/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 48171, 52, 1., 19.32, k_factor=1.),
    #sample('DY200to400Powheg',  'DY200to400Powheg', '/ZToMuMu_NNPDF30_13TeV-powheg_M_200_400/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 100000, 52, 1.,  2.731, k_factor=1.),
    #sample('DY400to800Powheg',  'DY400to800Powheg', '/ZToMuMu_NNPDF30_13TeV-powheg_M_400_800/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 100000, 52, 1., 61500, k_factor=1.),
    #sample('DY3500to4500Powheg',  'DY3500to4500Powheg', '/ZToMuMu_NNPDF30_13TeV-powheg_M_3500_4500/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM', 100000, 52, 1., 61500, k_factor=1.),
    sample('dy100to200',    'DY100-200', '/DYJetsToLL_M-100to200_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM', 66471,  38, 1., 226,    k_factor=1.),
    sample('dy200to400',    'DY200-400', '/DYJetsToLL_M-200to400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/AODSIM', 55741,  39, 1., 7.67,    k_factor=1.),
    
    ]

samples.reverse()

for sample in samples:
    exec '%s = sample' % sample.name
    # print sample.dataset.split('/')[1]
    
    # pattuple MC 740 federica-dy200-400-f646da20575c2cb2b2eda7b4413fb91e/USER
    #    dy50.ana_dataset = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/federica-%s-f646da20575c2cb2b2eda7b4413fb91e/USER'  % (sample.name)
   # if sample.name == 'dy100-200' or sample.name == 'dy50' or sample.name == 'ZZ' or sample.name == 'ttbar':
      #  sample.ana_dataset = '/%s/federica-%s-7a0d7047a2104d11a44d5593620f154b/USER'% (sample.dataset.split('/')[1], sample.name)
   # elif sample.name == 'WZ':
   #     sample.ana_dataset = '/%s/federica-%s_v2-7a0d7047a2104d11a44d5593620f154b/USER'% (sample.dataset.split('/')[1], sample.name)
  #  else:
      #  sample.ana_dataset = '/%s/federica-%s-f646da20575c2cb2b2eda7b4413fb91e/USER' % (sample.dataset.split('/')[1], sample.name)

#zpsi2250.ana_dataset = '/RelValZpMM_13/rradogna-datamc_%s-8613b30987dd6a37bceba633a6fea3c5/USER'
#ttbar.ana_dataset = '/RelValTTbar_13/rradogna-datamc_ttbar-750b21338a3f946db84cc0a53e55f580/USER'
#zz.ana_dataset = '/ZZTo4L_Tune4C_13TeV-powheg-pythia8/federica-ZZ_Phys14_PU20BX25-02dba98b5abbcd2765544ae02b3dcc74/USER'
#wz.ana_dataset = '/WZJetsTo3LNu_Tune4C_13TeV-madgraph-tauola/federica-WZ_Phys14_PU20BX25-02dba98b5abbcd2765544ae02b3dcc74/USER'
#wjets.ana_dataset = '/WJetsToLNu_13TeV-madgraph-pythia8-tauola/federica-WJets_Phys14_PU20BX25-02dba98b5abbcd2765544ae02b3dcc74/USER'
#tbarW.ana_dataset = '/Tbar_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/federica-Tbar_tW_Phys14_PU20BX25-02dba98b5abbcd2765544ae02b3dcc74/USER'
#tW.ana_dataset = '/T_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/federica-T_tW_Phys14_PU20BX25-02dba98b5abbcd2765544ae02b3dcc74/USER'
#ttbar.ana_dataset = '/TT_Tune4C_13TeV-pythia8-tauola/federica-TT_Phys14_PU20BX25-02dba98b5abbcd2765544ae02b3dcc74/USER'
#inclmu15.ana_dataset = '/QCD_Pt-20toInf_MuEnrichedPt15_PionKaonDecay_Tune4C_13TeV_pythia8/federica-QCD_Phys14_PU20BX25-02dba98b5abbcd2765544ae02b3dcc74/USER'
#dy50.ana_dataset = '/DYJetsToLL_M-50_13TeV-madgraph-pythia8/federica-DY_M-50_Phys14_PU20BX25-02dba98b5abbcd2765544ae02b3dcc74/USER'
#dy9500.ana_dataset = '/DYJetsToEEMuMu_M-9500_13TeV-madgraph/federica-DY_M-9500_Phys14_PU20BX25-02dba98b5abbcd2765544ae02b3dcc74/USER'
#dy8500.ana_dataset = '/DYJetsToEEMuMu_M-8500To9500_13TeV-madgraph/federica-DY_M-8500To9500_Phys14_PU20BX25-02dba98b5abbcd2765544ae02b3dcc74/USER'
#dy800.ana_dataset = '/DYJetsToEEMuMu_M-800To1400_13TeV-madgraph/federica-DY_M-800To1400_Phys14_PU20BX25-02dba98b5abbcd2765544ae02b3dcc74/USER'
#dy7500.ana_dataset = '/DYJetsToEEMuMu_M-7500To8500_13TeV-madgraph/federica-DY_M-7500To8500_Phys14_PU20BX25-02dba98b5abbcd2765544ae02b3dcc74/USER'
#dy6000.ana_dataset = '/DYJetsToEEMuMu_M-6000To7500_13TeV-madgraph/federica-DY_M-6000To7500_Phys14_PU20BX25-02dba98b5abbcd2765544ae02b3dcc74/USER'
#dy4500.ana_dataset = '/DYJetsToEEMuMu_M-4500To6000_13TeV-madgraph/federica-DY_M-4500To6000_Phys14_PU20BX25-02dba98b5abbcd2765544ae02b3dcc74/USER'
#dy400.ana_dataset = '/DYJetsToEEMuMu_M-400To800_13TeV-madgraph/federica-DY_M-400To800_Phys14_PU20BX25-02dba98b5abbcd2765544ae02b3dcc74/USER'
#dy3500.ana_dataset = '/DYJetsToEEMuMu_M-3500To4500_13TeV-madgraph/federica-DY_M-3500To4500_Phys14_PU20BX25-02dba98b5abbcd2765544ae02b3dcc74/USER'
#dy2300.ana_dataset = '/DYJetsToEEMuMu_M-2300To3500_13TeV-madgraph/federica-DY_M-2300To3500_Phys14_PU20BX25-02dba98b5abbcd2765544ae02b3dcc74/USER'
#dy200.ana_dataset = '/DYJetsToEEMuMu_M-200To400_13TeV-madgraph/federica-DY_M-200To400_Phys14_PU20BX25-02dba98b5abbcd2765544ae02b3dcc74/USER'
#dy1400.ana_dataset = '/DYJetsToEEMuMu_M-1400To2300_13TeV-madgraph/federica-DY_M-1400To2300_Phys14_PU20BX25-02dba98b5abbcd2765544ae02b3dcc74/USER'
#dy120.ana_dataset = '/DYJetsToEEMuMu_M-120To200_13TeV-madgraph/federica-DY_M-120To200_Phys14_PU20BX25-02dba98b5abbcd2765544ae02b3dcc74/USER'
#dy50.ana_dataset = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_dy50-c4b4ec8fa143ea00cec443e9d0afb38f/USER'
#ttbar.ana_dataset = '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_ttbar-1e36332d8badf10b79a5027340f46eb1/USER'
#ttbar_pow.ana_dataset = '/TT_TuneCUETP8M1_13TeV-powheg-pythia8/rradogna-datamc_ttbar_pow-1e36332d8badf10b79a5027340f46eb1/USER'
#ww_incl.ana_dataset = '/WW_TuneCUETP8M1_13TeV-pythia8/rradogna-datamc_ww_incl-1e36332d8badf10b79a5027340f46eb1/USER'
#zz_incl.ana_dataset = '/ZZ_TuneCUETP8M1_13TeV-pythia8/rradogna-datamc_zz_incl-1e36332d8badf10b79a5027340f46eb1/USER'
#tWantitop.ana_dataset = '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/alfloren-tWantitop-728a04705e311faf7e2183c346d6b42c/USER'
#tWtop.ana_dataset = '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/alfloren-tWtop-728a04705e311faf7e2183c346d6b42c/USER'
#wz.ana_dataset = '/WZ_TuneCUETP8M1_13TeV-pythia8/rradogna-datamc_wz-c4b4ec8fa143ea00cec443e9d0afb38f/USER'
#wjets.ana_dataset = '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_wjets-d2059c7d2b57376da41472544da161fa/USER'
#dy50_startup.ana_dataset = '/RelValZMM_13/rradogna-datamc_dy50_startup-8b577364235a1c7c11f4fb31512a2917/USER'
#DY120to200Powheg.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_120_200/alfloren-DY120to200Powheg-ea459820ba8ecaf0b251c44e2defe317/USER'
#DY200to400Powheg.ana_dataset = '/ZToMuMu_NNPDF30_13TeV-powheg_M_200_400/alfloren-DY200to400Powheg-ea459820ba8ecaf0b251c44e2defe317/USER'
dy100to200.ana_dataset = '/DYJetsToLL_M-100to200_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_dy100to200-1e36332d8badf10b79a5027340f46eb1/USER'
dy200to400.ana_dataset = '/DYJetsToLL_M-200to400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_dy200to400-1e36332d8badf10b79a5027340f46eb1/USER'

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
