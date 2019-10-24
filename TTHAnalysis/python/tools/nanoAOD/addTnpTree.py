import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import TLorentzVector

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

_rootLeafType2rootBranchType = { 'UChar_t':'b', 'Char_t':'B', 'UInt_t':'i', 'Int_t':'I', 'Float_t':'F', 'Double_t':'D', 'ULong64_t':'l', 'Long64_t':'L', 'Bool_t':'O' }

class addTnpTree(Module):
    def __init__(self, year, flavor):
        self.flavor = flavor
        if self.flavor == "Electron":
            self.probeSel = lambda x : x.pt > 5 and abs(x.eta) < 2.5
            if year == 2016:
                self.tagSel = lambda x : x.pt > 29 and x.cutBased > 3 and abs(x.eta) < 2.5
            if year == 2017:
                self.tagSel = lambda x : x.pt > 37 and x.cutBased > 3 and abs(x.eta) < 2.5 # Should the "cutBased" be changed to "cutBased_Fall17_V1", since this is the ID used in this year?
            if year == 2018:
                self.tagSel = lambda x : x.pt > 34 and x.cutBased > 3 and abs(x.eta) < 2.5
            self.kMaxMass = 140
            self.kMinMass = 60

        if self.flavor == "Muon":
            self.probeSel = lambda x : x.pt > 3 and x.looseId and abs(x.eta) < 2.4
            self.tagSel = lambda x : x.pt > 29 and x.tightId and abs(x.eta) < 2.4
            self.kMaxMass = 140
            self.kMinMass = 60
        
        self.year = year
        self.i = 0


    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):

        self.out = wrappedOutputTree
        ## Dump electron / muon variables
        _brlist = inputTree.GetListOfBranches()
        branches = [( _brlist.At(i).GetName(), _brlist.At(i).FindLeaf(_brlist.At(i).GetName()).GetTypeName()) for i in xrange(_brlist.GetEntries())]
        self.lepBranches = []
        for brname, brtype in branches:
            if brname.startswith(self.flavor + "_"):
                self.lepBranches.append( (brname.replace("%s_"%self.flavor,""), brtype) )

        for branch in self.lepBranches:
            self.out.branch('Tag_%s'%branch[0], _rootLeafType2rootBranchType[branch[1]])
            self.out.branch('Probe_%s'%branch[0], _rootLeafType2rootBranchType[branch[1]])

        ## Additional variables  added by hand 
        self.out.branch("Tag_isGenMatched", "I")
        self.out.branch("Probe_isGenMatched",     "I")

        self.out.branch("TnP_mass", "F")
        self.out.branch("TnP_ht",   "F")
        self.out.branch("TnP_met",  "F")
        self.out.branch("TnP_trigger", "I")
        self.out.branch("TnP_npairs",  "I")

        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def IsMatched(self, lep, trigObjCollection):
      dRmin = 0.1
      match = False
      for trigObj in trigObjCollection:
          trigObj.mass = 0 # :) 
          dR = lep.p4().DeltaR(trigObj.p4())
          if dR < dRmin: match = True
      return match

    def matchesPrompt(self, lep, genparts):
        return (lep.genPartFlav == 1 and genparts[lep.genPartIdx].statusFlags & 1) or  (lep.genPartFlav == 15 and genparts[lep.genPartIdx].statusFlags & (1 << 5))

    def analyze(self, event):
        # Get Jet and Ele collections
        jet      = Collection(event, 'Jet')
        lepton   = Collection(event, self.flavor)
        trigObj  = Collection(event, 'TrigObj')


        #### Construct the trigger object collection containing electrons triggering a single iso electron trigger
        selTrigObj = []
        for tr in trigObj:
            if self.flavor == "Electron":
                if not abs(tr.id) == 11: continue
                if not (tr.filterBits & 2): continue
            if self.flavor == "Muon":
                if not abs(tr.id) == 13: continue
                if self.year == 2016:
                    if not ((tr.filterBits & 2) or (tr.filterBits & 8)): continue
                else:
                    if not ((tr.filterBits & 2) and (tr.filterBits & 8)): continue
            selTrigObj.append(tr)

        # Calculate event-per-event variables
        # Trigger requirement... IsoEle
        if self.flavor == "Electron":
            if   self.year == 2016:
                passTrigger = event.HLT_Ele27_WPTight_Gsf
            elif self.year == 2017:
                passTrigger = event.HLT_Ele35_WPTight_Gsf
            elif self.year == 2018:
                passTrigger = event.HLT_Ele32_WPTight_Gsf
        if self.flavor == "Muon":
            if   self.year == 2016:
                passTrigger = event.HLT_IsoMu24 or event.HLT_IsoTkMu24
            elif self.year == 2017:
                passTrigger = event.HLT_IsoMu27
            elif self.year == 2018:
                passTrigger = event.HLT_IsoMu24
            

        # Compute HT and MET
        ht = 0; met = event.METFixEE2017_pt if self.year == 17 else event.MET_pt
        jetId = 1 if self.year == 2016 else 2 
        for j in jet: 
            ht += j.pt if j.pt > 30 and abs(j.eta)  < 2.4 and j.jetId&(1<<jetId) else 0

        isdata = 0 if hasattr(event, 'Electron_genPartFlav') else 1
        if not isdata: genparts = Collection(event, 'GenPart')

        #### Selection of tag and probe electrons
        # Tag: pT, eta, tightId, iso
        # Probe: pT, eta
        pair = []
        index = 0
        for tag in lepton:
            if not self.tagSel(tag): continue
            if not self.IsMatched(tag, selTrigObj): continue
            probes = [] 
            for probe in lepton: 
                if not self.probeSel(probe): continue
                if probe.charge*tag.charge > 0: continue
                mass = (probe.p4()+tag.p4()).M()
                if mass > self.kMaxMass or mass < self.kMinMass: continue    
                probes.append( (probe,mass) )
            if len(probes) == 1: pair.append( (tag, probes[0][0], probes[0][1]) )

        # Check that we have at least one pair... calculate the mass of the pair
        if len(pair) == 0: return False # events with 1 or 2 pairs!


        self.i += 1

        # Set variables for tag, probe and event
        for thisPair in pair:
          tag, probe, mass = thisPair

          for branch in self.lepBranches:
              branchName = branch[0]
              self.out.fillBranch("Tag_%s"%branchName, getattr(tag,branchName))
              self.out.fillBranch("Probe_%s"%branchName, getattr(probe,branchName))
              
          tagMatch = 1 if isdata else self.matchesPrompt(tag,genparts)
          self.out.fillBranch("Tag_isGenMatched", tagMatch)

          probeMatch = 1 if isdata else  self.matchesPrompt(probe, genparts)
          self.out.fillBranch("Probe_isGenMatched", probeMatch)

          # TnP variables
          self.out.fillBranch("TnP_mass",     mass);
          self.out.fillBranch("TnP_trigger",  passTrigger); 
          self.out.fillBranch("TnP_npairs",   len(pair)); 
          self.out.fillBranch("TnP_met",      met);
          self.out.fillBranch("TnP_ht",       ht);
          self.out.fill()
        return False

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
