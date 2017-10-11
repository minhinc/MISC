#include "freehandn.h"
#include "debug.h"
freehandn::freehandn(QGraphicsPathItem *p):QGraphicsPathItem(p){
trace("freehandn::freehandn")
setFlags(ItemIsMovable|ItemIsSelectable);
trace("~freehandn::freehandn")
}
freehandn::~freehandn(){
trace("freehandn::~freehandn")
trace("~freehandn::~freehandn")
}
