import QtQuick
import QtQuick.Controls
import Qt.labs.platform as Qtlabs
CustomMenu {
id:custommenuid
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
    dismiss()
    }
   }
   CustomMenuItem {
   text:qsTr("Replace All..")
    onTriggered: {
    filedialogid.mode="replace"
    filedialogid.fileMode=Qtlabs.FileDialog.OpenFiles
    filedialogid.folder=(filedialogid.lastfolder==undefined?filedialogid.folder:filedialogid.lastfolder)
    filedialogid.open()
    }
   }
   CustomMenuItem {
   text:qsTr("Delete Item..")
    onTriggered: {
     splitviewid.itemAt(splitviewid.currentIndex).files.splice(splitviewid.itemAt(splitviewid.currentIndex).fileindex,1)
     if (splitviewid.itemAt(splitviewid.currentIndex).files.length==splitviewid.itemAt(splitviewid.currentIndex).fileindex)
      splitviewid.itemAt(splitviewid.currentIndex).fileindex-=1
     else {
      splitviewid.itemAt(splitviewid.currentIndex).fileindex+=1
      splitviewid.itemAt(splitviewid.currentIndex).fileindex-=1
     }
     splitviewid.itemAt(splitviewid.currentIndex).forceActiveFocus()
     dismiss()
    }
   }
   CustomMenuItem {
   text:qsTr("Insert(Pre)..")
    onTriggered: {
     filedialogid.mode="insert"
     filedialogid.fileMode=Qtlabs.FileDialog.OpenFiles
     filedialogid.folder=(filedialogid.lastfolder=undefined?filedialigid.folder:filedialogid.lastfolder)
     filedialogid.open()
    }
    customsubmenu: CustomMenu {
     CustomMenuItem {
     text:qsTr("Post..")
      onTriggered: {
      filedialogid.mode="insertpost"
      filedialogid.fileMode=Qtlabs.FileDialog.OpenFiles
      filedialogid.folder=(filedialogid.lastfolder=undefined?filedialigid.folder:filedialogid.lastfolder)
      filedialogid.open()
      }
     }
    }
   }
   CustomMenuItem {
   text:qsTr("Replace Item(Pre)..")
    onTriggered: {
     filedialogid.mode="replaceitem"
     filedialogid.fileMode=Qtlabs.FileDialog.OpenFiles
     filedialogid.folder=(filedialogid.lastfolder=undefined?filedialogid.folder:filedialogid.lastfolder)
     filedialogid.open()
     dismiss()
    }
   }
  }
 }
 CustomMenuItem {
 text:qsTr("Split...")
  onTriggered: {
   for (var i=0;i<splitviewid.count;i++) //{
    splitviewid.itemAt(i).SplitView.preferredWidth=itemid.width/splitviewid.count;
//   }
  }
  customsubmenu: CustomMenu {
   CustomMenuItem {
   text:qsTr("Clear...")
    onTriggered: {
    let cellwidth=itemid.width/splitviewid.count
     if (splitviewid.count>2)
      if (splitviewid.currentIndex!=0)
      cellwidth=(itemid.width-(itemid.width*5)/6)/(splitviewid.count-3)
      else
      cellwidth=(itemid.width-(itemid.width*2)/3)/(splitviewid.count-2)
     for (var i=0;i<splitviewid.count;i++) {
     splitviewid.itemAt(i).SplitView.preferredWidth=cellwidth
      if (splitviewid.count>2)
       if (i==splitviewid.currentIndex)
       splitviewid.itemAt(i).SplitView.preferredWidth=itemid.width/2
       else if (i==splitviewid.currentIndex-1 || i==splitviewid.currentIndex+1)
       splitviewid.itemAt(i).SplitView.preferredWidth=itemid.width/6
     }
    }
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
  }
 }
 MenuItem {
 text:qsTr("FullScreen...")
  onTriggered: {
   if (itemid.visibility == Window.FullScreen)
   itemid.showNormal()
   else
   itemid.showFullScreen()
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
