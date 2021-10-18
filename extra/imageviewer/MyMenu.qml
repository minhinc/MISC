import QtQuick
import QtQuick.Controls
import Qt.labs.platform as Qtlabs
CustomMenu {
 CustomMenuItem {
 text:qsTr("New...")
  onTriggered: {
  filedialogid.mode="new"
  filedialogid.fileMode=Qtlabs.FileDialog.OpenFiles
  filedialogid.folder=(filedialogid.lastfolder==undefined?filedialogid.folder:filedialogid.lastfolder)
  filedialogid.open()
  }
  customsubmenu: CustomMenu {
   CustomMenuItem {
   text:qsTr("Open..")
    onTriggered: {
    filedialogid.fileMode=Qtlabs.FileDialog.SaveFile
    filedialogid.newfilename=''
    filedialogid.mode="new"
    filedialogid.acceptLabel="Open"
    filedialogid.open()
    }
   }
   CustomMenuItem {
   text:qsTr("Replace..")
    onTriggered: {
    filedialogid.mode="replace"
    filedialogid.fileMode=Qtlabs.FileDialog.OpenFiles
    filedialogid.folder=(filedialogid.lastfolder==undefined?filedialogid.folder:filedialogid.lastfolder)
    filedialogid.open()
    }
   }
  }
 }
 CustomMenuItem {
 text:qsTr("Split...")
  onTriggered: {
   for (var i=0;i<splitviewid.count;i++) {
    splitviewid.itemAt(i).SplitView.preferredWidth=itemid.width/splitviewid.count;
   }
  }
 }
 CustomMenuItem {
 text:qsTr("Refresh...")
  onTriggered: {
   let index=splitviewid.itemAt(splitviewid.currentIndex).fileindex
   splitviewid.itemAt(splitviewid.currentIndex).fileindex=-1
   splitviewid.itemAt(splitviewid.currentIndex).fileindex=index
  }
  customsubmenu:CustomMenu {
   CustomMenuItem {
   text:qsTr("Delete..")
    onTriggered: { 
    splitviewid.removeItem(splitviewid.takeItem(splitviewid.currentIndex))
     for (var i=0;i<splitviewid.count;i++)
     splitviewid.itemAt(i).currentindex=i
    }
   }
   CustomMenuItem {
   text:qsTr("FullScreen...")
    onTriggered: {
    if (itemid.visibility == Window.FullScreen)
    itemid.showNormal()
    else
    itemid.showFullScreen()
    }
   }
  }
 }
 Component {
  id:menuitemid
  CustomMenuItem {
  }
 }
 function addEntry(title) {
  addItem(menuitemid.createObject(this, { text: title }))
 }
}
