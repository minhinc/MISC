filter={
   'blend':{'blend':"blend=all_expr='A*(1-min(T/1,1))+B*(min(T/1,1))':eof_action=pass",
     'up': "blend=all_expr='if(lte(Y,(H-T/1*H)),A,B)':eof_action=pass", #Curtain up \
     'right':"blend=all_expr='if(gte(X,(T/1*W)),A,B)':eof_action=pass", #Curtain right \
     'down':"blend=all_expr='if(gte(Y,(T/1*H)),A,B)':eof_action=pass", #curtain down \
     'left':"blend=all_expr='if(lte(X,(W-T/1*W)),A,B)':eof_action=pass", #curtain left \
     'verticalopen':"blend=all_expr='if(between(X,(W/2-T/1*W/2),(W/2+T/1*W/2)),B,A)':eof_action=pass",
     'horizontalopen':"blend=all_expr='if(between(Y,(H/2-T/1*H/2),(H/2+T/1*H/2)),B,A)':eof_action=pass",
     'verticalclose':"",
     'horizontalclose':"",
     'circleopen':"blend=all_expr='if(gte(sqrt((X-W/2)*(X-W/2)+(H/2-Y)*(H/2-Y)),(T/1*max(W,H))),A,B)':eof_action=pass",
     'circleclose':"blend=all_expr='if(lte(sqrt((X-W/2)*(X-W/2)+(H/2-Y)*(H/2-Y)),(max(W,H)-(T/1*max(W,H)))),A,B)':eof_action=pass",
     'expandingwindow':"blend=all_expr='if(between(X,(W/2-T/1*W/2),(W/2+T/1*W/2))*between(Y,(H/2-T/1*H/2),(H/2+T/1*H/2)),B,A)':eof_action=pass",
     'circleopen_3s':"blend=all_expr='if(gte(sqrt((X-W/2)*(X-W/2)+(H/2-Y)*(H/2-Y)),(T/3*max(W,H))),A,B)':eof_action=pass",
     'fadein': "fade=in:st=0:d=3:alpha=1",
     'fadeinout': "fade=in:st=0:d=1:alpha=1,fade=out:st=0:d=1:alpha=1",
   },
   'overlay':{ 'normal':"overlay=x='(W-w)/2':y='(H-h)/2':eof_action=pass",
     'up' :"overlay=x='(W-w)/2':y='max((H-h)/2,H-t/1*((H+h)/2))':eof_action=pass",
     'right' : "overlay=x='min((W-w)/2,-w+t/1*W)':y='(H-h)/2':eof_action=pass",
     'bottom': "overlay=x='(W-w)/2':y='min((H-h)/2,-h+t/1*H)':eof_action=pass",
     'left' : "overlay=x='max((W-w)/2,W-t/1*W)':y='(H-h)/2':eof_action=pass",
     'up_4s' :"overlay=x='(W-w)/2':y='max((H-h)/2,H-t/4*((H+h)/2))':eof_action=pass",
     'up_6s' :"overlay=x='(W-w)/2':y='max((H-h)/2,H-t/6*((H+h)/2))':eof_action=pass",
     'up5t2_5s' :"overlay=x='(W-w)/2':y='max((H-h)/4,(H-h)/2-t/5*((H-h)/4))':eof_action=pass",
     'up_m2u' :"overlay=x='(W-w)/2':y='max(0,(H-h)/2-t/2*((H-h)/2))':eof_action=pass",
   },
   '41':r"crop=w=2*floor(iw/2):h=2*floor(ih/2)",
   '00t':((255,0,0,255),(128,128,128,128),0.25,False,'m',10),
   '00t_50rt':((255,0,0,255),(64,64,64,255),0.25,False,'m',10),
   '00t_50wb':((255,255,255,255),(0,0,0,255),0.25,False,'m',5),
   '01t':((255,255,255,255),(128,0,0,128),0.25,False,'m',10),
   '01_wt':((255,255,255,255),(0,0,0,0),0.15,False,'m',4),
   '01_wt_10':((255,255,255,255),(0,0,0,0),0.10,False,'m',3),
   '01_50wt':((255,255,255,255),(0,0,0,0),0.50,False,'m',10),
   '01_25wt':((255,255,255,255),(0,0,0,0),0.25,False,'m',5),
   '00_5t':((255,0,0,255),(128,128,128,128),0.50,False,'m',10),
   '00_5_2t':((128,0,0,128),(255,255,255,255),0.50,False,'m',10),
   '01_5t':((255,255,255,255),(200,0,0,200),0.50,False,'m',10),
   '02t':((0,85,255,255),(255,255,255,255),0.25,False,'m',5),
   '03t':((255,255,255,255),(0,85,255,255),0.25,False,'m',5),
   '02_5t':((0,85,255,255),(255,255,255,255),0.5,False,'m',5),
   '03_5t':((255,255,255,255),(0,85,255,255),0.5,False,'m',5),
   '04t_l5':((255,255,255,255),(0,0,0,0),0.5,False,'l',7),
   '04t_l25':((255,255,255,255),(0,0,0,0),0.25,False,'l',52),


   '05_yt_15':((205,252,110,255),(0,0,0,0),0.15,False,'m',5),
}
