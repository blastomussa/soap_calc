#!/user/local/bin/perl

# josephcourtney_soap_calc.pl
# Author: Joseph Courtney
# This a perl program that calculates the necessary amounts of liquids and
# lye(sodium hydroxide) in grams for a specific combination of fatty oils. It
# then outputs the full recipe. To run this program simply type perl
# sort.pl. the program will then ask the user for the total
# number of oils, the total weight of oils and the necessary superfatting
# ratio. It then asks the user for the name of the oils they would like to use
# and their respective ratios. The program calculates the necessary variables
# and outputs the complete soap recipe for the user. It then gives the option
# to resize the batch by changing the total oil weight and gives the user the
# option to save the recipe to a text file. The program will outputerror
# messages if the total percentage of oils is not 100 or if there is an unknown
# oil in the user input.

use strict;
use warnings;
use List::MoreUtils 'first_index';  # module to get index in array

                          # Variable Declarations #

my @oils = ( "aloe", "apricotkernel", "avocado", "babussa", "beeswax", "canola", "castor", "cocoa", "coconut", "coffee", "corn", "cottonseed", "flaxseed", "grapeseed", "hazelnut", "hempseed", "jojoba", "lard", "mango", "mustard", "neem", "olive", "palm", "peanut", "pumpkinseed", "ricebran", "sesame", "shea", "soybean", "sunflower", "sweetalmond", "walnut");
my @sap_ratios = ( 0.171, 0.135, 0.134, 0.179, 0.067, 0.123, 0.129, 0.138, 0.178, 0.134, 0.135, 0.137, 0.136, 0.135, 0.136, 0.138, 0.066, 0.138, 0.135, 0.123, 0.14, 0.135, 0.141, 0.135, 0.138, 0.135, 0.137, 0.128, 0.135, 0.136,  0.135, 0.138);
my @recipe_oils = ();
my @recipe_ratios = ();
my @sap_index_list = ();
my @oil_weights = ();
my $number_of_oils = 0;
my $total_oil_weight = 0;
my $superfat_ratio = 0;
my $ratio_test = 0;
my $lye_weight = 0;
my $index = 0;
my $temp = ();

                              # Main Program #

print "\n***************** Welcome to Joe and Alanna's Soap Calculator *****************\n\n";

ListOption();

OWSValidation();

OilInput();

WeightInput();

OilWeights();

Lye();

my $liquids = .33 * $total_oil_weight;   # uses common liquid to oil ratio

PrintRecipe();

SaveRecipe();

                          # Subroutine Declarations #

sub ListOption
{ # Begin ListOption()
  print STDOUT "Would you like to see the full list of oils recognized by this program(y/n)? ";
  my $ans = <STDIN>;  # user input
  chomp $ans;

  if ($ans eq 'y') {
    print "*-----------------------------FULL OIL LIST-----------------------------------*\n";
    my $size = scalar @oils;

    while ($index < $size) {    # prints index of recognized oils
      print "$oils[$index]";
      $index = $index + 1;
      print "\n";
    };
  };
  print "\n";
};  # End ListOption()


sub OWSValidation
{ # Begin OWSValidation()
  while ($number_of_oils <= 0 || $number_of_oils > 10 ) { # validates # of oils
    print STDOUT "How many oils would you like to calculate(1-10): ";
    $number_of_oils = <STDIN>;  # user input
    chomp $number_of_oils;
    print "\n";
  };

  while ($total_oil_weight <= 0) {   # validates total weight
    print STDOUT "What is the total weight in grams of oils you would like to calculate: ";
    $total_oil_weight = <STDIN>; # user input
    chomp $total_oil_weight;
    print "\n";
  };

  while ($superfat_ratio <= 0 || $superfat_ratio > 100) {  # validates suerfat
    print STDOUT "Enter a superfatting ratio (greater than 0): ";
    $superfat_ratio = <STDIN>;  # user input
    chomp $superfat_ratio;
    print "\n";
  };
};  # End OWSValidation()


sub OilInput
{ # Begin OilInput()
  $index = 1;

  while ($index <= $number_of_oils) {
    print STDOUT "Enter oil number $index: ";
    my $temp = <STDIN>;   # user input
    chomp $temp;

    if ($temp eq '') {    # blank field check
      next;
    } else {
      if ( "@oils" =~ /\b$temp\b/) {   # validates user input for oil with regex
        push @recipe_oils, $temp;      # updates @recipe_oils array
        # saves element location of corresponding @sap_ratios into new array
        push @sap_index_list, first_index { /\b$temp\b/ } @oils; #
        $index = $index + 1;
      } else {
        print "*** $temp oil not recognized ***\n";
      };
    };
  };
};  # End OilInput()


