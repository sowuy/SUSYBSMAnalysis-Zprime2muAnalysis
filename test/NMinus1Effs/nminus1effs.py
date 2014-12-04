#!/usr/bin/env python

import sys, os, FWCore.ParameterSet.Config as cms
from SUSYBSMAnalysis.Zprime2muAnalysis.Zprime2muAnalysis_cfg import process
from SUSYBSMAnalysis.Zprime2muAnalysis.HistosFromPAT_cfi import HistosFromPAT
from SUSYBSMAnalysis.Zprime2muAnalysis.OurSelectionDec2012_cff import loose_cut, trigger_match, tight_cut, allDimuons

readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
process.source = cms.Source ("PoolSource",fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( [
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_100_1_Bc7.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_101_1_YfK.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_10_1_e78.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_11_1_OzT.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_12_1_1qr.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_13_1_6EI.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_14_1_NFJ.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_15_1_yMJ.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_16_1_A8S.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_17_1_tnH.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_18_1_2f0.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_19_1_Psv.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_1_1_Zes.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_20_1_BRX.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_21_1_HJ6.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_22_1_ACy.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_23_1_RTy.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_24_1_0nC.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_25_1_QEJ.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_26_1_OJ0.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_27_1_dzA.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_28_1_ksz.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_29_1_EBN.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_2_1_xnL.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_30_1_F2R.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_31_1_Enx.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_32_1_UX3.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_33_1_QFH.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_34_1_rdI.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_35_1_XDg.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_36_1_CFV.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_37_1_ZOv.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_38_1_Z8K.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_39_1_hJJ.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_3_1_AF0.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_40_1_PrV.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_41_1_ZnE.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_42_1_OOd.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_43_1_6CX.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_44_1_nuS.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_45_1_vKA.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_46_1_u5F.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_47_1_ea8.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_48_1_15G.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_49_1_0rh.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_4_1_cc6.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_50_1_4Hl.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_51_1_kZX.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_52_1_ze6.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_53_1_ahT.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_54_1_WDv.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_55_1_z30.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_56_1_ypb.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_57_1_WCA.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_58_1_HW5.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_59_1_lKH.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_5_1_eNV.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_60_1_Twn.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_61_1_ChM.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_62_1_v1v.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_63_1_V5h.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_64_1_FhK.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_65_1_Bwc.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_66_1_mdg.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_67_1_UWx.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_68_1_Ze3.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_69_1_lay.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_6_1_s7E.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_70_1_Hvo.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_71_1_ZHF.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_72_1_g9r.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_73_1_8nb.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_74_1_7UH.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_75_1_lhC.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_76_1_qvV.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_77_1_7cn.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_78_1_GTz.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_79_1_Sik.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_7_1_pJc.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_80_1_CV0.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_81_1_nHL.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_82_1_Y5i.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_83_1_YQL.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_84_1_whW.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_85_1_ZG4.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_86_1_y0w.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_87_1_KMp.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_88_1_cEL.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_89_1_Hil.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_8_1_ODG.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_90_1_rDv.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_91_1_6Ii.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_92_1_M2j.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_93_1_J2J.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_94_1_mAI.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_95_1_aoc.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_96_1_oiz.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_97_1_dEF.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_98_1_a6K.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_99_1_sVv.root',
       '/store/user/rradogna/ZprimeToMuMu_M-1000_Tune4C_13TeV-pythia8/datamc_zpsi1000/5ae2dc0ad5519e42240ad5a71eb54bed/pat_9_1_RsK.root' ] );


secFiles.extend( [
               ] )

process.maxEvents.input = -1

# Define the numerators and denominators, removing cuts from the
# allDimuons maker. "NoX" means remove cut X entirely (i.e. the
# loose_cut denominators), "TiX" means move cut X from the loose_cut
# to the tight_cut (meaning only one muon instead of two has to pass
# the cut).  "NoNo" means remove nothing (i.e. the numerator). This
# will break if loose_, tight_cut strings are changed upstream, so we
# try to check those with a simple string test below.

cuts = [
    ('Pt',      'pt > 45'),
    ('DB',      'abs(dB) < 0.2'),
    ('Iso',     'isolationR03.sumPt / innerTrack.pt < 0.10'),
    ('TkLayers','globalTrack.hitPattern.trackerLayersWithMeasurement > 5'),
    ('PxHits',  'globalTrack.hitPattern.numberOfValidPixelHits >= 1'),
    ('MuHits',  'globalTrack.hitPattern.numberOfValidMuonHits > 0'),
    ('MuMatch', ('numberOfMatchedStations > 1', 'isTrackerMuon')),
    ]

for name, cut in cuts:
    if type(cut) != tuple:
        cut = (cut,)

    lc = loose_cut
    for c in cut:
        if c not in lc:
            raise ValueError('cut "%s" not in cut string "%s"' % (c, lc))
        lc = lc.replace(' && ' + c, '') # Relies on none of the cuts above being first in the list.

    obj_no = allDimuons.clone(loose_cut = lc)
    setattr(process, 'allDimuonsNo' + name, obj_no)
    
    obj_ti = obj_no.clone(tight_cut = tight_cut + ' && ' + ' && '.join(cut))
    setattr(process, 'allDimuonsTi' + name, obj_ti)

process.allDimuonsNoNo      = allDimuons.clone()
process.allDimuonsNoTrgMtch = allDimuons.clone(tight_cut = tight_cut.replace(trigger_match, ''))

alldimus = [x for x in dir(process) if 'allDimuonsNo' in x or 'allDimuonsTi' in x]

# Sanity check that the replaces above did something.
for x in alldimus:
    if 'NoNo' in x:
        continue
    o = getattr(process, x)
    assert o.loose_cut.value() != loose_cut or o.tight_cut.value() != tight_cut

process.p = cms.Path(process.goodDataFilter * process.muonPhotonMatch * process.leptons * reduce(lambda x,y: x*y, [getattr(process, x) for x in alldimus]))

# For all the allDimuons producers, make dimuons producers, and
# analyzers to make the histograms.
for alld in alldimus:
    dimu = process.dimuons.clone(src = alld)
    name = alld.replace('allD', 'd')
    setattr(process, name, dimu)
    hists = HistosFromPAT.clone(dilepton_src = name, leptonsFromDileptons = True)
    setattr(process, name.replace('dimuons', ''), hists)
    process.p *= dimu * hists

# Handle the cuts that have to be applied at the
# Zprime2muCompositeCandidatePicker level.
process.dimuonsNoB2B     = process.dimuons.clone()
process.dimuonsNoVtxProb = process.dimuons.clone()
process.dimuonsNoDptPt   = process.dimuons.clone()
delattr(process.dimuonsNoB2B,     'back_to_back_cos_angle_min')
delattr(process.dimuonsNoVtxProb, 'vertex_chi2_max')
delattr(process.dimuonsNoDptPt,   'dpt_over_pt_max')
process.p *= process.allDimuons
for dimu in ['dimuonsNoB2B', 'dimuonsNoVtxProb', 'dimuonsNoDptPt']:
    hists = HistosFromPAT.clone(dilepton_src = dimu, leptonsFromDileptons = True)
    setattr(process, dimu.replace('dimuons', ''), hists)
    process.p *= getattr(process, dimu) * hists

# Special case to remove |dB| and B2B cuts simultaneously, as they can
# be correlated (anti-cosmics).
process.allDimuonsNoCosm = process.allDimuons.clone(loose_cut = loose_cut.replace(' && abs(dB) < 0.2', ''))
process.dimuonsNoCosm = process.dimuons.clone(src = 'allDimuonsNoCosm')
delattr(process.dimuonsNoCosm, 'back_to_back_cos_angle_min')
process.NoCosm = HistosFromPAT.clone(dilepton_src = 'dimuonsNoCosm', leptonsFromDileptons = True)
process.p *= process.allDimuonsNoCosm * process.dimuonsNoCosm * process.NoCosm

if __name__ == '__main__' and 'submit' in sys.argv:
    crab_cfg = '''
[CRAB]
jobtype = cmssw
#scheduler = condor
scheduler = remoteGlidein

use_server = 0

[CMSSW]
datasetpath = %(ana_dataset)s
#dbs_url = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet
dbs_url=phys03
pset = nminus1effs.py
get_edm_output = 1
job_control

use_dbs3=1

[USER]
#ui_working_dir = /crab/crab_ana_nminus1_%(name)s
return_data = 1
'''

    just_testing = 'testing' in sys.argv
    if not 'no_data' in sys.argv:
        from SUSYBSMAnalysis.Zprime2muAnalysis.goodlumis import Run2012MuonsOnly_ll
        Run2012MuonsOnly_ll.writeJSON('tmp.json')

        dataset_details = [
            ('SingleMuRun2012A_13Jul2012_190450_193751', '/SingleMu/slava-datamc_SingleMuRun2012A-13Jul2012_190450_193751_20121011073628-426a2d966f78bce6bde85f3ed41c07ba/USER'),
            ('SingleMuRun2012A_06Aug2012_190782_190949', '/SingleMu/slava-datamc_SingleMuRun2012A-recover-06Aug2012_190782_190949_20121011120430-426a2d966f78bce6bde85f3ed41c07ba/USER'),
            ('SingleMuRun2012B_13Jul2012_193752_196531', '/SingleMu/slava-datamc_SingleMuRun2012B-13Jul2012_193752_196531_20121012044921-426a2d966f78bce6bde85f3ed41c07ba/USER'),
            ('SingleMuRun2012C_24Aug2012_197556_198913', '/SingleMu/slava-datamc_SingleMuRun2012C-24Aug2012_197556_198913_20121012113325-426a2d966f78bce6bde85f3ed41c07ba/USER'),
            ('SingleMuRun2012C_Prompt_198934_203772',    '/SingleMu/slava-datamc_SingleMuRun2012C-Prompt_198934_203772_20121015023300-8627c6a48d2426dec4aa557620a039a0/USER'),
            ('SingleMuRun2012D_Prompt_203773_204563',    '/SingleMu/slava-datamc_SingleMuRun2012D-Prompt_203773_204563_20121016104501-8627c6a48d2426dec4aa557620a039a0/USER'),
            ('SingleMuRun2012D_Prompt_204564_206087',    '/SingleMu/slava-datamc_SingleMuRun2012D-Prompt_204564_206087_20121029121943-8627c6a48d2426dec4aa557620a039a0/USER'),
            ('SingleMuRun2012D-Prompt_206088_206539',    '/SingleMu/slava-datamc_SingleMuRun2012D-Prompt_206088_206539_20121112085341-8627c6a48d2426dec4aa557620a039a0/USER'),
            ]

        for name, ana_dataset in dataset_details:
            print name

            new_py = open('nminus1effs.py').read()
            new_py += "\nprocess.GlobalTag.globaltag = 'GR_P_V42_AN2::All'\n"
            open('nminus1effs_crab.py', 'wt').write(new_py)

            new_crab_cfg = crab_cfg % locals()
            job_control = '''
total_number_of_lumis = -1
#number_of_jobs = 20
lumis_per_job = 500
lumi_mask = tmp.json'''
            new_crab_cfg = new_crab_cfg.replace('job_control', job_control)
            open('crab.cfg', 'wt').write(new_crab_cfg)

            if not just_testing:
                os.system('crab -create -submit all')

        if not just_testing:
            os.system('rm crab.cfg nminus1effs_crab.py nminus1effs_crab.pyc tmp.json')

    if not 'no_mc' in sys.argv:
        crab_cfg = crab_cfg.replace('job_control','''
total_number_of_events = -1
events_per_job = 50000
''')

        from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import *
        samples = [zpsi1000]#zmumu, ttbar, dy120_c1, dy200_c1, dy500_c1, dy800_c1, dy1000_c1, dy1500_c1, dy2000_c1, inclmu15]
        for sample in samples:
            print sample.name
            open('crab.cfg', 'wt').write(crab_cfg % sample)
            if not just_testing:
                os.system('crab -create -submit all')

        if not just_testing:
            os.system('rm crab.cfg')
