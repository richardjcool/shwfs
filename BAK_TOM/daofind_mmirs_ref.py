#!/usr/bin/env python

import os
from math import *
import sys
import re
import getopt
import numpy
import scipy.ndimage as nd
import pyfits
import imagestats
from pyraf import iraf

def dimm_seeing(fwhm, ref_fwhm, scale):

    # this is the eff wavelength of both systems
    lamb = 0.65e-6

    # 14 apertures/pupil is also pretty close for both cases
    # certainly for f/5 while f/9 is a little funky with the hex geom
    d = 6.5/14.0

    # reference files give me a mean fwhm of about 2.1-2.15 pix
    if fwhm > ref_fwhm:
        #
        # deconvolve reference fwhm and convert to radians.
        #
        f = sqrt(2.0)*sqrt(fwhm**2 - ref_fwhm**2)*scale/206265.0
        s = (f**2)/(8*log(2))

        r0 = ( 0.358*(lamb**2)*(d**(-1.0/3.0))/s )**0.6
        seeing = 206265*0.98*lamb/r0
        return seeing
    else:
        return 0.0

def ds9spots(file, xcol, ycol, color):
    data = file.split('\.')
    reg = data[0] + ".reg"
    xpa = open(reg, 'w')
    xpa.write("# Region file format: DS9 version 3.0\n")
    xpa.write("# Filename: %s\n" % file)
    xpa.write("global color=%s font=\"helvetica 10 normal\" select=1 edit=1 move=1 delete=1 include=1 fixed=0 source\n" % color)
    
    spots = open(file, 'r')
    for line in spots:
        data = line.split()
        x = data[xcol]
        y = data[ycol]
        xpa.write("image;circle(%f,%f,1) # color = %s\n" % (float(x), float(y), color))

    xpa.close()
    os.system("cat %s | xpaset WFS regions" % reg)

def rfits(file):
    f = pyfits.open(file)
    hdu = f[0]
    (im, hdr) = (hdu.data, hdu.header)
    f.close()
    return hdu

def get_seeing(file, scale, ref):
    coords = file.replace('fits','dao')
    log = file.replace('fits','psf')
    out = file.replace('fits','seeing')

    iraf.noao()
    iraf.noao.obsutil()
    iraf.set(stdgraph="uepsf")

    data = iraf.psfmeasure(file, coords='markall', wcs='logical', display='no', frame=1, level=0.5, size='FWHM', radius=10.0, sbuffer=1.0, swidth=3.0, iterations=1, logfile=log, imagecur=coords, Stdout=1)

    fwhm = data.pop().split().pop()

    fwhm_pix = float(fwhm)
    fwhm = fwhm_pix*scale
    seeing = dimm_seeing(fwhm_pix, ref, scale)
    print seeing
    fp = open(out, 'w')
    fp.write("%f %f\n" % (fwhm_pix, seeing))
    fp.close()
    os.system("echo \"image;text 85 500 # text={Spot FWHM = %5.2f pixels}\" | xpaset WFS regions" % fwhm_pix)
    os.system("echo \'image;text 460 500 # text={Seeing = %4.2f\"}\' | xpaset WFS regions" % seeing)
    os.system("echo \"set wfs_seeing %4.2f\" | nc hacksaw 7666" % seeing)

def get_center(im, xrefcen, yrefcen):
    (ycen, xcen) = nd.center_of_mass(im)
    #(ycen, xcen) = pos[0]
    xcen = xcen+1
    ycen = ycen+1
    
#    print "Pupil Center: X = %7.3f, Y = %7.3f" % (xcen, ycen)
#    os.system("echo \"circle %f %f 5 # color=yellow\" | xpaset WFS regions" % (xcen, ycen))
    xoff = xcen - xrefcen
    yoff = ycen - yrefcen
#    print "Pupil Offset: X = %7.3f, Y = %7.3f" % (xoff, yoff)
#    print "                  %6.2f\",     %6.2f\"" % (xoff*scale[mode]/sky[mode], yoff*scale[mode]/sky[mode])

    return (xcen, ycen)

