# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:11:39 2017

@author: Lennart
"""
import Wolke
import CharakterBeschreibung
from PyQt5 import QtWidgets

class BeschrWrapper(object):
    def __init__(self):
        super().__init__()
        self.formBeschr = QtWidgets.QWidget()
        self.uiBeschr = CharakterBeschreibung.Ui_formBeschreibung()
        self.uiBeschr.setupUi(self.formBeschr)
        
    def updateBeschreibung(self):
        if self.uiBeschr.editName.text() != "":
            Wolke.Char.name = self.uiBeschr.editName.text()
        if self.uiBeschr.editRasse.text() != "":
            Wolke.Char.rasse = self.uiBeschr.editRasse.text()
        Wolke.Char.status = self.uiBeschr.comboStatus.currentIndex()
        Wolke.Char.finanzen = self.uiBeschr.comboFinanzen.currentIndex()
        Wolke.Char.kurzbeschreibung = self.uiBeschr.editKurzbeschreibung.text()
        Wolke.Char.eigenheiten = []
        Wolke.Char.eigenheiten.append(self.uiBeschr.editEig1.text())
        Wolke.Char.eigenheiten.append(self.uiBeschr.editEig2.text())
        Wolke.Char.eigenheiten.append(self.uiBeschr.editEig3.text())
        Wolke.Char.eigenheiten.append(self.uiBeschr.editEig4.text())
        Wolke.Char.eigenheiten.append(self.uiBeschr.editEig5.text())
        Wolke.Char.eigenheiten.append(self.uiBeschr.editEig6.text())
        Wolke.Char.eigenheiten.append(self.uiBeschr.editEig7.text())
        Wolke.Char.eigenheiten.append(self.uiBeschr.editEig8.text())

    def loadBeschreibung(self):
        self.uiBeschr.editName.setText(Wolke.Char.name)
        self.uiBeschr.editRasse.setText(Wolke.Char.rasse)
        self.uiBeschr.comboStatus.setCurrentIndex(Wolke.Char.status)
        self.uiBeschr.comboFinanzen.setCurrentIndex(Wolke.Char.finanzen)
        self.uiBeschr.editKurzbeschreibung.setText(Wolke.Char.kurzbeschreibung)
        arr = ["", "", "", "", "", "", "", ""]
        count = 0
        for el in Wolke.Char.eigenheiten:
            arr[count] = el
            count += 1
        self.uiBeschr.editEig1.setText(arr[0])
        self.uiBeschr.editEig2.setText(arr[1])
        self.uiBeschr.editEig3.setText(arr[2])
        self.uiBeschr.editEig4.setText(arr[3])
        self.uiBeschr.editEig5.setText(arr[4])
        self.uiBeschr.editEig6.setText(arr[5])
        self.uiBeschr.editEig7.setText(arr[6])
        self.uiBeschr.editEig8.setText(arr[7])