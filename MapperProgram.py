from PyQt4 import QtCore, QtGui, uic
from threading import Thread
import sys, os, pickle
import grid, nbt
import time

try:
    gui, widg = uic.loadUiType("mcmap.ui")
except:
    from ui_mcmap import Ui_MCMIR_Screen
    gui = Ui_MCMIR_Screen
    widg = QtGui.QWidget

class MappGUI(widg, gui):
    updateTextDisplay= QtCore.pyqtSignal(object)
    updateDisplay=QtCore.pyqtSignal(object)
    unLock=QtCore.pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super(MappGUI, self).__init__(parent)
        self.setupUi(self)

        self.Rend=Renderer()

        #connections
        self.MapTree.currentItemChanged.connect(self.Selector)
        self.LocateFolderButton.clicked.connect(self.FindFolder)
        self.RenTogButton.clicked.connect(self.RenderTogether)
        self.RenPreButton.clicked.connect(self.RenderOne)
        self.RenEacButton.clicked.connect(self.RenderEach)
        self.AlignButton.clicked.connect(self.Aligner)
        self.updateDisplay.connect(self.displayImage)
        self.updateTextDisplay.connect(self.PrinttoCommand)
        self.unLock.connect(self._Lock)
        self._scaleRBs=[self.ScaleAllRB, self.Scale0RB, self.Scale1RB,
                  self.Scale2RB, self.Scale3RB, self.Scale4RB]
        for i in self._scaleRBs:
            i.clicked.connect(self._UpdateScale)
        self._dimRBs=[self.MainDimRB, self.NetherDimRB, self.EndDimRB]
        for i in self._dimRBs:
            i.clicked.connect(self._UpdateDim)
        self._CBopts=[self.BoundBoxCB, self.MapNameCB, self.SpawnpointCB, self.SkipCB]

        #variables
        self._dim={0:"Main",-1:"Nether",1:"End"}#dimension names
        self._scale={i:"1 pixel = {}".format('1 block' if not i else "{0} X {0} blocks".format(pow(2,i))) for i in range(16)}#scale sizes
        self._world=''#currently selected world
        self._map=''#currently selected map
        self._wMaps={}#world:[list of full paths to maps of world]
        self._mapData={}#full path of map:{dict of map data}
        self._RTscale=-1#render together scale selection
        self._RTdim=0#render together dimension selection
        self._save="sett.ings"#external settings file
        self._fold=os.path.join(os.environ['APPDATA'],'.minecraft','saves')#minecraft save folder
        self._oldfolds=[]#previously opened folders
        self.MapInfoLabelLeft.setText('')
        self.MapInfoLabelRight.setText('')
        self.load()#check to see if there's any settings to load

        #self._fold = 'C:\\Program Files (x86)\\Games\\.minecraft'
        
        self.PopulateMapTree(self._fold)
        self._updateFindFolderButton()
        
        
    def PopulateMapTree(self, Location=""):
        "Populates the Tree with maps from Location"
        Tree=self.MapTree
        Tree.clear()
        Tree.setColumnWidth(0,140)
        Tree.setColumnWidth(1,50)

        displayText=''
        sl='\\'
        if '/'in Location:sl='/'
        dis= Location.split(sl)
        if len(dis)>3:
            displayText='...'+sl+sl.join(dis[-2:])
        else:
            displayText=Location

        self.TopTreeLabel.setText(displayText)
        self.TopTreeLabel.setToolTip(Location)

        if Location not in self._oldfolds:
            self._oldfolds.insert(0, Location)

        if os.path.basename(Location)=='.minecraft':
            Location=os.path.join(Location,'saves')

        Tree.blockSignals(True)
        self.TopMiddleLabel.setText('Map Item Renderer')

        #three ways:
        #1. direct folder of the map.dats  (map.dats top level)
        #2. save folder of the world  (world/data/map.dats)
        #3. save folder containing saves (savefold/world_1/data/map.dats)

        try:
            #method 1:
            self._world=os.path.basename(Location)
            m1=self._mapTreeMap(Location)
            
            if m1:
                self._world = os.path.basename(Location)
                Tree.insertTopLevelItems(0,m1)
                self.SpawnpointCB.setEnabled(False)#won't be an option if its just the maps
                self.SpawnpointCB.setChecked(False)
                Tree.blockSignals(False)
                return
            else:pass#print 'not method 1'

            #method 2:
            m2=self._mapTreeWorld(Location)
            if m2:
                self._world = os.path.basename(Location)
                Tree.insertTopLevelItem(0,m2)
                Tree.blockSignals(False)
                return
            else:pass#print 'not method 2'

            #method 3:
            m3=self._mapTreeSave(Location)
            if m3:
                Tree.insertTopLevelItems(0,m3)
                Tree.blockSignals(False)
                return
            else:pass#print 'not method 3'

            #if no maps were found using above methods:
            Tree.setColumnWidth(0,210)
            Tree.setColumnWidth(1,0)
            
            item=QtGui.QTreeWidgetItem()
            item.setTextColor(0,QtCore.Qt.darkRed)
            item.setText(0,'No maps found at given folder')
            item.setToolTip(0,'Given folder is\n'+Location)
            if Location in self._oldfolds: self._oldfolds.remove(Location)
                                        
            Tree.insertTopLevelItem(0,item)
            self.TopMiddleLabel.setText('<span style="color:#8b0000;">No maps found at given folder</span>')
        except:#invalid folder
            Tree.setColumnWidth(0,210)
            Tree.setColumnWidth(1,0)
            
            item=QtGui.QTreeWidgetItem()
            item.setTextColor(0,QtCore.Qt.red)
            item.setText(0,'Not a valid folder')
            item.setToolTip(0,'Not a valid folder')
            self.TopMiddleLabel.setText('<span style="color:#ff0000;">NOT A VALID FOLDER</span>')
            Tree.insertTopLevelItem(0,item)

            if Location in self._oldfolds: self._oldfolds.remove(Location)

        self.unLock.emit(False)
        self._Lock(False)
        Tree.blockSignals(False)

    def _mapTreeMap(self, folder):
        "returns a list of tree widgets of maps where folder contains the map.dats"
        fyles=[]#get and sort map_n.dat files
        for f in os.listdir(folder):
            if not f.endswith(".dat"):continue#pass non .dat files
            if 'map' not in f:continue#not valid map file
            fyles.append(f)
            
        fyles=sorted(fyles,key=lambda x:(len(x),x))
        
        self._wMaps[unicode(self._world)]=[os.path.join(folder,f)for f in fyles]
        
        items=[]#create tree widgets of the map_n.dat files
        for f in fyles:
            mapitem=QtGui.QTreeWidgetItem()
            mapitem.setText(0,f)
            mapitem.setToolTip(0,f)
            fuloc=os.path.join(folder,f)

            data=nbt.load(fuloc)[1]['data']
            
            cols=data['colors']
            blank=0#blank map flag
            if len(cols)==cols.count(chr(0)):
                blank=1
                #print 'its an empty map'
            data['blank']=blank

            
            self._mapData[fuloc]=data

            di=self._dim[data['dimension']]
            if di=='Nether':mapitem.setTextColor(1,QtCore.Qt.darkRed)
            if di=='End':mapitem.setTextColor(1,QtCore.Qt.darkGray)
            mapitem.setText(1,di+' dimension')
            mapitem.setToolTip(1,di+' dimension')
            
            if blank:#blank map
                mapitem.setBackgroundColor(0,QtGui.QColor(198, 176, 139))
                mapitem.setBackgroundColor(1,QtGui.QColor(198, 176, 139))
                mapitem.setToolTip(0,'This map is blank')
                mapitem.setToolTip(1,'This map is blank')
            
            mapitem.setText(2, 'm')#2 is an unseen column, use it for flagging map or world
            mapitem.setToolTip(2, fuloc)#tooltip of col. 2 is full path to item
            
            items.append(mapitem)

        return items

    def _mapTreeWorld(self, folder):
        "returns a tree widget for a world where folder is the world"
        worldName=os.path.basename(folder)
        self._world=folder

        item=QtGui.QTreeWidgetItem()
        item.setText(0,worldName)
        item.setToolTip(0,worldName)
        item.setText(2, 'w')#2 is an unseen column, use it for flagging map or world
        item.setToolTip(2, folder)#tooltip of col. 2 is full path to item
        
        try:maps = self._mapTreeMap(os.path.join(folder,'data'))
        except:return None# if failed, no data folder, so not valid world save

        if not maps:
            item.setText(1,'no maps')
            item.setToolTip(1,'Like, none at all man!')
        else:
            item.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
            item.setTextColor(1,QtCore.Qt.darkGreen)
            n=len(maps)
            item.setText(1,'{} map{}'.format(n,''if n==1 else's'))
            item.setToolTip(1,'{} map{}'.format(n,''if n==1 else's'))
            item.insertChildren(0,maps)

        return item

    def _mapTreeSave(self, folder):
        "returns a list of tree widgets of worlds where folder contains the worlds"
        worlds = []
        for world in os.listdir(folder):
            full= os.path.join(folder, world)
            if os.path.isdir(full):
                self._world = world
                wrld = self._mapTreeWorld(full)
                if wrld:worlds.append(wrld)
        return worlds

    def _Lock(self, lock):
        "lock/unlock buttons while rendering"
        lockables=[self.RenTogGB, self.RenSepGB, self.LocateFolderButton,
                   self.MapTree]#self.OtherGB]
        for i in lockables:
            i.setEnabled(not lock)
            
    def FindFolder(self):
        "Opens a File dialog to locate a folder containing maps"
        new=QtGui.QFileDialog().getExistingDirectory()
        if not new:return#no given location
        self._fold=unicode(new)
        self.PopulateMapTree(self._fold)
        self._updateFindFolderButton()

    def _updateFindFolderButton(self):
        "adds menu to find folder button containing previous folders"
        if not self._oldfolds: return
        if len(self._oldfolds) > 9: self._oldfolds = self._oldfolds[:10]
        if len(self._oldfolds) == 1 and self._fold == self._oldfolds[0]: return

        seen = set();add = seen.add  # http://stackoverflow.com/a/480227
        self._oldfolds=[x for x in self._oldfolds if not(x in seen or add(x))]
        
        menu = QtGui.QMenu(self)
        menu.triggered.connect(self._previousFolder)
        menu.addAction("Open New...")
        menu.addSeparator()
        
        for fld in self._oldfolds: menu.addAction(fld)
        self.LocateFolderButton.setMenu(menu)

    def _previousFolder(self, event):
        "opens previous folder from find folder menu"
        loc = unicode(event.text())
        if loc == "Open New...":
            self.FindFolder()
            return
        
        self._oldfolds.remove(loc)
        self._oldfolds.insert(0, loc)
        self._fold = loc

        self.PopulateMapTree(loc)
        self._updateFindFolderButton()
        

    def _UpdateScale(self):
        "updates render together scale option"
        RB=dict(zip(self._scaleRBs,range(-1,5)))
        self._RTscale=RB.get(self.sender(),-1)

    def _UpdateDim(self):
        "updates render together dimension option"
        RB=dict(zip(self._dimRBs,[0,-1,1]))
        self._RTdim=RB.get(self.sender(),0)
        #print self._dim, dim[self._dim]

    def load(self):
        "loads settings from ._save file"
        try:
            fyle = open(self._save, 'rb')
            dat = pickle.load(fyle)
            self._fold, self._oldfolds = dat
            fyle.close()
        except: pass

    def closeEvent(self, event): self.save()

    def save(self):
        "saves settings to ._save file"
        fyle = open(self._save, 'wb')
        dat = (self._fold, self._oldfolds)
        pickle.dump(dat, fyle)
        fyle.close()

    def Selector(self, item, oldItem):
        "updates preview window and info text on selection change"
        if not item:return

        #columns:
        #if world item, 0 = world name, 1= num maps
        #if map item, 0=map name, 1 = dimension
        
        #2 is an unseen column, use it for flagging map or world
        # m for map, w for world
        # the tool tip for column 2 is the full path to world/map
        if item.text(2)=='m':
            self._map = unicode(item.toolTip(2))
        if item.text(2)=='w':
            self._world = unicode(item.toolTip(2))
            try:self._map=self._wMaps[self._world][0]
            except:return#selected a world that has no maps

        dat=self._mapData[self._map]
        leng=128*pow(2,dat['scale'])
        sql=pow(leng,2)

        sq='{:,} m^2'.format(sql)
        ac='{:,} acres'.format(round(sql*0.0002471053719,4))
        if sql>1e6:sql/=1e6;sq='{:,} km^2'.format(round(sql,4))
            
        sqinfo='Map covers an area of {0} x {0} meters\n({1} or {2})'.format(leng,sq,ac)
        leftInfo="Map center\nX = {}\nZ = {}".format(dat['xCenter'],dat['zCenter'])
        righInfo="Scale = {}\n ({})\n{} dimension".format(dat['scale'],self._scale[dat['scale']],self._dim[dat['dimension']])                                          

        self.MapInfoLabelLeft.setText(leftInfo)
        self.MapInfoLabelLeft.setToolTip(leftInfo)
        self.MapInfoLabelRight.setText(righInfo)
        self.MapInfoLabelRight.setToolTip(righInfo+'\n'+sqinfo)
        
        thrd=Thread(target=self.preview())
        thrd.start()

    def preview(self,save='',unlockFlag=0):
        "generates a single map image"
        sc=2
        nam=os.path.basename(save).replace('.png','').replace(os.path.basename(self._world)+'_','')
        if save:
            self.updateTextDisplay.emit('Rendering {}'.format(nam))
            sc = self.RenSepSB.value()
        try:
            dat=self._mapData[self._map]
            if dat['blank'] and save and self.SkipCB.isChecked():
                self.updateTextDisplay.emit('    '+nam+' is blank, skipping')
                return
            Map=dat['colors']
            cols=[int('{:02x}'.format(ord(z)),16) for z in Map]#convert the color ids
            img=self.Rend.single(cols,dat['height'],dat['width'],sc)
            self.updateDisplay.emit(QtGui.QImage(img.scaled(256,256)))

            if save:#save is the full path name of saved image
                img.save(os.path.basename(save))
                self.updateTextDisplay.emit(os.path.basename(save)+' saved')
        except Exception as err:
            err_name = type(err).__name__
            err_mess = str(err)

            line = 'line {}, '.format(sys.exc_info()[-1].tb_lineno)
            err='<span style="color:#ff0000;">{}: {}</span>'.format(line, err_name,err_mess)
            self.updateTextDisplay.emit(err)
        if unlockFlag:self.unLock.emit(False)

    def displayImage(self,image):
        "adds image to GUI for preview"
