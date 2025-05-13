"""
Ported from lt3_java/preprocessor_java/Chunker/src/domein Java package.
Created on 2016/10/31

"""

from lets.chunker_steps.chunker_util import matches, contains
from lets.chunker_steps.jcompat import JSortedSet, JIterator, JListIterator
from lets.chunker_steps.pos_codes import PoSCodes


class Chunkers(object):
    """Chunk methods for the suported languages."""

    @classmethod
    def chunk_english(cls, sent):
        """Chunks an English sentence and returns the chunk boundaries as a sorted set.

           :param: sent: JList - a sequence of Word objects
           :return: JSortedSet - the ordered collection of chunk boundaries
        """
        boundaries = JSortedSet()
        prepBoundaries = JSortedSet()

        it2 = JIterator(sent)

        # Correct PoS errors
        while it2.hasNext():
            w = it2.next()
            # over 400: IN -> RB
            if (w.getLemma() == "over") and it2.hasNext() and sent.get(w.getPosition() + 1).getPos() == "CD":
                w.setPos("RB")
                w.setMappedPos("ADV")

            # Particles: pointed out: RB -> RP
            elif (w.getPos() == "RB" and
                        (w.getLemma() == "out" or w.getLemma() == "up" or w.getLemma() == "on" or
                         w.getLemma() == "down" or w.getLemma() == "in" or w.getLemma() == "through") and
                    w.getPosition() > 0 and sent.get(w.getPosition() - 1).getPos().startswith("V")):
                w.setPos("RP")
                w.setMappedPos("PRT")

            # TO -> IN (to citizens, to a national veto)
            elif (w.getPos() == "TO" and w.getPosition() > 0 and it2.hasNext() and
                    (sent.get(w.getPosition() + 1).getPos() == "DT" or
                     sent.get(w.getPosition() + 1).getPos().startswith("PRP") or
                     sent.get(w.getPosition() + 1).getPos().startswith("N") or
                     sent.get(w.getPosition() + 1).getPos() == "JJ")):
                w.setPos("IN")
                w.setMappedPos("PREP")

            # the fixed, the hinged, the bleed valve
            elif (w.getMappedPos().startswith("V-p") and w.getPosition() > 0 and
                    sent.get(w.getPosition() - 1).getLemma() == "the" and
                    it2.hasNext() and sent.get(w.getPosition() + 1).getMappedPos().startswith("PREP")):
                w.setPos("NN")
                w.setMappedPos("N")

            elif (w.getMappedPos().startswith("V-p") and w.getPosition() > 0 and
                    sent.get(w.getPosition() - 1).getLemma() == "the"):
                w.setPos("JJ")
                w.setMappedPos("ADJ")

            # the tap
            elif (w.getMappedPos().startswith("V") and w.getPosition() > 0 and
                    sent.get(w.getPosition() - 1).getLemma() == "the"):
                w.setPos("NN")
                w.setMappedPos("N")

        it = JIterator(sent)
        while it.hasNext():
            w = it.next()

            # boundary before and after punctuation mark or coordinating conjunction or existential there
            if w.getPos() == "CC" or w.getPos() == "EX":
                boundaries.add(w.getPosition())
                boundaries.add(w.getPosition() - 1)

            # boundary before and after punctuation marks
            elif w.getMappedPos().startswith("PCT") or w.getMappedPos() == "SYM":
                boundaries.add(w.getPosition())
                boundaries.add(w.getPosition() - 1)

            # before "TO"
            elif w.getPos() == "TO":
                boundaries.add(w.getPosition() - 1)

            # before modal auxiliary
            elif w.getPos() == "MD":
                boundaries.add(w.getPosition() - 1)
                if it.hasNext() and sent.get(w.getPosition() + 1).getPos() == "RB":
                    boundaries.add(w.getPosition())

            # before personal pronoun or wh-word not preceded by preposition, e.g. "with them"
            elif ((w.getPos() == "PRP" or w.getPos().startswith("W")) and
                    w.getPosition() > 0 and
                    not (sent.get(w.getPosition() - 1).getPos() == "IN") and
                    not (sent.get(w.getPosition() - 1).getPos() == "TO")):
                boundaries.add(w.getPosition() - 1)

            # before a preposition
            elif w.getPos() == "IN" and it.hasNext():
                boundaries.add(w.getPosition() - 1)

            # before a verb not preceded by TO or other verb or IN
            elif (w.getPos().startswith("V") and w.getPosition() > 0 and
                    not (sent.get(w.getPosition() - 1).getPos() == "TO") and
                    not (sent.get(w.getPosition() - 1).getPos() == "IN") and
                    not (sent.get(w.getPosition() - 1).getPos() == "MD") and
                    not (sent.get(w.getPosition() - 1).getPos().startswith("V"))):
                boundaries.add(w.getPosition() - 1)

            # before determiner/possessive pronoun not preceded by preposition or (pre)determiner
            elif (((w.getPos() == "DT" or w.getPos() == "PRP$")) and w.getPosition() > 0 and
                    not (sent.get(w.getPosition() - 1).getPos() == "IN") and
                    not (sent.get(w.getPosition() - 1).getPos().endswith("DT")) and
                    not (sent.get(w.getPosition() - 1).getPos() == "TO")):
                boundaries.add(w.getPosition() - 1)

            # before an adverb preceded by a verb and followed by an adjective/CD
            elif (w.getPos().startswith("RB") and it.hasNext() and
                    sent.get(w.getPosition() + 1).getPos().startswith("JJ") and
                    w.getPosition() > 0 and sent.get(w.getPosition() - 1).getPos().startswith("V")):
                boundaries.add(w.getPosition() - 1)

            # before an adverb preceded by a ((pro)noun or wh-word or determiner  or modal auxiliary and followed by (modal) verb
            #else if (w.getPos().startsWith("RB") && it.hasNext() && (sent.get(w.getPosition()+1).getPos().startsWith("V") || sent.get(w.getPosition()+1).getPos().equals("MD")) &&
            #        w.getPosition() > 0 && (sent.get(w.getPosition()-1).getPos().startsWith("N") || sent.get(w.getPosition()-1).getPos().equals("DT") || sent.get(w.getPosition()-1).getPos().equals("PRP") || sent.get(w.getPosition()-1).getPos().startsWith("W")))
            #        boundaries.add(w.getPosition()-1);

            elif (w.getPos() == "RB" and it.hasNext() and
                    (sent.get(w.getPosition() + 1).getPos().startswith("V") or
                     sent.get(w.getPosition() + 1).getPos() == "MD") and
                  w.getPosition() > 0 and
                  (sent.get(w.getPosition() - 1).getPos().startswith("N") or
                   sent.get(w.getPosition() - 1).getPos() == "DT" or
                   sent.get(w.getPosition() - 1).getPos() == "PRP" or
                   sent.get(w.getPosition() - 1).getPos().startswith("W") or
                   sent.get(w.getPosition() - 1).getPos() == "MD")):
                boundaries.add(w.getPosition() - 1)

            # between an adverb and a verb
            if w.getPos() == "RB" and it.hasNext() and sent.get(w.getPosition() + 1).getPos().startswith("V"):
                boundaries.add(w.getPosition())

            # after verb not followed by a verb or particle
            elif (w.getPos().startswith("V") and it.hasNext() and
                    not sent.get(w.getPosition() + 1).getPos() == "RP" and
                    not sent.get(w.getPosition() + 1).getPos().startswith("V") and
                    not sent.get(w.getPosition() + 1).getToken() == "n't"):
                boundaries.add(w.getPosition())

            # between a past en present participle
            # e.g. will be screened | using ...
            elif ((w.getPos() == "VBD" or w.getPos() == "VBN") and not w.getLemma() == "be" and it.hasNext() and
                  sent.get(w.getPosition() + 1).getPos() == "VBG"):
                boundaries.add(w.getPosition())

            # after a particle or Wh-determiner or wh-adverb
            if w.getPos() == "RP" or w.getPos() == "WDT" or w.getPos() == "WRB":
                boundaries.add(w.getPosition())

            # between ((pro)noun or wh-word or determiner and (modal) verb
            elif ((w.getPos()[0] == 'N' or w.getPos() == "PRP" or w.getPos()[0] == 'W' or w.getPos() == "DT") and
                    it.hasNext() and (sent.get(w.getPosition() + 1).getPos()[0] == 'V' or
                                      sent.get(w.getPosition() + 1).getPos() == "MD")):
                boundaries.add(w.getPosition())

            # In questions: between modal verb and noun/determiner/
            elif (w.getPos() == "MD" and
                    it.hasNext() and (sent.get(w.getPosition() + 1).getPos().startswith("N") or
                                      sent.get(w.getPosition() + 1).getPos().endswith("DT") or
                                      sent.get(w.getPosition() + 1).getPos() == "PRP" or
                                      sent.get(w.getPosition() + 1).getPos().startswith("W"))):
                boundaries.add(w.getPosition())

            # between noun/adjective and adverb
            elif ((w.getPos().startswith("J") or w.getPos().startswith("N")) and it.hasNext() and
                    sent.get(w.getPosition() + 1).getPos().startswith("RB")):
                boundaries.add(w.getPosition())

            # between noun & adjective followed by preposition
            elif (w.getPos().startswith("N") and it.hasNext() and
                  sent.get(w.getPosition() + 1).getPos().startswith("J") and
                  (w.getPosition() + 2 < len(sent)) and sent.get(w.getPosition() + 2).getPos() == "IN"):
                boundaries.add(w.getPosition())

            # between two verb forms (past - present/past)
            elif (w.getPos().startswith("V") and
                    it.hasNext() and (sent.get(w.getPosition() + 1).getPos() == "VBZ" or
                                      sent.get(w.getPosition() + 1).getPos() == "MD")):
                boundaries.add(w.getPosition())

            # after "such as"
            elif (w.getToken().lower() == "as".lower() and w.getPosition() > 0 and
                    sent.get(w.getPosition() - 1).getToken().lower() == "such".lower()):
                boundaries.add(w.getPosition())
                if boundaries.contains(w.getPosition() - 1):
                    boundaries.remove(w.getPosition() - 1)

            # between subordinating conjunctions and (determiner) + (pro)noun
            # if preceded by verb, punctuation or start of sentence
            elif (PoSCodes.ENGLISH_SUBORD.contains(w.getToken().lower()) and w.getPos() == "IN" and
                    it.hasNext() and (sent.get(w.getPosition() + 1).getPos() == "DT" or
                                    sent.get(w.getPosition() + 1).getPos().startswith("PRP") or
                                    sent.get(w.getPosition() + 1).getPos().startswith("N") or
                                    sent.get(w.getPosition() + 1).getPos().startswith("NJ") or
                                    sent.get(w.getPosition() + 1).getPos() == "CD")):
                boundaries.add(w.getPosition())
                boundaries.add(w.getPosition() - 1)

            # between subordinating conjunctions and adverb
            elif (PoSCodes.ENGLISH_SUBORD.contains(w.getToken().lower()) and w.getPos() == "IN" and
                    it.hasNext() and sent.get(w.getPosition() + 1).getPos().startswith("RB")):
                boundaries.add(w.getPosition())
                boundaries.add(w.getPosition() - 1)

            # boundary after preposition
            elif (w.getPos() == "IN" and it.hasNext() and not sent.get(w.getPosition() + 1).getPos() == "VBG"):
                prepBoundaries.add(w.getPosition())

        it = JIterator(sent)
        while it.hasNext():
            w = it.next()

            if w.getMappedPos() == "DET" or w.getMappedPos() == "PRON-pos":
                boundaries.remove(w.getPosition())

            # Remove boundaries if VBN or VBG functions as adjective
            # not before VBG or VN functioning as adjective
            elif ((w.getPos() == "VBG" or w.getPos() == "VBN") and w.getPosition() > 0 and
                    (sent.get(w.getPosition() - 1).getPos().endswith("DT") or
                     sent.get(w.getPosition() - 1).getPos() == "PRP$") and
                     it.hasNext() and (sent.get(w.getPosition() + 1).getPos().startswith("N") or
                                       sent.get(w.getPosition() + 1).getPos() == "CD" or
                                       sent.get(w.getPosition() + 1).getPos() == "JJ")):
                boundaries.remove(w.getPosition() - 1)
                boundaries.remove(w.getPosition())

            # past and present participle if preceded by (pre)determiner or possessive pronoun + adverb and followed by N
            elif ((w.getPos() == "VBG" or w.getPos() == "VBN") and w.getPosition() > 1 and
                    sent.get(w.getPosition() - 1).getPos() == "RB" and
                        (sent.get(w.getPosition() - 2).getPos().endswith("DT") or
                         sent.get(w.getPosition() - 2).getPos() == "PRP$") and
                    it.hasNext() and sent.get(w.getPosition() + 1).getPos().startswith("N")):
                boundaries.remove(w.getPosition() - 1)
                boundaries.remove(w.getPosition())

            # past participle if preceded by preposition and followed by N
            # IN VNB N
            elif ((w.getPos() == "VBN") and w.getPosition() > 0 and
                    (sent.get(w.getPosition() - 1).getPos() == "IN") and
                    it.hasNext() and sent.get(w.getPosition() + 1).getPos().startswith("N")):
                boundaries.remove(w.getPosition() - 1)
                boundaries.remove(w.getPosition())

            #    NN CC VBN NN
            # IN NN CC VBD NN
            #
            elif ((w.getPos() == "VBN" or w.getPos() == "VBD") and w.getPosition() > 1 and
                    sent.get(w.getPosition() - 1).getPos() == "CC" and
                    sent.get(w.getPosition() - 2).getPos().startswith("N") and
                    it.hasNext() and sent.get(w.getPosition() + 1).getPos().startswith("N")):
                boundaries.remove(w.getPosition())

            elif ((w.getPos() == "VBN") and w.getPosition() > 1 and
                    sent.get(w.getPosition() - 1).getPos() == "," and
                    (sent.get(w.getPosition() - 2).getPos().startswith("N")) and
                    it.hasNext() and sent.get(w.getPosition() + 1).getPos().startswith("N")):
                boundaries.remove(w.getPosition())

            # remove boundaries at "&", e.g. Sales & Customer Service
            elif w.getToken() == "&":
                boundaries.remove(w.getPosition() - 1)
                boundaries.remove(w.getPosition())

        # remove prepBoundary before adjective (not part of PP, e.g. in particular, as possible, ...)
        itb = JListIterator(prepBoundaries)
        while itb.hasNext():
            b = itb.next()
            phrase = "{} {}".format(sent.get(b).getLemma(), sent.get(b + 1).getLemma())
            if (boundaries.contains(b + 1) and
                    phrase in ('as possible', 'in particular', 'as such', 'of course', 'at last', 'at least')):
                itb.remove()

        # add boundary at end of sentence
        boundaries.add(len(sent) - 1)
        # print boundaries -> enable to print boundaries

        # to test impact prepboundaries
        boundaries.addAll(prepBoundaries)
        # remove "-1" from boundaries
        boundaries.remove(-1)
        return boundaries

    @classmethod
    def chunk_dutch(cls, sent):
        """Chunks a dutch sentence and returns the chunk boundaries as a sorted set.

           :param: sent: JList - a sequence of Word objects
           :return: JSortedSet - the ordered collection of chunk boundaries
        """
        boundaries = JSortedSet()
        prepBoundaries = JSortedSet()

        it2 = JIterator(sent)
        # Correct PoS errors
        while it2.hasNext():
            w = it2.next()
            if matches("^[0-9]+$", w.getToken()):
                w.setPos("TW(hoofd)")
                w.setMappedPos("NUM")

            elif (w.getLemma() == "het" and w.getPosition() == 0 and
                    it2.hasNext() and (sent.get(w.getPosition() + 1).getPos().startswith("SPEC") or
                                       sent.get(w.getPosition() + 1).getPos().startswith("N"))):
                w.setPos("LID(bep,stan,evon)")
                w.setMappedPos("DET")

            # het evenaren van
            elif (w.getLemma() == "het" and it2.hasNext() and
                    sent.get(w.getPosition() + 1).getPos().startswith("WW(inf") and
                    w.getPosition() + 2 < len(sent) and sent.get(w.getPosition() + 2).getLemma() == "van"):
                w.setPos("LID(bep,stan,evon)")
                w.setMappedPos("DET")
                sent.get(w.getPosition() + 1).setMappedPos("N")

            # het louter aanleveren van: NOK
            elif (w.getLemma() == "het" and w.getPosition() + 3 < len(sent) and
                        (sent.get(w.getPosition() + 1).getPos().startswith("BW") or
                         sent.get(w.getPosition() + 1).getPos().startswith("ADJ")) and
                    sent.get(w.getPosition() + 2).getPos().startswith("WW(inf") and
                    sent.get(w.getPosition() + 3).getLemma() == "van"):
                w.setPos("LID(bep,stan,evon)")
                w.setMappedPos("DET")
                sent.get(w.getPosition() + 2).setMappedPos("N")

            elif (w.getLemma() == "het" and
                    it2.hasNext() and sent.get(w.getPosition() + 1).getMappedPos() == "JJ" and
                    w.getPosition() + 2 < len(sent) and
                    sent.get(w.getPosition() + 2).getMappedPos().startswith("N")):
                w.setPos("LID(bep,stan,evon)")
                w.setMappedPos("DET")

        it = JIterator(sent)
        while it.hasNext():
            w = it.next()

            #    boundary before and after punctuation mark
            # "-" only if not followed by "en" or not preceded and followed by digits
            if PoSCodes.DUTCH_PUNCT.contains(w.getLemma()):
                boundaries.add(w.getPosition())
                boundaries.add(w.getPosition() - 1)

            # boundary before and after coordinating conjunctions
            elif w.getPos().startswith("VG"):
                boundaries.add(w.getPosition())
                boundaries.add(w.getPosition() - 1)

            # before an article or other determiner not preceded by a preposition or another determiner
            elif ((w.getPos().startswith("LID") or contains(",det,", w.getPos())) and w.getPosition() > 0 and
                    not sent.get(w.getPosition() - 1).getPos().startswith("VZ") and
                    not contains(",det,", sent.get(w.getPosition() - 1).getPos())):
                boundaries.add(w.getPosition() - 1)

            # before a preposition
            elif w.getPos().startswith("VZ"):
                boundaries.add(w.getPosition() - 1)

            # ?? fout: de | te verwachten| toename
            #            de | in wezen | separatistische elementen
            #              door een | op sterke principes gebaseerde | vredesfilosofie

            # before a particle not preceded by another particle
            # nu, toch, ook , maar, eens, even
            if (PoSCodes.DUTCH_PART.contains(
                w.getLemma()) and w.getPosition() > 0 and
                    not (PoSCodes.DUTCH_PART.contains(sent.get(w.getPosition() - 1).getLemma()))):
                boundaries.add(w.getPosition() - 1)

            # before and after adverbs" waarmee, waaronder, daarvan ...
            elif (w.getPos().startswith("BW") and (w.getLemma().startswith("waar")
                    or w.getLemma().startswith("daar"))):
                boundaries.add(w.getPosition() - 1)
                boundaries.add(w.getPosition())

            # before and after Dutch "voegwoordelijke bijwoorden"
            elif PoSCodes.DUTCH_ZINSBIJW.contains(sent.get(w.getPosition()).getLemma()):
                boundaries.add(w.getPosition() - 1)
                boundaries.add(w.getPosition())

            # before personal pronoun or relative pronoun
            elif (w.getPos().startswith("VNW") and (contains("pron,nomin", w.getPos()) or
                                                    contains("pron,stan", w.getPos()) or
                                                    contains("pron,obl", w.getPos())) and
                     w.getPosition() > 0 and not (sent.get(w.getPosition() - 1).getPos().startswith("VZ"))):
                boundaries.add(w.getPosition() - 1)

            # before a indef. pronoun not preceded by an indef. pronoun or prep. or adverb
            elif (w.getPos().startswith("VNW(onbep") and contains("prenom", w.getPos()) and
                    w.getPosition() > 0 and
                    not sent.get(w.getPosition() - 1).getPos().startswith("VNW(onbep") and
                    not contains(",det,", sent.get(w.getPosition() - 1).getPos()) and
                    not sent.get(w.getPosition() - 1).getPos().startswith("BW")):
                boundaries.add(w.getPosition() - 1)

            # between two PVs or inf and PV
            elif (w.getPos().startswith("WW(pv") and w.getPosition() > 0 and
                    (sent.get(w.getPosition() - 1).getPos().startswith("WW(pv") or
                     sent.get(w.getPosition() - 1).getPos().startswith("WW(inf"))):
                boundaries.add(w.getPosition() - 1)

            # after papa preceded and followed by a pv, e.g. heeft ingediend | zijn
            elif (w.getPos().startswith("WW(pv") and w.getPosition() > 1 and
                    sent.get(w.getPosition() - 1).getPos().startswith("WW(vd") and
                    sent.get(w.getPosition() - 2).getPos().startswith("WW(pv")):
                boundaries.add(w.getPosition() - 1)

            # between two pa.pa
            elif (w.getPos().startswith("WW(vd,vrij") and it.hasNext() and
                    sent.get(w.getPosition() + 1).getPos().startswith("WW(vdgroup,vrij")):
                boundaries.add(w.getPosition())

            # between infinitive and past participle if precededby present participle
            # op die manier kunnen � die terroristische organisaties gaande houden | opgerold worden
            elif (w.getPos().startswith("WW(inf,vrij") and w.getPosition() > 1 and
                    sent.get(w.getPosition() - 1).getPos().startswith("WW(od") and
                    it.hasNext() and sent.get(w.getPosition() + 1).getPos().startswith("WW(vd,vrij")):
                boundaries.add(w.getPosition())

            # before a verb (pv, vd, od) not preceded other verb
            elif ((w.getPos().startswith("WW(pv") or w.getPos().startswith("WW(vd,vrij") or
                    w.getPos().startswith("WW(od,vrij")) and w.getPosition() > 0 and
                        (not sent.get(w.getPosition() - 1).getPos().startswith("WW") or
                         contains(",nom,", sent.get(w.getPosition() - 1).getPos()))):
                boundaries.add(w.getPosition() - 1)

            # before infinitive not preceded by "te" or other verb
            elif (w.getPos().startswith("WW(inf,vrij") and not w.getMappedPos() == "N" and
                    w.getPosition() > 0 and
                     sent.get(w.getPosition() - 1).getLemma().lower() != "te" and
                    (not sent.get(w.getPosition() - 1).getPos().startswith("WW") or
                         contains(",nom,", sent.get(w.getPosition() - 1).getPos()))):
                boundaries.add(w.getPosition() - 1)

            # before an adverb not preceded by an adverb or determiner, or preposition
            elif (w.getPos().startswith("BW") and w.getPosition() > 0 and
                    not sent.get(w.getPosition() - 1).getPos().startswith("BW") and
                    not sent.get(w.getPosition() - 1).getPos().startswith("LID") and
                    not contains(",det,", sent.get(w.getPosition() - 1).getPos()) and
                    not sent.get(w.getPosition() - 1).getPos().startswith("VZ")):
                boundaries.add(w.getPosition() - 1)

            # before an adjective (not postnom) preceded by verb or noun
            elif ((w.getPos().startswith("ADJ") or w.getPos().startswith("TW(rang")) and not
                        (contains("postnom", w.getPos())) and w.getPosition() > 0 and
                        ((sent.get(w.getPosition() - 1).getPos().startswith("WW") and
                                not sent.get(w.getPosition() - 1).getMappedPos() == "ADJ") or
                            sent.get(w.getPosition() - 1).getPos().startswith("N") or
                            contains(",nom,", sent.get(w.getPosition() - 1).getPos())) and
                        not contains(",gen,", sent.get(w.getPosition() - 1).getPos()) and
                        not contains(",gen)", sent.get(w.getPosition() - 1).getPos())):
                boundaries.add(w.getPosition() - 1)

            # before a pronoun preceded by a verb, noun, adjective
            elif (w.getPos().startswith("VNW") and w.getPosition() > 0 and
                    (sent.get(w.getPosition() - 1).getPos().startswith("WW") or
                     sent.get(w.getPosition() - 1).getPos().startswith("N") or
                     sent.get(w.getPosition() - 1).getPos().startswith("ADJ") or
                     sent.get(w.getPosition() - 1).getPos().startswith("TW"))):
                boundaries.add(w.getPosition() - 1)

            # after a postnom. adjective (not followed by a postnominal adjective)
            elif (w.getPos().startswith("ADJ(postnom") and it.hasNext() and
                  not (sent.get(w.getPosition() + 1).getPos().startswith("ADJ(postnom"))):
                boundaries.add(w.getPosition())

            # between adverb and noun
            elif (w.getPos().startswith("BW") and it.hasNext() and
                     (sent.get(w.getPosition() + 1).getPos().startswith("N") or
                      contains(",nom,", sent.get(w.getPosition() + 1).getPos()))):
                boundaries.add(w.getPosition())

            # after a verb not followed by another verb
            if (w.getPos().startswith("WW") and not contains("prenom", w.getPos())
                    and it.hasNext() and not sent.get(w.getPosition() + 1).getPos().startswith("WW")):
                boundaries.add(w.getPosition())

            # after personal pronoun or relative pronoun
            elif (w.getPos().startswith("VNW") and (contains("pron,nomin", w.getPos()) or
                                                    contains("pron,stan", w.getPos()) or
                                                    contains("pron,obl", w.getPos()))):
                boundaries.add(w.getPosition())

            elif (w.getPos() == "VZ(init)" and it.hasNext() and
                    not sent.get(w.getPosition() + 1).getPos().startswith("WW(inf")):
                prepBoundaries.add(w.getPosition())

            # after a particle not followed by another particle
            # nu, toch, ook , maar, eens, even
            if (PoSCodes.DUTCH_PART.contains(w.getLemma()) and it.hasNext() and
                    not (PoSCodes.DUTCH_PART.contains(sent.get(w.getPosition() + 1).getLemma()))):
                boundaries.add(w.getPosition())

        # second run -> delete certain boundaries
        it = JIterator(sent)
        while it.hasNext():
            w = it.next()

            # never a boundary after an article, except if followed by prep
            if (w.getPos().startswith("LID") and it.hasNext() and
                    not (sent.get(w.getPosition() + 1).getPos().startswith("VZ"))):
                boundaries.remove(w.getPosition())

            elif w.getLemma() == "met" and it.hasNext() and sent.get(w.getPosition() + 1).getToken() == "name":
                prepBoundaries.remove(w.getPosition())
                prepBoundaries.remove(w.getPosition() + 1)

            elif w.getLemma() == "onder" and it.hasNext() and sent.get(w.getPosition() + 1).getToken() == "andere":
                prepBoundaries.remove(w.getPosition())
                prepBoundaries.remove(w.getPosition() + 1)

            elif w.getToken() == "meer" and it.hasNext() and sent.get(w.getPosition() + 1).getToken() == "dan":
                boundaries.remove(w.getPosition())
                prepBoundaries.remove(w.getPosition())

            elif w.getToken() == "minder" and it.hasNext() and sent.get(w.getPosition() + 1).getToken() == "dan":
                boundaries.remove(w.getPosition())
                prepBoundaries.remove(w.getPosition())

            elif w.getLemma() == "omwille" and it.hasNext() and sent.get(w.getPosition() + 1).getToken() == "van":
                boundaries.remove(w.getPosition())
                boundaries.remove(w.getPosition() + 1)

            # remove boundaries at "&", e.g. Sales & Customer Service
            elif w.getToken() == "&":
                boundaries.remove(w.getPosition() - 1)
                boundaries.remove(w.getPosition())

            # remove boundaries at "-" (2005 - 2006)
            elif (w.getToken().startswith("-") and it.hasNext() and
                    matches("^[0-9]+$", sent.get(w.getPosition() + 1).getToken()) and
                    w.getPosition() > 0 and matches("^[0-9]+$", sent.get(w.getPosition() - 1).getToken())):
                boundaries.remove(w.getPosition() - 1)
                boundaries.remove(w.getPosition())

            # remove boundary between finite verb and "te" + infinitive (e.g. "hoort te houden")
            elif (w.getLemma() == "te" and w.getPosition() > 0 and
                    sent.get(w.getPosition() - 1).getMappedPos() == "V-fin" and
                    it.hasNext() and sent.get(w.getPosition() + 1).getMappedPos() == "V-inf"):
                boundaries.remove(w.getPosition() - 1)

        # add boundary at end of sentence
        boundaries.add(len(sent) - 1)
        # to test impact prepboundaries
        boundaries.addAll(prepBoundaries)
        # remove "-1" from boundaries
        boundaries.remove(-1)
        return boundaries

    @classmethod
    def chunk_french(cls, sent):
        """Chunks a french sentence and returns the chunk boundaries as a sorted set.

           :param: sent: JList - a sequence of Word objects
           :return: JSortedSet - the ordered collection of chunk boundaries
        """
        boundaries = JSortedSet()

        it = JIterator(sent)
        while it.hasNext():
            w = it.next()

            # boundary before and after conjunctions
            if w.getMappedPos().startswith("CONJ"):
                boundaries.add(w.getPosition())
                boundaries.add(w.getPosition() - 1)

            # boundary before and after punctuation marks
            elif w.getMappedPos().startswith("PCT") or w.getMappedPos() == "SYM":
                boundaries.add(w.getPosition())
                boundaries.add(w.getPosition() - 1)

            # boundaries aroud "pourquoi"
            if w.getLemma() == "pourquoi":
                boundaries.add(w.getPosition())
                boundaries.add(w.getPosition() - 1)

            # before an article or other determiner not preceded by a preposition, a determiner or PRON-IND
            elif ((w.getMappedPos().startswith("DET") or w.getMappedPos().startswith("PRON-dem") or
                    w.getMappedPos().startswith("PRON-pos")) and w.getPosition() > 0 and
                    not sent.get(w.getPosition() - 1).getMappedPos().startswith("PREP") and
                    not sent.get(w.getPosition() - 1).getMappedPos().startswith("PRON-ind") and
                    not sent.get(w.getPosition() - 1).getMappedPos().startswith("DET")):
                boundaries.add(w.getPosition() - 1)

            elif (w.getMappedPos().startswith("PRON-ind") and w.getPosition() > 0 and
                    not sent.get(w.getPosition() - 1).getMappedPos().startswith("PREP") and
                    not sent.get(w.getPosition() - 1).getMappedPos().startswith("DET") and
                    not sent.get(w.getPosition() - 1).getMappedPos().startswith("PRON-ind") and
                    not sent.get(w.getPosition() - 1).getMappedPos().startswith("PRON-per")):
                boundaries.add(w.getPosition() - 1)

            # before a preposition (or French Prep-det) not preceded by PREP
            elif (w.getMappedPos().startswith("PREP") and w.getPosition() > 0 and
                    not sent.get(w.getPosition() - 1).getMappedPos().startswith("PREP")):
                boundaries.add(w.getPosition() - 1)

            # before and after personal pronouns (allons | -nous | )
            elif w.getMappedPos() == "PRON-per" and w.getToken().startswith("-"):
                boundaries.add(w.getPosition() - 1)
                boundaries.add(w.getPosition())

            # before personal pronoun not preceded by a preposition
            elif (w.getMappedPos().startswith("PRON-per") and w.getPosition() > 0 and
                    not sent.get(w.getPosition() - 1).getMappedPos().startswith("PREP")):
                boundaries.add(w.getPosition() - 1)

            # before or relative pronoun
            elif w.getMappedPos() == "PRON-rel":
                boundaries.add(w.getPosition() - 1)

            # French: boundary before "ne ... pas"
            elif (w.getLemma() == "ne" and it.hasNext() and
                    sent.get(w.getPosition() + 1).getMappedPos().startswith("V")):
                boundaries.add(w.getPosition() - 1)

            # before an adverb followed by a past participle (les r�gions nordiques | faiblement peupl�s)
            # not preceded by a finite verb
            elif (w.getMappedPos().startswith("ADV") and it.hasNext() and
                    sent.get(w.getPosition() + 1).getMappedPos().startswith("V-papa") and
                    w.getPosition() > 0 and
                    not sent.get(w.getPosition() - 1).getMappedPos().startswith("V-fin")):
                boundaries.add(w.getPosition() - 1)

            # before an adverb following a past participle (est clairement traduite | ici)
            elif (w.getMappedPos().startswith("ADV") and w.getPosition() > 0 and
                    sent.get(w.getPosition() - 1).getMappedPos().startswith("V-papa")):
                boundaries.add(w.getPosition() - 1)

            # between an adjective and an adverb (est aussi applicable | actuellement au Danemark)
            elif (w.getMappedPos().startswith("ADV") and w.getPosition() > 0 and
                    sent.get(w.getPosition() - 1).getMappedPos().startswith("ADJ")):
                boundaries.add(w.getPosition() - 1)

            # before a finite verb not preceded other finite verb or preceded by preposition
            elif ((w.getMappedPos().startswith("V-fin") or w.getMappedPos().startswith("V-prpa")) and
                    w.getPosition() > 0 and
                    not sent.get(w.getPosition() - 1).getMappedPos().startswith("V-fin") and
                    not sent.get(w.getPosition() - 1).getMappedPos().startswith("V-inf") and
                    not sent.get(w.getPosition() - 1).getMappedPos().startswith("PREP") and
                    sent.get(w.getPosition() - 1).getLemma() != "ne" and
                    sent.get(w.getPosition() - 1).getLemma() != "se"):
                boundaries.add(w.getPosition() - 1)

            # between verbal group and noun or adjective
            elif (w.getMappedPos().startswith("V") and w.getPosition() > 0 and
                    sent.get(w.getPosition() - 1).getMappedPos().startswith("V")
                    and it.hasNext() and (sent.get(w.getPosition() + 1).getMappedPos().startswith("N") or
                                          sent.get(w.getPosition() + 1).getMappedPos().startswith("ADJ"))):
                boundaries.add(w.getPosition())

            elif (w.getMappedPos().startswith("N") and w.getPosition() > 0 and
                    sent.get(w.getPosition() - 1).getMappedPos().startswith("V")):
                boundaries.add(w.getPosition() - 1)

            # between finite verb and adv + adj (est | clairement necessaire)
            elif (w.getMappedPos().startswith("ADV") and w.getPosition() > 0 and
                    sent.get(w.getPosition() - 1).getMappedPos().startswith("V") and
                    it.hasNext() and sent.get(w.getPosition() + 1).getMappedPos().startswith("ADJ")):
                boundaries.add(w.getPosition() - 1)

        # add boundary at end of sentence
        boundaries.add(len(sent) - 1)
        # second run: remove certain boundaries in fixed expressions
        it = JIterator(sent)
        while it.hasNext():
            w = it.next()

            # merci beaucoup
            if (w.getToken().lower() == "merci".lower() and it.hasNext() and
                    sent.get(w.getPosition() + 1).getLemma() == "beaucoup"):
                boundaries.remove(w.getPosition())

            # parce que
            if (w.getToken().lower() == "parce".lower() and it.hasNext() and
                    sent.get(w.getPosition() + 1).getLemma() == "que"):
                boundaries.remove(w.getPosition())

            # tout � fait
            elif (w.getMappedPos() == "PREP" and w.getPosition() > 0 and
                    sent.get(w.getPosition() - 1).getToken().lower() == "tout".lower()
                    and it.hasNext() and sent.get(w.getPosition() + 1).getToken() == "fait"):
                boundaries.remove(w.getPosition() - 1)
                boundaries.add(w.getPosition() - 2)

        boundaries.remove(-1)
        return boundaries

    @classmethod
    def chunk(cls, sent):
        """Chunks a sentence and returns the chunk boundaries as a sorted set.

           :param: sent: JList - a sequence of Word objects
           :return: JSortedSet - the ordered collection of chunk boundaries
        """
        boundaries = JSortedSet()

        it = JIterator(sent)
        while it.hasNext():
            w = it.next()

            # boundary before and after conjunctions
            if w.getMappedPos().startswith("CONJ"):
                boundaries.add(w.getPosition())
                boundaries.add(w.getPosition() - 1)

            # boundary before and after punctuation marks
            elif w.getMappedPos().startswith("PCT") or w.getMappedPos() == "SYM":
                boundaries.add(w.getPosition())
                boundaries.add(w.getPosition() - 1)

            # before an article or other determiner not preceded by a preposition
            elif (w.getMappedPos().startswith("DET") and w.getPosition() > 0 and
                    not sent.get(w.getPosition() - 1).getMappedPos().startswith("PREP")):
                boundaries.add(w.getPosition() - 1)

            # before a preposition (or French Prep-det) not preceded by PREP
            elif (w.getMappedPos().startswith("PREP") and w.getPosition() > 0 and
                    not sent.get(w.getPosition() - 1).getMappedPos().startswith("PREP")):
                boundaries.add(w.getPosition() - 1)

            # before personal pronoun or relative pronoun
            elif w.getMappedPos() == "PRON-rel" or w.getMappedPos() == "PRON-per":
                boundaries.add(w.getPosition() - 1)

            # French: boundary before "ne ... pas"
            elif (w.getLemma() == "ne" and it.hasNext() and
                    sent.get(w.getPosition() + 1).getMappedPos().startswith("V")):
                boundaries.add(w.getPosition() - 1)

            # before a finite verb not preceded other finite verb or preceded by preposition
            elif ((w.getMappedPos().startswith("V-fin") or w.getMappedPos().startswith("V-prpa") or
                    w.getMappedPos().startswith("V-papa")) and w.getPosition() > 0 and
                    not sent.get(w.getPosition() - 1).getMappedPos().startswith("V-fin") and
                    not sent.get(w.getPosition() - 1).getMappedPos().startswith("V-inf") and
                    not sent.get(w.getPosition() - 1).getMappedPos().startswith("PREP") and
                    # Fench: "ne"
                    sent.get(w.getPosition() - 1).getLemma() != "ne" and
                    # French: se, s'
                    sent.get(w.getPosition() - 1).getLemma() != "se"):
                boundaries.add(w.getPosition() - 1)

            # between verbal group and noun
            elif (w.getMappedPos().startswith("V") and w.getPosition() > 0 and
                    sent.get(w.getPosition() - 1).getMappedPos().startswith("V") and
                    it.hasNext() and sent.get(w.getPosition() + 1).getMappedPos().startswith("N")):
                boundaries.add(w.getPosition())

        # add boundary at end of sentence
        boundaries.add(len(sent) - 1)

        boundaries.remove(-1)
        return boundaries


CHUNKER_MAP = {
    "en": Chunkers.chunk_english,
    "nl": Chunkers.chunk_dutch,
    "fr": Chunkers.chunk_french,
    "de": Chunkers.chunk,
}


def get_chunk_function(language):
    """Returns a chunk function appropriate for the given language."""
    assert language in ("en", "de", "fr", "nl")
    return CHUNKER_MAP[language]
