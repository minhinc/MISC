#include "ellipsen.h"
#include "debug.h"
ellipsen::ellipsen(QGraphicsEllipseItem *p):QGraphicsEllipseItem(p){
trace("ellipsen::ellipsen")
setFlags(ItemIsMovable|ItemIsSelectable);
trace("~ellipsen::ellipsen")
}
ellipsen::~ellipsen(){
trace("ellipsen::~ellipsen")
trace("~ellipsen::~ellipsen")
}
