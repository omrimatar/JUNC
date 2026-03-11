from pulp import *
from functools import reduce
from itertools import permutations
import ctypes

def n_choose_2(n):
    return int(reduce(lambda x, y: x * y[0] / y[1], zip(range(n - 2 + 1, n+1), range(1, 2+1)), 1))

def n_permutations_2(n):
    l = permutations(range(n),2)
    return [l1 for l1 in l if l1[0] < l1[1]]


DIRECTIONS = ['N','S','E','W']
LANE_TYPES = ['R','RT','T','TL','L','RTL','RL']



#EXCEL_FILENAME = 'criticalvolume.xlsx'


#נתוני ספירות תחזיות

def b_optimization(volume,lanes,nataz,solver):
    NcountR = round(volume[0],0)
    NcountT = round(volume[1],0)
    NcountL = round(volume[2],0)
    ScountR = round(volume[3],0)
    ScountT = round(volume[4],0)
    ScountL = round(volume[5],0)
    EcountR = round(volume[6],0)
    EcountT = round(volume[7],0)
    EcountL = round(volume[8],0)
    WcountR = round(volume[9],0)
    WcountT = round(volume[10],0)
    WcountL = round(volume[11],0)




    #נתוני ספירות /תחזיות

    NlanesR = lanes[0]
    NlanesRT = lanes[1]
    NlanesT = lanes[2]
    NlanesTL = lanes[3]
    NlanesL = lanes[4]
    NlanesRTL = lanes[5]
    NlanesRL = lanes[6]
    SlanesR = lanes[7]
    SlanesRT = lanes[8]
    SlanesT = lanes[9]
    SlanesTL = lanes[10]
    SlanesL = lanes[11]
    SlanesRTL = lanes[12]
    SlanesRL = lanes[13]
    ElanesR = lanes[14]
    ElanesRT = lanes[15]
    ElanesT = lanes[16]
    ElanesTL = lanes[17]
    ElanesL = lanes[18]
    ElanesRTL = lanes[19]
    ElanesRL = lanes[20]
    WlanesR = lanes[21]
    WlanesRT = lanes[22]
    WlanesT = lanes[23]
    WlanesTL = lanes[24]
    WlanesL = lanes[25]
    WlanesRTL = lanes[26]
    WlanesRL = lanes[27]

    lanes_count_dict = {}
    for i,d in enumerate(DIRECTIONS):
        lanes_count_dict[d] = {}
        for j,lt in enumerate(LANE_TYPES):
            lanes_count_dict[d][lt] = lanes[i *7 + j]

    #תוספת משתני נת"צ בינאריים ייחודיים עבור מקרה של נתיב מורכב שהוא נת"צ בחלקו בלבד

    NtrafficRTrbin=1
    NtrafficRLrbin=1
    NtrafficRTtbin=1
    NtrafficTLtbin=1
    NtrafficTLlbin=1
    NtrafficRLlbin=1
    NtrafficRTLrbin=1
    NtrafficRTLtbin=1
    NtrafficRTLlbin=1

    if nataz[1]==2:
        NtrafficRTrbin=0
    if nataz[1] == 3:
        NtrafficRTtbin=0
    if nataz[3]==3:
        NtrafficTLtbin=0
    if nataz[3]==4:
        NtrafficTLlbin=0
    if nataz[6]==2:
        NtrafficRLrbin=0
    if nataz[6]==4:
        NtrafficRLlbin=0

    if nataz[5] == 2 or nataz[5]==5 or nataz[5]==6:
        NtrafficRTLrbin=0
    if nataz[5] == 3 or nataz[5]==5 or nataz[5]==7:
        NtrafficRTLtbin=0
    if nataz[5] == 4 or nataz[5]==6 or nataz[5]==7:
        NtrafficRTLlbin=0

    StrafficRTrbin = 1
    StrafficRLrbin = 1
    StrafficRTtbin = 1
    StrafficTLtbin = 1
    StrafficTLlbin = 1
    StrafficRLlbin = 1
    StrafficRTLrbin = 1
    StrafficRTLtbin = 1
    StrafficRTLlbin = 1

    if nataz[8] == 2:
        StrafficRTrbin = 0
    if nataz[8] == 3:
        StrafficRTtbin = 0
    if nataz[10] == 3:
        StrafficTLtbin = 0
    if nataz[10] == 4:
        StrafficTLlbin = 0
    if nataz[13] == 2:
        StrafficRLrbin = 0
    if nataz[13] == 4:
        StrafficRLlbin = 0

    if nataz[12] == 2 or nataz[12] == 5 or nataz[12] == 6:
        StrafficRTLrbin = 0
    if nataz[12] == 3 or nataz[12] == 5 or nataz[12] == 7:
        StrafficRTLtbin = 0
    if nataz[12] == 4 or nataz[12] == 6 or nataz[12] == 7:
        StrafficRTLlbin = 0

    EtrafficRTrbin = 1
    EtrafficRLrbin = 1
    EtrafficRTtbin = 1
    EtrafficTLtbin = 1
    EtrafficTLlbin = 1
    EtrafficRLlbin = 1
    EtrafficRTLrbin = 1
    EtrafficRTLtbin = 1
    EtrafficRTLlbin = 1

    if nataz[15] == 2:
        EtrafficRTrbin = 0
    if nataz[15] == 3:
        EtrafficRTtbin = 0
    if nataz[17] == 3:
        EtrafficTLtbin = 0
    if nataz[17] == 4:
        EtrafficTLlbin = 0
    if nataz[20] == 2:
        EtrafficRLrbin = 0
    if nataz[20] == 4:
        EtrafficRLlbin = 0

    if nataz[19] == 2 or nataz[19] == 5 or nataz[19] == 6:
        EtrafficRTLrbin = 0
    if nataz[19] == 3 or nataz[19] == 5 or nataz[19] == 7:
        EtrafficRTLtbin = 0
    if nataz[19] == 4 or nataz[19] == 6 or nataz[19] == 7:
        EtrafficRTLlbin = 0

    WtrafficRTrbin = 1
    WtrafficRLrbin = 1
    WtrafficRTtbin = 1
    WtrafficTLtbin = 1
    WtrafficTLlbin = 1
    WtrafficRLlbin = 1
    WtrafficRTLrbin = 1
    WtrafficRTLtbin = 1
    WtrafficRTLlbin = 1

    if nataz[22] == 2:
        WtrafficRTrbin = 0
    if nataz[22] == 3:
        WtrafficRTtbin = 0
    if nataz[24] == 3:
        WtrafficTLtbin = 0
    if nataz[24] == 4:
        WtrafficTLlbin = 0
    if nataz[27] == 2:
        WtrafficRLrbin = 0
    if nataz[27] == 4:
        WtrafficRLlbin = 0

    if nataz[26] == 2 or nataz[26] == 5 or nataz[26] == 6:
        WtrafficRTLrbin = 0
    if nataz[26] == 3 or nataz[26] == 5 or nataz[26] == 7:
        WtrafficRTLtbin = 0
    if nataz[26] == 4 or nataz[26] == 6 or nataz[26] == 7:
        WtrafficRTLlbin = 0

    #ימינה חופשי מוגדר מעל 9 נתיבים
    error = 0
    message=0

    if NlanesR >= 9:
        if NcountR <900:
            NcountR = 0
        else:
            message = "north right turn dedicated lane exceed capacity"
    if SlanesR >= 9:
        if ScountR < 900:
            ScountR = 0
        else:
            message = "south right turn dedicated lane exceed capacity"
    if ElanesR >= 9:
        if EcountR < 900:
            EcountR = 0
        else:
            message = "east right turn dedicated lane exceed capacity"
    if WlanesR >= 9:
        if WcountR < 900:
            WcountR = 0
        else:
            message = "west right turn dedicated lane exceed capacity"

    if message !=0:
        print (message)
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, message, 'Phaser message', 1)

    # בדיקת שגיאות מספר נתיבים לא שלם
    for i in range (28):
        try:
            x = lanes[i]%1
            y= nataz[i]%1
        except:
            error= "number of lanes must be an integer"
            MessageBox = ctypes.windll.user32.MessageBoxW
            MessageBox(None, error, 'Phaser error', 0)
            exit()

        if x !=0 or y !=0:

            error= "number of lanes must be an integer"

    # בדיקת שגיאות קוד נת"צ שגוי
    if nataz[1] >3:
        error= "nataz coding error"
    if nataz[3]== 2 or nataz[3]>4:
        error= "nataz coding error"

    if nataz[6]==3 or nataz[6]>4:
        error = "nataz coding error"

    if nataz[5] >7:
        error = "nataz coding error"

    if nataz[8] > 3:
        error = "nataz coding error"
    if nataz[10] == 2 or nataz[3] > 4:
        error = "nataz coding error"

    if nataz[13] == 3 or nataz[6] > 4:
        error = "nataz coding error"

    if nataz[12] > 7:
        error = "nataz coding error"

    if nataz[15] > 3:
        error = "nataz coding error"
    if nataz[17] == 2 or nataz[3] > 4:
        error = "nataz coding error"

    if nataz[20] == 3 or nataz[6] > 4:
        error = "nataz coding error"

    if nataz[19] > 7:
        error = "nataz coding error"

    if nataz[22] > 3:
        error = "nataz coding error"
    if nataz[24] == 2 or nataz[3] > 4:
        error = "nataz coding error"

    if nataz[27] == 3 or nataz[6] > 4:
        error = "nataz coding error"

    if nataz[26] > 7:
        error = "nataz coding error"


    #בדיקת שגיאות יותר מנתיב מורכב אחד
    if NlanesRT>1 or NlanesRTL>1 or NlanesRL>1 or NlanesTL>1:
        error= "north routing is not possible- more then one complex lane"
    if SlanesRT>1 or SlanesRTL>1 or SlanesRL>1 or SlanesTL>1:
        error= "south routing is not possible- more then one complex lane"
    if ElanesRT>1 or ElanesRTL>1 or ElanesRL>1 or ElanesTL>1:
        error= "east routing is not possible- more then one complex lane"
    if WlanesRT>1 or WlanesRTL>1 or WlanesRL>1 or WlanesTL>1:
        error= "west routing is not possible- more then one complex lane"

    #בדיקת שגיאות עבור נפח בתנועה ללא נתיב מתאים (כולל נת"צ)
    if NlanesR+NlanesRT+NlanesRTL+NlanesRL +NtrafficRTrbin+NtrafficRTLrbin+NtrafficRLrbin-3 ==0 and NcountR>0:
        error= "missing north right turn"
    if NlanesT + NlanesRT + NlanesRTL + NlanesTL+NtrafficRTtbin+NtrafficRTLtbin+NtrafficTLtbin-3 == 0 and NcountT > 0:
        error="missing north through"
    if NlanesL + NlanesTL + NlanesRTL + NlanesRL+NtrafficTLlbin+NtrafficRTLlbin+NtrafficRLlbin-3 == 0 and NcountL > 0:
        error="missing north left turn"

    if SlanesR+SlanesRT+SlanesRTL+SlanesRL+StrafficRTrbin+StrafficRTLrbin+StrafficRLrbin-3==0 and ScountR>0:
        error="missing south right turn"
    if SlanesT + SlanesRT + SlanesRTL + SlanesTL+SlanesTL+StrafficRTtbin+StrafficRTLtbin+StrafficTLtbin-3 == 0 and ScountT > 0:
        error = "missing south through"
    if SlanesL + SlanesTL + SlanesRTL + SlanesRL+StrafficTLlbin+StrafficRTLlbin+StrafficRLlbin-3 == 0 and ScountL > 0:
        error= "missing south left turn"

    if ElanesR+ElanesRT+ElanesRTL+ElanesRL+EtrafficRTrbin+EtrafficRTLrbin+EtrafficRLrbin-3==0 and EcountR>0:
        error= "missing east right turn"
    if ElanesT + ElanesRT + ElanesRTL + ElanesTL+EtrafficRTtbin+EtrafficRTLtbin+EtrafficTLtbin-3 == 0 and EcountT > 0:
        error = "missing east through"
    if ElanesL + ElanesTL + ElanesRTL + ElanesRL+EtrafficTLlbin+EtrafficRTLlbin+EtrafficRLlbin-3 == 0 and EcountL > 0:
        error="missing east left turn"

    if WlanesR+WlanesRT+WlanesRTL+WlanesRL+WtrafficRTrbin+WtrafficRTLrbin+WtrafficRLrbin-3==0 and WcountR>0:
        error ="missing west right turn"
    if WlanesT + WlanesRT + WlanesRTL + WlanesTL+WtrafficRTtbin+WtrafficRTLtbin+WtrafficTLtbin-3 == 0 and WcountT > 0:
        error ="missing west through"
    if WlanesL + WlanesTL + WlanesRTL + WlanesRL+WtrafficTLlbin+WtrafficRTLlbin+WtrafficRLlbin-3 == 0 and WcountL > 0:
        error="missing west left turn"
    if error !=0:
        print (error)
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, error, 'Phaser error', 0)
        exit()

    prob = LpProblem("wardrop", LpMinimize)
    #משתני תנועה פנימיים. כמה פונים לכל כיוון ממי שנמצא בנתיב

    NtrafficRr = LpVariable('NtrafficRr', 0, 10000, LpInteger)
    NtrafficRTr = LpVariable('NtrafficRTr', 0, 10000, LpInteger)
    NtrafficRTt = LpVariable('NtrafficRTt', 0, 10000, LpInteger)
    NtrafficTt = LpVariable('NtrafficTt', 0, 10000, LpInteger)
    NtrafficTLt = LpVariable('NtrafficTLt', 0, 10000, LpInteger)
    NtrafficTLl = LpVariable('NtrafficTLl', 0, 10000, LpInteger)
    NtrafficLl = LpVariable('NtrafficLl', 0, 10000, LpInteger)
    NtrafficRTLr = LpVariable('NtrafficRTLr', 0, 10000, LpInteger)
    NtrafficRTLt = LpVariable('NtrafficRTLt', 0, 10000, LpInteger)
    NtrafficRTLl = LpVariable('NtrafficRTLl', 0, 10000, LpInteger)
    NtrafficRLr = LpVariable('NtrafficRLr', 0, 10000, LpInteger)
    NtrafficRLl = LpVariable('NtrafficRLl', 0, 10000, LpInteger)

    StrafficRr = LpVariable('StrafficRr', 0, 10000, LpInteger)
    StrafficRTr = LpVariable('StrafficRTr', 0, 10000, LpInteger)
    StrafficRTt = LpVariable('StrafficRTt', 0, 10000, LpInteger)
    StrafficTt = LpVariable('StrafficTt', 0, 10000, LpInteger)
    StrafficTLt = LpVariable('StrafficTLt', 0, 10000, LpInteger)
    StrafficTLl = LpVariable('StrafficTLl', 0, 10000, LpInteger)
    StrafficLl = LpVariable('StrafficLl', 0, 10000, LpInteger)
    StrafficRTLr = LpVariable('StrafficRTLr', 0, 10000, LpInteger)
    StrafficRTLt = LpVariable('StrafficRTLt', 0, 10000, LpInteger)
    StrafficRTLl = LpVariable('StrafficRTLl', 0, 10000, LpInteger)
    StrafficRLr = LpVariable('StrafficRLr', 0, 10000, LpInteger)
    StrafficRLl = LpVariable('StrafficRLl', 0, 10000, LpInteger)

    EtrafficRr = LpVariable('EtrafficRr', 0, 10000, LpInteger)
    EtrafficRTr = LpVariable('EtrafficRTr', 0, 10000, LpInteger)
    EtrafficRTt = LpVariable('EtrafficRTt', 0, 10000, LpInteger)
    EtrafficTt = LpVariable('EtrafficTt', 0, 10000, LpInteger)
    EtrafficTLt = LpVariable('EtrafficTLt', 0, 10000, LpInteger)
    EtrafficTLl = LpVariable('EtrafficTLl', 0, 10000, LpInteger)
    EtrafficLl = LpVariable('EtrafficLl', 0, 10000, LpInteger)
    EtrafficRTLr = LpVariable('EtrafficRTLr', 0, 10000, LpInteger)
    EtrafficRTLt = LpVariable('EtrafficRTLt', 0, 10000, LpInteger)
    EtrafficRTLl = LpVariable('EtrafficRTLl', 0, 10000, LpInteger)
    EtrafficRLr = LpVariable('EtrafficRLr', 0, 10000, LpInteger)
    EtrafficRLl = LpVariable('EtrafficRLl', 0, 10000, LpInteger)

    WtrafficRr = LpVariable('WtrafficRr', 0, 10000, LpInteger)
    WtrafficRTr = LpVariable('WtrafficRTr', 0, 10000, LpInteger)
    WtrafficRTt = LpVariable('WtrafficRTt', 0, 10000, LpInteger)
    WtrafficTt = LpVariable('WtrafficTt', 0, 10000, LpInteger)
    WtrafficTLt = LpVariable('WtrafficTLt', 0, 10000, LpInteger)
    WtrafficTLl = LpVariable('WtrafficTLl', 0, 10000, LpInteger)
    WtrafficLl = LpVariable('WtrafficLl', 0, 10000, LpInteger)
    WtrafficRTLr = LpVariable('WtrafficRTLr', 0, 10000, LpInteger)
    WtrafficRTLt = LpVariable('WtrafficRTLt', 0, 10000, LpInteger)
    WtrafficRTLl = LpVariable('WtrafficRTLl', 0, 10000, LpInteger)
    WtrafficRLr = LpVariable('WtrafficRLr', 0, 10000, LpInteger)
    WtrafficRLl = LpVariable('WtrafficRLl', 0, 10000, LpInteger)




    inner_vars = {}
    sum_vars = {}
    for j,d in enumerate(DIRECTIONS):
        inner_vars[d] = []
        direction_lanes_sum = sum(lanes[j*7:(j+1)*7])
        if direction_lanes_sum > 1:
            for i in range(n_choose_2(direction_lanes_sum)):
                inner_vars[d].append(LpVariable(d + 'inner_' + str(i), 0, 10000, LpInteger))
        else:
            inner_vars[d].append(LpVariable(d + 'inner_' + str(0), 0, 10000, LpInteger))
        sum_vars[d] = {}
        for lane_type in LANE_TYPES:
            var_name = d + 'sum' + lane_type
            sum_vars[d][var_name] = LpVariable(var_name, 0, 10000, LpInteger)

    sum_for_inner_vars = {}
    for d in DIRECTIONS:
        sum_for_inner_vars[d] = []
        for lt in LANE_TYPES:
            for i in range(lanes_count_dict[d][lt]):
                var_name = d + 'sum' + lt
                sum_for_inner_vars[d].append(sum_vars[d][var_name])

    for d in DIRECTIONS:
        direction_sum_lanes = sum(lanes_count_dict[d].values())
        pairs = n_permutations_2(direction_sum_lanes)
        for p in zip(pairs,inner_vars[d]):
            inner_var = p[1]
            sum_0 = p[0][0]
            sum_1 = p[0][1]
            prob += inner_var >= sum_for_inner_vars[d][sum_0]
            prob += inner_var >= sum_for_inner_vars[d][sum_1]









    #מגבלה ראשונה- סכום הפונים פנייה מסוימת מכל נתיב שווה לנתון הראשוני לגבי אותה פנייה מהזרוע

    prob += NtrafficRr*NlanesR+NtrafficRTr*NtrafficRTrbin*NlanesRT+NtrafficRTLr*NtrafficRTLrbin*NlanesRTL+NtrafficRLr*NtrafficRLrbin*NlanesRL >= NcountR
    prob += NtrafficTt*NlanesT+NtrafficRTt*NtrafficRTtbin*NlanesRT+NtrafficRTLt*NtrafficRTLtbin*NlanesRTL+NtrafficTLt*NtrafficTLtbin*NlanesTL >= NcountT
    prob += NtrafficLl*NlanesL+NtrafficTLl*NtrafficTLlbin*NlanesTL+NtrafficRTLl*NtrafficRTLlbin*NlanesRTL+NtrafficRLl*NtrafficRLlbin*NlanesRL >= NcountL

    prob += StrafficRr * SlanesR + StrafficRTr * StrafficRTrbin * SlanesRT + StrafficRTLr * StrafficRTLrbin * SlanesRTL + StrafficRLr * StrafficRLrbin * SlanesRL >= ScountR
    prob += StrafficTt * SlanesT + StrafficRTt * StrafficRTtbin * SlanesRT + StrafficRTLt * StrafficRTLtbin * SlanesRTL + StrafficTLt * StrafficTLtbin * SlanesTL >= ScountT
    prob += StrafficLl * SlanesL + StrafficTLl * StrafficTLlbin * SlanesTL + StrafficRTLl * StrafficRTLlbin * SlanesRTL + StrafficRLl * StrafficRLlbin * SlanesRL >= ScountL

    prob += EtrafficRr * ElanesR + EtrafficRTr * EtrafficRTrbin * ElanesRT + EtrafficRTLr * EtrafficRTLrbin * ElanesRTL + EtrafficRLr * EtrafficRLrbin * ElanesRL >= EcountR
    prob += EtrafficTt * ElanesT + EtrafficRTt * EtrafficRTtbin * ElanesRT + EtrafficRTLt * EtrafficRTLtbin * ElanesRTL + EtrafficTLt * EtrafficTLtbin * ElanesTL >= EcountT
    prob += EtrafficLl * ElanesL + EtrafficTLl * EtrafficTLlbin * ElanesTL + EtrafficRTLl * EtrafficRTLlbin * ElanesRTL + EtrafficRLl * EtrafficRLlbin * ElanesRL >= EcountL

    prob += WtrafficRr * WlanesR + WtrafficRTr * WtrafficRTrbin * WlanesRT + WtrafficRTLr * WtrafficRTLrbin * WlanesRTL + WtrafficRLr * WtrafficRLrbin * WlanesRL >= WcountR
    prob += WtrafficTt * WlanesT + WtrafficRTt * WtrafficRTtbin * WlanesRT + WtrafficRTLt * WtrafficRTLtbin * WlanesRTL + WtrafficTLt * WtrafficTLtbin * WlanesTL >= WcountT
    prob += WtrafficLl * WlanesL + WtrafficTLl * WtrafficTLlbin * WlanesTL + WtrafficRTLl * WtrafficRTLlbin * WlanesRTL + WtrafficRLl * WtrafficRLlbin * WlanesRL >= WcountL


    #באמצעות המשתנה הבינארי להכרזה על נת"צ שבנתיב מורכב, נקבע משתנים חדשים להכרזה על תוספת נפל לאוטובוסים
    NtrafficRTbus = (1- min(NtrafficRTrbin,NtrafficRTtbin))*50
    NtrafficTLbus = (1- min(NtrafficTLlbin,NtrafficTLtbin))*50
    NtrafficRLbus = (1- min(NtrafficRLrbin,NtrafficRLlbin))*50
    NtrafficRTLbus = (1- min(NtrafficRTLrbin,NtrafficRTLtbin,NtrafficRTLlbin))*50

    StrafficRTbus = (1 - min(StrafficRTrbin, StrafficRTtbin)) * 50
    StrafficTLbus = (1 - min(StrafficTLlbin, StrafficTLtbin)) * 50
    StrafficRLbus = (1 - min(StrafficRLrbin, StrafficRLlbin)) * 50
    StrafficRTLbus = (1 - min(StrafficRTLrbin, StrafficRTLtbin, StrafficRTLlbin)) * 50

    EtrafficRTbus = (1 - min(EtrafficRTrbin, EtrafficRTtbin)) * 50
    EtrafficTLbus = (1 - min(EtrafficTLlbin, EtrafficTLtbin)) * 50
    EtrafficRLbus = (1 - min(EtrafficRLrbin, EtrafficRLlbin)) * 50
    EtrafficRTLbus = (1 - min(EtrafficRTLrbin, EtrafficRTLtbin, EtrafficRTLlbin)) * 50

    WtrafficRTbus = (1 - min(WtrafficRTrbin, WtrafficRTtbin)) * 50
    WtrafficTLbus = (1 - min(WtrafficTLlbin, WtrafficTLtbin)) * 50
    WtrafficRLbus = (1 - min(WtrafficRLrbin, WtrafficRLlbin)) * 50
    WtrafficRTLbus = (1 - min(WtrafficRTLrbin, WtrafficRTLtbin, WtrafficRTLlbin)) * 50


    #מגבלה שנייה- הנפח בנתיב, שווה לסכום הנפחים באותו נתיב עבור כלל סוגי הפניות

    prob += NtrafficRr ==  sum_vars['N']['NsumR']
    prob += NtrafficRTr + NtrafficRTt + NtrafficRTbus == sum_vars['N']['NsumRT']
    prob += NtrafficTt == sum_vars['N']['NsumT']
    prob += NtrafficTLt + NtrafficTLl + NtrafficTLbus== sum_vars['N']['NsumTL']
    prob += NtrafficLl == sum_vars['N']['NsumL']
    prob += NtrafficRTLr +NtrafficRTLt+NtrafficRTLl+ NtrafficRTLbus== sum_vars['N']['NsumRTL']
    prob += NtrafficRLr +NtrafficRLl+ NtrafficRLbus== sum_vars['N']['NsumRL']

    prob += StrafficRr == sum_vars['S']['SsumR']
    prob += StrafficRTr + StrafficRTt + StrafficRTbus == sum_vars['S']['SsumRT']
    prob += StrafficTt == sum_vars['S']['SsumT']
    prob += StrafficTLt + StrafficTLl + StrafficTLbus == sum_vars['S']['SsumTL']
    prob += StrafficLl == sum_vars['S']['SsumL']
    prob += StrafficRTLr + StrafficRTLt + StrafficRTLl + StrafficRTLbus == sum_vars['S']['SsumRTL']
    prob += StrafficRLr + StrafficRLl + StrafficRLbus == sum_vars['S']['SsumRL']

    prob += EtrafficRr == sum_vars['E']['EsumR']
    prob += EtrafficRTr + EtrafficRTt + EtrafficRTbus == sum_vars['E']['EsumRT']
    prob += EtrafficTt == sum_vars['E']['EsumT']
    prob += EtrafficTLt + EtrafficTLl + EtrafficTLbus == sum_vars['E']['EsumTL']
    prob += EtrafficLl == sum_vars['E']['EsumL']
    prob += EtrafficRTLr + EtrafficRTLt + EtrafficRTLl + EtrafficRTLbus == sum_vars['E']['EsumRTL']
    prob += EtrafficRLr + EtrafficRLl + EtrafficRLbus == sum_vars['E']['EsumRL']

    prob += WtrafficRr == sum_vars['W']['WsumR']
    prob += WtrafficRTr + WtrafficRTt + WtrafficRTbus == sum_vars['W']['WsumRT']
    prob += WtrafficTt == sum_vars['W']['WsumT']
    prob += WtrafficTLt + WtrafficTLl + WtrafficTLbus == sum_vars['W']['WsumTL']
    prob += WtrafficLl == sum_vars['W']['WsumL']
    prob += WtrafficRTLr + WtrafficRTLt + WtrafficRTLl + WtrafficRTLbus == sum_vars['W']['WsumRTL']
    prob += WtrafficRLr + WtrafficRLl + WtrafficRLbus == sum_vars['W']['WsumRL']


    #  הגדרת  פונקציית המטרה של הזרוע כסכום כל המשתנים המדומים יהיה נקודת האופטימום שמייצגת את היותם קרובים ככל הניתן

    prob += sum(var for d in DIRECTIONS for var in inner_vars[d])


    #  פתרון והדפסה
    prob.solve(PULP_CBC_CMD(msg=False))
    #prob.solve(PULP_CBC_CMD(msg=False))
    #prob.solve()
    print("Status:", LpStatus[prob.status])
    if LpStatus[prob.status] != "Optimal":
        error = "solution not optimal (b)"
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, error, 'Phaser error', 0)
        exit()

   # for v in prob.variables():
     #  if v.varValue > 1:

    #    print(v.name, "=", v.varValue)

    ret_vals = []
    for d in DIRECTIONS:
        for lt in LANE_TYPES:
            if lanes_count_dict[d][lt] > 0:
                ret_vals.append(int(sum_vars[d][d + 'sum' + lt].varValue))
            else:
                ret_vals.append(0)
    #print (ret_vals)
    return ret_vals





