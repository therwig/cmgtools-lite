import os

conf = dict(
    muPt = 3, 
    elePt = 5, 
    #        miniRelIso = 0.4,  # we use Iperbolic, see old cfg run_susySOS_cfg.py
    sip3d = 2.5, 
    dxy =  0.05, 
    dz = 0.1, 
    minMet = 50.,
    ip3d = 0.0175,
    iperbolic_iso_0 = 20.,
    iperbolic_iso_1 = 300.,
#    eleId = "mvaFall17V2noIso_WPL", ## CHECK
#    muonId = "softMvaId" ###looseId
)
susySOS_skim_cut =  ("nMuon + nElectron >= 2 &&" + ##if heppy option fast
###        "MET_pt > {minMet}  &&"+
       "Sum$(Muon_pt > {muPt}) +"
       "Sum$(Electron_pt > {elePt}) >= 2").format(**conf) ## && Muon_miniPFRelIso_all < {miniRelIso} && Electron_miniPFRelIso_all < {miniRelIso}  #mettere qui MET_pt>50 #cp dal cfg la selezione
#cut  = ttH_skim_cut

muonSelection     = lambda l : abs(l.eta) < 2.4 and l.pt > conf["muPt"]  and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"]  and l.pfRelIso03_all*l.pt < ( conf["iperbolic_iso_0"]+conf["iperbolic_iso_1"]/l.pt) and abs(l.ip3d) < conf["ip3d"] ##is it relIso03?  ##and l.miniPFRelIso_all < conf["miniRelIso"]##l.relIso03*l.pt
electronSelection = lambda l : abs(l.eta) < 2.5 and l.pt > conf["elePt"]  and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"] and l.pfRelIso03_all*l.pt < ( conf["iperbolic_iso_0"]+conf["iperbolic_iso_1"]/l.pt) and abs(l.ip3d) < conf["ip3d"]  ##is it relIso03? ##and l.miniPFRelIso_all < conf["miniRelIso"] #l.relIso03*l.pt

#muonSelection     = lambda l : abs(l.eta) < 2.4 and l.pt > conf["muPt"]  and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"]  and ( ( l.pfIsolationR03.sumChargedHadronPt + max( l.pfIsolationR03.sumNeutralHadronEt +  l.pfIsolationR03.sumPhotonEt -  l.pfIsolationR03.sumPUPt/2,0.0) ) < ( conf["iperbolic_iso_0"]+conf["iperbolic_iso_1"]/l.pt)) and abs(l.ip3D) < conf["ip3d"] ##is it relIso03?  ##and l.miniPFRelIso_all < conf["miniRelIso"]##l.relIso03*l.pt
#electronSelection = lambda l : abs(l.eta) < 2.5 and l.pt > conf["elePt"]  and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"] and ( (l.chargedHadronIsoR(0.3) + max(l.neutralHadronIsoR(0.3)+l.photonIsoR(0.3)-l.rho*ele.EffectiveArea03,0)) < ( conf["iperbolic_iso_0"]+conf["iperbolic_iso_1"]/l.pt) ) and abs(l.ip3D) < conf["ip3d"] ##is it relIso03? ##and l.miniPFRelIso_all < conf["miniRelIso"] #l.relIso03*l.pt

from CMGTools.TTHAnalysis.tools.nanoAOD.ttHPrescalingLepSkimmer import ttHPrescalingLepSkimmer
# NB: do not wrap lepSkim a lambda, as we modify the configuration in the cfg itself 
lepSkim = ttHPrescalingLepSkimmer(0, ##do not apply prescale
                                  muonSel = muonSelection, electronSel = electronSelection,
                                  minLeptonsNoPrescale = 2, # things with less than 2 leptons are rejected irrespectively of the prescale
                                  minLeptons = 2, requireSameSignPair = False,
                                  jetSel = lambda j : j.pt > 25 and abs(j.eta) < 2.4  and j.jetId > 0, 
                                  minJets = 0, minMET = 0)

from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import collectionMerger
lepMerge = collectionMerger(input = ["Electron","Muon"], 
                            output = "LepGood", 
                            selector = dict(Muon = muonSelection, Electron = electronSelection))

from CMGTools.TTHAnalysis.tools.nanoAOD.ttHLeptonCombMasses import ttHLeptonCombMasses
lepMasses = ttHLeptonCombMasses( [ ("Muon",muonSelection), ("Electron",electronSelection) ], maxLeps = 4)

