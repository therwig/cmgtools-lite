#!/usr/bin/env python
import sys
import re
import os
import argparse

helpText = "LEP = '2los', '3los'\n\
REG = 'sr', 'sr_col', 'cr_dy', 'cr_tt', 'cr_vv', 'cr_ss', 'cr_wz', 'appl', 'appl_col'\n\
BIN = 'min', 'low', 'med', 'high'"
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                 epilog=helpText)
parser.add_argument("outDir", help="Choose the output directory.\nOutput will be saved to 'outDir/year/LEP_REG_BIN'")
parser.add_argument("year", help="Choose the year: '2016', '2017' or '2018'")
parser.add_argument("--lep", default=None, required=True, help="Choose number of leptons to use (REQUIRED)")
parser.add_argument("--reg", default=None, required=True, help="Choose region to use (REQUIRED)")
parser.add_argument("--bin", default=None, required=True, help="Choose bin to use (REQUIRED)")
parser.add_argument("--signal", action="store_true", default=False, help="Include signal")
parser.add_argument("--data", action="store_true", default=False, help="Include data")
parser.add_argument("--norm", action="store_true", default=False, help="Normalize signal to data")
parser.add_argument("--unc", action="store_true", default=False, help="Include uncertainties")
parser.add_argument("--inPlots", default=None, help="Select plots, separated by commas, no spaces")
parser.add_argument("--exPlots", default=None, help="Exclude plots, separated by commas, no spaces")
parser.add_argument("--signalMasses", default=None, help="Select only these signal samples (e.g 'signal_TChiWZ_100_70+'), comma separated. Use only when doing 'cards'")
parser.add_argument("--doWhat", default="plots", help="Do 'plots' or 'cards'. Default = '%(default)s'")
args = parser.parse_args()

ODIR=args.outDir
YEAR=args.year
conf="%s_%s_%s"%(args.lep,args.reg,args.bin)

if YEAR not in ("2016","2017","2018"): raise RuntimeError("Unknown year: Please choose '2016', '2017' or '2018'")
if args.lep not in ["2los","3l"]: raise RuntimeError("Unknown choice for LEP option. Please check help" )
if args.reg not in ["sr", "sr_col", "cr_dy", "cr_tt", "cr_vv", "cr_ss", "cr_wz", "appl", "appl_col"]: raise RuntimeError("Unknown choice for REG option. Please check help." )
if args.bin not in ["min", "low", "med", "high"]: raise RuntimeError("Unknown choice for BIN option. Please check help." )
if args.doWhat not in ["plots", "cards"]: raise RuntimeError("Unknown choice for DOWHAT option. Please check help." ) # More options to be added
if args.signalMasses and args.doWhat != "cards": print "Option SIGNALMASSES to be used only with the 'cards' option. Ignoring it...\n"

lumis = {
'2016': '35.9', # '33.2' for low MET
'2017': '41.5', # '36.7' for low MET
'2018': '59.7', # '59.2' for low MET
}
LUMI= " -l %s "%(lumis[YEAR])


submit = '{command}' 
#args.doWhat = "dumps" 
#args.doWhat = "yields" 
#args.doWhat = "ntuple"

P0="/eos/cms/store/cmst3/group/tthlep/peruzzi/NanoTrees_SOS_230819_v5/"
nCores = 8
TREESALL = " --Fs {P}/recleaner --FMCs {P}/bTagWeights -P "+P0+"%s "%(YEAR,)

