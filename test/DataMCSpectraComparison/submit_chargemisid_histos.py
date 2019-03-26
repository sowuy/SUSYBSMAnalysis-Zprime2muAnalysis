#!/usr/bin/env python

# customize CRAB request name here
ex = 'chargeMisId_test'

# https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVAnalysisSummaryTable
# 2017
dataGlobalTag = '94X_dataRun2_ReReco_EOY17_v6'
mcGlobalTag = '94X_mc2017_realistic_v17'

import sys, os, FWCore.ParameterSet.Config as cms
from SUSYBSMAnalysis.Zprime2muAnalysis.Zprime2muAnalysis_cff import switch_hlt_process_name
from SUSYBSMAnalysis.Zprime2muAnalysis.Zprime2muAnalysis_cfg import process
from SUSYBSMAnalysis.Zprime2muAnalysis.Zprime2muAnalysis_cff import goodDataFiltersMiniAOD

process.source.fileNames =[
        #'/store/mc/RunIIFall17MiniAODv2/ZToMuMu_NNPDF31_13TeV-powheg_M_800_1400/MINIAODSIM/MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/90000/FCC3FBEB-FAFE-E811-8520-0CC47AF9B32A.root',
        '/store/mc/RunIISummer16MiniAODv2/ZToMuMu_NNPDF30_13TeV-powheg_M_6000_Inf/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/408086F7-57D1-E611-97A5-90B11C2CA412.root' 
           ]
process.maxEvents.input = -1

# Legacy ReReco GT for 2017 
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmV2017Analysis#Conditions
# This will be changed in for_data() or for_mc() below
process.GlobalTag.globaltag ='94X_mc2017_realistic_v12' # Run 2017E #change line 52

#process.options.wantSummary = cms.untracked.bool(True)# false di default
process.MessageLogger.cerr.FwkReport.reportEvery = 1000 # default 1000

# Import trigger stuff
from SUSYBSMAnalysis.Zprime2muAnalysis.hltTriggerMatch_cfi import trigger_match, trigger_paths, offline_pt_threshold

# The histogramming module that will be cloned multiple times below
# for making histograms with different cut/dilepton combinations.

from SUSYBSMAnalysis.Zprime2muAnalysis.HistosFromPAT_cfi import HistosFromPAT_MiniAOD as HistosFromPAT
HistosFromPAT.leptonsFromDileptons = True
HistosFromPAT.usekFactor = False #### Set TRUE to use K Factor #####
ZSkim = False #### Set TRUE to skim dy50to120 with a Z pt < 100 GeV #####

# Electron stuff that is necessary even if it isnt used
from SUSYBSMAnalysis.Zprime2muAnalysis.Zprime2muAnalysis_cff import electrons_miniAOD
electrons_miniAOD(process)

# Ntuple base
SimpleNtupler = cms.EDAnalyzer('SimpleNtupler_miniAOD',
                    dimu_src = cms.InputTag('SimpleMuonsAllSigns'), # will be changed below
                    met_src = cms.InputTag("slimmedMETs"),
                    jet_src = cms.InputTag("slimmedJets"),
                    beamspot_src = cms.InputTag('offlineBeamSpot'),
                    vertices_src = cms.InputTag('offlineSlimmedPrimaryVertices'),
                    TriggerResults_src = cms.InputTag('TriggerResults', '', 'PAT'),   #mc
                    #TriggerResults_src = cms.InputTag('TriggerResults', '', 'RECO'), #data
                    genEventInfo = cms.untracked.InputTag('generator'),
                    metFilter = cms.VInputTag(
                        cms.InputTag("Flag_HBHENoiseFilter"),
                        cms.InputTag("Flag_HBHENoiseIsoFilter"),
                        cms.InputTag("Flag_EcalDeadCellTriggerPrimitiveFilter"),
                        cms.InputTag("Flag_eeBadScFilter"),
                        cms.InputTag("Flag_globalTightHalo2016Filter")
                        )
                    )

# These modules define the basic selection cuts. For the monitoring
# sets below, we don't need to define a whole new module, since they
# just change one or two cuts -- see below.
import SUSYBSMAnalysis.Zprime2muAnalysis.OurSelection2016_cff as OurSelection2016
import SUSYBSMAnalysis.Zprime2muAnalysis.ChargeMisIDSelection_cff as ChargeMisIDSelection 

# CandCombiner includes charge-conjugate decays with no way to turn it
# off. To get e.g. mu+mu+ separate from mu-mu-, cut on the sum of the
# pdgIds (= -26 for mu+mu+).
dils = [
    ('MuonsAllSigns',                '%(leptons_name)s:muons@- %(leptons_name)s:muons@-',         ''),
    ]

