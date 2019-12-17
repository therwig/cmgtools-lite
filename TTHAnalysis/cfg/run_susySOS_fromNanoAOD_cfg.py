import re, os, sys
from CMGTools.RootTools.samples.configTools import printSummary, mergeExtensions, doTestN, configureSplittingFromTime, cropToLumi
from CMGTools.RootTools.samples.autoAAAconfig import autoAAA
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()
def byCompName(components, regexps):
    return [ c for c in components if any(re.match(r, c.name) for r in regexps) ]

year = int(getHeppyOption("year", "2018"))
analysis = getHeppyOption("analysis", "main")
preprocessor = getHeppyOption("nanoPreProcessor")

#ch test
ch_test=True

if getHeppyOption("nanoPreProcessor"):
    if ch_test:
        pass
        # from CMGTools.RootTools.samples.ch_samples_2016_MINIAOD import samples as mcSamples_
        # from CMGTools.RootTools.samples.ch_data_2016_MINIAOD import dataSamples_17Jul2018 as allData
        # from CMGTools.RootTools.samples.triggers_13TeV_DATA2016 import all_triggers as triggers
    elif year == 2018:
        from CMGTools.RootTools.samples.samples_13TeV_RunIIAutumn18MiniAOD import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2018_MiniAOD import samples as allData
        from CMGTools.RootTools.samples.triggers_13TeV_DATA2018 import all_triggers as triggers
    elif year == 2017:
        from CMGTools.RootTools.samples.samples_13TeV_RunIIFall17MiniAOD import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2017 import dataSamples_31Mar2018 as allData
        from CMGTools.RootTools.samples.triggers_13TeV_DATA2017 import all_triggers as triggers
    elif year == 2016:
        from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv3 import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import dataSamples_17Jul2018 as allData
        from CMGTools.RootTools.samples.triggers_13TeV_DATA2016 import all_triggers as triggers
else:
    if ch_test:
        pass
    elif year == 2018:
        from CMGTools.RootTools.samples.samples_13TeV_RunIIAutumn18NanoAODv5 import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2018_NanoAOD import dataSamples_1June2019 as allData
        from CMGTools.RootTools.samples.triggers_13TeV_DATA2018 import all_triggers as triggers
    elif year == 2017:
        from CMGTools.RootTools.samples.samples_13TeV_RunIIFall17NanoAODv5 import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2017_NanoAOD import dataSamples_1June2019 as allData
        from CMGTools.RootTools.samples.triggers_13TeV_DATA2017 import all_triggers as triggers
    elif year == 2016:
        from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16NanoAODv5 import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2016_NanoAOD import dataSamples_1June2019 as allData
        from CMGTools.RootTools.samples.triggers_13TeV_DATA2016 import all_triggers as triggers


DatasetsAndTriggers = []
if year == 2018 and not ch_test:
    if analysis == "main":
        mcSamples = byCompName(mcSamples_, [

##            "DYJetsToLL_M10to50_LO",
            "DYJetsToLL_M50_LO", # for Tag and Probe studies
##            "DYJetsToLL_M50_LO_ext",


            "T_tWch_noFullyHad$",
            "TBar_tWch_noFullyHad$",

            "DYJetsToLL_M4to50_HT70to100",
            "DYJetsToLL_M4to50_HT100to200",
            "DYJetsToLL_M4to50_HT200to400",
            "DYJetsToLL_M4to50_HT400to600",
            "DYJetsToLL_M4to50_HT600toInf",

            "DYJetsToLL_M50_HT100to200",
            "DYJetsToLL_M50_HT200to400",
            "DYJetsToLL_M50_HT400to600," 
##            "DYJetsToLL_M50_HT400to600_ext2",
            "DYJetsToLL_M50_HT600to800",
            "DYJetsToLL_M50_HT800to1200",
            "DYJetsToLL_M50_HT1200to2500",
            "DYJetsToLL_M50_HT2500toInf",

            "TTJets_DiLepton$",

            #check if VVTo2L2Nu is there
            "WWTo2L2Nu$",
            "ZZTo2L2Nu",
            "TTJets_SingleLeptonFromT$", "TTJets_SingleLeptonFromTbar$", 
            
            "WJetsToLNu_HT100to200",
            "WJetsToLNu_HT200to400",
            "WJetsToLNu_HT400to600",
            "WJetsToLNu_HT600to800",
            "WJetsToLNu_HT800to1200",
            "WJetsToLNu_HT1200to2500",
            "WJetsToLNu_HT2500toInf",

            "WZTo3LNu_fxfx$",
            "WWToLNuQQ",
            #"WZTo1L1Nu2Q",
            "ZZTo4L$",
            "WWW",#_4F
            "WZZ$",
            "WWZ", #FIX! not _4F
            "ZZZ$",
            "T_tch$",
            "TBar_tch$",
            "T_sch_lep$",
            #"WWTo2L2Nu_DPS_hpp",           
            "TTWToLNu_fxfx$",
            "TTZToLLNuNu_amc$",
            "TTZToLLNuNu_m1to10$",
            "TTGJets$",
            "TGJets_lep", 

            #missing tbc
#            "ZZTo2L2Q", 
            "WpWpJJ",
#            "WZTo1L3Nu",
#            "WGToLNuG_amcatnlo_ext",
#            "ZGTo2LG_ext",
#            "WZTo2L2Q",

            ##signal SUSY
            "SMS_TChiWZ"
            
###relics from tth             
###            "TT[WZ]_LO$",
###            "TTHnobb_pow$",
###            "TZQToLL$", "tWll$", "TTTT$", "TTWW$",
###            "WpWpJJ$",
###            "GGHZZ4L$", "VHToNonbb_ll$",
###            "WWW_ll$", "WWZ$", "WZG$",  "WW_DPS$", 
            

        ])

    if analysis == "main":
