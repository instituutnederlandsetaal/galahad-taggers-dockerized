"""
POSReader unit tests data. See reader_test module for details.
Created on 2016/11/08

"""

MADAGASCAR_EN_POS_PART = """\
60 CD 0.992424
million CD 0.999906
years NNS 0.999625
ago RB 0.958702
, , 0.999958
on IN 0.999747
the DT 0.999819
shores NNS 0.997286
of IN 0.999900
this DT 0.999577
tropical JJ 0.993282
island NN 0.995081
, , 0.999956
an DT 0.999418
extraordinary JJ 0.997517
story NN 0.999754
began VBD 0.988478
. . 0.999996

The DT 0.999889
waves NNS 0.997983
brought VBD 0.900457
ashore RB 0.814344
an DT 0.999030
odd JJ 0.997483
band NN 0.999536
of IN 0.999972
survivors NNS 0.999057
- : 0.998594
a DT 0.997207
few JJ 0.999794
ancient JJ 0.879031
creatures NNS 0.999494
that WDT 0.993569
had VBD 0.999796
been VBN 0.999959
accidentally RB 0.999666
swept VBN 0.752597
across IN 0.970853
hundreds NNS 0.999120
of IN 0.999954
kilometres NNS 0.998201
of IN 0.999903
ocean NN 0.990595
from IN 0.999974
a DT 0.999878
distant JJ 0.989248
land NN 0.999307
. . 0.999995

"""

MADAGASCAR_EN_LEM_PART = """\
60 60 /
million million /
years year 0.998357
ago ago 0.996526
, , /
on on /
the the /
shores shore 0.993417
of of /
this this /
tropical tropical /
island island /
, , /
an an /
extraordinary extraordinary /
story story /
began begin 0.777042
. . /

The the /
waves wave 0.973181
brought bring 0.799948
ashore ashore 0.997623
an an /
odd odd /
band band /
of of /
survivors survivor 0.998137
- - /
a a /
few few /
ancient ancient /
creatures creature 0.998548
that that /
had have 0.848421
been be 0.809043
accidentally accidentally 0.999873
swept sweep 0.939658
across across /
hundreds hundred 0.997541
of of /
kilometres kilometre 0.996640
of of /
ocean ocean /
from from /
a a /
distant distant /
land land /
. . /

"""

MADAGASCAR_EN_CNK_PART_EXPECTED = """\
60    60    CD    B-NP
million    million    CD    I-NP
years    year    NNS    I-NP
ago    ago    RB    B-ADVP
,    ,    ,    O
on    on    IN    B-PP
the    the    DT    B-NP
shores    shore    NNS    I-NP
of    of    IN    B-PP
this    this    DT    B-NP
tropical    tropical    JJ    I-NP
island    island    NN    I-NP
,    ,    ,    O
an    an    DT    B-NP
extraordinary    extraordinary    JJ    I-NP
story    story    NN    I-NP
began    begin    VBD    B-VP
.    .    .    O

The    the    DT    B-NP
waves    wave    NNS    I-NP
brought    bring    VBD    B-VP
ashore    ashore    RB    B-ADVP
an    an    DT    B-NP
odd    odd    JJ    I-NP
band    band    NN    I-NP
of    of    IN    B-PP
survivors    survivor    NNS    B-NP
-    -    :    O
a    a    DT    B-NP
few    few    JJ    I-NP
ancient    ancient    JJ    I-NP
creatures    creature    NNS    I-NP
that    that    WDT    B-NP
had    have    VBD    B-VP
been    be    VBN    I-VP
accidentally    accidentally    RB    B-ADVP
swept    sweep    VBN    B-VP
across    across    IN    B-PP
hundreds    hundred    NNS    B-NP
of    of    IN    B-PP
kilometres    kilometre    NNS    B-NP
of    of    IN    B-PP
ocean    ocean    NN    B-NP
from    from    IN    B-PP
a    a    DT    B-NP
distant    distant    JJ    I-NP
land    land    NN    I-NP
.    .    .    O

"""

#: Part of PSA_inputCrossLang_en.pos
PSA_INPUT_CROSSLANG_EN_PART_POS = """\
switch NN 0.609433
*1 CD 0.978578
, , 0.999955
located VBN 0.886611
on IN 0.997279
the DT 0.999951
roof NN 0.904467
console NN 0.968581
, , 0.999935
activates NNS 0.896316
or CC 0.999781
deactivates VBZ 0.920117
the DT 0.999853
operation NN 0.999943
of IN 0.999967
the DT 0.999978
rear JJ 0.713202
controls NNS 0.879671
from IN 0.999927
the DT 0.999968
driver NN 0.998331
or CC 0.999823
front JJ 0.816935
passenger NN 0.997643
seat NN 0.996334

"""