# Define sets of cuts for which to make plots. If using a selection
# that doesn't have a trigger match, need to re-add a hltHighLevel
# filter somewhere below.
cuts = {
    'ChargeMisID'  : ChargeMisIDSelection,
    }

# Loop over all the cut sets defined and make the lepton, allDilepton
# (combinatorics only), and dilepton (apply cuts) modules for them.
for cut_name, Selection in cuts.iteritems():
    # Keep track of modules to put in the path for this set of cuts.
    path_list = []

    # Unfortunately necessary even if it isn't used :(
    path_list.append(process.egmGsfElectronIDSequence)

    # Clone the LeptonProducer to make leptons with the set of cuts
    # we're doing here flagged.  I.e., muon_cuts in LeptonProducer
    # just marks each muon with a userInt "cutFor" that is 0 if it
    # passes the cuts, and non-0 otherwise; it does not actually drop
    # any of the muons. The cutFor flag actually gets ignored by the
    # LooseTightPairSelector in use for all the cuts above, at
    # present.
    muon_cuts = Selection.loose_cut
    leptons_name = cut_name + 'Leptons'
    leptons = process.leptonsMini.clone(muon_cuts = muon_cuts)
    setattr(process, leptons_name, leptons)
    path_list.append(leptons)

    # Make all the combinations of dileptons we defined above.
    for dil_name, dil_decay, dil_cut in dils:

        # Unique names for the modules: allname for the allDileptons,
        # and name for dileptons.
        name = cut_name + dil_name
        allname = 'all' + name

        alldil = Selection.allDimuons.clone(decay = dil_decay % locals(), cut = dil_cut)
        if 'AllSigns' in dil_name:
            alldil.checkCharge = cms.bool(False)

        dil = Selection.dimuons.clone(src = cms.InputTag(allname))

        # Histos now just needs to know which leptons and dileptons to use.
        histos = HistosFromPAT.clone(lepton_src = cms.InputTag(leptons_name, 'muons'), dilepton_src = cms.InputTag(name))
        ntuple = SimpleNtupler.clone(dimu_src = cms.InputTag(name))

        # Add all these modules to the process and the path list.
        setattr(process, allname, alldil)
        setattr(process, name, dil)
        setattr(process, name + 'Histos', histos)
        setattr(process, name + 'Ntuple', ntuple)
        path_list.append(alldil * dil * histos * ntuple)

    # Finally, make the path for this set of cuts.
    pathname = 'path' + cut_name
    process.load("SUSYBSMAnalysis.Zprime2muAnalysis.EventCounter_cfi")
    pobj = process.EventCounter * process.muonPhotonMatchMiniAOD * reduce(lambda x,y: x*y, path_list)

    path = cms.Path(pobj)
    setattr(process, pathname, path)

def add_filters(process,is_mc=True):
    for cut_name, Selection in cuts.iteritems():
        path_name = 'path'+cut_name
        if hasattr(process,path_name) and cut_name != 'Simple':
            process.load('SUSYBSMAnalysis.Zprime2muAnalysis.goodData_cff')
            for dataFilter in goodDataFiltersMiniAOD:
                if is_mc:
                    dataFilter.src = cms.InputTag('TriggerResults','','PAT') # to submit MC
                getattr(process,path_name).insert(0,dataFilter)

def ntuplify(process, is_mc = True):
    # Function for customizing ntuple for data and mc
    if is_mc:
        process.load('SUSYBSMAnalysis.Zprime2muAnalysis.PrunedMCLeptons_cfi')
        obj = process.prunedMCLeptons
        obj.src = cms.InputTag('prunedGenParticles')
        from SUSYBSMAnalysis.Zprime2muAnalysis.HardInteraction_cff import hardInteraction
        for cut_name, Selection in cuts.iteritems():
            getattr(process,'path'+cut_name).insert(0,obj) 
            for dil_name, dil_decay, dil_cut in dils:
                getattr(process,cut_name+dil_name+'Ntuple').hardInteraction = hardInteraction
    else:
        for cut_name, Selection in cuts.iteritems():
            for dil_name, dil_decay, dil_cut in dils:
                getattr(process,cut_name+dil_name+'Ntuple').TriggerResults_src = cms.InputTag('TriggerResults', '', 'RECO')

def for_data(process):
    process.GlobalTag.globaltag = dataGlobalTag
    # Add filters
    add_filters(process,is_mc=False)
    # Customize ntuple for data
    ntuplify(process,is_mc=False)

def for_mc(process, hlt_process_name):
    process.GlobalTag.globaltag = mcGlobalTag
    # Add filters
    add_filters(process)
    # customize ntuple for mc
    ntuplify(process)
    # this must be done last (i.e. after anything that might have an InputTag for something HLT-related)
    switch_hlt_process_name(process, hlt_process_name)

