#!/usr/bin/env python

import os
from SUSYBSMAnalysis.Zprime2muAnalysis.tools import big_warn, files_from_dbs
from SUSYBSMAnalysis.Zprime2muAnalysis.crabtools import dataset_from_publish_log

miniAOD = True

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

	# Switching to NNPDF3.1 for 94X Fall17 MC samples requires new XS calculations
	# https://www.dropbox.com/s/1iuns6rqybkplgc/80X_94X_XsecMons.pdf?dl=0
	# https://indico.cern.ch/event/727541/contributions/2994873/attachments/1645469/2629652/Lanyov_Dimuon_mass_plots_vs_DY_xsec_07.05.2018.pdf
    sample('dy50to120',   'DY50to120', '/ZToMuMu_NNPDF31_13TeV-powheg_M_50_120/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 2961000, 209 , 1., 2112.905,   k_factor=1.),
    sample('dy120to200',  'DY120to200', '/ZToMuMu_NNPDF31_13TeV-powheg_M_120_200/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000, 210, 1., 20.553, k_factor=1.),
    sample('dy200to400',  'DY200to400', '/ZToMuMu_NNPDF31_13TeV-powheg_M_200_400/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000, 211, 1., 2.8861, k_factor=1.),
    sample('dy400to800',  'DY400to800', '/ZToMuMu_NNPDF31_13TeV-powheg_M_400_800/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000, 212, 1., 0.25126, k_factor=1.),
    sample('dy800to1400', 'DY800to1400', '/ZToMuMu_NNPDF31_13TeV-powheg_M_800_1400/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000, 72, 1., 0.017075, k_factor=1.),
    sample('dy1400to2300','DY1400to2300', '/ZToMuMu_NNPDF31_13TeV-powheg_M_1400_2300/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000, 70 , 1., 1.366E-3,    k_factor=1.),
    sample('dy2300to3500','DY2300to3500', '/ZToMuMu_NNPDF31_13TeV-powheg_M_2300_3500/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000, 70 , 1., 8.178E-5,    k_factor=1.),
    sample('dy3500to4500','DY3500to4500', '/ZToMuMu_NNPDF31_13TeV-powheg_M_3500_4500/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000, 70 , 1., 3.191E-6,    k_factor=1.),
    sample('dy4500to6000','DY4500to6000', '/ZToMuMu_NNPDF31_13TeV-powheg_M_4500_6000/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000, 70 , 1., 2.787E-7,    k_factor=1.),
    sample('dy6000toInf','DY6000toInf', '/ZToMuMu_NNPDF31_13TeV-powheg_M_6000_Inf/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000, 70 , 1., 9.569E-9,    k_factor=1.),

    # Following samples contain fix for tracker endcap misalignment issue
    sample('dy50to120_MUOTrkFix',   'DY50to120', '/ZToMuMu_NNPDF31_13TeV-powheg_M_50_120/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 2863000, 209 , 1., 2112.905,   k_factor=1.),
    sample('dy120to200_MUOTrkFix',  'DY120to200', '/ZToMuMu_NNPDF31_13TeV-powheg_M_120_200/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 210, 1., 20.553, k_factor=1.),
    sample('dy200to400_MUOTrkFix',  'DY200to400', '/ZToMuMu_NNPDF31_13TeV-powheg_M_200_400/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 211, 1., 2.8861, k_factor=1.),
    sample('dy400to800_MUOTrkFix',  'DY400to800', '/ZToMuMu_NNPDF31_13TeV-powheg_M_400_800/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 212, 1., 0.25126, k_factor=1.),
    sample('dy800to1400_MUOTrkFix', 'DY800to1400', '/ZToMuMu_NNPDF31_13TeV-powheg_M_800_1400/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 72, 1., 0.017075, k_factor=1.),
    sample('dy1400to2300_MUOTrkFix','DY1400to2300', '/ZToMuMu_NNPDF31_13TeV-powheg_M_1400_2300/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 70 , 1., 1.366E-3,    k_factor=1.),
    sample('dy2300to3500_MUOTrkFix','DY2300to3500', '/ZToMuMu_NNPDF31_13TeV-powheg_M_2300_3500/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 70 , 1., 8.178E-5,    k_factor=1.),
    sample('dy3500to4500_MUOTrkFix','DY3500to4500', '/ZToMuMu_NNPDF31_13TeV-powheg_M_3500_4500/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 70 , 1., 3.191E-6,    k_factor=1.),
    sample('dy4500to6000_MUOTrkFix','DY4500to6000', '/ZToMuMu_NNPDF31_13TeV-powheg_M_4500_6000/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 70 , 1., 2.787E-7,    k_factor=1.),
    sample('dy6000toInf_MUOTrkFix','DY6000toInf', '/ZToMuMu_NNPDF31_13TeV-powheg_M_6000_Inf/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 70 , 1., 9.569E-9,    k_factor=1.),

    
    # Diboson
     sample('WW', 'WW', '/WW_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 7791498, 208, 1.,63.21 , k_factor=1.),#NLO from MCFM
     sample('WZ', 'WZ', '/WZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 3928630, 98, 1., 22.82, k_factor=1.),#NLO from MCFM
     sample('ZZ', 'ZZ', '/ZZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 1949768, 94, 1., 10.32, k_factor=1.),#NLO from MCFM

     # WW binned in mass
     # Why are all the cross sections 10.48 on XSDB?
     #sample('WW','WW_200to600','/WWTo2L2Nu_Mll_200To600_13TeV-powheg/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM', 200000, 208, 1., 10.48, k_factor=1.), 
     #sample('WW','WW_600to1200','/WWTo2L2Nu_Mll_600To1200_13TeV-powheg/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM', 200000, 208, 1., 10.48, k_factor=1.), 
     #sample('WW','WW_1200to2500','/WWTo2L2Nu_Mll_1200To2500_13TeV-powheg/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM', 200000, 208, 1., 10.48, k_factor=1.), 
     #sample('WW','WW_2500toInf','/WWTo2L2Nu_Mll_2500ToInf_13TeV-powheg/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM', 38969, 208, 1., 10.48, k_factor=1.), 

     # ttbar
	 sample('ttbar','ttbar','/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',66979742,4,1.,72.1,k_factor=1.),
     # Still need ttbar binned in mass samples
     #sample('ttbar','ttbar_500to800','/TTToLL_MLL_500To800_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM', 200000, 4, 1, 76.63, k_factor=1.),
     #sample('ttbar','ttbar_800to1200','/TTToLL_MLL_800To1200_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM', 200000, 4, 1, 76.63, k_factor=1.),
     #sample('ttbar','ttbar_1200to1800','/TTToLL_MLL_1200To1800_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM', 200000, 4, 1, 76.63, k_factor=1.),
     #sample('ttbar','ttbar_1800toInf','/TTToLL_MLL_1200To1800_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM', 200000, 4, 1, 76.63, k_factor=1.),

     # Single Top
     sample('tW',     'tW', '/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',7660001,66 , 1., 34.91, k_factor=1.),#already NNLO xs
     sample('tbarW',     'tbarW', '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',7993682,66 , 1., 34.91, k_factor=1.),#already NNLO xs
 

    # As of 16 July 18:41 W+jets samples are still in production
 	#sample('Wjets', 'Wjets', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',XXXX,52,1.,56000,k_factor=1),#already NNLO xs
 	#sample('Wjets', 'Wjets', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM',XXXX,52,1.,56000,k_factor=1),#already NNLO xs
 	#sample('Wjets', 'Wjets', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM',XXXX,52,1.,56000,k_factor=1),#already NNLO xs # no PU?

	# What is XS? the madgraphMLM sample has xs=14420 on MCM but nothing for the amcatnloFXFX sample
 	#sample('dyInclusive50', 'DYInclusive50', '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 27413121, 209 , 1., 5765.4,    k_factor=1., is_madgraph=True),  
 	#sample('dyInclusive50', 'DYInclusive50', '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 182359906, 209 , 1., 5765.4,    k_factor=1., is_madgraph=True),  
 


# ###    sample('qcd50to80', 'QCD50to80', '/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 9954370,43,1.,1,k_factor=1),
# 	sample('qcd80to120', 'QCD80to120', '/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',6986740,43,1.,2762530,k_factor=1),
#     sample('qcd120to170', 'QCD120to170', '/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',6708572,43,1.,471100,k_factor=1),
#    	sample('qcd170to300', 'QCD170to300', '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',6958708,43,1.,117276,k_factor=1),
#     sample('qcd300to470', 'QCD300to470', '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', 4150588,43,1.,7823,k_factor=1),
#    	sample('qcd470to600', 'QCD470to600', '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',3959986,43,1.,648.2,k_factor=1),
#     sample('qcd600to800', 'QCD600to800', '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',3896412,43,1.,186.9,k_factor=1),
# 	sample('qcd800to1000', 'QCD800to1000', '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',3992112,43,10,32.293,k_factor=1),
#     sample('qcd1000to1400', 'QCD1000to1400', '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',2999069,43,1.,9.4183,k_factor=1),
#     sample('qcd1400to1800', 'QCD1400to1800', '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',396409,43,1.,0.84265,k_factor=1),
#     sample('qcd1800to2400', 'QCD1800to2400', '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',397660,43,1.,0.114943,k_factor=1),
#     sample('qcd2400to3200', 'QCD2400to3200', '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',399226,43,1.,0.00682981,k_factor=1),
#     sample('qcd3200', 'QCD3200', '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v3/MINIAODSIM',391735,43,1.,0.000165445,k_factor=1),
 
# ### 	N_EVENT scaled by: -N_EVENT * n_neg/n + n * n_pos/n (N_EVENT from report = 28968252; n from weight = 9112991 n_neg = 1507200 (0.1654); n_pos = 7605790 (0.8346); )

    ]

samples.reverse()


#if miniAOD:

#else:
# Isn't ana_dataset made obsolete by the switch to MiniAOD?
for sample in samples:
   exec '%s = sample' % sample.name
   if not miniAOD:
	   pass
       #sample.ana_dataset = '/%s/rradogna-datamc_%s-c4b4ec8fa143ea00cec443e9d0afb38f/USER'  % (sample.dataset.split('/')[1], sample.name)
   else:
	   pass
       #sample.ana_dataset = '/'+ sample.dataset.split('/')[1]+ '/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM'

#dy100to200.ana_dataset = '/DYJetsToLL_M-100to200_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_dy100to200-1e36332d8badf10b79a5027340f46eb1/USER'
#dy200to400.ana_dataset = '/DYJetsToLL_M-200to400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_dy200to400-1e36332d8badf10b79a5027340f46eb1/USER'
#dy400to500.ana_dataset = '/DYJetsToLL_M-400to500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_dy400to500-1e36332d8badf10b79a5027340f46eb1/USER'
#dy500to700.ana_dataset = '/DYJetsToLL_M-500to700_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_dy500to700-1e36332d8badf10b79a5027340f46eb1/USER'
#dy700to800.ana_dataset = '/DYJetsToLL_M-700to800_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_dy700to800-1e36332d8badf10b79a5027340f46eb1/USER'
#dy800to1000.ana_dataset = '/DYJetsToLL_M-800to1000_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_dy800to1000-1e36332d8badf10b79a5027340f46eb1/USER'
#dy1000to1500.ana_dataset = '/DYJetsToLL_M-1000to1500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_dy1000to1500-1e36332d8badf10b79a5027340f46eb1/USER'
#dy1500to2000.ana_dataset = '/DYJetsToLL_M-1500to2000_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_dy1500to2000-1e36332d8badf10b79a5027340f46eb1/USER'
#dy2000to3000.ana_dataset = '/DYJetsToLL_M-2000to3000_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/rradogna-datamc_dy2000to3000-1e36332d8badf10b79a5027340f46eb1/USER'

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
