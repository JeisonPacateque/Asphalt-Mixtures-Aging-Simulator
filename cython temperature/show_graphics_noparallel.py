import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import temperatura
import datetime

start_time = datetime.datetime.now()

n_elementos = 100
n_iteraciones = 1000

X, Y, U = temperatura.difusion(n_iteraciones, n_elementos)

end_time = datetime.datetime.now()
d_secs = end_time - start_time
print "Numero de elementos = ", n_elementos
print "Numero de iteraciones = ", n_iteraciones
print "Fue necesario", d_secs

plt.figure(1)
plt.clf()                      # clear figure
plt.pcolor(X,Y,U,cmap=cm.jet)  # pseudo-color plot using colormap "jet"
plt.axis('scaled')

plt.clim(0., 1.)               # colors range from u=0 to u=1
plt.colorbar()                 # add a color bar to show temperature scale
plt.title('Temperature')
plt.show()


plt.figure(2)
plt.clf()

# contour line levels:
clines = np.linspace(0., 1., 10)
#print clines

# do contour plot:
C = plt.contour(X,Y,U,clines,colors='k')
plt.axis('scaled')             # so x- and y-axis scaled the same (square)

# add labels on every other line:
plt.clabel(C, clines[1::2], inline=10, fontsize=10)

plt.title('Contours of temperature')

#plt.savefig('contour.png')
plt.show()