##        DatasetsAndTriggers.append( ("DoubleMuon", triggers["mumu_iso"] + triggers["3mu"]) )
        DatasetsAndTriggers.append( ("DoubleMuon",  triggers["SOS_doublemulowMET"] + triggers["mumu_iso"] + triggers["3mu"]) )
        DatasetsAndTriggers.append( ("MET",         triggers["SOS_highMET"] ) )
        DatasetsAndTriggers.append( ("EGamma",      triggers["SOS_eleTnP"] ) )
        DatasetsAndTriggers.append( ("SingleMuon",  triggers["SOS_muTnP"] ) )
##        DatasetsAndTriggers.append( ("SingleMuon", triggers["1mu_iso"]) ) ##which one?? ##PD SingleMuon o MET?
##conf db e cercare stream dato il nome del trigger

elif year == 2017 and not ch_test:
    mcSamples = byCompName(mcSamples_, [
        "DYJetsToLL_M50_LO", # for Tag and Probe studies
        "DYJetsToLL_M10to50_LO_ext,"
##        "DYJetsToLL_M50$", "TT(Lep|Semi)_pow", "TTHnobb_pow",

        ##main bkgs
        "T_tWch_noFullyHad", "TBar_tWch_noFullyHad",

        #"DYJetsToLL_M4to50_HT70to100," #Sample status = INVALID on DAS
        #"DYJetsToLL_M4to50_HT70to100_ext1", #Sample status = INVALID on DAS
        "DYJetsToLL_M4to50_HT100to200", 
        "DYJetsToLL_M4to50_HT100to200_ext1",
        "DYJetsToLL_M4to50_HT200to400",
        "DYJetsToLL_M4to50_HT200to400_ext1",
        "DYJetsToLL_M4to50_HT400to600",
        "DYJetsToLL_M4to50_HT400to600_ext1",
        "DYJetsToLL_M4to50_HT600toInf",

        "DYJetsToLL_M50_HT100to200", 
        "DYJetsToLL_M50_HT100to200_ext1",
        "DYJetsToLL_M50_HT200to400",
        "DYJetsToLL_M50_HT200to400_ext1",
        "DYJetsToLL_M50_HT400to600",
        "DYJetsToLL_M50_HT400to600_ext1",
        "DYJetsToLL_M50_HT600to800",
        "DYJetsToLL_M50_HT800to1200",
        "DYJetsToLL_M50_HT1200to2500",
        "DYJetsToLL_M50_HT2500toInf",

        "TTJets_DiLepton",

        #main VV
        "WWTo2L2Nu",
        "ZZTo2L2Nu",

        #fakesbkg
        "TTJets_SingleLeptonFromT",
        "TTJets_SingleLeptonFromTbar",

        "WJetsToLNu_HT100to200",
        "WJetsToLNu_HT200to400",
        "WJetsToLNu_HT400to600",
        "WJetsToLNu_HT600to800",
        "WJetsToLNu_HT800to1200",
        "WJetsToLNu_HT1200to2500",
        "WJetsToLNu_HT2500toInf",

        #rarebkg
        "WZTo3LNu_fxfx",
        "WWToLNuQQ",
        "WZTo1L1Nu2Q",
        "ZZTo4L",
        "WWW", #_4F
        "WZZ",
        "WWZ", #_4F
        "ZZZ",
        "T_tch",
        "TBar_tch",
        "T_sch_lep",
        "WWTo2L2Nu_DPS_hpp",
        "TTWToLNu_fxfx",
        "TTZToLLNuNu_amc",
        "TTZToLLNuNu_m1to10",
        "TTGJets",
        "TGJets_lep",

#more to be included
#            "ZZTo2L2Q",
            "WpWpJJ",
#            "WZTo1L3Nu",
#            "WGToLNuG_amcatnlo_ext",
#            "ZGTo2LG_ext",
#            "WZTo2L2Q",


        ##signal SUSY

    ])
    DatasetsAndTriggers.append( ("DoubleMuon", triggers["SOS_doublemulowMET"] + triggers["mumu_iso"] + triggers["3mu"]) )
    DatasetsAndTriggers.append( ("MET",     triggers["SOS_highMET"] ) )
    DatasetsAndTriggers.append( ("SingleElectron",  triggers["SOS_eleTnP"] ) )
    DatasetsAndTriggers.append( ("SingleMuon",      triggers["SOS_muTnP"] ) )