def daofind(im):
    cfile = open("/mmt/shwfs/%s_reference.center" % mode, 'r')
    [xrefcen, yrefcen] = cfile.read().split()
    xrefcen = float(xrefcen)
    yrefcen = float(yrefcen)
    cfile.close

    ffile = open("/mmt/shwfs/%s_reference.fwhm" % mode, 'r')
    [reffwhm, reffwhm_pix] = ffile.read().split()
    reffwhm = float(reffwhm)
    reffwhm_pix = float(reffwhm_pix)
    ffile.close

    im = im*1.0
    allstats = imagestats.ImageStats(im)
    stats = imagestats.ImageStats(im, nclip=5)
    mean = stats.mean
    sig = stats.stddev
    max = stats.max

    print "Mean = ", mean
    
    if mode == 'F9':
        smooth = nd.gaussian_filter(im, 5.0)
        maxstars = 140
    elif mode == 'F5':
        smooth = nd.gaussian_filter(im, 3.0)
        maxstars = 140
    else:
        smooth = nd.gaussian_filter(im, 1.0)
        maxstars = 225
        
    nsig = 5.0
    nstars = 0
    
    while nstars < maxstars:
        spot_clip = smooth >= (mean + nsig*sig)
        labels, num = nd.label(spot_clip)
        nstars = num
        nsig = nsig - 0.1
        if nsig <= -1.0:
            break
#        print num, " spots found."

    if num < 140:
        print "Pupil too far off image or seeing too poor."
        os.system("echo \"image;text 256 500 # text={Seeing too poor or pupil too far off image.}\" | xpaset WFS regions")
        return (False, False, False)
    
    if mode == 'F9':
        clip = smooth >= (mean + (nsig+2.0)*sig)
    elif mode == 'F5':
        clip = smooth >= (mean + (nsig-2.0)*sig)
    else:
        clip = smooth >= (mean + (nsig-2.0)*sig)

    pos = nd.center_of_mass(im, labels, range(num))
    counts = numpy.array( nd.sum(im, labels, range(num)) )
    countstats = imagestats.ImageStats(counts, nclip=3)
    cmean = countstats.mean
    csig = countstats.stddev

    daofile = fitsfile.replace('fits', 'dao')
    dao = open(daofile, 'w')

    spots = []
  
    for spot in pos[1:]:
        (y, x) = spot
        x = x + 1
        y = y + 1
        i = pos.index(spot)
        c = counts[i]-cmean
        if x < 470 and y < 500 and x > 25 and y > 35:
            spots.append( (x, y, c) )
            dao.write("%8.3f  %8.3f\n" % (x, y))
        
    dao.close()
    ds9spots(daofile, 0, 1, 'red')

    if mode == 'MMIRS':
        cen_clip = nd.gaussian_filter(im, 3.0) >= 50
    else:
        if mean < 750.0:
            cen_clip = nd.gaussian_filter(im, 20.0) >= mean
        else:
            cen_clip = nd.gaussian_filter(im, 20.0) >= 750
    
    (xcen, ycen) = get_center(cen_clip, xrefcen, yrefcen)
    get_seeing(fitsfile, scale[mode], reffwhm_pix)

    cenfile = fitsfile.replace('fits', 'center')
    cen = open(cenfile, 'w')
    cen.write("%f %f\n" % (xcen, ycen))
    cen.close()
    return (xcen, ycen, spots)

def average(fitsfiles):
    if fitsfiles.find(',') > -1:
        files = fitsfiles.split(',')
        averot = 0.0
        for file in files:
            hdu = rfits(file)
            im = hdu.data
            hdr = hdu.header
            try:
                rot = hdr['ROT']
            except KeyError:
                rot = 0.0

            averot = averot + float(rot)
            
            try:
                ave
            except NameError:
                ave = None

            if ave is None:
                ave = im/len(files)
            else:
                ave = ave + im/len(files)

        ave = ave/len(files)
        try:
            hdr['ROT'] = averot/len(files)
        except KeyError:
            hdr.add_history("Rotator angle not available.")
        hdr.add_history("Averaged %s." % fitsfiles)
        out = file.replace('.fits', '_ave.fits')
        hdu.data = ave
        hdu.header = hdr
        try:
            hdu.writeto(out)
        except:
            os.remove(out)
            hdu.writeto(out)
            
        return(out)
    else:
        return fitsfiles

