# -*- coding: utf-8 -*-
global lexiques
global temporalites
global registres
global frequences
global typesAllowed
global pays
global regions
global relations
global connotations
global diaintegrations
global genres
global contraintes
global argots

diaintegrations = {
    ur"{{anglicisme[^}]*}}": ur"(Anglicisme)",
    ur"{{germanisme[^}]*}}": ur"(Germanisme)",
    ur"{{gallicisme[^}]*}}": ur"(Gallicisme)",
    ur"{{hispanisme[^}]*}}": ur"(Hispanisme)",
    ur"{{italianisme[^}]*}}": ur"(Italianisme)",
    ur"{{lusitanisme[^}]*}}": ur"(Lusitanisme)",
    ur"{{latinisme[^}]*}}": ur"(Latinisme)"
}

genres = {
    ur"{{litt[^}]*}}": ur"(Littéraire)",
    ur"{{poét[^}]*}}": ur"(Poétique)",
    ur"{{didact[^}]*}}": ur"(Didactique)"
}

contraintes = {
    ur"{{épithète[^}]*}}": ur"(Épithète)",
    ur"{{apposition[^}]*}}": ur"(Apposition)",
    ur"{{absolument[^}]*}}": ur"(Absolument)",
    ur"{{ellip[^}]*}}": ur"(Ellipse)",
    ur"{{au pluriel[^}]*}}": ur"(Au pluriel)",
    ur"{{au singulier[^}]*}}": ur"(Au singulier)",
    ur"{{au masculin[^}]*}}": ur"(Au masculin)",
    ur"{{au féminin[^}]*}}": ur"(Au féminin)"
}

argots = {
    ur"{{arg[^}]*}}": ur"(Argot)",
    ur"{{argot scolaire[^}]*}}": ur"(Argot scolaire)",
    ur"{{argot polytechnicien[^}]*}}": ur"(Argot polytechnicien)",
    ur"{{argot policier[^}]*}}": ur"(Argot policier)",
    ur"{{argot Internet[^}]*}}": ur"(Argot Internet)",
    ur"{{argot typographes[^}]*}}": ur"(Argot typographes)",
    ur"{{argot militaire[^}]*}}": ur"(Argot militaire)",
    ur"{{argot poilu[^}]*}}": ur"(Argot poilu)",
    ur"{{argot voleurs[^}]*}}": ur"(Argot voleurs)",
    ur"{{Argadz[^}]*}}": ur"(Argadz)",
    ur"{{langage SMS[^}]*}}": ur"(Langage SMS)"
}
connotations = {
    ur"{{mélior[^}]*}}": ur"(Mélioratif)",
    ur"{{péj[^}]*}}": ur"(Péjoratif)",
    ur"{{péjor[^}]*}}": ur"(Péjoratif)",
    ur"{{affectueux[^}]*}}": ur"(Affectueux)", 	
    ur"{{par plaisanterie[^}]*}}": ur"(Par plaisanterie)",
    ur"{{par plais[^}]*}}": ur"(Par plaisanterie)",
    ur"{{plais[^}]*}}": ur"(Par plaisanterie)",
    ur"{{par dérision[^}]*}}": ur"(Par dérision)", 	
    ur"{{injurieux[^}]*}}": ur"(Injurieux)",
    ur"{{injur[^}]*}}": ur"(Injurieux)",
    ur"{{ironique[^}]*}}": ur"(Ironique)",
    ur"{{iron[^}]*}}": ur"(Ironique)"
}

relations = {
    ur"{{figuré[^}]*}}": ur"(Figuré)",
    ur"{{idiomatique[^}]*}}": ur"(Figuré)",
    ur"{{au figuré[^}]*}}": ur"(Au figuré)",
    ur"{{métaph[^}]*}}": ur"(Métaphore)",
    ur"{{métaphore[^}]*}}": ur"(Métaphore)",
    ur"{{sens propre[^}]*}}": ur"(Sens propre)",
    ur"{{propre[^}]*}}": ur"(Sens propre)",
    ur"{{par métonymie[^}]*}}": ur"(Par métonymie)",
    ur"{{métonymie[^}]*}}": ur"(Par métonymie)",
    ur"{{méton[^}]*}}": ur"(Par métonymie)",
    ur"{{par hyperbole[^}]*}}": ur"(Par hyperbole)",
    ur"{{hyperbole[^}]*}}": ur"(Hyperbole)",
    ur"{{hyperb[^}]*}}": ur"(Hyperbole)",
    ur"{{exag[^}]*}}": ur"(Exagération)",
    ur"{{exagération[^}]*}}": ur"(Exagération)",
    ur"{{par extension[^}]*}}": ur"(Par extension)",
    ur"{{par ext[^}]*}}": ur"(Par extension)",
    ur"{{par analogie[^}]*}}": ur"(Par analogie)",
    ur"{{analogie[^}]*}}": ur"(Analogie)",
    ur"{{en particulier[^}]*}}": ur"(En particulier)",
    ur"{{particulier[^}]*}}": ur"(En particulier)",
    ur"{{partic[^}]*}}": ur"(En particulier)",
    ur"{{part[^}]*}}": ur"(En particulier)",
    ur"{{par litote[^}]*}}": ur"(Par litote)",
    ur"{{par euphémisme[^}]*}}": ur"(Par euphémisme)",
    ur"{{euphémisme[^}]*}}": ur"(Par euphémisme)",
    ur"{{euph[^}]*}}": ur"(Par euphémisme)",
    ur"{{euphém[^}]*}}": ur"(Par euphémisme)",
    ur"{{spécifiquement[^}]*}}": ur"(Spécifiquement)",
    ur"{{génériquement[^}]*}}": ur"(Génériquement)",
    ur"{{spécialement[^}]*}}": ur"(Spécialement)",
    ur"{{généralement[^}]*}}": ur"(Généralement)",
}
pays = {
    "{{Canada[^}]*}}": ur"(Canada)",
    "{{France[^}]*}}": ur"(France)",
    "{{Guinée[^}]*}}": ur"(Guinée)",
    "{{Mali[^}]*}}": ur"(Mali)",
    "{{Belgique[^}]*}}": ur"(Belgique)"
}

