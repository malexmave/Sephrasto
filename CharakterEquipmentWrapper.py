# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:25:53 2017

@author: Lennart
"""
from Wolke import Wolke
import CharakterEquipment
from PyQt5 import QtWidgets, QtCore
import Objekte
import Definitionen
from WaffenPicker import WaffenPicker
import logging
from Hilfsmethoden import Hilfsmethoden

class EquipWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        logging.debug("Initializing EquipWrapper...")
        self.formEq = QtWidgets.QWidget()
        self.uiEq = CharakterEquipment.Ui_formAusruestung()
        self.uiEq.setupUi(self.formEq)
        self.initialLoad = True
        logging.debug("UI Setup...")
        #Signals
        # Connect all Spins and Edit boxes - hacky, sorry
        fields = [el for el in self.uiEq.__dir__() if el[0:4] == "spin"]
        for el in fields:
            eval("self.uiEq." + el + ".valueChanged.connect(self.updateEquipment)")
        fields = [el for el in self.uiEq.__dir__() if el[0:4] == "edit"]
        for el in fields:
            eval("self.uiEq." + el + ".editingFinished.connect(self.updateEquipment)")
        logging.debug("Signals Set...")
        for el in range(1,9):
            eval("self.uiEq.comboStil"+str(el)+".setCurrentIndex(0)")
            eval("self.uiEq.comboStil"+str(el)+".clear()")
            for el2 in Definitionen.Kampfstile:
                getName = lambda : el2
                eval("self.uiEq.comboStil"+str(el)+".addItem(getName())")
        logging.debug("Kampfstile added...")
        self.uiEq.addW1.clicked.connect(lambda state, idx=1: self.selectWeapon(idx))   
        self.uiEq.addW2.clicked.connect(lambda state, idx=2: self.selectWeapon(idx))   
        self.uiEq.addW3.clicked.connect(lambda state, idx=3: self.selectWeapon(idx))   
        self.uiEq.addW4.clicked.connect(lambda state, idx=4: self.selectWeapon(idx))   
        self.uiEq.addW5.clicked.connect(lambda state, idx=5: self.selectWeapon(idx))   
        self.uiEq.addW6.clicked.connect(lambda state, idx=6: self.selectWeapon(idx))   
        self.uiEq.addW7.clicked.connect(lambda state, idx=7: self.selectWeapon(idx))   
        self.uiEq.addW8.clicked.connect(lambda state, idx=8: self.selectWeapon(idx))   
        logging.debug("Check Toggle...")
        self.uiEq.checkZonen.stateChanged.connect(self.checkToggleEquip)
        self.defaultStyle = self.uiEq.spinW1h.styleSheet()
        self.currentlyLoading = False
        
        self.checkToggleEquip()
        
    def updateEquipment(self):
        if not self.currentlyLoading:
            changed = False
            ruestungNeu = []

            if self.uiEq.editR1name.text() != "":
                R = Objekte.Ruestung() 
                R.name = self.uiEq.editR1name.text()
                R.be = int(self.uiEq.spinR1be.value())
                if self.uiEq.checkZonen.isChecked():
                    R.rs = [self.uiEq.spinR1bein.value(), self.uiEq.spinR1larm.value(), self.uiEq.spinR1rarm.value(), self.uiEq.spinR1bauch.value(), self.uiEq.spinR1brust.value(), self.uiEq.spinR1kopf.value()]
                else:
                    R.rs = 6*[self.uiEq.spinR1RS.value()]
                ruestungNeu.append(R)
            if self.uiEq.editR2name.text() != "":
                R = Objekte.Ruestung() 
                R.name = self.uiEq.editR2name.text()
                R.be = self.uiEq.spinR2be.value()
                if self.uiEq.checkZonen.isChecked():
                    R.rs = [self.uiEq.spinR2bein.value(), self.uiEq.spinR2larm.value(), self.uiEq.spinR2rarm.value(), self.uiEq.spinR2bauch.value(), self.uiEq.spinR2brust.value(), self.uiEq.spinR2kopf.value()]
                else:
                    R.rs = 6*[self.uiEq.spinR2RS.value()]
                ruestungNeu.append(R)
            if self.uiEq.editR3name.text() != "":
                R = Objekte.Ruestung() 
                R.name = self.uiEq.editR3name.text()
                R.be = self.uiEq.spinR3be.value()
                if self.uiEq.checkZonen.isChecked():
                    R.rs = [self.uiEq.spinR3bein.value(), self.uiEq.spinR3larm.value(), self.uiEq.spinR3rarm.value(), self.uiEq.spinR3bauch.value(), self.uiEq.spinR3brust.value(), self.uiEq.spinR3kopf.value()]
                else:
                    R.rs = 6*[self.uiEq.spinR3RS.value()]
                ruestungNeu.append(R)

            if not Hilfsmethoden.ArrayEqual(ruestungNeu, Wolke.Char.rüstung):
                changed = True
                Wolke.Char.rüstung = ruestungNeu

            waffenNeu = []
            for el in ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8']:
                if (eval("self.uiEq.edit" + el + "name.text()") != ""):
                    if eval("self.uiEq.check" + el + "FK.isChecked()"):
                        W = Objekte.Fernkampfwaffe()
                        W.lz = eval("self.uiEq.spin" + el + "wm.value()")
                    else:
                        W = Objekte.Nahkampfwaffe()
                        W.wm = eval("self.uiEq.spin" + el + "wm.value()")
                    W.name = eval("self.uiEq.edit" + el + "name.text()")
                    W.rw = eval("self.uiEq.spin" + el + "rw.value()")
                    if W.name == "Unbewaffnet":
                        wsmod = Wolke.Char.rsmod + Wolke.Char.ws
                        if len(Wolke.Char.rüstung) > 0:    
                            wsmod += int(sum(Wolke.Char.rüstung[0].rs)/6+0.5+0.0001)
                        W.haerte = wsmod
                    else:
                        W.haerte = eval("self.uiEq.spin" + el + "h.value()")
                    W.W6 = eval("self.uiEq.spin" + el + "w6.value()")
                    W.plus = eval("self.uiEq.spin" + el + "plus.value()")
                    eigenschaftStr = eval("self.uiEq.edit" + el + "eig.text()")
                    if eigenschaftStr:
                        W.eigenschaften = list(map(str.strip, eigenschaftStr.split(","))) 
                    self.refreshKampfstile(int(el[-1])-1)
                    tmp = eval("self.uiEq.comboStil" + el[-1] + ".currentText()")
                    if tmp in Definitionen.Kampfstile:
                        W.kampfstil = Definitionen.Kampfstile.index(tmp)
                    waffenNeu.append(W)
            
            if not Hilfsmethoden.ArrayEqual(waffenNeu, Wolke.Char.waffen):
                Wolke.Char.waffen = waffenNeu
                changed = True

            if changed:
                Wolke.Char.aktualisieren()
                self.modified.emit()
            self.loadEquipment()
        
    def loadEquipment(self):
        self.currentlyLoading = True
        Rarr = ["R1", "R2", "R3"]
        count = 0
        # Add in Armor
        while count < len(Wolke.Char.rüstung):
            R = Wolke.Char.rüstung[count]
            if count < len(Rarr):
                getName = lambda : R.name
                eval("self.uiEq.edit" + Rarr[count] + "name.setText(getName())")
                eval("self.uiEq.spin" + Rarr[count] + "be.setValue(" + str(R.be) +")")
                eval("self.uiEq.spin" + Rarr[count] + "bein.setValue(" + str(R.rs[0]) +")")
                eval("self.uiEq.spin" + Rarr[count] + "larm.setValue(" + str(R.rs[1]) +")")
                eval("self.uiEq.spin" + Rarr[count] + "rarm.setValue(" + str(R.rs[2]) +")")
                eval("self.uiEq.spin" + Rarr[count] + "bauch.setValue(" + str(R.rs[3]) +")")
                eval("self.uiEq.spin" + Rarr[count] + "brust.setValue(" + str(R.rs[4]) +")")
                eval("self.uiEq.spin" + Rarr[count] + "kopf.setValue(" + str(R.rs[5]) +")")
                eval("self.uiEq.spin" + Rarr[count] + "RS.setValue(" + str(int(sum(R.rs)/6+0.5+0.0001)) +")")
                count += 1
        
        # Empty all other cells
        while count < 3:
            eval("self.uiEq.edit" + Rarr[count] + "name.setText(\"\")")
            eval("self.uiEq.spin" + Rarr[count] + "be.setValue(0)")
            eval("self.uiEq.spin" + Rarr[count] + "bein.setValue(0)")
            eval("self.uiEq.spin" + Rarr[count] + "larm.setValue(0)")
            eval("self.uiEq.spin" + Rarr[count] + "rarm.setValue(0)")
            eval("self.uiEq.spin" + Rarr[count] + "bauch.setValue(0)")
            eval("self.uiEq.spin" + Rarr[count] + "brust.setValue(0)")
            eval("self.uiEq.spin" + Rarr[count] + "kopf.setValue(0)")
            eval("self.uiEq.spin" + Rarr[count] + "RS.setValue(0)")
            count += 1
        
        count = 0
        # Load in Weapons
        while count < len(Wolke.Char.waffen):
            W = Wolke.Char.waffen[count]
            self.loadWeaponIntoFields(W, count+1)
            count += 1
        
        # Empty all other fields
        while count < 8:
            Warr = ["W1","W2","W3","W4","W5","W6","W7","W8"]
            eval("self.uiEq.edit" + Warr[count] + "name.setText(\"\")")
            eval("self.uiEq.comboStil" + str(count+1) + ".clear()")
            eval("self.uiEq.edit" + Warr[count] + "eig.setText(\"\")")
            eval("self.uiEq.spin" + Warr[count] + "w6.setValue(0)")
            eval("self.uiEq.spin" + Warr[count] + "plus.setValue(0)")
            eval("self.uiEq.spin" + Warr[count] + "h.setValue(6)")
            eval("self.uiEq.spin" + Warr[count] + "rw.setValue(0)")
            eval("self.uiEq.spin" + Warr[count] + "wm.setValue(0)")
            eval("self.uiEq.check" + Warr[count] + "FK.setChecked(False)")  
            count += 1
        
        self.initialLoad = False
        self.currentlyLoading = False
        
    def refreshKampfstile(self, index):
        logging.debug("Starting refreshKampfstile for index " + str(index))
        name = eval("self.uiEq.editW" + str(index+1) + "name.text()")
        tmp = eval("self.uiEq.comboStil" + str(index+1) + ".currentText()")
        if name != "":
            if name in Wolke.DB.waffen:
                entries = []
                entries.append(Definitionen.Kampfstile[0])
                if Wolke.DB.waffen[name].beid and Definitionen.Kampfstile[1] + " I" in Wolke.Char.vorteile:
                    entries.append(Definitionen.Kampfstile[1])
                if Wolke.DB.waffen[name].pari and Definitionen.Kampfstile[2] + " I" in Wolke.Char.vorteile:
                    entries.append(Definitionen.Kampfstile[2])
                if Wolke.DB.waffen[name].reit and Definitionen.Kampfstile[3] + " I" in Wolke.Char.vorteile:
                    entries.append(Definitionen.Kampfstile[3])
                if Wolke.DB.waffen[name].schi and Definitionen.Kampfstile[4] + " I" in Wolke.Char.vorteile:
                    entries.append(Definitionen.Kampfstile[4])
                if Wolke.DB.waffen[name].kraf and Definitionen.Kampfstile[5] + " I" in Wolke.Char.vorteile:
                    entries.append(Definitionen.Kampfstile[5])
                if Wolke.DB.waffen[name].schn and Definitionen.Kampfstile[6] + " I" in Wolke.Char.vorteile:
                    entries.append(Definitionen.Kampfstile[6])
                eval("self.uiEq.comboStil" + str(index+1) + ".setCurrentIndex(0)")
                eval("self.uiEq.comboStil" + str(index+1) + ".clear()")
                for el in entries:
                    getName = lambda : el
                    eval("self.uiEq.comboStil" + str(index+1) + ".addItem(getName())")
                if self.initialLoad:
                    stil = Definitionen.Kampfstile[Wolke.Char.waffen[index].kampfstil]
                    if stil in entries:
                        eval("self.uiEq.comboStil" + str(index+1) + ".setCurrentIndex(" + str(entries.index(stil)) + ")")
                    else:
                        eval("self.uiEq.comboStil" + str(index+1) + ".setCurrentIndex(0)")
                elif tmp in entries:
                    eval("self.uiEq.comboStil" + str(index+1) + ".setCurrentIndex(" + str(entries.index(tmp)) + ")")
                
                    
    def loadWeaponIntoFields(self, W, index):
        Warr = ["W1","W2","W3","W4","W5","W6","W7","W8"]
        count = index - 1
        getName = lambda : W.name
        eval("self.uiEq.edit" + Warr[count] + "name.setText(getName())")
        self.refreshKampfstile(count)
        getEigenschaften = lambda : ", ".join(W.eigenschaften)
        eval("self.uiEq.edit" + Warr[count] + "eig.setText(getEigenschaften())")
        eval("self.uiEq.spin" + Warr[count] + "w6.setValue("+ str(W.W6) +")")
        eval("self.uiEq.spin" + Warr[count] + "plus.setValue("+ str(W.plus) +")")
        if W.name == "Unbewaffnet":
            wsmod = Wolke.Char.rsmod + Wolke.Char.ws
            if len(Wolke.Char.rüstung) > 0:    
                wsmod += int(sum(Wolke.Char.rüstung[0].rs)/6+0.5+0.0001)
            eval("self.uiEq.spin" + Warr[count] + "h.setValue("+ str(wsmod) +")")
        else:
            eval("self.uiEq.spin" + Warr[count] + "h.setValue("+ str(W.haerte) +")")
        eval("self.uiEq.spin" + Warr[count] + "rw.setValue("+ str(W.rw) +")")
        if type(W) == Objekte.Fernkampfwaffe:
            eval("self.uiEq.spin" + Warr[count] + "wm.setValue("+ str(W.lz) +")")
            eval("self.uiEq.check" + Warr[count] + "FK.setChecked(True)")
        elif type(W) == Objekte.Nahkampfwaffe:
            eval("self.uiEq.spin" + Warr[count] + "wm.setValue("+ str(W.wm) +")")
            eval("self.uiEq.check" + Warr[count] + "FK.setChecked(False)")
        
    def selectWeapon(self, index):
        W = None
        try:
            wname = eval("self.uiEq.editW" + str(index) + "name.text()")
            for el in Wolke.DB.waffen:
                if Wolke.DB.waffen[el].name == wname:
                    W = el
                    logging.debug("Weapon found - its " + wname)
                    break
        except:
            pass
        logging.debug("Starting WaffenPicker")
        picker = WaffenPicker(W)
        logging.debug("WaffenPicker created")
        if picker.waffe is not None:
            self.currentlyLoading = True
            self.loadWeaponIntoFields(picker.waffe, index)
            self.currentlyLoading = False
            self.updateEquipment()
        
    def checkToggleEquip(self):
        if not self.currentlyLoading:
            self.currentlyLoading = True
            if self.uiEq.checkZonen.isChecked():
                self.uiEq.spinR1bauch.show()
                self.uiEq.spinR1brust.show()
                self.uiEq.spinR1larm.show()
                self.uiEq.spinR1rarm.show()
                self.uiEq.spinR1kopf.show()
                self.uiEq.spinR1bein.show()
                self.uiEq.spinR2bauch.show()
                self.uiEq.spinR2brust.show()
                self.uiEq.spinR2larm.show()
                self.uiEq.spinR2rarm.show()
                self.uiEq.spinR2kopf.show()
                self.uiEq.spinR2bein.show()
                self.uiEq.spinR3bauch.show()
                self.uiEq.spinR3brust.show()
                self.uiEq.spinR3larm.show()
                self.uiEq.spinR3rarm.show()
                self.uiEq.spinR3kopf.show()
                self.uiEq.spinR3bein.show()
                self.uiEq.spinR1RS.hide()
                self.uiEq.spinR2RS.hide()
                self.uiEq.spinR3RS.hide()
                self.uiEq.labelRS.hide()
                self.uiEq.labelBein.show()
                self.uiEq.labelBauch.show()
                self.uiEq.labelBrust.show()
                self.uiEq.labelLarm.show()
                self.uiEq.labelRarm.show()
                self.uiEq.labelKopf.show()
            else:
                self.uiEq.spinR1bauch.hide()
                self.uiEq.spinR1brust.hide()
                self.uiEq.spinR1larm.hide()
                self.uiEq.spinR1rarm.hide()
                self.uiEq.spinR1kopf.hide()
                self.uiEq.spinR1bein.hide()
                self.uiEq.spinR2bauch.hide()
                self.uiEq.spinR2brust.hide()
                self.uiEq.spinR2larm.hide()
                self.uiEq.spinR2rarm.hide()
                self.uiEq.spinR2kopf.hide()
                self.uiEq.spinR2bein.hide()
                self.uiEq.spinR3bauch.hide()
                self.uiEq.spinR3brust.hide()
                self.uiEq.spinR3larm.hide()
                self.uiEq.spinR3rarm.hide()
                self.uiEq.spinR3kopf.hide()
                self.uiEq.spinR3bein.hide()
                self.uiEq.spinR1RS.show()
                self.uiEq.spinR2RS.show()
                self.uiEq.spinR3RS.show()
                self.uiEq.labelRS.show()
                self.uiEq.labelBein.hide()
                self.uiEq.labelBauch.hide()
                self.uiEq.labelBrust.hide()
                self.uiEq.labelLarm.hide()
                self.uiEq.labelRarm.hide()
                self.uiEq.labelKopf.hide()
            self.currentlyLoading = False