import wikiscrape, time, spacy
import termtagging as tt

# DICTIONARIES AND THESAURUS' OF RELATED TERMS
biofluids = ["Plasma","Serum","Blood","Amniotic Fluid","Ascites","Bile","Breast Milk","Colostrum","Bronchoalveolar Lavage Fluid","Cerebrospinal Fluid","Aqueous Humor","Vitreous Humor","Feces","Fecal water","Paracentesis","Pericardial Fluid","Peritoneal","Interstitial","Lymph","Pleural","Saliva","Semen","Seminal Fluid","Synovial Fluid","Tear","Lacrimal Fluid","Thoracentesis","Urine"]
colors = ["Clear","Opaque","Translucent","Transparent","White","Off-White","Light Brown","Brown","Dark Brown","Black","Grey","Light Grey","Dark Grey","Turquoise","Red","Light red","Dark red","Scarlet","Yellow","Light yellow","Dark yellow","Magenta","Cyan","Blue","Light blue","Dark blue","Orange","Light orange","Dark orange","Green","Light green","Dark green","Violet","Light violet","Dark violet","Purple","Light purple","Dark purple","Pink","Light pink","Dark pink","Flesh","Gold","Silver","Bronze","Copper"]
states_and_textures = ['Solid','Liquid','Gas','Oil','Powder','Crystalline','Crystals','Gel','Gel-like','Amorphous','Fibrous','Fibre','Gummy','Sludge','Clay','Clay-like','Suspension','Soft','Hard','Fine','Coarse','Smooth','Rough','Velvety','Viscous','Watery','Sand','Sand-like']
tastes = ["Sour","sourness","Sweet","sweetness","Bitter","bitterness","Salty","saltiness","Pungent","acrid","Astringent","Unami","uminaminess","savory","Spicy","spiciness","piquance","Coolness","minty","mintiness"]
health_effects = ['high','low','pressure','diagnose','decrease','increase','pathway','Analgesic','pain relief','pain suppressant','Anesthetic','anesthetics','Angiogenic','angiogenics','Anti-aggregant','antiaggregant','antiaggregants','Anti-aging','antiaging','Anti-allergenic','antiallergenic','antihistamine','antihistamines','Anti-allergic','antiallergic','Anti-Alzheimer’s','antialzheimers','Anti-allodynic','antiallodynic','Anti-amyloid','antiamyloid','Anti-anemic','antianemic','antianemics','Anti-angiogenic','antiangiogenic','antiangiogenics','Anti-apoptotic','antiapoptotic','Anti-arthritic','antiarthritic','antiarthritics','Anti-atheroslcerotic','antiatherosclerotic','antiathersclerotics','Anti-bleeding','antibleeding','Anti-cancer ','anticancer','anticancers','Anti-coagulant','anticoagulant','anticoagulants','Anti-cold','anticold','Anti-convulsant','anticonvulsant','anticonvulsants','Anti-depressant','antidepressant','anti-depressants','Anti-diabetic ','antidiabetic','antidiabetics','Anti-diarrheal','antidiarrheal','antidiarrheals','Anti-diuretic','antidiuretic','antidiuretics','Anti-emetic','antiemetic','antiemetics','Anti-epileptic','antiepileptic','antiepileptics','Anti-fatiguing','antifatiguing','Anti-flu','antiflu','Anti-fungal','antifungals','antifungal','Anti-glycemic','antiglycemic','antiglycemics','Anti-glycolytic','antiglycolytic','antiglycolytics','Anti-gout','antigout','Anti-helmintic','antihelmintic','antihelmintics','Anti-hemorrhagic','antihemorrhagic','antihemorrhagics','Anti-histamine','antihistamine','antihistamines','Anti-hyperalgesic','antihyperalgesic','antiphyperalgesics','Anti-hypertensive','antihypertensive','antihypertensives','Anti-hypertrophic','antihypertrophic','antihypertrophics','Anti-infective','antiinfective','antiinfectives','Anti-inflammatory','antiinflammatory','antiinflammatories','Anti-ischemic','antiischemic','Anti-lipolytic','antilipolytic','antilipolytics','Anti-microbial','antimicrobial','Anti-mutagen','antimutagen','antimutagens','Anti-mycotic','antimycotic','antimycotics','Anti-myogenic','antimyogenic','antimyogenics','Anti-nauseant','antinauseant','antinauseants','Anti-neoplastic','antineoplastic','antineoplastics','Anti-neuralgic','antineuralgic','antineuralgics','Anti-nociceptive','antinociceptive','antinociceptives','Anti-obesity','antiobesity','Anti-oxidant','antioxidant','antioxidants','Anti-Parkinson’s','antiparkinsons','Anti-platelet','antiplatelet','antiplatelets','Anti-proliferative','antiproliferative','antiproliferatives','Anti-pruritic','antipruritic','antipruritics','Anti-psoratic','antipsoratic','antipsoratics','Anti-pyretic','antipyretic','Anti-rheumatic','antirheumatic','antirheumatics','Anti-scurvy','antiscurvy','Anti-spectic','antiseptic','antiseptics','Anti-thrombolytic','antithrombolytics','Anti-thrombotic','antithrombotic','antithrombotics','Anti-toxic','antitoxic','antitoxics','Anti-tumor','antitumor','Anti-viral','antiviral','antivirals','Anti-wrinkle','antiwrinkle','Antibiotic','antibiotics','antibacterial','Antilipogenic','Apoptotic','apoptotics','Appetite stimulant','appetite stimulants','Appetite suppressant','appetite suppressants','B-cell activator','B-cell activators','Beta-oxidant ','beta-oxidation','beta-oxidants','Bone protectant','Buffer','buffers','Cardioprotectant','cardioprotectants','Cardioprotective','cardioprotectives','Cardiostimulant','cardiostimulants','Catabolic','cachectic','cachexic','Chemoprotective','chemoprotectives','Cholesterol lowering','cholesterol reducing','CNS stimulant','CNS stimulants','stimulant','Coagulant','coagulants','coagulator','Cofactor','cofactors','Constipant','constipator','Depressant','depressants','Diuretic','diuretics','Egrogenic','ergogenics','increases energy','Emetic','emetics','Enhances BBB','maintains BBB','Enzyme cofactor','enzyme cofactors','Excitant','excitatory','Glycemic','Glycolytic','glycolytics','Hallucinogen','hallucinogenic','hallucinogens','Hepatogenic','Hepatoprotective','hepatoprotectives','Hormone','hormones','Hormone precursor','hormone precursors','Hyoplipidemic','hypolipidemics','Hypocholesterolemic','hypocholesterolemics','Iatrogenic','Iatrogen','Immunomodulator','Immunomodulators','Immunostimulant','immunostimulants','Immunosuppressant','Immunosuppressants','Improves gut function','Improves bone strength','Improves heart function','Improves heart health','Improves intestinal function','Improves kidney function','Improves liver function','Improves lung function','Improves mitochondrial function','Improves muscle function','Improves muscle strength','Improves pancreatic function','Insulin sensitizer','Insulin sensitizers','Laxative','laxatives','Lifespan enhancer','increases lifespan','longevity','Lipid lowering','lipid reducing','Lipogenic','Lipolytic','lipolytics','Memory enhancer','memory enhancers','Metal chelator','metal chelators','Mineralizer','mineralizers','Mood enhancer','mood enhancers','Mood stabilizer','mood stabilizers','Muscle building','anabolic','anabolics','myogenic','Neurogenic','Neuromodulator','neuromodulators','Neuroprotectant','Neuroprotective','neruoprotectants','Neuroprotective','neuroprotectives','Neurostimulant','neurostimulants','Neurotransmitter','neurotransmitters','Nociceptive','nociceptives','Nootropic','nootropics','Osmolyte','osmolytes','Oxidant','oxidants','Prebiotic','prebiotics','Pro-oxidant','prooxidant','prooxidants','Pro-nociceptive','pronociceptive','Protects brain','brain protectant','Protects eyes','eye protectant','Protects heart','heart protectant','Protects kidney','kidney protectant','Protects liver','liver protectant','Protects lungs','lung protectant','Protects prostate','prostate protectant','Protects skin','skin protectant','Prothrombotic','Prothrombotics','Radical scavenger','radical scavengers','Redox agent','redox control','Relaxant','relaxants','Sedative','sedatives','Sexual stimulant','sexual stimulants','Signalling','signal inhibitor','signal activator','Skin softener','Stabilizes cell membrane','Stabilizes mitocondria','Stabilizes neurons','Stroidogenic','T-cell activator','T-cell activators','Thermogenic','Thrombolytic','thrombolytics','Tissue repair','wound repair','tissue maintenance','Triglyceride lowering','triglyceride reducing','Vasoconstrictor','vasoconstrictors','Vasodilator','vasodilators','Vasoprotective','vasoprotectives','Vitamin','vitamins','Waste product','waste products']
food_function = ['Flavor enhancer','flavour enhancer','flavor enhancers','flavour enhancers','Food preservative','preservative','preservatives','Aroma enhancer','perfumerant','aromatic','Flavor sharpener','flavour sharpener','Flavorant','flavourant','flavorants','Acidity regulator','acidity regulators','Antifoaming agent','antifoaming agents','anti-foaming agent','Anticaking agent','anticaking agents','anti-caking agent','Bulking agent','bulking agents','Antioxidant','antioxidants','antioxidant','Food coloring','coloring agent','coloring agents','colouring agent','Color retention agent','color stabilizing agent','Emulsifier', 'emulsifiers','Humectant', 'humectants','Glazing agent', 'glazing agents','Stabilizer', 'stabilizers','Thickener', 'thickeners','Sweetener', 'sweeteners','Dietary supplement','dietary supplements','Essential mineral','essential minerals','Essential vitamin','essential vitamins','Essential nutrient','essential nutrients']
relationships = ['regulates','precursor','potent','converts','regulation','enzyme','converted','synthsized','intermediate','is a','is found in','Activator','Activators','Activates','Activity','adduct','adducts','affinities','affinity','Agonist','Agonists','Agonizes','allosteric','allostery','Antagonist','Antagonists','Antagonize','Antagonizes','attached','attaches','bind','binding','binds','binder','binders','bound','blocked','blocks','prevent','prevents','byproduct','byproducts','catabolism','catabolite','catabolites','catabolized','catabolize','catalyze','catalyzed','catalyzes','catalyst','catalysts','catalytic','cleave','cleaved','cleaves','co-imminoprecipitation','co-immunoprecipitated','co-immunoprecipitates','cofactor','cofactors','complex','complexation','complexes','coprecipitated','coprecipitates','coprecipitation','copurification','copurified','copurifies','cyclization','cyclized','cyclizes','decomposed','decomposes','decomposition','degradation','degrade','degraded','degrades','derivitise','derivitises','derivitization','derivitize','derivitizes','exported','exports','high-affinity','low-affinity','Hydrolyze','Hydrolyzed','Hydrolyzes','imported','imports','inhibited','inhibitor','inhibitors','inhibition','inhibits','interact','interacts','interaction','interactions','ligand','ligands','metabolite','metabolites','metabolized','metabolizes','modified','modifies','polymerization','polymerized','polymerizes','pump','pumped','pumps','receptor','receptors','substrate','Substrates','Target','targeted','targets','transport','transported','transports','structure','NMR','X-ray','Crystal','Structures','Binding constant','On-rate','Off-rate','Km','Ribosylated','Ribosylates','Ribosylation','Adenosinylated','Adenosinylates','Adenosinylation','Guanosylates','Guanosylated','Guanosylation','Uridinylates','Uridinylated','Uridinylation','Thymidinylates','Thymidinylated','Thymidinylation','Cytidinylated','Cytidinylation','Cytidinylates','Glutathionates','Glutathionated','Glutathionation','Sialylates','Sialylated','Sialylation','Geranylgeranylated','Geranylgeranylates','Geranylgeranylation','Stearoylates','Stearoylated','Stearoylation','Sulphates','Sulphation','Sulfation','Sulfated','Sulfates','Sulphated','Palmitoylates','Polmitoylation','Palmitoylated','Myristoylates','Myristoylation','Myristoylated','Farnesylates','Farnesylated','Farnesylation','Xanthylated','Xanthylates','Xanthylation','Glucuronidates','Glucuronidated','Glucronidation','Glucuronylates','Glucuronylated','Glucuronylation','Glycosylates','Glycosylation','Glycosylated','Glucosylates','Glucosylated','Glycosylation','Pentosylates','Pentosylated','Pentosylation','Adamantylates','Adamantylated','Adamantylation','Iodinates','Iodinated','Iodination','Succinylates','Succinylated','Succinylation','Aspartylated','Aspartylates','Aspartylation','Diaminopropionylates','Diaminopropionylated','Diaminopropionylatioin','Phosphorylates','Phosphorylated','Phosphorylation','Sulphonates','Sulphonated','Sulphonation','Dephosphorylates','Dephosphorylated','Dephosphorylation','Brominates','Brominated','Bromination','Chlorinates','Chlorinated','Chlorination','Sarcosylates','Sarcosylated','Sarcosylation','Acetylates','Acetylated','Actetylation','Deacetylates','Deacetylation','Deacetylated','Carbamylates','Carbamylated','Carbamylation','Methylates','Methylated','Methylation','Demethylates','Demethylated','Demethylation','Formylates','Formylated','Formylation','Deformylates','Deformylated','Deformylation','Hydroxylated','Hydroxylates','Hydroxylation','Dehydrated','Dehydrates','Dehydration','Dehydroxylates','Dehydroxylated','Dehydroxylation','Amidates','Amidated','Amidation','Deamidated','Deamidates','Deamidation','Carboxylates','Carboxylated','Carbosylation','Decarboxylates','Decarboxylated','Decarboxylation','Oxidizes','Oxidized','Oxidation','Reduces','Reduced','Reduction','Oxidation','Deoxidation','Deoxidates','Dehydrogenation','Dehydrogenates','Hydratase','Sulfatase','Carboxylase','Dehydratase','Hydroxylase','Formylase','Actylase']
dicts = {
    "biofluid" : biofluids,
    "color" : colors,
    "state and texture" : states_and_textures,
    "taste" : tastes,
    "health function" : health_effects,
    "food function" : food_function,
    "relationship" : relationships
    }

