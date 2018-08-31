#!/usr/bin/env python
# -*- coding: utf-8 -*- 

'''
 script permettant de dessiner les beachballs:
On lui donne en entree: soit le tenseur des moments
                        soit les angles strike, dip, slip

Les autres options permettent de choisir la couleur de la partie en compression 
du beachball, la partie en dilatation reste en blanc.
On peut aussi choisir le nom du fichier de sortie pour recuperer les beachball 
et les inserer dans une presentation

exemple:

./plot_beachball.py -np 200 26 56 -c b
./plot_beachball.py -mt -3.260000 1.960000 1.300000 -0.06790000 -0.6030000 -0.2030000

'''


from obspy.imaging.beachball import beachball,aux_plane, mt2plane, MomentTensor,beach
import argparse
import sys
import matplotlib.pylab as plt


class BB():

   def __init__(self,facecolor='r',edgecolor='k',
                alpha=1,
                bgcolor='w',
                outputname=None):


      self.edgecolor=edgecolor
      self.alpha = alpha
      self.bgcolor=bgcolor
      self.facecolor=facecolor
      self.lw=1.

      self.outputname = outputname


   def draw(self,fm,NP=None):

      fig=plt.figure(figsize=(8,8))
      ax = fig.add_axes([0.05,0.05,0.9,0.9])

      b = beach(fm, 
                xy=(0.5,0.5),
                facecolor=self.facecolor,
                linewidth=self.lw,
                bgcolor=self.bgcolor,
                edgecolor=self.edgecolor,
                alpha=self.alpha,
                width=1,
                size=1)

      b.set_zorder(10)
      ax.add_collection(b)

      if NP:
         b2 = beach(NP, 
                    xy=(0.5,0.5),
                    #facecolor=self.facecolor,
                    linewidth=self.lw+1,
                    #bgcolor=self.bgcolor,
                    #edgecolor=self.edgecolor,
                    #alpha=self.alpha,
                    nofill=True,
                    width=1,
                    size=1)

        

         b2.set_zorder(11)
         ax.add_collection(b2)

      ax.set_xticks(())
      ax.set_yticks(())
      ax.set_frame_on(False)

      if self.outputname:
         plt.savefig(self.outputname, bbox_inches='tight',transparent=True)
      else:
         plt.show()



def main():

    parser = argparse.ArgumentParser(description='Draws a beachball of an earthquake focal mechanism given strike, dip, rake or the 6 components of the moment tensor')

    parser.add_argument('--fm', help='Nodal plane (strike dip rake) or moment tensor (Mrr Mtt Mpp Mrt Mrp Mtp)',type=float,nargs='+')
    parser.add_argument('--dc', help='superpose the double couple component',action='store_true')
    parser.add_argument('-c','--color', help='Choose a color for the quadrant of tension (r,b,k,g,y...). Default color is red',default='r',type=str)
    parser.add_argument('-o','--output', help='Name of the output file (could be a png, ps, pdf,eps, and svg). Default is None',default=None,type=str)

    args = parser.parse_args()

    bb = BB(outputname=args.output,facecolor=args.color)

    NP = None

    if args.fm:

       if len(args.fm) == 6:
          print "Draw beachball from moment tensor"
          Mrr=args.fm[0]
          Mtt=args.fm[1]
          Mpp=args.fm[2]
          Mrt=args.fm[3]
          Mrp=args.fm[4]
          Mtp=args.fm[5]
          M = MomentTensor( (Mrr,Mtt,Mpp,Mrt,Mrp,Mtp), 0)
          nod_planes = mt2plane(M)
          if args.dc:
             NP = (nod_planes.strike,nod_planes.dip,nod_planes.rake )
             s2,d2,r2 = aux_plane(nod_planes.strike,nod_planes.dip,nod_planes.rake)

          print "Moment tensor:", \
            "\n Mrr :",Mrr, \
            "\n Mtt :",Mtt, \
            "\n Mpp :",Mpp, \
            "\n Mrt :",Mrt, \
            "\n Mrp :",Mrp, \
            "\n Mtp :",Mtp

          print "NP1:",round(nod_planes.strike),round(nod_planes.dip),round(nod_planes.rake)
          print "NP2:",round(s2),round(d2),round(r2)
         

       elif len(args.fm) == 3:
          print "Draw beachball from nodal plane"
          # compute auxiliary plane
          s2,d2,r2 = aux_plane(args.fm[0],args.fm[1],args.fm[2])

          print "NP1:",round(args.fm[0]),round(args.fm[1]),round(args.fm[2])
          print "NP2:",round(s2),round(d2),round(r2)


       bb.draw(args.fm, NP=NP)

if __name__ == "__main__":

   main()