if 'int_data' in sys.argv:
    for_data(process)
    
if 'int_mc' in sys.argv:
    for_mc(process, 'HLT')
    
#f = file('outfile_histos1', 'w')
#f.write(process.dumpPython())
#f.close()

if __name__ == '__main__' and 'submit' in sys.argv:
    crab_cfg = '''
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()
config.General.requestName = 'ana_datamc_%(name)s%(extra)s'
config.General.workArea = 'crab'
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'histos_crab.py'   
config.Data.inputDataset =  '%(ana_dataset)s'
config.Data.inputDBS = 'global'
job_control
config.Data.publication = False
config.Data.outputDatasetTag = 'ana_datamc_%(name)s%(extra)s'
config.Data.outLFNDirBase = '/store/user/'+getUsernameFromSiteDB()
config.Site.storageSite = 'T2_CH_CERN'
'''
    
    just_testing = 'testing' in sys.argv
    extra = '_'+ex if ex!='' else ''
        
    # Run on data.
    if 'no_data' not in sys.argv:
        from SUSYBSMAnalysis.Zprime2muAnalysis.goodlumis import *

        dataset_details = [
                ('SingleMuonRun2017B-31Mar2018-v1', '/SingleMuon/Run2017B-31Mar2018-v1/MINIAOD'),
                ('SingleMuonRun2017C-31Mar2018-v1', '/SingleMuon/Run2017C-31Mar2018-v1/MINIAOD'),
                ('SingleMuonRun2017D-31Mar2018-v1', '/SingleMuon/Run2017D-31Mar2018-v1/MINIAOD'),
                ('SingleMuonRun2017E-31Mar2018-v1', '/SingleMuon/Run2017E-31Mar2018-v1/MINIAOD'),
                ('SingleMuonRun2017F-31Mar2018-v1', '/SingleMuon/Run2017F-31Mar2018-v1/MINIAOD'),
            ]

        lumi_lists = ['Run2017MuonsOnly']

        jobs = []
        for lumi_name in lumi_lists:
            ll = eval(lumi_name + '_ll') if lumi_name != 'NoLumiMask' else None
            for dd in dataset_details:
                jobs.append(dd + (lumi_name, ll))
                
        for dataset_name, ana_dataset, lumi_name, lumi_list in jobs:
            json_fn = 'tmp.json'
            lumi_list.writeJSON(json_fn)
            lumi_mask = json_fn

            name = '%s_%s' % (lumi_name, dataset_name)
            print name

            new_py = open('submit_chargemisid_histos.py').read()
            new_py += "\nfor_data(process)\n"
            open('histos_crab.py', 'wt').write(new_py)

            new_crab_cfg = crab_cfg % locals()

            job_control = '''
config.Data.splitting = 'Automatic'
config.Data.lumiMask = '%(lumi_mask)s'
''' % locals()

            new_crab_cfg = new_crab_cfg.replace('job_control', job_control)
            open('crabConfig.py', 'wt').write(new_crab_cfg)

            if not just_testing:
                os.system('crab submit -c crabConfig.py')
            else:
                cmd = 'diff histos.py histos_crab.py | less'
                print cmd
                os.system(cmd)
                cmd = 'less crab.py'
                print cmd
                os.system(cmd)

        if not just_testing:
            os.system('rm crabConfig.py crabConfig.pyc histos_crab.py histos_crab.pyc tmp.json')

    if 'no_mc' not in sys.argv:
        # Set crab_cfg for MC.
        crab_cfg = crab_cfg.replace('job_control','''
config.Data.splitting = 'EventAwareLumiBased'
config.Data.totalUnits = -1
config.Data.unitsPerJob = %(neventsperjob)s
''')
       
        from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples
        for sample in samples:
            name = sample.name
            ana_dataset = sample.dataset
            if 'dy800to1400' not in name: continue
            print name

            new_py = open('submit_chargemisid_histos.py').read()
            new_py += "\nfor_mc(process,'HLT')\n"
            open('histos_crab.py', 'wt').write(new_py)

            neventsperjob = 10000 if 'dy' in name else 200000
            print crab_cfg
            open('crabConfig.py', 'wt').write(crab_cfg % locals())

            if not just_testing:
                os.system('crab submit -c crabConfig.py')
            else:
                cmd = 'diff histos.py histos_crab.py | less'
                print cmd
                os.system(cmd)
                cmd = 'less crabConfig.py'
                print cmd
                os.system(cmd)
            if not just_testing:
                os.system('rm crabConfig.py crabConfig.pyc histos_crab.py histos_crab.pyc')


