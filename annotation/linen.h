#ifndef LINEN_H
#define LINEN_H
#include <QGraphicsLineItem>
#include <QColor>
#include "itemn.h"
struct QGraphicsSceneMouseEvent;
struct QGraphicsSceneHoverEvent;
struct linen:QGraphicsLineItem,itemn{
linen(QGraphicsItem *p=0,void *sp=0);
~linen();
protected:
//void paint(QPainter*,const QStyleOptionGraphicsItem*,QWidget* w=0);
void mousePressEvent(QGraphicsSceneMouseEvent*);
void mouseMoveEvent(QGraphicsSceneMouseEvent*);
void mouseReleaseEvent(QGraphicsSceneMouseEvent*);
//void hoverMoveEvent(QGraphicsSceneHoverEvent*);
};
#endif
