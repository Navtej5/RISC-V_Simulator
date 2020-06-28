import sys
from PyQt5.QtCore import Qt
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtWidgets import *
import os
import pandas as pd
from check import original_to_basic,text_to_original
from testfinal import *
from PyQt5.QtGui import QFont
from phase2 import *

sometext="Welcome To RISC-V Simulator"
print(sometext)


class TabWidget(QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("RISC-V Simulator")
        self.top=100
        self.left=100
        self.width=400
        self.height=300
        self.setGeometry(50,50,1500,900)
        
    #def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("home.jpg"))
        #self.setWindowTitle(self.title)
        #self.setGeometry(self.left,self.top,self.width,self.height)
        
        tabWidget= QTabWidget()
        tabWidget.setStyleSheet("QTabWidget::tab-bar{alignment:center;}QTabBar::tab { min-width: 200px; }")
        tab1=FirstTab()
        tab2=SecondTab()
        index1=tabWidget.addTab(tab1,"Editor")
        tabWidget.setTabIcon(index1,QtGui.QIcon('text.png'))
        tabWidget.setIconSize(QtCore.QSize(30, 30))
        
        tabWidget.setFont(QtGui.QFont('SansSerif', 13))
        index2=tabWidget.addTab(tab2,"Simulator")
        tabWidget.setTabIcon(index2,QtGui.QIcon('simulator.png'))
        tabWidget.setIconSize(QtCore.QSize(40, 40))

        vbox = QVBoxLayout()
        #vbox.setAlignment(AlignCenter)
        vbox.addWidget(tabWidget)
        self.setLayout(vbox)
        
        
        self.show()


class FirstTab (QWidget):

        def __init__(self):
            super().__init__()
            self.editor = QTextEdit(self)
            self.clr_btn = QPushButton('Clear')
            self.sav_btn = QPushButton('Save')
            self.opn_btn = QPushButton('Open')
            self.check_btn = QPushButton('Check')
            self.check_btn.setIcon(QtGui.QIcon('che.png'))
            self.check_btn.setIconSize(QtCore.QSize(25,25))
            self.opn_btn.setIcon(QtGui.QIcon('open.png'))
            self.opn_btn.setIconSize(QtCore.QSize(25,25))
            self.sav_btn.setIcon(QtGui.QIcon('save.png'))
            self.sav_btn.setIconSize(QtCore.QSize(25,25))
            self.clr_btn.setIcon(QtGui.QIcon('clear.png'))
            self.clr_btn.setIconSize(QtCore.QSize(25,25))
            self.init_ui()

        def init_ui(self):
            v_layout = QVBoxLayout()
            h_layout = QHBoxLayout()

            h_layout.addWidget(self.clr_btn)
            h_layout.addWidget(self.sav_btn)
            h_layout.addWidget(self.opn_btn)
            h_layout.addWidget(self.check_btn)

            v_layout.addWidget(self.editor)
            v_layout.addLayout(h_layout)

            self.sav_btn.clicked.connect(self.save_text)
            self.clr_btn.clicked.connect(self.clear_text)
            self.opn_btn.clicked.connect(self.open_text)
            self.check_btn.clicked.connect(self.buttonClicked)
            #global sometext
            #sometext = self.editor.toPlainText()
            #print (sometext)
            #data=sometext.split()
            self.setLayout(v_layout)
            self.setWindowTitle('PyQt5 TextEdit')

            self.lbl = QLabel(self)
            self.lbl.move(1000, 9)
            self.label =QLabel(self)
            self.label.move(1100,12)
            

            self.show()

        def save_text(self):
            filename = QFileDialog.getSaveFileName(self, 'Save File', os.getenv('HOME'))
            with open(filename[0], 'w') as f:
                my_text = self.editor.toPlainText()
                f.write(my_text)

        def open_text(self):
            filename = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
            with open(filename[0], 'r') as f:
                file_text = f.read()
                self.editor.setText(file_text)

        def clear_text(self):
            self.editor.clear()

        def buttonClicked(self):
            #mem.text=[]
            #mem.data=[]
            sender = self.sender()
            #self.tab2=QWidget()
            #tabWidget= QTabWidget()
            #tabWidget.addTab(FirstTab(),"Simulator")
            writefile=open("t.asm","w")
            global sometext
            sometext=self.editor.toPlainText()
            all_lines=sometext.splitlines()
            writefile.write(sometext)
            writefile.close()
            #import reader
            instructions, labela,dataa = getDirectives()
            convertToMC(instructions, labela,dataa , data_out)
            from reader_main import iserror
            print (iserror)
            if iserror==0:
                self.lbl.setFont(QFont("dasd",13))
                self.lbl.setText("No Error")
                self.label.setPixmap(QtGui.QPixmap("correct.png"))
                self.label.show()
            else:
                #self.lbl.setFont(QFont("dasd",13))
                self.lbl.setText("Error!")
                self.label.hide()

            #print (sometext)

class SecondTab (QWidget):
    
    def __init__(self):
            super().__init__()
            #self.editor = QTextEdit(self)
            self.run_btn = QPushButton('Run')
            self.step_btn = QPushButton('Step')
            self.prev_btn =QPushButton('Previous')
            self.reset_btn = QPushButton('reset')
            self.stop_btn = QPushButton('Stop')
            self.assemble_btn = QPushButton('Assemble')
            self.tablewidget=QTableWidget(32,4)
            self.table2=QTableWidget(3,4)
            self.cb=QComboBox()
            self.tab11= QTabWidget()
            self.tabb=registertab()
            self.tab2=memorytab()
            self.tab11.addTab(self.tabb,"Register")
            self.tab11.addTab(self.tab2,"Memory")
            self.init_ui()
            self.row_id=1
            #self.table()

    def init_ui(self):
            v_layout = QVBoxLayout()
            h_layout = QHBoxLayout()
            h1=QHBoxLayout()
            v2=QVBoxLayout()
            h1.addWidget(self.assemble_btn)
            h1.addWidget(self.run_btn)
            h1.addWidget(self.step_btn)
            h1.addWidget(self.prev_btn)
            h1.addWidget(self.reset_btn)
            h1.addWidget(self.stop_btn)
            v2.addWidget(self.tab11)
            #v2.addWidget(self.table2)
            #v2.addWidget(self.cb)


            h_layout.addWidget(self.tablewidget)
            h_layout.addLayout(v2)
            
            v_layout.addLayout(h1)
            v_layout.addLayout(h_layout)

            self.assemble_btn.clicked.connect(self.assemble)
            self.run_btn.clicked.connect(self.run_code)
            self.step_btn.clicked.connect(self.step_code)
            self.reset_btn.clicked.connect(self.reset_code)
            self.prev_btn.clicked.connect(self.previous_code)
            self.stop_btn.clicked.connect(self.stop_code)
            self.setLayout(v_layout)
            self.setWindowTitle('PyQt5 TextEdit')

            self.show()

    def assemble(self):
        self.row_id=1
        self.table()

    def run_code(self):
        count=run()
        count=int(count/4)
        self.row_id=count+1
        self.table()
        self.tabb.settableregister1()
        #print(self.row_id)

    def step_code(self):
        row=step()
        row=int(row/4)+1
        #print(row)
        self.row_id=row
        self.table()
        self.tabb.settableregister1()
        self.tab2.settable2()

    def reset_code(self):
        reset()
        from testfinal import M
        print(M.data)
        mem.data=M.data
        self.row_id=1
        self.table()
        self.tabb.settableregister1()
        self.tab2.settable1()

    def previous_code(self):
        previous()

    def stop_code(self):
        stop()

    def table(self):
        #all_lines=sometext.splitlines()
        text=original_to_basic(sometext)
        optimized_code=text_to_original(sometext)
        all_lines=optimized_code.splitlines()
        print (all_lines)
        #print (text)
        da=text.splitlines()
        j=1
        readfile=open("out.mc","r+")
        mc=readfile.readlines()
        rfile=open("outfile.mc","r+")
        bc=rfile.readlines()
        #print(bc)
        #print (mc)
        #self.tablewidget.setFrameStyle(0)
        #self.tablewidget.setItem()
        self.tablewidget.setShowGrid(False)
        #tabWidget.setStyleSheet("QTabWidget::tab-bar{alignment:center;}QTabBar::tab { min-width: 200px; }")
        self.tablewidget.setStyleSheet('QTableView::item {border-right: 1px solid #d6d9dc;}QTableView::item {alignment:center;}')
        #self.tablewidget.setStyleSheet('QHeaderView { font-size: 21pt; }')
        self.tablewidget.horizontalHeader().setVisible(False)
        #self.tablewidget.verticalHeader().setVisible(False)
        item1=QTableWidgetItem("MACHINE CODE")
        item1.setFont(QFont("sads",9,))
        item1.setTextAlignment(Qt.AlignHCenter)
        item2=QTableWidgetItem("BASIC CODE")
        item2.setFont(QFont("sads",9))
        item2.setTextAlignment(Qt.AlignHCenter)
        item3=QTableWidgetItem("ORIGINAL CODE")
        item3.setFont(QFont("sads",9))
        item3.setTextAlignment(Qt.AlignHCenter)
        item4=QTableWidgetItem("PC")
        item4.setFont(QFont("sads",9))
        item4.setTextAlignment(Qt.AlignHCenter)
        self.tablewidget.setItem(0,1,item1)
        self.tablewidget.setItem(0,2,item2)
        self.tablewidget.setItem(0,3,item3)
        self.tablewidget.setItem(0,0,item4)
        for i in bc:
            #print(i)
            i=i.split(' ',2)
            #print(i)
            item=QTableWidgetItem(i[2])
            #print(item)
            item.setTextAlignment(Qt.AlignHCenter)
            self.tablewidget.setItem(j,2,item)
            #self.tablewidget.insertRow(j)
            j=j+1
        j=1
        flag=0
        for i in da:
                item=QTableWidgetItem(i)
                item.setTextAlignment(Qt.AlignHCenter)
                self.tablewidget.setItem(j,3,item)
                #self.tablewidget.insertRow(j)
                j=j+1
        j=1
        t=0
        #print (rext)
        for i in bc:
            i=i.split()
            i1=QTableWidgetItem(i[0])
            i2=QTableWidgetItem(i[1])
            i1.setTextAlignment(Qt.AlignHCenter)
            i2.setTextAlignment(Qt.AlignHCenter)
            self.tablewidget.setItem(j,0,i1)
            self.tablewidget.setItem(j,1,i2)
            #self.tablewidget.insertRow(j)
            j=j+1
            t=t+4
        #self.tablewidget.resizeColumnsToContents()
        self.tablewidget.setColumnWidth(0,50)
        self.tablewidget.setColumnWidth(1,200)
        self.tablewidget.setColumnWidth(2,200)
        self.tablewidget.setColumnWidth(3,200)
        self.tablewidget.setRowHeight(0,25)
        self.tablewidget.selectRow(self.row_id)
        self.tablewidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
class registertab(QWidget):
    def __init__(self):
        super().__init__()
        self.tableregister=QTableWidget(32,2)
        self.tableregister.setColumnWidth(0,100)
        self.tableregister.setColumnWidth(1,200)
        self.dict1={'x0':'0x00000000','x1':'0x00000000','x2':'0x7FFFFFF0','x3':'0x10000000','x4':'0x00000000','x5':'0x00000000','x6':'0x00000000','x7':'0x00000000','x8':'0x00000000','x9':'0x00000000',
        'x10':'0x00000000','x11':'0x00000000','x12':'0x00000000','x13':'0x00000000','x14':'0x00000000','x15':'0x00000000','x16':'0x00000000','x17':'0x00000000','x18':'0x00000000','x19':'0x00000000'
        ,'x20':'0x00000000','x21':'0x00000000','x22':'0x00000000','x23':'0x00000000','x24':'0x00000000','x25':'0x00000000','x26':'0x00000000','x27':'0x00000000','x28':'0x00000000','x29':'0x00000000'
        ,'x30':'0x00000000','x31':'0x00000000'}
        #self.table2=QTableWidget(3,4)
        #self.table3=QTableWidget(10,4)
        #self.table4=QTableWidget(7,4)
        self.cb=QComboBox()
        #self.init_ui1()
        #self.combobox()
        self.settableregister1()
        self.combobox()
        self.init_ui()
    def init_ui(self):
        v=QVBoxLayout()
        v.addWidget(self.tableregister)
        v.addWidget(self.cb)
        self.setLayout(v)
        self.show()
    def settableregister1(self):
        self.tableregister.horizontalHeader().setVisible(False)
        self.tableregister.verticalHeader().setVisible(False)
        from phase2 import registers
        #print(registers)
        j=0
        for v in registers:
            try:
                t=hex(int(v,2))
                t=t.replace("0x","")
                n=len(t)
                n=7-n
                while n>=0:
                    t="0"+ t
                    n=n-1
                t="0x"+ t
            except:
                t="0x00000000"
            #print(t)
            #print(r)
            #print(v)
            item="x"+str(j)
            self.tableregister.setItem(j,0,QTableWidgetItem(item))
            self.tableregister.setItem(j,1,QTableWidgetItem(t))
            j=j+1
        #self.tableregister
        #self.tableregister.clearContents()
    def settableregister2(self):
        self.tableregister.horizontalHeader().setVisible(False)
        self.tableregister.verticalHeader().setVisible(False)
        self.tableregister.clearContents()
        from phase2 import registers
        j=0
        for v in registers:
            try:
                t=str(int(v,2))
            except:
                t="0x00000000"
            print(t)
            item="x"+str(j)
            self.tableregister.setItem(j,0,QTableWidgetItem(item))
            self.tableregister.setItem(j,1,QTableWidgetItem(t))
            j=j+1

    def settableregister4(self):
        self.tableregister.horizontalHeader().setVisible(False)
        self.tableregister.verticalHeader().setVisible(False)
        self.tableregister.clearContents()
        from phase2 import registers
        j=0
        for v in registers:
            dec=int(v,2)
            if dec>0 and dec<128: 
                t=chr(dec)
            else:
                t='NA'
            item="x"+str(j)
            self.tableregister.setItem(j,0,QTableWidgetItem(item))
            self.tableregister.setItem(j,1,QTableWidgetItem(t))
            j=j+1

    def combobox(self):
        self.cb.addItems(["Hex","Decimal","ASCII"])
        self.cb.currentIndexChanged.connect(self.selectionchange)

    def selectionchange(self,i):
        #print "Items in the list are :"
        if i==0:
            self.settableregister1()
        elif i==1:
            self.settableregister2()
        elif i==2:
            self.settableregister4()

class memorytab(QWidget):
    def __init__(self):
        super().__init__()
        self.table1=QTableWidget(1000,5)
        self.table2=QTableWidget(3,4)
        self.table3=QTableWidget(10,4)
        self.table4=QTableWidget(7,4)
        self.cb=QComboBox()
        self.table1.setColumnWidth(0,200)
        self.table1.setColumnWidth(1,200)
        self.table1.setColumnWidth(2,200)
        self.table1.setColumnWidth(3,200)
        self.table1.setRowHeight(0,25)
        #self.init_ui1()
        self.combobox()
        self.setdefault()
        self.init_ui1()
    def init_ui1(self):
        v=QVBoxLayout()
        v.addWidget(self.table1)
        v.addWidget(self.cb)
        self.setLayout(v)
        self.show()
    def combobox(self):
        self.cb.addItems(["-select-","Text","Data","Heap","Stack"])
        self.cb.currentIndexChanged.connect(self.selectionchange)
    def selectionchange(self,i):
        #print "Items in the list are :"
        if i==0:
            self.setdefault()
        elif i==1:
            self.settable1()
        elif i==2:
            self.settable2()
        elif i==3:
            self.settable3()
        else:
            self.settable4()

    def settable1(self):
        #from phase2 import mem
        print(mem.text)
        #print("\n\n\n\n")
        #print(mem.text)
        #self.tablewidget.setItem()
        self.table1.setShowGrid(True)
        self.table1.clearContents()
        self.table1.horizontalHeader().setVisible(False)
        self.table1.verticalHeader().setVisible(False)
        self.table1.setItem(0,0,QTableWidgetItem("Address"))
        self.table1.setItem(0,1,QTableWidgetItem("+0"))
        self.table1.setItem(0,2,QTableWidgetItem("+1"))
        rfile=open("outfile.mc","r+")
        bc=rfile.readlines()
        #words=data.split()
        #print(words)
        flag=1
        j=1
        t=0

        for i in bc:
            i=i.split()
            #print (i[0])
            self.table1.setItem(j,0,QTableWidgetItem(i[0]))
            self.table1.setItem(j,1,QTableWidgetItem(i[1][8]+i[1][9]))
            self.table1.setItem(j,2,QTableWidgetItem(i[1][6]+i[1][7]))
            self.table1.setItem(j,3,QTableWidgetItem(i[1][4]+i[1][5]))
            self.table1.setItem(j,4,QTableWidgetItem(i[1][2]+i[1][3]))
            j=j+1
            t=t+4
            
        #self.table1.clearContents()
        self.table1.setItem(0,3,QTableWidgetItem("+2"))
        self.table1.setItem(0,4,QTableWidgetItem("+3"))
        #self.table1.clearContents()
        #self.table1.setItem(0,5,QTableWidgetItem("sf"))
        self.table1.resizeColumnsToContents()
        self.table1.setColumnWidth(500,500)

    def settable2(self):
        self.table1.setShowGrid(True)
        self.table1.clearContents()
        self.table1.setItem(0,0,QTableWidgetItem("Address"))
        self.table1.setItem(0,1,QTableWidgetItem("+0"))
        self.table1.setItem(0,2,QTableWidgetItem("+1"))
        self.table1.setItem(0,3,QTableWidgetItem("+2"))
        self.table1.setItem(0,4,QTableWidgetItem("+3"))
        j=0
        t=268435456
        for i in mem.data:
            #print (i)
            k=(j%4)+1
            print(j)
            o=int(j/4)+1
            #k=j%4
            self.table1.setItem(o,0,QTableWidgetItem(hex(t-3)))
            self.table1.setItem(o,k,QTableWidgetItem(str(i)))
            self.table1.setItem(o,k,QTableWidgetItem(str(i)))
            self.table1.setItem(o,k,QTableWidgetItem(str(i)))
            self.table1.setItem(o,k,QTableWidgetItem(str(i)))
            j=j+1
            t=t+1
        self.table1.resizeColumnsToContents()
        print(mem.data)

        

    def settable3(self):
        self.table1.setShowGrid(True)
        self.table1.clearContents()
        self.table1.setItem(0,0,QTableWidgetItem("Address"))
        self.table1.setItem(0,1,QTableWidgetItem("+0"))
        self.table1.setItem(0,2,QTableWidgetItem("+1"))
        self.table1.setItem(0,3,QTableWidgetItem("+2"))
        self.table1.setItem(0,4,QTableWidgetItem("+3"))
        i=268468200
        j=1
        while(i<268469200):
            self.table1.setItem(j,0,QTableWidgetItem(hex(i)))
            self.table1.setItem(j,1,QTableWidgetItem("00"))
            self.table1.setItem(j,2,QTableWidgetItem("00"))
            self.table1.setItem(j,3,QTableWidgetItem("00"))
            self.table1.setItem(j,4,QTableWidgetItem("00"))
            j=j+1
            i=i+4
        self.table1.resizeColumnsToContents()
    def settable4(self):
        self.table1.setShowGrid(True)
        self.table1.clearContents()
        self.table1.setItem(0,0,QTableWidgetItem("Address"))
        self.table1.setItem(0,1,QTableWidgetItem("+0"))
        self.table1.setItem(0,2,QTableWidgetItem("+1"))
        self.table1.setItem(0,3,QTableWidgetItem("+2"))
        self.table1.setItem(0,4,QTableWidgetItem("+3"))
        j=1
        t=0
        #for i in mem.stack:
        #    #print (i[0])
        #    self.table1.setItem(j,0,QTableWidgetItem(hex(t)))
        #    self.table1.setItem(j,1,QTableWidgetItem(i[8]+i[9]))
        #    self.table1.setItem(j,2,QTableWidgetItem(i[6]+i[7]))
        #    self.table1.setItem(j,3,QTableWidgetItem(i[4]+i[5]))
        #    self.table1.setItem(j,4,QTableWidgetItem(i[2]+i[3]))
        #    j=j+1
        #    t=t+4
        self.table1.resizeColumnsToContents()
        #print(mem.stack)


    def setdefault(self):
        self.table1.setShowGrid(False)
        #self.table1.setStyleSheet('QTableView::item {border-right: 0px solid #d6d9dc;}')
        self.table1.horizontalHeader().setVisible(False)
        self.table1.verticalHeader().setVisible(False)
        self.table1.clearContents()
        self.table1.setItem(0,4,QTableWidgetItem("MEMORY SEGMENT"))
        self.table1.resizeColumnsToContents()



    

app = QApplication(sys.argv)

window = TabWidget()
#window.show()

sys.exit(app.exec_())