def base(selection):
    CORE=TREESALL
    CORE+=" -f -j %d --split-factor=-1 --year %s --s2v -L susy-sos/functionsSOS.cc -L susy-sos/functionsSF.cc --tree NanoAOD --mcc susy-sos/mcc_sos.txt --mcc susy-sos/mcc_triggerdefs.txt "%(nCores,YEAR) # --neg"
    if YEAR == "2017": CORE += " --mcc susy-sos/mcc_METFixEE2017.txt "
    RATIO= " --maxRatioRange 0.0  1.99 --ratioYNDiv 505 "
    RATIO2=" --showRatio --attachRatioPanel --fixRatioRange "
    LEGEND=" --legendColumns 2 --legendWidth 0.25 "
    LEGEND2=" --legendFontSize 0.042 "
    SPAM=" --noCms --topSpamSize 1.1 --lspam '#scale[1.1]{#bf{CMS}} #scale[0.9]{#it{Preliminary}}' "
    if args.doWhat == "plots": 
        CORE+=LUMI+RATIO+RATIO2+LEGEND+LEGEND2+SPAM+" --showMCError "
        if args.signal: CORE+=" --noStackSig --showIndivSigs "
        else: CORE+=" --xp signal.* "

    wBG = " '1.0' "
    #wFS = " '1.0' "
    if selection=='2los':
         GO="%s susy-sos/mca/mca-2los-%s.txt susy-sos/2los_cuts.txt "%(CORE, YEAR)
         if args.doWhat in ["plots","ntuple"]: GO+=" susy-sos/2los_plots.txt "
         if args.doWhat in ["cards"]: GO+="  m2l [4,10,20,30,50] "
         

         if YEAR == "2016":
             wBG = " 'puWeight*eventBTagSF' " #" 'getLepSF_16(LepGood1_pt, LepGood1_eta, LepGood1_pdgId)*getLepSF_16(LepGood2_pt, LepGood2_eta, LepGood2_pdgId)*triggerSFfullsim(LepGood1_pt, LepGood1_eta, LepGood2_pt, LepGood2_eta, MET_pt, metmm_pt(LepGood1_pdgId, LepGood1_pt, LepGood1_phi, LepGood2_pdgId, LepGood2_pt,LepGood2_phi, MET_pt, MET_phi))' "
             #wFS = " 'getLepSFFS(LepGood1_pt, LepGood1_eta, LepGood1_pdgId)*getLepSFFS(LepGood2_pt, LepGood2_eta, LepGood2_pdgId)*ISREwkCor*bTagWeightFS*triggerEff(LepGood1_pt, LepGood1_eta, LepGood2_pt,LepGood2_eta, MET_pt, metmm_pt(LepGood1_pdgId, LepGood1_pt, LepGood1_phi, LepGood2_pdgId, LepGood2_pt, LepGood2_phi, MET_pt, MET_phi))' "
         elif YEAR == "2017": 
             wBG = " 'puWeight*eventBTagSF' " #" 'getLepSF_17(LepGood1_pt, LepGood1_eta, LepGood1_pdgId)*getLepSF_17(LepGood2_pt, LepGood2_eta, LepGood2_pdgId)' "
         elif YEAR == "2018":
             wBG = " 'puWeight*eventBTagSF' "
         GO="%s -W %s"%(GO,wBG)

         if args.doWhat == "plots": GO=GO.replace(LEGEND, " --legendColumns 3 --legendWidth 0.52 ")
         if args.doWhat == "plots": GO=GO.replace(RATIO,  " --maxRatioRange 0.6  1.99 --ratioYNDiv 210 ")
         if args.doWhat == "cards":         
             GO += " --binname %s "%args.bin
         else:
             GO += " --binname 2los "

 
    elif selection=='3l':
        GO="%s susy-sos/mca/mca-3l-%s.txt susy-sos/3l_cuts.txt "%(CORE,YEAR)
        if args.doWhat in ["plots","ntuple"]: GO+=" susy-sos/3l_plots.txt "
        
        if YEAR == "2016":
            wBG = " 'puWeight*eventBTagSF' " #" 'getLepSF_16(LepGood1_pt, LepGood1_eta, LepGood1_pdgId)*getLepSF_16(LepGood2_pt, LepGood2_eta, LepGood2_pdgId)*getLepSF_16(LepGood3_pt, LepGood3_eta, LepGood3_pdgId)*triggerSFfullsim3L(LepGood1_pt, LepGood1_eta, LepGood2_pt, LepGood2_eta, LepGood3_pt, LepGood3_eta, MET_pt, metmmm_pt(LepGood1_pt, LepGood1_phi, LepGood2_pt, LepGood2_phi, LepGood3_pt, LepGood3_phi, MET_pt, MET_phi, lepton_Id_selection(LepGood1_pdgId, LepGood2_pdgId, LepGood3_pdgId)), lepton_permut(LepGood1_pdgId, LepGood2_pdgId, LepGood3_pdgId))' "
            #wFS = " 'getLepSFFS(LepGood1_pt, LepGood1_eta, LepGood1_pdgId) * getLepSFFS(LepGood2_pt, LepGood2_eta, LepGood2_pdgId) * getLepSFFS(LepGood3_pt, LepGood3_eta, LepGood3_pdgId)*ISREwkCor*bTagWeightFS * triggerEff3L(LepGood1_pt, LepGood1_eta, LepGood2_pt, LepGood2_eta, LepGood3_pt, LepGood3_eta, MET_pt, metmmm_pt(LepGood1_pt, LepGood1_phi, LepGood2_pt, LepGood2_phi, LepGood3_pt, LepGood3_phi, MET_pt, MET_phi, lepton_Id_selection(LepGood1_pdgId, LepGood2_pdgId, LepGood3_pdgId)), lepton_permut(LepGood3_pdgId, LepGood3_pdgId, LepGood3_pdgId))' "
        elif YEAR == "2017":
            wBG = " 'puWeight*eventBTagSF' " #" 'getLepSF_17(LepGood1_pt, LepGood1_eta, LepGood1_pdgId)*getLepSF_17(LepGood2_pt, LepGood2_eta, LepGood2_pdgId)*getLepSF_17(LepGood3_pt, LepGood3_eta, LepGood3_pdgId)' "
        elif YEAR == "2018":
             wBG = " 'puWeight*eventBTagSF' "
        GO="%s -W %s"%(GO,wBG)

        if args.doWhat == "plots": GO=GO.replace(LEGEND, " --legendColumns 3 --legendWidth 0.42 ")
        if args.doWhat == "cards":         
            GO += " --binname %s "%args.bin
        else:
            GO += " --binname 3l "

    else:
        raise RuntimeError('Unknown selection')

    return GO

