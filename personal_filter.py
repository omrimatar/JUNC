#adjusted variables- read if you like dont change
from constants import MAX_LANES_PER_DIRECTION


def personal_filter(m):
        Nr = m[0]
        Nrt = m[1]
        Nt = m[2]
        Ntl = m[3]
        Nl = m[4]
        Nrtl = m[5]
        Nrl = m[6]
        Sr = m[7]
        Srt = m[8]
        St = m[9]
        Stl = m[10]
        Sl = m[11]
        Srtl = m[12]
        Srl = m[13]
        Er = m[14]
        Ert = m[15]
        Et = m[16]
        Etl = m[17]
        El = m[18]
        Ertl = m[19]
        Erl = m[20]
        Wr = m[21]
        Wrt = m[22]
        Wt = m[23]
        Wtl = m[24]
        Wl = m[25]
        Wrtl = m[26]
        Wrl = m[27]

        Nin= Nr + Nrt + Nt + Ntl + Nl + Nrtl + Nrl
        Sin= Sr + Srt + St + Stl + Sl + Srtl + Srl
        Ein= Er + Ert + Et + Etl + El + Ertl + Erl
        Win= Wr + Wrt + Wt + Wtl + Wl + Wrtl + Wrl
        Nout= max(St+Srt+Srtl+Stl, Er+Ert+Ertl+Erl, Wl+Wtl+Wrtl+Wtl)
        Sout= max(Nt+Nrt+Nrtl+Ntl, Wr+Wrt+Wrtl+Wrl, El+Etl+Ertl+Etl)
        Eout= max(Wt+Wrt+Wrtl+Wtl, Sr+Srt+Srtl+Srl, Nl+Ntl+Nrtl+Ntl)
        Wout= max(Et+Ert+Ertl+Etl, Nr+Nrt+Nrtl+Nrl, Sl+Stl+Srtl+Stl)


#todo: type constraints here:
#(DIRECTION)IN represents movement coming from that direction into the intersecection
#(DIRECTION)OUT represents movement coming to  that direction and out of the intersecection

        if (1
        and Nr < MAX_LANES_PER_DIRECTION
        and Nin <= MAX_LANES_PER_DIRECTION
        and Sin <= MAX_LANES_PER_DIRECTION
        and Ein <= MAX_LANES_PER_DIRECTION
        and Win <= MAX_LANES_PER_DIRECTION

        and Nout <= MAX_LANES_PER_DIRECTION
        and Sout <= MAX_LANES_PER_DIRECTION
        and Eout <= MAX_LANES_PER_DIRECTION
        and Wout <= MAX_LANES_PER_DIRECTION

        and St<= MAX_LANES_PER_DIRECTION
        and Wl<= MAX_LANES_PER_DIRECTION
        and Et<= MAX_LANES_PER_DIRECTION
        and Nr<= MAX_LANES_PER_DIRECTION
        and Nl+Nrl+Nrtl<= MAX_LANES_PER_DIRECTION
        and Nr+Nrl+Nrtl<= MAX_LANES_PER_DIRECTION
        and 1):
            return True


