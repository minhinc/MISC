#include "textn.h"
#include "debug.h"
textn::textn(QGraphicsTextItem *p):QGraphicsTextItem(p){
trace("textn::textn")
setFlags(ItemIsMovable|ItemIsSelectable);
trace("~textn::textn")
}
textn::~textn(){
trace("textn::~textn")
trace("~textn::~textn")
}
