#!/usr/bin/env python

import sys, os
from SUSYBSMAnalysis.Zprime2muAnalysis.PATTools import switchHLTProcessName,AODOnly,removeMuonMCClassification,removeSimLeptons, pruneMCLeptons
from tuple_common import cms, process, crab_cfg

# problema con pruned ed unscheduled, cioe anche se io ho il remove quello nn va avanti.
pruneMCLeptons(process, use_sim=True) # need to decide whether to move AODOnly() call in here, if so use_sim should just be set False

AODOnly(process) # definito in PATTools, ma l'ho modificato
#oltre alle menate AOD only, contienea i due processi sotto
#removeMuonMCClassification(process)#??? # throw the baby out with the
#removeSimLeptons(process)
#switchHLTProcessName(process, 'REDIGI311X')#no idea????

#!!!!!
#process.patDefaultSequence.remove(process.cleanPatElectrons*process.selectedPatElectrons*process.patElectrons*process.electronMatch)

process.source.fileNames = ['/store/mc/Phys14DR/DYJetsToEEMuMu_M-9500_13TeV-madgraph/AODSIM/PU20bx25_PHYS14_25_V1-v2/00000/18C7C360-E076-E411-9E2F-E0CB4E19F9BC.root',]
#process.source.fileNames=['/store/relval/CMSSW_7_1_0/RelValZMM_13/GEN-SIM-RECO/POSTLS171_V15-v1/00000/6650F961-99FB-E311-BA90-0025905A48BC.root']

#from PhysicsTools.PatAlgos.patInputFiles_cff import filesRelValProdTTbarAODSIM
#process.source.fileNames = filesRelValProdTTbarAODSIM

process.maxEvents.input = 10

process.GlobalTag.globaltag = 'PHYS14_25_V1::All'
#process.GlobalTag.globaltag = 'START71_V1::All'
#process.GlobalTag.globaltag = 'START53_V7C1::All'

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    job_control = '''
total_number_of_events = -1
events_per_job = 1000
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

        sample.job_control = job_control % sample.__dict__
        open('crab.cfg', 'wt').write(crab_cfg % sample.__dict__)
        if not just_testing:
            if create_only:
                os.system('crab -create')
            else:
                os.system('crab -create -submit all')
            os.system('rm crab.cfg')
