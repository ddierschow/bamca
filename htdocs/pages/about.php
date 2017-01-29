<!DOCTYPE html>
<html>
<?php
chdir('..');
include "bin/basics.php";
include "config.php";
$pif = GetPageInfo("about");
DoHead($pif);
DoPageHeader($pif);

$larr = Fetch("select url, name, description from link_line where page_id='links.others' and section_id='Labout' order by display_order", $pif);
$rows = count($larr);
?>

<br>
<table>
 <tr>
  <td colspan="5" class="boxend boxtop"></td>
 </tr>

 <tr>
  <td class="boxul"></td>
  <td class="boxhs" colspan=3></td>
  <td class="boxur"></td>
 </tr>

 <tr>
  <td rowspan="<?php echo $rows + 3; ?>" class="boxvs"></td>
  <td colspan="3" class="boxin boxtitle">
   Bay Area <img src="<?php echo $IMG_DIR_ART; ?>/matchboxb.gif" alt="[Matchbox]" style="vertical-align: baseline;"> Collectors' Association Website</td>
  <td rowspan="<?php echo $rows + 3; ?>" class="boxvs"></td>
 </tr>

 <tr>
  <td colspan="2" class="boxin">
   Welcome to our club's website.  We have attempted to make a site that would be enjoyable and informational
   for anyone interested in Matchbox toys.  Feel free to view
   <a href="faq.php">our FAQ</a> and
   <a href="contact.html">how to contact us or join our club</a>.
  </td>
  <td class="boxin c3" rowspan="<?php echo $rows + 2; ?>"></td>
 </tr>

<?php
foreach ($larr as $ent) {
 $nams = explode('|', $ent[1]);

 echo ' <tr>
  <td class="c1 boxin boxrow"><a href="' . $ent[0] . '"><img src="' . $IMG_DIR_ART . '/' . $nams[0] . '" alt="[' . $nams[1] . ']"></a></td>
  <td class="c2 boxin">' . $ent[2] . '</td>
 </tr>

';
}
?>
 <tr>
  <td colspan="2" class="boxin"><br>
   This website was created and is maintained by
   <a href="mailto:dean@xocolatl.com">Dean Dierschow</a>.  I
   have made a reasonable effort to verify information I have
   presented here, but I can't really take care of everything.
   Feel free to send me a note if you see something here that needs fixing.
   Please don't get frustrated if it takes me a long time to take
   care of it, though, as this isn't my Real Job.<p>

   Please do not hotlink to images on this site.  We reserve the
   right to change the name, location, or contents of any image at
   any time for any reason.
  </td>
 </tr>

 <tr>
  <td class="boxll"></td>
  <td class="boxhs" colspan="3"></td>
  <td class="boxlr"></td>
 </tr>

 <tr>
  <td colspan="5" class="boxend boxbottom"></td>
 </tr>
</table>

<hr>
<div class="black">
BAMCA is a private club and is not affiliated with Tyco Toys, Inc. or Matchbox
Toys (USA) Ltd.  Matchbox&reg; and the Matchbox logo are registered trademarks
of Matchbox International Ltd. and are used with permission.
</div>
<hr>

<img src="/pic/flags/au.gif" alt="Australia">
<img src="/pic/flags/at.gif" alt="Austria">
<img src="/pic/flags/be.gif" alt="Belgium">
<img src="/pic/flags/ca.gif" alt="Canada">
<img src="/pic/flags/eu.gif" alt="EC">
<img src="/pic/flags/fi.gif" alt="Finland">
<img src="/pic/flags/fr.gif" alt="France">
<img src="/pic/flags/de.gif" alt="Germany">
<img src="/pic/flags/it.gif" alt="Italy">
<img src="/pic/flags/jp.gif" alt="Japan">
<img src="/pic/flags/nl.gif" alt="Netherlands">
<img src="/pic/flags/nz.gif" alt="NewZealand">
<img src="/pic/flags/no.gif" alt="Norway">
<img src="/pic/flags/pt.gif" alt="Portugal">
<img src="/pic/flags/es.gif" alt="Spain">
<img src="/pic/flags/se.gif" alt="Sweden">
<img src="/pic/flags/gb.gif" alt="UK">
<img src="/pic/flags/us.gif" alt="USA">

</body>
</html>
