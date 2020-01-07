# COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

##Signals for SUSY SOS

##TChiWZ
#SMS_TChiWZ=kreator.makeMCComponent("SMS_TChiWZ","/SMS-TChiWZ_ZToLL_mZMin-0p1_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-GridpackScan_102X_upgrade2018_realistic_v15-v1/MINIAODSIM","CMS",".*root",1) #2018
#SMS_TChiWZ=kreator.makeMCComponent("SMS_TChiWZ","/SMS-TChiWZ_ZToLL_mZMin-0p1_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_GridpackScan_94X_mc2017_realistic_v14-v1/MINIAODSIM","CMS",".*root",1) #2017
SMS_TChiWZ=kreator.makeMCComponent("SMS_TChiWZ","/SMS-TChiWZ_ZToLL_mZMin-0p1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_GridpackScan_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM","CMS",".*root",1) #2016

SignalSUSY = [SMS_TChiWZ]
mcSamples = SignalSUSY
samples = mcSamples



# ---------------------------------------------------------------------

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
