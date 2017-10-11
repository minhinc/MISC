#include <QColor>
#include <QLineF>
#include <QList>
#include "itemn.h"
#include "debug.h"

itemn::itemn(){//:editbi(false){
trace("itemn::itemn")
colori=new QColor;
widthi=new qint8;
*(qint8*)widthi=8;
layeri=new QString;
posi=new QPointF;
translateorrotate=new qint8;
trace("~itemn::itemn")
}
itemn::~itemn(){
trace("itemn::~itemn")
delete (QColor*)colori;
delete (qint8*)widthi;
delete (QString*)layeri;
delete (QPointF*)posi;
delete (qint8*)translateorrotate;
trace("~itemn::~itemn")
}