##        self.PreviewDisplay.clear()
        img = QtGui.QGraphicsPixmapItem()
        img.setPixmap(QtGui.QPixmap(image))
          
        scene=QtGui.QGraphicsScene()
        scene.addItem(img)

        self.PreviewDisplay.setScene(scene)
        self.PreviewDisplay.centerOn(img)

    def RenderTogether(self):
        "renders all maps of selected world as one"
        self._Lock(True)
        thrd=Thread(target=self._RenTog)
        thrd.start()
    def _RenTog(self):
        try:
            wrld=os.path.basename(self._world)
            st_tm = time.time()
            self.updateTextDisplay.emit("\nStarting to render {}'{} maps".format(wrld,''if wrld[-1]=='s'else's'))
            maps = self._getMapScale(self._getMapDim())
            self.updateTextDisplay.emit("Processing {:,} map{} of {}".format(len(maps),''if len(maps)==1 else's',wrld))
            
            #sort by age, scale (smallest last, newest last)
            sortRule=lambda x:(-self._mapData[x]['scale'],os.path.getmtime(x))
            maps = sorted(maps, key = sortRule)
            #for i in maps:print i, self._mapData[i]['scale'], datetime.fromtimestamp(os.path.getmtime(i))
    
            self.updateTextDisplay.emit("Determining size...")
            tWidth, tHeight, Xcen, Zcen, minSc, maxSc = self._detSize(maps)
            
            self.updateTextDisplay.emit("Image of size {} X {}".format(tWidth,tHeight))
            
            #determine file name
            Name ="{}_{}_Combined_".format(wrld,self._dim[self._RTdim])
            Name+='scale_all'if self._RTscale==-1 else"scale_{}".format(self._RTscale)
            if self.BoundBoxCB.isChecked():Name+="_bounded"
            if self.MapNameCB.isChecked():Name+="_named"
            if self.SpawnpointCB.isChecked():Name+="_spawnPointMarked"
            Name+=".png"
            
            Img=QtGui.QImage(tWidth,tHeight,4)
            Img.fill(QtGui.QColor(198, 176, 139))
            
            sX,sZ=0,0#collect spawnpoint
            if self.SpawnpointCB.isChecked():
                lvl=nbt.load(os.path.join(self._world,'level.dat'))[1]['Data']
                sX,sZ=lvl['SpawnX'], lvl['SpawnZ']
                self.updateTextDisplay.emit('Spawn point: {}, {}'.format(sX,sZ))
            
            for M in maps:#draw the maps
                mapName=os.path.basename(M).replace('.dat','')
                dat=self._mapData[M]
                if dat['blank'] and self.SkipCB.isChecked():
                    self.updateTextDisplay.emit("    Skipping {} (is blank)".format(mapName))
                else:
                    self.updateTextDisplay.emit("Drawing {}".format(mapName))
                    
                numName=mapName.replace('map_','')
                
                #adjust scaling
                Xscld = (dat['xCenter']/pow(2.,dat['scale']) -dat['width']/2.)
                Zscld = (dat['zCenter']/pow(2.,dat['scale']) -dat['height']/2.)
                sXscld= sX/pow(2.,dat['scale'])
                sZscld= sZ/pow(2.,dat['scale'])
                
                tWidth, tHeight, Xcen, Zcen, minSc, maxSc
                scaling = self.RenSepSB.value()
    
                if self._RTscale != -1 or minSc == maxSc:# if just one scale, just move by one scale size
                    Xscld-=Xcen/scaling
                    Zscld-=Zcen/scaling
                    sXscld-=Xcen/scaling
                    sZscld-=Zcen/scaling
                else:# if all scales, coords need to be scale shifted
                    Xscld-=Xcen/pow(2.,dat['scale'])
                    Zscld-=Zcen/pow(2.,dat['scale'])
                    sXscld-=Xcen/pow(2.,dat['scale'])
                    sZscld-=Zcen/pow(2.,dat['scale'])
                
                if self._RTscale== -1 and minSc!=maxSc:
                    scaling = pow(2.,(dat['scale']-minSc))
                    if minSc>=2:scaling=pow(2.,(dat['scale']-2))
                
                #color ids, map center, scale and map's height, width
                cols=dat['colors']
                cols=[int('{:02x}'.format(ord(z)),16) for z in cols]#convert the color ids
                mapInfo = [cols, Xscld, Zscld,
                           scaling, dat['width'], dat['height']]
                
                opts=[self.BoundBoxCB.isChecked(),(self.MapNameCB.isChecked(), numName),
                       (self.SpawnpointCB.isChecked(), sXscld,sZscld)]
                
                #draw the map
                Img = self.Rend.multiple(Img, mapInfo, opts)
                tmp = Img.scaled(256,256)
                self.updateDisplay.emit(tmp)
                
            self.updateTextDisplay.emit("Saving...")
            Img.save(Name)
            en_tm = time.time()
            self.updateTextDisplay.emit("Image saved to {}".format(Name))
            
            self.updateTextDisplay.emit("Processing complete")

        except Exception as err:
            err_name = type(err).__name__
            err_mess = str(err)

            line = 'line {}, '.format(sys.exc_info()[-1].tb_lineno)
            err='<span style="color:#ff0000;">{}: {}</span>'.format(line, err_name,err_mess)
            self.updateTextDisplay.emit(err)
        self.unLock.emit(False)

    def _detSize(self, maps):
        "determines image size needed for render together"
        minSc,maxSc=256,-1
        if self._RTscale==-1:#all scales
            for m in maps:#find smallest necessary scale
                dat=self._mapData[m]
                if self.SkipCB.isChecked() and dat['blank']:
                    continue
                s=dat['scale']
                if s<minSc:minSc=s
                if s>maxSc:maxSc=s
        
        Xmin,Xmax,Zmin,Zmax=2**25,-2**25,2**25,-2**25
        for m in maps:#determine size
            dat=self._mapData[m]
            
            if self.SkipCB.isChecked() and dat['blank']:continue
            H,W=dat['height'],dat['width']
            x, z = dat['xCenter'],dat['zCenter']
            s = dat['scale']
            
            Sp=pow(2.,s)
            top,left=(z/Sp-H/2.),(x/Sp-W/2.)
            bottom,right=top+H,left+W
            
            scaling=self.RenSepSB.value()
            if self._RTscale== -1 and minSc!=maxSc:
                scaling = pow(2.,(s-minSc))
                if minSc>=2:scaling=2.**(s-2)

            top*=scaling
            left*=scaling
            bottom*=scaling
            right*=scaling

            if left<Xmin:Xmin=left
            if right>Xmax:Xmax=right
            if top<Zmin:Zmin=top
            if bottom>Zmax:Zmax=bottom

        Xcen=(Xmin+Xmax)/2.
        Zcen=(Zmin+Zmax)/2.

        X,Z=int(abs(Xmax-Xmin)),int(abs(Zmax-Zmin))
        return X,Z,Xcen,Zcen,minSc,maxSc
            
    def _getMapDim(self):
        "returns a list of maps of dimension ._RTdim of ._world"
        maps = self._wMaps[self._world]
        subset=[]
        for i in maps:
            if self._mapData[i]['dimension']==self._RTdim:
                subset.append(i)
        return subset
    
    def _getMapScale(self, maps):
        "returns a subset from maps list of maps whose scale matches ._RTscale"
        if self._RTscale==-1:return maps#all scales
        subset=[]
        for i in maps:
            if self._mapData[i]['scale']==self._RTscale:
                subset.append(i)
        return subset

    def RenderOne(self):
        "renders one map of selected world"
        if not self._map:return
        self._Lock(True)
        name = self._world+'_'+os.path.basename(self._map)+'.png'
        name=name.replace('.dat','')
        thrd=Thread(target=self.preview(name,1))
        thrd.start()

    def RenderEach(self):
        "renders every map of selected world separately"
        self._Lock(True)
        thrd=Thread(target=self._RenEach)
        thrd.start()
    def _RenEach(self):
        wrld=os.path.basename(unicode(self._world))
        allmaps=self._wMaps[self._world]
        self.updateTextDisplay.emit("\nProcessing {:,} map{} of {}".format(len(allmaps),''if len(allmaps)==1 else's',wrld))
        for i in allmaps:
            name = self._world+'_'+os.path.basename(i)+'.png'
            name=name.replace('.dat','')
            self._map=i
            self.preview(name)
        self.updateTextDisplay.emit("Complete")
        self.unLock.emit(False)

    def Aligner(self):
        "launches map aligement tool"
        self._gridTool=grid.GridGUI()
        self._gridTool.show()

    def PrinttoCommand(self, text):
        "add text to text display"    
        self.Prompt_Text.append(text)