from CMGTools.TTHAnalysis.tools.nanoAOD.autoPuWeight import autoPuWeight
from CMGTools.TTHAnalysis.tools.nanoAOD.yearTagger import yearTag
from CMGTools.TTHAnalysis.tools.nanoAOD.xsecTagger import xsecTag
from CMGTools.TTHAnalysis.tools.nanoAOD.lepJetBTagAdder import lepJetBTagCSV, lepJetBTagDeepCSV, eleJetBTagDeepCSV, muonJetBTagDeepCSV

susySOS_sequence_step1 = [lepSkim, lepMerge, autoPuWeight, yearTag, xsecTag, lepJetBTagCSV, lepJetBTagDeepCSV, lepMasses]


#==== 
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from CMGTools.TTHAnalysis.tools.nanoAOD.ttHLepQCDFakeRateAnalyzer import ttHLepQCDFakeRateAnalyzer
lepFR = ttHLepQCDFakeRateAnalyzer(jetSel = lambda j : j.pt > 25 and abs(j.eta) < 2.4,
                                  pairSel = lambda pair : deltaR(pair[0].eta, pair[0].phi, pair[1].eta, pair[1].phi) > 0.7,
                                  maxLeptons = 1, requirePair = True)

#susySOS_sequence_step1_FR = [m for m in susySOS_sequence_step1 if m != lepSkim] + [ lepFR ]
#ttH_skim_cut_FR = ("nMuon + nElectron >= 1 && nJet >= 1 && Sum$(Jet_pt > 25 && abs(Jet_eta)<2.4) >= 1 &&" + 
#       "Sum$(Muon_pt > {muPt} && Muon_miniPFRelIso_all < {miniRelIso} && Muon_sip3d < {sip3d}) +"
#       "Sum$(Electron_pt > {muPt} && Electron_miniPFRelIso_all < {miniRelIso} && Electron_sip3d < {sip3d} && Electron_{eleId}) >= 1").format(**conf)


#==== items below are normally run as friends ====

def ttH_idEmu_cuts_E3(lep):
    if (abs(lep.pdgId)!=11): return True
    if (lep.hoe>=(0.10-0.00*(abs(lep.eta+lep.deltaEtaSC)>1.479))): return False
    if (lep.eInvMinusPInv<=-0.04): return False
    if (lep.sieie>=(0.011+0.019*(abs(lep.eta+lep.deltaEtaSC)>1.479))): return False
    return True

def conept_TTH(lep):
    if (abs(lep.pdgId)!=11 and abs(lep.pdgId)!=13): return lep.pt
    if (abs(lep.pdgId)!=13 or lep.mediumId>0) and lep.mvaTTH > 0.90: return lep.pt
    else: return 0.90 * lep.pt * (1 + lep.jetRelIso)


def clean_and_FO_selection_TTH(lep):
    return lep.conept>10 and lep.jetBTagDeepCSV<0.4941 and (abs(lep.pdgId)!=11 or ttH_idEmu_cuts_E3(lep)) \
        and (lep.mvaTTH>0.90 or \
             (abs(lep.pdgId)==13 and lep.jetBTagDeepCSV<0.07 and lep.segmentComp>0.3 and 1/(1 + lep.jetRelIso)>0.60) or \
             (abs(lep.pdgId)==11 and lep.jetBTagDeepCSV<0.07 and lep.mvaFall17V1noIso>0.5 and 1/(1 + lep.jetRelIso)>0.60)) 

import numpy
from numpy import log
def calculateRawMVA(score):
    if score == -1.:
        return -999.
    elif score == 1.:
        return 999.
    else:
        return -0.5*numpy.log((1-score)/(1+score))


def SOSTightID2018(lep):
    if (lep.pt < 10): ##loose at low pt
        return lep.mvaFall17V2noIso_WPL
    else: #susy tight at higher, from https://twiki.cern.ch/twiki/pub/CMS/SUSLeptonSF/Run2_SUSYwp_EleCB_MVA_8Jan19.pdf
        mvaRaw = calculateRawMVA(lep.mvaFall17V2noIso)
        if abs(lep.eta)<0.8:
            if lep.pt<25:
                return mvaRaw > 4.277 + 0.112*(lep.pt - 25)
            else:
                return mvaRaw > 4.277
        elif abs(lep.eta)>=0.8 and abs(lep.eta)<1.479:
            if lep.pt<25:
                return mvaRaw > 3.152 + 0.60*(lep.pt - 25)
            else:
                return mvaRaw > 3.152
        elif abs(lep.eta)>=1.479:
            if lep.pt<25:
                return mvaRaw > 2.359 + 0.89*(lep.pt - 25)
            else:
                return mvaRaw > 2.359


