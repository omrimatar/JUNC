from pulp import *
from functools import reduce
from itertools import permutations

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

    # ---- Free right-turn lane capacity check (>=9 lanes = free right) ----
    if NlanesR >= 9:
        if NcountR < 900:
            NcountR = 0
        else:
            print("WARNING: North right-turn free lane volume exceeds 900 veh/hr (cell C8). "
                  "Volume will not be zeroed out — verify this is intentional.")
    if SlanesR >= 9:
        if ScountR < 900:
            ScountR = 0
        else:
            print("WARNING: South right-turn free lane volume exceeds 900 veh/hr (cell K8). "
                  "Volume will not be zeroed out — verify this is intentional.")
    if ElanesR >= 9:
        if EcountR < 900:
            EcountR = 0
        else:
            print("WARNING: East right-turn free lane volume exceeds 900 veh/hr (cell S8). "
                  "Volume will not be zeroed out — verify this is intentional.")
    if WlanesR >= 9:
        if WcountR < 900:
            WcountR = 0
        else:
            print("WARNING: West right-turn free lane volume exceeds 900 veh/hr (cell AA8). "
                  "Volume will not be zeroed out — verify this is intentional.")

    # ---- Negative volume / lane check ----
    _vol_cells = ['D4', 'E4', 'F4', 'H4', 'I4', 'J4', 'L4', 'M4', 'N4', 'P4', 'Q4', 'R4']
    _vol_names = ['North right', 'North through', 'North left',
                  'South right', 'South through', 'South left',
                  'East right',  'East through',  'East left',
                  'West right',  'West through',  'West left']
    for _i, (_v, _cell, _name) in enumerate(zip(volume, _vol_cells, _vol_names)):
        if _v < 0:
            raise ValueError(
                f"Negative volume in {_name} (cell {_cell} / {_cell[0]}{int(_cell[1:])+1}): "
                f"value = {_v}. Traffic volumes must be 0 or greater. "
                f"Check rows 4-5 (morning/evening volumes) and the inflation factor in cell V46."
            )

    _lane_cells  = ['C8','D8','E8','F8','G8','H8','I8',
                    'K8','L8','M8','N8','O8','P8','Q8',
                    'S8','T8','U8','V8','W8','X8','Y8',
                    'AA8','AB8','AC8','AD8','AE8','AF8','AG8']
    _lane_types  = ['R','RT','T','TL','L','RTL','RL'] * 4
    _lane_dirs   = ['North']*7 + ['South']*7 + ['East']*7 + ['West']*7
    for _i, (_ln, _cell, _lt, _ld) in enumerate(zip(lanes, _lane_cells, _lane_types, _lane_dirs)):
        if _ln < 0:
            raise ValueError(
                f"Negative lane count for {_ld} {_lt} lane (cell {_cell}): "
                f"value = {_ln}. Lane counts must be 0 or greater. "
                f"Check row 8 (lane counts)."
            )

    # ---- Lane count / nataz must be integers ----
    for i in range(28):
        try:
            x = lanes[i] % 1
            y = nataz[i] % 1
        except Exception:
            raise ValueError(
                f"Non-numeric value in lane count or nataz code at index {i} "
                f"(cell {_lane_cells[i]} or row-9 equivalent). "
                f"All values in row 8 (lane counts) and row 9 (nataz codes) must be integers."
            )
        if x != 0 or y != 0:
            raise ValueError(
                f"Non-integer value at {_lane_dirs[i]} {_lane_types[i]} "
                f"(lane cell {_lane_cells[i]}, nataz cell {_lane_cells[i].replace('8','9')}). "
                f"Lane counts and nataz codes must be whole numbers (no decimals)."
            )

    # ---- Nataz code range validation ----
    # North RT (cell D9): valid 0-3
    if nataz[1] > 3:
        raise ValueError(
            f"Invalid nataz code in cell D9 (North RT lane): value = {nataz[1]}. "
            f"Valid codes: 0=none, 1=full transit, 2=transit straight only, 3=transit right only. "
            f"Maximum allowed value is 3."
        )
    # North TL (cell F9): valid 0,1,3,4 — code 2 is forbidden
    if nataz[3] == 2 or nataz[3] > 4:
        raise ValueError(
            f"Invalid nataz code in cell F9 (North TL lane): value = {nataz[3]}. "
            f"Valid codes: 0=none, 1=full transit, 3=transit left only, 4=transit straight only. "
            f"Code 2 is not valid for TL lanes; maximum allowed value is 4."
        )
    # North RL (cell I9): valid 0,1,2,4 — code 3 is forbidden
    if nataz[6] == 3 or nataz[6] > 4:
        raise ValueError(
            f"Invalid nataz code in cell I9 (North RL lane): value = {nataz[6]}. "
            f"Valid codes: 0=none, 1=full transit, 2=transit left only, 4=transit right only. "
            f"Code 3 is not valid for RL lanes; maximum allowed value is 4."
        )
    # North RTL (cell H9): valid 0-7
    if nataz[5] > 7:
        raise ValueError(
            f"Invalid nataz code in cell H9 (North RTL lane): value = {nataz[5]}. "
            f"Valid codes: 0-7 (0=none, 1=full transit, 2=block right, 3=block straight, "
            f"4=block left, 5=block right+straight, 6=block right+left, 7=block straight+left)."
        )
    # South RT (cell L9): valid 0-3
    if nataz[8] > 3:
        raise ValueError(
            f"Invalid nataz code in cell L9 (South RT lane): value = {nataz[8]}. "
            f"Valid codes: 0=none, 1=full transit, 2=transit straight only, 3=transit right only. "
            f"Maximum allowed value is 3."
        )
    # South TL (cell N9): valid 0,1,3,4 — code 2 forbidden
    if nataz[10] == 2 or nataz[3] > 4:
        raise ValueError(
            f"Invalid nataz code in cell N9 (South TL lane): value = {nataz[10]}. "
            f"Valid codes: 0=none, 1=full transit, 3=transit left only, 4=transit straight only. "
            f"Code 2 is not valid for TL lanes; maximum allowed value is 4."
        )
    # South RL (cell Q9): valid 0,1,2,4 — code 3 forbidden
    if nataz[13] == 3 or nataz[6] > 4:
        raise ValueError(
            f"Invalid nataz code in cell Q9 (South RL lane): value = {nataz[13]}. "
            f"Valid codes: 0=none, 1=full transit, 2=transit left only, 4=transit right only. "
            f"Code 3 is not valid for RL lanes; maximum allowed value is 4."
        )
    # South RTL (cell P9): valid 0-7
    if nataz[12] > 7:
        raise ValueError(
            f"Invalid nataz code in cell P9 (South RTL lane): value = {nataz[12]}. "
            f"Valid codes: 0-7 (0=none, 1=full transit, 2=block right, 3=block straight, "
            f"4=block left, 5=block right+straight, 6=block right+left, 7=block straight+left)."
        )
    # East RT (cell T9): valid 0-3
    if nataz[15] > 3:
        raise ValueError(
            f"Invalid nataz code in cell T9 (East RT lane): value = {nataz[15]}. "
            f"Valid codes: 0=none, 1=full transit, 2=transit straight only, 3=transit right only. "
            f"Maximum allowed value is 3."
        )
    # East TL (cell V9): valid 0,1,3,4 — code 2 forbidden
    if nataz[17] == 2 or nataz[3] > 4:
        raise ValueError(
            f"Invalid nataz code in cell V9 (East TL lane): value = {nataz[17]}. "
            f"Valid codes: 0=none, 1=full transit, 3=transit left only, 4=transit straight only. "
            f"Code 2 is not valid for TL lanes; maximum allowed value is 4."
        )
    # East RL (cell Y9): valid 0,1,2,4 — code 3 forbidden
    if nataz[20] == 3 or nataz[6] > 4:
        raise ValueError(
            f"Invalid nataz code in cell Y9 (East RL lane): value = {nataz[20]}. "
            f"Valid codes: 0=none, 1=full transit, 2=transit left only, 4=transit right only. "
            f"Code 3 is not valid for RL lanes; maximum allowed value is 4."
        )
    # East RTL (cell X9): valid 0-7
    if nataz[19] > 7:
        raise ValueError(
            f"Invalid nataz code in cell X9 (East RTL lane): value = {nataz[19]}. "
            f"Valid codes: 0-7 (0=none, 1=full transit, 2=block right, 3=block straight, "
            f"4=block left, 5=block right+straight, 6=block right+left, 7=block straight+left)."
        )
    # West RT (cell AB9): valid 0-3
    if nataz[22] > 3:
        raise ValueError(
            f"Invalid nataz code in cell AB9 (West RT lane): value = {nataz[22]}. "
            f"Valid codes: 0=none, 1=full transit, 2=transit straight only, 3=transit right only. "
            f"Maximum allowed value is 3."
        )
    # West TL (cell AD9): valid 0,1,3,4 — code 2 forbidden
    if nataz[24] == 2 or nataz[3] > 4:
        raise ValueError(
            f"Invalid nataz code in cell AD9 (West TL lane): value = {nataz[24]}. "
            f"Valid codes: 0=none, 1=full transit, 3=transit left only, 4=transit straight only. "
            f"Code 2 is not valid for TL lanes; maximum allowed value is 4."
        )
    # West RL (cell AG9): valid 0,1,2,4 — code 3 forbidden
    if nataz[27] == 3 or nataz[6] > 4:
        raise ValueError(
            f"Invalid nataz code in cell AG9 (West RL lane): value = {nataz[27]}. "
            f"Valid codes: 0=none, 1=full transit, 2=transit left only, 4=transit right only. "
            f"Code 3 is not valid for RL lanes; maximum allowed value is 4."
        )
    # West RTL (cell AF9): valid 0-7
    if nataz[26] > 7:
        raise ValueError(
            f"Invalid nataz code in cell AF9 (West RTL lane): value = {nataz[26]}. "
            f"Valid codes: 0-7 (0=none, 1=full transit, 2=block right, 3=block straight, "
            f"4=block left, 5=block right+straight, 6=block right+left, 7=block straight+left)."
        )

    # ---- Max 1 complex lane per type per direction ----
    if NlanesRT > 1 or NlanesRTL > 1 or NlanesRL > 1 or NlanesTL > 1:
        _issues = []
        if NlanesRT  > 1: _issues.append(f"RT={NlanesRT} (cell D8)")
        if NlanesTL  > 1: _issues.append(f"TL={NlanesTL} (cell F8)")
        if NlanesRTL > 1: _issues.append(f"RTL={NlanesRTL} (cell H8)")
        if NlanesRL  > 1: _issues.append(f"RL={NlanesRL} (cell I8)")
        raise ValueError(
            f"North routing error: only 1 complex lane of each type is allowed per direction. "
            f"Offending cells — {', '.join(_issues)}. "
            f"Reduce each value to 0 or 1 in row 8."
        )
    if SlanesRT > 1 or SlanesRTL > 1 or SlanesRL > 1 or SlanesTL > 1:
        _issues = []
        if SlanesRT  > 1: _issues.append(f"RT={SlanesRT} (cell L8)")
        if SlanesTL  > 1: _issues.append(f"TL={SlanesTL} (cell N8)")
        if SlanesRTL > 1: _issues.append(f"RTL={SlanesRTL} (cell P8)")
        if SlanesRL  > 1: _issues.append(f"RL={SlanesRL} (cell Q8)")
        raise ValueError(
            f"South routing error: only 1 complex lane of each type is allowed per direction. "
            f"Offending cells — {', '.join(_issues)}. "
            f"Reduce each value to 0 or 1 in row 8."
        )
    if ElanesRT > 1 or ElanesRTL > 1 or ElanesRL > 1 or ElanesTL > 1:
        _issues = []
        if ElanesRT  > 1: _issues.append(f"RT={ElanesRT} (cell T8)")
        if ElanesTL  > 1: _issues.append(f"TL={ElanesTL} (cell V8)")
        if ElanesRTL > 1: _issues.append(f"RTL={ElanesRTL} (cell X8)")
        if ElanesRL  > 1: _issues.append(f"RL={ElanesRL} (cell Y8)")
        raise ValueError(
            f"East routing error: only 1 complex lane of each type is allowed per direction. "
            f"Offending cells — {', '.join(_issues)}. "
            f"Reduce each value to 0 or 1 in row 8."
        )
    if WlanesRT > 1 or WlanesRTL > 1 or WlanesRL > 1 or WlanesTL > 1:
        _issues = []
        if WlanesRT  > 1: _issues.append(f"RT={WlanesRT} (cell AB8)")
        if WlanesTL  > 1: _issues.append(f"TL={WlanesTL} (cell AD8)")
        if WlanesRTL > 1: _issues.append(f"RTL={WlanesRTL} (cell AF8)")
        if WlanesRL  > 1: _issues.append(f"RL={WlanesRL} (cell AG8)")
        raise ValueError(
            f"West routing error: only 1 complex lane of each type is allowed per direction. "
            f"Offending cells — {', '.join(_issues)}. "
            f"Reduce each value to 0 or 1 in row 8."
        )

    # ---- Volume exists but no lane can serve that movement ----
    if NlanesR+NlanesRT+NlanesRTL+NlanesRL+NtrafficRTrbin+NtrafficRTLrbin+NtrafficRLrbin-3 == 0 and NcountR > 0:
        raise ValueError(
            f"North right-turn volume = {int(NcountR)} veh/hr (cells D4/D5) but no lane can serve it. "
            f"Add at least one of: R (cell C8), RT (cell D8), RTL (cell H8), RL (cell I8). "
            f"If a shared lane is present, check that its nataz code (row 9) does not block right turns."
        )
    if NlanesT+NlanesRT+NlanesRTL+NlanesTL+NtrafficRTtbin+NtrafficRTLtbin+NtrafficTLtbin-3 == 0 and NcountT > 0:
        raise ValueError(
            f"North through volume = {int(NcountT)} veh/hr (cells E4/E5) but no lane can serve it. "
            f"Add at least one of: T (cell E8), RT (cell D8), RTL (cell H8), TL (cell F8). "
            f"If a shared lane is present, check that its nataz code (row 9) does not block straight movement."
        )
    if NlanesL+NlanesTL+NlanesRTL+NlanesRL+NtrafficTLlbin+NtrafficRTLlbin+NtrafficRLlbin-3 == 0 and NcountL > 0:
        raise ValueError(
            f"North left-turn volume = {int(NcountL)} veh/hr (cells F4/F5) but no lane can serve it. "
            f"Add at least one of: L (cell G8), TL (cell F8), RTL (cell H8), RL (cell I8). "
            f"If a shared lane is present, check that its nataz code (row 9) does not block left turns."
        )

    if SlanesR+SlanesRT+SlanesRTL+SlanesRL+StrafficRTrbin+StrafficRTLrbin+StrafficRLrbin-3 == 0 and ScountR > 0:
        raise ValueError(
            f"South right-turn volume = {int(ScountR)} veh/hr (cells H4/H5) but no lane can serve it. "
            f"Add at least one of: R (cell K8), RT (cell L8), RTL (cell P8), RL (cell Q8). "
            f"If a shared lane is present, check that its nataz code (row 9) does not block right turns."
        )
    if SlanesT+SlanesRT+SlanesRTL+SlanesTL+SlanesTL+StrafficRTtbin+StrafficRTLtbin+StrafficTLtbin-3 == 0 and ScountT > 0:
        raise ValueError(
            f"South through volume = {int(ScountT)} veh/hr (cells I4/I5) but no lane can serve it. "
            f"Add at least one of: T (cell M8), RT (cell L8), RTL (cell P8), TL (cell N8). "
            f"If a shared lane is present, check that its nataz code (row 9) does not block straight movement."
        )
    if SlanesL+SlanesTL+SlanesRTL+SlanesRL+StrafficTLlbin+StrafficRTLlbin+StrafficRLlbin-3 == 0 and ScountL > 0:
        raise ValueError(
            f"South left-turn volume = {int(ScountL)} veh/hr (cells J4/J5) but no lane can serve it. "
            f"Add at least one of: L (cell O8), TL (cell N8), RTL (cell P8), RL (cell Q8). "
            f"If a shared lane is present, check that its nataz code (row 9) does not block left turns."
        )

    if ElanesR+ElanesRT+ElanesRTL+ElanesRL+EtrafficRTrbin+EtrafficRTLrbin+EtrafficRLrbin-3 == 0 and EcountR > 0:
        raise ValueError(
            f"East right-turn volume = {int(EcountR)} veh/hr (cells L4/L5) but no lane can serve it. "
            f"Add at least one of: R (cell S8), RT (cell T8), RTL (cell X8), RL (cell Y8). "
            f"If a shared lane is present, check that its nataz code (row 9) does not block right turns."
        )
    if ElanesT+ElanesRT+ElanesRTL+ElanesTL+EtrafficRTtbin+EtrafficRTLtbin+EtrafficTLtbin-3 == 0 and EcountT > 0:
        raise ValueError(
            f"East through volume = {int(EcountT)} veh/hr (cells M4/M5) but no lane can serve it. "
            f"Add at least one of: T (cell U8), RT (cell T8), RTL (cell X8), TL (cell V8). "
            f"If a shared lane is present, check that its nataz code (row 9) does not block straight movement."
        )
    if ElanesL+ElanesTL+ElanesRTL+ElanesRL+EtrafficTLlbin+EtrafficRTLlbin+EtrafficRLlbin-3 == 0 and EcountL > 0:
        raise ValueError(
            f"East left-turn volume = {int(EcountL)} veh/hr (cells N4/N5) but no lane can serve it. "
            f"Add at least one of: L (cell W8), TL (cell V8), RTL (cell X8), RL (cell Y8). "
            f"If a shared lane is present, check that its nataz code (row 9) does not block left turns."
        )

    if WlanesR+WlanesRT+WlanesRTL+WlanesRL+WtrafficRTrbin+WtrafficRTLrbin+WtrafficRLrbin-3 == 0 and WcountR > 0:
        raise ValueError(
            f"West right-turn volume = {int(WcountR)} veh/hr (cells P4/P5) but no lane can serve it. "
            f"Add at least one of: R (cell AA8), RT (cell AB8), RTL (cell AF8), RL (cell AG8). "
            f"If a shared lane is present, check that its nataz code (row 9) does not block right turns."
        )
    if WlanesT+WlanesRT+WlanesRTL+WlanesTL+WtrafficRTtbin+WtrafficRTLtbin+WtrafficTLtbin-3 == 0 and WcountT > 0:
        raise ValueError(
            f"West through volume = {int(WcountT)} veh/hr (cells Q4/Q5) but no lane can serve it. "
            f"Add at least one of: T (cell AC8), RT (cell AB8), RTL (cell AF8), TL (cell AD8). "
            f"If a shared lane is present, check that its nataz code (row 9) does not block straight movement."
        )
    if WlanesL+WlanesTL+WlanesRTL+WlanesRL+WtrafficTLlbin+WtrafficRTLlbin+WtrafficRLlbin-3 == 0 and WcountL > 0:
        raise ValueError(
            f"West left-turn volume = {int(WcountL)} veh/hr (cells R4/R5) but no lane can serve it. "
            f"Add at least one of: L (cell AE8), TL (cell AD8), RTL (cell AF8), RL (cell AG8). "
            f"If a shared lane is present, check that its nataz code (row 9) does not block left turns."
        )

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
        raise ValueError(
            f"Traffic assignment solver failed (status: {LpStatus[prob.status]}). "
            f"The lane configuration cannot carry all the specified volumes. "
            f"Possible causes: "
            f"(1) A shared lane has a nataz code (row 9) that blocks all movements with volume. "
            f"(2) An RL lane (right+left, no through) is combined with through volume — "
            f"RL lanes cannot carry straight-through traffic. "
            f"(3) Volumes are extremely high relative to the number of lanes. "
            f"Review the lane layout (row 8) and nataz codes (row 9)."
        )

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





