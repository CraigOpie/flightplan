#!/usr/bin/env python
"""
Name:       Craig Opie
Copyright:  November 1st, 2018
Project:    Flight Plan
File:       flightPlan.py

Algorithm:
"""

# Import from PySide or PySide2 (QtWidgets)
try:
    from PySide import QtGui, QtCore
    import PySide.QtGui as QtWidgets
except ImportError:
    from PySide2 import QtGui, QtCore, QtWidgets
import sys

# Creates the Main Dialog Box as an Object (Class)
class MyGui(QtWidgets.QMainWindow):
    """ Main Dialog Box that allow reading plain text files """
    def __init__(self):
        """ Initiallizes the Main Dialog Box and establishes object variables """
        # Setup the Main Dialog Box properties
        QtWidgets.QMainWindow.__init__(self)
        self.initMenu()
        self.text = QtWidgets.QTextEdit()
        self.text.setReadOnly(True)
        self.setCentralWidget(self.text)
        self.setGeometry(250,250,700,400)
        self.setWindowTitle("Flight Plan Update Program")
        self.show()
        self.writefile = ""
        self.readfiles = []
        self.display = ""
        self.flightPlan = ""

    def initMenu(self):
        """ Creates the Main Dialog Box menu items """
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("File")

        # Opens a load Dialog for the user to load flight plan file name
        open_p = QtWidgets.QAction("Select Flight Plan", self)
        open_p.triggered.connect(self.openPFile)
        fileMenu.addAction(open_p)

        # Opens a load Dialog for the user to load new data file(s) name(s)
        open_d = QtWidgets.QAction("Open New Data Files", self)
        open_d.triggered.connect(self.openDFile)
        fileMenu.addAction(open_d)

        # Parses files that are loaded into flight plan
        parse = QtWidgets.QAction("Parse Information", self)
        parse.triggered.connect(self.parseFile)
        fileMenu.addAction(parse)

        # Opens a save Dialog for the user to save the displayed information
        save_ = QtWidgets.QAction("Save New Flight Plan", self)
        save_.triggered.connect(self.saveFile)
        fileMenu.addAction(save_)

        # Allows the user to quit the application
        quit_ = QtWidgets.QAction("Quit", self)
        quit_.triggered.connect(self.closeFile)
        fileMenu.addAction(quit_)

    def openPFile(self):
        """ Opens a plain text file to display in the Main Dialog Box """
        filter = "XYZ (*.xyz);;TXT (*.txt)"
        filenames = QtWidgets.QFileDialog()
        filenames.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        names = filenames.getOpenFileNames(self, "Open File",".", filter)
        if not names:
            self.display += ("\n\nError: Something went wrong.  Please contact CraigOpie@Gmail.com")
            self.text.setText(self.display)
        else:
            name = names[0]
            filename = name[0]
            self.writefile = filename
            self.display += ("\n\nFlight Plan has been loaded: \n" + filename)
            self.text.setText(self.display)

    def openDFile(self):
        """ Opens a plain text file to display in the Main Dialog Box """
        filter = "XYZ (*.xyz);;TXT (*.txt)"
        filenames = QtWidgets.QFileDialog()
        filenames.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        names = filenames.getOpenFileNames(self, "Open File",".", filter)
        if not names:
            self.display += ("\n\nError: Something went wrong.  Please contact CraigOpie@Gmail.com.")
            self.text.setText(self.display)
        else:
            self.readfiles = names[0]
            self.display += ("\n\nNew Data files have been loaded: ")
            for names in self.readfiles:
                self.display += ("\n" + names)
            self.text.setText(self.display)

    def parseFile(self):
        readfiles = self.readfiles
        writefile = self.writefile

        def DataIn(filename):
            infile = open(filename, "r")
            content = infile.readlines()
            infile.close()

            linedata = []
            plan = []
            plannum = []
            planrev = []

            for eachline in content:
                eachline = eachline.strip().split(" ")
                if eachline[0] == "Line" or eachline[0] == "line":
                    linedata.append(eachline)

            for eachline in linedata:
                plan.append(eachline[1])

            for eachline in plan:
                eachline = list(eachline)
                flight = ""
                for num in range(len(eachline)-1):
                    flight += eachline[num]
                plannum.append(flight)
                planrev.append(eachline[len(eachline)-1])

            for eachline in range(len(planrev)):
                planrev[eachline] = int(planrev[eachline])

            data = dict(zip(plannum, planrev))
            return(data)

        def DataOut(filename, revisions):
            infile = open(filename, "r")
            content = infile.readlines()
            infile.close()

            for eachline in content:
                eachline = eachline.strip("\n").split(" ")
                if eachline[0] == "Line" or eachline[0] == "line":
                    for key in revisions:
                        if eachline[1] == key:
                            eachline[1] = revisions[key]

                line = " "
                eachline = line.join(eachline)
                self.flightPlan += eachline+"\n"

        if not readfiles:
            self.display += ("\n\nError: Please load the Data Files first.")
            self.text.setText(self.display)
        else:
            if (writefile != ""):
                revisions = {}
                for eachfile in readfiles:
                    file1 = DataIn(eachfile)
                    file2 = DataIn(writefile)

                    for key in file2:
                        if key in file1:
                            if file2[key] != file1[key]:
                                if file2[key] < file1[key]:
                                    org = key+str(file2[key])
                                    file2[key] = file1[key]
                                    rev = key+str(file2[key])
                                    revisions[org] = rev

                content = DataOut(writefile, revisions)
                self.display += ("\n\nYou are about to make " + str(len(revisions)) + " revision(s):")
                for eachline in revisions:
                    self.display += "\nline " + eachline + " became " + revisions[eachline]

                self.text.setText(self.display)
            else:
                self.display += ("\n\nError: Please load the Flight Plan first.")
                self.text.setText(self.display)

    def saveFile(self):
        """ Saves parsed information """
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File",".")
        if (filename != ""):
            outfile = open(filename, "w")
            outfile.write(self.flightPlan)
            outfile.close()
            self.closeFile()

    def closeFile(self):
        sys.exit(app.exec_())

# Specifies the variable that references Qt module data
app = QtWidgets.QApplication(sys.argv)

# Creates an instance of the MyGui Class/Object
mygui = MyGui()

# Executes the above code to create the Main Dialog Box
sys.exit(app.exec_())
