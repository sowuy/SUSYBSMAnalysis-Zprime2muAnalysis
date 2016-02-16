import copy
from FWCore.PythonUtilities.LumiList import LumiList

def for_cmssw(ll):
    return ll.getCMSSWString().split(',')

# These run numbers guide the combination of the prompt and DCS-only
# JSONs.
first_run = 246908 #first DCS run or first analyzed run
last_rereco_run = 198523
# B+C MuonPhys 50ns
last_50ns_prompt_run = 255031
# C+D MuonPhys 25ns
last_25ns_prompt_run = 260627
last_run = 260627 #last DCS run or last analyzed run
last_prompt_run = 260627

# Sometimes the same run-range json gets made in other versions.
prompt_version = '_v2'

# Lumis to manually throw out.
#to_remove = {'190949': [[82,1149]], '191090': [[56,339]]}   # These are 20/pb of "low pileup" runs in which they enabled only Mu15 and disabled Mu40 (set prescale to 0).
#to_remove.update({'191367': [[1,289]], '191391': [[1,14]]}) # Runs with < 0.2/pb data where triggers were switched off (prescale set to 0).  Just in DCS-only JSON.
#to_remove.update({'193112': [[54,235]], '193116': [[1,693]]}) # ~2/pb + ~5/pb of "low pileup" runs in which they enabled only Mu15 and disabled Mu40 (set prescale to 0).
to_remove = {}
to_remove = LumiList(compactList=to_remove)

# These runs are <= last_prompt_run, but they were not actually
# considered in the certification for the latest prompt JSON. So,
# don't drop them from the DCS-only list when combining later.
holes = []

# Order of priorities: rereco, then prompt reco, and then DCS.
runs_to_remove_from_prompt  = range(first_run, last_rereco_run+1)
runs_to_remove_from_dcsonly = range(first_run, last_prompt_run+1)
for hole in holes:
    print 'goodlumis warning: re-adding "hole" run %i from DCS-only list' % hole
    runs_to_remove_from_dcsonly.remove(hole)

#DCSOnly_ll           = LumiList('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/DCSOnly/json_DCSONLY.txt')
#DCSOnlyForNewRuns_ll = LumiList('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/DCSOnly/json_DCSONLY.txt')
DCSOnly_ll           = LumiList('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/DCSOnly/json_DCSONLY.txt')
DCSOnlyForNewRuns_ll = LumiList('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/DCSOnly/json_DCSONLY.txt')
DCSOnlyForNewRuns_ll.removeRuns(runs_to_remove_from_dcsonly)

# Remove runs outside the range [first_run, last_run] since DCS-only
# list includes HI runs, etc. ###### Use later
#for ll in (DCSOnly_ll, DCSOnlyForNewRuns_ll):
#    ll.removeRuns(xrange(1, first_run))
#    ll.removeRuns(xrange(last_run+1, 300000)) # dummy number

# Prompt reconstruction, 2015A
#Cert_246908-248038_13TeV_PromptReco_Collisions15_ZeroTesla_JSON.txt
#/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-248038_13TeV_PromptReco_Collisions15_ZeroTesla_JSON_MuonPhys.txt
#Prompt 2015C
#Cert_246908-255031_13TeV_PromptReco_Collisions15_50ns_JSON_MuonPhys.txt
#Cert_246908-255031_13TeV_PromptReco_Collisions15_25ns_JSON_MuonPhys.txt

# 25ns Golden
Prompt_ll          = LumiList('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_%i-%i_13TeV_PromptReco_Collisions15_25ns_JSON%s.txt' % (first_run, last_25ns_prompt_run, prompt_version))

# 25ns MuonPhys
PromptMuonsOnly25ns_ll = LumiList('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_%i-%i_13TeV_PromptReco_Collisions15_25ns_JSON_MuonPhys%s.txt' % (first_run, last_25ns_prompt_run, prompt_version))

# 50ns MuonPhys
PromptMuonsOnly50ns_ll = LumiList('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_%i-%i_13TeV_PromptReco_Collisions15_50ns_JSON_MuonPhys%s.txt' % (first_run, last_50ns_prompt_run, prompt_version))

def combine(prompt_ll, rereco1_ll, rereco2_ll, rereco3_ll, dcsonly_ll=None):
    prompt_ll = copy.deepcopy(prompt_ll)
    prompt_ll.removeRuns(runs_to_remove_from_prompt)
    ll = prompt_ll | rereco1_ll | rereco2_ll | rereco3_ll
    if dcsonly_ll is not None:
        dcsonly_ll = copy.deepcopy(dcsonly_ll)
        dcsonly_ll.removeRuns(runs_to_remove_from_dcsonly)
        ll = ll | dcsonly_ll
    return ll

# Combine all lists example : Run2012_ll          = combine(Prompt_ll,          Jul13_ll,          Aug06_ll,          Aug24_ll)
Run2015_ll          = Prompt_ll
Run2015MuonsOnly25ns_ll = PromptMuonsOnly25ns_ll
Run2015MuonsOnly50ns_ll = PromptMuonsOnly50ns_ll

dcsonly_ll = copy.deepcopy(DCSOnly_ll)
dcsonly_ll.removeRuns(runs_to_remove_from_dcsonly)
#Run2012PlusDCSOnly_ll          = Jan22_ll | dcsonly_ll
#Run2012PlusDCSOnlyMuonsOnly_ll = Jan22MuonsOnly_ll | dcsonly_ll

all_ll_names = ['DCSOnly', 'Run2015', 'Run2015MuonsOnly25ns','Run2015MuonsOnly50ns']

#print 'DCSOnly', DCSOnly_ll
#print 'Run2015', Run2015_ll
#print 'Run2015MuonsOnly', Run2015MuonsOnly_ll

def all_lls():
    return [(x, eval(x + '_ll')) for x in all_ll_names]

for base_name, ll in all_lls():
    exec '%s_ll = ll - to_remove' % base_name
    exec '%s = for_cmssw(%s_ll)' % (base_name, base_name)

if __name__ == '__main__':
    import sys
    if 'write' in sys.argv:
        Run2015MuonsOnly25ns_ll.writeJSON('Run2015MuonsOnly25ns.json')
        Run2015MuonsOnly50ns_ll.writeJSON('Run2015MuonsOnly50ns.json')
        Run2015_ll.writeJSON('Run2015.json')
    elif 'write_all' in sys.argv:
        for base_name, ll in all_lls():
            ll.writeJSON('zp2mu_goodlumis_%s.json' % base_name)
