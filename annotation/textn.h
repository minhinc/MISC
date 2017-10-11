#ifndef TEXTN_H
#define TEXTN_H
#include <QGraphicsTextItem>
#include "itemn.h"
struct textn:QGraphicsTextItem,itemn{
textn(QGraphicsTextItem *p=0);
~textn();
};
#endif
