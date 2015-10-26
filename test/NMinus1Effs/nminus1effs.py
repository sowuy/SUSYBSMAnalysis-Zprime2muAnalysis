#!/usr/bin/env python

import sys, os, FWCore.ParameterSet.Config as cms
from SUSYBSMAnalysis.Zprime2muAnalysis.Zprime2muAnalysis_cfg import process
from SUSYBSMAnalysis.Zprime2muAnalysis.HistosFromPAT_cfi import HistosFromPAT
from SUSYBSMAnalysis.Zprime2muAnalysis.OurSelectionDec2012_cff import loose_cut, trigger_match, tight_cut, allDimuons

readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
process.source = cms.Source ("PoolSource",fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( [
                   '/store/user/rradogna/RelValTTbar_13/datamc_ttbar_startup/150730_143116/0000/pat_1.root',
#                   '/store/user/rradogna/RelValZMM_13/datamc_dy50_startup/150730_143145/0000/pat_1.root'
                   ] );


secFiles.extend( [
               ] )

process.maxEvents.input = -1

# Define the numerators and denominators, removing cuts from the
# allDimuons maker. "NoX" means remove cut X entirely (i.e. the
# loose_cut denominators), "TiX" means move cut X from the loose_cut
# to the tight_cut (meaning only one muon instead of two has to pass
# the cut).  "NoNo" means remove nothing (i.e. the numerator). This
# will break if loose_, tight_cut strings are changed upstream, so we
# try to check those with a simple string test below.

cuts = [
    ('Pt',      'pt > 53'),
    ('DB',      'abs(dB) < 0.2'),
    ('Iso',     'isolationR03.sumPt / innerTrack.pt < 0.10'),
    ('TkLayers','globalTrack.hitPattern.trackerLayersWithMeasurement > 5'),
    ('PxHits',  'globalTrack.hitPattern.numberOfValidPixelHits >= 1'),
    ('MuHits',  'globalTrack.hitPattern.numberOfValidMuonHits > 0'),
    ('MuMatch', ('numberOfMatchedStations > 1', 'isTrackerMuon')),
    ]

for name, cut in cuts:
    if type(cut) != tuple:
        cut = (cut,)

    lc = loose_cut
    for c in cut:
        if c not in lc:
            raise ValueError('cut "%s" not in cut string "%s"' % (c, lc))
        lc = lc.replace(' && ' + c, '') # Relies on none of the cuts above being first in the list.

    obj_no = allDimuons.clone(loose_cut = lc)
#    obj_no = allDimuons.clone(loose_cut = lc,tight_cut = tight_cut.replace(trigger_match, ''))#N-2
    setattr(process, 'allDimuonsNo' + name, obj_no)
    
    obj_ti = obj_no.clone(tight_cut = tight_cut + ' && ' + ' && '.join(cut))
    setattr(process, 'allDimuonsTi' + name, obj_ti)

process.allDimuonsNoNo      = allDimuons.clone()
#process.allDimuonsNoNo      = allDimuons.clone(tight_cut = tight_cut.replace(trigger_match, ''))#N-2
process.allDimuonsNoTrgMtch = allDimuons.clone(tight_cut = tight_cut.replace(trigger_match, ''))

alldimus = [x for x in dir(process) if 'allDimuonsNo' in x or 'allDimuonsTi' in x]

# Sanity check that the replaces above did something.
for x in alldimus:
    if 'NoNo' in x:
        continue
    o = getattr(process, x)
    assert o.loose_cut.value() != loose_cut or o.tight_cut.value() != tight_cut

process.p = cms.Path(process.goodDataFilter * process.muonPhotonMatch * process.leptons * reduce(lambda x,y: x*y, [getattr(process, x) for x in alldimus]))

# For all the allDimuons producers, make dimuons producers, and
# analyzers to make the histograms.
for alld in alldimus:
    dimu = process.dimuons.clone(src = alld)
    name = alld.replace('allD', 'd')
    setattr(process, name, dimu)
    hists = HistosFromPAT.clone(dilepton_src = name, leptonsFromDileptons = True)
    setattr(process, name.replace('dimuons', ''), hists)
    process.p *= dimu * hists

# Handle the cuts that have to be applied at the
# Zprime2muCompositeCandidatePicker level.
#process.allDimuonsN2 = allDimuons.clone(tight_cut = tight_cut.replace(trigger_match, ''))#N-2
#process.p *= process.allDimuonsN2#N-2
process.dimuonsNoB2B     = process.dimuons.clone()
process.dimuonsNoVtxProb = process.dimuons.clone()
process.dimuonsNoDptPt   = process.dimuons.clone()
#process.dimuonsNoB2B     = process.dimuons.clone(src = 'allDimuonsN2')#N-2
#process.dimuonsNoVtxProb = process.dimuons.clone(src = 'allDimuonsN2')#N-2
#process.dimuonsNoDptPt   = process.dimuons.clone(src = 'allDimuonsN2')#N-2
delattr(process.dimuonsNoB2B,     'back_to_back_cos_angle_min')
delattr(process.dimuonsNoVtxProb, 'vertex_chi2_max')
delattr(process.dimuonsNoDptPt,   'dpt_over_pt_max')
process.p *= process.allDimuons
for dimu in ['dimuonsNoB2B', 'dimuonsNoVtxProb', 'dimuonsNoDptPt']:
    hists = HistosFromPAT.clone(dilepton_src = dimu, leptonsFromDileptons = True)
    setattr(process, dimu.replace('dimuons', ''), hists)
    process.p *= getattr(process, dimu) * hists

# Special case to remove |dB| and B2B cuts simultaneously, as they can
# be correlated (anti-cosmics).
process.allDimuonsNoCosm = process.allDimuons.clone(loose_cut = loose_cut.replace(' && abs(dB) < 0.2', ''))
#process.allDimuonsNoCosm = process.allDimuons.clone(loose_cut = loose_cut.replace(' && abs(dB) < 0.2', ''), tight_cut = tight_cut.replace(trigger_match, '')) #N-2
process.dimuonsNoCosm = process.dimuons.clone(src = 'allDimuonsNoCosm')
delattr(process.dimuonsNoCosm, 'back_to_back_cos_angle_min')
process.NoCosm = HistosFromPAT.clone(dilepton_src = 'dimuonsNoCosm', leptonsFromDileptons = True)
process.p *= process.allDimuonsNoCosm * process.dimuonsNoCosm * process.NoCosm

if __name__ == '__main__' and 'submit' in sys.argv:
    crab_cfg = '''
from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'ana_nminus1_%(name)s'
config.General.workArea = 'crab'
#config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'nminus1effs.py'
#config.JobType.priority = 1

config.Data.inputDataset =  '%(ana_dataset)s'
config.Data.publishDataName = 'ana_nminus1_%(name)s'
config.Data.inputDBS = 'phys03'
job_control
config.Data.publication = False
config.Data.outLFNDirBase = '/store/user/cschnaib'

config.Site.storageSite = 'T2_CH_CERN'

'''

#config.General.requestName = 'ana_nminus1_%(name)s_%(spacing)s'
#config.Data.publishDataName = 'ana_nminus1_%(name)s_%(spacing)s'


    just_testing = 'testing' in sys.argv
    if not 'no_data' in sys.argv:
        from SUSYBSMAnalysis.Zprime2muAnalysis.goodlumis import Run2015MuonsOnly25ns_ll, Run2015MuonsOnly50ns_ll

        dataset_details = [
#            ('SingleMuonRun2015B-Prompt_251162_251499',    '/SingleMuon/rradogna-datamc_SingleMuonRun2015B-Prompt_251162_251499_20150713100409-3aa7688518cb1f1b044caf15b1a9ed05/USER','74X_dataRun2_Prompt_v0','50ns'),
#            ('SingleMuonRun2015B-Prompt_251500_251603',    '/SingleMuon/rradogna-datamc_SingleMuonRun2015B-Prompt_251500_251603_20150718235715-9996471c14459acaec01707975d1e954/USER','74X_dataRun2_Prompt_v0','50ns'),
#            ('SingleMuonRun2015B-Prompt_251613_251883',    '/SingleMuon/rradogna-datamc_SingleMuonRun2015B-Prompt_251613_251883_20150719000207-9996471c14459acaec01707975d1e954/USER','74X_dataRun2_Prompt_v0','50ns'),

#            ('SingleMuonRun2015C-Prompt_253888_254914',    '/SingleMuon/rradogna-datamc_SingleMuonRun2015C-Prompt_253888_254914_20150831150018-681693e882ba0f43234b3b41b1bbc39d/USER','74X_dataRun2_Prompt_v1','50ns'),
#             ('SingleMuonRun2015C-Prompt_253888_254914',    '/SingleMuon/rradogna-datamc_SingleMuonRun2015C-Prompt_253888_254914_20150831150018-681693e882ba0f43234b3b41b1bbc39d/USER','74X_dataRun2_Prompt_v1','25ns'),

#              ('SingleMuonRun2015D-Prompt_256629_258158',    '/SingleMuon/rradogna-datamc_SingleMuonRun2015D-Prompt_256629_258158_20151013000746-c9b39dd88dc98b683a1d7cecc8f6c42c/USER','74X_dataRun2_Prompt_v2','25ns'),
              ('SingleMuonRun2015D-Prompt_258159_258750',    '/SingleMuon/rradogna-datamc_SingleMuonRun2015D-Prompt_258159_258750_20151021181222-c9b39dd88dc98b683a1d7cecc8f6c42c/USER','74X_dataRun2_Prompt_v2','25ns'),
            ]


        for name, ana_dataset, gtag, spacing in dataset_details:
            print name, gtag, spacing

            if spacing == '25ns':
                Run2015MuonsOnly25ns_ll.writeJSON('tmp.json')
            if spacing == '50ns':
                Run2015MuonsOnly50ns_ll.writeJSON('tmp.json')

            new_py = open('nminus1effs.py').read()
            new_py += "\nprocess.GlobalTag.globaltag = '%s'\n"%(gtag)
            open('nminus1effs_crab.py', 'wt').write(new_py)

            new_crab_cfg = crab_cfg % locals()
            job_control = '''
config.Data.splitting = 'LumiBased'
config.Data.totalUnits = -1
config.Data.unitsPerJob = 100
config.Data.lumiMask = 'tmp.json' ####### use lumiMask as defined in goodlumis.py
#config.Data.runRange = '246908-258159' # to ensure that the last dataset gets run over
#config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions15/13TeV/Cert_254833_13TeV_PromptReco_Collisions15_JSON.txt'
'''
            new_crab_cfg = new_crab_cfg.replace('job_control', job_control)
            open('crabConfig.py', 'wt').write(new_crab_cfg)

            if not just_testing:
                os.system('crab submit -c crabConfig.py') #--dryrun
            if just_testing:
                os.system('crab submit -c crabConfig.py --dryrun')

        if not just_testing:
            os.system('rm crabConfig.py nminus1effs_crab.py nminus1effs_crab.pyc tmp.json crabConfig.pyc')

    if not 'no_mc' in sys.argv:
        crab_cfg = crab_cfg.replace('job_control','''
config.Data.splitting = 'EventAwareLumiBased'
config.Data.totalUnits = -1
config.Data.unitsPerJob  = 10000
''')

        from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import *
        #samples =[inclmu15]
        #samples =[wjets]
        #samples =[wz,ww_incl,zz_incl,wjets,tWantitop,tWtop,dy2300to3500,DY3500to4500Powheg,dy4500to6000,zpsi5000]
        #samples =[dy50to120,DY120to200Powheg,DY200to400Powheg,DY400to800Powheg,DY800to1400Powheg,dy1400to2300, ttbar_pow]#,ttbar, wz, ww_incl, zz_incl, dy50to120]
        #samples =[dy50, dy120, dy200, dy400, dy800, dy1400, dy2300, dy3500, dy4500, dy6000, dy7500, dy8500, dy9500, zpsi5000, ttbar, inclmu15]
        #samples = [dy50to120_s,dy120to200_s,dy200to400_s,dy400to800_s,dy800to1400_s,dy1400to2300_s,dy2300to3500_s,dy3500to4500_s,dy4500to6000_s,dy6000_s]#,zpsi5000_s]
        #samples = [qcd50to80,qcd80to120,qcd120to170,qcd170to300,qcd300to470,qcd470to600,qcd800to1000,qcd1000to1400,qcd1400to1800,qcd1800to2400,qcd3200]
        #samples = [zpsi5000_s,zpsi5000]
        samples = [zpsi5000_s,dy120to200_s,dy800to1400_s,dy3500to4500_s,qcd50to80,qcd80to120,qcd1800to2400]
        for sample in samples:
            print sample.name
            open('crabConfig.py', 'wt').write(crab_cfg % sample)
            if not just_testing:
                os.system('crab submit -c crabConfig.py')
            if just_testing:
                os.system('crab submit -c crabConfig.py --dryrun')

        if not just_testing:
            os.system('rm crabConfig.py crabConfig.pyc')





#            ('SingleMuonRun2015C-Prompt_253888_254914',    '/SingleMuon/rradogna-datamc_SingleMuonRun2015C-Prompt_253888_254914_20150831150018-681693e882ba0f43234b3b41b1bbc39d/USER','74X_dataRun2_Prompt_v1','25ns'),

#            ('SingleMuonRun2015D-Prompt_256629_256842',    '/SingleMuon/rradogna-datamc_SingleMuonRun2015D-Prompt_256629_256842_20150926113604-c9b39dd88dc98b683a1d7cecc8f6c42c/USER','74X_dataRun2_Prompt_v2','25ns'),
#            ('SingleMuonRun2015D-Prompt_256843_257819',    '/SingleMuon/rradogna-datamc_SingleMuonRun2015D-Prompt_256843_257819_20151002140028-c9b39dd88dc98b683a1d7cecc8f6c42c/USER','74X_dataRun2_Prompt_v2', '25ns'),
#            ('SingleMuonRun2015D-Prompt_257820_258157',    '/SingleMuon/rradogna-datamc_SingleMuonRun2015D-Prompt_257820_258157_20151004232715-c9b39dd88dc98b683a1d7cecc8f6c42c/USER','74X_dataRun2_Prompt_v2', '25ns'),
#            ('SingleMuonRun2015D-Prompt_258158_258158',    '/SingleMuon/rradogna-datamc_SingleMuonRun2015D-Prompt_258158_258158_20151009194535-c9b39dd88dc98b683a1d7cecc8f6c42c/USER','74X_dataRun2_Prompt_v2', '25ns'),
#            ('SingleMuonRun2015D-Prompt_258159_258432',    '/SingleMuon/rradogna-datamc_SingleMuonRun2015D-Prompt_258159_258432_20151009203706-c9b39dd88dc98b683a1d7cecc8f6c42c/USER','74X_dataRun2_Prompt_v2', '25ns'),
 #           ('SingleMuonRun2015D-Prompt_256629_258158',    '/SingleMuon/rradogna-datamc_SingleMuonRun2015D-Prompt_256629_258158_20151013000746-c9b39dd88dc98b683a1d7cecc8f6c42c/USER','74X_dataRun2_Prompt_v1','25ns'),

 #           ('SingleMuonRun2015D-Prompt_258159_258432',    '/SingleMuon/rradogna-datamc_SingleMuonRun2015D-Prompt_258159_258432_20151009203706-c9b39dd88dc98b683a1d7cecc8f6c42c/USER','74X_dataRun2_Prompt_v1','25ns'),
