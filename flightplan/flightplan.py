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
        self.text.setText("Please select your flight plan and data files: ")
        self.writefile = ""
        self.readfiles = []
        self.display = ""
        self.flightPlan = ""

    def initMenu(self):
        """ Creates the Main Dialog Box menu items """
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("File")

        # Opens a load Dialog for the user to load flight plan file name
        open_p = QtWidgets.QAction("Flight Plan", self)
        open_p.triggered.connect(self.openPFile)
        fileMenu.addAction(open_p)

        # Opens a load Dialog for the user to load new data file(s) name(s)
        open_d = QtWidgets.QAction("Data File(s)", self)
        open_d.triggered.connect(self.openDFile)
        fileMenu.addAction(open_d)

        # Opens a save Dialog for the user to save the displayed information
        save_ = QtWidgets.QAction("Save", self)
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
        # Checks to see that a file name was added if not, display an error message
        if not names:
            self.display += ("\n\nError: Something went wrong.  Please contact CraigOpie@Gmail.com")
            self.text.setText(self.display)
        # If a file name was added then the path is displayed for the user
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
        # Checks to see that file names were added if not, display an error message
        if not names:
            self.display += ("\n\nError: Something went wrong.  Please contact CraigOpie@Gmail.com.")
            self.text.setText(self.display)
        # If file names were added then the path is displayed for the user
        else:
            self.readfiles = names[0]
            self.display += ("\n\nNew Data files have been loaded: ")
            for names in self.readfiles:
                self.display += ("\n" + names)
            self.text.setText(self.display)
            # Immediately parse the information
            self.parseFile()

    def parseFile(self):
        """ Parses the revisions from the data files into the flight plan """
        readfiles = self.readfiles
        writefile = self.writefile

        # Loads the information from the files into a list
        def DataIn(filename):
            infile = open(filename, "r")
            content = infile.readlines()
            infile.close()

            linedata = []
            plan = []
            plannum = []
            planrev = []

            # Splits out the lines and searches for lines beginning with 'Line' or 'line' and adds
            # the line to a separate list
            for eachline in content:
                eachline = eachline.strip().split(" ")
                if eachline[0] == "Line" or eachline[0] == "line":
                    linedata.append(eachline)

            # Takes the number information from the 'line' data
            for eachline in linedata:
                plan.append(eachline[1])

            # Breaks the flight number data into a list of each character and then removes the last
            # character (revision number), then recombines the flight number without the revision
            # and adds it to the 'plannum' list.  The revision is then added to the list 'planrev'
            for eachline in plan:
                eachline = list(eachline)
                flight = ""
                for num in range(len(eachline)-1):
                    flight += eachline[num]
                plannum.append(flight)
                planrev.append(eachline[len(eachline)-1])

            # Converts the revision values into an integer for comparison
            for eachline in range(len(planrev)):
                planrev[eachline] = int(planrev[eachline])

            # Combines the flight number and revision into a dictionary with the flight number as
            # the key and the revision as the value
            data = dict(zip(plannum, planrev))
            return(data)

        # Loads the flight plan as a list 'content'
        def DataOut(filename, revisions):
            infile = open(filename, "r")
            content = infile.readlines()
            infile.close()

            # Searches through the flight plan 'content' for 'lines' or 'Lines' and compares the
            # flight number to the original flight number stored in revisions.  Then where ever
            # the flight numbers match it replaces the old number with the new number/revision
            for eachline in content:
                eachline = eachline.strip("\n").split(" ")
                if eachline[0] == "Line" or eachline[0] == "line":
                    for key in revisions:
                        if eachline[1] == key:
                            eachline[1] = revisions[key]

                # Add the spaces back into each list item and joins them back as a string to
                # recreate the flight plan
                line = " "
                eachline = line.join(eachline)
                self.flightPlan += eachline+"\n"

        # If data is not loaded in from the flight plan and data files then issue an error
        # Otherwise, for each data file perform the above DataIn function on the flight plan and
        # data file.  Then compare the dictionary flight plan numbers and for matching flight plans
        # check the revision values. If the revision value in data is larger than the existing
        # revision value in flight plan, the flight plan is overwritten to the new revision number
        # and the user is notified of the pending changes in the dialog box
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
        """ Saves parsed information and exits the application """
        filename = self.writefile
        if (filename != ""):
            outfile = open(filename, "w")
            outfile.write(self.flightPlan)
            outfile.close()
            self.closeFile()

    def closeFile(self):
        """ Exits the application """
        sys.exit(app.exec_())

# Specifies the variable that references Qt module data
app = QtWidgets.QApplication(sys.argv)

# Creates an instance of the MyGui Class/Object
mygui = MyGui()

# Closes the application
sys.exit(app.exec_())
