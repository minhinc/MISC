#ifndef VIEWN_H
#define VIEWN_H
#include <QGraphicsView>
struct QContextMenuEvent;
struct viewn:QGraphicsView{
viewn(QGraphicsView *p=0);
~viewn();
//paint(QPainter*
protected:
void contextMenuEvent(QContextMenuEvent *e);
private:
Q_OBJECT
};
#endif
