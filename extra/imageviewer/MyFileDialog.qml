import QtQuick
import QtQuick.Controls
import Qt.labs.platform
FileDialog {
property var mode:undefined
property string newfilename:''
property var lastfolder:undefined
 onFolderChanged: {
// console.log('folder changed folder,currentFile,newfilename',folder,currentFile,newfilename)
  if (fileMode == FileDialog.SaveFile && (newfilename =='' || currentFile != newfilename)) {
  newfilename='file://'+re.newfilename(re.sub('^file://','',folder,re.I))
  currentFile=newfilename
  }
 }
 onAccepted: {
// var currentindex=splitviewid.count
 var files=filedialogid.files
 let qmlfile='Ding'
 filedialogid.lastfolder=filedialogid.folder
  if (re.search('^image',re.filetype(re.sub('^file://','',files[0],re.I)),re.I))
  qmlfile='MyAnimatedImage.qml'
  else if (re.search('(^text|empty|nofile)',re.filetype(re.sub('^file://','',files[0],re.I)),re.I))
  qmlfile='MyTextEdit.qml'
  if (filedialogid.mode=="replace") {
  let lastwidth=splitviewid.itemAt(splitviewid.currentIndex).width
  splitviewid.insertItem(splitviewid.currentIndex,Qt.createComponent(qmlfile).createObject(splitviewid,{files:files.concat(),fileindex:0}));
  splitviewid.removeItem(splitviewid.takeItem(splitviewid.currentIndex))
  splitviewid.itemAt(splitviewid.currentIndex).SplitView.preferredWidth=lastwidth
  }else if (filedialogid.mode == "new") {
  let freewidth=0
   for (var i=0;i<splitviewid.count;i++)
    if (i!=splitviewid.currentIndex) {
    freewidth+=splitviewid.itemAt(i).width/2
    splitviewid.itemAt(i).SplitView.preferredWidth=splitviewid.itemAt(i).width/2
    }
  splitviewid.insertItem(splitviewid.currentIndex+1,Qt.createComponent(qmlfile).createObject(splitviewid,{files:files.concat(),fileindex:0}));
   if (splitviewid.count>1) {
   splitviewid.itemAt(splitviewid.currentIndex).SplitView.preferredWidth=(splitviewid.width-freewidth)/2
   splitviewid.itemAt(splitviewid.currentIndex+1).SplitView.preferredWidth=(splitviewid.width-freewidth)/2
   splitviewid.setCurrentIndex(splitviewid.currentIndex+1)
   }
  }
  for (var i=0;i<splitviewid.count;i++)
  splitviewid.itemAt(i).currentindex=i
 }
}
