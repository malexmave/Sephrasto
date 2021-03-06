# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 11:21:32 2017

@author: Aeolitus
"""
import Fertigkeiten
from Hilfsmethoden import Hilfsmethoden, VoraussetzungException
import DatenbankEditFertigkeit
from PyQt5 import QtWidgets, QtCore

class DatenbankEditFertigkeitWrapper(object):
    def __init__(self, datenbank, fertigkeit=None, ueber=False):
        super().__init__()
        self.datenbank = datenbank
        if fertigkeit is None:
            fertigkeit = Fertigkeiten.Fertigkeit()
        self.fertigkeitPicked = fertigkeit
        self.fertigkeitUeber = ueber
        self.nameValid = True
        self.voraussetzungenValid = True
        fertDialog = QtWidgets.QDialog()
        self.ui = DatenbankEditFertigkeit.Ui_talentDialog()
        self.ui.setupUi(fertDialog)
        
        if not fertigkeit.isUserAdded:
            self.ui.warning.setVisible(True)
        
        fertDialog.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        self.ui.nameEdit.setText(fertigkeit.name)
        self.ui.nameEdit.textChanged.connect(self.nameChanged)
        self.nameChanged()
        self.ui.steigerungsfaktorEdit.setValue(fertigkeit.steigerungsfaktor)
        self.ui.comboAttribut1.setCurrentText(fertigkeit.attribute[0])
        self.ui.comboAttribut2.setCurrentText(fertigkeit.attribute[1])
        self.ui.comboAttribut3.setCurrentText(fertigkeit.attribute[2])
        if ueber:
            self.ui.voraussetzungenEdit.setPlainText(Hilfsmethoden.VorArray2Str(fertigkeit.voraussetzungen, None))
            self.ui.radioUebernatuerlich.setChecked(True)
            self.ui.radioProfan.setCheckable(False)
            self.ui.checkKampffertigkeit.setCheckable(False)
        else:
            self.ui.voraussetzungenEdit.setPlainText(" - ")
            self.ui.voraussetzungenEdit.setReadOnly(True)
            self.ui.radioProfan.setChecked(True)
            self.ui.radioUebernatuerlich.setCheckable(False)
            if fertigkeit.kampffertigkeit == 1:
                self.ui.checkKampffertigkeit.setChecked(True)

        self.ui.voraussetzungenEdit.textChanged.connect(self.voraussetzungenTextChanged)

        self.ui.textEdit.setPlainText(fertigkeit.text)
        fertDialog.show()
        ret = fertDialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            self.fertigkeit = Fertigkeiten.Fertigkeit()
            self.fertigkeit.name = self.ui.nameEdit.text()
            self.fertigkeit.steigerungsfaktor = int(self.ui.steigerungsfaktorEdit.value())
            if self.ui.radioProfan.isChecked():
                if self.ui.checkKampffertigkeit.isChecked():
                    self.fertigkeit.kampffertigkeit = 1;
            else:
                self.fertigkeit.voraussetzungen = Hilfsmethoden.VorStr2Array(self.ui.voraussetzungenEdit.toPlainText(), datenbank)
            self.fertigkeit.attribute = [self.ui.comboAttribut1.currentText(), 
                             self.ui.comboAttribut2.currentText(),
                             self.ui.comboAttribut3.currentText()]
            self.fertigkeit.text = self.ui.textEdit.toPlainText()

            self.fertigkeit.isUserAdded = False
            if self.fertigkeit == self.fertigkeitPicked:
                self.fertigkeit = None
            else:
                self.fertigkeit.isUserAdded = True
        else:
            self.fertigkeit = None
     
    def nameChanged(self):
        name = self.ui.nameEdit.text()
        if name == "":
            self.ui.nameEdit.setToolTip("Name darf nicht leer sein.")
            self.ui.nameEdit.setStyleSheet("border: 1px solid red;")
            self.nameValid = False
        elif name != self.fertigkeitPicked.name and \
                ((self.fertigkeitUeber and name in self.datenbank.übernatürlicheFertigkeiten) or \
                 (not self.fertigkeitUeber and name in self.datenbank.fertigkeiten)):
            self.ui.nameEdit.setToolTip("Name existiert bereits.")
            self.ui.nameEdit.setStyleSheet("border: 1px solid red;")
            self.nameValid = False
        else:
            self.ui.nameEdit.setToolTip("")
            self.ui.nameEdit.setStyleSheet("")
            self.nameValid = True
        self.updateSaveButtonState()
            
    def voraussetzungenTextChanged(self):
        try:
            Hilfsmethoden.VorStr2Array(self.ui.voraussetzungenEdit.toPlainText(), self.datenbank)
            self.ui.voraussetzungenEdit.setStyleSheet("")
            self.ui.voraussetzungenEdit.setToolTip("")
            self.voraussetzungenValid = True
        except VoraussetzungException as e:
            self.ui.voraussetzungenEdit.setStyleSheet("border: 1px solid red;")
            self.ui.voraussetzungenEdit.setToolTip(str(e))
            self.voraussetzungenValid = False
        self.updateSaveButtonState()

    def updateSaveButtonState(self):
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(self.nameValid and self.voraussetzungenValid)