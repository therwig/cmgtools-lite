from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 

from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
import ROOT
from math import sqrt

class mllReweight( Module ):
    """ Calculate weights to correct unpolarized N2 > l+ l- N1 decays for 
    the case of positive/negative product of eigenvalues m(N1)*m(N2).
    (For Higgsino, this is is negative, for wino/bino it may be either.)
    """
    def __init__(self,
                 label = "mll_rwt",
             ):
        self.label = label
        self.events = 0

        # lineshape functions (ROOT.TF1s)
        self.numerator_pos={}
        self.numerator_neg={}
        self.denominator={}

        #utilities
        self.mZ=91.2
        self.barcodeN1=1000022
        self.barcodeN2=1000023
        self.lepIDs=[11,13,15]
        #self.barcodeC1=1000024

        # Weights only relevant for the far-off-shell case.
        # Integral diverges over the Z pole, so specify the 
        # maximum N2-N1 for which weights are calculated
        self.max_dm=80.

        # testing only
        self.run_diagnostics = True
        if self.run_diagnostics:
            self.rand=ROOT.TRandom3(1776)

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        self.wrappedOutputTree.branch(self.label+"_pos",'F')
        self.wrappedOutputTree.branch(self.label+"_neg",'F')

        if self.run_diagnostics:
            self.wrappedOutputTree.branch(self.label+"_fpos",'F')
            self.wrappedOutputTree.branch(self.label+"_fneg",'F')
            self.wrappedOutputTree.branch(self.label+"_fPS",'F')
            self.wrappedOutputTree.branch(self.label+"_mll",'F')
            self.wrappedOutputTree.branch(self.label+"_mllRel",'F')
            self.wrappedOutputTree.branch(self.label+"_dm",'F')
            self.wrappedOutputTree.branch(self.label+"_nlep",'F')

    def GetNormFunction(self, name, formula, mN1, mN2):
        """return a function from a formula, 
        normalized over its region of validity"""
        # help out integration step w/ basic guess
        normGuess = (0.5*(mN2-mN1))*sqrt(((mN2-mN1)**2-(0.5*(mN2-mN1))**2)*((mN2+mN1)**2-(0.5*(mN2-mN1))**2))
        fRaw = ROOT.TF1("raw_"+name, "1./{}*({})".format(normGuess,formula), 0, mN2-mN1)
        norm = fRaw.Integral(0, mN2-mN1)
        # print mN1, mN2, norm
        return ROOT.TF1(name, "1./({}*{})*({})".format(normGuess,norm,formula), 0, mN2-mN1)

    def StoreReweightFunctions(self, mN1, mN2):
        """The first time a mass point is processed, compute the weight functions"""
        # formula for mLL lineshape, where params are the signed eigenvalue sums and differences
        phaseSpace = "x*sqrt((({0})**2-x**2)*(({1})**2-x**2))" # generic pythia 3-body decay
        fullCalc = "x*sqrt(x**4-x**2*(({0})**2+({1})**2)+(({0})*({1}))**2)/" + \
                   "(x**2-({2})**2)^2*(-2*x**4+x**2*(2*({1})**2-({0})**2)+(({0})*({1}))**2)"
        fPos = self.GetNormFunction("fPos_{}_{}".format(mN1, mN2),
                               fullCalc.format(mN2-mN1, mN2+mN1, self.mZ), mN1, mN2)
        fNeg = self.GetNormFunction("fNeg_{}_{}".format(mN1, mN2),
                               fullCalc.format(mN2+mN1, mN2-mN1, self.mZ), mN1, mN2)
        fPS  = self.GetNormFunction("fPS_{}_{}".format(mN1, mN2),
                               phaseSpace.format(mN2-mN1, mN2+mN1), mN1, mN2)        

        self.numerator_pos[(mN1, mN2)] = fPos
        self.numerator_neg[(mN1, mN2)] = fNeg
        self.denominator[(mN1, mN2)] = fPS

    def GetWeights(self, mll, mN1, mN2):
        # for out of bounds mll, or failures in computation
        if mN2-mN1 > self.max_dm or mll<-1+1e5:
            return (1.,1.)
        # correct unphysical configurations due to imperfect precision
        if mll < 0: mll=1e-5
        elif mll > mN2-mN1: mll=mN2-mN1-1e5
        # retrieve reweighting functions if not already computed
        if not((mN1,mN2) in self.denominator):
            self.StoreReweightFunctions(mN1,mN2)
        den = self.denominator[(mN1, mN2)].Eval(mll)
        if den==0: return (1.,1.)
        
        if self.run_diagnostics:
            # record PDFs
            self.wrappedOutputTree.fillBranch(self.label+"_fpos", self.numerator_pos[(mN1, mN2)].Eval(mll))
            self.wrappedOutputTree.fillBranch(self.label+"_fneg", self.numerator_neg[(mN1, mN2)].Eval(mll))
            self.wrappedOutputTree.fillBranch(self.label+"_fPS", den)

        return (self.numerator_pos[(mN1, mN2)].Eval(mll) / den,
                self.numerator_neg[(mN1, mN2)].Eval(mll) / den)


    def analyze(self, event):
        mN1=0
        mN2=0
        # find the initial N1, N2 from the truth particles
        genParts = Collection(event, 'GenPart')
        n2_lep_vecs=[]
        for ip,p in enumerate(genParts):
            # find N1, N2
            if (not mN1 and abs(p.pdgId) == self.barcodeN1 
                and abs(p.genPartIdxMother) != self.barcodeN1):
                mN1 = int(p.mass+1e-5)
            if (not mN2 and abs(p.pdgId) == self.barcodeN2 
                and abs(p.genPartIdxMother) != self.barcodeN2):
                mN2 = int(p.mass+1e-5) 
            # find leptons
            if abs(p.pdgId) in self.lepIDs:
                if p.genPartIdxMother>=0 and abs(genParts[p.genPartIdxMother].pdgId) in self.lepIDs:
                    continue #skip leptons from leptons (incl taus) to avoid double-counting
                if p.genPartIdxMother>=0 and not (abs(genParts[p.genPartIdxMother].pdgId) in [23,self.barcodeN2]):
                    continue # require z or n2 parent (no light hadrons)
                q=p # q traverses graph to look for n2 parents
                while q.genPartIdxMother>=0:
                    q = genParts[q.genPartIdxMother]
                    if q.pdgId == self.barcodeN2:
                        n2_lep_vecs += [p.p4()]
                        break
                
        mll=-1.
        if len(n2_lep_vecs)>1:
            mll=(n2_lep_vecs[0]+n2_lep_vecs[1]).M()

        if self.run_diagnostics:
            self.wrappedOutputTree.fillBranch(self.label+"_nlep", len(n2_lep_vecs))
            self.wrappedOutputTree.fillBranch(self.label+"_mll", mll)
            self.wrappedOutputTree.fillBranch(self.label+"_mllRel", mll/(mN2-mN1))
            self.wrappedOutputTree.fillBranch(self.label+"_dm", mN2-mN1)
        wPos, wNeg = self.GetWeights(mll, mN1, mN2)
        self.wrappedOutputTree.fillBranch(self.label+"_pos", wPos)
        self.wrappedOutputTree.fillBranch(self.label+"_neg", wNeg)
        return True

