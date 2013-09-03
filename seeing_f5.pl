#!/usr/bin/perl

$file = $ARGV[0];

$nspots = 0;
$sum = 0;

open(SF, "$file") || die "Can't open $file. \n";

while (<SF>) {

  next if /^#/;
  next if /^\s*$/;

  @data = split(' ');

  $sum += $data[4];
  $nspots++;

}

close(SF);

if ($nspots > 0) {
  $ave_hwhm = $sum/$nspots;

  $seeing = get_seeing($ave_hwhm);

  printf "%5.2f %5.2f\n",$ave_hwhm, $seeing;
}

# the relations used here are taken from:
# http://www.ing.iac.es/Astronomy/development/hap/dimm.html
#
# i assume the spot width is all random motion, though it seems that
# starfind's FWHM's are somewhat biased, especially of the spots are
# strongly non-gaussian.
#
sub get_seeing {

  my $hwfm = $_[0];

  # 6000 A is a pretty close approx for both WFS's
  my $lambda = 0.6e-6;

  # 14 apertures/pupil is also pretty close for both cases
  # certainly for f/5 while f/9 is a little funky with the hex geom
  my $d = 6.5/14;
  my $r = $d;

  if ($hwfm > 1.25) {
    my $fwhm = sqrt(2.0)*sqrt((2*$hwfm)**2 - 2.5**2)*20;

    my $s = ($fwhm**2)/(8*log(2));

    my $r0 = ( 2.0*$lambda*($d**(-1/3))*(0.179-0.0968)/($s) )**(0.6);

    return 0.98*$lambda/$r0;
  } else {
    return 0.0
  }

}