regions = {
    "{{Bordelais[^}]*}}": ur"(Bordelaise)",
    "{{Acadie[^}]*}}": ur"(Acadie)",
    "{{Auvergne[^}]*}}": ur"(Auvergne)",
    "{{Aquitaine[^}]*}}": ur"(Aquitaine)",
    "{{Antilles[^}]*}}": ur"(Antilles)",
    "{{Anjou[^}]*}}": ur"(Anjou)",
    "{{Bourgogne[^}]*}}": ur"(Bourgogne)",
    "{{Berry[^}]*}}": ur"(Berry)",
    "{{Bretagne[^}]*}}": ur"(Bretagne)",
    "{{Champagne[^}]*}}": ur"(Champagne)",
    "{{Corse[^}]*}}": ur"(Corse)",
    "{{Franche-Comté[^}]*}}": ur"(Franche-Comté)",
    "{{Gaspésie[^}]*}}": ur"(Gaspésie)",
    "{{Gascogne[^}]*}}": ur"(Gascogne)",
    "{{Guadeloupe[^}]*}}": ur"(Guadeloupe)",
    "{{Guyane[^}]*}}": ur"(Guyane)",
    "{{Le Mans[^}]*}}": ur"(Le Mans)",
    "{{Languedoc-Roussillon[^}]*}}": ur"(Langedoc-Roussillon)",
    "{{Limousin[^}]*}}": ur"(Limousin)",
    "{{Lorraine[^}]*}}": ur"(Lorraine)",
    "{{Louisiane[^}]*}}": ur"(Louisiane)",
    "{{Lyonnais[^}]*}}": ur"(Lyonnais)",
    "{{Lorraine[^}]*}}": ur"(Lorraine)",
    "{{Martinique[^}]*}}": ur"(Martinique)",
    "{{Mayotte[^}]*}}": ur"(Mayotte)",
    "{{Midi[^}]*}}": ur"(Midi)",
    "{{Midi toulousain[^}]*}}": ur"(Midi toulousain)",
    "{{Montréal[^}]*}}": ur"(Montréal)",
    "{{Provence[^}]*}}": ur"(Provence)",
    "{{Québec[^}]*}}": ur"(Québec)",
    "{{Quercy[^}]*}}": ur"(Quercy)",
    "{{Normandie[^}]*}}": ur"(Normandie)",
    "{{Nantes[^}]*}}": ur"(Nantes)",
    "{{Picardie[^}]*}}": ur"(Picardie)",
    "{{Poitou[^}]*}}": ur"(Poitou)",
    "{{Polynésie française[^}]*}}": ur"(Polynésie française)",
    "{{Occitanie[^}]*}}": ur"(Occitanie)",
    "{{Provence[^}]*}}": ur"(Provence)",
    "{{Réunion[^}]*}}": ur"(Réunion)",
    "{{Rhône-Alpes[^}]*}}": ur"(Rhône-Alpes)",
    "{{Vosges[^}]*}}": ur"(Vosges)",
    "{{Var[^}]*}}": ur"(Var)",
    "{{Velay[^}]*}}": ur"(Velay)"
}

