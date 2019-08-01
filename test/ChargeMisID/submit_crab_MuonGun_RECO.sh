#!/bin/bash

#,2000,2500,3000,4000}
for p in {50,100,300,500,750,1000,1250,1500}
do 
        python submit_crab_MuonGun_RECO.py -mc MuonGun_P-${p} -dr -s -x 20181209
        python submit_crab_MuonGun_RECO.py -mc MuonGun_P-${p} -dr -s -x 20181209 -a startup --no_ape
done
