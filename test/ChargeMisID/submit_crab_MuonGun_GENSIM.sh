#!/bin/bash

#for p in {50,100,300,500,750,1000,1250,1500,2000,2500,3000,4000}
for p in {50,100,300,500}
    do python submit_crab_MuonGun_GENSIM.py -e ${p} -n 10000 -j 100 -s -dr -x 20181207
done
for p in {750,1000,1250,1500}
    do python submit_crab_MuonGun_GENSIM.py -e ${p} -n 5000 -j 100 -s -dr -x 20181207
done
