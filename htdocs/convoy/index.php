<!DOCTYPE html>
<html>
<?php
chdir('..');
include "bin/basics.php";
include "config.php";
include "subs.php";
$pif = GetPageInfo("convoy");
$desc = 'Index';
$pif['title'] = $pif['title'] . ' - ' . $desc;
DoHead($pif);
?>
  <meta name="author" content="John Baum and Dean Dierschow">
  <meta name="description" content="<?php echo $desc; ?>">
<?php
DoPageHeader($pif);
?>

<div class="cyindex">
  <span class="ititle"><img alt="" src="/pic/convoy/banner.jpg"><br>
  The Matchbox Convoy Project</span>
  <p>
    Welcome to our site. The Matchbox Convoy Project is an effort to compile
    and list the models and variations of the truck and trailer combinations
    made under the Matchbox name in the 1:72 or smaller scale. This is a
    combined volunteer effort of dedicated collectors throughout the world,
    and is intended to be used as a reference site for other collectors.
  <p>
  <span class="iwarn">
    This site is a work in progress, and will be updated as new models and variations are found and issued.
  </span><p>
  <span class="iimportant">
    This site deals mainly with code 1 models (factory issued) <br>
    There are a few code 2 and 3 models shown, but they are far too many others out there to try and index here.<br>
  </span>

  <hr size="2" width="100%"> 

  <table class="itable">
    <tbody>
      <tr>
	<td colspan="4">
	  <b><font face="Arial" size="+1">The Basics </font></b><br>
	  <font face="Arial">What you need to know and how to speak the language.</font>
	</td>
      </tr>
      <tr>
	<td align="center" valign="middle" width="180">
	  <b><a href="cabs.php">Truck Cabs </a></b>
	</td>
	<td align="center" valign="middle" width="240" colspan="2">
	  <a href="definitions.php"><b>Basic Information &amp;<br>Definitions</b></a>
	</td>
	<td align="center" valign="middle" width="180">
	  <b><a href="trailer.php">Trailers </a></b>
	</td>
      </tr>
      <tr>
	<td colspan="4" align="center" valign="middle" width="200">
	  <b><font face="Arial" size="+2"><font size="+1">The Guts</font></font></b><br>
	  <font face="Arial">This is where we have the models posted</font>
	</td>
      </tr>
      <tr>
	<td align="center" valign="middle" width="300" colspan="2">
	  <b><a href="series.php"><b>Convoy Index</b></a><br> by tractor/trailer</b>
	</td>
	<!--<td align="center" valign="middle" width="200" colspan="2">
	  <b><b><a href="year.php"><b>Convoy Index</b></a><br> by year</b></b>
	</td>-->
	<td align="center" valign="middle" width="300" colspan="2">
	  <a href="ids.php" style="font-weight: bold">Convoy Index </a><br>
	  <span style="font-weight: bold">by ID</span>
	</td>
      </tr>
      <tr>
	<td colspan="4" align="center" valign="middle">
	  <b><font face="Arial" size="+2"><font size="+1">More Info</font></font></b><br>
	  A few things that will help you understand the current state of these pages
	</td>
      </tr>
      <tr>
	<td align="center" valign="middle" width="300" colspan="2">
	  <b><a href="updates.php"><b>Updates</b></a></b><br>The history of these pages
	</td>
	<td align="center" valign="middle" width="300" colspan="2">
	  <a href="TODO.php" style="font-weight: bold">Not Covered </a><br>Some of the things not yet documented
	</td>
      </tr>
    </tbody>
  </table>
      
  <hr size="2" width="100%">
  <span class="iimportant">These pages last updated June, 2017</span>
  <hr size="2" width="100%">
  <span class="iimportant">As of June 2017, this project has become part of the BAMCA site.  Over time it will be merged into the BAMCA database.</span>
  <hr size="2" width="100%">

      <div class="disclaim">
The Matchbox Convoy Project was originall established on November 28, 2003.
This web site is a noncommercial educational site and has no official relationship to
Matchbox or Mattel Inc., the current owner of the Matchbox brand.
All comments, or questions should be addressed to <a href="mailto:staff@bamca.org">staff@bamca.org</a><p>
<i>Life is too short not to play with toys.</i>
      </div>
    </div>
  </body>
</html>