class Renderer(QtGui.QPixmap):
    def __init__(self, parent = None):
        QtGui.QPixmap.__init__(self)
        self.ColorID=self.genCols()

    def single(self,Data,h,w,scale):
        
        Image=QtGui.QImage(w*scale,h*scale,4)#4 = 32 bit rgb format, see ref.
        Image.fill(QtGui.QColor(198, 176, 139))
        
        p=QtGui.QPainter(Image)
        p.scale(scale,scale)
        y=0
        for c,Id in enumerate(Data):
            col=QtGui.QColor()
            r,g,b=self.ColorID[Id];col.setRgb(r,g,b)
            p.setPen(QtGui.QPen(col,1))
            x=c%w
            if not x and c:y+=1

            if Id<4:continue# unexplored sections, don't draw
            if y>h:break
            p.drawPoint(x,y)

        return Image
    
    def multiple(self, Img, mapInfo, Opts):
        IDs,mX,mZ,Sc,mW,mH=mapInfo#color ids, map center, scale and map's height, width
        drawRect, drawName, drawSpawn = Opts
 
        p=QtGui.QPainter(Img)
        p.translate(Img.size().width()/2,Img.size().height()/2)
        p.scale(Sc,Sc)
        
        j,k=0,0
        x,z=(j+mX),(k+mZ)
        xX,zZ=(j+mX),(k+mZ)

        for i in IDs:
            col=QtGui.QColor()
            r,g,b=self.ColorID[i];col.setRgb(r,g,b)
            p.setPen(QtGui.QPen(col,1))
            
            x,z=(j+mX),(k+mZ)
            
            j+=1
            if j>mW-1:k+=1;j=0
            if i<4:continue# unexplored sections, don't draw
            if k>mH:break
            p.drawPoint(x,z)
        
        Co=QtGui.QColor(255, 165, 0)
        p.setPen(QtGui.QPen(Co,0))
        if drawRect:# draw bounding box    
            p.drawRect(xX,zZ,abs(x-xX),abs(z-zZ))
        if drawName[0]:#draw name
            p.drawText(xX+2,zZ+12,str(drawName[1]))
        if drawSpawn[0]:#mark spawnpoint
            Co=QtGui.QColor(252, 255, 17)
            p.setPen(QtGui.QPen(Co,1))
            sX,sZ=drawSpawn[1],drawSpawn[2]
            p.drawPoint(sX,sZ)
            p.drawEllipse(sX-5.,sZ-5.,10,10)
            #for q in range(20,51,40):
            #    p.drawEllipse(sX-q/2.,sZ-q/2.,q,q)
        return Img

    def genCols(self):
        "generates all color ids"

        BaseColors=[# see http://minecraft.gamepedia.com/Map_item_format#Color_table
        (  0,   0,   0), (127, 178,  56), (247, 233, 163), (167, 167, 167),
        (255,   0,   0), (160, 160, 255), (167, 167, 167), (  0, 124,   0),
        (255, 255, 255), (164, 168, 184), (183, 106,  47), (112, 112, 112),
        ( 64,  64, 255), (104,  83,  50), (255, 252, 245), (216, 127,  51),
        (178,  76, 216), (102, 153, 216), (229, 229,  51), (127, 204,  25),
        (242, 127, 165), ( 76,  76,  76), (153, 153, 153), ( 76, 127, 153),
        (127,  63, 178), ( 51,  76, 178), (102,  76,  51), (102, 127,  51),
        (153,  51,  51), ( 25,  25,  25), (250, 238,  77), ( 92, 219, 213),
        ( 74, 128, 255), (  0, 217,  58), ( 21,  20,  31), (112,   2,   0),
        (126,  84,  48),
        ]

        MapColors = []
        scaleFactors = [180, 220, 255, 135]  # used to make color variants

        for bC in BaseColors:
            variants=[]
            
            for s in scaleFactors:
                newCol=tuple(int(k*s/255.)for k in bC)
                variants.append(newCol)
            
            MapColors.extend(variants)
        return MapColors


def main():
    app = QtGui.QApplication(sys.argv)
    app.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
    w = MappGUI();w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':main()