typesAllowed = [
    ur"adjectif",
    ur"adjectif démonstratif",
    ur"adjectif exclamatif",
    ur"adjectif indéfini",
    ur"adjectif interrogatif",
    ur"adjectif numéral",
    ur"adjectif possessif",
    ur"adverbe",
    ur"adverbe indéfini",
    ur"adverbe interrogatif",
    ur"dverbe pronominal",
    ur"adverbe relatif",
    ur"article défini",
    ur"article indéfini",
    ur"article",
    ur"conjonction de coordination",
    ur"déterminant",
    ur"nom",
    ur"nom commun",
    ur"préposition",
    ur"pronom démonstratif",
    ur"pronom indéfini",
    ur"pronom interrogatif",
    ur"ronom personnel",
    ur"pronom possessif",
    ur"pronom relatif",
    ur"pronom",
    ur"pronom-adjectif",
    ur"verbe" 
]
registres = {
    "{{très fam[^}]*}}": ur"(Très familier)",
    "{{fam[^}]*}}": ur"(Familier)",
    "{{dial[^}]*}}": ur"(Familier)",
    "{{oral[^}]*}}": ur"(Familier)",
    "{{informel[^}]*}}": ur"(Informel)",
    "{{populaire[^}]*}}": ur"(Populaire)",
    "{{pop[^}]*}}": ur"(Populaire)",
    "{{vulgaire[^}]*}}": ur"(Vulgaire)",
    "{{vulg[^}]*}}": ur"(Vulgaire)",
    "{{soutenu[^}]*}}": ur"(Soutenu)",
    "{{écrit[^}]*}}": ur"(Soutenu)",
    "{{formel[^}]*}}": ur"(Soutenu)",
    "{{enfantin[^}]*}}": ur"(Langage enfantin}"
}

