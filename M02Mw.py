#!/usr/bin/env python

from math import log10
import argparse


def moment2Mw(M0):
    """
    Convert seismic moment M0 to moment magnitude
    :param M0: seismic moment
    :type M0: float
    :return  Mw: moment magnitude
    :type Mw: float

    """
    return (2./3.) * log10(M0) - 10.7

def energy(M0):
    '''

    '''
    return 1.6 * M0 * 1.e-5


if __name__ == "__main__":
                    
    parser = argparse.ArgumentParser(prog='M02Mw.py',
            description='convert seismic moment to moment magnitude Mw')
    parser.add_argument('M0', help='Give seismic moment in N.m ',metavar="M0",type=float)
    parser.add_argument('--dyne',action='store_true', help='convert M0 to N.m')
    args = parser.parse_args()
    if args.dyne:
        scale = 1.
        print ' M0 = {:.3e} dyne.cm ({:.3e} N.m)'.format(float(args.M0), float(args.M0)/1.e7 )
    else:
        scale = 1.e7
        print ' M0 = {:.3e} N.m ({:.3e} dyne.cm)'.format(float(args.M0), float(args.M0*scale))
        
    print " Mw = {:.2f}".format(float(moment2Mw(args.M0*scale)))
    print " Es = {:.3e} joules".format(float(energy(args.M0*scale)))
