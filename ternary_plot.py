#!/usr/bin/env python
# -*- coding: utf-8 -*- 

'''

Representation in a ternary diagram of the type of fault mechanism

strike-slip fault are defined for a dip of principal axis N > 60

ref:
 Frohlich et Apperson, tectonics,1992
"Eartquake Focal Mechanisms, moment tensors, and the consistency of seismic 
 activity near plate boundary"

usage :(example with Atlantic earthquake  13-02-2015 -- Mw=7.0)

./ternary_plot.py --mt -0.379  -1.030   1.410   0.891  -0.052  -4.910


-------
Pour l'utiliser depuis un autre script:
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
import sys
sys.path.insert(0, 'path_to_the_script')
import ternary_plot

...

ternary_plot(M)
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
'''

from math import sqrt, sin, cos
import numpy as np
import matplotlib.pylab as plt
import matplotlib.tri as tri
from datetime import datetime
from obspy.imaging.beachball import MomentTensor,mt2axes, beach
import argparse


# conversion deg to radians
degtorad=np.pi/180.

def read_foc_mec_file(fmfile):


    fm = {}
    idx = 0
    with open(fmfile, 'r') as f:
      data = f.readlines()

      for line in data:
          line = line.strip()
          if not line.startswith("#"):
              col = line.split()
              idx +=1
              fm[idx] = {}

              fm[idx]['Mrr']  = float(col[0])
              fm[idx]['Mtt']  = float(col[1])
              fm[idx]['Mpp']  = float(col[2])              
              fm[idx]['Mrt']  = float(col[3])
              fm[idx]['Mrp']  = float(col[4])
              fm[idx]['Mtp']  = float(col[5])

    return fm


def sdrToMt(strike, dip, rake):
    '''
    convert strike dip rake to moment tensor
    '''


    strike *=degtorad
    dip *= degtorad
    rake *= degtorad
    # moment tensor (r=up, t=south and p=east)
    is2 = 1/sqrt(2.0)

    mrr = is2*( sin(2*dip) * sin(rake) )
    mtt = -is2*( sin(dip) * cos(rake) * sin(2*strike) + sin(2*dip) * sin(rake) * sin(strike)**2 )
    mpp = is2*( sin(dip) * cos(rake) * sin(2*strike) - sin(2*dip) * sin(rake) * cos(strike)**2 )
    mtp = -is2*( sin(dip) * cos(rake) * cos(2*strike) + 0.5*sin(2*dip) * sin(rake) * sin(2*strike) )
    mrp = is2*( cos(dip) * cos(rake) * sin(strike) - cos(2*dip) * sin(rake) * cos(strike))
    mrt = -is2*( cos(dip) * cos(rake) * cos(strike) + cos(2*dip) * sin(rake) * sin(strike) )

    #mt = MomentTensor((mrr, mtt, mpp, mrt, mrp, mtp), 0)
    return mrr, mtt, mpp, mrt, mrp, mtp


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
             #print key, value

    return cmt_dict

class ternaryDiagram():

    def __init__(self,scaling=True, start_angle=90,rotate_labels=False,label_offset=-0.4,sides=3):

        #self.data = data

        self.scaling=scaling
        # Direction of first vertex.
        self.start_angle=start_angle
        # Orient labels perpendicular to vertices.
        self.rotate_labels=rotate_labels
        # Labels for vertices.
        self.labels=('strike-slip','Normal','Reverse')
        # Can accomodate more than 3 dimensions if desired.
        self.sides=sides
        # Offset for label from vertex (percent of distance from origin).
        self.label_offset=label_offset
        # Any matplotlib keyword args for plots.
        self.edge_args={'color':'black', 'linewidth':2}
        # Any matplotlib keyword args for figures.
        self.fig_args = {'figsize':(8,8),'facecolor':'white','edgecolor':'white',
                         'tight_layout':False}

        self.bb_args = {'width':50, 'facecolor':'k','bgcolor':'w','alpha':1}

    def background(self):

        self.basis = np.array(
            [
                [
                    np.cos(2*_*np.pi/self.sides + self.start_angle*degtorad),
                    np.sin(2*_*np.pi/self.sides + self.start_angle*degtorad)
                ] 
                for _ in range(self.sides)
            ]
        )
    


        fig = plt.figure(**self.fig_args)
        self.ax = fig.add_axes([0.05,0.05,0.9,0.9])

        SS_bb = beach([45.,90.,0.], xy=(6.73e-17, 1.15),axes=self.ax, **self.bb_args)
        R_bb = beach([0.,45.,90.], xy=(0.95, -0.6),axes=self.ax, **self.bb_args)
        N_bb  = beach([0.,45.,-90.], xy=(-0.95, -0.6),axes=self.ax, **self.bb_args)

        SN_bb = beach([330.,45.,-140.], xy=(-0.55, 0.3),axes=self.ax, **self.bb_args)
        RS_bb = beach([30.,45.,140.], xy=(0.55, 0.3),axes=self.ax, **self.bb_args)
        NR_bb  = beach([0.,90.,-90.], xy=(6.73e-17, -0.6),axes=self.ax, **self.bb_args)

        self.ax.add_collection(SS_bb)
        self.ax.add_collection(R_bb)
        self.ax.add_collection(N_bb)
        self.ax.add_collection(SN_bb)
        self.ax.add_collection(RS_bb)
        self.ax.add_collection(NR_bb)

        # gestion des labels
        for i,l in enumerate(self.labels):
            if i >= self.sides:
                break
            x = self.basis[i,0]
            y = self.basis[i,1]

            if self.rotate_labels:
                angle = 180*np.arctan(y/x)/np.pi + 90
                if angle > 90 and angle <= 270:
                    angle = np.mod(angle + 180,360)
            else:
                angle = 0
            self.ax.text(
                x*(1 + self.label_offset),
                y*(1 + self.label_offset),
                l,
                horizontalalignment='center',
                verticalalignment='center',
                rotation=angle,
                alpha=0.6
            )

        # Plot border
        self.ax.plot(
            [self.basis[_,0] for _ in range(self.sides) + [0,]],
            [self.basis[_,1] for _ in range(self.sides) + [0,]],
            **self.edge_args
        )

        # Clear normal matplotlib axes graphics.
        self.ax.set_xticks(())
        self.ax.set_yticks(())
        self.ax.set_frame_on(False)



    def plot_data(self,data,M,mag=None):

        # If data is Nxsides, newdata is Nx2.
        if self.scaling:
            # Scales data for you.
            tridata = np.dot((data.T / data.sum(-1)).T,self.basis)
        else:
            # Assumes data already sums to 1.
            tridata = np.dot(data,self.basis)        

        '''
        self.ax.plot(tridata[:,0], tridata[:,1],
                     marker='o', 
                     ms=10, 
                     alpha=0.8,
                     color='r')
        '''
        if mag:
            width=mag*0.05
        else:
            width=0.09

        b = beach(M, 
                  xy=(tridata[:,0], tridata[:,1]),
                  width=width, 
                  linewidth=1,
                  facecolor='r')
        
        b.set_zorder(1)
        self.ax.add_collection(b)



