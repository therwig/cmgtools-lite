from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 

from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput

class truthAna( Module ):
    def __init__(self,
                 label = "truth_",
             ):
        self.label = label
        self.lepIDs=[11,13,15]

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        self.wrappedOutputTree.branch(self.label+"_mll",'F')
        self.wrappedOutputTree.branch(self.label+"_nTruthLep",'I')
        self.wrappedOutputTree.branch(self.label+"_ht",'F')

    def analyze(self, event):
        genParts = Collection(event, 'GenPart')
        n2_lep_vecs=[]
        for ip,p in enumerate(genParts):
            # find leptons
            if p.genPartIdxMother>=0 and abs(genParts[p.genPartIdxMother].pdgId) in self.lepIDs:
                continue #skip leptons from leptons (incl taus) to avoid double-counting
            if abs(p.pdgId) in self.lepIDs:
                if p.genPartIdxMother>=0 and p.statusFlags & (1<<0): 
                    n2_lep_vecs += [p.p4()]
                                    
        mll=-1.
        if len(n2_lep_vecs)>1:
            mll=(n2_lep_vecs[0]+n2_lep_vecs[1]).M()
        self.wrappedOutputTree.fillBranch(self.label+"_mll", mll)
        self.wrappedOutputTree.fillBranch(self.label+"_nTruthLep", len(n2_lep_vecs))

        genJets = Collection(event, 'GenJet')
        ht=0
        for j in genJets:
            ht += j.pt
        self.wrappedOutputTree.fillBranch(self.label+"_ht", ht)

        return True

