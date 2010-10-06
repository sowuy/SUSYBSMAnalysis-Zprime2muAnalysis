#!/bin/tcsh

pushd $CMSSW_BASE/src

cvs co -r V00-03-04 MuonAnalysis/Examples
cvs co -r V01-09-01 MuonAnalysis/MuonAssociators
#cvs co -r V02-04-00 RecoMuon/TrackingTools
cvs co -r V02-06-01 SimMuon/MCTruth
cvs co -r V01-08-17 SimTracker/TrackAssociation
cvs co -r V00-01-03-01 SimTracker/TrackAssociatorESProducer
cvs co -r V00-05-00 -d SHarper/HEEPAnalyzer UserCode/SHarper/HEEPAnalyzer
cvs co -r V00-00-02 -d UserCode/Examples UserCode/AEverett/Examples
cvs co -r lumi2010-Sep28 RecoLuminosity/LumiDB
cvs co -r V01-04-00 FWCore/PythonUtilities

# fix InputTag.h location
#find . -type f \! -name setup.csh | xargs grep -l "interface/InputTag.h" | xargs -I {} sed -i {} -e "s#FWCore/ParameterSet/interface/InputTag.h#FWCore/Utilities/interface/InputTag.h#g"
sed -i SimMuon/MCTruth/test/testAssociatorRecoMuon.cc -e "s#FWCore/ParameterSet/interface/InputTag.h#FWCore/Utilities/interface/InputTag.h#g"

scramv1 b -j 4
popd
