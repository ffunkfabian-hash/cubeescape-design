import math
def circlep(x,y,r,n=10):return [(x+r*math.cos(2*math.pi*k/n),y+r*math.sin(2*math.pi*k/n)) for k in range(n)]
def screws(pts,c,r=3.2):return [(circlep(x,y,r),c,False,0) for x,y in pts]
def slots(x0,x1,step,y,w,h,c):return [([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],c,False,1) for x in range(x0,x1,step)]
def bore(x,y,r,c='#0A0A0D'):return [(x+0.4,[(y+r*math.sin(k*0.5236),r*math.cos(k*0.5236)) for k in range(12)],c,False)]