temporalites = {
    "{{vieilli[^}]*}}": ur"(Vieilli)",
    "{{archaïsme[^}]*}}": ur"(Archaïsme)",
    "{{désuet[^}]*}}": ur"(Désuet)",
    "{{néologisme[^}]*}}": ur"(Néologisme)"
}
frequences = {
    "{{courant[^}]*}}": ur"(Courant)",
    "{{cour[^}]*}}": ur"(Courant)",
    "{{peu usité[^}]*}}": ur"(Peu usité)",
    "{{rare[^}]*}}": ur"(Rare)",
    "{{rar[^}]*}}": ur"(Rare)",
    "{{très rare[^}]*}}": ur"(Très rare)",
    "{{extrêmement rare[^}]*}}": ur"(Extrêmement rare)",
    "{{hapax[^}]*}}": ur"(Hapax)",
    "{{peu attesté[^}]*}}": ur"(Peu attesté)",
    "{{plus rare[^}]*}}": ur"(Plus rare}",
    "{{moins courant[^}]*}}": ur"(Moins courant}",
    "{{beaucoup moins courant[^}]*}}": ur"(Beaucoup moins courant}",
    "{{plus courant[^}]*}}": ur"(Plus courant}",
    "{{beaucoup plus courant[^}]*}}": ur"(Beaucoup plus courant}"
}
lexiques = {
        ur"{{acoustique[^}]*}}": ur"(Acoustique)",
        ur"{{administration[^}]*}}": ur"(Administration)",
        ur"{{aéronautique[^}]*}}": ur"(Aéronautique)",
        ur"{{agriculture[^}]*}}": ur"(Agriculture)",
        ur"{{agronomie[^}]*}}": ur"(Agronomie)",
        ur"{{aïkido[^}]*}}": ur"(Aïkido)",
        ur"{{alchimie[^}]*}}": ur"(Alchimie)",
        ur"{{algèbre[^}]*}}": ur"(Algèbre)",
        ur"{{alpinisme[^}]*}}": ur"(Alpinisme)",
        ur"{{analyse[^}]*}}": ur"(Analyse)",
        ur"{{anatomie[^}]*}}": ur"(Anatomie)",
        ur"{{anthropologie[^}]*}}": ur"(Anthropologie)",
        ur"{{antiquité[^}]*}}": ur"(Antiquité)",
        ur"{{apiculture[^}]*}}": ur"(Apiculture)",
        ur"{{arboriculture[^}]*}}": ur"(Arboriculture)",
        ur"{{archéologie[^}]*}}": ur"(Archéologie)",
        ur"{{architecture[^}]*}}": ur"(Architecture)",
        ur"{{Argadz[^}]*}}": ur"(Argadz)",
        ur"{{armement[^}]*}}": ur"(Armement)",
        ur"{{arts[^}]*}}": ur"(Arts)",
        ur"{{arts martiaux[^}]*}}": ur"(Arts martiaux)",
        ur"{{assurance[^}]*}}": ur"(Assurance)",
        ur"{{astrologie[^}]*}}": ur"(Astrologie)",
        ur"{{astronautique[^}]*}}": ur"(Astronautique)",
        ur"{{astronomie[^}]*}}": ur"(Astronomie)",
        ur"{{astrophysique[^}]*}}": ur"(Astrophysique)",
        ur"{{athlétisme[^}]*}}": ur"(Athlétisme)",
        ur"{{audiovisuel[^}]*}}": ur"(Audiovisuel)",
        ur"{{automatique[^}]*}}": ur"(Automatique)",
        ur"{{automobile[^}]*}}": ur"(Automobile)",
        ur"{{aviation[^}]*}}": ur"(Aviation)",
        ur"{{baby-foot[^}]*}}": ur"(Baby-foot)",
        ur"{{bactériologie[^}]*}}": ur"(Bactériologie)",
        ur"{{badminton[^}]*}}": ur"(Badminton)",
        ur"{{base de données[^}]*}}": ur"(Base de données)",
        ur"{{baseball[^}]*}}": ur"(Baseball)",
        ur"{{basket-ball[^}]*}}": ur"(Basket-ball)",
        ur"{{BD[^}]*}}": ur"(BD)",
        ur"{{beaux-arts[^}]*}}": ur"(Beaux-arts)",
        ur"{{bibliothéconomie[^}]*}}": ur"(Bibliothéconomie)",
        ur"{{bijouterie[^}]*}}": ur"(Bijouterie)",
        ur"{{billard[^}]*}}": ur"(Billard)",
        ur"{{biochimie[^}]*}}": ur"(Biochimie)",
        ur"{{biogéographie[^}]*}}": ur"(Biogéographie)",
        ur"{{biologie[^}]*}}": ur"(Biologie)",
        ur"{{biophysique[^}]*}}": ur"(Biophysique)",
        ur"{{bonsaï[^}]*}}": ur"(Bonsaï)",
        ur"{{botanique[^}]*}}": ur"(Botanique)",
        ur"{{boucherie[^}]*}}": ur"(Boucherie)",
        ur"{{bouddhisme[^}]*}}": ur"(Bouddhisme)",
        ur"{{bourrellerie[^}]*}}": ur"(Bourrellerie)",
        ur"{{bowling[^}]*}}": ur"(Bowling)",
        ur"{{boxe[^}]*}}": ur"(Boxe)",
        ur"{{bridge[^}]*}}": ur"(Bridge)",
        ur"{{calendrier[^}]*}}": ur"(Calendrier)",
        ur"{{calligraphie[^}]*}}": ur"(Calligraphie)",
        ur"{{canoë-kayak[^}]*}}": ur"(Canoë-kayak)",
        ur"{{capoeira[^}]*}}": ur"(Capoeira)",
        ur"{{cartes[^}]*}}": ur"(Cartes)",
        ur"{{cartographie[^}]*}}": ur"(Cartographie)",
        ur"{{caséologie[^}]*}}": ur"(Caséologie)",
        ur"{{catch[^}]*}}": ur"(Catch)",
        ur"{{CB[^}]*}}": ur"(CB)",
        ur"{{céramique[^}]*}}": ur"(Céramique)",
        ur"{{charpenterie[^}]*}}": ur"(Charpenterie)",
        ur"{{charronnerie[^}]*}}": ur"(Charronnerie)",
        ur"{{chasse[^}]*}}": ur"(Chasse)",
        ur"{{chimie[^}]*}}": ur"(Chimie)",
        ur"{{chiromancie[^}]*}}": ur"(Chiromancie)",
        ur"{{chirurgie[^}]*}}": ur"(Chirurgie)",
        ur"{{christianisme[^}]*}}": ur"(Christianisme)",
        ur"{{chronologie[^}]*}}": ur"(Chronologie)",
        ur"{{cinéma[^}]*}}": ur"(Cinéma)",
        ur"{{cirque[^}]*}}": ur"(Cirque)",
        ur"{{climatologie[^}]*}}": ur"(Climatologie)",
        ur"{{coiffure[^}]*}}": ur"(Coiffure)",
        ur"{{colorimétrie[^}]*}}": ur"(Colorimétrie)",
        ur"{{commerce[^}]*}}": ur"(Commerce)",
        ur"{{comptabilité[^}]*}}": ur"(Comptabilité)",
        ur"{{construction[^}]*}}": ur"(Construction)",
        ur"{{copropriété[^}]*}}": ur"(Copropriété)",
        ur"{{cordonnerie[^}]*}}": ur"(Cordonnerie)",
        ur"{{cosmétologie[^}]*}}": ur"(Cosmétologie)",
        ur"{{couche application[^}]*}}": ur"(Couche application)",
        ur"{{couche liaison[^}]*}}": ur"(Couche liaison)",
        ur"{{couche physique[^}]*}}": ur"(Couche physique)",
        ur"{{couche présentation[^}]*}}": ur"(Couche présentation)",
        ur"{{couche réseau[^}]*}}": ur"(Couche réseau)",
        ur"{{couche session[^}]*}}": ur"(Couche session)",
        ur"{{couche transport[^}]*}}": ur"(Couche transport)",
        ur"{{course à pied[^}]*}}": ur"(Course à pied)",
        ur"{{couture[^}]*}}": ur"(Couture)",
        ur"{{cricket[^}]*}}": ur"(Cricket)",
        ur"{{cryptographie[^}]*}}": ur"(Cryptographie)",
        ur"{{cryptomonnaie[^}]*}}": ur"(Cryptomonnaie)",
        ur"{{cuisine[^}]*}}": ur"(Cuisine)",
        ur"{{cyclisme[^}]*}}": ur"(Cyclisme)",
        ur"{{dames[^}]*}}": ur"(Dames)",
        ur"{{danse[^}]*}}": ur"(Danse)",
        ur"{{dentisterie[^}]*}}": ur"(Dentisterie)",
        ur"{{dermatologie[^}]*}}": ur"(Dermatologie)", 
        ur"{{dessin[^}]*}}": ur"(Dessin)",
        ur"{{didactique[^}]*}}": ur"(Didactique)",
        ur"{{diplomatie[^}]*}}": ur"(Diplomatie)",
        ur"{{drogue[^}]*}}": ur"(Drogue)",
        ur"{{droit[^}]*}}": ur"(Droit)",
        ur"{{échafaudage[^}]*}}": ur"(Échafaudage)",
        ur"{{échecs[^}]*}}": ur"(Échecs)",
        ur"{{écologie[^}]*}}": ur"(Écologie)",
        ur"{{économie[^}]*}}": ur"(Économie)",
        ur"{{édition[^}]*}}": ur"(Édition)",
        ur"{{éducation[^}]*}}": ur"(Éducation)",
        ur"{{électoraux[^}]*}}": ur"(Électoraux)",
        ur"{{électricité[^}]*}}": ur"(Électricité)",
        ur"{{électronique[^}]*}}": ur"(Électronique)",
        ur"{{électrotechnique[^}]*}}": ur"(Électrotechnique)",
        ur"{{élevage[^}]*}}": ur"(Élevage)",
        ur"{{embryologie[^}]*}}": ur"(Embryologie)",
        ur"{{entomologie[^}]*}}": ur"(Entomologie)",
        ur"{{équitation[^}]*}}": ur"(Équitation)",
        ur"{{escrime[^}]*}}": ur"(Escrime)",
        ur"{{ethnobiologie[^}]*}}": ur"(Ethnobiologie)",
        ur"{{ethnologie[^}]*}}": ur"(Ethnologie)",
        ur"{{famille[^}]*}}": ur"(Famille)",
        ur"{{fantastique[^}]*}}": ur"(Fantastique)",
        ur"{{fauconnerie[^}]*}}": ur"(Fauconnerie)",
        ur"{{ferroviaire[^}]*}}": ur"(Ferroviaire)",
        ur"{{finance[^}]*}}": ur"(Finance)",
        ur"{{fiscalité[^}]*}}": ur"(Fiscalité)",
        ur"{{fontainerie[^}]*}}": ur"(Fontainerie)",
        ur"{{football[^}]*}}": ur"(Football)",
        ur"{{foresterie[^}]*}}": ur"(Foresterie)",
        ur"{{franc-maçonnerie[^}]*}}": ur"(Franc-maçonnerie)",
        ur"{{généalogie[^}]*}}": ur"(Généalogie)",
        ur"{{génétique[^}]*}}": ur"(Génétique)",
        ur"{{géographie[^}]*}}": ur"(Géographie)",
        ur"{{géologie[^}]*}}": ur"(Géologie)",
        ur"{{géomatique[^}]*}}": ur"(Géomatique)",
        ur"{{géométrie[^}]*}}": ur"(Géométrie)", 
        ur"{{géophysique[^}]*}}": ur"(Géophysique)",
        ur"{{géostatistique[^}]*}}": ur"(Géostatistique)",
        ur"{{glaciologie[^}]*}}": ur"(Glaciologie)",
        ur"{{golf[^}]*}}": ur"(Golf)",
        ur"{{grammaire[^}]*}}": ur"(Grammaire)",
        ur"{{gravure[^}]*}}": ur"(Gravure)",
        ur"{{gymnastique[^}]*}}": ur"(Gymnastique)",
        ur"{{handball[^}]*}}": ur"(Handball)",
        ur"{{handisport[^}]*}}": ur"(Handisport)",
        ur"{{héraldique[^}]*}}": ur"(Héraldique)", 
        ur"{{hindouisme[^}]*}}": ur"(Hindouisme)",
        ur"{{hippisme[^}]*}}": ur"(Hippisme)",
        ur"{{hippologie[^}]*}}": ur"(Hippologie)",
        ur"{{histoire[^}]*}}": ur"(Histoire)",
        ur"{{histologie[^}]*}}": ur"(Histologie)",
        ur"{{hockey[^}]*}}": ur"(Hockey)",
        ur"{{horlogerie[^}]*}}": ur"(Horlogerie)",
        ur"{{horticulture[^}]*}}": ur"(Horticulture)",
        ur"{{hydraulique[^}]*}}": ur"(Hydraulique)",
        ur"{{hydrobiologie[^}]*}}": ur"(Hydrobiologie)",
        ur"{{hydrologie[^}]*}}": ur"(Hydrologie)",
        ur"{{hygiène[^}]*}}": ur"(Hygiène)",
        ur"{{ichtyologie[^}]*}}": ur"(Ichtyologie)",
        ur"{{illégalité[^}]*}}": ur"(Illégalité)",
        ur"{{imprimerie[^}]*}}": ur"(Imprimerie)",
        ur"{{industrie[^}]*}}": ur"(Industrie)",
        ur"{{infographie[^}]*}}": ur"(Infographie)",
        ur"{{informatique[^}]*}}": ur"(Informatique)",
        ur"{{intelligence artificielle[^}]*}}": ur"(Intelligence artificielle)",
        ur"{{internet[^}]*}}": ur"(Internet)",
        ur"{{islam[^}]*}}": ur"(Islam)",
        ur"{{jardinage[^}]*}}": ur"(Jardinage)",
        ur"{{jazz[^}]*}}": ur"(Jazz)",
        ur"{{jeu de go[^}]*}}": ur"(Jeu de go)",
        ur"{{jeu de paume[^}]*}}": ur"(Jeu de paume)",
        ur"{{jeux[^}]*}}": ur"(Jeux)",
        ur"{{jeux vidéo[^}]*}}": ur"(Jeux vidéo)",
        ur"{{jonglerie[^}]*}}": ur"(Jonglerie)",
        ur"{{journalisme[^}]*}}": ur"(Journalisme)",
        ur"{{judaïsme[^}]*}}": ur"(Judaïsme)",
        ur"{{judo[^}]*}}": ur"(Judo)",
        ur"{{justice[^}]*}}": ur"(Justice)",
        ur"{{karaté[^}]*}}": ur"(Karaté)",
        ur"{{langage Java[^}]*}}": ur"(Langage Java)",
        ur"{{législation[^}]*}}": ur"(Législation)",
        ur"{{lexicographie[^}]*}}": ur"(Lexicographie)",
        ur"{{LGBT[^}]*}}": ur"(LGBT)",
        ur"{{linguistique[^}]*}}": ur"(Linguistique)",
        ur"{{littérature[^}]*}}": ur"(Littérature)",
        ur"{{liturgie[^}]*}}": ur"(Liturgie)",
        ur"{{livre[^}]*}}": ur"(Livre)",
        ur"{{logique[^}]*}}": ur"(Logique)",
        ur"{{logistique[^}]*}}": ur"(Logistique)",
        ur"{{loisirs[^}]*}}": ur"(Loisirs)",
        ur"{{lutherie[^}]*}}": ur"(Lutherie)",
        ur"{{maçonnerie[^}]*}}": ur"(Maçonnerie)",
        ur"{{magnétisme[^}]*}}": ur"(Magnétisme)",
        ur"{{mah-jong[^}]*}}": ur"(Mah-jong)",
        ur"{{maintenance[^}]*}}": ur"(Maintenance)",
        ur"{{marbrerie[^}]*}}": ur"(Marbrerie)",
        ur"{{maréchalerie[^}]*}}": ur"(Maréchalerie)",
        ur"{{marine[^}]*}}": ur"(Marine)",
        ur"{{maroquinerie[^}]*}}": ur"(Maroquinerie)",
        ur"{{mathématiques[^}]*}}": ur"(Mathématiques)",
        ur"{{mécanique[^}]*}}": ur"(Mécanique)",
        ur"{{médecine[^}]*}}": ur"(Médecine)",
        ur"{{médecine non conv[^}]*}}": ur"(Médecine non conv)",
        ur"{{médecine vétérinaire[^}]*}}": ur"(Médecine vétérinaire)",
        ur"{{média[^}]*}}": ur"(Média)",
        ur"{{menuiserie[^}]*}}": ur"(Menuiserie)", 
        ur"{{mercatique[^}]*}}": ur"(Mercatique)",
        ur"{{metal[^}]*}}": ur"(Metal)",
        ur"{{métallurgie[^}]*}}": ur"(Métallurgie)",
        ur"{{météorologie[^}]*}}": ur"(Météorologie)",
        ur"{{métrologie[^}]*}}": ur"(Métrologie)",
        ur"{{meunerie[^}]*}}": ur"(Meunerie)",
        ur"{{microbiologie[^}]*}}": ur"(Microbiologie)",
        ur"{{militaire[^}]*}}": ur"(Militaire)",
        ur"{{minéralogie[^}]*}}": ur"(Minéralogie)",
        ur"{{miroiterie[^}]*}}": ur"(Miroiterie)",
        ur"{{monarchie[^}]*}}": ur"(Monarchie)",
        ur"{{morphologie végétale[^}]*}}": ur"(Morphologie végétale)",
        ur"{{motocyclisme[^}]*}}": ur"(Motocyclisme)",
        ur"{{Moyen Âge[^}]*}}": ur"(Moyen Âge)",
        ur"{{muscle[^}]*}}": ur"(Muscle)",
        ur"{{musculation[^}]*}}": ur"(Musculation)",
        ur"{{muséologie[^}]*}}": ur"(Muséologie)",
        ur"{{musique[^}]*}}": ur"(Musique)",
        ur"{{mycologie[^}]*}}": ur"(Mycologie)",
        ur"{{mythologie[^}]*}}": ur"(Mythologie)",
        ur"{{narratologie[^}]*}}": ur"(Narratologie)",
        ur"{{natation[^}]*}}": ur"(Natation)",
        ur"{{navigation[^}]*}}": ur"(Navigation)",
        ur"{{neurologie[^}]*}}": ur"(Neurologie)",
        ur"{{noblesse[^}]*}}": ur"(Noblesse)",
        ur"{{nosologie[^}]*}}": ur"(Nosologie)",
        ur"{{novlangue[^}]*}}": ur"(Novlangue)",
        ur"{{nucléaire[^}]*}}": ur"(Nucléaire)",
        ur"{{numismatique[^}]*}}": ur"(Numismatique)",
        ur"{{nutrition[^}]*}}": ur"(Nutrition)",
        ur"{{occultisme[^}]*}}": ur"(Occultisme)",
        ur"{{océanographie[^}]*}}": ur"(Océanographie)",
        ur"{{œnologie[^}]*}}": ur"(Œnologie)",
        ur"{{optimisation[^}]*}}": ur"(Optimisation)",
        ur"{{optique[^}]*}}": ur"(Optique)",
        ur"{{orgues[^}]*}}": ur"(Orgues)",
        ur"{{ornement[^}]*}}": ur"(Ornement)",
        ur"{{ornithologie[^}]*}}": ur"(Ornithologie)",
        ur"{{paléographie[^}]*}}": ur"(Paléographie)",
        ur"{{paléontologie[^}]*}}": ur"(Paléontologie)",
        ur"{{papeterie[^}]*}}": ur"(Papeterie)",
        ur"{{patinage[^}]*}}": ur"(Patinage)",
        ur"{{pâtisserie[^}]*}}": ur"(Pâtisserie)",
        ur"{{pêche[^}]*}}": ur"(Pêche)",
        ur"{{pédologie[^}]*}}": ur"(Pédologie)",
        ur"{{peinture[^}]*}}": ur"(Peinture)",
        ur"{{pelote[^}]*}}": ur"(Pelote)",
        ur"{{pétanque[^}]*}}": ur"(Pétanque)",
        ur"{{pétrochimie[^}]*}}": ur"(Pétrochimie)",
        ur"{{pharmacologie[^}]*}}": ur"(Pharmacologie)",
        ur"{{phénologie[^}]*}}": ur"(Phénologie)",
        ur"{{phénoménologie[^}]*}}": ur"(Phénoménologie)",
        ur"{{philatélie[^}]*}}": ur"(Philatélie)",
        ur"{{philosophie[^}]*}}": ur"(Philosophie)",
        ur"{{phonétique[^}]*}}": ur"(Phonétique)",
        ur"{{phonologie[^}]*}}": ur"(Phonologie)",
        ur"{{photographie[^}]*}}": ur"(Photographie)",
        ur"{{physiologie[^}]*}}": ur"(Physiologie)",
        ur"{{physique[^}]*}}": ur"(Physique)",
        ur"{{phytosociologie[^}]*}}": ur"(Phytosociologie)",
        ur"{{planche à neige[^}]*}}": ur"(Planche à neige)",
        ur"{{planche à roulettes[^}]*}}": ur"(Planche à roulettes)",
        ur"{{plomberie[^}]*}}": ur"(Plomberie)",
        ur"{{plongée[^}]*}}": ur"(Plongée)",
        ur"{{poésie[^}]*}}": ur"(Poésie)",
        ur"{{poker[^}]*}}": ur"(Poker)",
        ur"{{police[^}]*}}": ur"(Police)",
        ur"{{politique[^}]*}}": ur"(Politique)",
        ur"{{préhistoire[^}]*}}": ur"(Préhistoire)",
        ur"{{prestidigitation[^}]*}}": ur"(Prestidigitation)",
        ur"{{probabilités[^}]*}}": ur"(Probabilités)",
        ur"{{programmation[^}]*}}": ur"(Programmation)",
        ur"{{programmation orientée objet[^}]*}}": ur"(Programmation orientée objet)",
        ur"{{propriété[^}]*}}": ur"(Propriété)",
        ur"{{psychanalyse[^}]*}}": ur"(Psychanalyse)",
        ur"{{psychiatrie[^}]*}}": ur"(Psychiatrie)",
        ur"{{psychologie[^}]*}}": ur"(Psychologie)",
        ur"{{pyrotechnie[^}]*}}": ur"(Pyrotechnie)",
        ur"{{raffinage[^}]*}}": ur"(Raffinage)",
        ur"{{regex[^}]*}}": ur"(Regex)",
        ur"{{relations internationales[^}]*}}": ur"(Relations internationales)",
        ur"{{religion[^}]*}}": ur"(Religion)",
        ur"{{reliure[^}]*}}": ur"(Reliure)",
        ur"{{renseignement[^}]*}}": ur"(Renseignement)",
        ur"{{reproduction[^}]*}}": ur"(Reproduction)",
        ur"{{réseaux informatiques[^}]*}}": ur"(Réseaux informatiques)",
        ur"{{rhétorique[^}]*}}": ur"(Rhétorique)",
        ur"{{robotique[^}]*}}": ur"(Robotique)",
        ur"{{rugby[^}]*}}": ur"(Rugby)",
        ur"{{saliculture[^}]*}}": ur"(Saliculture)",
        ur"{{saut en hauteur[^}]*}}": ur"(Saut en hauteur)",
        ur"{{science-fiction[^}]*}}": ur"(Science-fiction)",
        ur"{{sciences[^}]*}}": ur"(Sciences)",
        ur"{{Scrabble[^}]*}}": ur"(Scrabble)",
        ur"{{sculpture[^}]*}}": ur"(Sculpture)",
        ur"{{serrurerie[^}]*}}": ur"(Serrurerie)",
        ur"{{sexualité[^}]*}}": ur"(Sexualité)",
        ur"{{sidérurgie[^}]*}}": ur"(Sidérurgie)",
        ur"{{ski alpin[^}]*}}": ur"(Ski alpin)",
        ur"{{ski de fond[^}]*}}": ur"(Ski de fond)",
        ur"{{snowboard[^}]*}}": ur"(Snowboard)",
        ur"{{socialisme[^}]*}}": ur"(Socialisme)",
        ur"{{sociolinguistique[^}]*}}": ur"(Sociolinguistique)",
        ur"{{sociologie[^}]*}}": ur"(Sociologie)",
        ur"{{sport[^}]*}}": ur"(Sport)",
        ur"{{squelette[^}]*}}": ur"(Squelette)",
        ur"{{statistiques[^}]*}}": ur"(Statistiques)",
        ur"{{stéréochimie[^}]*}}": ur"(Stéréochimie)",
        ur"{{stéréotomie[^}]*}}": ur"(Stéréotomie)",
        ur"{{stéréotype[^}]*}}": ur"(Stéréotype)",
        ur"{{surf[^}]*}}": ur"(Surf)",
        ur"{{sylviculture[^}]*}}": ur"(Sylviculture)",
        ur"{{taille de pierre[^}]*}}": ur"(Taille de pierre)",
        ur"{{tauromachie[^}]*}}": ur"(Tauromachie)",
        ur"{{technique[^}]*}}": ur"(Technique)",
        ur"{{technologie[^}]*}}": ur"(Technologie)",
        ur"{{télécommunications[^}]*}}": ur"(Télécommunications)",
        ur"{{téléinformatique[^}]*}}": ur"(Téléinformatique)",
        ur"{{téléphonie[^}]*}}": ur"(Téléphonie)",
        ur"{{tennis[^}]*}}": ur"(Tennis)",
        ur"{{tennis de table[^}]*}}": ur"(Tennis de table)",
        ur"{{tératologie[^}]*}}": ur"(Tératologie)",
        ur"{{textile[^}]*}}": ur"(Textile)",
        ur"{{théâtre[^}]*}}": ur"(Théâtre)",
        ur"{{théologie[^}]*}}": ur"(Théologie)",
        ur"{{théorie des graphes[^}]*}}": ur"(Théorie des graphes)",
        ur"{{thermodynamique[^}]*}}": ur"(Thermodynamique)",
        ur"{{tonnellerie[^}]*}}": ur"(Tonnellerie)",
        ur"{{topographie[^}]*}}": ur"(Topographie)",
        ur"{{topologie[^}]*}}": ur"(Topologie)",
        ur"{{toponymie[^}]*}}": ur"(Toponymie)",
        ur"{{tourisme[^}]*}}": ur"(Tourisme)",
        ur"{{transport[^}]*}}": ur"(Transport)",
        ur"{{travail[^}]*}}": ur"(Travail)",
        ur"{{triathlon[^}]*}}": ur"(Triathlon)",
        ur"{{typographie[^}]*}}": ur"(Typographie)",
        ur"{{ufologie[^}]*}}": ur"(Ufologie)",
        ur"{{urbanisme[^}]*}}": ur"(Urbanisme)",
        ur"{{usinage[^}]*}}": ur"(Usinage)",
        ur"{{vaudou[^}]*}}": ur"(Vaudou)",
        ur"{{versification[^}]*}}": ur"(Versification)",
        ur"{{vexillologie[^}]*}}": ur"(Vexillologie)",
        ur"{{virologie[^}]*}}": ur"(Virologie)",
        ur"{{viticulture[^}]*}}": ur"(Viticulture)",
        ur"{{vitrerie[^}]*}}": ur"(Vitrerie)",
        ur"{{volley-ball[^}]*}}": ur"(Volley-ball)",
        ur"{{wiki[^}]*}}": ur"(Wiki)",
        ur"{{yoga[^}]*}}": ur"(Yoga)",
        ur"{{zoologie[^}]*}}": ur"(Zoologie)"
    }