def susyEleIdParametrization(p1,p2,pt,year):
    if year ==  2016 or year ==2018:
        return p1 + p2*(pt-25.)
    else:
        return p1 + (p2/15.)*(pt-10.)

def VLooseFOEleID(lep,year):# from https://twiki.cern.ch/twiki/pub/CMS/SUSLeptonSF/Run2_SUSYwp_EleCB_MVA_8Jan19.pdf
    if year == 2016:
        cuts = dict(cEB = [-0.259, -0.388, 0.109, -0.388], 
                    oEB = [-0.256, -0.696, 0.106, -0.696],
                    EE  = [-1.630, -1.219, 0.148, -1.219],
                    IdVersion = "mvaFall17V2noIso") 
    elif year == 2017:
        cuts = dict(cEB = [-0.135, -0.930, 0.043, -0.887], 
                    oEB = [-0.417, -0.930, 0.040, -0.890],
                    EE  = [-0.470, -0.942, 0.032, -0.910],
                    IdVersion = "mvaFall17V1noIso") 
    elif year == 2018:
        cuts = dict(cEB = [+0.053, -0.106, 0.062, -0.106], 
                    oEB = [-0.434, -0.769, 0.038, -0.769],
                    EE  = [-0.956, -1.461, 0.042, -1.461],
                    IdVersion = "mvaFall17V2noIso") 
    else:
        print "Year not in [2016,2017,2018], returning False"
        return False
    mvaValue = getattr(lep, cuts["IdVersion"]) if year==2017 else  calculateRawMVA(getattr(lep, cuts["IdVersion"])) ##raw for 2016 and 2018, normalized for 2017
    if abs(lep.eta)<0.8:
        if lep.pt<10:
            return mvaValue > cuts["cEB"][0]
        elif lep.pt<25:
            return mvaValue > susyEleIdParametrization( cuts["cEB"][1],  cuts["cEB"][2], lep.pt, year)
        else:
            return mvaValue >  cuts["cEB"][3]
    elif abs(lep.eta)>=0.8 and abs(lep.eta)<1.479:
        if lep.pt<10:
            return mvaValue > cuts["oEB"][0]
        elif lep.pt<25:
            return mvaValue > susyEleIdParametrization( cuts["oEB"][1],  cuts["oEB"][2], lep.pt, year)
        else:
            return mvaValue >  cuts["oEB"][3]
    elif abs(lep.eta)>=1.479:
        if lep.pt<10:
            return mvaValue > cuts["EE"][0]
        elif lep.pt<25:
            return mvaValue > susyEleIdParametrization( cuts["EE"][1],  cuts["EE"][2], lep.pt, year)
        else:
            return mvaValue >  cuts["EE"][3]



