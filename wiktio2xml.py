#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Bruno Coudoin
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, see <http://www.gnu.org/licenses/>.
#

from xml.sax import parse
from xml.sax.handler import ContentHandler
import sys
import re
import os

from optparse import OptionParser

import wiktio
from wiktio import Wiktio

compteur = 0
compteurMax = 10
debug = False
toAdd = False
# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass

class EndOfParsing(Error):
    """Raised when parsing is over"""
    pass

class WikiHandler(ContentHandler):

    def __init__ (self, searchWords, locale, _wiktio, verbose):
 
        self.searchWords= searchWords;
        self.locale = locale
        self.wiktio = _wiktio
        self.verbose = verbose

        self.isPageElement = False

        self.isTitleElement = False
        self.titleContent = u""

        self.isTextElement = False
        self.textContent = u""

        self.lilevel = 0

    def startElement(self, name, attrs):
        if name == 'page':
            self.isPageElement = True
        elif name == 'title':
            self.isTitleElement = True
            self.titleContent = ""
        elif name == 'text':
            self.isTextElement = True
            self.textContent = ""

        self.genders = {
            "{{m}}": u"masculin",
            "{{f}}": u"féminin",
            "{{mf}}": u"masculin et féminin"
            }

        self.wordTypes = {
            u"{{.*nom.*}}": u"nom",
            u"{{-nom-pr.*}}": u"nom propre",
            u"{{.*verb.*}}": u"verbe",
            u"{{.*pronom.*}}": u"pronom",
            u"{{.*adjectif.*}}": u"adjectif",
            u"{{.*adverbe.*}}": u"adverbe",
            u"{-art-.*}}": u"article",
            u"{-conj-.*}}": u"conjunction",
            u"{-prèp-.*}}": u"préposition",
            u"{-post-.*}}": u"postposition"
            }
        self.typesAllowed = [
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
            ur"pronom démonstratif",
            ur"pronom indéfini",
            ur"pronom interrogatif",
            ur"ronom personnel",
            ur"pronom possessif",
            ur"pronom relatif",
            ur"pronom",
            ur"pronom-adjectif",
            ur"verbe" ]

        # This is the list of word types we don't want to keep
        self.wordSkipTypes = [
            "{{-flex-verb-"
            ]

        self.wordSubTypes = {
            "{{1ergroupe}}": "1er groupe",
            "{{2egroupe}}": "2eme groupe",
            "{{3egroupe}}": "3eme groupe",
            }

        self.registres = {
            "{{familier[^}]*}}": ur"(Familier)",
            "{{informel[^}]*}}": ur"(Informel)",
            "{{populaire[^}]*}}": ur"(Populaire)",
            "{{vulgaire[^}]*}}": ur"(Vulgaire)",
            "{{soutenu[^}]*}}": ur"(Soutenu)",
            "{{formel[^}]*}}": ur"(Soutenu)",
            "{{enfantin[^}]*}}": ur"(Langage enfantin}"
            }

	self.lexique = {
            "{{acoustique[^}]}}": ur"(Acoustique)",
            "{{administration[^}]}}": ur"(Administration)",
            "{{aéronautique[^}]}}": ur"(Aéronautique)",
            "{{agriculture[^}]}}": ur"(Agriculture)",
            "{{agronomie[^}]}}": ur"(Agronomie)",
            "{{aïkido[^}]}}": ur"(Aïkido)",
            "{{alchimie[^}]}}": ur"(Alchimie)",
            "{{algèbre[^}]}}": ur"(Algèbre)",
            "{{alpinisme[^}]}}": ur"(Alpinisme)",
            "{{analyse[^}]}}": ur"(Analyse)",
            "{{anatomie[^}]}}": ur"(Anatomie)",
            "{{anthropologie[^}]}}": ur"(Anthropologie)",
            "{{antiquité[^}]}}": ur"(Antiquité)",
            "{{apiculture[^}]}}": ur"(Apiculture)",
            "{{arboriculture[^}]}}": ur"(Arboriculture)",
            "{{archéologie[^}]}}": ur"(Archéologie)",
            "{{architecture[^}]}}": ur"(Architecture)",
            "{{Argadz[^}]}}": ur"(Argadz)",
            "{{armement[^}]}}": ur"(Armement)",
            "{{arts[^}]}}": ur"(Arts)",
            "{{arts martiaux[^}]}}": ur"(Arts martiaux)",
            "{{assurance[^}]}}": ur"(Assurance)",
            "{{astrologie[^}]}}": ur"(Astrologie)",
            "{{astronautique[^}]}}": ur"(Astronautique)",
            "{{astronomie[^}]}}": ur"(Astronomie)",
            "{{astrophysique[^}]}}": ur"(Astrophysique)",
            "{{athlétisme[^}]}}": ur"(Athlétisme)",
            "{{audiovisuel[^}]}}": ur"(Audiovisuel)",
            "{{automatique[^}]}}": ur"(Automatique)",
            "{{automobile[^}]}}": ur"(Automobile)",
            "{{aviation[^}]}}": ur"(Aviation)",
            "{{baby-foot[^}]}}": ur"(Baby-foot)",
            "{{bactériologie[^}]}}": ur"(Bactériologie)",
            "{{badminton[^}]}}": ur"(Badminton)",
            "{{base de données[^}]}}": ur"(Base de données)",
            "{{baseball[^}]}}": ur"(Baseball)",
            "{{basket-ball[^}]}}": ur"(Basket-ball)",
            "{{BD[^}]}}": ur"(BD)",
            "{{beaux-arts[^}]}}": ur"(Beaux-arts)",
            "{{bibliothéconomie[^}]}}": ur"(Bibliothéconomie)",
            "{{bijouterie[^}]}}": ur"(Bijouterie)",
            "{{billard[^}]}}": ur"(Billard)",
            "{{biochimie[^}]}}": ur"(Biochimie)",
            "{{biogéographie[^}]}}": ur"(Biogéographie)",
            "{{biologie[^}]}}": ur"(Biologie)",
            "{{biophysique[^}]}}": ur"(Biophysique)",
            "{{bonsaï[^}]}}": ur"(Bonsaï)",
            "{{botanique[^}]}}": ur"(Botanique)",
            "{{boucherie[^}]}}": ur"(Boucherie)",
            "{{bouddhisme[^}]}}": ur"(Bouddhisme)",
            "{{bourrellerie[^}]}}": ur"(Bourrellerie)",
            "{{bowling[^}]}}": ur"(Bowling)",
            "{{boxe[^}]}}": ur"(Boxe)",
            "{{bridge[^}]}}": ur"(Bridge)",
            "{{calendrier[^}]}}": ur"(Calendrier)",
            "{{calligraphie[^}]}}": ur"(Calligraphie)",
            "{{canoë-kayak[^}]}}": ur"(Canoë-kayak)",
            "{{capoeira[^}]}}": ur"(Capoeira)",
            "{{cartes[^}]}}": ur"(Cartes)",
            "{{cartographie[^}]}}": ur"(Cartographie)",
            "{{caséologie[^}]}}": ur"(Caséologie)",
            "{{catch[^}]}}": ur"(Catch)",
            "{{CB[^}]}}": ur"(CB)",
            "{{céramique[^}]}}": ur"(Céramique)",
            "{{charpenterie[^}]}}": ur"(Charpenterie)",
            "{{charronnerie[^}]}}": ur"(Charronnerie)",
            "{{chasse[^}]}}": ur"(Chasse)",
            "{{chimie[^}]}}": ur"(Chimie)",
            "{{chiromancie[^}]}}": ur"(Chiromancie)",
            "{{chirurgie[^}]}}": ur"(Chirurgie)",
            "{{christianisme[^}]}}": ur"(Christianisme)",
            "{{chronologie[^}]}}": ur"(Chronologie)",
            "{{cinéma[^}]}}": ur"(Cinéma)",
            "{{cirque[^}]}}": ur"(Cirque)",
            "{{climatologie[^}]}}": ur"(Climatologie)",
            "{{coiffure[^}]}}": ur"(Coiffure)",
            "{{colorimétrie[^}]}}": ur"(Colorimétrie)",
            "{{commerce[^}]}}": ur"(Commerce)",
            "{{comptabilité[^}]}}": ur"(Comptabilité)",
            "{{construction[^}]}}": ur"(Construction)",
            "{{copropriété[^}]}}": ur"(Copropriété)",
            "{{cordonnerie[^}]}}": ur"(Cordonnerie)",
            "{{cosmétologie[^}]}}": ur"(Cosmétologie)",
            "{{couche application[^}]}}": ur"(Couche application)",
            "{{couche liaison[^}]}}": ur"(Couche liaison)",
            "{{couche physique[^}]}}": ur"(Couche physique)",
            "{{couche présentation[^}]}}": ur"(Couche présentation)",
            "{{couche réseau[^}]}}": ur"(Couche réseau)",
            "{{couche session[^}]}}": ur"(Couche session)",
            "{{couche transport[^}]}}": ur"(Couche transport)",
            "{{course à pied[^}]}}": ur"(Course à pied)",
            "{{couture[^}]}}": ur"(Couture)",
            "{{cricket[^}]}}": ur"(Cricket)",
            "{{cryptographie[^}]}}": ur"(Cryptographie)",
            "{{cryptomonnaie[^}]}}": ur"(Cryptomonnaie)",
            "{{cuisine[^}]}}": ur"(Cuisine)",
            "{{cyclisme[^}]}}": ur"(Cyclisme)",
            "{{dames[^}]}}": ur"(Dames)",
            "{{danse[^}]}}": ur"(Danse)",
            "{{dentisterie[^}]}}": ur"(Dentisterie)",
            "{{dermatologie[^}]}}": ur"(Dermatologie)", 
            "{{dessin[^}]}}": ur"(Dessin)",
            "{{didactique[^}]}}": ur"(Didactique)",
            "{{diplomatie[^}]}}": ur"(Diplomatie)",
            "{{drogue[^}]}}": ur"(Drogue)",
            "{{droit[^}]}}": ur"(Droit)",
            "{{échafaudage[^}]}}": ur"(Échafaudage)",
            "{{échecs[^}]}}": ur"(Échecs)",
            "{{écologie[^}]}}": ur"(Écologie)",
            "{{économie[^}]}}": ur"(Économie)",
            "{{édition[^}]}}": ur"(Édition)",
            "{{éducation[^}]}}": ur"(Éducation)",
            "{{électoraux[^}]}}": ur"(Électoraux)",
            "{{électricité[^}]}}": ur"(Électricité)",
            "{{électronique[^}]}}": ur"(Électronique)",
            "{{électrotechnique[^}]}}": ur"(Électrotechnique)",
            "{{élevage[^}]}}": ur"(Élevage)",
            "{{embryologie[^}]}}": ur"(Embryologie)",
            "{{entomologie[^}]}}": ur"(Entomologie)",
            "{{équitation[^}]}}": ur"(Équitation)",
            "{{escrime[^}]}}": ur"(Escrime)",
            "{{ethnobiologie[^}]}}": ur"(Ethnobiologie)",
            "{{ethnologie[^}]}}": ur"(Ethnologie)",
            "{{famille[^}]}}": ur"(Famille)",
            "{{fantastique[^}]}}": ur"(Fantastique)",
            "{{fauconnerie[^}]}}": ur"(Fauconnerie)",
            "{{ferroviaire[^}]}}": ur"(Ferroviaire)",
            "{{finance[^}]}}": ur"(Finance)",
            "{{fiscalité[^}]}}": ur"(Fiscalité)",
            "{{fontainerie[^}]}}": ur"(Fontainerie)",
            "{{football[^}]}}": ur"(Football)",
            "{{foresterie[^}]}}": ur"(Foresterie)",
            "{{franc-maçonnerie[^}]}}": ur"(Franc-maçonnerie)",
            "{{généalogie[^}]}}": ur"(Généalogie)",
            "{{génétique[^}]}}": ur"(Génétique)",
            "{{géographie[^}]}}": ur"(Géographie)",
            "{{géologie[^}]}}": ur"(Géologie)",
            "{{géomatique[^}]}}": ur"(Géomatique)",
            "{{géométrie[^}]}}": ur"(Géométrie)", 
            "{{géophysique[^}]}}": ur"(Géophysique)",
            "{{géostatistique[^}]}}": ur"(Géostatistique)",
            "{{glaciologie[^}]}}": ur"(Glaciologie)",
            "{{golf[^}]}}": ur"(Golf)",
            "{{grammaire[^}]}}": ur"(Grammaire)",
            "{{gravure[^}]}}": ur"(Gravure)",
            "{{gymnastique[^}]}}": ur"(Gymnastique)",
            "{{handball[^}]}}": ur"(Handball)",
            "{{handisport[^}]}}": ur"(Handisport)",
            "{{héraldique[^}]}}": ur"(Héraldique)", 
            "{{hindouisme[^}]}}": ur"(Hindouisme)",
            "{{hippisme[^}]}}": ur"(Hippisme)",
            "{{hippologie[^}]}}": ur"(Hippologie)",
            "{{histoire[^}]}}": ur"(Histoire)",
            "{{histologie[^}]}}": ur"(Histologie)",
            "{{hockey[^}]}}": ur"(Hockey)",
            "{{horlogerie[^}]}}": ur"(Horlogerie)",
            "{{horticulture[^}]}}": ur"(Horticulture)",
            "{{hydraulique[^}]}}": ur"(Hydraulique)",
            "{{hydrobiologie[^}]}}": ur"(Hydrobiologie)",
            "{{hydrologie[^}]}}": ur"(Hydrologie)",
            "{{hygiène[^}]}}": ur"(Hygiène)",
            "{{ichtyologie[^}]}}": ur"(Ichtyologie)",
            "{{illégalité[^}]}}": ur"(Illégalité)",
            "{{imprimerie[^}]}}": ur"(Imprimerie)",
            "{{industrie[^}]}}": ur"(Industrie)",
            "{{infographie[^}]}}": ur"(Infographie)",
            "{{informatique[^}]}}": ur"(Informatique)",
            "{{intelligence artificielle[^}]}}": ur"(Intelligence artificielle)",
            "{{internet[^}]}}": ur"(Internet)",
            "{{islam[^}]}}": ur"(Islam)",
            "{{jardinage[^}]}}": ur"(Jardinage)",
            "{{jazz[^}]}}": ur"(Jazz)",
            "{{jeu de go[^}]}}": ur"(Jeu de go)",
            "{{jeu de paume[^}]}}": ur"(Jeu de paume)",
            "{{jeux[^}]}}": ur"(Jeux)",
            "{{jeux vidéo[^}]}}": ur"(Jeux vidéo)",
            "{{jonglerie[^}]}}": ur"(Jonglerie)",
            "{{journalisme[^}]}}": ur"(Journalisme)",
            "{{judaïsme[^}]}}": ur"(Judaïsme)",
            "{{judo[^}]}}": ur"(Judo)",
            "{{justice[^}]}}": ur"(Justice)",
            "{{karaté[^}]}}": ur"(Karaté)",
            "{{langage Java[^}]}}": ur"(Langage Java)",
            "{{législation[^}]}}": ur"(Législation)",
            "{{lexicographie[^}]}}": ur"(Lexicographie)",
            "{{LGBT[^}]}}": ur"(LGBT)",
            "{{linguistique[^}]}}": ur"(Linguistique)",
            "{{littérature[^}]}}": ur"(Littérature)",
            "{{liturgie[^}]}}": ur"(Liturgie)",
            "{{livre[^}]}}": ur"(Livre)",
            "{{logique[^}]}}": ur"(Logique)",
            "{{logistique[^}]}}": ur"(Logistique)",
            "{{loisirs[^}]}}": ur"(Loisirs)",
            "{{lutherie[^}]}}": ur"(Lutherie)",
            "{{maçonnerie[^}]}}": ur"(Maçonnerie)",
            "{{magnétisme[^}]}}": ur"(Magnétisme)",
            "{{mah-jong[^}]}}": ur"(Mah-jong)",
            "{{maintenance[^}]}}": ur"(Maintenance)",
            "{{marbrerie[^}]}}": ur"(Marbrerie)",
            "{{maréchalerie[^}]}}": ur"(Maréchalerie)",
            "{{marine[^}]}}": ur"(Marine)",
            "{{maroquinerie[^}]}}": ur"(Maroquinerie)",
            "{{mathématiques[^}]}}": ur"(Mathématiques)",
            "{{mécanique[^}]}}": ur"(Mécanique)",
            "{{médecine[^}]}}": ur"(Médecine)",
            "{{médecine non conv[^}]}}": ur"(Médecine non conv)",
            "{{médecine vétérinaire[^}]}}": ur"(Médecine vétérinaire)",
            "{{média[^}]}}": ur"(Média)",
            "{{menuiserie[^}]}}": ur"(Menuiserie)", 
            "{{mercatique[^}]}}": ur"(Mercatique)",
            "{{metal[^}]}}": ur"(Metal)",
            "{{métallurgie[^}]}}": ur"(Métallurgie)",
            "{{météorologie[^}]}}": ur"(Météorologie)",
            "{{métrologie[^}]}}": ur"(Métrologie)",
            "{{meunerie[^}]}}": ur"(Meunerie)",
            "{{microbiologie[^}]}}": ur"(Microbiologie)",
            "{{militaire[^}]}}": ur"(Militaire)",
            "{{minéralogie[^}]}}": ur"(Minéralogie)",
            "{{miroiterie[^}]}}": ur"(Miroiterie)",
            "{{monarchie[^}]}}": ur"(Monarchie)",
            "{{morphologie végétale[^}]}}": ur"(Morphologie végétale)",
            "{{motocyclisme[^}]}}": ur"(Motocyclisme)",
            "{{Moyen Âge[^}]}}": ur"(Moyen Âge)",
            "{{muscle[^}]}}": ur"(Muscle)",
            "{{musculation[^}]}}": ur"(Musculation)",
            "{{muséologie[^}]}}": ur"(Muséologie)",
            "{{musique[^}]}}": ur"(Musique)",
            "{{mycologie[^}]}}": ur"(Mycologie)",
            "{{mythologie[^}]}}": ur"(Mythologie)",
            "{{narratologie[^}]}}": ur"(Narratologie)",
            "{{natation[^}]}}": ur"(Natation)",
            "{{navigation[^}]}}": ur"(Navigation)",
            "{{neurologie[^}]}}": ur"(Neurologie)",
            "{{noblesse[^}]}}": ur"(Noblesse)",
            "{{nosologie[^}]}}": ur"(Nosologie)",
            "{{novlangue[^}]}}": ur"(Novlangue)",
            "{{nucléaire[^}]}}": ur"(Nucléaire)",
            "{{numismatique[^}]}}": ur"(Numismatique)",
            "{{nutrition[^}]}}": ur"(Nutrition)",
            "{{occultisme[^}]}}": ur"(Occultisme)",
            "{{océanographie[^}]}}": ur"(Océanographie)",
            "{{œnologie[^}]}}": ur"(Œnologie)",
            "{{optimisation[^}]}}": ur"(Optimisation)",
            "{{optique[^}]}}": ur"(Optique)",
            "{{orgues[^}]}}": ur"(Orgues)",
            "{{ornement[^}]}}": ur"(Ornement)",
            "{{ornithologie[^}]}}": ur"(Ornithologie)",
            "{{paléographie[^}]}}": ur"(Paléographie)",
            "{{paléontologie[^}]}}": ur"(Paléontologie)",
            "{{papeterie[^}]}}": ur"(Papeterie)",
            "{{patinage[^}]}}": ur"(Patinage)",
            "{{pâtisserie[^}]}}": ur"(Pâtisserie)",
            "{{pêche[^}]}}": ur"(Pêche)",
            "{{pédologie[^}]}}": ur"(Pédologie)",
            "{{peinture[^}]}}": ur"(Peinture)",
            "{{pelote[^}]}}": ur"(Pelote)",
            "{{pétanque[^}]}}": ur"(Pétanque)",
            "{{pétrochimie[^}]}}": ur"(Pétrochimie)",
            "{{pharmacologie[^}]}}": ur"(Pharmacologie)",
            "{{phénologie[^}]}}": ur"(Phénologie)",
            "{{phénoménologie[^}]}}": ur"(Phénoménologie)",
            "{{philatélie[^}]}}": ur"(Philatélie)",
            "{{philosophie[^}]}}": ur"(Philosophie)",
            "{{phonétique[^}]}}": ur"(Phonétique)",
            "{{phonologie[^}]}}": ur"(Phonologie)",
            "{{photographie[^}]}}": ur"(Photographie)",
            "{{physiologie[^}]}}": ur"(Physiologie)",
            "{{physique[^}]}}": ur"(Physique)",
            "{{phytosociologie[^}]}}": ur"(Phytosociologie)",
            "{{planche à neige[^}]}}": ur"(Planche à neige)",
            "{{planche à roulettes[^}]}}": ur"(Planche à roulettes)",
            "{{plomberie[^}]}}": ur"(Plomberie)",
            "{{plongée[^}]}}": ur"(Plongée)",
            "{{poésie[^}]}}": ur"(Poésie)",
            "{{poker[^}]}}": ur"(Poker)",
            "{{police[^}]}}": ur"(Police)",
            "{{politique[^}]}}": ur"(Politique)",
            "{{préhistoire[^}]}}": ur"(Préhistoire)",
            "{{prestidigitation[^}]}}": ur"(Prestidigitation)",
            "{{probabilités[^}]}}": ur"(Probabilités)",
            "{{programmation[^}]}}": ur"(Programmation)",
            "{{programmation orientée objet[^}]}}": ur"(Programmation orientée objet)",
            "{{propriété[^}]}}": ur"(Propriété)",
            "{{psychanalyse[^}]}}": ur"(Psychanalyse)",
            "{{psychiatrie[^}]}}": ur"(Psychiatrie)",
            "{{psychologie[^}]}}": ur"(Psychologie)",
            "{{pyrotechnie[^}]}}": ur"(Pyrotechnie)",
            "{{raffinage[^}]}}": ur"(Raffinage)",
            "{{regex[^}]}}": ur"(Regex)",
            "{{relations internationales[^}]}}": ur"(Relations internationales)",
            "{{religion[^}]}}": ur"(Religion)",
            "{{reliure[^}]}}": ur"(Reliure)",
            "{{renseignement[^}]}}": ur"(Renseignement)",
            "{{reproduction[^}]}}": ur"(Reproduction)",
            "{{réseaux informatiques[^}]}}": ur"(Réseaux informatiques)",
            "{{rhétorique[^}]}}": ur"(Rhétorique)",
            "{{robotique[^}]}}": ur"(Robotique)",
            "{{rugby[^}]}}": ur"(Rugby)",
            "{{saliculture[^}]}}": ur"(Saliculture)",
            "{{saut en hauteur[^}]}}": ur"(Saut en hauteur)",
            "{{science-fiction[^}]}}": ur"(Science-fiction)",
            "{{sciences[^}]}}": ur"(Sciences)",
            "{{Scrabble[^}]}}": ur"(Scrabble)",
            "{{sculpture[^}]}}": ur"(Sculpture)",
            "{{serrurerie[^}]}}": ur"(Serrurerie)",
            "{{sexualité[^}]}}": ur"(Sexualité)",
            "{{sidérurgie[^}]}}": ur"(Sidérurgie)",
            "{{ski alpin[^}]}}": ur"(Ski alpin)",
            "{{ski de fond[^}]}}": ur"(Ski de fond)",
            "{{snowboard[^}]}}": ur"(Snowboard)",
            "{{socialisme[^}]}}": ur"(Socialisme)",
            "{{sociolinguistique[^}]}}": ur"(Sociolinguistique)",
            "{{sociologie[^}]}}": ur"(Sociologie)",
            "{{sport[^}]}}": ur"(Sport)",
            "{{squelette[^}]}}": ur"(Squelette)",
            "{{statistiques[^}]}}": ur"(Statistiques)",
            "{{stéréochimie[^}]}}": ur"(Stéréochimie)",
            "{{stéréotomie[^}]}}": ur"(Stéréotomie)",
            "{{stéréotype[^}]}}": ur"(Stéréotype)",
            "{{surf[^}]}}": ur"(Surf)",
            "{{sylviculture[^}]}}": ur"(Sylviculture)",
            "{{taille de pierre[^}]}}": ur"(Taille de pierre)",
            "{{tauromachie[^}]}}": ur"(Tauromachie)",
            "{{technique[^}]}}": ur"(Technique)",
            "{{technologie[^}]}}": ur"(Technologie)",
            "{{télécommunications[^}]}}": ur"(Télécommunications)",
            "{{téléinformatique[^}]}}": ur"(Téléinformatique)",
            "{{téléphonie[^}]}}": ur"(Téléphonie)",
            "{{tennis[^}]}}": ur"(Tennis)",
            "{{tennis de table[^}]}}": ur"(Tennis de table)",
            "{{tératologie[^}]}}": ur"(Tératologie)",
            "{{textile[^}]}}": ur"(Textile)",
            "{{théâtre[^}]}}": ur"(Théâtre)",
            "{{théologie[^}]}}": ur"(Théologie)",
            "{{théorie des graphes[^}]}}": ur"(Théorie des graphes)",
            "{{thermodynamique[^}]}}": ur"(Thermodynamique)",
            "{{tonnellerie[^}]}}": ur"(Tonnellerie)",
            "{{topographie[^}]}}": ur"(Topographie)",
            "{{topologie[^}]}}": ur"(Topologie)",
            "{{toponymie[^}]}}": ur"(Toponymie)",
            "{{tourisme[^}]}}": ur"(Tourisme)",
            "{{transport[^}]}}": ur"(Transport)",
            "{{travail[^}]}}": ur"(Travail)",
            "{{triathlon[^}]}}": ur"(Triathlon)",
            "{{typographie[^}]}}": ur"(Typographie)",
            "{{ufologie[^}]}}": ur"(Ufologie)",
            "{{urbanisme[^}]}}": ur"(Urbanisme)",
            "{{usinage[^}]}}": ur"(Usinage)",
            "{{vaudou[^}]}}": ur"(Vaudou)",
            "{{versification[^}]}}": ur"(Versification)",
            "{{vexillologie[^}]}}": ur"(Vexillologie)",
            "{{virologie[^}]}}": ur"(Virologie)",
            "{{viticulture[^}]}}": ur"(Viticulture)",
            "{{vitrerie[^}]}}": ur"(Vitrerie)",
            "{{volley-ball[^}]}}": ur"(Volley-ball)",
            "{{wiki[^}]}}": ur"(Wiki)",
            "{{yoga[^}]}}": ur"(Yoga)",
            "{{zoologie[^}]}}": ur"(Zoologie)"
	}
        self.temporalites = {
            "{{vieilli[^}]*}}": ur"(Vieilli)",
            "{{archaïsme[^}]*}}": ur"(Archaïsme)",
            "{{désuet[^}]*}}": ur"(Désuet)",
            "{{néologisme[^}]*}}": ur"(Néologisme)"
            }
        self.frequence = {
            "{{courant[^}]*}}": ur"(Courant)",
            "{{peu usité[^}]*}}": ur"(Peu usité)",
            "{{rare[^}]*}}": ur"(Rare)",
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
        # These definitions will always be skipped
        self.filterDefinitionType = [ ur"{{vulg[^}]*}}",
                                      ur"{{injur[^}]*}}",
                                      ur"{{sexe[^}]*}}",
                                      ur"{{sexua[^}]*}}",
                                      ur"coït",
                                      ur"argot"]

        # These definitions will be skipped only if not in the first
        # sense found
        self.filterSecondDefinitionType = [
                                      ur"{{dés[^}]*}}",
                                      ur"{{vx[^}]*}}",
                                      ur"{{métonymie[^}]*}}",
                                      ur"{{familier[^}]*}}",
                                      ur"{{hérald[^}]*}}",
                                      ur"{{botan[^}]*}}",
                                      ur"{{zool[^}]*}}",
                                      ur"{{polit[^}]*}",
                                      ur"{{péj[^}]*}}",
                                      ur"{{oeno[^}]*}}",
                                      ur"{{litt[^}]*}}",
#                                      ur"{{par ext[^}]*}}",
                                      ur"{{figuré[^}]*}}"
                                      ]

    def endElement(self, name):
        if name == 'page':
            global compteur
            self.isPageElement= False
            if self.titleContent in self.searchWords:
                word = self.parseText()
                if word and word.name:
                    #Remove words with space (expression for example). Keep words with accent thanks to re.UNICODE trick
                    matching_titleContent_whitespace = re.match(".* .*",self.titleContent, re.UNICODE)
                    #Remove words with digit in it
                    matching_titleContent_number = re.match("\d",self.titleContent)
                if len(self.titleContent) > 1 and matching_titleContent_whitespace is None and matching_titleContent_number is None and toAdd == True:
                    self.wiktio.addWord(word)
                    compteur = compteur + 1
                    global compteurMax
                    if compteur == compteurMax:
                        raise EndOfParsing
            self.titleContent = ""
            self.textContent = ""
        elif name == 'title':
            self.isTitleElement= False
        elif name == 'text':
            self.isTextElement = False

    def characters (self, ch):
        if self.isTitleElement:
            self.titleContent += ch
        elif self.isTextElement:
            self.textContent += ch


# Manages bullets and numbered lists
# mediawiki specification:
# Bulleted: *
# Numbered: #
# Indent with no marking: :
# Definition list: ;
# Notes:
# These may be combined at the start of the line to create
# nested lists, e.g. *** to give a bulleted list three levels
# deep, or **# to have a numbered list within two-levels of
# bulleted list nesting.
#
# html specification:
# Bulleted: <ul> [<li> </li>]+ </ul>
# Numbered: <ol> [<li> </li>]+ </ol>
# Notes:
# These may be nested.
#
# We keep the level of indentation to close in:
# self.lilevel
#
# Returns a list [text, level, numbered]
# numbered = True if this is a numbered list
#
    def indents2xml(self, text, asText):
        numbered = False
        result = re.search(r"^[ ]*[*#:;]+[ ]*", text)
        if not result:
            self.lilevel = 0
            return [text, self.lilevel, numbered]

        indent = result.group(0).rstrip()
        self.lilevel = len(indent)
        text = text[result.end():]

        if asText:
            return [text, self.lilevel, numbered]

        if indent[-1:] == "#":
            numbered = True

        return [text, self.lilevel, numbered]

    # Replaces '''xx''' and ''xx'' from the given text
    # with openXml xx closeXml
    def quote2xml(self, quote, openXml, closeXml, text):
        index = 0
        while index >= 0:
            index = text.find(quote)
            index2 = text.find(quote, index + len(quote))
            if index >= 0 and index2 >=0:
                text = text.replace(quote, openXml, 1)
                text = text.replace(quote, closeXml, 1)
            else:
                return text
        return text

    # Replace standard Wiki tags to XML
    # Returns a list [text, level, numbered]
    # numbered = True if this is a numbered list
    def wiki2xml(self, text, asText):

        text = re.sub(r"{{[-\)\(]}}", "", text)
        text = re.sub(r"\[\[\w+:\w+\]\]", "", text)
        text = re.sub(r"{{\(\|(.*)}}", r"", text)
        if text == "":
            return self.indents2xml(text, asText)

        [text, level, numbered] = self.indents2xml(text, asText)
        text = re.sub(ur"{{par ext[^}]*}}", ur"(Par extension)", text)
        text = re.sub(ur"{{figuré[^}]*}}", ur"(Figuré)", text)
        text = re.sub(ur"{{géométrie[^}]*}}", ur"(Géométrie)", text)
        text = re.sub(ur"{{w\|([^}]+)}}", ur"<i>\1</i>", text)
        #text = re.sub(ur"{{source\|([^}]+)}}", ur"- (\1)", text)
#        text = re.sub(ur"{{source\|([^}]+)}}", ur"Source :", text)
        for registreWiki in self.registres.keys():
            text = re.sub(registreWiki, self.registres[registreWiki], text)
        
        for frequenceWiki in self.frequence.keys():
            text = re.sub(frequenceWiki, self.frequence[frequenceWiki], text)
        
        for temporaliteWiki in self.temporalites.keys():
            text = re.sub(temporaliteWiki, self.temporalites[temporaliteWiki], text)

        for lexiqueWiki in self.lexique.keys():
            text = re.sub(lexiqueWiki, self.lexique[lexiqueWiki], text)
        # Remove all unrecognized wiki tags
        text = re.sub(r"{{[^}]+}}", "", text)

        # bold
        text = self.quote2xml("'''", "<b>", "</b>", text)
        # italic
        text = self.quote2xml("''", "<i>", "</i>", text)
        variable = text
        
        #Get rid of Image
        if text.startswith("[[Image") or text.startswith("[[Fichier") or text.startswith("="):
            text=""
            return [text, level, numbered]

        # Get rid of hyperlinks
        while text.find("[[") != -1:
            start = text.find("[[")
            stop = text.find("]]")
            pipe = text.find("|", start, stop)
            if pipe == -1:
                text = text.replace("[[", "", 1)
                text = text.replace("]]", "", 1)
            else:
                text = text[:start] + text[pipe+1:]
                text = text.replace("]]", "", 1)

        return [text, level, numbered]

    # Wikipedia text content is interpreted and transformed in XML
    def parseText(self):
        print "Processing " + self.titleContent
        inWord = wiktio.Word()

        global toAdd
        toAdd = False
        state = Wiktio.SKIP

        wordType = ""
        wordSubType = ""
        filterIndent = ""
        gender = ""

        for textSplitted in re.split(r"(=== {{S\|.*\|fr\|{0,1}[\w\W]*?}} ===[\w\W]*?)=== {{S", self.textContent, flags=re.M|re.UNICODE):

            #self.textContent = text
            # Append an end of text marker, it forces the end of the definition
            textSplitted += "\n{{-EndOfTest-}}"

            # Remove html comment (multilines)
            textSplitted = re.sub(r"<!--[^>]*-->", "",
                                     textSplitted, re.M)

            definition = wiktio.Definition()
            inWord.addDefinition(definition)
            concat = ""
            for l in textSplitted.splitlines():
                l = concat + l
                concat = ""
                next = False

                if re.search(r"<[^>]+$", l):
                    # Wiki uses a trick to format text area by ending in uncomplete
                    # html tags. In this case, we concat this line with the next one
                    # before processing it
                    concat = l
                    continue
                #Retrieve nature of the word in line like === {{S|wordNature|fr(|.*optional)}} ===
                matching_word_nature = re.match(r"=== {{S\|([\w\W]*?)\|fr}} ===",l,re.UNICODE)
                matching_word_nature_bis = re.match(r"=== {{S\|([\w\W]*?)\|fr\|.*}} ===",l,re.UNICODE)
                # Determine the section of the document we are in

                if l.startswith("'''" + self.titleContent + "'''"):
                    for wt in self.genders.keys():
                        if re.search(wt, l):
                            gender = self.genders[wt]
                            definition.setGender(gender)
                            break
                    inWord.setName(self.titleContent)
                    # Get rid of the word, we don't want it in the definition
                    l = re.sub(r"'''.*'''[ ]*(.*)", r"\1", l)
                    # Get rid of non wiki tags
                    l = re.sub(r'}}[^}]+{{', r'}} {{', l)
                    #state = Wiktio.DEFINITION
                    definition.addDescription("", 0, False)
                elif matching_word_nature:
                    if "flexion" not in l and matching_word_nature.group(1) in self.typesAllowed:
                        definition.setType(matching_word_nature.group(1)) 
                        state=Wiktio.DEFINITION
                        toAdd = True
                elif matching_word_nature_bis:
                    if "flexion" not in l and matching_word_nature_bis.group(1) in self.typesAllowed:
                        if self.titleContent == "énervé":
                            print matching_word_nature_bis.group(1)
                        definition.setType(matching_word_nature_bis.group(1)) 
                        state=Wiktio.DEFINITION
                        toAdd = True
                elif re.match(r"==.*{{.*}}.*==",l):
                    state=Wiktio.SKIP
                elif re.search(r"{{-.*-.*}}", l):
                    if not definition.rootDescription.isEmpty():
                       # print "  new definition:" + l + ":"
                        # Next definition
                        filterIndent = ""
                        definition = wiktio.Definition()
                        inWord.addDefinition(definition)
                    state = Wiktio.SKIP

                

                # Are we still in the correct language section
                # We assume the correct language is ahead
                lang = re.match(r"==[ ]+{{=([a-z]+)=}}[ ]+==", l)
                if lang and lang.group(1) != None and lang.group(1) != self.locale:
                    return inWord

#                for wt in self.wordTypes.keys():
 #                   if re.search(wt, l):
  #                      wordType = self.wordTypes[wt]
    #                    definition.setType(wordType)
   #                     break

                if state == Wiktio.SKIP:
                    continue

                if filterIndent != "":
                    # We are filtering, check this line is
                    # at a lower indentation level
                    result = re.search(r"^[ ]*[*#:;]+[ ]*", l)
                    if result:
                        if len(result.group(0).rstrip()) > len(filterIndent):
                            next = True
                        else:
                            filterIndent = ""
                    else:
                        filterIndent = ""


                # We already found a meaning for this word, we pick
                # other senses restrictively
                '''
                if not definition.rootDescription.isEmpty():
                    for filter in self.filterSecondDefinitionType:
                        if re.search(filter, l, re.I):
                            result = re.search(r"^[ ]*[*#:;]+[ ]*", l)
                            if result:
                                # Keep the indent level for which we filter
                                print result.group(0)
                                filterIndent = result.group(0).rstrip()
                            next = True
                            break
                '''
                if next:
                    continue

                # Categories
                if re.match(ur"\[\[Catégorie:", l):
                    text = re.sub(ur"\[\[Catégorie:([^|}\]]+).*", r"\1", l)
                    definition.add(Wiktio.CATEGORY, text)
                    continue

                if state == Wiktio.DEFINITION:
                    [text, level, numbered] = self.wiki2xml(l, False)
                    definition.addDescription(text, level, numbered)
                else:
                    if len(l) > 0:
                        definition.add(state, self.wiki2xml(l, True)[0])

        return inWord

# Set UTF-8 stdout in case of the user piping our output
reload(sys)
sys.setdefaultencoding('utf-8')

usage = "usage: %prog [options] wiktionary_dump.xml word_list.txt"
parser = OptionParser(usage=usage)
parser.add_option("-o", "--output", dest="output",
              help="write result to file or directory")
parser.add_option("-q", "--quiet",
              action="store_false", dest="verbose", default=True,
              help="don't print in progress messages to stdout")
parser.add_option("-d", "--debug",
              action="store_true", dest="debug", default=False,
              help="print debug traces to stdout")
parser.add_option("-s", "--site",
              action="store_true", dest="site", default=False,
              help="Creates a web site")
(options, args) = parser.parse_args()

if len(sys.argv) < 3:
    parser.print_help()
    sys.exit()

wikiFile = sys.argv[1]
wordsFile = sys.argv[2]

if options.site:
    if not os.path.isdir(options.output):
        print "ERROR: There must me a directory named " + options.output
        sys.exit(1)

# Import the list of words
f = open(wordsFile, "r")
words = []
words = [w.rstrip() for w in f.readlines()]
f.close()

_wiktio = wiktio.Wiktio()

try:
    parse(wikiFile, WikiHandler(words, 'fr', _wiktio, options.verbose))
except:
    print "Fin du parsing"

if options.site:
    _wiktio.dump2htmlSite(options.output)
else:
    _wiktio.dump2html(options.output)