# need this for f/9.....
def getmags():
    fp = open("xyrc.tst", 'r')
    lines = fp.readlines()
    fp.close

    spots = []
    nr = 0
    nc = 0
    for line in lines:
        data = line.split()
        x = float(data[0])
        y = float(data[1])
        row = int(float(data[2]))
        col = int(float(data[3]))
        spots.append([x,y,row,col])
        if row > nr:
            nr = row
        if col > nc:
            nc = col

    rows = []
    cols = []
    for i in range(0,nr+1):
        rows.append([])
    for i in range(0,nc+1):
        cols.append([])

    for spot in spots:
        rows[spot[2]].append(spot[1])
        cols[spot[3]].append(spot[0])

    nyave = 0
    yave = 0
    for row in rows:
        row.sort()
        if len(row) > 3:
            for i in range(0,len(row)-1):
                diff = row[i+1] - row[i]
                if diff < 50.0:
                    yave = yave + diff
                    nyave = nyave + 1

    # correct for hexagonal array
    yave = (25.0/26.0)*(1.732/2.0)*yave/nyave

    nxave = 0
    xave = 0
    for col in cols:
        col.sort()
        if len(col) > 3:
            for i in range(0,len(col)-1):
                diff = abs(col[i+1] - col[i])
                if diff < 75.0:
                    xave = xave + diff
                    nxave = nxave + 1

    # correct for hexagonal array
    xave = (12.0/13.0)*xave/(2.0*nxave)
    return (xave, yave)
    
def shcenfind(fitsfile, mode, xcen, ycen):
    if mode == 'F9':
        pipe = os.popen("export WFSROOT=/mmt/shwfs; /mmt/shwfs/shcenfind %s" % fitsfile.replace('fits', 'dao'))
    if mode == 'F5':
        pipe = os.popen("export WFSROOT=/mmt/shwfs; /mmt/shwfs/shcenfind_f5 %s" % fitsfile.replace('fits', 'dao'))
    if mode == 'MMIRS':
        pipe = os.popen("export WFSROOT=/mmt/shwfs; /mmt/shwfs/shcenfind_mmirs %s" % fitsfile.replace('fits', 'dao'))

    rows, cols = pipe.read().split()
    print "Found %s rows and %s cols." % (rows, cols)
    
    dao = open(fitsfile.replace('fits', 'dao'), 'r')
    daolines = dao.readlines()
    dao.close()

    (dum1, dum2, xmag, ymag, xc, yc) = daolines[0].split(' ')
    if mode == 'F9':
        if rows == '26' and cols == '13':
            daolines[0] = "# X %s %s %s %s" % (xmag, ymag, xc, yc)
            os.system("echo \"image;circle %f %f 5 # color=yellow\" | xpaset WFS regions" % (float(xc), float(yc)))
        else:
            (xmag, ymag) = getmags()
            daolines[0] = "# X %8.4f %8.4f %8.4f %8.4f\n" % (xmag, ymag, xcen-9.0, ycen-7.0)
            os.system("echo \"image;circle %f %f 5 # color=red\" | xpaset WFS regions" % (xcen-9.0, ycen-7.0))
            os.system("echo \"image;text 256 20 # text={%s rows, %s cols}\" | xpaset WFS regions" % (rows, cols))
    elif mode == 'F5' and rows == '14' and cols == '14':
        daolines[0] = "# X %s %s %s %s" % (xmag, ymag, xc, yc)
        os.system("echo \"image;circle %f %f 5 # color=yellow\" | xpaset WFS regions" % (float(xc), float(yc)))
    elif mode == 'MMIRS': #and rows == '14' and cols == '14':
        daolines[0] = "# X %s %s %s %s" % (xmag, ymag, xc, yc)
        os.system("echo \"image;circle %f %f 5 # color=yellow\" | xpaset WFS regions" % (float(xc), float(yc)))
    else:
        daolines[0] = "# X %s %s %8.4f %8.4f\n" % (xmag, ymag, xcen, ycen)
        os.system("echo \"image;circle %f %f 5 # color=red\" | xpaset WFS regions" % (xcen, ycen))

    dao = open(fitsfile.replace('fits', 'dao'), 'w')
    dao.write("# %s\n" % fitsfiles)
    dao.writelines(daolines)
    dao.flush()
    dao.close()

