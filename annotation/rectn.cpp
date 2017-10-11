#include <QPainter>
#include <QGraphicsSceneMouseEvent>
#include <QPen>
#include "rectn.h"
#include "debug.h"
rectn::rectn(QGraphicsRectItem *p):QGraphicsRectItem(p){
trace("rectn::rectn")
//setFlags(ItemIsMovable|ItemIsSelectable);
colori=Qt::black;
widthi=15;
trace("~rectn::rectn")
}
rectn::~rectn(){
trace("rectn::~rectn")
trace("~rectn::~rectn")
}
//void rectn::mousePressEvent(QGraphicsSceneMouseEvent *e){
//trace("><rectn::mousePressEven,pos"<<e->pos())
//QGraphicsRectItem::mousePressEvent(e);
//}
//void rectn::mouseMoveEvent(QGraphicsSceneMouseEvent *e){
//trace("><rectn::mouseMoveEvent,pos"<<e->pos())
//QGraphicsRectItem::mouseMoveEvent(e);
//}
void rectn::paint(QPainter *painter,QStyleOptionGraphicsItem *option,QWidget *widget){
trace("><rectn::paint")
painter->setPen(QPen(Qt::red,25));
painter->drawRect(10,10,100,100);
QGraphicsRectItem::paint(painter,option,widget);
}
