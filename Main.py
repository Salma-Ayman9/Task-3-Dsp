from PyQt5 import QtWidgets, QtCore, uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QMessageBox)
import pyqtgraph as pg
import numpy as np
import mixer as mixx
import cv2 as cv
import logging
import sys
from imageModel import ImageModel
from modesEnum import Modes
logging.basicConfig(filename="logTest.Log",level=logging.INFO)
log_file = logging.getLogger()

class ApplicationWindow(mixx.Ui_MainWindow):

    def __init__(self, mainApp):
        super(ApplicationWindow, self).setupUi(mainApp)
        self.upload.triggered.connect(self.load)
        self.value1 = 0
        self.value2 = 0
        self.widgCount = 0
        self.widimg = [self.widImg1,self.widImg2]
        self.Img = [[],[]]
        self.showcomp = [self.showcomp1,self.showcomp2]
        self.widcomp = [self.widcomp1,self.widcomp2]
        self.slider = [self.slider1,self.slider2]
        self.value = [self.value1,self.value2]
        self.widgoutt = [self.widgOut,self.widgOut2]
        self.showcomp1.activated[str].connect(lambda:self.check(self.showcomp1,self.widcomp1,0))
        self.showcomp2.activated[str].connect(lambda:self.check(self.showcomp2,self.widcomp2,1))
        self.slider1.valueChanged.connect(lambda:self.getValue(0))
        self.slider2.valueChanged.connect(lambda:self.getValue(1))
        self.choiceCombos = [self.choosecomp1,self.choosecomp2,self.chooseimg1,self.chooseimg2]

        self.choosecomp1.activated.connect(self.choices)
        self.chooseimg1.activated.connect(self.choices)
        self.chooseimg2.activated.connect(self.choices)
        self.choosecomp2.activated.connect(self.choices)


    def load(self,widget):
        try:
            self.text = QFileDialog.getOpenFileName(None, "Open File", "results")
            if self.text[0]:
                if self.widgCount == 0:
                    self.Img[self.widgCount] = ImageModel(self.text[0])
                    self.draw(self.Img[self.widgCount].imgByte.T,self.widimg[self.widgCount])
                    self.widgCount+=1
                elif self.widgCount == 1:
                    if self.Img[0].imgByte.shape == cv.cvtColor(cv.imread(self.text[0]), cv.COLOR_BGR2GRAY).shape:
                        self.Img[self.widgCount] = ImageModel(self.text[0])
                        self.draw(self.Img[self.widgCount].imgByte.T,self.widimg[self.widgCount])
                    else:
                        warning = QMessageBox()
                        warning.setWindowTitle("Size Error")
                        warning.setText("please choose image with same size")
                        warning.setStandardButtons(QMessageBox.Ok)
                        warning.setIcon(QMessageBox.Critical)
                        warning.exec_()

        except:
            pass


        log_file.info("Loading Image")


    def draw(self,Img,widget):
        widget.setImage(Img)
        widget.ui.roiPlot.hide()
        widget.ui.histogram.hide()
        widget.ui.roiBtn.hide()
        widget.ui.menuBtn.hide()
        widget.ui.roiPlot.hide()
        widget.getView().setAspectLocked(False)
        widget.view.setAspectLocked(False)        

    def check(self,comboBox,widget,i):
        try:

            component = str(comboBox.currentText())
            if component == "Magnitude":
                #self.Magnitude(widget)
                self.draw(20*np.log(np.fft.fftshift(self.Img[i].magnitude)+1),widget)
                log_file.info("Showing Magnitude")
            elif component == "Phase":
                #self.phase(widget)
                self.draw(20*np.log(np.fft.fftshift(self.Img[i].phase)+1),widget)
                log_file.info("Showing Phase")
            elif component == "Real":
                #self.real(widget)
                self.draw(20*np.log(np.fft.fftshift(self.Img[i].real)+1),widget)
                log_file.info("Showing Real")
            elif component == "Imaginary":
                #self.imaginary(widget)
                self.draw(20*np.log(np.fft.fftshift(self.Img[i].imaginary)+1),widget)
                log_file.info("Showing Imaginary")

        except:
            pass

    def getValue(self,i):
        self.value[i] = (self.slider[i].value())/100
        print ("value",self.value)
        self.choices()

    def choices(self):
        choice1 = str(self.choosecomp1.currentText())
        choice2 = str(self.choosecomp2.currentText())
        comp2Index = self.choosecomp2.currentIndex()
        index1 = self.chooseimg1.currentIndex()
        index2 = self.chooseimg2.currentIndex()
        widindex = self.chooseOut.currentIndex()
        try:
            if choice1 == "Magnitude":
                self.choosecomp2.clear()
                self.choosecomp2.addItem("Phase")
                self.choosecomp2.addItem("Uniform Phase")
                self.choosecomp2.setCurrentIndex(comp2Index)
                if choice2 == "Phase":
                    self.Output = self.Img[index1].mix(self.Img[index2],self.value[0],self.value[1],Modes.magnitudeAndPhase)
                    self.draw(self.Output.T,self.widgoutt[widindex])
                    log_file.info("Mix Magnitude and Phase")
                elif choice2 == "Uniform Phase":
                    self.Output = self.Img[index1].mix(self.Img[index2],self.value[0],self.value[1],Modes.magnitudeAndUniformP)
                    self.draw(self.Output.T,self.widgoutt[widindex])
                    log_file.info("Mix Magnitude and Uniform Phase")
           

            if choice1 == "Phase":
                self.choosecomp2.clear()
                self.choosecomp2.addItem("Magnitude")
                self.choosecomp2.addItem("Uniform Magnitude")
                self.choosecomp2.setCurrentIndex(comp2Index)
                if choice2 == "Magnitude":
                    self.Output = self.Img[index2].mix(self.Img[index1],self.value[1],self.value[0],Modes.magnitudeAndPhase)
                    self.draw(self.Output.T,self.widgoutt[widindex])
                    log_file.info("Mix Phase and Magnitude")
                elif choice2 == "Uniform Magnitude":
                    self.Output = self.Img[index2].mix(self.Img[index1],self.value[1],self.value[0],Modes.uniformMAndPhase)
                    self.draw(self.Output.T,self.widgoutt[widindex])
                    log_file.info("Mix Phase and Unfiorm Magnitude")

            if choice1 == "Uniform Magnitude":
                self.choosecomp2.clear()
                self.choosecomp2.addItem("Phase")
                self.choosecomp2.addItem("Uniform Phase")
                self.choosecomp2.setCurrentIndex(comp2Index)
                if choice2 == "Phase":
                    self.Output = self.Img[index1].mix(self.Img[index2],self.value[0],self.value[1],Modes.uniformMAndPhase)
                    self.draw(self.Output.T,self.widgoutt[widindex])
                    log_file.info("Mix Unfiorm Magnitude and Phase")
                elif choice2 == "Uniform Phase":
                    self.Output = self.Img[index1].mix(self.Img[index2],self.value[0],self.value[1],Modes.uniformAndUniform)
                    self.draw(self.Output.T,self.widgoutt[widindex])
                    log_file.info("Mix Unfiorm Magnitude and Uniform Phase")


            if choice1 == "Uniform Phase":
                self.choosecomp2.clear()
                self.choosecomp2.addItem("Magnitude")
                self.choosecomp2.addItem("Uniform Magnitude")
                self.choosecomp2.setCurrentIndex(comp2Index)
                if choice2 == "Magnitude":
                    self.Output = self.Img[index2].mix(self.Img[index1],self.value[1],self.value[0],Modes.magnitudeAndUniformP)
                    self.draw(self.Output.T,self.widgoutt[widindex])
                    log_file.info("Mix Unfiorm Phase and Magnitude")
                elif choice2 == "Uniform Magnitude":
                    self.Output = self.Img[index2].mix(self.Img[index1],self.value[1],self.value[0],Modes.uniformAndUniform)
                    self.draw(self.Output.T,self.widgoutt[widindex])
                    log_file.info("Mix Unfiorm Phase and Unfiorm Magnitude")


            if choice1 == "Real":
                self.choosecomp2.clear()
                self.choosecomp2.addItem ("Imaginary")
                self.choosecomp2.setCurrentIndex(comp2Index)
                self.Output = self.Img[index1].mix(self.Img[index2],self.value[0],self.value[1],Modes.realAndImaginary)
                self.draw(self.Output.T,self.widgoutt[widindex])
                log_file.info("Mix Real and Imaginary")

            if choice1 == "Imaginary":
                self.choosecomp2.clear()
                self.choosecomp2.addItem("Real")
                self.choosecomp2.setCurrentIndex(comp2Index)
                self.Output= self.Img[index2].mix(self.Img[index1],self.value[1],self.value[0],Modes.realAndImaginary)
                self.draw(self.Output.T,self.widgoutt[widindex])
                log_file.info("Mix Imaginary and Real")

        except:
            pass


        # if cimg1 == "Image 1":
        #     if choice1 == "Magnitude":
        #         self.Img1.mix (self.Img2,self.value1,self.value2,magnitudeAndPhase)

        #     if choice1 == "Real":
        #         self.Img1.mix(self.Img2,self.value1,self.value2,realAndImaginary)

        #     if choice1 == "Phase":
        #         self.Img2.mix(self.Img1,self.value2,self.value1,magnitudeAndPhase)

        #     if choice1 == "Imaginary":
        #         self.Img2.mix(self.Img1,self.value2,self.value1,realAndImaginary)

        # if cimg1 == "Image 2":
        #     if choice1 == "Magnitude":
        #         self.Img2.mix (self.Img1,self.value1,self.value2,magnitudeAndPhase)

        #     if choice1 == "Real":
        #         self.Img2.mix(self.Img1,self.value1,self.value2,realAndImaginary)

        #     if choice1 == "Phase":
        #         self.Img1.mix(self.Img2,self.value2,self.value1,magnitudeAndPhase)
                
        #     if choice1 == "Imaginary":
        #         self.Img1.mix(self.Img2,self.value2,self.value1,realAndImaginary)











            


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = QtWidgets.QMainWindow()
    Window = ApplicationWindow(application)
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

