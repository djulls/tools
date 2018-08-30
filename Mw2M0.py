#!/usr/bin/env python

import argparse

def Mw2moment(Mw):
    '''
    Convert moment magnitude Mw to seismic moment M0
    :param Mw: moment magnitude
    :type Mw: float
    :return M0: seismic moment in Nm
    :type M0: float
    '''
    
    return 10.0 ** ((Mw + 6.0) / 2.0 * 3)
                   
def energy(M0):
    '''

    '''
    return 1.6 * M0 * 1.e-5

if __name__ == "__main__":
                    
    parser = argparse.ArgumentParser(prog='Mw2M0.py', description='convert moment magnitude Mw to seismic moment')
    parser.add_argument('Mw', type=float,help='Give moment magnitude ',metavar="Mw")

    args = parser.parse_args()
    print " Mw = {:.2f}".format(float(args.Mw))
    print ' M0 = {:.3e} N.m'.format(float(Mw2moment(args.Mw)))
    print " Es = {:.3e} joules".format(float(energy(Mw2moment(args.Mw)*1.e7)))
