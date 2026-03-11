from constants import DEFAULT_CAPACITY


class General_Info:
    """
      A class used to represent the  general info of the junc
    """

    def __init__(self):
        self.__Capacity = DEFAULT_CAPACITY
        self.__NLSL_Allowed = False
        self.__ELWL_Allowed = False
        self.__5th_Image = False
        self.__6th_Image = False
        self.__Geometry_N_S = 3
        self.__Geometry_E_W = 3
        self.__Inflation = 1
        self.__Looping = False
        self.__OneWay = 0

    @property
    def CAP(self):
        """Get the capacity of the Junction"""
        return self.__Capacity

    @CAP.setter
    def CAP(self, cap_set):
        """Set the capacity of the Junction"""
        self.__Capacity = cap_set

    @property
    def NLSL(self):
        """Get if north left and south left is allowed together"""
        return self.__NLSL_Allowed

    @NLSL.setter
    def NLSL(self, NLSL_set):
        """Set if north left and south left is allowed together"""
        self.__NLSL_Allowed = bool(NLSL_set)

    @property
    def ELWL(self):
        """Get if east left and west left is allowed together"""
        return self.__ELWL_Allowed

    @ELWL.setter
    def ELWL(self, ELWL_set):
        """Set if east left and west left is allowed together"""
        self.__ELWL_Allowed = bool(ELWL_set)

    @property
    def IMG5(self):
        """Get if 5th image is allowed for this junction"""
        return self.__5th_Image

    @IMG5.setter
    def IMG5(self, img5_set):
        """Set if 5th image is allowed for this junction"""
        self.__5th_Image = bool(img5_set)

    @property
    def IMG6(self):
        """Get if 6th image is allowed for this junction"""
        return self.__6th_Image

    @IMG6.setter
    def IMG6(self, img6_set):
        """Get if 6th image is allowed for this junction"""
        self.__6th_Image = bool(img6_set)

    @property
    def GEONS(self):
        """Get the Geometry for north south | future option"""
        return self.__Geometry_N_S

    @GEONS.setter
    def GEONS(self, geons_set):
        """Set the Geometry for north south | future option"""
        self.__Geometry_N_S = geons_set

    @property
    def GEOEW(self):
        """Get the Geometry for east west | future option"""
        return self.__Geometry_E_W

    @GEOEW.setter
    def GEOEW(self, geoew_set):
        """Set the Geometry for east west | future option"""
        self.__Geometry_E_W = geoew_set

    @property
    def INF(self):
        """Get the inflation of the Junction"""
        return self.__Inflation

    @INF.setter
    def INF(self, inf_set):
        """Set the inflation of the Junction"""
        self.__Inflation = inf_set

    @property
    def LOOP(self):
        """Get the looping option of the Junction"""
        return self.__Looping

    @LOOP.setter
    def LOOP(self, loop_set):
        """Set the looping option of the Junction"""
        self.__Looping = bool(loop_set)

    @property
    def ONEWAY(self):
        """Get the oneway direction option of the Junction"""
        return self.__OneWay

    @ONEWAY.setter
    def ONEWAY(self, oneway):
        """Set the oneway direction option of the Junction"""
        self.__OneWay = oneway
