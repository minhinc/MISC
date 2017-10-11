#ifndef MAINWINDOWN_H
#define MAINWINDOWN_H
#include <QMainWindow>
#include <QString>
struct QAction;
struct QMenu;
struct QToolBar;
struct scenen;
struct mainwindown:QMainWindow{
mainwindown(scenen *s=0);
~mainwindown();
QMenu *menufilei;
QMenu *menuediti;
QMenu *menutooli;
QMenu *menuhelpi;
QToolBar *toolbari;
QAction *imagefilei;
QAction *annotationfilei;
QAction *savei;
QAction *saveasi;
QAction *restorei;
QAction *cuti;
QAction *copyi;
QAction *pastei;
QAction *colori;
QAction *widthi;
QAction *layeri;
QAction *layersi;
QAction *zoomi;
QAction *abouti;
QAction *licensingi;
QAction *quiti;
QAction *addlinei;
QAction *addellipsei;
QAction *addrectanglei;
QAction *addfreehandi;
QAction *addtexti;
scenen *scenei;
QAction* newaction(const char*,const char*,const QString&);
private:
Q_OBJECT
};
#endif
