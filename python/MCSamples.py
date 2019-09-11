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

    # 2017 DY MC no tracker endcap fix
    #sample('dy50to120',   'DY50to120', '/ZToMuMu_NNPDF31_13TeV-powheg_M_50_120/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM', 2961000, 209 , 1., 2112.905,   k_factor=1.),
    #sample('dy120to200',  'DY120to200', '/ZToMuMu_NNPDF31_13TeV-powheg_M_120_200/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000, 210, 1., 20.553, k_factor=1.),
    #sample('dy200to400',  'DY200to400', '/ZToMuMu_NNPDF31_13TeV-powheg_M_200_400/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000, 211, 1., 2.8861, k_factor=1.),
    #sample('dy400to800',  'DY400to800', '/ZToMuMu_NNPDF31_13TeV-powheg_M_400_800/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000, 212, 1., 0.25126, k_factor=1.),
    #sample('dy800to1400', 'DY800to1400', '/ZToMuMu_NNPDF31_13TeV-powheg_M_800_1400/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000, 72, 1., 0.017075, k_factor=1.),
    #sample('dy1400to2300','DY1400to2300', '/ZToMuMu_NNPDF31_13TeV-powheg_M_1400_2300/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000, 70 , 1., 1.366E-3,    k_factor=1.),
    #sample('dy2300to3500','DY2300to3500', '/ZToMuMu_NNPDF31_13TeV-powheg_M_2300_3500/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000, 70 , 1., 8.178E-5,    k_factor=1.),
    #sample('dy3500to4500','DY3500to4500', '/ZToMuMu_NNPDF31_13TeV-powheg_M_3500_4500/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000, 70 , 1., 3.191E-6,    k_factor=1.),
    #sample('dy4500to6000','DY4500to6000', '/ZToMuMu_NNPDF31_13TeV-powheg_M_4500_6000/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000, 70 , 1., 2.787E-7,    k_factor=1.),
    #sample('dy6000toInf','DY6000toInf', '/ZToMuMu_NNPDF31_13TeV-powheg_M_6000_Inf/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 100000, 70 , 1., 9.569E-9,    k_factor=1.),

    # Following samples contain fix for tracker endcap misalignment issue
    sample('dy50to120_MUOTrkFix_2017',   'DY50to120', '/ZToMuMu_NNPDF31_13TeV-powheg_M_50_120/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 2863000, 209 , 1., 2112.905,   k_factor=1.),
    sample('dy120to200_MUOTrkFix_2017',  'DY120to200', '/ZToMuMu_NNPDF31_13TeV-powheg_M_120_200/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 210, 1., 20.553, k_factor=1.),
    sample('dy200to400_MUOTrkFix_2017',  'DY200to400', '/ZToMuMu_NNPDF31_13TeV-powheg_M_200_400/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 211, 1., 2.8861, k_factor=1.),
    sample('dy400to800_MUOTrkFix_2017',  'DY400to800', '/ZToMuMu_NNPDF31_13TeV-powheg_M_400_800/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 212, 1., 0.25126, k_factor=1.),
    sample('dy800to1400_MUOTrkFix_2017', 'DY800to1400', '/ZToMuMu_NNPDF31_13TeV-powheg_M_800_1400/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 72, 1., 0.017075, k_factor=1.),
    sample('dy1400to2300_MUOTrkFix_2017','DY1400to2300', '/ZToMuMu_NNPDF31_13TeV-powheg_M_1400_2300/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 70 , 1., 1.366E-3,    k_factor=1.),
    sample('dy2300to3500_MUOTrkFix_2017','DY2300to3500', '/ZToMuMu_NNPDF31_13TeV-powheg_M_2300_3500/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 70 , 1., 8.178E-5,    k_factor=1.),
    sample('dy3500to4500_MUOTrkFix_2017','DY3500to4500', '/ZToMuMu_NNPDF31_13TeV-powheg_M_3500_4500/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 70 , 1., 3.191E-6,    k_factor=1.),
    sample('dy4500to6000_MUOTrkFix_2017','DY4500to6000', '/ZToMuMu_NNPDF31_13TeV-powheg_M_4500_6000/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 70 , 1., 2.787E-7,    k_factor=1.),
    sample('dy6000toInf_MUOTrkFix_2017','DY6000toInf', '/ZToMuMu_NNPDF31_13TeV-powheg_M_6000_Inf/RunIIFall17MiniAODv2-MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', 100000, 70 , 1., 9.569E-9,    k_factor=1.),
    sample('MuonGun_PTOT-5-2500','MuonGun','/MuonGun_PTOT-5-2500/calderon-SingleMuFlatP5To2500_MuonTrackFix_pythia8_cfi_step2_MINIAODSIMoutput-a6b654af77fa2c5986bb260b8225f8a1/USER',100000 , 70 , 1.,2000,k_factor=1.),

     # ttbar
	 #sample('ttbar','ttbar','/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',66979742,4,1.,72.1,k_factor=1.),
     # Still need ttbar binned in mass samples
     #sample('ttbar','ttbar_500to800','/TTToLL_MLL_500To800_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM', 200000, 4, 1, 76.63, k_factor=1.),
     #sample('ttbar','ttbar_800to1200','/TTToLL_MLL_800To1200_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM', 200000, 4, 1, 76.63, k_factor=1.),
     #sample('ttbar','ttbar_1200to1800','/TTToLL_MLL_1200To1800_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM', 200000, 4, 1, 76.63, k_factor=1.),
     #sample('ttbar','ttbar_1800toInf','/TTToLL_MLL_1200To1800_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM', 200000, 4, 1, 76.63, k_factor=1.),


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
