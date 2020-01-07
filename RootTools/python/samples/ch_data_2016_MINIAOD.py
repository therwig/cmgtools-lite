import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

### ----------------------------- Zero Tesla run  ----------------------------------------

dataDir = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data"  # use environmental variable, useful for instance to run on CRAB
json='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt'

run_range = (273158, 284044)
label = "_runs%s_%s"%(run_range[0], run_range[1])


# JetHT_Run2016H_17Jul2018          = kreator.makeDataComponent("JetHT_Run2016H_17Jul2018"         , "/JetHT/Run2016H-17Jul2018-v1/MINIAOD"         , "CMS", ".*root", json)
# HTMHT_Run2016H_17Jul2018          = kreator.makeDataComponent("HTMHT_Run2016H_17Jul2018"         , "/HTMHT/Run2016H-17Jul2018-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016H_17Jul2018            = kreator.makeDataComponent("MET_Run2016H_17Jul2018"           , "/MET/Run2016H-17Jul2018-v2/MINIAOD"           , "CMS", ".*root", json)
# SingleElectron_Run2016H_17Jul2018 = kreator.makeDataComponent("SingleElectron_Run2016H_17Jul2018", "/SingleElectron/Run2016H-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
# SingleMuon_Run2016H_17Jul2018     = kreator.makeDataComponent("SingleMuon_Run2016H_17Jul2018"    , "/SingleMuon/Run2016H-17Jul2018-v1/MINIAOD"    , "CMS", ".*root", json)
# SinglePhoton_Run2016H_17Jul2018   = kreator.makeDataComponent("SinglePhoton_Run2016H_17Jul2018"  , "/SinglePhoton/Run2016H-17Jul2018-v1/MINIAOD"  , "CMS", ".*root", json)
# DoubleEG_Run2016H_17Jul2018       = kreator.makeDataComponent("DoubleEG_Run2016H_17Jul2018"      , "/DoubleEG/Run2016H-17Jul2018-v1/MINIAOD"      , "CMS", ".*root", json)
# MuonEG_Run2016H_17Jul2018        = kreator.makeDataComponent("MuonEG_Run2016H_17Jul2018"        , "/MuonEG/Run2016H-17Jul2018-v1/MINIAOD"        , "CMS", ".*root", json)
# DoubleMuon_Run2016H_17Jul2018     = kreator.makeDataComponent("DoubleMuon_Run2016H_17Jul2018"    , "/DoubleMuon/Run2016H-17Jul2018-v1/MINIAOD"    , "CMS", ".*root", json)
# Tau_Run2016H_17Jul2018     = kreator.makeDataComponent("Tau_Run2016H_17Jul2018"    , "/Tau/Run2016H-17Jul2018-v1/MINIAOD"    , "CMS", ".*root", json)

#dataSamples_Run2016H_17Jul2018 = [JetHT_Run2016H_17Jul2018, HTMHT_Run2016H_17Jul2018, MET_Run2016H_17Jul2018, SingleElectron_Run2016H_17Jul2018, SingleMuon_Run2016H_17Jul2018, SinglePhoton_Run2016H_17Jul2018, DoubleEG_Run2016H_17Jul2018, MuonEG_Run2016H_17Jul2018, DoubleMuon_Run2016H_17Jul2018, Tau_Run2016H_17Jul2018]
dataSamples_Run2016H_17Jul2018 = [] # [MET_Run2016H_17Jul2018]


### Summary of 17Jul2018
dataSamples_17Jul2018 = dataSamples_Run2016H_17Jul2018 #dataSamples_Run2016B_17Jul2018 + dataSamples_Run2016C_17Jul2018 + dataSamples_Run2016D_17Jul2018 + dataSamples_Run2016E_17Jul2018 + dataSamples_Run2016F_17Jul2018 + dataSamples_Run2016G_17Jul2018 + 


### ----------------------------- summary of prompt reco ----------------------------------------
dataSamples_PromptReco = dataSamples_17Jul2018

dataSamples = dataSamples_PromptReco
samples = dataSamples

### ---------------------------------------------------------------------
if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
