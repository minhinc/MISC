#ifndef NDEBUG_H
#define NDEBUG_H
#include <QDebug>
#ifndef NNODEBUG
#define trace(arg) qDebug()<<arg;
#else
#define trace(arg);
#endif
#define LINE_I 6
#define ELLIPSE_I 4
#define RECT_I 3
#define PATH_I 2
#define TEXT_I 8
#define SCENE_WIDTH 400
#define SCENE_HEIGHT 400
#define CROSS_OFFSET 10
#define ROTATEP1 1
#define ROTATEP2 2
#define TRANSLATE 3
#endif