# temporary hardcoding of chemical synonyms
synonyms = ['11-deoxycortisol', 'cortexolone', 'cortodoxone', '17α,21-dihydroxyprogesterone', '17α,21-dihydroxypregn-4-ene-3,20-dione', "substance s", "compound s", "reichstein 's substance s"]

# irrelevant terms to remove from nouns
bad_nouns = ["=", "( inn", "see", "tadeusz reichstein", "it", "( cortisol", "a single step", "the first report", "upjohn", ]

# irrelevant terms to remove from verbs
bad_verbs = ["see", "publish", "have", "know", "discover", "begin", "look", "announce", "explain", "refer", "="]

def main():
    start = time.perf_counter()
    
    # load nlp from spacy and text from wiki
    nlp = spacy.load("en_core_web_sm")
    chemical = "11-deoxycortisol"
    text = " ".join(wikiscrape.get_wiki_words(chemical, False))
    doc = nlp(text)

    nouns = tt.get_nouns(doc)
    nouns.append("cortisol")
    verbs = tt.get_verbs(doc)

    nouns = tt.remove_nouns(bad_nouns, nouns, synonyms)
    verbs = tt.remove_verbs(bad_verbs, verbs)

    tagged_terms = tt.tag_words(dicts, nouns, verbs)

    candidate_facts = tt.generate_facts(tagged_terms,verbs)

    print(candidate_facts)
    print("Generated " + str(len(candidate_facts)) + " candidate facts.")
    end = time.perf_counter()
    print("Completed in " + str(end - start) + " seconds.")

main()