def zernikes(fitsfile, mode, ref, rotangle):
    if mode == 'F9':
        zern = os.popen("/mmt/shwfs/getZernikesAndPhases %s %s 0 %s" % (ref, fitsfile.replace('fits', 'dao'), rotangle))
    if mode == 'F5':
        zern = os.popen("/mmt/shwfs/getZernikesAndPhases_f5 %s %s 0 %s" % (ref, fitsfile.replace('fits', 'dao'), rotangle))
    if mode == 'MMIRS':
        zern = os.popen("/mmt/shwfs/getZernikesAndPhases_mmirs %s %s 0 %s" % (ref, fitsfile.replace('fits', 'dao'), rotangle))
    print zern.read()

def draw_dirs(rot, off, daofile):
    l = 35.0
    cntr = open(daofile, 'r')
    pound, char, xmag, ymag, x, y = cntr.readlines()[1].split()
    x = float(x)
    y = float(y)
    el = rot + off + 90
    az = el + 270
    ang = pi*(rot + off)/180.0

    az_y = l/( (sin(ang)**2/cos(ang)) + cos(ang) )
    az_x = -1.0*az_y*sin(ang)/cos(ang)
    el_y = l/( (cos(ang)**2/sin(ang)) + sin(ang) )
    el_x = el_y*cos(ang)/sin(ang)

    laz_y = (l-10.0)/( (sin(ang)**2/cos(ang)) + cos(ang) )
    laz_x = -1.0*laz_y*sin(ang)/cos(ang)
    lel_y = (l-10.0)/( (cos(ang)**2/sin(ang)) + sin(ang) )
    lel_x = lel_y*cos(ang)/sin(ang)

    el_x += x
    el_y += y
    az_x += x
    az_y += y

    lel_x += x
    lel_y += y
    laz_x += x
    laz_y += y

    os.system("echo \'image;text %f %f  # text={+El}\' | xpaset WFS regions" % (el_x, el_y))
    os.system("echo \'image;text %f %f  # text={+Az}\' | xpaset WFS regions" % (az_x, az_y))
    os.system("echo \'image;vector %f %f 25 %f' | xpaset WFS regions" % (x, y, az))
    os.system("echo \'image;vector %f %f 25 %f' | xpaset WFS regions" % (x, y, el))
       
########################################################################3

scale = {}
scale['F5'] = 0.135
scale['F9'] = 0.12
scale['MMIRS'] = 0.208

sky = {}
sky['F5'] = 0.297
sky['F9'] = 0.167
sky['MMIRS'] = 0.297

ref = {}
ref['F5'] = "/mmt/shwfs/f5sysfile.cntr"
ref['F9'] = "/mmt/shwfs/f9newsys.cntr"
ref['MMIRS'] = "/mmt/shwfs/mmirs_sysfile.cntr"

rotoff = {}
rotoff['F5'] = 135.0
rotoff['F9'] = -225.0
rotoff['MMIRS'] = -90

fitsfiles = sys.argv[1]
mode = sys.argv[2]
fitsfile = average(fitsfiles)
if fitsfile.find('/') is -1:
    fitsfile = "%s/%s" % (os.getcwd(), fitsfile)

os.system("rm -f back.fits")
iraf.images()
iraf.images.imfit()
iraf.images.imutil()
#iraf.crutil()
if mode == 'MMIRS':
    flipme = True
    headers = iraf.imhead(fitsfile, long='yes', Stdout=1)
    for line in headers:
        if re.match('WAT', line):
            flipme = False

    if flipme:
        print "not flipped"
        iraf.imsurfit(fitsfile, 'back.fits', xorder=2, yorder=2, upper=2, lower=2, ngrow=15)
        iraf.imarith(fitsfile, '-', 'back.fits', fitsfile)
        iraf.imcopy(fitsfile + '[*,*]', fitsfile)
#        iraf.cosmicrays(fitsfile, fitsfile, interactive='no')
        
    else:
        print "flipped"

else:
    iraf.imsurfit(fitsfile, 'back.fits', xorder=2, yorder=2)
    iraf.imarith(fitsfile, '-', 'back.fits', fitsfile)

hdu = rfits(fitsfile)
image = hdu.data
hdr = hdu.header
try:
    rot = hdr['ROT']
except KeyError:
    rot = 0.0

os.system("xpaset -p WFS cd `pwd`")
os.system("xpaset -p WFS file %s" % fitsfile)

xcen, ycen, spots = daofind(image)

if spots:
    avfile = fitsfile.replace('fits', 'dao')
    print avfile, rot
    shcenfind(fitsfile,mode,xcen,ycen)
    #draw_dirs(rot, rotoff[mode], avfile)