#include <QContextMenuEvent>
#include "viewn.h"
#include "debug.h"
viewn::viewn(QGraphicsView *p):QGraphicsView(p){
trace("viewn::viewn")
trace("~viewn::viewn")
}
void viewn::contextMenuEvent(QContextMenuEvent *e){
trace("viewn::contextMenuEvent"<<e->pos()<<" "<<e->globalPos()<<" "<<e->x()<<" "<<e->y())
trace("~viewn::contextMenuEvent")
}
viewn::~viewn(){
trace("viewn::~viewn")
trace("~viewn::~viewn")
}
