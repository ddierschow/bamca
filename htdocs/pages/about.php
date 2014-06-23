<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<?php
chdir('..');
include "bin/basics.php";
include "config.php";
$pif = GetPageInfo("about");
$c = array(30, 184, 410, 146, 30);
DoHead($pif);
?>

<style type="text/css">
.horiz {height: <?php echo $c[0]; ?>px;}
.vert {width: <?php echo $c[0]; ?>px;}
.corner {height: <?php echo $c[0]; ?>px; width: <?php echo $c[0]; ?>px;}
</style>

<?php
DoPageHeader($pif);

$larr = Fetch("select url, name, description from link_line where page_id='links.others' and section_id='Labout' order by display_order", $pif);

echo '<!-- ' . array_sum($c) . '-->';

?>

<table>
 <tr>
  <td colspan="5" class="boxend"><img src="../pic/gfx/logo.gif" class="centered"></td>
 </tr>

 <tr>
  <td class="corner" style="background-image: url(../pic/gfx/box-ul.gif)"></td>
  <td class="horiz" width="<?php echo $c[1] + $c[2] + $c[3]; ?>" colspan=3></td>
  <td class="corner" style="background-image: url(../pic/gfx/box-ur.gif)"></td>
 </tr>

 <tr>
  <td width="<?php echo $c[0]; ?>" rowspan="<?php echo count($larr) * 2 + 3; ?>" background="../pic/gfx/box-v.gif">&nbsp;</td>
  <td width="<?php echo $c[1] + $c[2] + $c[3]; ?>" colspan=3 class="int" style="text-align: center; font-size: x-large; font-weight: bold;">
   Bay Area <img src="../pic/gfx/matchboxb.gif" alt="[Matchbox]" style="vertical-align: baseline;"> Collectors' Association Website</td>
  <td width="<?php echo $c[0]; ?>" rowspan="<?php echo count($larr) * 2 + 3; ?>" background="../pic/gfx/box-v.gif">&nbsp;</td>
 </tr>

 <tr>
  <td width="<?php echo $c[1] + $c[2]; ?>" colspan="2" class="int">
   Welcome to our club's website.  We have attempted to make a site that would be enjoyable and informational
   for anyone interested in Matchbox toys.  Feel free to view
   <a href="faq.html">our FAQ</a> and
   <a href="contact.html">how to contact us or join our club</a>.
  </td>
  <td width="<?php echo $c[3]; ?>" rowspan="<?php echo count($larr) * 2 + 1; ?>" class="int">
   <img src="../pic/gfx/boxmokoles.gif">
  </td>
 </tr>

<?php
foreach ($larr as $ent) {
 $nams = explode('|', $ent[1]);

 echo ' <tr><td colspan="2" class="int">&nbsp;</td></tr>
 <tr>
  <td width="' . $c[1] . '" style="text-align: center" class="int"><a href="' . $ent[0] . '"><img src="../pic/gfx/' . $nams[0] . '" alt="[' . $nams[1] . ']" border=0></a></td>
  <td width="' . $c[2] . '" class="int">' . $ent[2] . '</td>
 </tr>

';
}
?>
 <tr>
  <td colspan="3" class="int">&nbsp;<p>
   This website was created and is maintained by
   <a href="mailto:dean@xocolatl.com">Dean Dierschow</a>.  I
   have made a reasonable effort to verify information I have
   presented here, but I can't really take care of everything.
   Please send me a note if you see something here that needs fixing.
   Please don't get frustrated if it takes me a long time to take
   care of it, though, as this isn't my Real Job.<p>
   Please do not hotlink to images on this site.  We reserve the
   right to change the name, location, or contents of any image at
   any time for any reason.
  </td>
 </tr>

 <tr>
  <td height="<?php echo $c[0]; ?>" background="../pic/gfx/box-ll.gif">&nbsp;</td>
  <td colspan="3" class="horiz">&nbsp;</td>
  <td height="<?php echo $c[0]; ?>" background="../pic/gfx/box-lr.gif">&nbsp;</td>
 </tr>

 <tr>
  <td colspan="5" height="200" class="boxend"><img src="../pic/gfx/box30.gif" class="centered"></td>
 </tr>
</table>

<hr>
<div style="color:#FFFFFF;">
BAMCA is a private club and is not affiliated with Tyco Toys, Inc. or Matchbox
Toys (USA) Ltd.  Matchbox&reg; and the Matchbox logo are registered trademarks
of Matchbox International Ltd. and are used with permission.
</div>
<hr>

<table width=600 border=0>
<tr><td>
<img src="../pic/flags/au.gif" alt="Australia">
<img src="../pic/flags/at.gif" alt="Austria">
<img src="../pic/flags/be.gif" alt="Belgium">
<img src="../pic/flags/ca.gif" alt="Canada">
<img src="../pic/flags/eu.gif" alt="EC">
<img src="../pic/flags/fi.gif" alt="Finland">
<img src="../pic/flags/fr.gif" alt="France">
<img src="../pic/flags/de.gif" alt="Germany">
<img src="../pic/flags/it.gif" alt="Italy">
<img src="../pic/flags/jp.gif" alt="Japan">
<img src="../pic/flags/nl.gif" alt="Netherlands">
<img src="../pic/flags/nz.gif" alt="NewZealand">
<img src="../pic/flags/no.gif" alt="Norway">
<img src="../pic/flags/pt.gif" alt="Portugal">
<img src="../pic/flags/es.gif" alt="Spain">
<img src="../pic/flags/se.gif" alt="Sweden">
<img src="../pic/flags/gb.gif" alt="UK">
<img src="../pic/flags/us.gif" alt="USA">
</td></tr></table>

</body>
</html>