#: Part of PSA_inputCrossLang_en.lem
PSA_INPUT_CROSSLANG_EN_PART_LEM = """\
switch switch /
*1 *1 /
, , /
located locate 0.997722
on on /
the the /
roof roof /
console console /
, , /
activates activate 0.999030
or or /
deactivates deactivate 0.999730
the the /
operation operation /
of of /
the the /
rear rear /
controls control 0.998648
from from /
the the /
driver driver /
or or /
front front /
passenger passenger /
seat seat /

"""

#: Part of PSA_inputCrossLang_en.cnk expected
PSA_INPUT_CROSSLANG_EN_PART_CNK_EXPECTED = """\
switch    switch    NN    B-NP
*1    *1    CD    I-NP
,    ,    ,    O
located    locate    VBN    B-VP
on    on    IN    B-PP
the    the    DT    B-NP
roof    roof    NN    I-NP
console    console    NN    I-NP
,    ,    ,    O
activates    activate    NNS    B-NP
or    or    CC    O
deactivates    deactivate    VBZ    B-VP
the    the    DT    B-NP
operation    operation    NN    I-NP
of    of    IN    B-PP
the    the    DT    B-NP
rear    rear    JJ    I-NP
controls    control    NN    I-NP
from    from    IN    B-PP
the    the    DT    B-NP
driver    driver    NN    I-NP
or    or    CC    O
front    front    JJ    B-NP
passenger    passenger    NN    I-NP
seat    seat    NN    I-NP

"""

JDN_JAAR_INPUT_EN_POS = """\
The DT 0.999975
fact NN 0.998379
that IN 0.928603
Jan NNP 0.999380
De NNP 0.996285
Nul NNP 0.999957
Group NNP 0.997312
employs VBZ 0.977274
500 CD 0.999935
engineers NNS 0.999801
, , 0.999958
is VBZ 0.999844
in IN 0.999158
itself PRP 0.997880
no DT 0.990605
surprise NN 0.994733
, , 0.999941
being VBG 0.999008
a DT 0.998639
rapidly RB 0.995704
expanding VBG 0.997888
high-tech JJ 0.971827
company NN 0.999905
. . 0.999996

"""

JDN_JAAR_INPUT_EN_LEM = """\
The the /
fact fact /
that that /
Jan Jan /
De De /
Nul Nul /
Group Group /
employs employ 0.999739
500 500 /
engineers engineer 0.998982
, , /
is be 0.703572
in in /
itself itself 0.964619
no no /
surprise surprise /
, , /
being be 0.978195
a a /
rapidly rapidly 0.999788
expanding expand 0.992513
high-tech high-tech /
company company /
. . /

"""

JDN_JAAR_INPUT_EN_CNK_EXPECTED = """\
The    the    DT    B-NP
fact    fact    NN    I-NP
that    that    IN    B-PP
Jan    Jan    NNP    B-NP
De    De    NNP    I-NP
Nul    Nul    NNP    I-NP
Group    Group    NNP    I-NP
employs    employ    VBZ    B-VP
500    500    CD    B-NP
engineers    engineer    NNS    I-NP
,    ,    ,    O
is    be    VBZ    B-VP
in    in    IN    O
itself    itself    PRP    B-PP
no    no    DT    B-NP
surprise    surprise    NN    I-NP
,    ,    ,    O
being    be    VBG    B-VP
a    a    DT    B-ADVP
rapidly    rapidly    RB    I-ADVP
expanding    expand    VBG    B-VP
high-tech    high-tech    JJ    B-NP
company    company    NN    I-NP
.    .    .    O

"""

JDN_JAAR_INPUT_DU_POS_PART = """\
Während KOUS 0.999761
wir PPER 0.999843
die ART 0.999945
Krise NN 0.999341
von APPR 0.998959
2008-2009 CARD 0.982804
durch APPR 0.999145
die ART 0.999867
Trägheit NN 0.997636
und KON 0.999956
den ART 0.999807
Verzögerungseffekt NN 0.999087
, $, 0.999941
der PRELS 0.995178
dem ART 0.999552
Infrastrukturmarkt NN 0.999769
eigen ADJD 0.931396
ist VAFIN 0.999894
, $, 0.999849
nicht PTKNEG 0.999919
in APPR 0.999950
den ART 0.999954
Ziffern NN 0.998530
von APPR 0.999183
2009 CARD 0.999988
gespürt VVPP 0.998354
haben VAFIN 0.970766
, $, 0.999947
ist VAFIN 0.999923
die ART 0.998780
Wirkung NN 0.999725
davon PROAV 0.997282
doch ADV 0.997678
im APPRART 0.999949
Jahr NN 0.999508
2010 CARD 0.999977
spürbar ADJD 0.998487
, $, 0.999899
sei VAFIN 0.999579
es PPER 0.999973
etwas ADV 0.577612
abgeflacht VVPP 0.737072
und KON 0.999959
gemäßigt VVPP 0.548050
. $. 1.000000

"""