def promptsub(x):
    procs = [ '' ]
    if args.doWhat == "cards": procs += ['_FRe_norm_Up','_FRe_norm_Dn','_FRe_pt_Up','_FRe_pt_Dn','_FRe_be_Up','_FRe_be_Dn','_FRm_norm_Up','_FRm_norm_Dn','_FRm_pt_Up','_FRm_pt_Dn','_FRm_be_Up','_FRm_be_Dn']
    return x + ' '.join(["--plotgroup data_fakes%s+='.*_promptsub%s'"%(x,x) for x in procs])+" --neglist '.*_promptsub.*' "

def procs(GO,mylist):
    return GO+' '+" ".join([ '-p %s'%l for l in mylist ])

def sigprocs(GO,mylist):
    return procs(GO,mylist)+' --showIndivSigs --noStackSig'

def runIt(GO,name):
    if args.data: name=name+"_data"
    if args.norm: name=name+"_norm"
    if args.unc: name=name+"_unc"
    print name+"\n"
    if args.doWhat == "plots":  print submit.format(command=' '.join(['python mcPlots.py',"--pdir %s/%s/%s"%(ODIR,YEAR,name),GO,' '.join(['--sP %s'%p for p in (args.inPlots.split(",") if args.inPlots is not None else []) ]),' '.join(['--xP %s'%p for p in (args.exPlots.split(",") if args.exPlots is not None else []) ])]))

    if args.doWhat == "cards":  print submit.format(command=' '.join(['python makeShapeCardsNew.py --savefile',"--outdir %s/%s/%s"%(ODIR,YEAR,name),GO,' '.join(['--sP %s'%p for p in (args.inPlots.split(",") if args.inPlots is not None else []) ]),' '.join(['--xP %s'%p for p in (args.exPlots.split(",") if args.exPlots is not None else []) ]), "--xp='signal(?!.*%s).*'"%args.signalMasses.strip('signal') if args.signalMasses is not None else ''   ]))


    # What is supposed to be included in sys.argv[4] and after?
    #elif args.doWhat == "yields": print 'echo %s; python mcAnalysis.py'%name,GO,' '.join(sys.argv[4:])
    #elif args.doWhat == "dumps":  print 'echo %s; python mcDump.py'%name,GO,' '.join(sys.argv[4:])
    #elif args.doWhat == "ntuple": print 'echo %s; python mcNtuple.py'%name,GO,' '.join(sys.argv[4:])

