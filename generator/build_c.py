from cepaths import E3D,OUT
import sys,importlib
sys.path.insert(0,E3D+'')
from views import *
NN=sys.argv[1];M=importlib.import_module('c'+NN)
k=M.META
h=card(M.model(),M.CENTER,NN,k['name'],f'VARIANTE C · „{k["var"]}“ · ALLE PERSPEKTIVEN, GEZEICHNET',k['col'],k['pill'],k['desc'],k['pal'],k['form'],'c'+NN)
open(f'{OUT}/C3D{NN}.dc.html','w').write(h)
open(f'{E3D}/prev_c{NN}.html','w').write(h.replace('<script src="./support.js"></script>',''))
