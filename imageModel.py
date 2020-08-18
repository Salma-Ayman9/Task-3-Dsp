## This is the abstract class that the students should implement  

from modesEnum import Modes
import numpy as np
import cv2 as cv

class ImageModel():

    """
    A class that represents the ImageModel"
    """

    def __init__(self):
        pass

    def __init__(self, imgPath):
        self.imgPath =imgPath
        ###
        # ALL the following properties should be assigned correctly after reading imgPath 
        ###
        self.imgByte =cv.cvtColor(cv.imread(self.imgPath), cv.COLOR_BGR2GRAY)
        self.dft = np.fft.fft2(self.imgByte)
        self.real =np.real(self.dft)
        self.imaginary =np.imag(self.dft)
        self.magnitude =np.abs(self.dft)
        self.phase = np.angle(self.dft,deg = False)
   
    def mix(self, imageToBeMixed: 'ImageModel', magnitudeOrRealRatio: float, phaesOrImaginaryRatio: float, mode: 'Modes') -> np.ndarray:
        if mode == Modes.magnitudeAndPhase:
            Output_Magnitude = self.magnitude*magnitudeOrRealRatio + imageToBeMixed.magnitude *(1- magnitudeOrRealRatio)
            Output_phase = imageToBeMixed.phase * phaesOrImaginaryRatio + self.phase * (1- phaesOrImaginaryRatio)
            Output_fourrier = Output_Magnitude*np.exp(Output_phase*1j)
            Output = np.abs(np.fft.ifft2(Output_fourrier))

        elif mode == Modes.realAndImaginary:
            Output_real = self.real * magnitudeOrRealRatio + imageToBeMixed.real *(1- magnitudeOrRealRatio)
            Output_imaginary = imageToBeMixed.imaginary * phaesOrImaginaryRatio + self.imaginary * (1- phaesOrImaginaryRatio)
            Output_fourrier = Output_real+(Output_imaginary*1j)
            Output = np.abs(np.fft.ifft2(Output_fourrier))

        elif mode == Modes.magnitudeAndUniformP:
            Output_Magnitude = self.magnitude*magnitudeOrRealRatio + imageToBeMixed.magnitude *(1- magnitudeOrRealRatio)
            Output_phase = np.zeros(self.imgByte.shape)
            Output_fourrier = Output_Magnitude*np.exp(Output_phase*1j)
            Output = np.abs(np.fft.ifft2(Output_fourrier))

        elif mode == Modes.uniformMAndPhase:
            Output_Magnitude = np.ones(self.imgByte.shape)
            Output_phase = imageToBeMixed.phase * phaesOrImaginaryRatio + self.phase * (1- phaesOrImaginaryRatio)
            Output_fourrier = Output_Magnitude*np.exp(Output_phase*1j)
            Output = np.abs(np.fft.ifft2(Output_fourrier))

        elif mode == Modes.uniformAndUniform :
            Output_Magnitude = np.ones(self.imgByte.shape)
            Output_phase = np.zeros(self.imgByte.shape)
            Output_fourrier = Output_Magnitude*np.exp(Output_phase*1j)
            Output = np.abs(np.fft.ifft2(Output_fourrier))


        return Output