def tightEleID(lep,year):# from https://twiki.cern.ch/twiki/pub/CMS/SUSLeptonSF/Run2_SUSYwp_EleCB_MVA_8Jan19.pdf
    if year == 2016:
        cuts = dict(cEB = [3.447, 0.063, 4.392], 
                    oEB = [2.522, 0.058, 3.392],
                    EE  = [1.555, 0.075, 2.680],
                    IdVersion = "mvaFall17V2noIso",
                    wpLowPt = "WP80") 
    elif year == 2017:
        cuts = dict(cEB = [0.200, 0.032, 0.680], 
                    oEB = [0.100, 0.025, 0.475],
                    EE  = [-0.100, 0.028, 0.320],
                    IdVersion = "mvaFall17V1noIso",
                    wpLowPt = "WP90") 
    elif year == 2018:
        cuts = dict(cEB = [4.277, 0.112, 4.277], 
                    oEB = [3.152, 0.060, 3.152],
                    EE  = [2.359, 0.087, 2.359],
                    IdVersion = "mvaFall17V2noIso",
                    wpLowPt = "WP80") 
    else:
        print "Year not in [2016,2017,2018], returning False"
        return False
    mvaValue = getattr(lep, cuts["IdVersion"]) if year==2017 else  calculateRawMVA(getattr(lep, cuts["IdVersion"])) ##raw for 2016 and 2018, normalized for 2017
    if lep.pt<10:
        return getattr(lep, cuts["IdVersion"]+"_"+cuts["wpLowPt"])
    if abs(lep.eta)<0.8:
        if lep.pt<25:
            return mvaValue > susyEleIdParametrization( cuts["cEB"][0],  cuts["cEB"][1], lep.pt, year)
        elif lep.pt<40: #2016 still has slope between 25 and 40
            if year == 2016:
                return mvaValue > susyEleIdParametrization( cuts["cEB"][0],  cuts["cEB"][1], lep.pt, year)
            else:
                return mvaValue >  cuts["cEB"][2]
        else:
            return mvaValue >  cuts["cEB"][2]

    elif abs(lep.eta)>=0.8 and abs(lep.eta)<1.479:
        if lep.pt<25:
            return mvaValue > susyEleIdParametrization( cuts["oEB"][0],  cuts["oEB"][1], lep.pt, year)
        elif lep.pt<40:
            if year == 2016:
                return mvaValue > susyEleIdParametrization( cuts["cEB"][0],  cuts["cEB"][1], lep.pt, year)
            else:
                return mvaValue >  cuts["oEB"][2]
        else:
            return mvaValue >  cuts["oEB"][2]
    elif abs(lep.eta)>=1.479:
        if lep.pt<25:
            return mvaValue > susyEleIdParametrization( cuts["EE"][0],  cuts["EE"][1], lep.pt, year)
        elif lep.pt<40:
            if year == 2016:
                return mvaValue > susyEleIdParametrization( cuts["EE"][0],  cuts["EE"][1], lep.pt, year)
            else:
                return mvaValue >  cuts["EE"][2]
        else:
            return mvaValue >  cuts["EE"][2]




def clean_and_FO_selection_SOS(lep, year):
    bTagCut = 0.4 if year==2016 else 0.1522 if year==2017 else 0.1241 ##2016 loose recomm is 0.2217, while 0.4 derived to match 2018 performance
#    print "btagDeepB ",lep.btagDeepB
 #   print "jetBTagDeepCSV ",lep.jetBTagDeepCSV
    return lep.jetBTagDeepCSV < bTagCut and ( (abs(lep.pdgId)==11 and VLooseFOEleID(lep, year) and lep.lostHits==0 and lep.convVeto)
                                         or (abs(lep.pdgId)==13 and lep.softId ) )

def clean_and_FO_selection_SOS_noBtag(lep, year):
    return ( (abs(lep.pdgId)==11 and VLooseFOEleID(lep, year) and lep.lostHits==0 and lep.convVeto)
                                         or (abs(lep.pdgId)==13 and lep.softId ) )


##tightLeptonSel = lambda lep : clean_and_FO_selection_TTH(lep) and (abs(lep.pdgId)!=13 or lep.mediumId>0) and lep.mvaTTH > 0.90
tightLeptonSel_SOS = lambda lep,year : clean_and_FO_selection_SOS(lep,year) and ((abs(lep.pdgId)==13 or tightEleID(lep, year) ) and lep.pfRelIso03_all<0.5 and (lep.pfRelIso03_all*lep.pt)<5. and abs(lep.ip3d)<0.01 and lep.sip3d<2)


# (abs(lep.pdgId)!=13 or lep.mediumId>0) and lep.mvaTTH > 0.90



fullCleaningLeptonSel_noBtag = lambda lep,year :( (abs(lep.pdgId)==11 and (VLooseFOEleID(lep, year) and lep.lostHits<=1)) or (abs(lep.pdgId)==13 and lep.looseId)) and clean_and_FO_selection_SOS_noBtag(lep, year) #veryLooseFO wp
fullTightLeptonSel_noBtag = lambda lep,year : ((abs(lep.pdgId)==11 and (VLooseFOEleID(lep, year) and lep.lostHits<=1)) or (abs(lep.pdgId)==13 and lep.looseId)) and clean_and_FO_selection_SOS_noBtag(lep, year) and ((abs(lep.pdgId)==13 or tightEleID(lep, year) ) and lep.pfRelIso03_all<0.5 and (lep.pfRelIso03_all*lep.pt)<5. and abs(lep.ip3d)<0.01 and lep.sip3d<2) #veryLooseFO wp


