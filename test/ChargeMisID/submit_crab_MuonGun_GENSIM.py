import sys,os
import argparse

parser = argparse.ArgumentParser(description='Submit GEN-SIM of muon gun samples with user-input energies')
parser.add_argument('-e','--energy',nargs='+',default=[1000],type=float,help='Muon energy in GeV')
parser.add_argument('-n','--numEvts',default=1000,type=int,help='Number of events to generate per job')
parser.add_argument('-j','--numJobs',default=100,type=int,help='Number of jobs to submit to CRAB')
parser.add_argument('-s','--submit',action='store_true',help='Submit to CRAB')
parser.add_argument('-dr','--dryRun',action='store_true',help='Make CRAB cfg files but don\'t submit')
parser.add_argument('-x','--extra',type=str,help='Extra name to append to crab request name')
args = parser.parse_args()

NEVTS = args.numEvts
NJOBS = args.numJobs
# Energy can either be range or singular value
if len(args.energy)>1:
    minEnergy = args.energy[0]
    maxEnergy = args.energy[1]
    PSETHACK = 'single mu E '+str(minEnergy)+'to'+str(maxEnergy)
else:
    minEnergy = args.energy[0]-0.01
    maxEnergy = args.energy[0]+0.01
    PSETHACK = 'single mu E '+str(args.energy[0])


baseName = 'MuonGun_P'
for e in args.energy:
    print e
    baseName += '-'+str(int(e))
outputDatasetTag = baseName + '_GEN-SIM'
requestName = outputDatasetTag + ('_'+args.extra if args.extra else '')

with open('SingleMuGun_P_pythia8_cfi_GEN_SIM_CRAB_TMP.py','r') as infile:
    new_py = infile.read()

new_py = new_py.replace('OUTPUT_FILENAME','\''+baseName+'.root\'')
new_py = new_py.replace('MAX_ENERGY',str(maxEnergy))
new_py = new_py.replace('MIN_ENERGY',str(minEnergy))
new_py = new_py.replace('PSETHACK','\''+PSETHACK+'\'')

gensim_cfg = requestName+'.py'
with open(gensim_cfg,'w') as outfile:
    outfile.write(new_py)

crab_cfg = \
'''from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()
config.General.requestName = '{requestName}'
config.General.workArea = 'crab'

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = '{gensim_cfg}'

config.Data.outputPrimaryDataset = '{baseName}'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = {NEVTS}
config.Data.totalUnits = config.Data.unitsPerJob * {NJOBS}
config.Data.publication = True
config.Data.outputDatasetTag = '{outputDatasetTag}'
config.Data.outLFNDirBase = '/store/user/'+getUsernameFromSiteDB()

config.Site.storageSite = 'T2_CH_CERN'
'''

with open('gensim_crab.py','w') as crabfile:
    crabfile.write(crab_cfg.format(**locals()))

if args.submit:
    os.system('crab submit -c gensim_crab.py')
if not args.dryRun:
    os.system('rm {gensim_cfg} gensim_crab.py'.format(**locals()))
os.system('rm *.pyc')


