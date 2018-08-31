#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Roch Julien
# Bruno HERNANDEZ 20150330

'''
Input : 
strike, dip, rake of NP1.

Output : 
strike, dip, rake of NP1.
MT elements
Principal axes

usage :

./np1_np2TNP.py 321 69 -173

'''

from math import sqrt,sin,cos,pi
from obspy.imaging.beachball import aux_plane,MomentTensor,mt2axes
import argparse
import sys

# input

parser = argparse.ArgumentParser(prog='np1_np2TNP.py',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description='''Get strike, dip, rake, of auxiliray plane given strike, dip, rake of first plane''',
                                 epilog='exemple : ./np1_np2TNP.py 321 69 -173')
parser.add_argument('np', help='Give nodal plane angle (strike,dip,slip)', nargs=3,type=int,metavar=("strike","dip","slip"))

args = parser.parse_args()
NP1=args.np
s1=NP1[0]
d1=NP1[1]
r1=NP1[2]

# Strike,dip and rake of the second plane

s2,d2,r2 = aux_plane(s1,d1,r1)

# degre to radian 

strike=((s1*pi)/180.)
dip=((d1*pi)/180.)
rake=((r1*pi)/180.)

# moment tensor (r=up, t=south and p=east)

is2 = 1/sqrt(2.0)

mrr = is2*( sin(2*dip) * sin(rake) )
mtt = -is2*( sin(dip) * cos(rake) * sin(2*strike) + sin(2*dip) * sin(rake) * sin(strike)**2 )
mpp = is2*( sin(dip) * cos(rake) * sin(2*strike) - sin(2*dip) * sin(rake) * cos(strike)**2 )
mtp = -is2*( sin(dip) * cos(rake) * cos(2*strike) + 0.5*sin(2*dip) * sin(rake) * sin(2*strike) )
mrp = is2*( cos(dip) * cos(rake) * sin(strike) - cos(2*dip) * sin(rake) * cos(strike))
mrt = -is2*( cos(dip) * cos(rake) * cos(strike) + cos(2*dip) * sin(rake) * sin(strike) )

mt = MomentTensor((mrr, mtt, mpp, mrt, mrp, mtp), 0)

# principal axes

(T, N, P) = mt2axes(mt)

# output

print " "
print "MOMENT TENSOR:"
print "MRR = ", mrr
print "MTT = ", mtt
print "MPP = ", mpp
print "MTP = ", mtp
print "MRP = ", mrp
print "MRT = ", mrt
print " "
print "PRINCIPAL AXES:"
print "T axis: VAL = ", round(T.val), " PLG = ", round(T.dip), "AZM = ", round(T.strike)
print "N axis: VAL = ", round(N.val), " PLG = ", round(N.dip), "AZM = ", round(N.strike)
print "P axis: VAL = ", round(P.val), " PLG = ", round(P.dip), "AZM = ", round(P.strike)
print " "
print "DOUBLE COUPLE:"
print "NP1: Strike = ",round(s1)," Dip = ",round(d1)," Rake = ",round(r1)
print "NP2: Strike = ",round(s2)," Dip = ",round(d2)," Rake = ",round(r2)
print " "

