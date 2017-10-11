#include <QGraphicsView>
#include <QGraphicsSceneMouseEvent>
#include <QImage>
#include <QPainter>
#include <QFileDialog>
#include "mainwindown.h"
#include "scenen.h"
#include "linen.h"
#include "debug.h"
scenen::scenen(QObject *p):QGraphicsScene(p),imagei(0),initiali(0){
trace("scenen::scenen")
int i=0;
mwi=new mainwindown(this);
viewi=new QGraphicsView(this);
for(i=0;i<views().size();i++)views().at(i)->setRenderHint(QPainter::Antialiasing,true);
mwi->setCentralWidget(viewi);
setSceneRect(0,0,SCENE_WIDTH,SCENE_HEIGHT);
mwi->show();
trace("~scenen::scenen")
}
scenen::~scenen(){
int i=0;
trace("scenen::~scenen")
delete (QString*)imagei;
for(i=0;i<itemli.size();i++) delete itemli[i];
trace("~scenen:~scenen")
}
void scenen::slotaction(){
int i=0;
trace("scenen::slotaction"<<this)
if((QAction*)sender()==mwi->addlinei){
addItem(new linen(0,this));
trace("x,y"<<views().at(0)->mapToScene(0,0))
scenepos(QPoint(0,0));
}else if((QAction*)sender()==mwi->imagefilei){
if(!imagei)
imagei=new QString;
*(QString*)imagei=QFileDialog::getOpenFileName(NULL,tr("Open Image"),"/",tr("Image Files (*.png *.jpg *.bmp,*.gif)"));
pm.load(*(QString*)imagei);
setSceneRect(QImage(*(QString*)imagei).rect());
views().at(0)->activateWindow();
}
trace("~scenen::slotaction")
}
void scenen::drawBackground(QPainter *painter, const QRectF& rect){
if(imagei)
painter->drawPixmap(0,0,pm);
QGraphicsScene::drawBackground(painter,rect);
}
QPointF scenen::scenepos(const QPoint& p){
trace("><scenen::scenepos"<<this)
QPointF r(0,0);
//r=views().at(0)->mapToScene(0,0);
trace("<>scene::scenepos"<<views().at(0)->mapToScene(0,0))
return r;
}