def add(GO,opt):
    return '%s %s'%(GO,opt)

def setwide(x):
    x2 = add(x,'--wide')
    x2 = x2.replace('--legendWidth 0.35','--legendWidth 0.20')
    return x2

def binYearChoice(x,torun,YEAR):
    metBin = ''
    x2 = add(x,'-E ^eventFilters_'+YEAR[-2:]+'$ ')
    if '_min' in torun:
        metBin = 'met75'
    elif '_low' in torun:
        metBin = 'met125'
    elif '_med' in torun:
        metBin = 'met200'
        x2 = add(x2,'-X ^mm$ ')
    elif '_high' in torun:
        metBin = 'met250'
        x2 = add(x2,'-X ^mm$ ')
    if metBin != '': x2 = add(x2,'-E ^'+metBin+'$ -E ^'+metBin+'_trig_'+YEAR[-2:]+'$ ')
    else: print "\n--- NO TRIGGER APPLIED! ---\n"
    return x2

allow_unblinding = False


if __name__ == '__main__':

    torun = conf

    if (not args.doWhat=="cards" ) and ((not allow_unblinding) and args.data and (not any([re.match(x.strip()+'$',torun) for x in ['.*appl.*','.*cr.*','3l.*_Zpeak.*']]))): raise RuntimeError, 'You are trying to unblind!'


    if '2los_' in torun:
        x = base('2los')
        x = binYearChoice(x,torun,YEAR)
    
        if 'sr' in torun:
            if '_col' in torun:
                x = add(x,"-X ^mT$ -X ^SF$ ")
                if '_med' in torun: 
                     x = add(x,"-X ^pt5sublep$ ")
                     x = x.replace('-E ^met200$','-E ^met200_col$')
                if '_high' in torun: 
                     x = add(x,"-X ^pt5sublep$ ")
                     x = x.replace('-E ^met250$','-E ^met300_col$')

        if 'appl' in torun:
            if '_col' in torun:
                x = add(x,"-X ^mT$ -X ^SF$ ")
                if '_med' in torun: 
                    x = add(x,"-X ^pt5sublep$ ")
                    x = x.replace('-E ^met200$','-E ^met200_col$')
                if '_high' in torun: 
                    x = add(x,"-X ^pt5sublep$ ")
                    x = x.replace('-E ^met250$','-E ^met300_col$')
            x = add(x,"-X ^twoTight$ ")
            x = add(x,"-E ^oneNotTight$ ")

        if 'cr' in torun:
            x = add(x, "-X ^SF$ ")

        if 'cr_dy' in torun:
            if '_med' in torun: x = x.replace('-E ^met200$','-E ^met200_CR$')
            x = add(x,"-X ^ledlepPt$ -X ^twoTight$ ")
            x = add(x,"-I ^mtautau$ ")
            x = add(x,"-E ^CRDYlepId$ -E ^CRDYledlepPt$ ")

        if 'cr_tt' in torun:
            if '_med' in torun:
                x = x.replace('-E ^met200$','-E ^met200_CR$')
                x = add(x,'-X ^pt5sublep$ ')
            x = add(x,"-X ^ledlepPt$ -X ^twoTight$ -X ^bveto$ -X ^mT$ ")
            x = add(x,"-E ^CRTTlepId$ -E ^CRTTledlepPt$ -E ^btag$ ")

        if 'cr_vv' in torun:
            if '_med' in torun:
                x = x.replace('-E ^met200$','-E ^met200_CR$')
                x = add(x,'-X ^pt5sublep$ ')
            x = add(x,"-X ^ledlepPt$ -X ^twoTight$ -X ^mT$ ")
            x = add(x,"-E ^CRVVlepId$ -E ^CRVVleplepPt$ -E ^CRVVmT$ ")

        if 'cr_ss' in torun:
            if '_med' in torun:
                x = x.replace('-E ^met200$','-E ^met200_CR$')
                x = add(x,'-X ^pt5sublep$ ')
            x = add(x,"-X ^mT$ ")
            x = add(x,"-I ^OS$ ")

    elif '3l_' in torun:
        x = base('3l')
        x = binYearChoice(x,torun,YEAR)
    
        if 'appl' in torun:
            x = add(x,"-X ^threeTight$ ")
            x = add(x,"-E ^oneNotTight$ ")

        if 'cr_wz' in torun:
            x = add(x,"-X ^minMll$ -X ^ZvetoTrigger$ -X ^ledlepPt$ -X ^threeTight$ -X ^pt5sublep$ ")
            x = add(x,"-E ^CRWZlepId$ -E ^CRWZmll$ ")
            x = x.replace('-E ^met200$','-E ^met200_CR$')
            if '_min' in torun: 
                x = add(x,"-E ^CRWZPtLep_MuMu$ ")
                x = x.replace('-E ^met75_trig','-E ^met75_trig_CR')
            if '_low' in torun: 
                x = add(x,"-E ^CRWZPtLep_MuMu$ ")
                x = x.replace('-E ^met125_trig','-E ^met125_trig_CR')
            if '_med' in torun: x = add(x,"-E ^CRWZPtLep_HighMET$ ")


    if not args.data: x = add(x,'--xp data ')
    if args.unc: x = add(x,"--unc susy-sos/systsUnc.txt")
    if args.norm: x = add(x,"--sp '.*' --scaleSigToData ")

    if '_low' in torun :
        if YEAR=="2016" and "cr_wz" not in torun: x = x.replace(LUMI," -l 33.2 ")
        if YEAR=="2017": x = x.replace(LUMI," -l 36.7 ")
        if YEAR=="2018" and "cr_wz" not in torun: x = x.replace(LUMI," -l 59.2 ")

    if args.doWhat == "cards" and args.signalMasses:
        masses=args.signalMasses.rstrip('+').split('_')
        masses='_'.join(masses[-2:])
        torun=torun+'_'+masses
    runIt(x,'%s'%torun)

