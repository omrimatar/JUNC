from pulp import *


#לקבל נתונים מבעיה ב ומאקסל
# הדפסה סלקטיבית לנתונים לתוך אקסל

#לבצע פורלופים לכתיבה תמציתית?



#משתני אינפוט. בעתיד יגיע מאקסל

def c_optimization(car_sum,instructions,nataz,solver):
    for n in range(28):
        if nataz[n] > 0 and nataz[n] < 9:
            nataz[n] = 50
    capacity= instructions[0]

    NlSlallowed = instructions[1]
    ElWlallowed = instructions[2]
    E_image_enables = instructions[3]
    F_image_enables = instructions[4]
    #עדכון מיוחד לתנועות מיוחדות לרק"ל

    if instructions[8]== 1:
        lrt_junction_ns=1
    else: lrt_junction_ns=0
    if instructions[8] == 2:
        lrt_junction_nse = 1
    else:
        lrt_junction_nse = 0
    if instructions[8] == 3:
        lrt_junction_nsw = 1
    else:
        lrt_junction_nsw = 0


    if instructions[9]== 1:
        lrt_junction_ew=1
    else: lrt_junction_ew=0
    if instructions[9] == 2:
        lrt_junction_ewn = 1
    else:
        lrt_junction_ewn = 0
    if instructions[9] == 3:
        lrt_junction_ews = 1
    else:
        lrt_junction_ews = 0

    if instructions[8] == 4 and instructions[9]== 4:
        lrt_junction_ne=1
    else:
        lrt_junction_ne = 0

    if instructions[8] == 5 and instructions[9] == 5:
        lrt_junction_es = 1
    else:
        lrt_junction_es = 0

    if instructions[8] == 6 and instructions[9] == 6:
        lrt_junction_sw = 1
    else:
        lrt_junction_sw = 0

    if instructions[8] == 7 and instructions[9] == 7:
        lrt_junction_wn = 1
    else:
        lrt_junction_wn = 0



    Nr = max(car_sum[0],nataz[0])
    Nrt= max(car_sum[1],nataz[1])
    Nt = max(car_sum[2],nataz[2])
    Ntl = max(car_sum[3],nataz[3])
    Nl = max(car_sum[4],nataz[4])
    Nrtl = max(car_sum[5],nataz[5])
    Nrl = max(car_sum[6],nataz[6])

    Sr = max(car_sum[7],nataz[7])
    Srt= max(car_sum[8],nataz[8])
    St = max(car_sum[9],nataz[9])
    Stl = max(car_sum[10],nataz[10])
    Sl = max(car_sum[11],nataz[11])
    Srtl = max(car_sum[12],nataz[12])
    Srl = max(car_sum[13],nataz[13])

    Er = max(car_sum[14],nataz[14])
    Ert= max(car_sum[15],nataz[15])
    Et = max(car_sum[16],nataz[16])
    Etl = max(car_sum[17],nataz[17])
    El = max(car_sum[18],nataz[18])
    Ertl = max(car_sum[19],nataz[19])
    Erl = max(car_sum[20],nataz[20])

    Wr = max(car_sum[21],nataz[21])
    Wrt= max(car_sum[22],nataz[22])
    Wt = max(car_sum[23],nataz[23])
    Wtl =max(car_sum[24],nataz[24])
    Wl = max(car_sum[25],nataz[25])
    Wrtl = max(car_sum[26],nataz[26])
    Wrl = max(car_sum[27],nataz[27])



    prob = LpProblem("image_optimization", LpMinimize)

    #images variables

    imageA = LpVariable('imageA', 0, 10000, LpInteger)
    imageB = LpVariable('imageB', 0, 10000, LpInteger)
    imageC = LpVariable('imageC', 0, 10000, LpInteger)
    imageD = LpVariable('imageD', 0, 10000, LpInteger)
    imageE = LpVariable('imageE', 0, 10000, LpInteger)
    imageF = LpVariable('imageF', 0, 10000, LpInteger)


    #imagepresence check

    imageCcheck = LpVariable('tmunaCcheck', 0, 1, LpBinary)
    imageDcheck = LpVariable('tmunaDcheck', 0, 1, LpBinary)
    imageEcheck = LpVariable('tmunaEcheck', 0, 1, LpBinary)
    imageFcheck = LpVariable('tmunaFcheck', 0, 1, LpBinary)



    #mofa variables
    #224 משתנים בשתי קטגוריות. 7 משתנים ב-4 כיווני השמיים ועבור כל אחת מארבע תמונות
    #imageA
    # north

    ANr = LpVariable('ANr', 0, 10000, LpInteger)
    ANrt = LpVariable('ANrt', 0, 10000, LpInteger)
    ANt = LpVariable('ANt', 0, 10000, LpInteger)
    ANtl = LpVariable('ANtl', 0, 10000, LpInteger)
    ANl = LpVariable('ANl', 0, 10000, LpInteger)
    ANrtl = LpVariable('ANrtl', 0, 10000, LpInteger)
    ANrl = LpVariable('ANrl', 0, 10000, LpInteger)

    # south

    ASr = LpVariable('ASr', 0, 10000, LpInteger)
    ASrt = LpVariable('ASrt', 0, 10000, LpInteger)
    ASt = LpVariable('ASt', 0, 10000, LpInteger)
    AStl = LpVariable('AStl', 0, 10000, LpInteger)
    ASl = LpVariable('ASl', 0, 10000, LpInteger)
    ASrtl = LpVariable('ASrtl', 0, 10000, LpInteger)
    ASrl = LpVariable('ASrl', 0, 10000, LpInteger)

    # east

    AEr = LpVariable('AEr', 0, 10000, LpInteger)
    AErt = LpVariable('AErt', 0, 10000, LpInteger)
    AEt = LpVariable('AEt', 0, 10000, LpInteger)
    AEtl = LpVariable('AEtl', 0, 10000, LpInteger)
    AEl = LpVariable('AEl', 0, 10000, LpInteger)
    AErtl = LpVariable('AErtl', 0, 10000, LpInteger)
    AErl = LpVariable('AErl', 0, 10000, LpInteger)

    # west

    AWr = LpVariable('AWr', 0, 10000, LpInteger)
    AWrt = LpVariable('AWrt', 0, 10000, LpInteger)
    AWt = LpVariable('AWt', 0, 10000, LpInteger)
    AWtl = LpVariable('AWtl', 0, 10000, LpInteger)
    AWl = LpVariable('AWl', 0, 10000, LpInteger)
    AWrtl = LpVariable('AWrtl', 0, 10000, LpInteger)
    AWrl = LpVariable('AWrl', 0, 10000, LpInteger)

    #conflicts

    # northconflicts

    ANrcheck = LpVariable('ANrcheck', 0, 1, LpBinary)
    ANrtcheck = LpVariable('ANrtcheck', 0, 1, LpBinary)
    ANtcheck = LpVariable('ANtcheck', 0, 1, LpBinary)
    ANtlcheck = LpVariable('ANtlcheck', 0, 1, LpBinary)
    ANlcheck = LpVariable('ANlcheck', 0, 1, LpBinary)
    ANrtlcheck = LpVariable('ANrtlcheck', 0, 1, LpBinary)
    ANrlcheck = LpVariable('ANrlcheck', 0, 1, LpBinary)

    # southconflicts

    ASrcheck = LpVariable('ASrcheck', 0, 1, LpBinary)
    ASrtcheck = LpVariable('ASrtcheck', 0, 1, LpBinary)
    AStcheck = LpVariable('AStcheck', 0, 1, LpBinary)
    AStlcheck = LpVariable('AStlcheck', 0, 1, LpBinary)
    ASlcheck = LpVariable('ASlcheck', 0, 1, LpBinary)
    ASrtlcheck = LpVariable('ASrtlcheck', 0, 1, LpBinary)
    ASrlcheck = LpVariable('ASrlcheck', 0, 1, LpBinary)

    # eastconflicts

    AErcheck = LpVariable('AErcheck', 0, 1, LpBinary)
    AErtcheck = LpVariable('AErtcheck', 0, 1, LpBinary)
    AEtcheck = LpVariable('AEtcheck', 0, 1, LpBinary)
    AEtlcheck = LpVariable('AEtlcheck', 0, 1, LpBinary)
    AElcheck = LpVariable('AElcheck', 0, 1, LpBinary)
    AErtlcheck = LpVariable('AErtlcheck', 0, 1, LpBinary)
    AErlcheck = LpVariable('AErlcheck', 0, 1, LpBinary)

    # westconflicts

    AWrcheck = LpVariable('AWrcheck', 0, 1, LpBinary)
    AWrtcheck = LpVariable('AWrtcheck', 0, 1, LpBinary)
    AWtcheck = LpVariable('AWtcheck', 0, 1, LpBinary)
    AWtlcheck = LpVariable('AWtlcheck', 0, 1, LpBinary)
    AWlcheck = LpVariable('AWlcheck', 0, 1, LpBinary)
    AWrtlcheck = LpVariable('AWrtlcheck', 0, 1, LpBinary)
    AWrlcheck = LpVariable('AWrlcheck', 0, 1, LpBinary)

    #IMAGEB

    BNr = LpVariable('BNr', 0, 10000, LpInteger)
    BNrt = LpVariable('BNrt', 0, 10000, LpInteger)
    BNt = LpVariable('BNt', 0, 10000, LpInteger)
    BNtl = LpVariable('BNtl', 0, 10000, LpInteger)
    BNl = LpVariable('BNl', 0, 10000, LpInteger)
    BNrtl = LpVariable('BNrtl', 0, 10000, LpInteger)
    BNrl = LpVariable('BNrl', 0, 10000, LpInteger)

    # south

    BSr = LpVariable('BSr', 0, 10000, LpInteger)
    BSrt = LpVariable('BSrt', 0, 10000, LpInteger)
    BSt = LpVariable('BSt', 0, 10000, LpInteger)
    BStl = LpVariable('BStl', 0, 10000, LpInteger)
    BSl = LpVariable('BSl', 0, 10000, LpInteger)
    BSrtl = LpVariable('BSrtl', 0, 10000, LpInteger)
    BSrl = LpVariable('BSrl', 0, 10000, LpInteger)

    # east

    BEr = LpVariable('BEr', 0, 10000, LpInteger)
    BErt = LpVariable('BErt', 0, 10000, LpInteger)
    BEt = LpVariable('BEt', 0, 10000, LpInteger)
    BEtl = LpVariable('BEtl', 0, 10000, LpInteger)
    BEl = LpVariable('BEl', 0, 10000, LpInteger)
    BErtl = LpVariable('BErtl', 0, 10000, LpInteger)
    BErl = LpVariable('BErl', 0, 10000, LpInteger)

    # west

    BWr = LpVariable('BWr', 0, 10000, LpInteger)
    BWrt = LpVariable('BWrt', 0, 10000, LpInteger)
    BWt = LpVariable('BWt', 0, 10000, LpInteger)
    BWtl = LpVariable('BWtl', 0, 10000, LpInteger)
    BWl = LpVariable('BWl', 0, 10000, LpInteger)
    BWrtl = LpVariable('BWrtl', 0, 10000, LpInteger)
    BWrl = LpVariable('BWrl', 0, 10000, LpInteger)

    #conflicts

    # northconflicts

    BNrcheck = LpVariable('BNrcheck', 0, 1, LpBinary)
    BNrtcheck = LpVariable('BNrtcheck', 0, 1, LpBinary)
    BNtcheck = LpVariable('BNtcheck', 0, 1, LpBinary)
    BNtlcheck = LpVariable('BNtlcheck', 0, 1, LpBinary)
    BNlcheck = LpVariable('BNlcheck', 0, 1, LpBinary)
    BNrtlcheck = LpVariable('BNrtlcheck', 0, 1, LpBinary)
    BNrlcheck = LpVariable('BNrlcheck', 0, 1, LpBinary)

    # southconflicts

    BSrcheck = LpVariable('BSrcheck', 0, 1, LpBinary)
    BSrtcheck = LpVariable('BSrtcheck', 0, 1, LpBinary)
    BStcheck = LpVariable('BStcheck', 0, 1, LpBinary)
    BStlcheck = LpVariable('BStlcheck', 0, 1, LpBinary)
    BSlcheck = LpVariable('BSlcheck', 0, 1, LpBinary)
    BSrtlcheck = LpVariable('BSrtlcheck', 0, 1, LpBinary)
    BSrlcheck = LpVariable('BSrlcheck', 0, 1, LpBinary)

    # eastconflicts

    BErcheck = LpVariable('BErcheck', 0, 1, LpBinary)
    BErtcheck = LpVariable('BErtcheck', 0, 1, LpBinary)
    BEtcheck = LpVariable('BEtcheck', 0, 1, LpBinary)
    BEtlcheck = LpVariable('BEtlcheck', 0, 1, LpBinary)
    BElcheck = LpVariable('BElcheck', 0, 1, LpBinary)
    BErtlcheck = LpVariable('BErtlcheck', 0, 1, LpBinary)
    BErlcheck = LpVariable('BErlcheck', 0, 1, LpBinary)

    # westconflicts

    BWrcheck = LpVariable('BWrcheck', 0, 1, LpBinary)
    BWrtcheck = LpVariable('BWrtcheck', 0, 1, LpBinary)
    BWtcheck = LpVariable('BWtcheck', 0, 1, LpBinary)
    BWtlcheck = LpVariable('BWtlcheck', 0, 1, LpBinary)
    BWlcheck = LpVariable('BWlcheck', 0, 1, LpBinary)
    BWrtlcheck = LpVariable('BWrtlcheck', 0, 1, LpBinary)
    BWrlcheck = LpVariable('BWrlcheck', 0, 1, LpBinary)

    #IMAGEC

    # north

    CNr = LpVariable('CNr', 0, 10000, LpInteger)
    CNrt = LpVariable('CNrt', 0, 10000, LpInteger)
    CNt = LpVariable('CNt', 0, 10000, LpInteger)
    CNtl = LpVariable('CNtl', 0, 10000, LpInteger)
    CNl = LpVariable('CNl', 0, 10000, LpInteger)
    CNrtl = LpVariable('CNrtl', 0, 10000, LpInteger)
    CNrl = LpVariable('CNrl', 0, 10000, LpInteger)

    # south

    CSr = LpVariable('CSr', 0, 10000, LpInteger)
    CSrt = LpVariable('CSrt', 0, 10000, LpInteger)
    CSt = LpVariable('CSt', 0, 10000, LpInteger)
    CStl = LpVariable('CStl', 0, 10000, LpInteger)
    CSl = LpVariable('CSl', 0, 10000, LpInteger)
    CSrtl = LpVariable('CSrtl', 0, 10000, LpInteger)
    CSrl = LpVariable('CSrl', 0, 10000, LpInteger)

    # east

    CEr = LpVariable('CEr', 0, 10000, LpInteger)
    CErt = LpVariable('CErt', 0, 10000, LpInteger)
    CEt = LpVariable('CEt', 0, 10000, LpInteger)
    CEtl = LpVariable('CEtl', 0, 10000, LpInteger)
    CEl = LpVariable('CEl', 0, 10000, LpInteger)
    CErtl = LpVariable('CErtl', 0, 10000, LpInteger)
    CErl = LpVariable('CErl', 0, 10000, LpInteger)

    # west

    CWr = LpVariable('CWr', 0, 10000, LpInteger)
    CWrt = LpVariable('CWrt', 0, 10000, LpInteger)
    CWt = LpVariable('CWt', 0, 10000, LpInteger)
    CWtl = LpVariable('CWtl', 0, 10000, LpInteger)
    CWl = LpVariable('CWl', 0, 10000, LpInteger)
    CWrtl = LpVariable('CWrtl', 0, 10000, LpInteger)
    CWrl = LpVariable('CWrl', 0, 10000, LpInteger)

    #conflicts

    # northconflicts

    CNrcheck = LpVariable('CNrcheck', 0, 1, LpBinary)
    CNrtcheck = LpVariable('CNrtcheck', 0, 1, LpBinary)
    CNtcheck = LpVariable('CNtcheck', 0, 1, LpBinary)
    CNtlcheck = LpVariable('CNtlcheck', 0, 1, LpBinary)
    CNlcheck = LpVariable('CNlcheck', 0, 1, LpBinary)
    CNrtlcheck = LpVariable('CNrtlcheck', 0, 1, LpBinary)
    CNrlcheck = LpVariable('CNrlcheck', 0, 1, LpBinary)

    # southconflicts

    CSrcheck = LpVariable('CSrcheck', 0, 1, LpBinary)
    CSrtcheck = LpVariable('CSrtcheck', 0, 1, LpBinary)
    CStcheck = LpVariable('CStcheck', 0, 1, LpBinary)
    CStlcheck = LpVariable('CStlcheck', 0, 1, LpBinary)
    CSlcheck = LpVariable('CSlcheck', 0, 1, LpBinary)
    CSrtlcheck = LpVariable('CSrtlcheck', 0, 1, LpBinary)
    CSrlcheck = LpVariable('CSrlcheck', 0, 1, LpBinary)

    # eastconflicts

    CErcheck = LpVariable('CErcheck', 0, 1, LpBinary)
    CErtcheck = LpVariable('CErtcheck', 0, 1, LpBinary)
    CEtcheck = LpVariable('CEtcheck', 0, 1, LpBinary)
    CEtlcheck = LpVariable('CEtlcheck', 0, 1, LpBinary)
    CElcheck = LpVariable('CElcheck', 0, 1, LpBinary)
    CErtlcheck = LpVariable('CErtlcheck', 0, 1, LpBinary)
    CErlcheck = LpVariable('CErlcheck', 0, 1, LpBinary)

    # westconflicts

    CWrcheck = LpVariable('CWrcheck', 0, 1, LpBinary)
    CWrtcheck = LpVariable('CWrtcheck', 0, 1, LpBinary)
    CWtcheck = LpVariable('CWtcheck', 0, 1, LpBinary)
    CWtlcheck = LpVariable('CWtlcheck', 0, 1, LpBinary)
    CWlcheck = LpVariable('CWlcheck', 0, 1, LpBinary)
    CWrtlcheck = LpVariable('CWrtlcheck', 0, 1, LpBinary)
    CWrlcheck = LpVariable('CWrlcheck', 0, 1, LpBinary)

    #IMAGE D
    # north

    DNr = LpVariable('DNr', 0, 10000, LpInteger)
    DNrt = LpVariable('DNrt', 0, 10000, LpInteger)
    DNt = LpVariable('DNt', 0, 10000, LpInteger)
    DNtl = LpVariable('DNtl', 0, 10000, LpInteger)
    DNl = LpVariable('DNl', 0, 10000, LpInteger)
    DNrtl = LpVariable('DNrtl', 0, 10000, LpInteger)
    DNrl = LpVariable('DNrl', 0, 10000, LpInteger)

    # south

    DSr = LpVariable('DSr', 0, 10000, LpInteger)
    DSrt = LpVariable('DSrt', 0, 10000, LpInteger)
    DSt = LpVariable('DSt', 0, 10000, LpInteger)
    DStl = LpVariable('DStl', 0, 10000, LpInteger)
    DSl = LpVariable('DSl', 0, 10000, LpInteger)
    DSrtl = LpVariable('DSrtl', 0, 10000, LpInteger)
    DSrl = LpVariable('DSrl', 0, 10000, LpInteger)

    # east

    DEr = LpVariable('DEr', 0, 10000, LpInteger)
    DErt = LpVariable('DErt', 0, 10000, LpInteger)
    DEt = LpVariable('DEt', 0, 10000, LpInteger)
    DEtl = LpVariable('DEtl', 0, 10000, LpInteger)
    DEl = LpVariable('DEl', 0, 10000, LpInteger)
    DErtl = LpVariable('DErtl', 0, 10000, LpInteger)
    DErl = LpVariable('DErl', 0, 10000, LpInteger)

    # west

    DWr = LpVariable('DWr', 0, 10000, LpInteger)
    DWrt = LpVariable('DWrt', 0, 10000, LpInteger)
    DWt = LpVariable('DWt', 0, 10000, LpInteger)
    DWtl = LpVariable('DWtl', 0, 10000, LpInteger)
    DWl = LpVariable('DWl', 0, 10000, LpInteger)
    DWrtl = LpVariable('DWrtl', 0, 10000, LpInteger)
    DWrl = LpVariable('DWrl', 0, 10000, LpInteger)

    #conflicts

    # northconflicts

    DNrcheck = LpVariable('DNrcheck', 0, 1, LpBinary)
    DNrtcheck = LpVariable('DNrtcheck', 0, 1, LpBinary)
    DNtcheck = LpVariable('DNtcheck', 0, 1, LpBinary)
    DNtlcheck = LpVariable('DNtlcheck', 0, 1, LpBinary)
    DNlcheck = LpVariable('DNlcheck', 0, 1, LpBinary)
    DNrtlcheck = LpVariable('DNrtlcheck', 0, 1, LpBinary)
    DNrlcheck = LpVariable('DNrlcheck', 0, 1, LpBinary)

    # southconflicts

    DSrcheck = LpVariable('DSrcheck', 0, 1, LpBinary)
    DSrtcheck = LpVariable('DSrtcheck', 0, 1, LpBinary)
    DStcheck = LpVariable('DStcheck', 0, 1, LpBinary)
    DStlcheck = LpVariable('DStlcheck', 0, 1, LpBinary)
    DSlcheck = LpVariable('DSlcheck', 0, 1, LpBinary)
    DSrtlcheck = LpVariable('DSrtlcheck', 0, 1, LpBinary)
    DSrlcheck = LpVariable('DSrlcheck', 0, 1, LpBinary)

    # eastconflicts

    DErcheck = LpVariable('DErcheck', 0, 1, LpBinary)
    DErtcheck = LpVariable('DErtcheck', 0, 1, LpBinary)
    DEtcheck = LpVariable('DEtcheck', 0, 1, LpBinary)
    DEtlcheck = LpVariable('DEtlcheck', 0, 1, LpBinary)
    DElcheck = LpVariable('DElcheck', 0, 1, LpBinary)
    DErtlcheck = LpVariable('DErtlcheck', 0, 1, LpBinary)
    DErlcheck = LpVariable('DErlcheck', 0, 1, LpBinary)

    # westconflicts

    DWrcheck = LpVariable('DWrcheck', 0, 1, LpBinary)
    DWrtcheck = LpVariable('DWrtcheck', 0, 1, LpBinary)
    DWtcheck = LpVariable('DWtcheck', 0, 1, LpBinary)
    DWtlcheck = LpVariable('DWtlcheck', 0, 1, LpBinary)
    DWlcheck = LpVariable('DWlcheck', 0, 1, LpBinary)
    DWrtlcheck = LpVariable('DWrtlcheck', 0, 1, LpBinary)
    DWrlcheck = LpVariable('DWrlcheck', 0, 1, LpBinary)


    ENr = LpVariable('ENr', 0, 10000, LpInteger)
    ENrt = LpVariable('ENrt', 0, 10000, LpInteger)
    ENt = LpVariable('ENt', 0, 10000, LpInteger)
    ENtl = LpVariable('ENtl', 0, 10000, LpInteger)
    ENl = LpVariable('ENl', 0, 10000, LpInteger)
    ENrtl = LpVariable('ENrtl', 0, 10000, LpInteger)
    ENrl = LpVariable('ENrl', 0, 10000, LpInteger)

    # south

    ESr = LpVariable('ESr', 0, 10000, LpInteger)
    ESrt = LpVariable('ESrt', 0, 10000, LpInteger)
    ESt = LpVariable('ESt', 0, 10000, LpInteger)
    EStl = LpVariable('EStl', 0, 10000, LpInteger)
    ESl = LpVariable('ESl', 0, 10000, LpInteger)
    ESrtl = LpVariable('ESrtl', 0, 10000, LpInteger)
    ESrl = LpVariable('ESrl', 0, 10000, LpInteger)

    # east

    EEr = LpVariable('EEr', 0, 10000, LpInteger)
    EErt = LpVariable('EErt', 0, 10000, LpInteger)
    EEt = LpVariable('EEt', 0, 10000, LpInteger)
    EEtl = LpVariable('EEtl', 0, 10000, LpInteger)
    EEl = LpVariable('EEl', 0, 10000, LpInteger)
    EErtl = LpVariable('EErtl', 0, 10000, LpInteger)
    EErl = LpVariable('EErl', 0, 10000, LpInteger)

    # west

    EWr = LpVariable('EWr', 0, 10000, LpInteger)
    EWrt = LpVariable('EWrt', 0, 10000, LpInteger)
    EWt = LpVariable('EWt', 0, 10000, LpInteger)
    EWtl = LpVariable('EWtl', 0, 10000, LpInteger)
    EWl = LpVariable('EWl', 0, 10000, LpInteger)
    EWrtl = LpVariable('EWrtl', 0, 10000, LpInteger)
    EWrl = LpVariable('EWrl', 0, 10000, LpInteger)

    # conflicts

    # northconflicts

    ENrcheck = LpVariable('ENrcheck', 0, 1, LpBinary)
    ENrtcheck = LpVariable('ENrtcheck', 0, 1, LpBinary)
    ENtcheck = LpVariable('ENtcheck', 0, 1, LpBinary)
    ENtlcheck = LpVariable('ENtlcheck', 0, 1, LpBinary)
    ENlcheck = LpVariable('ENlcheck', 0, 1, LpBinary)
    ENrtlcheck = LpVariable('ENrtlcheck', 0, 1, LpBinary)
    ENrlcheck = LpVariable('ENrlcheck', 0, 1, LpBinary)

    # southconflicts

    ESrcheck = LpVariable('ESrcheck', 0, 1, LpBinary)
    ESrtcheck = LpVariable('ESrtcheck', 0, 1, LpBinary)
    EStcheck = LpVariable('EStcheck', 0, 1, LpBinary)
    EStlcheck = LpVariable('EStlcheck', 0, 1, LpBinary)
    ESlcheck = LpVariable('ESlcheck', 0, 1, LpBinary)
    ESrtlcheck = LpVariable('ESrtlcheck', 0, 1, LpBinary)
    ESrlcheck = LpVariable('ESrlcheck', 0, 1, LpBinary)

    # eastconflicts

    EErcheck = LpVariable('EErcheck', 0, 1, LpBinary)
    EErtcheck = LpVariable('EErtcheck', 0, 1, LpBinary)
    EEtcheck = LpVariable('EEtcheck', 0, 1, LpBinary)
    EEtlcheck = LpVariable('EEtlcheck', 0, 1, LpBinary)
    EElcheck = LpVariable('EElcheck', 0, 1, LpBinary)
    EErtlcheck = LpVariable('EErtlcheck', 0, 1, LpBinary)
    EErlcheck = LpVariable('EErlcheck', 0, 1, LpBinary)

    # westconflicts

    EWrcheck = LpVariable('EWrcheck', 0, 1, LpBinary)
    EWrtcheck = LpVariable('EWrtcheck', 0, 1, LpBinary)
    EWtcheck = LpVariable('EWtcheck', 0, 1, LpBinary)
    EWtlcheck = LpVariable('EWtlcheck', 0, 1, LpBinary)
    EWlcheck = LpVariable('EWlcheck', 0, 1, LpBinary)
    EWrtlcheck = LpVariable('EWrtlcheck', 0, 1, LpBinary)
    EWrlcheck = LpVariable('EWrlcheck', 0, 1, LpBinary)

    FNr = LpVariable('FNr', 0, 10000, LpInteger)
    FNrt = LpVariable('FNrt', 0, 10000, LpInteger)
    FNt = LpVariable('FNt', 0, 10000, LpInteger)
    FNtl = LpVariable('FNtl', 0, 10000, LpInteger)
    FNl = LpVariable('FNl', 0, 10000, LpInteger)
    FNrtl = LpVariable('FNrtl', 0, 10000, LpInteger)
    FNrl = LpVariable('FNrl', 0, 10000, LpInteger)

    # south

    FSr = LpVariable('FSr', 0, 10000, LpInteger)
    FSrt = LpVariable('FSrt', 0, 10000, LpInteger)
    FSt = LpVariable('FSt', 0, 10000, LpInteger)
    FStl = LpVariable('FStl', 0, 10000, LpInteger)
    FSl = LpVariable('FSl', 0, 10000, LpInteger)
    FSrtl = LpVariable('FSrtl', 0, 10000, LpInteger)
    FSrl = LpVariable('FSrl', 0, 10000, LpInteger)

    # east

    FEr = LpVariable('FEr', 0, 10000, LpInteger)
    FErt = LpVariable('FErt', 0, 10000, LpInteger)
    FEt = LpVariable('FEt', 0, 10000, LpInteger)
    FEtl = LpVariable('FEtl', 0, 10000, LpInteger)
    FEl = LpVariable('FEl', 0, 10000, LpInteger)
    FErtl = LpVariable('FErtl', 0, 10000, LpInteger)
    FErl = LpVariable('FErl', 0, 10000, LpInteger)

    # west

    FWr = LpVariable('FWr', 0, 10000, LpInteger)
    FWrt = LpVariable('FWrt', 0, 10000, LpInteger)
    FWt = LpVariable('FWt', 0, 10000, LpInteger)
    FWtl = LpVariable('FWtl', 0, 10000, LpInteger)
    FWl = LpVariable('FWl', 0, 10000, LpInteger)
    FWrtl = LpVariable('FWrtl', 0, 10000, LpInteger)
    FWrl = LpVariable('FWrl', 0, 10000, LpInteger)

    # conflicts

    # northconflicts

    FNrcheck = LpVariable('FNrcheck', 0, 1, LpBinary)
    FNrtcheck = LpVariable('FNrtcheck', 0, 1, LpBinary)
    FNtcheck = LpVariable('FNtcheck', 0, 1, LpBinary)
    FNtlcheck = LpVariable('FNtlcheck', 0, 1, LpBinary)
    FNlcheck = LpVariable('FNlcheck', 0, 1, LpBinary)
    FNrtlcheck = LpVariable('FNrtlcheck', 0, 1, LpBinary)
    FNrlcheck = LpVariable('FNrlcheck', 0, 1, LpBinary)

    # southconflicts

    FSrcheck = LpVariable('FSrcheck', 0, 1, LpBinary)
    FSrtcheck = LpVariable('FSrtcheck', 0, 1, LpBinary)
    FStcheck = LpVariable('FStcheck', 0, 1, LpBinary)
    FStlcheck = LpVariable('FStlcheck', 0, 1, LpBinary)
    FSlcheck = LpVariable('FSlcheck', 0, 1, LpBinary)
    FSrtlcheck = LpVariable('FSrtlcheck', 0, 1, LpBinary)
    FSrlcheck = LpVariable('FSrlcheck', 0, 1, LpBinary)

    # eastconflicts

    FErcheck = LpVariable('FErcheck', 0, 1, LpBinary)
    FErtcheck = LpVariable('FErtcheck', 0, 1, LpBinary)
    FEtcheck = LpVariable('FEtcheck', 0, 1, LpBinary)
    FEtlcheck = LpVariable('FEtlcheck', 0, 1, LpBinary)
    FElcheck = LpVariable('FElcheck', 0, 1, LpBinary)
    FErtlcheck = LpVariable('FErtlcheck', 0, 1, LpBinary)
    FErlcheck = LpVariable('FErlcheck', 0, 1, LpBinary)

    # westconflicts

    FWrcheck = LpVariable('FWrcheck', 0, 1, LpBinary)
    FWrtcheck = LpVariable('FWrtcheck', 0, 1, LpBinary)
    FWtcheck = LpVariable('FWtcheck', 0, 1, LpBinary)
    FWtlcheck = LpVariable('FWtlcheck', 0, 1, LpBinary)
    FWlcheck = LpVariable('FWlcheck', 0, 1, LpBinary)
    FWrtlcheck = LpVariable('FWrtlcheck', 0, 1, LpBinary)
    FWrlcheck = LpVariable('FWrlcheck', 0, 1, LpBinary)

    # target function

    prob += 0.99*imageA + imageB + imageC + imageD+imageE+imageF +50*imageCcheck+51*imageDcheck+52*imageEcheck+53*imageFcheck


    # PROB
    # תמונה היא המשך המקסימלי של מופע

    prob += imageA >= ANr
    prob += imageA >= ANrt
    prob += imageA >= ANt
    prob += imageA >= ANtl
    prob += imageA >= ANl
    prob += imageA >= ANrtl
    prob += imageA >= ANrl

    prob += imageA >= ASr
    prob += imageA >= ASrt
    prob += imageA >= ASt
    prob += imageA >= AStl
    prob += imageA >= ASl
    prob += imageA >= ASrtl
    prob += imageA >= ASrl

    prob += imageA >= AEr
    prob += imageA >= AErt
    prob += imageA >= AEt
    prob += imageA >= AEtl
    prob += imageA >= AEl
    prob += imageA >= AErtl
    prob += imageA >= AErl

    prob += imageA >= AWr
    prob += imageA >= AWrt
    prob += imageA >= AWt
    prob += imageA >= AWtl
    prob += imageA >= AWl
    prob += imageA >= AWrtl
    prob += imageA >= AWrl

    prob += imageB >= BNr
    prob += imageB >= BNrt
    prob += imageB >= BNt
    prob += imageB >= BNtl
    prob += imageB >= BNl
    prob += imageB >= BNrtl
    prob += imageB >= BNrl

    prob += imageB >= BSr
    prob += imageB >= BSrt
    prob += imageB >= BSt
    prob += imageB >= BStl
    prob += imageB >= BSl
    prob += imageB >= BSrtl
    prob += imageB >= BSrl

    prob += imageB >= BEr
    prob += imageB >= BErt
    prob += imageB >= BEt
    prob += imageB >= BEtl
    prob += imageB >= BEl
    prob += imageB >= BErtl
    prob += imageB >= BErl

    prob += imageB >= BWr
    prob += imageB >= BWrt
    prob += imageB >= BWt
    prob += imageB >= BWtl
    prob += imageB >= BWl
    prob += imageB >= BWrtl
    prob += imageB >= BWrl


    prob += imageC >= CNr
    prob += imageC >= CNrt
    prob += imageC >= CNt
    prob += imageC >= CNtl
    prob += imageC >= CNl
    prob += imageC >= CNrtl
    prob += imageC >= CNrl

    prob += imageC >= CSr
    prob += imageC >= CSrt
    prob += imageC >= CSt
    prob += imageC >= CStl
    prob += imageC >= CSl
    prob += imageC >= CSrtl
    prob += imageC >= CSrl

    prob += imageC >= CEr
    prob += imageC >= CErt
    prob += imageC >= CEt
    prob += imageC >= CEtl
    prob += imageC >= CEl
    prob += imageC >= CErtl
    prob += imageC >= CErl

    prob += imageC >= CWr
    prob += imageC >= CWrt
    prob += imageC >= CWt
    prob += imageC >= CWtl
    prob += imageC >= CWl
    prob += imageC >= CWrtl
    prob += imageC >= CWrl

    prob += imageD >= DNr
    prob += imageD >= DNrt
    prob += imageD >= DNt
    prob += imageD >= DNtl
    prob += imageD >= DNl
    prob += imageD >= DNrtl
    prob += imageD >= DNrl

    prob += imageD >= DSr
    prob += imageD >= DSrt
    prob += imageD >= DSt
    prob += imageD >= DStl
    prob += imageD >= DSl
    prob += imageD >= DSrtl
    prob += imageD >= DSrl

    prob += imageD >= DEr
    prob += imageD >= DErt
    prob += imageD >= DEt
    prob += imageD >= DEtl
    prob += imageD >= DEl
    prob += imageD >= DErtl
    prob += imageD >= DErl

    prob += imageD >= DWr
    prob += imageD >= DWrt
    prob += imageD >= DWt
    prob += imageD >= DWtl
    prob += imageD >= DWl
    prob += imageD >= DWrtl
    prob += imageD >= DWrl


    # אם המופע אינו בצ'ק אז הוא 0

    prob += ANr <= 10000* ANrcheck
    prob += ANrt <= 10000* ANrtcheck
    prob += ANt <= 10000* ANtcheck
    prob += ANtl <= 10000* ANtlcheck
    prob += ANl <= 10000* ANlcheck
    prob += ANrtl <= 10000* ANrtlcheck
    prob += ANrl <= 10000* ANrlcheck

    prob += ASr <= 10000* ASrcheck
    prob += ASrt <= 10000* ASrtcheck
    prob += ASt <= 10000* AStcheck
    prob += AStl <= 10000* AStlcheck
    prob += ASl <= 10000* ASlcheck
    prob += ASrtl <= 10000* ASrtlcheck
    prob += ASrl <= 10000* ASrlcheck

    prob += AEr <= 10000* AErcheck
    prob += AErt <= 10000* AErtcheck
    prob += AEt <= 10000* AEtcheck
    prob += AEtl <= 10000* AEtlcheck
    prob += AEl <= 10000* AElcheck
    prob += AErtl <= 10000* AErtlcheck
    prob += AErl <= 10000* AErlcheck

    prob += AWr <= 10000* AWrcheck
    prob += AWrt <= 10000* AWrtcheck
    prob += AWt <= 10000* AWtcheck
    prob += AWtl <= 10000* AWtlcheck
    prob += AWl <= 10000* AWlcheck
    prob += AWrtl <= 10000* AWrtlcheck
    prob += AWrl <= 10000* AWrlcheck

    prob += BNr <= 10000* BNrcheck
    prob += BNrt <= 10000* BNrtcheck
    prob += BNt <= 10000* BNtcheck
    prob += BNtl <= 10000* BNtlcheck
    prob += BNl <= 10000* BNlcheck
    prob += BNrtl <= 10000* BNrtlcheck
    prob += BNrl <= 10000* BNrlcheck

    prob += BSr <= 10000* BSrcheck
    prob += BSrt <= 10000* BSrtcheck
    prob += BSt <= 10000* BStcheck
    prob += BStl <= 10000* BStlcheck
    prob += BSl <= 10000* BSlcheck
    prob += BSrtl <= 10000* BSrtlcheck
    prob += BSrl <= 10000* BSrlcheck

    prob += BEr <= 10000* BErcheck
    prob += BErt <= 10000* BErtcheck
    prob += BEt <= 10000* BEtcheck
    prob += BEtl <= 10000* BEtlcheck
    prob += BEl <= 10000* BElcheck
    prob += BErtl <= 10000* BErtlcheck
    prob += BErl <= 10000* BErlcheck

    prob += BWr <= 10000* BWrcheck
    prob += BWrt <= 10000* BWrtcheck
    prob += BWt <= 10000* BWtcheck
    prob += BWtl <= 10000* BWtlcheck
    prob += BWl <= 10000* BWlcheck
    prob += BWrtl <= 10000* BWrtlcheck
    prob += BWrl <= 10000* BWrlcheck

    prob += CNr <= 10000* CNrcheck
    prob += CNrt <= 10000* CNrtcheck
    prob += CNt <= 10000* CNtcheck
    prob += CNtl <= 10000* CNtlcheck
    prob += CNl <= 10000* CNlcheck
    prob += CNrtl <= 10000* CNrtlcheck
    prob += CNrl <= 10000* CNrlcheck

    prob += CSr <= 10000* CSrcheck
    prob += CSrt <= 10000* CSrtcheck
    prob += CSt <= 10000* CStcheck
    prob += CStl <= 10000* CStlcheck
    prob += CSl <= 10000* CSlcheck
    prob += CSrtl <= 10000* CSrtlcheck
    prob += CSrl <= 10000* CSrlcheck

    prob += CEr <= 10000* CErcheck
    prob += CErt <= 10000* CErtcheck
    prob += CEt <= 10000* CEtcheck
    prob += CEtl <= 10000* CEtlcheck
    prob += CEl <= 10000* CElcheck
    prob += CErtl <= 10000* CErtlcheck
    prob += CErl <= 10000* CErlcheck

    prob += CWr <= 10000* CWrcheck
    prob += CWrt <= 10000* CWrtcheck
    prob += CWt <= 10000* CWtcheck
    prob += CWtl <= 10000* CWtlcheck
    prob += CWl <= 10000* CWlcheck
    prob += CWrtl <= 10000* CWrtlcheck
    prob += CWrl <= 10000* CWrlcheck

    prob += DNr <= 10000* DNrcheck
    prob += DNrt <= 10000* DNrtcheck
    prob += DNt <= 10000* DNtcheck
    prob += DNtl <= 10000* DNtlcheck
    prob += DNl <= 10000* DNlcheck
    prob += DNrtl <= 10000* DNrtlcheck
    prob += DNrl <= 10000* DNrlcheck

    prob += DSr <= 10000* DSrcheck
    prob += DSrt <= 10000* DSrtcheck
    prob += DSt <= 10000* DStcheck
    prob += DStl <= 10000* DStlcheck
    prob += DSl <= 10000* DSlcheck
    prob += DSrtl <= 10000* DSrtlcheck
    prob += DSrl <= 10000* DSrlcheck

    prob += DEr <= 10000* DErcheck
    prob += DErt <= 10000* DErtcheck
    prob += DEt <= 10000* DEtcheck
    prob += DEtl <= 10000* DEtlcheck
    prob += DEl <= 10000* DElcheck
    prob += DErtl <= 10000* DErtlcheck
    prob += DErl <= 10000* DErlcheck

    prob += DWr <= 10000* DWrcheck
    prob += DWrt <= 10000* DWrtcheck
    prob += DWt <= 10000* DWtcheck
    prob += DWtl <= 10000* DWtlcheck
    prob += DWl <= 10000* DWlcheck
    prob += DWrtl <= 10000* DWrtlcheck
    prob += DWrl <= 10000* DWrlcheck



    # על פני כל התמונות, כל נפח הפנייה עובר
    prob += ANr+BNr+CNr+DNr+ENr+FNr == Nr
    prob += ANrt+BNrt+CNrt+DNrt+ENrt+FNrt == Nrt
    prob += ANt+BNt+CNt+DNt+ENt+FNt == Nt
    prob += ANtl+BNtl+CNtl+DNtl+ENtl+FNtl == Ntl
    prob += ANl+BNl+CNl+DNl+ENl+FNl == Nl
    prob += ANrtl+BNrtl+CNrtl+DNrtl+ENrtl+FNrtl == Nrtl
    prob += ANrl+BNrl+CNrl+DNrl+ENrl+FNrl == Nrl

    prob += ASr + BSr + CSr + DSr + ESr + FSr == Sr
    prob += ASrt + BSrt + CSrt + DSrt + ESrt + FSrt == Srt
    prob += ASt + BSt + CSt + DSt + ESt + FSt == St
    prob += AStl + BStl + CStl + DStl + EStl + FStl == Stl
    prob += ASl + BSl + CSl + DSl + ESl + FSl == Sl
    prob += ASrtl + BSrtl + CSrtl + DSrtl + ESrtl + FSrtl == Srtl
    prob += ASrl + BSrl + CSrl + DSrl + ESrl + FSrl == Srl

    prob += AEr + BEr + CEr + DEr + EEr + FEr == Er
    prob += AErt + BErt + CErt + DErt + EErt + FErt == Ert
    prob += AEt + BEt + CEt + DEt + EEt + FEt == Et
    prob += AEtl + BEtl + CEtl + DEtl + EEtl + FEtl == Etl
    prob += AEl + BEl + CEl + DEl + EEl + FEl == El
    prob += AErtl + BErtl + CErtl + DErtl + EErtl + FErtl == Ertl
    prob += AErl + BErl + CErl + DErl + EErl + FErl == Erl

    prob += AWr + BWr + CWr + DWr + EWr + FWr == Wr
    prob += AWrt + BWrt + CWrt + DWrt + EWrt + FWrt == Wrt
    prob += AWt + BWt + CWt + DWt + EWt + FWt == Wt
    prob += AWtl + BWtl + CWtl + DWtl + EWtl + FWtl == Wtl
    prob += AWl + BWl + CWl + DWl + EWl + FWl == Wl
    prob += AWrtl + BWrtl + CWrtl + DWrtl + EWrtl + FWrtl == Wrtl
    prob += AWrl + BWrl + CWrl + DWrl + EWrl + FWrl == Wrl

    #  בדיקה לקיום תמונות מרובות לצורך קנס

    prob += 10000*imageCcheck >=  imageC
    prob += 10000*imageDcheck >=  imageD
    prob += 10000*imageEcheck >=  imageE
    prob += 10000*imageFcheck >=  imageF




    #conflicts

    #קונפליקטיים תמידיים תנועה מורכבת מתאפשרת רק אם תנועה פשוטה ממנה אפשרית

    # ימין
    if Nrt > 0:
        prob += ANrtcheck == ANrcheck

    if Nrtl > 0:
        prob += ANrtlcheck == ANrcheck

    if Nrl > 0:
        prob += ANrlcheck == ANrcheck

    if Srt > 0:
        prob += ASrtcheck == ASrcheck
    if Srtl > 0:
        prob += ASrtlcheck == ASrcheck
    if Srl > 0:
        prob += ASrlcheck == ASrcheck

    if Ert > 0:
        prob += AErtcheck == AErcheck
    if Ertl > 0:
        prob += AErtlcheck == AErcheck
    if Erl > 0:
        prob += AErlcheck == AErcheck
    if Wrt > 0:
        prob += AWrtcheck == AWrcheck
    if Wrtl > 0:
        prob += AWrtlcheck == AWrcheck
    if Wrl > 0:
        prob += AWrlcheck == AWrcheck

    # ישר

    if Nrt > 0:
        prob += ANrtcheck == ANtcheck
    if Nrtl > 0:
        prob += ANrtlcheck == ANtcheck
    if Ntl > 0:
        prob += ANtlcheck == ANtcheck

    if Srt > 0:
        prob += ASrtcheck == AStcheck
    if Srtl > 0:
        prob += ASrtlcheck == AStcheck
    if Stl > 0:
        prob += AStlcheck == AStcheck

    if Ert > 0:
        prob += AErtcheck == AEtcheck
    if Ertl > 0:
        prob += AErtlcheck == AEtcheck
    if Etl > 0:
        prob += AEtlcheck == AEtcheck

    if Wrt > 0:
        prob += AWrtcheck == AWtcheck
    if Wrtl > 0:
        prob += AWrtlcheck == AWtcheck
    if Wtl > 0:
        prob += AWtlcheck == AWtcheck

    # שמאלה

    if Ntl > 0:
        prob += ANtlcheck == ANlcheck
    if Nrtl > 0:
        prob += ANrtlcheck == ANlcheck
    if Nrl > 0:
        prob += ANrlcheck == ANlcheck

    if Stl > 0:
        prob += AStlcheck == ASlcheck
    if Srtl > 0:
        prob += ASrtlcheck == ASlcheck
    if Srl > 0:
        prob += ASrlcheck == ASlcheck

    if Etl > 0:
        prob += AEtlcheck == AElcheck
    if Ertl > 0:
        prob += AErtlcheck == AElcheck
    if Erl > 0:
        prob += AErlcheck == AElcheck

    if Wtl > 0:
        prob += AWtlcheck == AWlcheck
    if Wrtl > 0:
        prob += AWrtlcheck == AWlcheck
    if Wrl > 0:
        prob += AWrlcheck == AWlcheck


    # ימין
    if Nrt > 0:
        prob += BNrtcheck == BNrcheck

    if Nrtl > 0:
        prob += BNrtlcheck == BNrcheck

    if Nrl > 0:
        prob += BNrlcheck == BNrcheck

    if Srt > 0:
        prob += BSrtcheck == BSrcheck
    if Srtl > 0:
        prob += BSrtlcheck == BSrcheck
    if Srl > 0:
        prob += BSrlcheck == BSrcheck

    if Ert > 0:
        prob += BErtcheck == BErcheck
    if Ertl > 0:
        prob += BErtlcheck == BErcheck
    if Erl > 0:
        prob += BErlcheck == BErcheck
    if Wrt > 0:
        prob += BWrtcheck == BWrcheck
    if Wrtl > 0:
        prob += BWrtlcheck == BWrcheck
    if Wrl > 0:
        prob += BWrlcheck == BWrcheck

    # ישר

    if Nrt > 0:
        prob += BNrtcheck == BNtcheck
    if Nrtl > 0:
        prob += BNrtlcheck == BNtcheck
    if Ntl > 0:
        prob += BNtlcheck == BNtcheck

    if Srt > 0:
        prob += BSrtcheck == BStcheck
    if Srtl > 0:
        prob += BSrtlcheck == BStcheck
    if Stl > 0:
        prob += BStlcheck == BStcheck

    if Ert > 0:
        prob += BErtcheck == BEtcheck
    if Ertl > 0:
        prob += BErtlcheck == BEtcheck
    if Etl > 0:
        prob += BEtlcheck == BEtcheck

    if Wrt > 0:
        prob += BWrtcheck == BWtcheck
    if Wrtl > 0:
        prob += BWrtlcheck == BWtcheck
    if Wtl > 0:
        prob += BWtlcheck == BWtcheck

    # שמאלה

    if Ntl > 0:
        prob += BNtlcheck == BNlcheck
    if Nrtl > 0:
        prob += BNrtlcheck == BNlcheck
    if Nrl > 0:
        prob += BNrlcheck == BNlcheck

    if Stl > 0:
        prob += BStlcheck == BSlcheck
    if Srtl > 0:
        prob += BSrtlcheck == BSlcheck
    if Srl > 0:
        prob += BSrlcheck == BSlcheck

    if Etl > 0:
        prob += BEtlcheck == BElcheck
    if Ertl > 0:
        prob += BErtlcheck == BElcheck
    if Erl > 0:
        prob += BErlcheck == BElcheck

    if Wtl > 0:
        prob += BWtlcheck == BWlcheck
    if Wrtl > 0:
        prob += BWrtlcheck == BWlcheck
    if Wrl > 0:
        prob += BWrlcheck == BWlcheck

    # ימין
    if Nrt > 0:
        prob += CNrtcheck == CNrcheck

    if Nrtl > 0:
        prob += CNrtlcheck == CNrcheck

    if Nrl > 0:
        prob += CNrlcheck == CNrcheck

    if Srt > 0:
        prob += CSrtcheck == CSrcheck
    if Srtl > 0:
        prob += CSrtlcheck == CSrcheck
    if Srl > 0:
        prob += CSrlcheck == CSrcheck

    if Ert > 0:
        prob += CErtcheck == CErcheck
    if Ertl > 0:
        prob += CErtlcheck == CErcheck
    if Erl > 0:
        prob += CErlcheck == CErcheck
    if Wrt > 0:
        prob += CWrtcheck == CWrcheck
    if Wrtl > 0:
        prob += CWrtlcheck == CWrcheck
    if Wrl > 0:
        prob += CWrlcheck == CWrcheck

    # ישר

    if Nrt > 0:
        prob += CNrtcheck == CNtcheck
    if Nrtl > 0:
        prob += CNrtlcheck == CNtcheck
    if Ntl > 0:
        prob += CNtlcheck == CNtcheck

    if Srt > 0:
        prob += CSrtcheck == CStcheck
    if Srtl > 0:
        prob += CSrtlcheck == CStcheck
    if Stl > 0:
        prob += CStlcheck == CStcheck

    if Ert > 0:
        prob += CErtcheck == CEtcheck
    if Ertl > 0:
        prob += CErtlcheck == CEtcheck
    if Etl > 0:
        prob += CEtlcheck == CEtcheck

    if Wrt > 0:
        prob += CWrtcheck == CWtcheck
    if Wrtl > 0:
        prob += CWrtlcheck == CWtcheck
    if Wtl > 0:
        prob += CWtlcheck == CWtcheck

    # שמאלה

    if Ntl > 0:
        prob += CNtlcheck == CNlcheck
    if Nrtl > 0:
        prob += CNrtlcheck == CNlcheck
    if Nrl > 0:
        prob += CNrlcheck == CNlcheck

    if Stl > 0:
        prob += CStlcheck == CSlcheck
    if Srtl > 0:
        prob += CSrtlcheck == CSlcheck
    if Srl > 0:
        prob += CSrlcheck == CSlcheck

    if Etl > 0:
        prob += CEtlcheck == CElcheck
    if Ertl > 0:
        prob += CErtlcheck == CElcheck
    if Erl > 0:
        prob += CErlcheck == CElcheck

    if Wtl > 0:
        prob += CWtlcheck == CWlcheck
    if Wrtl > 0:
        prob += CWrtlcheck == CWlcheck
    if Wrl > 0:
        prob += CWrlcheck == CWlcheck

    # ימין
    if Nrt > 0:
        prob += DNrtcheck == DNrcheck

    if Nrtl > 0:
        prob += DNrtlcheck == DNrcheck

    if Nrl > 0:
        prob += DNrlcheck == DNrcheck

    if Srt > 0:
        prob += DSrtcheck == DSrcheck
    if Srtl > 0:
        prob += DSrtlcheck == DSrcheck
    if Srl > 0:
        prob += DSrlcheck == DSrcheck

    if Ert > 0:
        prob += DErtcheck == DErcheck
    if Ertl > 0:
        prob += DErtlcheck == DErcheck
    if Erl > 0:
        prob += DErlcheck == DErcheck
    if Wrt > 0:
        prob += DWrtcheck == DWrcheck
    if Wrtl > 0:
        prob += DWrtlcheck == DWrcheck
    if Wrl > 0:
        prob += DWrlcheck == DWrcheck

    # ישר

    if Nrt > 0:
        prob += DNrtcheck == DNtcheck
    if Nrtl > 0:
        prob += DNrtlcheck == DNtcheck
    if Ntl > 0:
        prob += DNtlcheck == DNtcheck

    if Srt > 0:
        prob += DSrtcheck == DStcheck
    if Srtl > 0:
        prob += DSrtlcheck == DStcheck
    if Stl > 0:
        prob += DStlcheck == DStcheck

    if Ert > 0:
        prob += DErtcheck == DEtcheck
    if Ertl > 0:
        prob += DErtlcheck == DEtcheck
    if Etl > 0:
        prob += DEtlcheck == DEtcheck

    if Wrt > 0:
        prob += DWrtcheck == DWtcheck
    if Wrtl > 0:
        prob += DWrtlcheck == DWtcheck
    if Wtl > 0:
        prob += DWtlcheck == DWtcheck

    # שמאלה

    if Ntl > 0:
        prob += DNtlcheck == DNlcheck
    if Nrtl > 0:
        prob += DNrtlcheck == DNlcheck
    if Nrl > 0:
        prob += DNrlcheck == DNlcheck

    if Stl > 0:
        prob += DStlcheck == DSlcheck
    if Srtl > 0:
        prob += DSrtlcheck == DSlcheck
    if Srl > 0:
        prob += DSrlcheck == DSlcheck

    if Etl > 0:
        prob += DEtlcheck == DElcheck
    if Ertl > 0:
        prob += DErtlcheck == DElcheck
    if Erl > 0:
        prob += DErlcheck == DElcheck

    if Wtl > 0:
        prob += DWtlcheck == DWlcheck
    if Wrtl > 0:
        prob += DWrtlcheck == DWlcheck
    if Wrl > 0:
        prob += DWrlcheck == DWlcheck

    #קונפליקטים אמיתיים- תנועות ראשיות בלבד

    prob += ASlcheck+AWtcheck <=1
    prob += ASlcheck+AWlcheck <=1
    prob += ASlcheck+ANrcheck <=1
    prob += ASlcheck+ANtcheck <=1
    prob += ASlcheck+ANlcheck <= NlSlallowed+1
    prob += ASlcheck+AEtcheck <=1
    prob += ASlcheck+AElcheck <=1

    prob += AStcheck+AWtcheck <=1
    prob += AStcheck+AWlcheck <=1
    prob += AStcheck+ANlcheck <=1
    prob += AStcheck+AEtcheck <=1
    prob += AStcheck+AErcheck <=1
    prob += AStcheck+AElcheck <=1

    prob += ASrcheck+AWtcheck <=1
    prob += ASrcheck+ANlcheck <=1

    prob += AElcheck+AWrcheck <=1
    prob += AElcheck+AWtcheck <=1
    prob += AElcheck+AWlcheck <= ElWlallowed+1
    prob += AElcheck+ANtcheck <=1
    prob += AElcheck+ANlcheck <=1

    prob += AEtcheck+AWlcheck <=1
    prob += AEtcheck+ANrcheck <=1
    prob += AEtcheck+ANtcheck <=1
    prob += AEtcheck+ANlcheck <=1

    prob += AErcheck+AWlcheck <=1

    prob += ANlcheck+AWtcheck <=1
    prob += ANlcheck+AWlcheck <=1

    prob += ANtcheck+AWrcheck <=1
    prob += ANtcheck+AWtcheck <=1
    prob += ANtcheck+AWlcheck <=1

    prob += BSlcheck+BWtcheck <=1
    prob += BSlcheck+BWlcheck <=1
    prob += BSlcheck+BNrcheck <=1
    prob += BSlcheck+BNtcheck <=1
    prob += BSlcheck+BNlcheck <= NlSlallowed+1
    prob += BSlcheck+BEtcheck <=1
    prob += BSlcheck+BElcheck <=1

    prob += BStcheck+BWtcheck <=1
    prob += BStcheck+BWlcheck <=1
    prob += BStcheck+BNlcheck <=1
    prob += BStcheck+BEtcheck <=1
    prob += BStcheck+BErcheck <=1
    prob += BStcheck+BElcheck <=1

    prob += BSrcheck+BWtcheck <=1
    prob += BSrcheck+BNlcheck <=1

    prob += BElcheck+BWrcheck <=1
    prob += BElcheck+BWtcheck <=1
    prob += BElcheck+BWlcheck <= ElWlallowed+1
    prob += BElcheck+BNtcheck <=1
    prob += BElcheck+BNlcheck <=1

    prob += BEtcheck+BWlcheck <=1
    prob += BEtcheck+BNrcheck <=1
    prob += BEtcheck+BNtcheck <=1
    prob += BEtcheck+BNlcheck <=1

    prob += BErcheck+BWlcheck <=1

    prob += BNlcheck+BWtcheck <=1
    prob += BNlcheck+BWlcheck <=1

    prob += BNtcheck+BWrcheck <=1
    prob += BNtcheck+BWtcheck <=1
    prob += BNtcheck+BWlcheck <=1

    prob += CSlcheck+CWtcheck <=1
    prob += CSlcheck+CWlcheck <=1
    prob += CSlcheck+CNrcheck <=1
    prob += CSlcheck+CNtcheck <=1
    prob += CSlcheck+CNlcheck <= NlSlallowed+1
    prob += CSlcheck+CEtcheck <=1
    prob += CSlcheck+CElcheck <=1

    prob += CStcheck+CWtcheck <=1
    prob += CStcheck+CWlcheck <=1
    prob += CStcheck+CNlcheck <=1
    prob += CStcheck+CEtcheck <=1
    prob += CStcheck+CErcheck <=1
    prob += CStcheck+CElcheck <=1

    prob += CSrcheck+CWtcheck <=1
    prob += CSrcheck+CNlcheck <=1

    prob += CElcheck+CWrcheck <=1
    prob += CElcheck+CWtcheck <=1
    prob += CElcheck+CWlcheck <= ElWlallowed+1
    prob += CElcheck+CNtcheck <=1
    prob += CElcheck+CNlcheck <=1

    prob += CEtcheck+CWlcheck <=1
    prob += CEtcheck+CNrcheck <=1
    prob += CEtcheck+CNtcheck <=1
    prob += CEtcheck+CNlcheck <=1

    prob += CErcheck+CWlcheck <=1

    prob += CNlcheck+CWtcheck <=1
    prob += CNlcheck+CWlcheck <=1

    prob += CNtcheck+CWrcheck <=1
    prob += CNtcheck+CWtcheck <=1
    prob += CNtcheck+CWlcheck <=1

    prob += DSlcheck+DWtcheck <=1
    prob += DSlcheck+DWlcheck <=1
    prob += DSlcheck+DNrcheck <=1
    prob += DSlcheck+DNtcheck <=1
    prob += DSlcheck+DNlcheck <= NlSlallowed+1
    prob += DSlcheck+DEtcheck <=1
    prob += DSlcheck+DElcheck <=1

    prob += DStcheck+DWtcheck <=1
    prob += DStcheck+DWlcheck <=1
    prob += DStcheck+DNlcheck <=1
    prob += DStcheck+DEtcheck <=1
    prob += DStcheck+DErcheck <=1
    prob += DStcheck+DElcheck <=1

    prob += DSrcheck+DWtcheck <=1
    prob += DSrcheck+DNlcheck <=1

    prob += DElcheck+DWrcheck <=1
    prob += DElcheck+DWtcheck <=1
    prob += DElcheck+DWlcheck <= ElWlallowed+1
    prob += DElcheck+DNtcheck <=1
    prob += DElcheck+DNlcheck <=1

    prob += DEtcheck+DWlcheck <=1
    prob += DEtcheck+DNrcheck <=1
    prob += DEtcheck+DNtcheck <=1
    prob += DEtcheck+DNlcheck <=1

    prob += DErcheck+DWlcheck <=1

    prob += DNlcheck+DWtcheck <=1
    prob += DNlcheck+DWlcheck <=1

    prob += DNtcheck+DWrcheck <=1
    prob += DNtcheck+DWtcheck <=1
    prob += DNtcheck+DWlcheck <=1

    # תמונה חמישית ושישית
    if E_image_enables == 0:
        prob+=imageEcheck==0
    if F_image_enables == 0 or E_image_enables == 0:
        prob+=imageFcheck==0

    prob += imageE >= ENr
    prob += imageE >= ENrt
    prob += imageE >= ENt
    prob += imageE >= ENtl
    prob += imageE >= ENl
    prob += imageE >= ENrtl
    prob += imageE >= ENrl

    prob += imageE >= ESr
    prob += imageE >= ESrt
    prob += imageE >= ESt
    prob += imageE >= EStl
    prob += imageE >= ESl
    prob += imageE >= ESrtl
    prob += imageE >= ESrl

    prob += imageE >= EEr
    prob += imageE >= EErt
    prob += imageE >= EEt
    prob += imageE >= EEtl
    prob += imageE >= EEl
    prob += imageE >= EErtl
    prob += imageE >= EErl

    prob += imageE >= EWr
    prob += imageE >= EWrt
    prob += imageE >= EWt
    prob += imageE >= EWtl
    prob += imageE >= EWl
    prob += imageE >= EWrtl
    prob += imageE >= EWrl

    # אם המופע אינו בצ'ק אז הוא 0

    prob += ENr <= 10000 * ENrcheck
    prob += ENrt <= 10000 * ENrtcheck
    prob += ENt <= 10000 * ENtcheck
    prob += ENtl <= 10000 * ENtlcheck
    prob += ENl <= 10000 * ENlcheck
    prob += ENrtl <= 10000 * ENrtlcheck
    prob += ENrl <= 10000 * ENrlcheck

    prob += ESr <= 10000 * ESrcheck
    prob += ESrt <= 10000 * ESrtcheck
    prob += ESt <= 10000 * EStcheck
    prob += EStl <= 10000 * EStlcheck
    prob += ESl <= 10000 * ESlcheck
    prob += ESrtl <= 10000 * ESrtlcheck
    prob += ESrl <= 10000 * ESrlcheck

    prob += EEr <= 10000 * EErcheck
    prob += EErt <= 10000 * EErtcheck
    prob += EEt <= 10000 * EEtcheck
    prob += EEtl <= 10000 * EEtlcheck
    prob += EEl <= 10000 * EElcheck
    prob += EErtl <= 10000 * EErtlcheck
    prob += EErl <= 10000 * EErlcheck

    prob += EWr <= 10000 * EWrcheck
    prob += EWrt <= 10000 * EWrtcheck
    prob += EWt <= 10000 * EWtcheck
    prob += EWtl <= 10000 * EWtlcheck
    prob += EWl <= 10000 * EWlcheck
    prob += EWrtl <= 10000 * EWrtlcheck
    prob += EWrl <= 10000 * EWrlcheck

    # ימין
    if Nrt > 0:
        prob += ENrtcheck == ENrcheck

    if Nrtl > 0:
        prob += ENrtlcheck == ENrcheck

    if Nrl > 0:
        prob += ENrlcheck == ENrcheck

    if Srt > 0:
        prob += ESrtcheck == ESrcheck
    if Srtl > 0:
        prob += ESrtlcheck == ESrcheck
    if Srl > 0:
        prob += ESrlcheck == ESrcheck

    if Ert > 0:
        prob += EErtcheck == EErcheck
    if Ertl > 0:
        prob += EErtlcheck == EErcheck
    if Erl > 0:
        prob += EErlcheck == EErcheck
    if Wrt > 0:
        prob += EWrtcheck == EWrcheck
    if Wrtl > 0:
        prob += EWrtlcheck == EWrcheck
    if Wrl > 0:
        prob += EWrlcheck == EWrcheck

    # ישר

    if Nrt > 0:
        prob += ENrtcheck == ENtcheck
    if Nrtl > 0:
        prob += ENrtlcheck == ENtcheck
    if Ntl > 0:
        prob += ENtlcheck == ENtcheck

    if Srt > 0:
        prob += ESrtcheck == EStcheck
    if Srtl > 0:
        prob += ESrtlcheck == EStcheck
    if Stl > 0:
        prob += EStlcheck == EStcheck

    if Ert > 0:
        prob += EErtcheck == EEtcheck
    if Ertl > 0:
        prob += EErtlcheck == EEtcheck
    if Etl > 0:
        prob += EEtlcheck == EEtcheck

    if Wrt > 0:
        prob += EWrtcheck == EWtcheck
    if Wrtl > 0:
        prob += EWrtlcheck == EWtcheck
    if Wtl > 0:
        prob += EWtlcheck == EWtcheck

    # שמאלה

    if Ntl > 0:
        prob += ENtlcheck == ENlcheck
    if Nrtl > 0:
        prob += ENrtlcheck == ENlcheck
    if Nrl > 0:
        prob += ENrlcheck == ENlcheck

    if Stl > 0:
        prob += EStlcheck == ESlcheck
    if Srtl > 0:
        prob += ESrtlcheck == ESlcheck
    if Srl > 0:
        prob += ESrlcheck == ESlcheck

    if Etl > 0:
        prob += EEtlcheck == EElcheck
    if Ertl > 0:
        prob += EErtlcheck == EElcheck
    if Erl > 0:
        prob += EErlcheck == EElcheck

    if Wtl > 0:
        prob += EWtlcheck == EWlcheck
    if Wrtl > 0:
        prob += EWrtlcheck == EWlcheck
    if Wrl > 0:
        prob += EWrlcheck == EWlcheck

    # קונפליקטים אמיתיים- תנועות ראשיות בלבד

    prob += ESlcheck + EWtcheck <= 1
    prob += ESlcheck + EWlcheck <= 1
    prob += ESlcheck + ENrcheck <= 1
    prob += ESlcheck + ENtcheck <= 1
    prob += ESlcheck + ENlcheck <= NlSlallowed + 1
    prob += ESlcheck + EEtcheck <= 1
    prob += ESlcheck + EElcheck <= 1

    prob += EStcheck + EWtcheck <= 1
    prob += EStcheck + EWlcheck <= 1
    prob += EStcheck + ENlcheck <= 1
    prob += EStcheck + EEtcheck <= 1
    prob += EStcheck + EErcheck <= 1
    prob += EStcheck + EElcheck <= 1

    prob += ESrcheck + EWtcheck <= 1
    prob += ESrcheck + ENlcheck <= 1

    prob += EElcheck + EWrcheck <= 1
    prob += EElcheck + EWtcheck <= 1
    prob += EElcheck + EWlcheck <= ElWlallowed + 1
    prob += EElcheck + ENtcheck <= 1
    prob += EElcheck + ENlcheck <= 1

    prob += EEtcheck + EWlcheck <= 1
    prob += EEtcheck + ENrcheck <= 1
    prob += EEtcheck + ENtcheck <= 1
    prob += EEtcheck + ENlcheck <= 1

    prob += EErcheck + EWlcheck <= 1

    prob += ENlcheck + EWtcheck <= 1
    prob += ENlcheck + EWlcheck <= 1

    prob += ENtcheck + EWrcheck <= 1
    prob += ENtcheck + EWtcheck <= 1
    prob += ENtcheck + EWlcheck <= 1



    prob += imageF >= FNr
    prob += imageF >= FNrt
    prob += imageF >= FNt
    prob += imageF >= FNtl
    prob += imageF >= FNl
    prob += imageF >= FNrtl
    prob += imageF >= FNrl

    prob += imageF >= FSr
    prob += imageF >= FSrt
    prob += imageF >= FSt
    prob += imageF >= FStl
    prob += imageF >= FSl
    prob += imageF >= FSrtl
    prob += imageF >= FSrl

    prob += imageF >= FEr
    prob += imageF >= FErt
    prob += imageF >= FEt
    prob += imageF >= FEtl
    prob += imageF >= FEl
    prob += imageF >= FErtl
    prob += imageF >= FErl

    prob += imageF >= FWr
    prob += imageF >= FWrt
    prob += imageF >= FWt
    prob += imageF >= FWtl
    prob += imageF >= FWl
    prob += imageF >= FWrtl
    prob += imageF >= FWrl

    # אם המופע אינו בצ'ק אז הוא 0

    prob += FNr <= 10000 * FNrcheck
    prob += FNrt <= 10000 * FNrtcheck
    prob += FNt <= 10000 * FNtcheck
    prob += FNtl <= 10000 * FNtlcheck
    prob += FNl <= 10000 * FNlcheck
    prob += FNrtl <= 10000 * FNrtlcheck
    prob += FNrl <= 10000 * FNrlcheck

    prob += FSr <= 10000 * FSrcheck
    prob += FSrt <= 10000 * FSrtcheck
    prob += FSt <= 10000 * FStcheck
    prob += FStl <= 10000 * FStlcheck
    prob += FSl <= 10000 * FSlcheck
    prob += FSrtl <= 10000 * FSrtlcheck
    prob += FSrl <= 10000 * FSrlcheck

    prob += FEr <= 10000 * FErcheck
    prob += FErt <= 10000 * FErtcheck
    prob += FEt <= 10000 * FEtcheck
    prob += FEtl <= 10000 * FEtlcheck
    prob += FEl <= 10000 * FElcheck
    prob += FErtl <= 10000 * FErtlcheck
    prob += FErl <= 10000 * FErlcheck

    prob += FWr <= 10000 * FWrcheck
    prob += FWrt <= 10000 * FWrtcheck
    prob += FWt <= 10000 * FWtcheck
    prob += FWtl <= 10000 * FWtlcheck
    prob += FWl <= 10000 * FWlcheck
    prob += FWrtl <= 10000 * FWrtlcheck
    prob += FWrl <= 10000 * FWrlcheck

    # ימין
    if Nrt > 0:
        prob += FNrtcheck == FNrcheck

    if Nrtl > 0:
        prob += FNrtlcheck == FNrcheck

    if Nrl > 0:
        prob += FNrlcheck == FNrcheck

    if Srt > 0:
        prob += FSrtcheck == FSrcheck
    if Srtl > 0:
        prob += FSrtlcheck == FSrcheck
    if Srl > 0:
        prob += FSrlcheck == FSrcheck

    if Ert > 0:
        prob += FErtcheck == FErcheck
    if Ertl > 0:
        prob += FErtlcheck == FErcheck
    if Erl > 0:
        prob += FErlcheck == FErcheck
    if Wrt > 0:
        prob += FWrtcheck == FWrcheck
    if Wrtl > 0:
        prob += FWrtlcheck == FWrcheck
    if Wrl > 0:
        prob += FWrlcheck == FWrcheck

    # ישר

    if Nrt > 0:
        prob += FNrtcheck == FNtcheck
    if Nrtl > 0:
        prob += FNrtlcheck == FNtcheck
    if Ntl > 0:
        prob += FNtlcheck == FNtcheck

    if Srt > 0:
        prob += FSrtcheck == FStcheck
    if Srtl > 0:
        prob += FSrtlcheck == FStcheck
    if Stl > 0:
        prob += FStlcheck == FStcheck

    if Ert > 0:
        prob += FErtcheck == FEtcheck
    if Ertl > 0:
        prob += FErtlcheck == FEtcheck
    if Etl > 0:
        prob += FEtlcheck == FEtcheck

    if Wrt > 0:
        prob += FWrtcheck == FWtcheck
    if Wrtl > 0:
        prob += FWrtlcheck == FWtcheck
    if Wtl > 0:
        prob += FWtlcheck == FWtcheck

    # שמאלה

    if Ntl > 0:
        prob += FNtlcheck == FNlcheck
    if Nrtl > 0:
        prob += FNrtlcheck == FNlcheck
    if Nrl > 0:
        prob += FNrlcheck == FNlcheck

    if Stl > 0:
        prob += FStlcheck == FSlcheck
    if Srtl > 0:
        prob += FSrtlcheck == FSlcheck
    if Srl > 0:
        prob += FSrlcheck == FSlcheck

    if Etl > 0:
        prob += FEtlcheck == FElcheck
    if Ertl > 0:
        prob += FErtlcheck == FElcheck
    if Erl > 0:
        prob += FErlcheck == FElcheck

    if Wtl > 0:
        prob += FWtlcheck == FWlcheck
    if Wrtl > 0:
        prob += FWrtlcheck == FWlcheck
    if Wrl > 0:
        prob += FWrlcheck == FWlcheck

    # קונפליקטים אמיתיים- תנועות ראשיות בלבד

    prob += FSlcheck + FWtcheck <= 1
    prob += FSlcheck + FWlcheck <= 1
    prob += FSlcheck + FNrcheck <= 1
    prob += FSlcheck + FNtcheck <= 1
    prob += FSlcheck + FNlcheck <= NlSlallowed + 1
    prob += FSlcheck + FEtcheck <= 1
    prob += FSlcheck + FElcheck <= 1

    prob += FStcheck + FWtcheck <= 1
    prob += FStcheck + FWlcheck <= 1
    prob += FStcheck + FNlcheck <= 1
    prob += FStcheck + FEtcheck <= 1
    prob += FStcheck + FErcheck <= 1
    prob += FStcheck + FElcheck <= 1

    prob += FSrcheck + FWtcheck <= 1
    prob += FSrcheck + FNlcheck <= 1

    prob += FElcheck + FWrcheck <= 1
    prob += FElcheck + FWtcheck <= 1
    prob += FElcheck + FWlcheck <= ElWlallowed + 1
    prob += FElcheck + FNtcheck <= 1
    prob += FElcheck + FNlcheck <= 1

    prob += FEtcheck + FWlcheck <= 1
    prob += FEtcheck + FNrcheck <= 1
    prob += FEtcheck + FNtcheck <= 1
    prob += FEtcheck + FNlcheck <= 1

    prob += FErcheck + FWlcheck <= 1

    prob += FNlcheck + FWtcheck <= 1
    prob += FNlcheck + FWlcheck <= 1

    prob += FNtcheck + FWrcheck <= 1
    prob += FNtcheck + FWtcheck <= 1
    prob += FNtcheck + FWlcheck <= 1









