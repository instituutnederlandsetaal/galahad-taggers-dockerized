import unittest

from abstract_crfpp import AbstractCRFPP


class CRFPPTest(unittest.TestCase):
    def tests_simple(self):
        crfpp = AbstractCRFPP("lemmatizer_steps/models/Lemmatizer1.nl")
        line1 = "binnenpaneel ADJ(basis,zonder) l el eel neel aneel paneel npaneel enpaneel"
        line2 = "dakversteviging N(ev) g ng ing ging iging viging eviging teviging"
        line3 = "achter VZ(init) r er ter hter chter achter achter achter"
        results = crfpp.process_lines([line1, line2, line3])
        expected1 = 'binnenpaneel	ADJ(basis,zonder)	l	el	eel	neel	aneel	paneel	npaneel	enpaneel	+Del+Ilen/0.939984'
        expected2 = 'dakversteviging	N(ev)	g	ng	ing	ging	iging	viging	eviging	teviging	+Ding+Iaan/0.936940'
        expected3 = 'achter	VZ(init)	r	er	ter	hter	chter	achter	achter	achter	+Der/0.788459'
        for result, expected in zip(results, [expected1, expected2, expected3]):
            print(expected)
            print(result[1])
            # crfpp.process_lines([])
