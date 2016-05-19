from PyQt4 import QtCore, QtGui, uic
import sys

try:
    gui, widg = uic.loadUiType("grid.ui")
except:
    from ui_grid import Ui_Grid_Screen
    gui = Ui_Grid_Screen
    widg = QtGui.QWidget

class GridGUI(widg, gui):
    
    def __init__(self, parent=None):
        super(GridGUI, self).__init__(parent)
        self.setupUi(self)

        self.clip=QtGui.QApplication.clipboard()
        
        self.GridTable.itemSelectionChanged.connect(self.CalledItem)
        self.ComDisplay.textEdited.connect(self.setY)
         
        self.GenPosi.clicked.connect(self.Generate)
        self.Close_PB.clicked.connect(self.close)

        self.tpCom="/tp {} {} {}"
        self.y='~'#256
        self.x=0;self.z=0

        self.giveCom = "/give @p minecraft:filled_map 1 0"

        #/give @p filled_map 1 <this number ruins everything> {"data":{"scale":"3","dimension":"0","height":"128","width":"128","xCenter":"577","zCenter":"345"}}
    def Generate(self):
        "generates the positions of maps"
        x=self.xCen_SB.value()
        z=self.zCen_SB.value()
        s=self.scale_SB.value()

        z_shift = x_shift = 128*pow(2,s)
        #map is 128 by 128 (at lowest scale)
        #a map next to this map would have its edge
        #at 128/2 spaces away. the center of that map would then
        #be 128/2 from the edge.
        self.PopulateTable(x, z, x_shift, z_shift)


    def spiral(self, row, col):
        "http://stackoverflow.com/a/1196922"
        x,y = 0,0   
        dx, dy = 0, -1

        for dumb in xrange(row*col):
            if abs(x) == abs(y) and [dx,dy] != [1,0] or x>0 and y == 1-x:  
                dx, dy = -dy, dx            # corner, change direction

            if abs(x)>row/2 or abs(y)>col/2:# non-square
                dx, dy = -dy, dx            # change direction
                x, y = -y+dx, x+dy          # jump

            yield x, y
            x, y = x+dx, y+dy

        #x = row
        #y = col

    def PopulateTable(self,x, y, dx, dy):
        tRows=25
        tCols=25

        self.GridTable.blockSignals(True)
        self.GridTable.clear()
        self.GridTable.setRowCount(tRows-1)
        self.GridTable.setColumnCount(tCols)

        tabposi=[]#table positions
        mapCens=[]#map centers
        for i in self.spiral(tRows, tCols):
            tabposi.append(i)
            newX= x - i[0]*dx# map center
            newY= y + i[1]*dy
            mapCens.append((newY, newX))

        #find top left
        left=max([i[1]for i in tabposi])+1#col
        top=min([i[0]for i in tabposi])#row

        #set grid size
        size=75
        for j in range(tRows):
            self.GridTable.setRowHeight(j,size)  
        for j in range(tCols):
            self.GridTable.setColumnWidth(j,size)

        #fill table
        for j,i in enumerate(tabposi):
            r = i[0]+abs(top)
            c = i[1]-abs(left)

            mapC = mapCens[j]
            
            Z, X=mapC

            block=QtGui.QTableWidgetItem(str(mapC[::-1]))
            block.setToolTip(str(X)+'\n'+str(Z))
            block.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
            block.setTextAlignment(QtCore.Qt.AlignCenter)
            
            self.GridTable.setItem(r, c, block)

            #color help
            if mapC[0]==y:block.setBackgroundColor(QtGui.QColor(230,230,230))
            if mapC[1]==x:block.setBackgroundColor(QtGui.QColor(230,230,230))
            if abs(i[0])==abs(i[1]):
                block.setBackgroundColor(QtGui.QColor(240,240,240))
            if mapC==(y,x):#find center block
                cBlk=block
                cBlk.setBackgroundColor(QtCore.Qt.green)

        #center on center block
        self.GridTable.scrollToItem(cBlk, 3)#3 = center position
        self.GridTable.blockSignals(False)

    def setY(self,text):
        "changes the y value of the tp command"
        sp = str(text).split()
        li = self.tpCom.split()
        
        try: # check if edit matches correct tp command
            if sp[0]==li[0] and len(sp)==len(li):
                if sp[1]==str(self.x) and sp[-1]==str(self.z):
                    self.y=sp[-2]#if it does, set the y value
        except:pass

    def CalledItem(self):
        "places tp code to map center of item into clipboard"

        cell = self.GridTable.selectedItems()[-1]
        x,z=str(cell.toolTip()).split()
        self.x=x;self.z=z

        tp=self.tpCom.format(x,self.y,z)

        self.ComDisplay.setText(tp)
        if self.clipCB.isChecked():
            self.clip.clear()
            self.clip.setText(tp)


def main():
    app = QtGui.QApplication(sys.argv)
    app.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
    w = GridGUI();w.show()
    sys.exit(app.exec_())

if __name__ == '__main__': main()
