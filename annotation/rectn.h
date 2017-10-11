#ifndef RECTN_H
#define RECTN_H
#include <QGraphicsRectItem>
#include "itemn.h"
struct QGraphicsSceneMouseEvent;
struct QPainter;
struct QStyleOptionGraphicsItem;
struct QWidget;
struct rectn:QGraphicsRectItem,itemn{
rectn(QGraphicsRectItem *p=0);
~rectn();
Qt::GlobalColor colori;
int widthi;
void paint(QPainter*,QStyleOptionGraphicsItem*,QWidget* widget=0);
protected:
//void mousePressEvent(QGraphicsSceneMouseEvent*);
//void mouseMoveEvent(QGraphicsSceneMouseEvent*);
};
#endif