fullCleaningLeptonSel = lambda lep,year : ((abs(lep.pdgId)==11 and (VLooseFOEleID(lep, year) and lep.lostHits<=1)) or (abs(lep.pdgId)==13 and lep.looseId)) and clean_and_FO_selection_SOS(lep, year) #veryLooseFO wp
fullTightLeptonSel = lambda lep,year : ((abs(lep.pdgId)==11 and (VLooseFOEleID(lep, year) and lep.lostHits<=1)) or (abs(lep.pdgId)==13 and lep.looseId)) and clean_and_FO_selection_SOS(lep, year) and ((abs(lep.pdgId)==13 or tightEleID(lep, year) ) and lep.pfRelIso03_all<0.5 and (lep.pfRelIso03_all*lep.pt)<5. and abs(lep.ip3d)<0.01 and lep.sip3d<2) #veryLooseFO wp


from CMGTools.TTHAnalysis.tools.functionsTTH import tauID_oldDMdR0p3wLT2017v2_WP # FIXME get rid of this after validation
foTauSel = lambda tau: False #tau.pt > 20 and abs(tau.eta)<2.3 and abs(tau.dxy) < 1000 and abs(tau.dz) < 0.2 and tauID_oldDMdR0p3wLT2017v2_WP(tau.pt,tau.rawMVAoldDMdR032017v2,1) and tau.idDecayMode
tightTauSel = lambda tau: False #tauID_oldDMdR0p3wLT2017v2_WP(tau.pt,tau.rawMVAoldDMdR032017v2,2)

from CMGTools.TTHAnalysis.tools.combinedObjectTaggerForCleaning import CombinedObjectTaggerForCleaning
from CMGTools.TTHAnalysis.tools.nanoAOD.fastCombinedObjectRecleaner import fastCombinedObjectRecleaner
recleaner_step1 = lambda : CombinedObjectTaggerForCleaning("InternalRecl",
                                       #looseLeptonSel = lambda lep : lep.miniPFRelIso_all < 0.4 and lep.sip3d < 8,

                                       looseLeptonSel = lambda lep,year : ((abs(lep.pdgId)==11 and (VLooseFOEleID(lep, year) and lep.lostHits<=1))) or (abs(lep.pdgId)==13 and lep.looseId),

                                       cleaningLeptonSel = lambda lep,year : clean_and_FO_selection_SOS(lep, year), #veryLooseFO wp
                                       FOLeptonSel = lambda lep,year : clean_and_FO_selection_SOS(lep, year), #veryLooseFO wp
                                       tightLeptonSel = tightLeptonSel_SOS, #tight wp
                                       FOTauSel = foTauSel,
                                       tightTauSel = tightTauSel,
                                       selectJet = lambda jet: abs(jet.eta)<2.4 and jet.pt > 25 and jet.jetId > 0, # FIXME need to select on pt or ptUp or ptDown
                                        coneptdef = lambda lep: lep.pt)
recleaner_step2_mc = lambda : fastCombinedObjectRecleaner(label="Recl", inlabel="_InternalRecl",
                                       cleanTausWithLooseLeptons=True,
                                       cleanJetsWithFOTaus=True,
                                       doVetoZ=False, doVetoLMf=False, doVetoLMt=False,
                                       jetPts=[25,40],
                                       jetPtsFwd=[25,40],
#                                       btagL_thr=0.4,#0.1241,#0.1522,
#                                       btagM_thr=0.6324,#0.4184,#0.4941,
                                       btagL_thr=lambda year : 0.4 if year==2016 else 0.1522 if year==2017 else 0.1241,#      0.4 if year == 2016 elif 0.1241 if #0.1241,#0.1522,
                                       btagM_thr=lambda year : 0.6324 if year==2016 else 0.4941 if year==2017 else 0.4184,#0.6324,#0.4184,#0.4941,
                                       isMC = True)
recleaner_step2_data = lambda : fastCombinedObjectRecleaner(label="Recl", inlabel="_InternalRecl",
                                         cleanTausWithLooseLeptons=True,
                                         cleanJetsWithFOTaus=True,
                                         doVetoZ=False, doVetoLMf=False, doVetoLMt=False,
                                         jetPts=[25,40],
                                         jetPtsFwd=[25,40],
#                                         btagL_thr=0.4,#0.1241,#0.1522,
#                                         btagM_thr=0.6324,#0.4184,#0.4941,
                                         btagL_thr=lambda year : 0.4 if year==2016 else 0.1522 if year==2017 else 0.1241,#0.4,#0.1241,#0.1522,
                                         btagM_thr=lambda year : 0.6324 if year==2016 else 0.4941 if year==2017 else 0.4184,#0.6324,#0.4184,#0.4941,
                                         isMC = False)

