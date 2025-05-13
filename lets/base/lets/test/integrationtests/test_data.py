from tokenizer import Tokenizer
import unittest

from lemmatizer import Lemmatizer
from lemmatizer_steps.crfpp1 import CRFPP1
from lemmatizer_steps.crfpp2 import CRFPP2

from lemmatizer_steps.adjust_capitalization import AdjustCapitalization
from lemmatizer_steps.make_features_for_lemmatizing1 import MakeFeaturesForLemmatizing1
from lemmatizer_steps.make_features_for_lemmatizing2 import MakeFeaturesForLemmatizing2
from lemmatizer_steps.make_lemma_output_DEF import MakeLemmaOutputDEF
from os import listdir
from os.path import join
from postag_steps.feat_vects import FeatVects
from postag_steps.clean_output import CleanOutput
import postag_steps.crfpp
from postag import POSTag
from chunker import Chunker
from preprocessor import PreProcessor
import os.path
import re
from pathlib import Path
import datetime
from ner import NER


class MixinTests:
    def test_all_data(self):
        import os
        print()
        data_folder = 'test/integrationtests/data'
        file_excludes = self.file_excludes if hasattr(self, 'file_excludes') else []
        used_languages = ['Nl', 'En', 'De', 'Fr']
        # used_languages = ['En']
        languages = [l for l in listdir(data_folder) if l in used_languages]
        print("step", self.step)
        for language in languages:
            print("Language: {}".format(language))
            subdir = join(data_folder, language)
            out_files = [f for f in listdir(subdir) if
                         f.endswith(self.out_ext) and f not in [e + self.out_ext for e in file_excludes]]
            in_exts = [self.in_ext] if isinstance(self.in_ext, str) else self.in_ext
            base_files = [re.match(r'(.*)' + self.out_ext, f).group(1) for f in out_files]

            existing_base_files = filter(lambda f: all(Path(join(subdir, f + e)).is_file() for e in in_exts),
                                         base_files)

            for ef in existing_base_files:
                in_files = [join(subdir, ef + e) for e in in_exts]
                out_file = join(subdir, ef + self.out_ext)

                print("\tHandling {}".format(ef))

                lines = [open(f, 'r', encoding='utf8') for f in in_files]
                step = self.step(language.lower())
                with open(out_file, 'rt') as expected_tokens:
                    i = 0
                    start = datetime.datetime.now()
                    if (len(lines) == 1):
                        result = step.process_lines(*lines)
                    else:
                        result = step.process_dual_lines(*lines)
                    for line in result:
                        i += 1
                        if i % 10000 == 0:
                            print("\t\t", i, datetime.datetime.now(), datetime.datetime.now() - start)
                            start = datetime.datetime.now()
                        try:
                            expected_line = next(expected_tokens).strip()
                        except StopIteration:
                            expected_line = ''
                        # print("l:", l, "e:", expected_line)
                        # print('l', line)
                        # print('e', expected_line)
                        if (line != expected_line):
                            print('i', i)
                            print('l', line)
                            print('e', expected_line)
                            # print(line)
                        self.assertEqual(line, expected_line)
                    try:
                        while (True):
                            found = next(expected_tokens)
                            self.assertTrue(found.strip() == '', found)
                    except StopIteration:
                        pass
                    finally:
                        for f in lines:
                            f.close()


# class TokenizerTests(MixinTests, unittest.TestCase):
#     step = Tokenizer
#     in_ext = '.utf8'
#     out_ext = '.tokperl'


# class POSTagTests(MixinTests, unittest.TestCase):
#     step = POSTag
#     in_ext = '.tok'
#     out_ext = '.pos'


# class LemmatizerTests(MixinTests, unittest.TestCase):
#     step = Lemmatizer
#     in_ext = '.pos'
#     out_ext = '.lem'
#     file_excludes = ['allExpertReviews', 'JDN_jaar_input_nl', 'PSA_inputCrossLang_nl', 'emea-deen-de']


class ChunkerTests(MixinTests, unittest.TestCase):
    step = Chunker
    in_ext = ['.lem', '.pos']
    out_ext = '.cnk'
    file_excludes = ['allExpertReviews', 'JDN_jaar_input_nl', 'PSA_inputCrossLang_nl']


# class NERTests(MixinTests, unittest.TestCase):
#     step = NER
#     in_ext = '.pos'
#     out_ext = '.ner'
#     file_excludes = ['allExpertReviews', 'JDN_jaar_input_nl', 'PSA_inputCrossLang_nl']


# class FeatVectsTests(MixinTests, unittest.TestCase):
#     step = FeatVects
#     in_ext = '.tok'
#     out_ext = '.tmp'

# class CleanOutputTests(MixinTests, unittest.TestCase):
#     step = CleanOutput
#     in_ext = '.tmq'
#     out_ext = '.pos'
# class PostagCRFPPTests(MixinTests, unittest.TestCase):
#     step = postag_steps.crfpp.CRFPP
#     in_ext = '.tmp'
#     out_ext = '.tmq'
#
# class AdjustCapitalizationTests(MixinTests, unittest.TestCase):
#     step = AdjustCapitalization
#     in_ext = '.pos'
#     out_ext = '.lemFeat1'


#
# class MakeFeaturesForLemmatizing1Tests(MixinTests, unittest.TestCase):
#     step = MakeFeaturesForLemmatizing1
#     in_ext = '.lemFeat1'
#     out_ext = '_1.lemFeat2'
#
# class MakeFeaturesForLemmatizing2Tests(MixinTests, unittest.TestCase):
#     step = MakeFeaturesForLemmatizing2
#     in_ext = '.lemFeat1'
#     out_ext = '_2.lemFeat2'
#
# class CRFPP1Tests(MixinTests, unittest.TestCase):
#     step = CRFPP1
#     in_ext = '_1.lemFeat2'
#     out_ext = '_1.lemOut1'
#
# class CRFPP2Tests(MixinTests, unittest.TestCase):
#     step = CRFPP2
#     in_ext = '_2.lemFeat2'
#     out_ext = '_2.lemOut2'
#
# class MakeLemmaOutputDEFTests(MixinTests, unittest.TestCase):
#     step = MakeLemmaOutputDEF
#     in_ext = ['.lemFeat1', '_1.lemOut1', '_2.lemOut2']
#     out_ext = '.lem'
#     file_excludes = ['PSA_inputCrossLang_nl']


if __name__ == '__main__':
    unittest.main()