elif year == 2016 and not ch_test:
    mcSamples = byCompName(mcSamples_, [
        "DYJetsToLL_M50_LO", # for Tag and Probe studies
        "DYJetsToLL_M10to50_LO$",

        ##main bkgs
        "T_tWch_noFullyHad", #extensions are to be included?
        "TBar_tWch_noFullyHad",

        "DYJetsToLL_M5to50_HT100to200",
        "DYJetsToLL_M5to50_HT100to200_ext",
        "DYJetsToLL_M5to50_HT200to400",
        "DYJetsToLL_M5to50_HT200to400_ext",
        "DYJetsToLL_M5to50_HT400to600",
        "DYJetsToLL_M5to50_HT400to600_ext",
        "DYJetsToLL_M5to50_HT600toInf",
        "DYJetsToLL_M5to50_HT600toInf_ext",
##        "DYJetsToLL_M4to50_HT70to100", 
##        "DYJetsToLL_M4to50_HT70to100_ext1",
##        "DYJetsToLL_M4to50_HT100to200", 
##        "DYJetsToLL_M4to50_HT100to200_ext1",
##        "DYJetsToLL_M4to50_HT200to400",
##        "DYJetsToLL_M4to50_HT200to400_ext1",
##        "DYJetsToLL_M4to50_HT400to600",
##        "DYJetsToLL_M4to50_HT400to600_ext1",
##        "DYJetsToLL_M4to50_HT600toInf",


        "DYJetsToLL_M50_HT70to100", 
        "DYJetsToLL_M50_HT100to200",
        "DYJetsToLL_M50_HT100to200_ext",
        "DYJetsToLL_M50_HT200to400",
        "DYJetsToLL_M50_HT200to400_ext",
        "DYJetsToLL_M50_HT400to600",
        "DYJetsToLL_M50_HT400to600_ext",
        "DYJetsToLL_M50_HT600to800",
        "DYJetsToLL_M50_HT800to1200",
        "DYJetsToLL_M50_HT1200to2500",
        "DYJetsToLL_M50_HT2500toInf",
#        "DYJetsToLL_M50_HT100to200", 
#        "DYJetsToLL_M50_HT100to200_ext1",
#        "DYJetsToLL_M50_HT200to400",
#        "DYJetsToLL_M50_HT200to400_ext1",
#        "DYJetsToLL_M50_HT400to600",
#        "DYJetsToLL_M50_HT400to600_ext1",
#        "DYJetsToLL_M50_HT600to800",
#        "DYJetsToLL_M50_HT800to1200",
#        "DYJetsToLL_M50_HT1200to2500",
#        "DYJetsToLL_M50_HT2500toInf",

        "TTJets_DiLepton",

        #main VV
        "WWTo2L2Nu",
        "ZZTo2L2Nu",

        #fakesbkg
        "TTJets_SingleLeptonFromT",
        "TTJets_SingleLeptonFromTbar",

        "WJetsToLNu_HT70to100",
        "WJetsToLNu_HT100to200",
        "WJetsToLNu_HT100to200_ext",
        "WJetsToLNu_HT100to200_ext2",
        "WJetsToLNu_HT200to400",
        "WJetsToLNu_HT200to400_ext",
        "WJetsToLNu_HT200to400_ext2",
        "WJetsToLNu_HT400to600",
        "WJetsToLNu_HT400to600_ext",
        "WJetsToLNu_HT600to800",
        "WJetsToLNu_HT600to800_ext",
        "WJetsToLNu_HT800to1200",
        "WJetsToLNu_HT800to1200_ext",
        "WJetsToLNu_HT1200to2500",
        "WJetsToLNu_HT1200to2500_ext",
        "WJetsToLNu_HT2500toInf",
        "WJetsToLNu_HT2500toInf_ext",
##        "WJetsToLNu_HT100to200",
##        "WJetsToLNu_HT200to400",
##        "WJetsToLNu_HT400to600",
##        "WJetsToLNu_HT600to800",
##        "WJetsToLNu_HT800to1200",
##        "WJetsToLNu_HT1200to2500",
##        "WJetsToLNu_HT2500toInf",

        #rarebkg
        "WZTo3LNu_fxfx",
        "WWToLNuQQ",
        "WZTo1L1Nu2Q",
        "ZZTo4L",
        "WWW", #_4F
        "WZZ",
        "WWZ", #why not _4F?
        "ZZZ",
        "T_tch",
        "TBar_tch",
        "T_sch_lep",
##        "WWTo2L2Nu_DPS_hpp", #missing
        "TTWToLNu", "TTWToLNu_ext",  #_fxfx
        "TTZToLLNuNu", "TTZToLLNuNu_ext", "TTZToLLNuNu_ext2", #_amc
        "TTZToLLNuNu_m1to10",
        "TTGJets", "TTGJets_ext"
       # "TGJets_lep" #missing

#more to be included
        "ZZTo2L2Q", 
        "WpWpJJ",
        "WZTo1L3Nu",
        "WGToLNuG_amcatnlo",
        "WGToLNuG_amcatnlo_ext",
        "ZGTo2LG",
        "WZTo2L2Q",


        ##signal SUSY
        "SMS_TChiWZ"

###        "DYJetsToLL_M50$", "TT(Lep|Semi)_pow" 
    ])
    DatasetsAndTriggers.append( ("DoubleMuon",      triggers["SOS_doublemulowMET"] + triggers["mumu_iso"] + triggers["3mu"]) )
    DatasetsAndTriggers.append( ("MET",             triggers["SOS_highMET"] ) )
    DatasetsAndTriggers.append( ("SingleElectron",  triggers["SOS_eleTnP"] ) )
    DatasetsAndTriggers.append( ("SingleMuon",      triggers["SOS_muTnP"] ) )
