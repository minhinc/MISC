#include <QAction>
#include <QMenuBar>
#include <QMenu>
#include <QToolBar>
#include <QGraphicsView>
#include "mainwindown.h"
#include "scenen.h"
#include "debug.h"
mainwindown::mainwindown(scenen* s):scenei(s){
trace("mainwindown::mainwindown"<<scenei);
imagefilei=newaction("&Image File","Ctrl+I",":images/image.png");
annotationfilei=newaction("&Annotation File","Ctrl+A",":images/annotation.png");
savei=newaction("&Save Fie","Ctrl+S",":images/save.png");
saveasi=newaction("&Save File","Ctrl+v",":images/saveas.png");
restorei=newaction("&Restore","Ctrl+R",":images/restore.png");
cuti=newaction("&Cut","Ctrl+C",":images/cut.png");
pastei=newaction("&Paste","Ctrl+p",":images/paste.png");
copyi=newaction("C&opy","Ctrl+o",":images/copy.png");
colori=newaction("Co&lor","Ctrl+l",":images/color.png");
widthi=newaction("&Width","Ctrl+w",":images/width.png");
layeri=newaction("&Layer","Ctrl+l",":images/layer.png");
zoomi=newaction("&Zoom","Ctrl+z",":images/zoom.png");
layersi=newaction("&Layers","Ctrl+l",":images/layers.png");
abouti=newaction("&About","Ctrl+a",":images/about.png");
licensingi=newaction("&Licensing","Ctrl+l",":images/licensing.png");
quiti=newaction("&Quit","Ctrl+q",":images/quit.png");
addlinei=newaction("&Line","Ctrl+l",":images/line.png");
addellipsei=newaction("&ellipse","Ctrl+e",":images/ellipse.png");
addrectanglei=newaction("&Rectangle","Ctrl+r",":images/rectangle.png");
addfreehandi=newaction("&FreeHand","Ctrl+f",":images/freehand.png");
addtexti=newaction("&Text","Ctrl+t",":images/text.png");
(menufilei=menuBar()->addMenu(tr("&File")))->addAction(imagefilei);
menufilei->addAction(annotationfilei);
menufilei->addAction(savei);
menufilei->addAction(saveasi);
menufilei->addSeparator();
menufilei->addAction(restorei);
menufilei->addSeparator();
menufilei->addAction(quiti);
(menuediti=menuBar()->addMenu(tr("&Edit")))->addAction(cuti);
menuediti->addAction(copyi);
menuediti->addAction(pastei);
menuediti->addSeparator();
menuediti->addAction(colori);
menuediti->addAction(widthi);
menuediti->addAction(layeri);
(menutooli=menuBar()->addMenu(tr("&Tool")))->addAction(zoomi);
menutooli->addAction(zoomi);
menutooli->addAction(layersi);
(menuhelpi=menuBar()->addMenu(tr("&Help")))->addAction(abouti);
menuhelpi->addAction(licensingi);
toolbari=addToolBar(tr("Edit"));
toolbari->addAction(addlinei);
toolbari->addSeparator();
toolbari->addAction(addellipsei);
toolbari->addSeparator();
toolbari->addAction(addrectanglei);
toolbari->addSeparator();
toolbari->addAction(addfreehandi);
toolbari->addSeparator();
toolbari->addAction(addtexti);
}
QAction* mainwindown::newaction(const char* actionname,const char* shortcut,const QString& imagefile){
trace("mainwindown::newaction"<<actionname<<" "<<shortcut<<" "<<imagefile)
QAction *ta=new QAction(tr(actionname),this);
ta->setShortcut(tr(shortcut));
ta->setIcon(QIcon(imagefile));
connect(ta,SIGNAL(triggered()),scenei,SLOT(slotaction()));
trace("~mainwindow::mainwindow")
return ta;
}
mainwindown::~mainwindown(){
trace("mainwindow::~mainwindow")
trace("~mainwindow::~mainwindow")
}
