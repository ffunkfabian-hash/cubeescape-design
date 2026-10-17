PE,CR,KO,DK='#1F4E5F','#F4EBD9','#FF6F59','#14181C'
INFO=dict(num='01',name='Pistole',nick='KORALLENRIFF',col=KO,pill='PETROL · CREME · KORALLE',pal=[PE,CR,KO,DK],center=(400,350,0),
 alt='Pistole Variante F: Revolver-Pistole in Petrol und Creme mit runder Trommel, Korallen-Kammern und schwerer Mündung',
 desc='Statt kantigem Block jetzt ein Revolver: Die Creme-Trommel steht seitlich aus dem Rahmen, der Lauf fluchtet mit der oberen Kammer. Die Trommel sitzt in einem Rahmenfenster zwischen oberem und unterem Steg. Unter dem Lauf liegt die Unterhülse, oben die Kühlrippe als Visierschiene – Kimme und Korn sind separat gezeichnet. Der Griff ist geschwungen und nach hinten geneigt.',
 form='Rahmen mit Fenster für die Trommel (sechs Kammern) · Lauf mit Kühlrippe als Visierschiene und Unterhülse · Mündung · geschwungener Griff mit Abzugbügel · Kimme und Korn separat')
from fsight import clipall,xmin,xmax,ymin,ymax
_FR=[(170,222),(430,222),(450,242),(450,316),(340,326),(250,326),(190,318),(160,282)]
# Rahmen mit Fenster fuer die Trommel (x 296-384): hinterer Block, vorderer Block, oberer und unterer Steg
FRAME=[
 dict(t='poly',p=clipall(_FR,xmax(296)),c=PE,z=(-28,28),r=12,L='Rahmen',
      d=[([(190,238),(286,238),(286,248),(186,248)],CR,False,3),([(196,298),(280,298),(280,305),(196,305)],KO,True,2)]),
 dict(t='poly',p=clipall(_FR,xmin(384)),c=PE,z=(-28,28),r=12,L='Rahmen',
      d=[([(400,240),(436,240),(436,250),(400,250)],DK,False,2),([(400,258),(436,258),(436,268),(400,268)],DK,False,2)]),
 dict(t='poly',p=clipall(_FR,xmin(296),xmax(384),ymax(227)),c=PE,z=(-22,22),r=2),
 dict(t='poly',p=clipall(_FR,xmin(296),xmax(384),ymin(317)),c=PE,z=(-22,22),r=2),
]
ITEMS=[
 dict(t='poly',p=[(262,322),(328,322),(306,470),(292,486),(240,486),(226,470)],c=DK,z=(-22,22),r=10,L='Griff',
      d=[([(272,342),(314,342),(298,452),(256,452)],KO,False,6),([(268,378),(306,378),(304,388),(266,388)],DK,False,0),([(262,412),(302,412),(300,422),(260,422)],DK,False,0)]),
 dict(t='poly',p=[(323,362),(396,360),(396,368),(322,370)],c=DK,z=(-4,4)),
 dict(t='poly',p=[(388,318),(396,318),(396,368),(388,368)],c=DK,z=(-4,4)),
 dict(t='poly',p=[(348,322),(360,322),(368,354),(358,356)],c=CR,z=(-6,6),L='Abzug'),
 dict(t='poly',p=[(128,232),(172,226),(172,270),(136,262)],c=DK,z=(-10,10),r=5),
] + FRAME + [
 dict(t='cyl',x=(296,384),y=272,R=44,c=CR,L='Trommel'),
 dict(t='cyl',x=(318,322),y=272,R=45,c=DK),
 dict(t='cyl',x=(358,362),y=272,R=45,c=DK),
]
import math
ITEMS[[i for i,it in enumerate(ITEMS) if it.get('L')=='Trommel'][0]]['ends']=[(272+28*math.sin(2*math.pi*k/6+math.pi/6),28*math.cos(2*math.pi*k/6+math.pi/6),8,KO,True) for k in range(6)]+[(272,0,7,DK,False)]
ITEMS+=[
 dict(t='cyl',x=(384,630),y=244,R=18,c=DK,L='Lauf'),
 dict(t='poly',p=[(384,261),(600,261),(618,272),(600,285),(384,285)],c=PE,z=(-16,16),r=8,d=[([(420,270),(580,270),(580,276),(420,276)],KO,True,2)]),
 dict(t='poly',p=[(400,220),(612,220),(612,230),(400,230)],c=CR,z=(-5,5),r=3,L='Visierschiene'),
 dict(t='poly',p=[(404,207),(422,207),(422,220.5),(404,220.5)],c=DK,z=(-8,8),r=3,L='Kimme',S=True),
 dict(t='cyl',x=(630,666),y=244,R=26,c=KO,cap=[(15,DK,False),(7,CR,True)],L='Mündung'),
 dict(t='poly',p=[(640,208),(656,208),(656,219),(640,219)],c=DK,z=(-4,4),r=2,L='Korn',S=True),
]