#קונפליקטים לרקל
    #קונפליקטNS
    prob += lrt_junction_ns + AWtcheck <= 1
    prob += lrt_junction_ns + AWlcheck <= 1
    prob += lrt_junction_ns + ANlcheck <= 1
    prob += lrt_junction_ns + AEtcheck <= 1
   # prob += lrt_junction_ns + AErcheck <= 1
    prob += lrt_junction_ns + AElcheck <= 1
    prob += lrt_junction_ns + ASlcheck <= 1
    #prob += lrt_junction_ns + AWrcheck <= 1

    # קונפליקט EW

    prob += ASlcheck+lrt_junction_ew <=1
    prob += AStcheck+lrt_junction_ew <=1
    prob += lrt_junction_ew + AWlcheck <= 1
   # prob += lrt_junction_ew + ANrcheck <= 1
    prob += lrt_junction_ew + ANtcheck <= 1
    prob += lrt_junction_ew + ANlcheck <= 1
    #prob += ASrcheck+lrt_junction_ew <=1
    prob += AElcheck + lrt_junction_ew <= 1


    # עדכון קונפליקטים מיוחדים לרקל

    # קונפליקט מיוחד EW כאשר רכבת צדית מצפון

    prob += lrt_junction_ewn + AErcheck <= 1
    prob += lrt_junction_ewn + ANtcheck <= 1
    prob += lrt_junction_ewn + ANrcheck <= 1
    prob += lrt_junction_ewn + ANlcheck <= 1
    prob += lrt_junction_ewn + AStcheck <= 1
    prob += lrt_junction_ewn + AWlcheck <= 1

    # קונפליקט מיוחד EW כאשר רכבת צדית מדרום

    prob += lrt_junction_ews + AWrcheck <= 1
    prob += lrt_junction_ews + AStcheck <= 1
    prob += lrt_junction_ews + ASrcheck <= 1
    prob += lrt_junction_ews + ASlcheck <= 1
    prob += lrt_junction_ews + ANtcheck <= 1
    prob += lrt_junction_ews + AElcheck <= 1

    # קונפליקט מיוחד NS כאשר רכבת צדית ממזרח

    prob += lrt_junction_nse + ASrcheck <= 1
    prob += lrt_junction_nse + AEtcheck <= 1
    prob += lrt_junction_nse + AErcheck <= 1
    prob += lrt_junction_nse + AElcheck <= 1
    prob += lrt_junction_nse + AWtcheck <= 1
    prob += lrt_junction_nse + ANlcheck <= 1


    # קונפליקט מיוחד NS כאשר רכבת צדית ממערב


    prob += lrt_junction_nsw + ANrcheck <= 1
    prob += lrt_junction_nsw + AWtcheck <= 1
    prob += lrt_junction_nsw + AWrcheck <= 1
    prob += lrt_junction_nsw + AWlcheck <= 1
    prob += lrt_junction_nsw + AEtcheck <= 1
    prob += lrt_junction_nsw + ASlcheck <= 1


    # קונפליקט מיוחד  כאשר רכבת חוצה מצפון למזרח


    prob += lrt_junction_ne + AEtcheck <= 1
    prob += lrt_junction_ne + AElcheck <= 1
    prob += lrt_junction_ne + AWlcheck <= 1
    prob += lrt_junction_ne + AStcheck <= 1
    prob += lrt_junction_ne + ASlcheck <= 1


    # קונפליקט מיוחד  כאשר רכבת חוצה ממזרח לדרום

    prob += lrt_junction_es + AStcheck <= 1
    prob += lrt_junction_es + ASlcheck <= 1
    prob += lrt_junction_es + ANlcheck <= 1
    prob += lrt_junction_es + AWtcheck <= 1
    prob += lrt_junction_es + AWlcheck <= 1



    # קונפליקט מיוחד  כאשר רכבת חוצה מדרום למערב

    prob += lrt_junction_sw + ANtcheck <= 1
    prob += lrt_junction_sw + ANlcheck <= 1
    prob += lrt_junction_sw + AWlcheck <= 1
    prob += lrt_junction_sw + AWtcheck <= 1
    prob += lrt_junction_sw + AElcheck <= 1

    # קונפליקט מיוחד  כאשר רכבת חוצה ממערב לצפון

    prob += lrt_junction_wn + ANlcheck <= 1
    prob += lrt_junction_wn + ANtcheck <= 1
    prob += lrt_junction_wn + ASlcheck <= 1
    prob += lrt_junction_wn + AEtcheck <= 1
    prob += lrt_junction_wn + AElcheck <= 1



    #prob.solve()
    prob.solve(PULP_CBC_CMD(msg=False))
    print("Status:", LpStatus[prob.status])
    if LpStatus[prob.status] != "Optimal":
        raise ValueError(f"Solver did not find an optimal solution (status: {LpStatus[prob.status]})")
    v_over_c= (imageA.varValue + imageB.varValue + imageC.varValue + imageD.varValue+imageE.varValue+imageF.varValue) / (
                capacity - 50 * imageCcheck.varValue - 50 * imageDcheck.varValue-50*imageEcheck.varValue-50*imageFcheck.varValue -300)

    print("v/c=", v_over_c)
    if v_over_c <0.8:
        print("LOS C")
    elif v_over_c <0.9:
        print("LOS D")
    elif v_over_c <1:
        print("LOS E")
    else:
        print("LOS F")
    sum_of_images = imageA.varValue + imageB.varValue + imageC.varValue + imageD.varValue+imageE.varValue+imageF.varValue
    print("sum of images=",sum_of_images)
    return_pulp_vars = {}
    for v in prob.variables():
       if "image" in v.name or v.varValue > 1:
           #print(v.name, "=", v.varValue)
           return_pulp_vars[v.name] =  v.varValue

    images_values = [imageA.varValue,imageB.varValue,imageC.varValue,imageD.varValue,imageE.varValue,imageF.varValue]

    # Determine which phases B-F are LRT-compatible (contain no LRT-conflicting movements)
    _lrt_conflict_movements = []
    if lrt_junction_ns:
        _lrt_conflict_movements = ['Wtcheck', 'Wlcheck', 'Nlcheck', 'Etcheck', 'Elcheck', 'Slcheck']
    elif lrt_junction_ew:
        _lrt_conflict_movements = ['Slcheck', 'Stcheck', 'Wlcheck', 'Ntcheck', 'Nlcheck', 'Elcheck']
    elif lrt_junction_ewn:
        _lrt_conflict_movements = ['Ercheck', 'Ntcheck', 'Nrcheck', 'Nlcheck', 'Stcheck', 'Wlcheck']
    elif lrt_junction_ews:
        _lrt_conflict_movements = ['Wrcheck', 'Stcheck', 'Srcheck', 'Slcheck', 'Ntcheck', 'Elcheck']
    elif lrt_junction_nse:
        _lrt_conflict_movements = ['Srcheck', 'Etcheck', 'Ercheck', 'Elcheck', 'Wtcheck', 'Nlcheck']
    elif lrt_junction_nsw:
        _lrt_conflict_movements = ['Nrcheck', 'Wtcheck', 'Wrcheck', 'Wlcheck', 'Etcheck', 'Slcheck']
    elif lrt_junction_ne:
        _lrt_conflict_movements = ['Wtcheck', 'Wlcheck', 'Elcheck', 'Stcheck']
    elif lrt_junction_es:
        _lrt_conflict_movements = ['Stcheck', 'Slcheck', 'Nlcheck', 'Etcheck']
    elif lrt_junction_sw:
        _lrt_conflict_movements = ['Ntcheck', 'Wlcheck', 'Wtcheck', 'Elcheck']
    elif lrt_junction_wn:
        _lrt_conflict_movements = ['Wtcheck', 'Nlcheck', 'Ntcheck', 'Slcheck']

    lrt_compatible_phases = [True]  # Phase A is always LRT-compatible (enforced by constraints)
    if _lrt_conflict_movements:
        _check_vals = {v.name: v.varValue for v in prob.variables()
                       if v.name.endswith('check') and len(v.name) == 8}
        for phase in ['B', 'C', 'D', 'E', 'F']:
            hostile = any(_check_vals.get(phase + mov, 0) == 1 for mov in _lrt_conflict_movements)
            lrt_compatible_phases.append(not hostile)
    else:
        lrt_compatible_phases = [True] * 6  # No LRT active

    return v_over_c, sum_of_images, return_pulp_vars, images_values, lrt_compatible_phases