def main():

    parser = argparse.ArgumentParser(description='Ternary plot to display the type pf mechanism')
    group_input = parser.add_mutually_exclusive_group(required=False)
    group_input.add_argument('-c', '--cmtfile', help='Give a file at the CMTSOLUTION format from the Global CMT catalog')

    group_input.add_argument('--mt', 
                             help='Give the moment tensor in the following order: Mrr,Mtt,Mpp,Mrt,Mrp,Mtp',
                             nargs=6,
                             type=float,
                             metavar=("Mrr","Mtt","Mpp","Mrt","Mrp","Mtp"))

    group_input.add_argument('--np', help='Give nodal plane angle (strike,dip,slip)',
                             nargs=3,
                             type=float,
                             metavar=("strike","dip","slip"))

    parser.add_argument('--infile',help='read input file with several moment tensor')

    parser.add_argument('--debug', help='debug mode', action='store_true')
    parser.add_argument('-o','--output', help='save figure (png, svg, eps, pdf)')

    args = parser.parse_args()

    if args.infile:
        fm = read_foc_mec_file(args.infile)        
        print fm

        
    if args.cmtfile:
       cmtfile  = args.cmtfile
       cmt_dict = parse_cmt(cmtfile)
       Mrr = float(cmt_dict['Mrr'])
       Mtt = float(cmt_dict['Mtt'])
       Mpp = float(cmt_dict['Mpp'])
       Mrt = float(cmt_dict['Mrt'])
       Mrp = float(cmt_dict['Mrp'])
       Mtp = float(cmt_dict['Mtp'])
 
    elif args.mt:

       Mrr=args.mt[0]
       Mtt=args.mt[1]
       Mpp=args.mt[2]
       Mrt=args.mt[3]
       Mrp=args.mt[4]
       Mtp=args.mt[5]


    elif args.np:
        
        Mrr,Mtt,Mpp,Mrt,Mrp,Mtp = sdrToMt(args.np[0], args.np[1], args.np[2])


    M = MomentTensor( (Mrr,Mtt,Mpp,Mrt,Mrp,Mtp), 0)
    # principal axes
    (T, N, P) = mt2axes(M)



    if args.debug:
        
        print "Moment tensor: \n Mrr :",Mrr, \
            "\n Mtt :",Mtt, \
            "\n Mpp :",Mpp, \
            "\n Mrt :",Mrt, \
            "\n Mrp :",Mrp, \
            "\n Mtp :",Mtp

        print "PRINCIPAL AXES:"
        print "T axis: VAL = ", round(T.val), " PLG = ", round(T.dip), "AZM = ", round(T.strike)
        print "N axis: VAL = ", round(N.val), " PLG = ", round(N.dip), "AZM = ", round(N.strike)
        print "P axis: VAL = ", round(P.val), " PLG = ", round(P.dip), "AZM = ", round(P.strike)


    x = sin(T.dip*degtorad)
    y = sin(N.dip*degtorad)
    z = sin(P.dip*degtorad)

    data = np.array([[y,z,x]])


    tri=ternaryDiagram()
    tri.background()

    tri.plot_data(data,M)

    if args.output:
        plt.savefig(output, bbox_inches='tight')
    else:
        plt.show()

if __name__ == '__main__':

    main()