sub WeightInput
{ # Begin WeightInput()
  $index = 1;
  print "\n";

  while ($index <= $number_of_oils) {
    print STDOUT "Enter $recipe_oils[$index-1] oil's ratio in whole numbers: ";
    my $temp = <STDIN>;   # user input
    chomp $temp;

    if ($temp <= 0 || $temp > 100) {     # input validation
      print "*** Invalid Weight ***\n";
    } else {
      push @recipe_ratios, $temp;       # updates @recipe_ratios array
      $ratio_test = $ratio_test + $temp;
      $index = $index + 1;
    };
  };
  RatioTest();
};  # End WeightInput()


sub RatioTest
{ # Begin RatioTest()
  if ($ratio_test != 100) {     # ratios of oils must equal 100% to continue
    print "*** The provided ratios equal $ratio_test not 100 ***\n";
    $ratio_test = 0;
    @recipe_ratios = ();
    WeightInput();
  };
};  # End RatioTest()


sub OilWeights
{ # Begin OilWeights()
  foreach my $ratio (@recipe_ratios) {
    # calculates and stores individual weights to array
    $temp = ($ratio / 100) * $total_oil_weight;
    push @oil_weights, $temp;
  };
};  # End OilWeights()


sub Lye
{ # Begin Lye()
  $index = 0;

  foreach my $element (@sap_index_list) {
    $temp = $sap_ratios[$element] * $oil_weights[$index];
    $lye_weight = $lye_weight + $temp;      # updates accumulator
    $index = $index + 1;
  };

  $lye_weight = $lye_weight - (($superfat_ratio/100) * $lye_weight);  #superfat
  return $lye_weight    # returns accumulator
};  # End Lye()


sub PrintRecipe
{ # Begin PrintRecipe()
  $index = 0;
  my $oils_size = scalar @recipe_oils;

  # prints full recipe
  print "\n";
  while ($index < $oils_size ) {
    print "$recipe_oils[$index] oil: $oil_weights[$index] grams\n";
    $index = $index + 1;
  };
  print "Lye(sodium hydroxide): $lye_weight grams\n";
  print "liquids: $liquids grams\n";
  print "Total Weight: ", ($total_oil_weight + $lye_weight + $liquids), " grams\n";
  Resize();
};  # End PrintRecipe()


sub Resize
{ # Begin Resize()
  print STDOUT "\nWould you like to resize this recipe(y/n)? ";
  my $ans = <STDIN>;    # user input
  chomp $ans;

  if ($ans eq 'y') {    # input validation
    @oil_weights = ();  # sets necessary variables back empty or 0
    $total_oil_weight = 0;
    $lye_weight = 0;

    while ($total_oil_weight <= 0) {
      print STDOUT "What is the total weight in grams of oils you would like to calculate: ";
      $total_oil_weight = <STDIN>;    # user input
      chomp $total_oil_weight;
    };

    # recalculates recipe totals and reprints recipe
    OilWeights();
    $liquids = .33 * $total_oil_weight;
    Lye();
    PrintRecipe();
  };
};  # End Resize()


sub SaveRecipe
{ # Begin SaveRecipe()
  print STDOUT "\nWould you like to save this recipe to a text file (y/n)? ";
  my $ans = <STDIN>;    # user input
  chomp $ans;

  if ($ans eq 'y'){     # input validation
    my $file = "soap_recipes.txt";
    if (-e $file) {
      unless(open FILE, '>>'.$file) {   # appends file if it exists
        die "\nUnable to open $file\n";
      };
      print FILE "\n";
    } else {
      unless(open FILE, '>'.$file) {    # creates file if it doesn't exist
          die "\nUnable to create $file\n";
      };
    };

    print STDOUT "\nWhat would you like to call your soap recipe? ";
    $ans = <STDIN>;   # user input for title of soap recipe
    chomp $ans;
    $index = 0;
    my $oils_size = scalar @recipe_oils;

    # prints recipe to file and displays closing statement
    print FILE "***$ans***", "\n";
    while ($index < $oils_size ) {
      print FILE "$recipe_oils[$index] oil: $oil_weights[$index] grams\n";
      $index = $index + 1;
    };
    print FILE "Lye(sodium hydroxide): $lye_weight grams\n";
    print FILE "liquids: $liquids grams\n";
    print FILE "Total Weight: ", ($total_oil_weight + $lye_weight + $liquids), " grams\n";
    close FILE;
    print "\n** Your recipe has been saved to your working directory as $file! **\n";
    print "\n************* Thank You For Using Joe and Alanna's Soap Calculator *************\n\n";
  } else {
    print "\n************* Thank You For Using Joe and Alanna's Soap Calculator *************\n\n";
    exit;
  };
};  # End SaveRecipe

__END__