# make MC

mcSamples=[]
# triggers=[]
# DatasetsAndTriggers=[]
print "mcSamples ",mcSamples

mcTriggers = sum((trigs for (pd,trigs) in DatasetsAndTriggers), [])
for comp in mcSamples:
    comp.triggers = mcTriggers

# make data
dataSamples = []; vetoTriggers = []
for pd, triggers in DatasetsAndTriggers:
    for comp in byCompName(allData, [pd]):
        # print 'comp',comp
        comp.triggers = triggers[:]
        comp.vetoTriggers = vetoTriggers[:]
        dataSamples.append(comp)
    vetoTriggers += triggers[:]
selectedComponents = mcSamples + dataSamples
if getHeppyOption('selectComponents'):
    selectedComponents = byCompName(selectedComponents, getHeppyOption('selectComponents').split(","))
if not ch_test: autoAAA(selectedComponents, quiet=False)##not(getHeppyOption("verboseAAA",False)))
configureSplittingFromTime(mcSamples,250 if preprocessor else 10,10)
configureSplittingFromTime(dataSamples,80 if preprocessor else 10,10)
selectedComponents, _ = mergeExtensions(selectedComponents)


#if ch_test:
    # mcSamples = byCompName(mcSamples_, ["SMS_TChiWZ"])
    # DatasetsAndTriggers.append( ("DoubleMuon",      triggers["SOS_doublemulowMET"] + triggers["mumu_iso"] + triggers["3mu"]) )
    # DatasetsAndTriggers.append( ("MET",             triggers["SOS_highMET"] ) )
    # DatasetsAndTriggers.append( ("SingleElectron",  triggers["SOS_eleTnP"] ) )
    # DatasetsAndTriggers.append( ("SingleMuon",      triggers["SOS_muTnP"] ) )
    #TChiWZ = kreator.makeMCComponent("TChiWZ","/SMS-TChiWZ_ZToLL_mZMin-0p1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_GridpackScan_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM","CMS",".*root",1.)
    #TChiWZ.files = ["/uscms_data/d1/therwig/2C2D9686-52F7-E811-A33C-F04DA274CA28.root"]