from CMGTools.TTHAnalysis.tools.eventVars_2lss import EventVars2LSS
eventVars = lambda : EventVars2LSS('','Recl', doSystJEC=False)

from CMGTools.TTHAnalysis.tools.objTagger import ObjTagger
isMatchRightCharge = lambda : ObjTagger('isMatchRightCharge','LepGood', [lambda l,g : (l.genPartFlav==1 or l.genPartFlav == 15) and (g.pdgId*l.pdgId > 0) ], linkColl='GenPart',linkVar='genPartIdx')
mcMatchId     = lambda : ObjTagger('mcMatchId','LepGood', [lambda l : (l.genPartFlav==1 or l.genPartFlav == 15) ])
mcPromptGamma = lambda : ObjTagger('mcPromptGamma','LepGood', [lambda l : (l.genPartFlav==22)])
mcMatch_seq   = [ isMatchRightCharge, mcMatchId ,mcPromptGamma]

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import jetmetUncertainties2016, jetmetUncertainties2017, jetmetUncertainties2018
from CMGTools.TTHAnalysis.tools.nanoAOD.lepJetBTagAdder import eleJetBTagDeepCSV, muonJetBTagDeepCSV, eleJetBTagCSV, muonJetBTagCSV

isVLFOEle = lambda : ObjTagger('isVLFOEle', "Electron", [lambda lep,year : (VLooseFOEleID(lep, year)) ])
isTightEle = lambda : ObjTagger('isTightEle', "Electron", [lambda lep,year : (tightEleID(lep, year))  ])
isCleanEle_noBtag = lambda : ObjTagger('isCleanEle_noBtag', "Electron", [ lambda lep,year: fullCleaningLeptonSel_noBtag(lep,year) and electronSelection(lep)  ])
isCleanMu_noBtag = lambda : ObjTagger('isCleanMu_noBtag', "Muon", [ lambda lep,year: fullCleaningLeptonSel_noBtag(lep,year) and muonSelection(lep) ])

isTightSOSEle_noBtag = lambda : ObjTagger('isTightSOSEle_noBtag', "Electron", [ lambda lep,year: fullTightLeptonSel_noBtag(lep,year) and electronSelection(lep) ])
isTightSOSMu_noBtag = lambda : ObjTagger('isTightSOSMu_noBtag', "Muon", [ lambda lep,year: fullTightLeptonSel_noBtag(lep,year) and muonSelection(lep) ])

isCleanEle = lambda : ObjTagger('isCleanEle', "Electron", [ lambda lep,year: fullCleaningLeptonSel(lep,year) and electronSelection(lep) ])
isCleanMu = lambda : ObjTagger('isCleanMu', "Muon", [ lambda lep,year: fullCleaningLeptonSel(lep,year) and muonSelection(lep) ])

isTightSOSEle = lambda : ObjTagger('isTightSOSEle', "Electron", [ lambda lep,year: fullTightLeptonSel(lep,year) and electronSelection(lep) ])
isTightSOSMu = lambda : ObjTagger('isTightSOSMu', "Muon", [ lambda lep,year: fullTightLeptonSel(lep,year) and muonSelection(lep) ])

isTightSOSLepGood = lambda : ObjTagger('isTightSOSLepGood', "LepGood", [ fullTightLeptonSel ])




isTightLepDY = lambda : ObjTagger('isTightLepDY', "LepGood", [   lambda lep,year : clean_and_FO_selection_SOS(lep,year) and 
                                                                (
                                                                     (abs(lep.pdgId)==13 or tightEleID(lep, year) 
                                                                  ) 
                                                                and lep.pfRelIso03_all<0.5 
                                                                and (
                                                                          (lep.pfRelIso03_all*lep.pt)<5. or lep.pfRelIso03_all<0.1 
                                                                     ) 
                                                                 )
                                                             ]) #no sip3d cut, no ip3d cut, relax iso cut
