#!/usr/bin/env python
# -*- coding: utf-8 -*- 

'''
script permettant de determiner le pourcentage de DC, ISO et CLVD dans un 
tenseur des moments.
Example:

CMTSOLUTION format (filename=iceland_Event-20141015.txt):

PDEQ2014 10 15 11 16 34.00  64.4500  -18.0400  10.0 0.0 5.1 ICELAND                                 
event name:     201410151116A  
time shift:      8.2300
half duration:   1.5000
latitude:       64.6000
longitude:     -17.3000
depth:          12.0000
Mrr:      -3.260000e+24
Mtt:       1.960000e+24
Mpp:       1.300000e+24
Mrt:      -6.790000e+22
Mrp:      -6.030000e+23
Mtp:      -2.030000e+23

  using the -c (cmtfile) option:
   ./moment_tensor_dec.py -c iceland_Event-20141015.txt


  or using the option -m (--moment_tensor)
   ./moment_tensor_dec.py -m -3.260000 1.960000 1.300000 -0.06790000 -0.6030000 -0.2030000

Pour la deuxieme option, argaprse ne semble pas reconnaitre les nombres negatifs 
lorsqu'ils sont en notations scientifiques. Donc on decompose le tenseur, en notant
l'exposant a part. L'exposant n'est pas utilise de toute facon. On pourrait 
tres bien s'en passer mais je l'ai conserver pour etre coherent et pour 
l'evolution futur du code.

TODO:
 - pouvoir dessiner les differentes contributions du tenseur des moments
  i.e. la partie CLVD, DC,m ISO (cf MoPad)
  on utilsera obspy et son module beachball.

'''

import numpy as np
import argparse
import sys




#-------------------------------------------------------------------------------
def parse_cmt(cmtfile):
    cmt_dict = {}

    with open(cmtfile, 'r') as fcmt :
         cmt_lines = fcmt.readlines()

         line = cmt_lines[0]
         cmt_dict['mag'] = float(line.split()[10])
         cmt_dict['pde_time'] = line[5:24]

         for line in cmt_lines[1:]:
             key   = line.rstrip().split(':')[0]
             value = ' '.join(line.rstrip().split(':')[1:])
             cmt_dict[key] = value
         return cmt_dict



def main(Mrr,Mtt,Mpp,Mrt,Mrp,Mtp):

    mt_matrix = np.array([[Mrr,Mrt,Mrp],[Mrt,Mtt,Mtp],[Mrp,Mtp,Mpp]])

    # conversion in matrix form
    m = np.asmatrix(mt_matrix)
    print "\nTenseur des moments sismiques :"
    print m



    # calcul les valeurs propres (diagonalise)
    (m1,m2,m3) = np.linalg.eigvals(m)

    # on definit la trace comme la somme des valuers propres.
    tr_m = m1+m2+m3

    # Isotropic part
    iso_m = 0.3333*tr_m * np.identity(3)
    print "\nIsotropic part of the matrix :"
    print iso_m

    # deviatoric part
    m11 = m1 - 0.3333*tr_m
    m12 = m2 - 0.3333*tr_m
    m13 = m3 - 0.3333*tr_m

    print "\nDeviatoric part of the moment tensor :"
    dev_m = np.array([[m11,0,0],[0,m12,0],[0,0,m13]])
    print dev_m

    # Extract the percentage of CLVD and mean DC from the Deviatoric part:
    # valeur propre de la partie deviatoric
    eigval_dev = [m11,m12,m13]
    # tri par ordre croissant de la valeur absolue des valeurs propres deviatorique
    eigval_dev_sort = sorted(np.abs(eigval_dev))
    #print eigval_dev_sort

    # eps = - m_min/m_max
    # eps estimate the DC contribution to the deviatoric moement tensor.
    # For a pure DC: eps = 0 (min=0)
    # For a pure CLVD: eps = 0.5
    eps = eigval_dev_sort[0] / eigval_dev_sort[2]
    #print eps

    iso_perc = 0.3333* 100.* tr_m / abs(eigval_dev_sort[2])
    clvd_perc = -2.* eps * (100. - iso_perc)
    dc_perc = 100. - abs(iso_perc) - abs(clvd_perc)

    return iso_perc, clvd_perc,dc_perc


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='moment_tensor_dec.py',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Estimation of the DC, CLVD and ISO part of a givent moment tensor.',
                                     epilog='''example: 
./moment_tensor_dec.py -m -3.260000 1.960000 1.300000 -0.06790000 -0.6030000 -0.2030000
         or
./moment_tensor_dec.py -c CMTSOLUTION''')
    
    group_input = parser.add_mutually_exclusive_group(required=True)
    group_input.add_argument('-c', '--cmtfile', help='Give a file at the CMTSOLUTION format from the Global CMT catalog')
    group_input.add_argument('-m', '--moment_tensor', help='Give the moment tensor in the following order: Mrr,Mtt,Mpp,Mrt,Mrp,Mtp',
                           nargs=6,type=float,metavar=("Mrr","Mtt","Mpp","Mrt","Mrp","Mtp"))

    args = parser.parse_args()

    if args.cmtfile:
       cmtfile  = args.cmtfile
       cmt_dict = parse_cmt(cmtfile)
       Mrr = float(cmt_dict['Mrr'])
       Mtt = float(cmt_dict['Mtt'])
       Mpp = float(cmt_dict['Mpp'])
       Mrt = float(cmt_dict['Mrt'])
       Mrp = float(cmt_dict['Mrp'])
       Mtp = float(cmt_dict['Mtp'])

 
    elif args.moment_tensor:

       mt = args.moment_tensor

       Mrr=args.moment_tensor[0]
       Mtt=args.moment_tensor[1]
       Mpp=args.moment_tensor[2]
       Mrt=args.moment_tensor[3]
       Mrp=args.moment_tensor[4]
       Mtp=args.moment_tensor[5]


       print "Moment tensor: \n Mrr :",Mrr, \
                     "\n Mtt :",Mtt, \
                     "\n Mpp :",Mpp, \
                     "\n Mrt :",Mrt, \
                     "\n Mrp :",Mrp, \
                     "\n Mtp :",Mtp

 
    iso,clvd,dc = main(Mrr,Mtt,Mpp,Mrt,Mrp,Mtp)

    print "percentage of ISO  : ", np.round(abs(iso),decimals=2)," %"
    print "percentage of DC   : ", np.round(dc,decimals=2)," %"
    print "percentage of CLVD : ", np.round(abs(clvd),decimals=2)," %"