if ch_test:
    # TChiWZ = kreator.makeMCComponent("TChiWZ","/SMS-TChiWZ_ZToLL_mZMin-0p1_TuneCP2_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-GridpackScan_102X_upgrade2018_realistic_v15-v1/MINIAODSIM","CMS",".*root",1.)
    # TChiWZ.files = ["/uscms_data/d1/therwig/local_data/2C6D8A44-2C2C-584E-B87E-7C002FAD10A8.root"]    
    # selectedComponents = [TChiWZ]

    TChiWZ = kreator.makeMCComponent("DYJetsToLL_M1to4_HT100to200","/DYJetsToLL_M-1to4_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM","CMS",".*root",1.)
    TChiWZ.files = ["/uscms_data/d1/therwig/local_data/CB6680DB-4365-B142-9658-D9D01C66CE56.root"]    
    selectedComponents = [TChiWZ]

# create and set preprocessor if requested
if getHeppyOption("nanoPreProcessor"):
    from CMGTools.Production.nanoAODPreprocessor import nanoAODPreprocessor
    preproc_cfg = {2016: ("mc94X2016","data94X2016"),
                   2017: ("mc94Xv2","data94Xv2"),
                   2018: ("mc102X","data102X_ABC","data102X_D")}
    preproc_cmsswArea = "/uscms/home/therwig/nobackup/sos/CMSSW_10_2_16_UL" #MODIFY ACCORDINGLY
    preproc_mc = nanoAODPreprocessor(cfg='%s/src/PhysicsTools/NanoAOD/test/%s_NANO.py'%(preproc_cmsswArea,preproc_cfg[year][0]),cmsswArea=preproc_cmsswArea,keepOutput=True)
    if year==2018:
        preproc_data_ABC = nanoAODPreprocessor(cfg='%s/src/PhysicsTools/NanoAOD/test/%s_NANO.py'%(preproc_cmsswArea,preproc_cfg[year][1]),cmsswArea=preproc_cmsswArea,keepOutput=True, injectTriggerFilter=True, injectJSON=True)
        preproc_data_D = nanoAODPreprocessor(cfg='%s/src/PhysicsTools/NanoAOD/test/%s_NANO.py'%(preproc_cmsswArea,preproc_cfg[year][2]),cmsswArea=preproc_cmsswArea,keepOutput=True, injectTriggerFilter=True, injectJSON=True)
        for comp in selectedComponents:
            if comp.isData:
                comp.preprocessor = preproc_data_D if '2018D' in comp.name else preproc_data_ABC
            else:
                comp.preprocessor = preproc_mc
    else:
        preproc_data = nanoAODPreprocessor(cfg='%s/src/PhysicsTools/NanoAOD/test/%s_NANO.py'%(preproc_cmsswArea,preproc_cfg[year][1]),cmsswArea=preproc_cmsswArea,keepOutput=True, injectTriggerFilter=True, injectJSON=True)
        for comp in selectedComponents:
            comp.preprocessor = preproc_data if comp.isData else preproc_mc
    if year==2017:
        preproc_mcv1 = nanoAODPreprocessor(cfg='%s/src/PhysicsTools/NanoAOD/test/%s_NANO.py'%(preproc_cmsswArea,"mc94Xv1"),cmsswArea=preproc_cmsswArea,keepOutput=True)
        for comp in selectedComponents:
            if comp.isMC and "Fall17MiniAODv2" not in comp.dataset:
                print "Warning: %s is MiniAOD v1, dataset %s" % (comp.name, comp.dataset)
                comp.preprocessor = preproc_mcv1

    if getHeppyOption("fast"):
        for comp in selectedComponents:
            comp.preprocessor._cfgHasFilter = True
            comp.preprocessor._inlineCustomize = ("""
process.selectEl = cms.EDFilter("PATElectronRefSelector",
    src = cms.InputTag("slimmedElectrons"),
    cut = cms.string("pt > 4.5"),
    filter = cms.bool(False),
)
process.selectMu = cms.EDFilter("PATMuonRefSelector",
    src = cms.InputTag("slimmedMuons"),
    cut = cms.string("pt > 3"),
    filter = cms.bool(False),
)
process.skimNLeps = cms.EDFilter("PATLeptonCountFilter",
    electronSource = cms.InputTag("selectEl"),
    muonSource = cms.InputTag("selectMu"),
    tauSource = cms.InputTag(""),
    countElectrons = cms.bool(True),
    countMuons = cms.bool(True),
    countTaus = cms.bool(False),
    minNumber = cms.uint32(2),
    maxNumber = cms.uint32(999),
)
process.nanoAOD_step.insert(0, cms.Sequence(process.selectEl + process.selectMu + process.skimNLeps))
""")

