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
   Bay Area <img src="<?php echo $IMG_DIR_ICON; ?>/a_matchboxb.gif" alt="[Matchbox]" class="mblogo"> Collectors' Association Website</td>
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
 $nams = explode('|', $ent['name']);

 echo ' <tr>
  <td class="c1 boxin boxrow"><a href="' . $ent['url'] . '"><img src="' . $IMG_DIR_ICON . '/a_' . $nams[0] . '" alt="[' . $nams[1] . ']"></a></td>
  <td class="c2 boxin">' . $ent['description'] . '</td>
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
   any time for any reason.<p>

   This site is 100% a volunteer effort.  It was created by the members
   of the club, and has never spent money on web development or programming.
   Instead, we've done all of this ourselves, in our spare time.
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

<?php include "pages/credits.php"; ?>

<hr>

<div class="infopanel">
If you'd like to know about the current status of the website, or how to contribute, please look at our <a href="status.php">status page</a>.
If you'd like to find out more about the history of the club and the website, look at the <a href="club.php">club history page</a>.
Feel free to check out our <a href="http://blog.bamca.org/">blog</a>,
our <a href="http://bamca.tumblr.com/">Tumblr</a>,
and our <a href="https://www.facebook.com/Bay-Area-Matchbox-Collectors-Association-BAMCA-106213056100271/">FaceBook page</a>.
And, we do have a <a href="faq.php">Frequently Asked Questions</a> page available as well.
</div>

<hr>

<img src="/pic/flags/au.gif" alt="Australia" label="Australia">
<img src="/pic/flags/at.gif" alt="Austria" label="Austria">
<img src="/pic/flags/be.gif" alt="Belgium" label="Belgium">
<img src="/pic/flags/ca.gif" alt="Canada" label="Canada">
<img src="/pic/flags/eu.gif" alt="EC" label="EC">
<img src="/pic/flags/fi.gif" alt="Finland" label="Finland">
<img src="/pic/flags/fr.gif" alt="France" label="France">
<img src="/pic/flags/de.gif" alt="Germany" label="Germany">
<img src="/pic/flags/it.gif" alt="Italy" label="Italy">
<img src="/pic/flags/jp.gif" alt="Japan" label="Japan">
<img src="/pic/flags/nl.gif" alt="Netherlands" label="Netherlands">
<img src="/pic/flags/nz.gif" alt="NewZealand" label="NewZealand">
<img src="/pic/flags/no.gif" alt="Norway" label="Norway">
<img src="/pic/flags/pt.gif" alt="Portugal" label="Portugal">
<img src="/pic/flags/es.gif" alt="Spain" label="Spain">
<img src="/pic/flags/se.gif" alt="Sweden" label="Sweden">
<img src="/pic/flags/gb.gif" alt="UK" label="UK">
<img src="/pic/flags/us.gif" alt="USA" label="USA">

<?php
DoButtonComment($pif);
DoFoot($pif); ?>
</html>
