#ifndef FREEHANDN_H
#define FREEHANDN_H
#include <QGraphicsPathItem>
#include "itemn.h"
struct freehandn:QGraphicsPathItem,itemn{
freehandn(QGraphicsPathItem *p=0);
~freehandn();
};
#endif
