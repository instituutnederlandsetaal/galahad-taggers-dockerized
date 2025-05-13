"""
Q&D tool for checking the differences between .ner output available
in preprocessor/test/integrationtests/data and the one produced by
the Java code using the available models.

sha1 sums of the models files used for the tests:

7085831e78ea5b2b917217c50bb5f4a895d5ffa7  NER.de
79957a1ca83700699e36f8dacff109746e409d04  NER.en
b1b4416f843b6ffd6e0acdb3f0d4d09d37e8956c  NER.fr
f5d6965b2f8a5fe5a1951ef7fdb5d3996c0675eb  NER.nl

Differencies reported here:
 https://yazzoom.codebasehq.com/projects/ugent_lt3/discussions/sample-differences-of-ner-output

Created on 2016/12/01.

"""

import sys
from os.path import join as pjoin

from test.unittests.testutil import collect_filenames

HOME_DIR = r"/home/yassen/Work/spaces/eclipse-4.6/ugent_lt3_java/WORK/ner4"
SUBDIRS = ('Fr', 'Nl')


def collect_ner_files(adir, excludefn=None):
    ner_files = collect_filenames(adir, '.ner')
    if not excludefn:
        return ner_files
    result = list()
    for fname in ner_files:
        if not excludefn(fname):
            result.append(fname)
    return result


def compare_lines(origline, line):
    origrec = origline.split()
    nerrec = line.split()
    if (not origrec) and (not nerrec):
        return True
    return origrec[:2] == nerrec[:2]
    

def compare_ner_files(homedir, orignerf, nerf):
    print("\nComparing: [", orignerf, "] vs. [", nerf, "]:", sep="")
    with open(pjoin(homedir, orignerf)) as in_orig, \
            open(pjoin(homedir, nerf)) as in_ner:
        diff_count = 0
        line_count = 0
        for origline, line in zip(in_orig, in_ner):
            line_count += 1
            if compare_lines(origline, line):
                continue
            diff_count += 1
            if diff_count < 6:
                print(" - Line {}:  expected: {!r} but was: {!r}"
                      .format(line_count, origline.rstrip("\n"), line.rstrip("\n"), file=sys.stderr))
        print("Total lines:", line_count, "; diffs in second column:", diff_count)


def main():
    for subdir in SUBDIRS:
        full_dir = pjoin(HOME_DIR, subdir)
        print("\n" + 72*'-' + '\n', full_dir)
        orig_ner_files = collect_filenames(full_dir, '.ner.orig')
        ner_files = collect_ner_files(full_dir, excludefn=lambda f: f.endswith('.new.ner'))
        for orignerf, nerf  in zip(sorted(orig_ner_files), sorted(ner_files)):
            compare_ner_files(full_dir, orignerf, nerf)


if __name__ == '__main__':
    main()
