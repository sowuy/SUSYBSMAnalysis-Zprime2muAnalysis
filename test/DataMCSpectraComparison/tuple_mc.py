#!/usr/bin/env python

import sys, os
from SUSYBSMAnalysis.Zprime2muAnalysis.PATTools import switchHLTProcessName,AODOnly,removeMuonMCClassification,removeSimLeptons, pruneMCLeptons
from tuple_common import cms, process, crab_cfg

pruneMCLeptons(process, use_sim=True) # because of unscheduled I can't remove this for data.

AODOnly(process)# it contains
    #removeMuonMCClassification(process)#?
    #removeSimLeptons(process)
    #switchHLTProcessName(process, 'REDIGI311X')# ???

#process.source.fileNames = ['file:../../python/9081056A-10E7-E411-A322-00259059391E.root',]
process.source.fileNames=['/store/relval/CMSSW_7_4_0/RelValZpMM_2250_13TeV_Tauola/GEN-SIM-RECO/MCRUN2_74_V7-v1/00000/AE8D58C2-14DB-E411-A038-002618943901.root']



process.maxEvents.input = -1

#process.GlobalTag.globaltag = 'MCRUN2_74_V6B'
process.GlobalTag.globaltag = 'MCRUN2_74_V9'


#switchHLTProcessName(process, "HLT")


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    job_control = '''
total_number_of_events = -1
events_per_job = 5000
'''

    just_testing = 'testing' in sys.argv
    create_only = 'create_only' in sys.argv

    from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples
    for sample in samples:
        print sample.name

        new_py = open('tuple_mc.py').read()
        new_py += '\nswitchHLTProcessName(process, "%(hlt_process_name)s")\n' % sample.__dict__

        sample.pset = 'crab/psets/tuple_mc_crab_%(name)s.py' % sample.__dict__
        open(sample.pset,'wt').write(new_py)

        #sample.job_control = job_control % sample.__dict__
        sample.job = 'crab_%(name)s.py' % sample.__dict__
        open(sample.job, 'wt').write(crab_cfg % sample.__dict__)
        if not just_testing:
            if create_only:
                os.system('crab submit -c ' + sample.job)
           # else:
              #  os.system('crab -create -submit all')
           # os.system('rm crab.cfg')
