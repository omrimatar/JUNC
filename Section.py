from Phases import *
from constants import LOS_C_THRESHOLD, LOS_D_THRESHOLD


class Section:
    """
      A class used to represent all the data for a specific timing, including images
    """

    def __init__(self):
        self.__Image_A = Phases()
        self.__Image_B = Phases()
        self.__Image_C = Phases()
        self.__Image_D = Phases()
        self.__Image_E = Phases()
        self.__Image_F = Phases()
        self.__LRT_volume = 0
        self.__Total_count = 0
        self.__Volume_To_Capacity = 0
        self.__Level_Of_Service = ""

    @property
    def A(self):
        """Get the A image info"""
        return self.__Image_A

    @A.setter
    def A(self, value):
        """Set the A image info"""
        self.__Image_A = value

    @property
    def B(self):
        """Get the B image info"""
        return self.__Image_B

    @B.setter
    def B(self, value):
        """Set the B image info"""
        self.__Image_B = value

    @property
    def C(self):
        """Get the C image info"""
        return self.__Image_C

    @C.setter
    def C(self, value):
        """Set the C image info"""
        self.__Image_C = value

    @property
    def D(self):
        """Get the D image info"""
        return self.__Image_D

    @D.setter
    def D(self, value):
        """Set the D image info"""
        self.__Image_D = value

    @property
    def E(self):
        """Get the E image info"""
        return self.__Image_E

    @E.setter
    def E(self, value):
        """Set the E image info"""
        self.__Image_E = value

    @property
    def F(self):
        """Get the F image info"""
        return self.__Image_F

    @F.setter
    def F(self, value):
        """Set the F image info"""
        self.__Image_F = value

    @property
    def LRT(self):
        """Get the LRT table info"""
        return self.__LRT_volume

    @LRT.setter
    def LRT(self, value):
        """Set the LRT table info"""
        self.__LRT_volume = value

    @property
    def TOT(self):
        """Get the total count of all volumes in the section of the table"""
        return self.__Total_count

    @TOT.setter
    def TOT(self, value):
        """Set the total count of all volumes"""
        self.__Total_count = value

    @property
    def VOC(self):
        """Get the volume to capacity in the section of the table"""
        return self.__Volume_To_Capacity

    @VOC.setter
    def VOC(self, value):
        """Set the volume to capacity"""
        self.__Volume_To_Capacity = round(value, 2)

    @property
    def LOS(self):
        """Get the level of service in the section of the table"""
        return self.__Level_Of_Service

    @LOS.setter
    def LOS(self, value):
        """Set the level of service"""
        self.__Level_Of_Service = value

    def split_img(self, dir_output):
        """The method receives string in the format IMG_DIRECTION_ARROWS (for example, BStr -> image:B,
        direction:South, Arrows: through right) and divides it to each image. """
        images = {"A": self.A, "B": self.B, "C": self.C, "D": self.D, "E": self.E, "F": self.F}
        for img in dir_output:
            if img[0] in images.keys():
                images[img[0]].split_direction(img[1:])

    def set_los(self):
        """The method converts the VOC to a level of service character."""
        if self.VOC < LOS_C_THRESHOLD:
            self.LOS = "C"
        elif self.VOC < LOS_D_THRESHOLD:
            self.LOS = "D"
        elif self.VOC < 1:
            self.LOS = "E"
        else:
            self.LOS = "F"
