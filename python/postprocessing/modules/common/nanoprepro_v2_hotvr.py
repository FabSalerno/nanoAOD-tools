import ROOT
import math
import numpy as np
from array import array
#from datetime import datetime
ROOT.PyConfig.IgnoreCommandLineOptions = True
#from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
#from PhysicsTools.NanoAODTools.postprocessing.skimtree_utils import *



def closest_hvr(obj, collection, presel=lambda x, y: True):
    ret = None
    jet = None
    drMin = 999
    for i, x in enumerate(collection):
        if not presel(obj, x):
            continue
        dr = deltaR(obj, x)
        if dr < drMin:
            jet = x
            ret = i
            drMin = dr
    return (jet, ret, drMin)


def matching(genpart, gen, jet, sgn_top, dR = 0.4):
    b       = sgn_top*5
    w       = sgn_top*24
    sgn_u   = sgn_top
    sgn_d   = -sgn_top
    match   = False
    jet_out = None
    dr = None

    #Matching della b proveniente da un top con un jet/fatjet
    #gen è un elemento di genpart che è il vettore contente i flavour per ogni evento (è il favour di una particella in un evento)
    if (gen.pdgId == b and gen.genPartIdxMother_prompt > -1 and genpart[gen.genPartIdxMother_prompt].pdgId == sgn_top*6):
        #se è un b prompt, ha madre e la madre è un top(antitop)
        #print('b quark cand ', gen.pdgId)
        j, dr =  closest_(gen, jet) #dà il jet più vicino 
        if dr < dR: #se la distanza è minore della larghezza del jet
            #print('found match b quark', j)
            jet_out = j
            match   = True
    # Matching di un u/c proveniente da una W proveniente dal top con un jet/fatjet      
    elif (gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId) == sgn_u and gen.genPartIdxMother_prompt > -1 and genpart[gen.genPartIdxMother_prompt].pdgId == w):
        # La W deve provenire da un top 
        if (genpart[genpart[gen.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId == sgn_top*6):
            #print('u quark cand', gen.pdgId)
            j, dr = closest_(gen, jet)
            if dr < dR:
                #print('found match up quark', j)
                jet_out = j
                match   = True
    # Matching di un d/s proveniente da una W proveniente dal top con un jet/fatjet            
    elif (gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId) == sgn_d and gen.genPartIdxMother_prompt > -1 and genpart[gen.genPartIdxMother_prompt].pdgId == w):
        # La W deve provenire da un to
        if (genpart[genpart[gen.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId == sgn_top*6):
            #print('d quark cand')
            j, dr =  closest_(gen, jet)
            if dr < dR:
                #print('found match down quark', j)
                jet_out = j
                match = True
    return match, jet_out, dr



def matching_hvr(genpart, gen, jet, sgn_top):
    b       = sgn_top*5
    w       = sgn_top*24
    sgn_u   = sgn_top
    sgn_d   = -sgn_top
    match   = False
    jet_out = None
    dr = None

    #Matching della b proveniente da un top con un jet/fatjet
    #gen è un elemento di genpart che è il vettore contente i flavour per ogni evento (è il favour di una particella in un evento)
    if (gen.pdgId == b and gen.genPartIdxMother_prompt > -1 and genpart[gen.genPartIdxMother_prompt].pdgId == sgn_top*6):
        #se è un b prompt, ha madre e la madre è un top(antitop)
        #print('b quark cand ', gen.pdgId)
        jet, j, dr =  closest_hvr(gen, jet) #dà il jet più vicino
        #print("type",type(jet),type(j),"\n") 
        #print(jet,"\n") 
        if jet!=None:
            if dr < 600/jet.pt: #se la distanza è minore della larghezza del jet
                #print('found match b quark', b ,"nel jet",j)
                jet_out = j
                match   = True
    # Matching di un u/c proveniente da una W proveniente dal top con un jet/fatjet      
    elif (gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId) == sgn_u and gen.genPartIdxMother_prompt > -1 and genpart[gen.genPartIdxMother_prompt].pdgId == w):
        # La W deve provenire da un top 
        if (genpart[genpart[gen.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId == sgn_top*6):
            #print('u quark cand', gen.pdgId)
            jet, j, dr = closest_hvr(gen, jet)
            if jet!=None:
                if dr < 600/jet.pt:
                    #print('found match up quark', sgn_u,"nel jet",j)
                    jet_out = j
                    match   = True
    # Matching di un d/s proveniente da una W proveniente dal top con un jet/fatjet            
    elif (gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId) == sgn_d and gen.genPartIdxMother_prompt > -1 and genpart[gen.genPartIdxMother_prompt].pdgId == w):
        # La W deve provenire da un top
        if (genpart[genpart[gen.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId == sgn_top*6):
            #print('d quark cand')
            jet, j, dr =  closest_hvr(gen, jet)
            if jet!=None:
                if dr < 600/jet.pt:
                    #print('found match down quark', sgn_d,"nel jet",j)
                    jet_out = j
                    match = True
    return match, jet_out, dr


    '''Matching della b proveniente da un top con un jet/fatjet
    #gen è un elemento di genpart che è il vettore contente i flavour per ogni evento (è il favour di una particella in un evento)
    if (gen.pdgId == b and gen.genPartIdxMother_prompt > -1 and genpart[gen.genPartIdxMother_prompt].pdgId == sgn_top*6):
        #se è un b prompt, ha madre e la madre è un top(antitop)
        #print('b quark cand ', gen.pdgId)
        j, dr =  closest_(gen, jet) #dà il jet più vicino 
        if dr < dR: #se la distanza è minore della larghezza del jet
            #print('found match b quark', j)
            jet_out = j
            match   = True
    # Matching di un u/c proveniente da una W proveniente dal top con un jet/fatjet      
    elif (gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId) == sgn_u and gen.genPartIdxMother_prompt > -1 and genpart[gen.genPartIdxMother_prompt].pdgId == w):
        # La W deve provenire da un top 
        if (genpart[genpart[gen.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId == sgn_top*6):
            #print('u quark cand', gen.pdgId)
            j, dr = closest_(gen, jet)
            if dr < dR:
                #print('found match up quark', j)
                jet_out = j
                match   = True
    # Matching di un d/s proveniente da una W proveniente dal top con un jet/fatjet            
    elif (gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId) == sgn_d and gen.genPartIdxMother_prompt > -1 and genpart[gen.genPartIdxMother_prompt].pdgId == w):
        # La W deve provenire da un to
        if (genpart[genpart[gen.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId == sgn_top*6):
            #print('d quark cand')
            j, dr =  closest_(gen, jet)
            if dr < dR:
                #print('found match down quark', j)
                jet_out = j
                match = True
    return match, jet_out'''




class nanoprepro(Module):
    def __init__(self, isMC=1):
        self.isMC = isMC
        pass
        
        
    def beginJob(self):
        pass
        
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        #self.out.branch("Jet_deltaR",      "F", lenVar="nJet") 
        self.out.branch("selectedJets_nominal_matched",      "F", lenVar="nJet")    # 0,1,2,3
        self.out.branch("selectedJets_nominal_pdgId",        "F", lenVar="nJet")    # quark flav 
        self.out.branch("selectedJets_nominal_topMother",    "F", lenVar="nJet")
        self.out.branch("selectedFatJets_nominal_matched",   "F", lenVar="nFatJet") # 0,1
        self.out.branch("selectedFatJets_nominal_pdgId",     "F", lenVar="nFatJet") # quark flav
        self.out.branch("selectedFatJets_nominal_topMother", "F", lenVar="nFatJet")
        self.out.branch("selectedHOTVRJets_nominal_matched",   "F", lenVar="nHVRJet") # 0,1
        self.out.branch("selectedHOTVRJets_nominal_pdgId",     "F", lenVar="nHVRJet") # quark flav
        self.out.branch("selectedHOTVRJets_nominal_topMother", "F", lenVar="nHVRJet")


    def endFile(self, inputFile, outputFile, inputTree,wrappedOutputTree):
        pass


    def analyze(self, event):
        #t0 = datetime.now()
        """process event, return True (go to next module) or False (fail, go to next event)"""        
        jets       = Collection(event,"selectedJets_nominal")
        Njets      = len(jets)
        fatjets    = Collection(event,"selectedFatJets_nominal")
        Nfatjets   = len(fatjets)
        hvrjets    = Collection(event,"selectedHOTVRJets_nominal")
        Nhvrjets   = len(hvrjets)
        muons      = Collection(event, "Muon")
        electrons  = Collection(event, "Electron")
        if self.isMC==1:
            #LHE     = Collection(event, "LHEPart")
            genpart = Collection(event, "genParticle")
        '''init variables to branch'''
        #jets_deltar = []
        #ind_fatjets = []
        #ind_jets    = []
        jets_pdgId        = np.zeros(Njets)
        jets_matched      = np.zeros(Njets)
        jets_topMother    = np.zeros(Njets)
        fatjets_pdgId     = np.zeros(Nfatjets)
        fatjets_matched   = np.zeros(Nfatjets)
        fatjets_topMother = np.zeros(Nfatjets)
        hvrjets_pdgId     = np.zeros(Nhvrjets)
        hvrjets_matched   = np.zeros(Nhvrjets)
        hvrjets_topMother = np.zeros(Nhvrjets)
        
        if self.isMC==1:
            #if (len(looseMu)>0 or len(looseEle)>0):# and met.pt>25:
            if False:#abs(LHE[1].pdgId)>6 and abs(LHE[2].pdgId)>6:
                return False
            else:
                #print flavquarks
                #print("NEW EVENT <----------------------------")
                
                ntop    = 0
                sgn_top = 0
                for gen in genpart:
                    # Trova i top nei tDM e TTbar
                    if (gen.genPartIdxMother_prompt == -1 and abs(gen.pdgId)==6):
                        if (gen.genPartIdxMother == 0):
                            ntop   += 1
                            sgn_top = gen.pdgId/abs(gen.pdgId)
                    # Trova i top nei Tprime
                    elif (gen.genPartIdxMother_prompt != -1 and abs(gen.pdgId)==6):
                        if ((gen.genPartIdxMother == 0 or abs(genpart[gen.genPartIdxMother_prompt].pdgId) == 8000001)):
                            ntop   += 1
                            sgn_top = gen.pdgId/abs(gen.pdgId)
                #print('# top ',ntop)
                #print(' top sgn ', sgn_top) sempre -1 immagino siano ordinati
                if ntop == 1:
                    uquark_matched   = False
                    dquark_matched   = False 
                    bquark_matched   = False 
                    uquarkFJ_matched = False
                    dquarkFJ_matched = False 
                    bquarkFJ_matched = False 
                    uquarkHVRJ_matched = False
                    dquarkHVRJ_matched = False 
                    bquarkHVRJ_matched = False 
                elif ntop == 2:
                    b_matched        = False
                    u_matched        = False
                    dbar_matched     = False
                    bbar_matched     = False                    
                    d_matched        = False
                    ubar_matched     = False
                    bFJ_matched      = False
                    uFJ_matched      = False
                    dbarFJ_matched   = False
                    bbarFJ_matched   = False                    
                    dFJ_matched      = False
                    ubarFJ_matched   = False
                    bHVRJ_matched      = False
                    uHVRJ_matched      = False
                    dbarHVRJ_matched   = False
                    bbarHVRJ_matched   = False                    
                    dHVRJ_matched      = False
                    ubarHVRJ_matched   = False
                    dr_FJ_matched = []
                    FJ_gen_id = []
                    dr_HVRJ_matched = []
                    HVRJ_gen_id = []
                    HVRJ_sign = []

                #Ad ogni particella collego il segno del top da cui proviene e la matcho a un jet, per i jet c'è un raporto 1-1 perchè ce ne sono molti e closest generalmente funziona
                for gen in genpart:
                    tosave = False
                    if ntop == 1:
                        match, j, dr = matching(genpart, gen, jets, sgn_top, dR=0.4)
                        #if match: print("jet matched ", match, gen.pdgId, j, sgn_top)
                    elif ntop ==2:
                        match, j, dr = matching(genpart, gen, jets, +1, dR=0.4)
                        #print('top +6 :', match, j)
                        sgn_top = 1
                        if not match:
                            match, j, dr = matching(genpart, gen, jets, -1, dR=0.4)
                            sgn_top = -1
                            #print('top -6 :', match, j)
                    else: match = False
                    
                    #print("genpart (b,u,d)", bquark_matched, uquark_matched, dquark_matched)
                    #print(match)
                    if (match and ntop == 1 and not (bquark_matched*uquark_matched*dquark_matched)):
                        #print("genpart matched (b,u,d)", bquark_matched, uquark_matched, dquark_matched)
                        if (not bquark_matched and gen.pdgId==sgn_top*5) :
                            #print('b quark matched')
                            bquark_matched = True
                            tosave = True
                        elif (not uquark_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top): 
                            #print('u quark matched')
                            uquark_matched = True
                            tosave = True
                        elif (not dquark_matched and gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top): 
                            #print('d quark matched')
                            dquark_matched = True
                            tosave = True
                        if tosave:
                            #print("saving jet #", j, gen.pdgId)
                            jets_topMother[j] = sgn_top*6
                            jets_matched[j] += 1
                            if jets_matched[j]==1: jets_pdgId[j] = abs(gen.pdgId) #unità id del primo
                            elif jets_matched[j]==2: jets_pdgId[j] += abs(gen.pdgId)*10 #decine id del secondo
                            elif jets_matched[j]==3: jets_pdgId[j] += abs(gen.pdgId)*100 #centinaia id del terzo
                            #ind_jets[j] = j

                    elif (match and ntop == 2):
                        #print  sgn_top
                        if(sgn_top == 1 and not b_matched*u_matched*dbar_matched):
                            #print "t"
                            if (not b_matched and gen.pdgId==sgn_top*5) :
                                #print "   b matched"
                                b_matched = True
                                tosave = True
                            elif (not u_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top):
                                #print "   u matched"
                                u_matched = True
                                tosave = True
                            elif (not dbar_matched and gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top):
                                #print "   dbar matched"
                                dbar_matched = True
                                tosave = True
                            if tosave :
                                #print "...saving jet pgd"
                                jets_topMother[j] = sgn_top*6
                                jets_matched[j] += 1
                                if jets_matched[j]==1: jets_pdgId[j] = abs(gen.pdgId)
                                elif jets_matched[j]==2: jets_pdgId[j] += abs(gen.pdgId)*10
                                elif jets_matched[j]==3: jets_pdgId[j] += abs(gen.pdgId)*100
                                #ind_jets[-1] = j
                        elif(sgn_top == -1 and not bbar_matched*ubar_matched*d_matched): #posso aggiungere qui bmatched
                            #print "tbar"
                            if (not bbar_matched and gen.pdgId==sgn_top*5) :
                                #print "   bbar matched"
                                bbar_matched = True
                                tosave = True
                            elif (not ubar_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top):
                                #print "   ubar matched"
                                ubar_matched = True
                                tosave = True
                            elif (not d_matched and gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top):
                                #print "   d matched"
                                d_matched = True
                                tosave = True
                            if tosave:
                                #print "...saving jet pgd"
                                jets_topMother[j] = sgn_top*6
                                jets_matched[j]  += 1
                                #print(jets_matched[j])
                                if jets_matched[j]  ==1: jets_pdgId[j] = abs(gen.pdgId) 
                                elif jets_matched[j]==2: jets_pdgId[j] += abs(gen.pdgId)*10 
                                elif jets_matched[j]==3: jets_pdgId[j] += abs(gen.pdgId)*100 
                                #ind_jets[-1] = j
    
                for gen in genpart:
                    #print(gen,"GENPART DA MATCHARE",gen.pdgId, "generato",gen.genPartIdxMother)
                    tosave = False
                    if ntop == 1:
                        match,j,dr = matching(genpart, gen, fatjets, sgn_top, dR=0.8)
                    elif ntop ==2:
                        match,j,dr = matching(genpart, gen, fatjets, sgn_top=+1, dR=0.8) #secondo me qui succede qualcosa, anche quando sgn_top=-1 matcha
                        sgn_top = 1
                        if not match:
                            match,j,dr = matching(genpart, gen, fatjets, -1, dR=0.8)
                            sgn_top = -1
                    else: match = False
                    #print("IL SEGNO DEL TOP è", sgn_top)
                    if (match and ntop ==1 and 
                        not (bquarkFJ_matched*uquarkFJ_matched*dquarkFJ_matched)):
                        
                        if (not bquarkFJ_matched and gen.pdgId==sgn_top*5) : 
                            bquarkFJ_matched = True
                            tosave = True
                        elif (not uquarkFJ_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top): 
                            uquarkFJ_matched = True
                            tosave = True
                        elif (not dquarkFJ_matched and gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top): 
                            dquarkFJ_matched = True
                            tosave = True
                        if tosave:
                            fatjets_topMother[j] = sgn_top*6
                            fatjets_matched[j] += 1
                            if fatjets_matched[j]==1: 
                                fatjets_pdgId[j] = abs(gen.pdgId) 
                                #print("fat1single",gen.pdgId)
                            elif fatjets_matched[j]==2: 
                                fatjets_pdgId[j] += abs(gen.pdgId)*10 
                                #print("fat2single",gen.pdgId)
                            elif fatjets_matched[j]==3: 
                                fatjets_pdgId[j] += abs(gen.pdgId)*100 
                                #print("fat3single",gen.pdgId)
                            elif fatjets_matched[j]==4: 
                                fatjets_pdgId[j] += abs(gen.pdgId)*1000 
                                #print("fat4single",gen.pdgId)

                    elif (match and ntop == 2):
                        #print(match)
                        if(sgn_top == 1 and not bFJ_matched*uFJ_matched*dbarFJ_matched): 
                            #print("t")
                            if (not bFJ_matched and gen.pdgId==sgn_top*5) :
                                #print ("   b matched")
                                bFJ_matched = True
                                tosave = True
                            elif (not uFJ_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top):
                                #print("   u matched")
                                uFJ_matched = True
                                tosave = True
                            elif (not dbarFJ_matched and gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top):
                                #print("   dbar matched")
                                dbarFJ_matched = True
                                tosave = True
                            if tosave :
                                #print "...saving jet pgd"
                                fatjets_topMother[j] = sgn_top*6
                                fatjets_matched[j] += 1
                                #FJ_gen_id.append(gen.pdgId)
                                #dr_FJ_matched.append(dr)
                                if fatjets_matched[j]==1: 
                                    fatjets_pdgId[j] = abs(gen.pdgId)
                                    #print("fat1top",gen.pdgId)
                                elif fatjets_matched[j]==2: 
                                    fatjets_pdgId[j] += abs(gen.pdgId)*10
                                    #print("fat2top",gen.pdgId)
                                elif fatjets_matched[j]==3: 
                                    fatjets_pdgId[j] += abs(gen.pdgId)*100
                                    #print("fat3top",gen.pdgId)
                                elif fatjets_matched[j]==4: 
                                    fatjets_pdgId[j] += abs(gen.pdgId)*1000 
                                    #print("fat4antitop",gen.pdgId,"dr",dr_FJ_matched,"gen id", FJ_gen_id)
                            
                        elif(sgn_top == -1 and not bbarFJ_matched*ubarFJ_matched*dFJ_matched):
                            #print("tbar")
                            if (not bbarFJ_matched and gen.pdgId==sgn_top*5) :
                                #print("   bbar matched")
                                bbarFJ_matched = True
                                tosave = True
                            elif (not ubarFJ_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top):
                                #print("   ubar matched")
                                ubarFJ_matched = True
                                tosave = True
                            elif (not dFJ_matched and gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top):
                                #print("   d matched")
                                dFJ_matched = True
                                tosave = True
                            if tosave:
                                #print "...saving jet pgd"
                                fatjets_topMother[j] = sgn_top*6
                                fatjets_matched[j] += 1
                                #FJ_gen_id.append(gen.pdgId)
                                #dr_FJ_matched.append(dr)
                                if fatjets_matched[j]==1: 
                                    fatjets_pdgId[j] = abs(gen.pdgId) 
                                    #print("fat1antitop",gen.pdgId)
                                elif fatjets_matched[j]==2: 
                                    fatjets_pdgId[j] += abs(gen.pdgId)*10 
                                    #print("fat2antitop",gen.pdgId)
                                elif fatjets_matched[j]==3: 
                                    fatjets_pdgId[j] += abs(gen.pdgId)*100 
                                    #print("fat3antitop",gen.pdgId)
                                elif fatjets_matched[j]==4: 
                                    fatjets_pdgId[j] += abs(gen.pdgId)*1000 
                                    #print("fat4antitop",gen.pdgId,"dr",dr_FJ_matched,"gen id", FJ_gen_id)

                    #for i1 in len(FJ_gen_id):
                        #for i2 in len(FJ_gen_id): 
                            #if 


                #hotvr
                for gen in genpart:
                    #print(gen)
                    tosave = False
                    if ntop == 1:
                        match,j,dr = matching_hvr(genpart, gen, hvrjets, sgn_top)
                    elif ntop ==2:
                        match,j,dr = matching_hvr(genpart, gen, hvrjets, +1)
                        sgn_top = 1
                        if not match:
                            match,j,dr = matching_hvr(genpart, gen, hvrjets, -1)
                            sgn_top = -1
                    else: match = False
                    #if match:
                        #print("Ho trovato top",match,sgn_top)
                    if (match and ntop ==1 and 
                        not (bquarkHVRJ_matched*uquarkHVRJ_matched*dquarkHVRJ_matched)):
                        
                        if (not bquarkHVRJ_matched and gen.pdgId==sgn_top*5) : 
                            bquarkHVRJ_matched = True
                            tosave = True
                        elif (not uquarkHVRJ_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top): 
                            uquarkHVRJ_matched = True
                            tosave = True
                        elif (not dquarkHVRJ_matched and gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top): 
                            dquarkHVRJ_matched = True
                            tosave = True
                        if tosave:
                            hvrjets_topMother[j] = sgn_top*6
                            hvrjets_matched[j] += 1
                            HVRJ_sign.append(sgn_top)
                            HVRJ_gen_id.append(gen.pdgId)
                            dr_HVRJ_matched.append(dr)
                            if hvrjets_matched[j]==1: hvrjets_pdgId[j] = abs(gen.pdgId)
                            elif hvrjets_matched[j]==2: hvrjets_pdgId[j] += abs(gen.pdgId)*10
                            elif hvrjets_matched[j]==3: hvrjets_pdgId[j] += abs(gen.pdgId)*100
                            elif hvrjets_matched[j]==4: hvrjets_pdgId[j] += abs(gen.pdgId)*1000
                            elif hvrjets_matched[j]==5: hvrjets_pdgId[j] += abs(gen.pdgId)*10000
                            elif hvrjets_matched[j]==6: 
                                    hvrjets_matched[j]==0 


                    elif (match and ntop == 2):
                        #print(ntop,sgn_top)
                        if(sgn_top == 1 and not bHVRJ_matched*uHVRJ_matched*dbarHVRJ_matched):
                            #print("t")
                            if (not bHVRJ_matched and gen.pdgId==sgn_top*5) :
                                #print("   b matched")
                                bHVRJ_matched = True
                                tosave = True
                            elif (not uHVRJ_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top):
                                #print("   u matched")
                                uHVRJ_matched = True
                                tosave = True
                            elif (not dbarHVRJ_matched and gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top):
                                #print("   dbar matched")
                                dbarHVRJ_matched = True
                                tosave = True
                            if tosave :
                                #print "...saving jet pgd"
                                hvrjets_topMother[j] = sgn_top*6
                                hvrjets_matched[j] += 1
                                HVRJ_sign.append(sgn_top)
                                HVRJ_gen_id.append(gen.pdgId)
                                dr_HVRJ_matched.append(dr)
                                if hvrjets_matched[j]==1: hvrjets_pdgId[j] = abs(gen.pdgId)
                                elif hvrjets_matched[j]==2: hvrjets_pdgId[j] += abs(gen.pdgId)*10
                                elif hvrjets_matched[j]==3: hvrjets_pdgId[j] += abs(gen.pdgId)*100
                                elif hvrjets_matched[j]==4: hvrjets_pdgId[j] += abs(gen.pdgId)*1000
                                elif hvrjets_matched[j]==5: hvrjets_pdgId[j] += abs(gen.pdgId)*10000
                                elif hvrjets_matched[j]==6: 
                                    hvrjets_matched[j]==0 #Se li prende tutti per ora non lo considero matched
                            
                        elif(sgn_top == -1 and not bbarHVRJ_matched*ubarHVRJ_matched*dHVRJ_matched):
                            #print("tbar")
                            if (not bbarHVRJ_matched and gen.pdgId==sgn_top*5) :
                                #print ("   bbar matched")
                                bbarHVRJ_matched = True
                                tosave = True
                            elif (not ubarHVRJ_matched and gen.pdgId%2 == 0 and gen.pdgId/abs(gen.pdgId)==sgn_top):
                                #print("   ubar matched")
                                ubarHVRJ_matched = True
                                tosave = True
                            elif (not dHVRJ_matched and gen.pdgId%2 != 0 and gen.pdgId/abs(gen.pdgId)==(-1)*sgn_top):
                                #print("   d matched")
                                dHVRJ_matched = True
                                tosave = True
                            if tosave:
                                #print "...saving jet pgd"
                                hvrjets_topMother[j] = sgn_top*6
                                hvrjets_matched[j] += 1
                                HVRJ_sign.append(sgn_top)
                                HVRJ_gen_id.append(gen.pdgId)
                                dr_HVRJ_matched.append(dr)
                                if hvrjets_matched[j]==1: hvrjets_pdgId[j] = abs(gen.pdgId)
                                elif hvrjets_matched[j]==2: hvrjets_pdgId[j] += abs(gen.pdgId)*10
                                elif hvrjets_matched[j]==3: hvrjets_pdgId[j] += abs(gen.pdgId)*100
                                elif hvrjets_matched[j]==4: hvrjets_pdgId[j] += abs(gen.pdgId)*1000
                                elif hvrjets_matched[j]==5: hvrjets_pdgId[j] += abs(gen.pdgId)*10000
                                elif hvrjets_matched[j]==6: 
                                    hvrjets_matched[j]==0

                    if match>0: #si può usare un criterio simile 
                        sgn_top = max(HVRJ_sign, key=lambda x:HVRJ_sign.count(x))
                        hvrjets_topMother[j]=sgn_top*6
                        #HVRJ_gen_id[HVRJ_sign.index(-sgn_top)]
                        #print("matched hvr",hvrjets_matched,"pdgid", hvrjets_pdgId,"topmother",hvrjets_topMother,"vector sign",HVRJ_sign)
                
                #self.out.fillBranch("Jet_deltaR", jets_deltar)
                #print(jets_topMother)
                self.out.fillBranch("selectedJets_nominal_matched", jets_matched)
                self.out.fillBranch("selectedJets_nominal_pdgId", jets_pdgId)
                self.out.fillBranch("selectedJets_nominal_topMother", jets_topMother)
                
                self.out.fillBranch("selectedFatJets_nominal_matched", fatjets_matched)
                self.out.fillBranch("selectedFatJets_nominal_pdgId", fatjets_pdgId)
                self.out.fillBranch("selectedFatJets_nominal_topMother", fatjets_topMother)

                self.out.fillBranch("selectedHOTVRJets_nominal_matched", hvrjets_matched)
                self.out.fillBranch("selectedHOTVRJets_nominal_pdgId", hvrjets_pdgId)
                self.out.fillBranch("selectedHOTVRJets_nominal_topMother", hvrjets_topMother)

                #self.out.fillBranch("Top_indFatJet", ind_fatjets) 
                #self.out.fillBranch("Top_indJet", ind_jets) 
                # t1 = datetime.now()
                # print("nanprepro module time :", t1-t0) 
                return True
