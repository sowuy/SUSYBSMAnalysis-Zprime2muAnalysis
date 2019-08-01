# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step2 --conditions auto:phase1_2017_realistic -s DIGI:pdigi_valid,L1,DIGI2RAW,HLT:@relval2017,RAW2DIGI,L1Reco,RECO --datatier GEN-SIM-RECO -n 10 --geometry DB:Extended --era Run2_2017 --eventcontent FEVTDEBUG --no_exec
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('RECO',eras.Run2_2017)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
#process.load('HLTrigger.Configuration.HLT_2e34v40_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

# Input source
process.source = cms.Source("PoolSource",
    dropDescendantsOfDroppedBranches = cms.untracked.bool(False),
    fileNames = cms.untracked.vstring('file:SingleMuP1000_pythia8_cfi_GEN_SIM.root'),
    inputCommands = cms.untracked.vstring('keep *', 
        'drop *_genParticles_*_*', 
        'drop *_genParticlesForJets_*_*', 
        'drop *_kt4GenJets_*_*', 
        'drop *_kt6GenJets_*_*', 
        'drop *_iterativeCone5GenJets_*_*', 
        'drop *_ak4GenJets_*_*', 
        'drop *_ak7GenJets_*_*', 
        'drop *_ak8GenJets_*_*', 
        'drop *_ak4GenJetsNoNu_*_*', 
        'drop *_ak8GenJetsNoNu_*_*', 
        'drop *_genCandidatesForMET_*_*', 
        'drop *_genParticlesForMETAllVisible_*_*', 
        'drop *_genMetCalo_*_*', 
        'drop *_genMetCaloAndNonPrompt_*_*', 
        'drop *_genMetTrue_*_*', 
        'drop *_genMetIC5GenJs_*_*'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step2 nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.FEVTDEBUGoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-RECO'),
        filterName = cms.untracked.string('')
    ),
    #fileName = cms.untracked.string('step2_DIGI_L1_DIGI2RAW_HLT_RAW2DIGI_L1Reco_RECO.root'),
    fileName = cms.untracked.string('step2_DIGI_L1_DIGI2RAW_RAW2DIGI_L1Reco_RECO.root'),
    outputCommands = process.FEVTDEBUGEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
process.mix.digitizers = cms.PSet(process.theDigitizersValid)
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2017_realistic', '')
process.GlobalTag.toGet = cms.VPSet(
#
# fixed TrackerAlignment scenario (vd mail/thread Patrick Connor 8.Aug.2018)
# fixed for 2018 productions, corrects a huge weak mode (twist-like ?)
# not built within a GT yet to date... will go inside a GT for the ultralegacy rereco of 2017 MC
# -->  TrackerAlignment_Upgrade2017_realistic_v3 
#        cms.PSet(record = cms.string("TrackerAlignmentRcd"),
#                 tag = cms.string("TrackerAlignment_Upgrade2017_realistic_v3"),
#                 connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
#                 )
#
# startup
        cms.PSet(record = cms.string("DTAlignmentRcd"),
                 tag = cms.string("DTAlignment_CRAFT15HWBased_v1_mc"),
                 connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
                 ),
        cms.PSet(record = cms.string("CSCAlignmentRcd"),
                 tag = cms.string("CSCAlignment_CRAFT15HWBased_v1_mc"),
                 connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
                 ),
        cms.PSet(record = cms.string("DTAlignmentErrorExtendedRcd"),
                 tag = cms.string("DTAlignmentErrorsExt_2016_StartupHW_mc"),
                 connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
                 ),
        cms.PSet(record = cms.string("CSCAlignmentErrorExtendedRcd"),
                 tag = cms.string("CSCAlignmentErrorsExt_2016_StartupHW_mc"),
                 connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
                 ),
# zero APE
        cms.PSet(record = cms.string("DTAlignmentErrorExtendedRcd"),
                 tag = cms.string("MuonDTAPEObjectsExtended_v0_mc"),
                 connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
                 ),
        cms.PSet(record = cms.string("CSCAlignmentErrorExtendedRcd"),
                 tag = cms.string("MuonCSCAPEObjectsExtended_v0_mc"),
                 connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
                 )
        )


# Path and EndPath definitions
process.digitisation_step = cms.Path(process.pdigi_valid)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGoutput_step = cms.EndPath(process.FEVTDEBUGoutput)

# Schedule definition
process.schedule = cms.Schedule(process.digitisation_step,process.L1simulation_step,process.digi2raw_step)#,process.HLTSchedule,process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.endjob_step,process.FEVTDEBUGoutput_step)
#process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.endjob_step,process.FEVTDEBUGoutput_step])
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from HLTrigger.Configuration.customizeHLTforMC
#from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 

#call to customisation function customizeHLTforMC imported from HLTrigger.Configuration.customizeHLTforMC
#process = customizeHLTforMC(process)

# End of customisation functions

# Customisation from command line

#Have logErrorHarvester wait for the same EDProducers to finish as those providing data for the OutputModule
#from FWCore.Modules.logErrorHarvester_cff import customiseLogErrorHarvesterUsingOutputCommands
#process = customiseLogErrorHarvesterUsingOutputCommands(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
