def boost_PFC(pt_top,eta_top,phi_top,M_top,pt_PFC,eta_PFC,phi_PFC,M_PFC):
    pt_old = pt_PFC
    eta_old = eta_PFC
    phi_old = phi_PFC
    mass_old = M_PFC
    
    particle_old = ROOT.TLorentzVector()
    particle_old.SetPtEtaPhiM(pt_old, eta_old, phi_old, mass_old)

    pt_new_frame = pt_top
    eta_new_frame = eta_top
    phi_new_frame = phi_top
    mass_new_frame = M_top

    new_frame = ROOT.TLorentzVector()
    new_frame.SetPtEtaPhiM(pt_new_frame, eta_new_frame, phi_new_frame, mass_new_frame)

    boost_vector = new_frame.BoostVector()


    particle_old.Boost(-boost_vector.X(), -boost_vector.Y(), -boost_vector.Z())  


    pt_new = particle_old.Pt()
    eta_new = particle_old.Eta()
    phi_new = particle_old.Phi()
    mass_new = particle_old.M()

    return pt_new, eta_new, phi_new, mass_new


def fill_PFCs(n_PFCs, PFCs_dnn, PFCs, idx_top, pt_top, eta_top, phi_top, M_top): 
    for i,particle in enumerate(PFCs):
        if i<n_PFCs: #minore e non minore e uguale perchè parte da 0
            pt_boost, eta_boost, phi_boost, mass_boost = boost_PFC(pt_top, eta_top, phi_top, M_top, particle.pt ,particle.eta, particle.phi, particle.mass)
            PFCs_dnn[idx_top, i, 0] = pt_boost
            PFCs_dnn[idx_top, i, 1] = eta_boost
            PFCs_dnn[idx_top, i, 2] = phi_boost
            PFCs_dnn[idx_top, i, 3] = mass_boost
            PFCs_dnn[idx_top, i, 4] = particle.charge
            PFCs_dnn[idx_top, i, 5] = particle.pdgId
            PFCs_dnn[idx_top, i, 6] = particle.d0
            PFCs_dnn[idx_top, i, 7] = particle.dz
            PFCs_dnn[idx_top, i, 8] = particle.pvAssocQuality  
            PFCs_dnn[idx_top, i, 9] = particle.JetDeltaR
            PFCs_dnn[idx_top, i, 10] = particle.FatJetDeltaR
            PFCs_dnn[idx_top, i, 11] = particle.IsInJet
            PFCs_dnn[idx_top, i, 12] = particle.IsInFatJet
    return PFCs_dnn

class nanoTopcand(Module):
    def __init__(self, isMC=1):
        self.isMC = isMC
        pass
    def beginJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("nTopMixed", "I")
        self.out.branch("TopMixed_idxFatJet", "I", lenVar="nTopMixed")
        self.out.branch("TopMixed_idxJet0", "I", lenVar="nTopMixed")
        self.out.branch("TopMixed_idxJet1", "I", lenVar="nTopMixed")
        self.out.branch("TopMixed_idxJet2", "I", lenVar="nTopMixed")
        self.out.branch("Indexes_idxPFC", "I", lenVar="nIndexes")
        self.out.branch("nIndexes", "I") 
        #self.out.branch("TopMixed_idxPFC_3j1fj", "I", lenVar="nTopMixed") 
        #self.out.branch("TopMixed_idxPFC_3j0fj", "I", lenVar="nTopMixed")
        #self.out.branch("TopMixed_idxPFC_2j1fj", "I", lenVar="nTopMixed")
        #self.out.branch("TopMixed_sumjetPt", "F", lenVar="nTopMixed")
        #self.out.branch("TopMixed_sumjetEta", "F", lenVar="nTopMixed")
        #self.out.branch("TopMixed_sumjetPhi", "F", lenVar="nTopMixed")
        #self.out.branch("TopMixed_sumjetMass", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_pt", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_eta", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_phi", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_mass", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_truth", "F", lenVar="nTopMixed")
        self.out.branch("TopMixed_category", "I", lenVar="nTopMixed")
       

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        #t0 = datetime.now()
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        jets        = Collection(event,"Jet")
        njets       = len(jets)
        fatjets     = Collection(event,"FatJet")
        nfatjets    = len(fatjets)
        goodjets, goodfatjets = presel(jets, fatjets)
        ngoodjets = len(goodjets)
        ngoodfatjets = len(goodfatjets)
        PFCands               = Collection(event,"PFCands")
        sorted_PFCands = sorted(PFCands, key=lambda particle: particle.pt, reverse=True)