isTightLepTT = lambda : ObjTagger('isTightLepTT', "LepGood", [ lambda lep,year : clean_and_FO_selection_SOS(lep,year) and 
                                                                  ( 
                                                                      (abs(lep.pdgId)==13 or tightEleID(lep, year) 
                                                                   ) 
                                                                      and lep.pfRelIso03_all<0.5 
                                                                      and ( 
                                                                          (lep.pfRelIso03_all*lep.pt)<5. or lep.pfRelIso03_all<0.1 ) 
                                                                      and abs(lep.ip3d)<0.01 
                                                                      and lep.sip3d<2)      ]) #relax iso cut
isTightLepVV = lambda : ObjTagger('isTightLepVV', "LepGood", [ lambda lep,year : clean_and_FO_selection_SOS(lep,year) and ((abs(lep.pdgId)==13 or tightEleID(lep, year) ) and lep.pfRelIso03_all<0.5 and ( (lep.pfRelIso03_all*lep.pt)<5. or lep.pfRelIso03_all<0.1 ) and abs(lep.ip3d)<0.01 and lep.sip3d<2)      ]) #relax iso cut
isTightLepWZ = lambda : ObjTagger('isTightLepWZ', "LepGood", [ lambda lep,year : clean_and_FO_selection_SOS(lep,year) and ((abs(lep.pdgId)==13 or tightEleID(lep, year) ) and lep.pfRelIso03_all<0.5 and ( (lep.pfRelIso03_all*lep.pt)<5. or lep.pfRelIso03_all<0.1 ) and abs(lep.ip3d)<0.01 and lep.sip3d<2)      ]) #relax iso cut

eleSel_seq = [isVLFOEle, isTightEle]
tightLepCR_seq = [isTightLepDY,isTightLepTT,isTightLepVV,isTightLepWZ]


