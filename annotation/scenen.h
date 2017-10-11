#ifndef SCENEN_H
#define SCENEN_H
#include <QGraphicsScene>
#include <QPointF>
#include <QPixmap>
#include <QList>
struct QGraphicsLineItem;
struct QGraphicsView;
struct QGraphicsSceneMouseEvent;
struct mainwindown;
struct QPainter;
struct QGraphicsItem;

struct scenen:QGraphicsScene{
scenen(QObject *p=0);
~scenen();
QGraphicsView *viewi;
void *imagei;
mainwindown *mwi;
QList<QGraphicsItem*> itemli;
QPixmap pm;
void *initiali;
QPointF scenepos(const QPoint&);
protected:
void drawBackground(QPainter *p,const QRectF&);
//void mouseMoveEvent(QGraphicsSceneMouseEvent *e);
//void mousePressEvent(QGraphicsSceneMouseEvent *e);
public slots:
void slotaction();
private:
Q_OBJECT
};
#endif