cropToLumi(byCompName(selectedComponents,["T_","TBar_"]),100.)

# print summary of components to process
if getHeppyOption("justSummary"): 
    printSummary(selectedComponents)
    sys.exit(0)

from CMGTools.TTHAnalysis.tools.nanoAOD.susySOS_modules import *

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

modules = susySOS_sequence_step1
cut = susySOS_skim_cut
# Switch to Tag and Probe skimming/sequence
if getHeppyOption("TnP"):
    collection = getHeppyOption("TnPCollection", "None")
    if collection == "None":
        raise RuntimeError("You omitted the TnP collection to run on!")
    if collection != "Muon" and collection != "Electron":
        raise RuntimeError("Invalid TnP collection to run on: Should be either 'Muon' or 'Electron'!")
    modules = susySOS_sequence_TnP(year,collection)
    cut = susySOS_TnP_cut 

branchsel_in = os.environ['CMSSW_BASE']+"/src/CMGTools/TTHAnalysis/python/tools/nanoAOD/branchsel_in.txt"
branchsel_out = None
compression = "ZLIB:3" #"LZ4:4" #"LZMA:9"

POSTPROCESSOR = PostProcessor(None, [], modules = modules,
        cut = cut, prefetch = True, longTermCache = True,
        branchsel = branchsel_in, outputbranchsel = branchsel_out, compression = compression)



test = getHeppyOption("test")
if test == "94X-MC":
    TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_mtop166p5_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )
    TTLep_pow.files = ["/afs/cern.ch/user/g/gpetrucc/cmg/NanoAOD_94X_TTLep.root"]
    lepSkim.requireSameSignPair = False
    lepSkim.minJets = 0
    lepSkim.minMET = 0
    lepSkim.prescaleFactor = 0
    selectedComponents = [TTLep_pow]
elif test == "94X-MC-miniAOD":
    TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_mtop166p5_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )
    TTLep_pow.files = [ 'root://cms-xrd-global.cern.ch//store/mc/RunIIFall17MiniAOD/TTTo2L2Nu_mtop166p5_TuneCP5_PSweights_13TeV-powheg-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/70000/3CC234EB-44E0-E711-904F-FA163E0DF774.root' ]
    localfile = os.path.expandvars("/tmp/$USER/%s" % os.path.basename(TTLep_pow.files[0]))
    if os.path.exists(localfile): TTLep_pow.files = [ localfile ] 
    from CMGTools.Production.nanoAODPreprocessor import nanoAODPreprocessor
    TTLep_pow.preprocessor = nanoAODPreprocessor("/afs/cern.ch/work/g/gpetrucc/ttH/CMSSW_10_4_0/src/nanov4_NANO_cfg.py")
    selectedComponents = [TTLep_pow]
elif test == "102X-MC":
    TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2), useAAA=True )
    TTLep_pow.files = TTLep_pow.files[:1]
    selectedComponents = [TTLep_pow]
elif test in ('2','3','3s'):
    doTestN(test, selectedComponents)



print "Finished up in the SOS config"
