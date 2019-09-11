import sys,os
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Submit DIGI-RECO of muon gun samples with user-input energies')
parser.add_argument('-mc','--mcSample',default='MuonGun_P-100',type=str,help='Muon energy in GeV')
parser.add_argument('-s','--submit',action='store_true',help='Submit to CRAB')
parser.add_argument('-dr','--dryRun',action='store_true',help='Make CRAB cfg files but don\'t submit')
parser.add_argument('-x','--extra',type=str,help='Extra name to append to crab request name')
parser.add_argument('-a','--alignment',default='asymptotic',help='Alignment scenario startup or asymptotic')
parser.add_argument('--no_ape',action='store_true',help='Remove APEs')

args = parser.parse_args()

# Change these according to the output of the GEN-SIM step
    
if args.mcSample=='MuonGun_P-50':
    sample = '/MuonGun_P-50/swuycken-MuonGun_P-50_GEN-SIM-75036ba637c5dfa992704e548e933684/USER'
elif args.mcSample=='MuonGun_P-100':
    sample = '/MuonGun_P-100/swuycken-MuonGun_P-100_GEN-SIM-172e789d34388f16d6486ddc174cf948/USER'
elif args.mcSample=='MuonGun_P-300':
    sample = '/MuonGun_P-300/swuycken-MuonGun_P-300_GEN-SIM-9e3ed6671f9a06cd30649ad843ca2780/USER'
elif args.mcSample=='MuonGun_P-500':
    sample = '/MuonGun_P-500/swuycken-MuonGun_P-500_GEN-SIM-cdcd84152118fe658f58c7f9866e6a76/USER'
elif args.mcSample=='MuonGun_P-750':
    sample = '/MuonGun_P-750/swuycken-MuonGun_P-750_GEN-SIM-01f21b301833a2bf82b2511220d83b1e/USER'
elif args.mcSample=='MuonGun_P-1000':
    sample = '/MuonGun_P-1000/swuycken-MuonGun_P-1000_GEN-SIM-c18e2b5607fe29091b18c24090961be2/USER'
elif args.mcSample=='MuonGun_P-1250':
    sample = '/MuonGun_P-1250/swuycken-MuonGun_P-1250_GEN-SIM-4eb532e0fa0266ad4613f9946a6b8831/USER'
elif args.mcSample=='MuonGun_P-1500':
    sample = '/MuonGun_P-1500/swuycken-MuonGun_P-1500_GEN-SIM-b2b7528fc0837f552b37a96a2e026ea2/USER'
elif args.mcSample=='MuonGun_P-2500':
    sample = '/MuonGun_P-2500/cschnaib-MuonGun_P-2500_GEN-SIM-85f827a27d633e29373f39c3c042685f/USER'
elif args.mcSample=='MuonGun_P-3000':
    sample = '/MuonGun_P-3000/cschnaib-MuonGun_P-3000_GEN-SIM-0eb43af79d300b7860b693aac82cf828/USER'
elif args.mcSample=='MuonGun_P-4000':
    sample = '/MuonGun_P-4000/cschnaib-MuonGun_P-4000_GEN-SIM-97553f16a5566c589f4cc968923ca6e3/USER'


APE = ('no' if args.no_ape else '')+'APE'

baseName = args.mcSample
baseName += '_RECO'
baseName += '_'+args.alignment
baseName += '_'+APE
requestName = baseName + ('_'+args.extra if args.extra else '')

ALIGNMENT_APE = ''
if args.alignment=='asymptotic':
    # fixed TrackerAlignment scenario (vd mail/thread Patrick Connor 8.Aug.2018)
    # fixed for 2018 productions, corrects a huge weak mode (twist-like ?)
    # not built within a GT yet to date... will go inside a GT for the ultralegacy rereco of 2017 MC
    # -->  TrackerAlignment_Upgrade2017_realistic_v3 
    # Now included in GT by default: 94X_mc2017_realistic_MuonTrackFix_01
    #ALIGNMENT_APE += '''
    #    cms.PSet(record = cms.string("TrackerAlignmentRcd"),
    #             tag = cms.string("TrackerAlignment_Upgrade2017_realistic_v3"),
    #             connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
    #             ),\n'''

    # removes APEs
    if args.no_ape:
        ALIGNMENT_APE += '''process.GlobalTag.toGet = cms.VPSet(
        cms.PSet(record = cms.string("DTAlignmentErrorExtendedRcd"),
                 tag = cms.string("MuonDTAPEObjectsExtended_v0_mc"),
                 connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
                 ),
        cms.PSet(record = cms.string("CSCAlignmentErrorExtendedRcd"),
                 tag = cms.string("MuonCSCAPEObjectsExtended_v0_mc"),
                 connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
                 )\n)'''
elif args.alignment=='startup':
    # Replace asymptotic with startup conditions 
    ALIGNMENT_APE += '''process.GlobalTag.toGet = cms.VPSet(
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
                 ),\n'''

    # removes APEs
    if args.no_ape:
        ALIGNMENT_APE += '''
        cms.PSet(record = cms.string("DTAlignmentErrorExtendedRcd"),
                 tag = cms.string("MuonDTAPEObjectsExtended_v0_mc"),
                 connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
                 ),
        cms.PSet(record = cms.string("CSCAlignmentErrorExtendedRcd"),
                 tag = cms.string("MuonCSCAPEObjectsExtended_v0_mc"),
                 connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS')
                 ),'''
    ALIGNMENT_APE += '\n)'

else:
    print args.alignment,'not a valid alignment'
    exit()

with open('step2_DIGI_L1_DIGI2RAW_HLT_RAW2DIGI_L1Reco_RECO_CRAB_TMP.py','r') as infile:
    new_py = infile.read()
new_py = new_py.replace('ALIGNMENT_APE',ALIGNMENT_APE)

reco_cfg = baseName+'.py'
with open(reco_cfg,'w') as outfile:
    outfile.write(new_py)

crab_cfg = \
'''from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()
config.General.requestName = '{requestName}'
config.General.workArea = 'crab'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '{reco_cfg}'

config.Data.inputDataset = '{sample}'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.inputDBS = 'phys03'
config.Data.publication = True
config.Data.outputDatasetTag = '{baseName}'
config.Data.outLFNDirBase = '/store/user/swuycken'
config.Site.whitelist = ["T2_BE_UCL"]
config.Data.ignoreLocality = True
config.Site.storageSite = 'T2_BE_UCL'
config.Site.ignoreGlobalBlacklist = True
'''

with open('reco_crab.py','w') as crabfile:
    crabfile.write(crab_cfg.format(**locals()))

if args.submit:
    os.system('crab submit -c reco_crab.py')
if not args.dryRun:
    os.system('rm {reco_cfg} reco_crab.py'.format(**locals()))
#os.system('rm *.pyc')
