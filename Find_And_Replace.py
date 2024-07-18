"""
NAME: Find And Replace
ICON: icon.png
KEYBOARD_SHORTCUT: Ctrl+Shift+F
SCOPE:
Searches node names for string and replaces with set new string (applicible to selection or all nodes)

"""

# The following symbols are added when run as a shelf item script:
# exit():      Allows 'error-free' early exit from the script.
# console_print(message, raiseTab=False):
#              Prints the given message to the result area of the largest
#              available Python tab.
#              If raiseTab is passed as True, the tab will be raised to the
#              front in its pane.
#              If no Python tab exists, prints the message to the shell.
# console_clear(raiseTab=False):
#              Clears the result area of the largest available Python tab.
#              If raiseTab is passed as True, the tab will be raised to the
#              front in its pane.


#   NOTES:
#   - Clean up how stuff printed to console looks (delete un-needed, add spaces, etc.)



from PyQt5 import (QtGui, QtWidgets)
from Katana import (NodegraphAPI, UI4)

# Class implementing a dialog to configure settings for a Search & Replace function
class SaR_Dialog(QtWidgets.QDialog):

    # Set up dialog box
    def __init__(self,):

        QtWidgets.QDialog.__init__(self, UI4.App.MainWindow.GetMainWindow())
        self.setWindowTitle('Search & Replace')
        self.move(QtGui.QCursor.pos())
        self.setMinimumWidth(500)
        self.setMinimumHeight(250)
        self.initUI()

    # Set up dialog box UI
    def initUI(self):

        # Create and setup 'Search' text Input
        self.Search_Label = QtWidgets.QLabel('Search For:') 
        self.Search_Label.setObjectName('Search_Label')
        self.Search_Label.setMinimumWidth(80)
        self.Search_Edit = QtWidgets.QLineEdit()
        self.Search_Edit.setObjectName('Search_Edit')
        # Set up 'Search' layout
        self.Search_Layout = QtWidgets.QHBoxLayout()
        self.Search_Layout.addWidget(self.Search_Label)
        self.Search_Layout.addWidget(self.Search_Edit)


        # Create and setup 'Replace' text input
        self.Replace_Label = QtWidgets.QLabel('Replace With:')
        self.Replace_Label.setObjectName('Replace_Label')
        self.Replace_Label.setMinimumWidth(80)
        self.Replace_Edit = QtWidgets.QLineEdit()
        self.Replace_Edit.setObjectName('Replace_Edit')
        # Set up 'Replace' layout
        self.Replace_Layout = QtWidgets.QHBoxLayout()
        self.Replace_Layout.addWidget(self.Replace_Label)
        self.Replace_Layout.addWidget(self.Replace_Edit)


        # Create and setup 'Selected/Type/All Nodes' buttons
        self.Selected_RadioBox = QtWidgets.QRadioButton('Selected Nodes')
        self.Selected_RadioBox.setObjectName('Selected_RadioBox')
        self.Selected_RadioBox.setChecked(True)
        self.Type_RadioBox = QtWidgets.QRadioButton('All Nodes By Type')
        self.Type_RadioBox.setObjectName('Type_RadioBox')
        self.All_RadioBox = QtWidgets.QRadioButton('All Nodes')
        self.All_RadioBox.setObjectName('All_RadioBox')
        # Set up 'Selected/Type/All Nodes' buttons layout
        self.NodeSelect_Layout = QtWidgets.QHBoxLayout()
        self.NodeSelect_Layout.addSpacing(100)
        self.NodeSelect_Layout.addWidget(self.Selected_RadioBox)
        self.NodeSelect_Layout.addSpacing(20)
        self.NodeSelect_Layout.addWidget(self.Type_RadioBox)
        self.NodeSelect_Layout.addSpacing(20)
        self.NodeSelect_Layout.addWidget(self.All_RadioBox)
        self.NodeSelect_Layout.addStretch()


        # Create and setup 'Type' text Input
        self.Type_Label = QtWidgets.QLabel('Node Type:') 
        self.Type_Label.setObjectName('Type_Label')
        self.Type_Label.setMinimumWidth(80)
        self.Type_Edit = QtWidgets.QLineEdit()
        self.Type_Edit.setObjectName('Type_Edit')
        self.Type_Edit.setMinimumWidth(100)
        self.Type_Edit.setMaximumWidth(170)
        # Link 'Type' Radio Button to function
        self.Type_RadioBox.toggled.connect(self.Type_Button_Toggled)
        # Set up 'Type' layout
        self.Type_Layout = QtWidgets.QHBoxLayout()
        self.Type_Layout.addWidget(self.Type_Label)
        self.Type_Layout.addWidget(self.Type_Edit)
        self.Type_Layout.addStretch()
        self.Type_Label.hide()
        self.Type_Edit.hide()


        # Create and setup 'Replace/Apply/Cancel' buttons
        self.Replace_Button = QtWidgets.QPushButton('Replace')
        self.Replace_Button.setObjectName('Replace_Button')
        self.Apply_Button = QtWidgets.QPushButton('Apply')
        self.Apply_Button.setObjectName('Apply_Button')
        self.Cancel_Button = QtWidgets.QPushButton('Cancel')
        self.Cancel_Button.setObjectName('Cancel_Button')
        # Link 'Replace/Apply/Cancel' buttons to functions
        self.Replace_Button.clicked.connect(self.Replace_Button_Clicked)
        self.Apply_Button.clicked.connect(self.Apply_Button_Clicked)
        self.Cancel_Button.clicked.connect(self.Cancel_Button_Clicked)
        # Set up 'Replace/Apply/Cancel' buttons layout
        self.Button_Layout = QtWidgets.QHBoxLayout()
        self.Button_Layout.addWidget(self.Replace_Button)
        self.Button_Layout.addWidget(self.Apply_Button)
        self.Button_Layout.addWidget(self.Cancel_Button)


        # Set up dialog box layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addSpacing(10)
        self.layout.addLayout(self.Search_Layout)
        self.layout.addLayout(self.Replace_Layout)
        self.layout.addSpacing(10)
        self.layout.addLayout(self.NodeSelect_Layout)
        self.layout.addSpacing(10)
        self.layout.addLayout(self.Type_Layout)
        self.layout.addStretch()
        self.layout.addLayout(self.Button_Layout)

        self.setLayout(self.layout)

    # Action when 'All Nodes By Type' button is toggled
    def Type_Button_Toggled(self):
        if self.Type_RadioBox.isChecked() == True:
            self.Type_Label.show()
            self.Type_Edit.show()

        else:
            self.Type_Label.hide()
            self.Type_Edit.hide()

    # Action when 'Replace' button is clicked
    def Replace_Button_Clicked(self):
        
        self.Selection_Check()

        # Check something is selected & there's something in 'Search For:' before closing
        if self.Selected_RadioBox.isChecked() == True:
            if NodegraphAPI.GetAllSelectedNodes() != []:
                if self.Search_Edit.text() != (""):
                    self.close() 

        # Check something is avaiable & there's something in 'Search For:' before closing
        elif self.Type_RadioBox.isChecked() == True:
            if NodegraphAPI.GetAllNodesByType(self.Type_Edit.text()) != []:
                if self.Search_Edit.text() != (""):
                    self.close() 

        # Check something is avaiable & there's something in 'Search For:' before closing
        elif self.All_RadioBox.isChecked() == True:  
            if (len(NodegraphAPI.GetAllNodes())) != 1:
                if self.Search_Edit.text() != (""):
                    self.close()

    # Action when 'Apply' button is clicked
    def Apply_Button_Clicked(self):
        self.Selection_Check()
 
    # Action when 'Cancel' button is clicked
    def Cancel_Button_Clicked(self):
        self.close()
        
    # Run through and check if scope was set to "Selected" or "All"
    def Selection_Check(self):
        print ("")
        print ("Running Search & Replace:")

        # See if "Selected Nodes" Box is checked
        if self.Selected_RadioBox.isChecked() == True:            
            
            SelectedNodes = NodegraphAPI.GetAllSelectedNodes()

            # See if any Nodes are selected
            if SelectedNodes == []:
                print ("    No Nodes Selected")
                QtWidgets.QMessageBox.warning(
                 None,
                 "Warning",
                 "No Nodes Selected"
                )

            else:
                self.SaR_Function(SelectedNodes, "Selected_Nodes")       

        # See if "All Nodes By Type" Box is checked
        elif self.Type_RadioBox.isChecked() == True:            
            
            TypeNodes = NodegraphAPI.GetAllNodesByType(self.Type_Edit.text())

            # See if any Nodes of set type are present
            if TypeNodes == []:
                print ("    No Nodes of that Type Available")
                QtWidgets.QMessageBox.warning(
                    None,
                    "Warning",
                    "No Nodes of that Type Available"
                    )
                
            else:
                self.SaR_Function(TypeNodes, "Type_Nodes")

        # See if "All Nodes" Box is checked
        elif self.All_RadioBox.isChecked() == True:            
            
            AllNodes = NodegraphAPI.GetAllNodes()

            # See if any Nodes are present, (len(AllNodes)) set to 1 because of rootNode
            if (len(AllNodes)) == 1:
                print ("    No Nodes Available")
                QtWidgets.QMessageBox.warning(
                    None,
                    "Warning",
                    "No Nodes Available"
                    )
            
            else:
                self.SaR_Function(AllNodes, "All_Nodes")
        
        else:
            print ("    Could Not Read Scope Choice")
            QtWidgets.QMessageBox.warning(
                 None,
                 "Warning",
                 "Could Not Read Scope Choice"
                )       

    # Looks through each node for if searched string is present in node names,
    # if so replace with new string
    def SaR_Function(self, NodeCollection, SelectionType):
        
        #Set checker value for 
        ReplacedNode = 0

        # Checks if there is input in 'Search For:' Box
        if self.Search_Edit.text() == (""):
            print ("   'Search For:' Box Missing Input")
            QtWidgets.QMessageBox.warning(
                 None,
                 "Warning",
                 "'Search For:' Box Missing Input"
                )  

        else:
            print ("    Replacing '", self.Search_Edit.text(), "' with '", self.Replace_Edit.text(), "'")

            # Goes through each node and runs SaR Function
            for Node in NodeCollection:

                NodeName = Node.getName()

                # Disregards the root Node (safeguard)
                if NodeName == "rootNode": continue

                if NodeName.find("Backdrop") != -1: continue


                # Skips any nodes that don't have searched string
                if NodeName.find(self.Search_Edit.text()) == -1: 

                    # Togggles 'node Unaffected' on for 'Selected Nodes' checkbox
                    if SelectionType == "Selected_Nodes":
                        print ("        x", NodeName)
                    continue
                
                # Replaces searched string with new string
                else:
                    NewNodeName = NodeName.replace(self.Search_Edit.text(), self.Replace_Edit.text())
                    Node.setName (NewNodeName)

                    ReplacedNode = 1
                    print ("       ", NodeName, "-->", NewNodeName)
                    
                    NameParam = NodegraphAPI.GetNode(NewNodeName).getParameter('name')

                    if Node.getType() == 'ArnoldShadingNode' or 'NetworkMaterial':
                        if NameParam:
                            NameParam.setValue(NewNodeName, 0)
                    
                    else:
                        continue

            # Checks if any node names got replaced (updates 'ReplacedNode')
            if ReplacedNode == 0:
                print ("    No Nodes Were Replaced")
                QtWidgets.QMessageBox.warning(
                    None,
                    "Warning",
                    "No Nodes Were Replaced"
                    )  

# Create instance of Dialog class and show dialog box
sar_Dialog = SaR_Dialog()
sar_Dialog.show()