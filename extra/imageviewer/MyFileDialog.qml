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
 function createobject(currentindexp,qmlfilep,filesp) {
  var component=Qt.createComponent(qmlfilep)
  if (component.status == Component.Ready) {
   var object=component.createObject(splitviewid)
   object.files=filesp
   object.fileindex=0
   splitviewid.insertItem(currentindexp,object)
  }
 }
 onAccepted: {
// var currentindex=splitviewid.count
 var files=re.sortfile(filedialogid.files)
 let qmlfile='Ding'
 filedialogid.lastfolder=filedialogid.folder
  if (re.search('^image',re.filetype(re.sub('^file://','',files[0],re.I)),re.I))
  qmlfile='MyAnimatedImage.qml'
  else if (re.search('(^text|empty|nofile)',re.filetype(re.sub('^file://','',files[0],re.I)),re.I))
  qmlfile='MyTextEdit.qml'
  if (filedialogid.mode=="replace") {
  let lastwidth=splitviewid.itemAt(splitviewid.currentIndex).width
//  splitviewid.insertItem(splitviewid.currentIndex,Qt.createComponent(qmlfile).createObject(splitviewid,{files:files.concat(),fileindex:0}));
  createobject(splitviewid.currentIndex,qmlfile,files)
  splitviewid.removeItem(splitviewid.takeItem(splitviewid.currentIndex))
  splitviewid.itemAt(splitviewid.currentIndex).SplitView.preferredWidth=lastwidth
  }else if (filedialogid.mode == "new") {
  let freewidth=0
   for (var i=0;i<splitviewid.count;i++)
    if (i!=splitviewid.currentIndex) {
    freewidth+=splitviewid.itemAt(i).width/2
    splitviewid.itemAt(i).SplitView.preferredWidth=splitviewid.itemAt(i).width/2
    }
//  splitviewid.insertItem(splitviewid.currentIndex+1,Qt.createComponent(qmlfile).createObject(splitviewid,{files:files.concat(),fileindex:0}));
   createobject(splitviewid.currentIndex+1,qmlfile,files)
   if (splitviewid.count>1) {
   splitviewid.itemAt(splitviewid.currentIndex).SplitView.preferredWidth=(splitviewid.width-freewidth)/2
   splitviewid.itemAt(splitviewid.currentIndex+1).SplitView.preferredWidth=(splitviewid.width-freewidth)/2
   splitviewid.setCurrentIndex(splitviewid.currentIndex+1)
   }
  }else if (filedialogid.mode=="insert"){
   splitviewid.itemAt(splitviewid.currentIndex).files.splice(splitviewid.itemAt(splitviewid.currentIndex).fileindex,0,...files)
   splitviewid.itemAt(splitviewid.currentIndex).forceActiveFocus()
  }else if (filedialogid.mode=="insertpost"){
   splitviewid.itemAt(splitviewid.currentIndex).files.splice(splitviewid.itemAt(splitviewid.currentIndex).fileindex+1,0,...files)
   splitviewid.itemAt(splitviewid.currentIndex).forceActiveFocus()
  }else if (filedialogid.mode == "replaceitem") {
   splitviewid.itemAt(splitviewid.currentIndex).files.splice(splitviewid.itemAt(splitviewid.currentIndex).fileindex,1,...files)
   splitviewid.itemAt(splitviewid.currentIndex).fileindex+=1
   splitviewid.itemAt(splitviewid.currentIndex).fileindex-=1
//  splitviewid.itemAt(splitviewid.currentIndex).files.splice(splitviewid.itemAt(splitviewid.currentIndex).fileindex,1)
   splitviewid.itemAt(splitviewid.currentIndex).forceActiveFocus()
  }
  for (var i=0;i<splitviewid.count;i++)
  splitviewid.itemAt(i).currentindex=i
 }
}