######################################################################################
# Useful options for plotting, to be used when needed
#
#        if '_appl' in torun: x = add(x,'-I ^TT ')
#        if '_1fo' in torun:
#            x = add(x,"-A alwaystrue 1FO 'LepGood1_isLepTight+LepGood2_isLepTight==1'")
#        if '_2fo' in torun: x = add(x,"-A alwaystrue 2FO 'LepGood1_isLepTight+LepGood2_isLepTight==0'")
#        if '_relax' in torun: x = add(x,'-X ^TT ')
#        if '_extr' in torun:
#            x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-sigextr.txt').replace('--showRatio --maxRatioRange 0 2','--showRatio --maxRatioRange 0 1 --ratioYLabel "S/B"')
#        if '_data' not in torun: x = add(x,'--xp data ')
#        if '_table' in torun:
#            x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-table.txt')
#        if '_frdata' in torun: # Why?
#            x = promptsub(x)
#            if '_blinddata' in torun:
#                x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata.txt')
#                x = add(x,'--xp data ')
#            elif not '_data' in torun: raise RuntimeError
#            x = x.replace('mca-2lss-mcdata.txt','mca-2lss-mcdata-frdata.txt')
#            if '_table' in torun:
#                x = x.replace('mca-2lss-mcdata-frdata.txt','mca-2lss-mcdata-frdata-table.txt')
###
#            if '_leadmupt25' in torun: x = add(x,"-A 'entry point' leadmupt25 'abs(LepGood1_pdgId)==13 && LepGood1_pt>25' ")
#            if '_highMetNoBCut' in torun: x = add(x,"-A 'entry point' highMET 'met_pt>60'")
#            else: x = add(x,"-E ^1B ")
