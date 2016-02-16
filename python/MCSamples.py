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
           #sample('dy50to120',     'DY50to120', '/ZToMuMu_NNPDF30_13TeV-powheg_M_50_120/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 2898838, 209 , 1., 1975, k_factor=1.),
           #sample('dy120to200',    'DY120to200', '/ZToMuMu_NNPDF30_13TeV-powheg_M_120_200/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 100000, 210, 1., 19.32, k_factor=1.),
           sample('dy200to400',    'DY200to400', '/ZToMuMu_NNPDF30_13TeV-powheg_M_200_400/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 100000, 211, 1., 2.731, k_factor=1.),
           # sample('dy400to800',    'DY400to800', '/ZToMuMu_NNPDF30_13TeV-powheg_M_400_800/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 100000, 212, 1., 0.241, k_factor=1.),
          #  sample('dy800to1400',    'DY800to1400', '/ZToMuMu_NNPDF30_13TeV-powheg_M_800_1400/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 100000, 72, 1., 0.01678, k_factor=1.),
           # sample('dy1400to2300',    'DY1400to2300', '/ZToMuMu_NNPDF30_13TeV-powheg_M_1400_2300/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 99600, 71 , 1., 0.00139, k_factor=1.),
           # sample('dy2300to3500',    'DY2300to3500', '/ZToMuMu_NNPDF30_13TeV-powheg_M_2300_3500/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 100000, 70 , 1., 0.00008948, k_factor=1.),
           # sample('dy3500to4500',    'DY3500to4500', '/ZToMuMu_NNPDF30_13TeV-powheg_M_3500_4500/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM', 100000, 30, 1., 0.0000041, k_factor=1.),
            # sample('dy4500to6000',    'DY4500to6000', '/ZToMuMu_NNPDF30_13TeV-powheg_M_4500_6000/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v3/AODSIM',100000, 31 , 1., 4.56E-7, k_factor=1.),
    
           #sample('ttbar_pow_s',     't#bar{t}', '/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM', 19869898, 4 , 1., 815.96, k_factor=1.),
           # sample('tWantitop_s', 'tWantiTop',        '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM',1000000,63 , 1., 35.6, k_factor=1.),
           #sample('tWtop_s',     'tWTop',            '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM',999200,66 , 1., 35.6, k_factor=1.),
           #sample('wz_s',        'WZ',               '/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM', 1000000, 98, 1., 66.1, k_factor=1.),
           #sample('zz_incl_s',   'ZZ',               '/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM', 988880,  94, 1., 15.4, k_factor=1.),
           #sample('ww_incl_s',  'WW',               '/WW_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Startup25ns_EXOReReco_74X_Spring15_mcRun2_startup25ns_v0-v1/AODSIM', 994416,   91, 1., 118.7 , k_factor=1. ),
    
    ]

samples.reverse()

for sample in samples:
    exec '%s = sample' % sample.name
    # print sample.dataset.split('/')[1]


#dy50to120.ana_dataset ='/ZToMuMu_NNPDF30_13TeV-powheg_M_50_120/alfloren-dy50to120-f1c862f6f3d7656594801a05b2168a1c/USER'
#dy120to200.ana_dataset ='/ZToMuMu_NNPDF30_13TeV-powheg_M_120_200/alfloren-dy120to200-f1c862f6f3d7656594801a05b2168a1c/USER'
#dy200to400.ana_dataset ='/ZToMuMu_NNPDF30_13TeV-powheg_M_200_400/alfloren-dy200to400-f1c862f6f3d7656594801a05b2168a1c/USER'
#dy400to800.ana_dataset ='ZToMuMu_NNPDF30_13TeV-powheg_M_400_800/alfloren-dy400to800-f1c862f6f3d7656594801a05b2168a1c/USER'
#dy800to1400.ana_dataset ='ZToMuMu_NNPDF30_13TeV-powheg_M_800_1400/alfloren-dy800to1400-f1c862f6f3d7656594801a05b2168a1c/USER'
#dy1400to2300.ana_dataset ='/ZToMuMu_NNPDF30_13TeV-powheg_M_1400_2300/alfloren-dy1400to2300-f1c862f6f3d7656594801a05b2168a1c/USER'
#dy2300to3500.ana_dataset ='/ZToMuMu_NNPDF30_13TeV-powheg_M_2300_3500/alfloren-dy2300to3500-f1c862f6f3d7656594801a05b2168a1c/USER'
#dy3500to4500.ana_dataset ='/ZToMuMu_NNPDF30_13TeV-powheg_M_3500_4500/alfloren-dy3500to4500-f1c862f6f3d7656594801a05b2168a1c/USER'
#dy4500to6000.ana_dataset ='/ZToMuMu_NNPDF30_13TeV-powheg_M_4500_6000/alfloren-dy4500to6000-f1c862f6f3d7656594801a05b2168a1c/USER'
    


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
