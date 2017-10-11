#include <QGraphicsView>
#include <QPen>
#include <QPainter>
#include <QGraphicsSceneMouseEvent>
#include <QList>
#include <QPointF>
#include "scenen.h"
#include "linen.h"
#include "debug.h"
linen::linen(QGraphicsItem *p,void *sp):QGraphicsLineItem(p){
trace("linen::linen")
//setFlags(ItemIsMovable|ItemIsSelectable);
setPen(QPen(Qt::black,*(qint8*)widthi,Qt::SolidLine,Qt::RoundCap));
setLine(0,0,100,20);
setPos((((scenen*)sp)->views().at(0)->mapToScene(0,0)).x()+20,(((scenen*)sp)->views().at(0)->mapToScene(0,0)).y()+20);
trace("scene()*"<<scene())
//setPos(((scenen*)scene())->scenepos(QPoint(0,0)));
trace("~linen::linen")
}
linen::~linen(){
trace("linen::~linen")
trace("~linen::~linen")
}
void linen::mousePressEvent(QGraphicsSceneMouseEvent *e){
trace("><linen::mousePressEvent,pos"<<e->pos()<<"scene:"<<e->scenePos()<<"line"<<line())
*(QPointF*)posi=e->pos();
if(qAbs(line().p1().x()-e->pos().x())<8 && qAbs(line().p1().y()-e->pos().y())<8)
*(qint8*)translateorrotate=ROTATEP1;
else if(qAbs(line().p2().x()-e->pos().x())<8 && qAbs(line().p2().y()-e->pos().y())<8)
*(qint8*)translateorrotate=ROTATEP2;
else
*(qint8*)translateorrotate=TRANSLATE;
}
void linen::mouseMoveEvent(QGraphicsSceneMouseEvent *e){
trace("><linen::mouseMoveEvent,scenePos"<<e->scenePos()<<"pos"<<e->pos()<<"line()"<<line())
//if(e->scenePos().x()<0)beg.setX(0);
//else if(e->scenePos().x()>scene()->sceneRect().width())beg.setX(scene()->sceneRect().width());
//if(e->scenePos().y()<0)beg.setY(0);
//else if(e->scenePos().y()>scene()->sceneRect().height())beg.setY(scene()->sceneRect().height());
if(*(qint8*)translateorrotate==ROTATEP1 & 0<=e->scenePos().x() * e->scenePos().y()*(scene()->width()-e->scenePos().x())*(scene()->height()-e->scenePos().y()) )
setLine(mapFromScene(e->scenePos()).x(),mapFromScene(e->scenePos()).y(),line().p2().x(),line().p2().y());
else if(*(qint8*)translateorrotate==ROTATEP2 & e->scenePos().x()>0 & e->scenePos().x()<scene()->width() & e->scenePos().y()>0 & e->scenePos().y()<scene()->height())
setLine(line().p1().x(),line().p1().y(),mapFromScene(e->scenePos()).x(),mapFromScene(e->scenePos()).y());
else if(*(qint8*)translateorrotate==TRANSLATE & (e->scenePos()-*(QPointF*)posi).x()>0 & (e->scenePos()-*(QPointF*)posi).y()>0 & (e->scenePos()+line().p2()-*(QPointF*)posi).x()<scene()->width() & (e->scenePos()+line().p2()-*(QPointF*)posi).y()<scene()->height())
setPos(e->scenePos()-*(QPointF*)posi);
update();
QGraphicsLineItem::mouseMoveEvent(e);
}
//void linen::hoverMoveEvent(QGraphicsSceneHoverEvent* e){
//trace("><linen::hoverleaveevent")
//setPos(e->scenePos());
//}
void linen::mouseReleaseEvent(QGraphicsSceneMouseEvent* e){
trace("><line::mouseReleaseEvent,scenePos,Pos,line"<<e->scenePos()<<e->pos()<<line()<<"dxdy"<<line().dx()<<line().dy()<<scene())
if(line().p2().x()<line().p1().x()){
setPos(mapToScene(line().p2()));
trace("dx,dy"<<line().dx()<<line().dy())
setLine(0,0,-line().dx(),-line().dy());
}
}
