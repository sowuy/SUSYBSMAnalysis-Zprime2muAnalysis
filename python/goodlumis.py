import copy
from FWCore.PythonUtilities.LumiList import LumiList

def for_cmssw(ll):
    return ll.getCMSSWString().split(',')

# These run numbers guide the combination of the prompt and DCS-only
# JSONs.
first_run = 294927 #first DCS run or first analyzed run
last_rereco_run = 306462
last_prompt_run = 306462
last_run = 306462 #last DCS run or last analyzed run

# Sometimes the same run-range json gets made in other versions.
prompt_version = ''

# Lumis to manually throw out.
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

Prompt_ll          = LumiList('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PromptReco/Cert_%i-%i_13TeV_PromptReco_Collisions17_JSON%s.txt' % (first_run, last_prompt_run, prompt_version))
PromptMuonsOnly_ll = LumiList('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Final/Cert_%i-%i_13TeV_PromptReco_Collisions17_JSON_MuonPhys%s.txt' % (first_run, last_prompt_run, prompt_version))

ReReco_ll          = LumiList('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt')
ReRecoMuonsOnly_ll = LumiList('/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_MuonPhys.txt')


def combine(prompt_ll, rereco1_ll, rereco2_ll, rereco3_ll, dcsonly_ll=None):
    prompt_ll = copy.deepcopy(prompt_ll)
    prompt_ll.removeRuns(runs_to_remove_from_prompt)
    ll = prompt_ll | rereco1_ll | rereco2_ll | rereco3_ll
    if dcsonly_ll is not None:
        dcsonly_ll = copy.deepcopy(dcsonly_ll)
        dcsonly_ll.removeRuns(runs_to_remove_from_dcsonly)
        ll = ll | dcsonly_ll
    return ll

# Combine all lists
#Run2017_ll          = Prompt_ll
#Run2017MuonsOnly_ll = PromptMuonsOnly_ll
Run2017_ll          = ReReco_ll
Run2017MuonsOnly_ll = ReRecoMuonsOnly_ll
all_ll_names = ['Run2017', 'Run2017MuonsOnly']

def all_lls():
    return [(x, eval(x + '_ll')) for x in all_ll_names]

for base_name, ll in all_lls():
    exec '%s_ll = ll - to_remove' % base_name
    exec '%s = for_cmssw(%s_ll)' % (base_name, base_name)

if __name__ == '__main__':
    import sys
    if 'write' in sys.argv:
        Run2017MuonsOnly_ll.writeJSON('Run2017MuonsOnly.json')
        Run2017_ll.writeJSON('Run2017.json')
    elif 'write_all' in sys.argv:
        for base_name, ll in all_lls():
            ll.writeJSON('zp2mu_goodlumis_%s.json' % base_name)