#btag weights
from CMGTools.TTHAnalysis.tools.bTagEventWeightsCSVFullShape import BTagEventWeightFriend
eventBTagWeight_16 = lambda : BTagEventWeightFriend(csvfile=os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/btag/DeepCSV_2016LegacySF_V1.csv", discrname="btagDeepB")
eventBTagWeight_17 = lambda : BTagEventWeightFriend(csvfile=os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/btag/DeepCSV_94XSF_V4_B_F.csv", discrname="btagDeepB")
eventBTagWeight_18 = lambda : BTagEventWeightFriend(csvfile=os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/btag/DeepCSV_102XSF_V1.csv", discrname="btagDeepB")


### TnP stuff
susySOS_TnP_cut =  ("Sum$(Muon_pt > 3.0 && fabs(Muon_eta) < 2.4 && Muon_looseId == 1) >= 2 || " +
        "Sum$(Electron_pt > 5.0 && fabs(Electron_eta) < 2.5) >= 2")

from CMGTools.TTHAnalysis.tools.nanoAOD.lepJetBTagAdder import eleJetBTagDeepCSV, muonJetBTagDeepCSV, eleJetBTagCSV, muonJetBTagCSV
from CMGTools.TTHAnalysis.tools.nanoAOD.addTnpTree import addTnpTree

def TnPMasses(collection):
    if collection == "Muon": return ttHLeptonCombMasses( [("Muon", (lambda l : abs(l.eta) < 2.4 and l.pt > 3.0 and l.looseId == 1) )], maxLeps = 4)
    if collection == "Electron": return ttHLeptonCombMasses( [("Electron", (lambda l : abs(l.eta) < 2.5 and l.pt > 5.0) )], maxLeps = 4)
def TnPisTightLepDY(collection):
    if collection == "Muon": return ( lambda : ObjTagger('isTightLepDY', "Muon", [ lambda lep,year : clean_and_FO_selection_SOS(lep,year) and muonSelection(lep) and
        ( (abs(lep.pdgId)==13 or tightEleID(lep, year) ) and lep.pfRelIso03_all<0.5 and ( (lep.pfRelIso03_all*lep.pt)<5. or lep.pfRelIso03_all<0.1 ) ) ]) )
    if collection == "Electron": return ( lambda : ObjTagger('isTightLepDY', "Electron", [ lambda lep,year : clean_and_FO_selection_SOS(lep,year) and electronSelection(lep) and
        ( (abs(lep.pdgId)==13 or tightEleID(lep, year) ) and lep.pfRelIso03_all<0.5 and ( (lep.pfRelIso03_all*lep.pt)<5. or lep.pfRelIso03_all<0.1 ) ) ]) )
def TnPisTightLepTT(collection):
    if collection == "Muon": return ( lambda : ObjTagger('isTightLepTT', "Muon", [ lambda lep,year : clean_and_FO_selection_SOS(lep,year) and muonSelection(lep) and
        ( (abs(lep.pdgId)==13 or tightEleID(lep, year) ) and lep.pfRelIso03_all<0.5 and ( (lep.pfRelIso03_all*lep.pt)<5. or lep.pfRelIso03_all<0.1 ) and abs(lep.ip3d)<0.01 and lep.sip3d<2 ) ]) )
    if collection == "Electron": return ( lambda : ObjTagger('isTightLepTT', "Electron", [ lambda lep,year : clean_and_FO_selection_SOS(lep,year) and electronSelection(lep) and
        ( (abs(lep.pdgId)==13 or tightEleID(lep, year) ) and lep.pfRelIso03_all<0.5 and ( (lep.pfRelIso03_all*lep.pt)<5. or lep.pfRelIso03_all<0.1 ) and abs(lep.ip3d)<0.01 and lep.sip3d<2 ) ]) )
def TnPisTightLepVV(collection):
    if collection == "Muon": return ( lambda : ObjTagger('isTightLepVV', "Muon", [ lambda lep,year : clean_and_FO_selection_SOS(lep,year) and muonSelection(lep) and
        ( (abs(lep.pdgId)==13 or tightEleID(lep, year) ) and lep.pfRelIso03_all<0.5 and ( (lep.pfRelIso03_all*lep.pt)<5. or lep.pfRelIso03_all<0.1 ) and abs(lep.ip3d)<0.01 and lep.sip3d<2 ) ]) )
    if collection == "Electron": return ( lambda : ObjTagger('isTightLepVV', "Electron", [ lambda lep,year : clean_and_FO_selection_SOS(lep,year) and electronSelection(lep) and
        ( (abs(lep.pdgId)==13 or tightEleID(lep, year) ) and lep.pfRelIso03_all<0.5 and ( (lep.pfRelIso03_all*lep.pt)<5. or lep.pfRelIso03_all<0.1 ) and abs(lep.ip3d)<0.01 and lep.sip3d<2 ) ]) )
def TnPisTightLepWZ(collection):
    if collection == "Muon": return ( lambda : ObjTagger('isTightLepWZ', "Muon", [ lambda lep,year : clean_and_FO_selection_SOS(lep,year) and muonSelection(lep) and
        ( (abs(lep.pdgId)==13 or tightEleID(lep, year) ) and lep.pfRelIso03_all<0.5 and ( (lep.pfRelIso03_all*lep.pt)<5. or lep.pfRelIso03_all<0.1 ) and abs(lep.ip3d)<0.01 and lep.sip3d<2 ) ]) )
    if collection == "Electron": return ( lambda : ObjTagger('isTightLepWZ', "Electron", [ lambda lep,year : clean_and_FO_selection_SOS(lep,year) and electronSelection(lep) and
        ( (abs(lep.pdgId)==13 or tightEleID(lep, year) ) and lep.pfRelIso03_all<0.5 and ( (lep.pfRelIso03_all*lep.pt)<5. or lep.pfRelIso03_all<0.1 ) and abs(lep.ip3d)<0.01 and lep.sip3d<2 ) ]) )
def TnP(year,collection):
    return ( lambda : addTnpTree(year,collection) )

def susySOS_sequence_TnP(year,collection): # TnP module should always be last
    if collection == "Muon":
        return [autoPuWeight, yearTag, xsecTag, muonJetBTagCSV, muonJetBTagDeepCSV, TnPMasses(collection), isCleanMu, isTightSOSMu, TnPisTightLepDY(collection), TnPisTightLepTT(collection), TnPisTightLepVV(collection), TnPisTightLepWZ(collection), TnP(year,collection) ]
    if collection == "Electron":
        return [autoPuWeight, yearTag, xsecTag, eleJetBTagCSV, eleJetBTagDeepCSV, TnPMasses(collection), isVLFOEle, isTightEle, isCleanEle, isTightSOSEle, TnPisTightLepDY(collection), TnPisTightLepTT(collection), TnPisTightLepVV(collection), TnPisTightLepWZ(collection), TnP(year,collection) ]