JDN_JAAR_INPUT_DU_LEM_PART = """\
Während während /
wir wir 0.972969
die der 0.933342
Krise Krise 0.965274
von von /
2008-2009 2008-2009 0.393283
durch durch /
die der 0.933342
Trägheit Trägheit 0.999137
und und /
den der 0.521623
Verzögerungseffekt Verzögerungseffekt 0.995738
, , /
der der 0.947858
dem der 0.543886
Infrastrukturmarkt Infrastrukturmarkt 0.991086
eigen eigen 0.502382
ist sein 0.906114
, , /
nicht nicht /
in in /
den der 0.521623
Ziffern Ziffer 0.929351
von von /
2009 2009 0.393283
gespürt spüren 0.992713463896
haben haben 0.984668
, , /
ist sein 0.906114
die der 0.933342
Wirkung Wirkung 0.999531
davon davon /
doch doch /
im in 0.939634
Jahr Jahr 0.996088
2010 2010 0.393283
spürbar spürbar 0.998771
, , /
sei sein 0.561532
es es 0.951286
etwas etwas /
abgeflacht abflachen 0.99313282461
und und /
gemäßigt mäßigen 0.997356808723
. . /

"""

JDN_JAAR_INPUT_DU_CNK_PART_EXPECTED = """\
Während    während    KOUS    O
wir    wir    PPER    B-NP
die    der    ART    B-NP
Krise    Krise    NN    I-NP
von    von    APPR    B-NP
2008-2009    2008-2009    CARD    I-NP
durch    durch    APPR    B-NP
die    der    ART    I-NP
Trägheit    Trägheit    NN    I-NP
und    und    KON    O
den    der    ART    B-NP
Verzögerungseffekt    Verzögerungseffekt    NN    I-NP
,    ,    $,    O
der    der    PRELS    B-NP
dem    der    ART    B-NP
Infrastrukturmarkt    Infrastrukturmarkt    NN    I-NP
eigen    eigen    ADJD    I-NP
ist    sein    VAFIN    B-VP
,    ,    $,    O
nicht    nicht    PTKNEG    B-ADVP
in    in    APPR    B-NP
den    der    ART    I-NP
Ziffern    Ziffer    NN    I-NP
von    von    APPR    B-NP
2009    2009    CARD    I-NP
gespürt    spüren    VVPP    B-VP
haben    haben    VAFIN    B-VP
,    ,    $,    O
ist    sein    VAFIN    B-VP
die    der    ART    B-NP
Wirkung    Wirkung    NN    I-NP
davon    davon    PROAV    I-NP
doch    doch    ADV    I-NP
im    in    APPRART    B-NP
Jahr    Jahr    NN    I-NP
2010    2010    CARD    I-NP
spürbar    spürbar    ADJD    I-NP
,    ,    $,    O
sei    sein    VAFIN    B-VP
es    es    PPER    B-ADVP
etwas    etwas    ADV    I-ADVP
abgeflacht    abflachen    VVPP    B-VP
und    und    KON    O
gemäßigt    mäßigen    VVPP    B-VP
.    .    $.    O

"""

RIZIV_NL_CNK_PART_EXPECTED = """\
[    [    LET()    B-NP
W    W    N(soort,ev,basis,zijd,stan)    I-NP
-    -    LET()    O
Wet    wet    N(soort,ev,basis,zijd,stan)    B-NP
22-2-98    22-2-98    SPEC(symb)    I-NP
-    -    LET()    O
B.S.    B.S.    SPEC(symb)    O
3-3    3-3    SPEC(symb)    O
]    ]    LET()    O

"""

RIZIV_NL_POS_PART = """\
[ LET() 0.995896
W N(soort,ev,basis,zijd,stan) 0.464211
- LET() 0.999483
Wet N(soort,ev,basis,zijd,stan) 0.581854
22-2-98 SPEC(symb) 0.678637
- LET() 0.993079
B.S. SPEC(symb) 0.961402
3-3 SPEC(symb) 0.994506
] LET() 0.993268

"""

