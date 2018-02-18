# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:52:34 2017

@author: Aeolitus
"""
import Fertigkeiten
import DatenbankEditVorteil
from Hilfsmethoden import Hilfsmethoden
from PyQt5 import QtWidgets, QtCore

class DatenbankEditVorteilWrapper(object):
    def __init__(self, vorteil=None):
        super().__init__()
        if vorteil is None:
            vorteil = Fertigkeiten.Vorteil()
        vorteilDialog = QtWidgets.QDialog()
        ui = DatenbankEditVorteil.Ui_talentDialog()
        ui.setupUi(vorteilDialog)
        
        vorteilDialog.setWindowFlags(
                QtCore.Qt.Window |
                QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowTitleHint |
                QtCore.Qt.WindowCloseButtonHint)
        
        ui.nameEdit.setText(vorteil.name)
        ui.kostenEdit.setValue(vorteil.kosten)
        ui.comboNachkauf.setCurrentText(vorteil.nachkauf)
        ui.comboTyp.setCurrentIndex(vorteil.typ)
        ui.voraussetzungenEdit.setPlainText(Hilfsmethoden.VorArray2Str(vorteil.voraussetzungen, None))
        ui.textEdit.setPlainText(vorteil.text)
        ui.checkVariable.setChecked(vorteil.variable!=-1)
        vorteilDialog.show()
        ret = vorteilDialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            self.vorteil = Fertigkeiten.Vorteil()
            self.vorteil.name = ui.nameEdit.text()
            self.vorteil.kosten = ui.kostenEdit.value()
            self.vorteil.nachkauf = ui.comboNachkauf.currentText()
            self.vorteil.voraussetzungen = Hilfsmethoden.VorStr2Array(ui.voraussetzungenEdit.toPlainText(),None)
            self.vorteil.typ = ui.comboTyp.currentIndex()
            if ui.checkVariable.isChecked():
                self.vorteil.variable = 1
            else:
                self.vorteil.variable = -1
            self.vorteil.text = ui.textEdit.toPlainText()
        else:
            self.vorteil = None
            