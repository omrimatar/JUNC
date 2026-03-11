from constants import DEFAULT_CYCLE_TIME


class LRT_Info:
    """
      A class used to represent the LRT info of the junction
    """

    def __init__(self):
        self.__LRT_Dir = 0  # 0= no LRT, 1 = North & South, 2 = East & West , 3 = North, South, East & West
        self.__cycle_time = DEFAULT_CYCLE_TIME
        self.__train_lost_time = 25
        self.__train_headway = 4
        self.__MCU = 1
        self.__lost_time = 0
        self.__Metro_Dir = 0  # 0= no metro, 1 = North & South, 2 = East & West
        self.__LRT_orig_dir = [0, 0]  # [North & South , East & West]

    @property
    def LRT_Dir(self):
        """Get the Direction of the lrt"""
        return self.__LRT_Dir

    @LRT_Dir.setter
    def LRT_Dir(self, state):
        """the Direction of the lrt"""
        self.__LRT_Dir = state

    @property
    def CYC_TIME(self):
        """Get the cycle time"""
        return self.__cycle_time

    @CYC_TIME.setter
    def CYC_TIME(self, cycle_time):
        """Set the cycle time"""
        self.__cycle_time = cycle_time

    @property
    def LRT_LOST_TIME(self):
        """Get the lrt lost time"""
        return self.__train_lost_time

    @LRT_LOST_TIME.setter
    def LRT_LOST_TIME(self, lrt_lost_time):
        """Set the lrt lost time"""
        self.__train_lost_time = lrt_lost_time

    @property
    def LRT_HDWAY(self):
        """Get the train headway time"""
        return self.__train_headway

    @LRT_HDWAY.setter
    def LRT_HDWAY(self, lrt_hdway):
        """Set the train headway time"""
        self.__train_headway = lrt_hdway

    @property
    def LRT_MCU(self):
        """Get the train MCU value"""
        return self.__MCU

    @LRT_MCU.setter
    def LRT_MCU(self, lrt_mcu):
        """Set the train MCU value"""
        self.__MCU = lrt_mcu

    @property
    def GEN_LOST_TIME(self):
        """Get the general lost time"""
        return self.__lost_time

    @GEN_LOST_TIME.setter
    def GEN_LOST_TIME(self, gen_lost_time):
        """Set the general lost time"""
        self.__lost_time = gen_lost_time

    @property
    def Metro_Dir(self):
        """Get the state of the Metro"""
        return self.__Metro_Dir

    @Metro_Dir.setter
    def Metro_Dir(self, state):
        """Set the state of the Metro"""
        self.__Metro_Dir = state

    @property
    def LRT_Orig(self):
        """Get the original state of the LRT, as set in the data received, before translated to LRT_Dir"""
        return self.__LRT_orig_dir

    @LRT_Orig.setter
    def LRT_Orig(self, direc):
        """Set the original state of the LRT, as set in the data received, before translated to LRT_Dir"""
        self.__LRT_orig_dir = direc

    def lrt_orig_to_dir(self):
        """
        The method translates the received LRT direction to a number that represents that LRT direction,
        stored in LRT_Dir.

        [North & South , East & West] ->  0/1/2/3
        0 = no LRT
        1 = North & South
        2 = East & West
        3 = North, South, East & West
        """
        # lrt_orig_ns / lrt_orig_ew encoding:
        #   0 = no LRT on this axis
        #   1 = both arms active (legacy: full N-S or E-W axis)
        #   2 = first arm only  (N for ns, E for ew)
        #   3 = second arm only (S for ns, W for ew)
        ns, ew = self.LRT_Orig
        n = ns in (1, 2)
        s = ns in (1, 3)
        e = ew in (1, 2)
        w = ew in (1, 3)
        arm_map = {
            (False, False, False, False):  0,  # no LRT
            (True,  True,  False, False):  1,  # N-S straight
            (False, False, True,  True ):  2,  # E-W straight
            (True,  True,  True,  True ):  3,  # all four arms
            (True,  False, True,  False):  4,  # N-E corner
            (False, True,  True,  False):  5,  # S-E corner
            (True,  False, False, True ):  6,  # N-W corner
            (False, True,  False, True ):  7,  # S-W corner
            (True,  False, True,  True ):  8,  # N + E-W
            (False, True,  True,  True ):  9,  # S + E-W
            (True,  True,  True,  False): 10,  # N-S + E
            (True,  True,  False, True ): 11,  # N-S + W
            (True,  False, False, False): 12,  # N only
            (False, True,  False, False): 13,  # S only
            (False, False, True,  False): 14,  # E only
            (False, False, False, True ): 15,  # W only
        }
        self.LRT_Dir = arm_map.get((n, s, e, w), 0)