RIZIV_NL_LEM_PART = """\
[ [ /
W W /
- - /
Wet wet /
22-2-98 22-2-98 /
- - /
B.S. B.S. /
3-3 3-3 /
] ] /

"""

RIZIV_NL_CNK_PART2_EXPECTED = """\
Het    het    LID(bep)    B-NP
multidisciplinair    multidisciplinair    ADJ(prenom,basis,zonder)    I-NP
oncologisch    oncologisch    ADJ(prenom,basis,zonder)    I-NP
onderzoek    onderzoek    N(soort,ev,basis,onz,stan)    I-NP
,    ,    LET()    O
dat    dat    VNW(betr,pron,3,ev)    B-NP
nu    nu    BW()    B-ADVP
aangerekend    aanrekenen    WW(vd,vrij,zonder)    B-VP
kan    kunnen    WW(pv,tgw,ev)    I-VP
worden    worden    WW(inf,vrij,zonder)    I-VP
,    ,    LET()    O
zal    zullen    WW(pv,tgw,ev)    B-VP
een    een    LID(onbep)    B-NP
vereiste    vereisen    WW(vd,nom,met-e,zonder-n)    I-NP
worden    worden    WW(inf,vrij,zonder)    B-VP
.    .    LET()    O

"""

RIZIV_NL_POS_PART2 = """\
Het LID(bep) 0.993649
multidisciplinair ADJ(prenom,basis,zonder) 0.911211
oncologisch ADJ(prenom,basis,zonder) 0.997371
onderzoek N(soort,ev,basis,onz,stan) 0.999789
, LET() 1.000000
dat VNW(betr,pron,3,ev) 0.854678
nu BW() 0.999077
aangerekend WW(vd,vrij,zonder) 0.665646
kan WW(pv,tgw,ev) 0.999519
worden WW(inf,vrij,zonder) 0.994237
, LET() 1.000000
zal WW(pv,tgw,ev) 0.999728
een LID(onbep) 0.999185
vereiste WW(vd,nom,met-e,zonder-n) 0.530200
worden WW(inf,vrij,zonder) 0.858349
. LET() 1.000000

"""

RIZIV_NL_LEM_PART2 = """\
Het het 0.905417
multidisciplinair multidisciplinair /
oncologisch oncologisch /
onderzoek onderzoek /
, , /
dat dat 0.910022
nu nu /
aangerekend aanrekenen 0.982803405818
kan kunnen 0.778056
worden worden /
, , /
zal zullen 0.893846
een een 0.634522
vereiste vereisen 0.813540198034
worden worden /
. . /

"""

RIZIV_NL_CNK_PART3_EXPECTED = """\
-Verzekeringscomité    -Verzekeringscomité    SPEC(afgebr)    O
-    -    LET()    O
01/10/07    01/10/07    SPEC(symb)    O
-    -    LET()    O
2    2    TW(hoofd)    B-NP
opeenvolgende    opeenvolgend    ADJ(prenom,basis,met-e,stan)    I-NP
vergaderingen    vergadering    N(soort,mv,basis)    I-NP
(    (    LET()    O
beslissing    beslissing    N(soort,ev,basis,zijd,stan)    B-NP
budget    budget    N(soort,ev,basis,onz,stan)    I-NP
2008    2008    TW(hoofd)    I-NP
)    )    LET()    O

"""

RIZIV_NL_POS_PART3 = """\
-Verzekeringscomité SPEC(afgebr) 0.977825
- LET() 0.999760
01/10/07 SPEC(symb) 0.730171
- LET() 0.997932
2 TW(hoofd,prenom,stan) 0.472010
opeenvolgende ADJ(prenom,basis,met-e,stan) 0.955405
vergaderingen N(soort,mv,basis) 0.993420
( LET() 0.999974
beslissing N(soort,ev,basis,zijd,stan) 0.952677
budget N(soort,ev,basis,onz,stan) 0.944441
2008 TW(hoofd,vrij) 0.947308
) LET() 0.999783

"""

RIZIV_NL_LEM_PART3 = """\
-Verzekeringscomité -Verzekeringscomité /
- - /
01/10/07 01/10/07 /
- - /
2 2 /
opeenvolgende opeenvolgend 0.999624
vergaderingen vergadering 0.999540
( ( /
beslissing beslissing /
budget budget /
2008 2008 /
) ) /

"""
