def sumuj(x,y):
   z=(x[0]+y[0],x[1]+y[1],x[2]+y[2])
   return z

c=2.770185435983049#0.0709981290379# stezenie w molach na litr
d=0.2# grubosc w cm
print ("16 1.96")
# 5928 170.96
# 7866 1148,31
# 9158 325.47
# 11073 266.66
# 12474 144.08
# 13280 26.28
# 21102 24.55
# 22.154 63.02
# 23491 24.12
s=4.33e-9/(c*d)
f_6h11=170.96*4.33e-9/(c*d)
wl=5928
u=(0.0960,0.0346,0.6447)
print ("%1.3E %i %1.4f %1.4f %1.4f"% (f_6h11, wl, u[0], u[1], u[2]))

f_6h9=1148.31*s
u=sumuj((0,0.0177,0.1985),(0.9349,0.8310,0.2002))
wl=7866
print ("%1.3E %i %1.4f %1.4f %1.4f"% (f_6h9, wl, u[0], u[1], u[2]))
wl=9158
f_6h7=325.47*s
u=sumuj((0,0.574,0.7201),(0,0.0007,0.0394))
print ("%1.3E %i %1.4f %1.4f %1.4f"% (f_6h7, wl, u[0], u[1], u[2]))
f_6f7=266.66*s
wl=11073
u=(0, 0.1362,0.7124)
print ("%1.3E %i %1.4f %1.4f %1.4f"% (f_6f7, wl, u[0], u[1], u[2]))
f_6f5=144.08*s
wl=12474
u=(0, 0.0,0.3454)
print ("%1.3E %i %1.4f %1.4f %1.4f"% (f_6f5, wl, u[0], u[1], u[2]))
f_6f3=26.08*s
wl=13280
u=(0, 0.0,0.0612)
print ("%1.3E %i %1.4f %1.4f %1.4f"% (f_6f3, wl, u[0], u[1], u[2]))
f_4f3=24.55*s
wl=21102
u=(0, 0.0049,0.0303)
print ("%1.3E %i %1.4f %1.4f %1.4f"% (f_4f3, wl, u[0], u[1], u[2]))
f_4i3=63.02*s
wl=22154
u=(0.0072, 0.0003,0.0684)
print ("%1.3E %i %1.4f %1.4f %1.4f"% (f_4i3, wl, u[0], u[1], u[2]))
f_4g11=24.12*s
wl=23491
u=(0.0004, 0.0146,0.0003)
print ("%1.3E %i %1.4f %1.4f %1.4f"% (f_4g11, wl, u[0], u[1], u[2]))