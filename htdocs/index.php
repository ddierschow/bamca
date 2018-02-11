<!DOCTYPE html>
<html>
<?php
include "bin/basics.php";
include "config.php";
$pif = GetPageInfo("index");
DoHead($pif);
DoPageHeader($pif);
?> 

<table width="1024" class="banner">
<tr><td class="bannercell" width="406">
<img src="/pic/gfx/bamcabay.gif">
</td>
<td class="bannercell">
<center><img src="/pic/gfx/bannertitle.gif"></center>
</td></tr>
</table>

<table width="1024">
<tr><td width="50">&nbsp;</td>
<td valign="top">

<?php include "announce.php";?>

<table class="index"><tr><td>
<ul>
<li>Information about BAMCA, the Bay Area Matchbox Collectors Association
 <ul>
 <li><a href="/pages/faq.php">The BAMCA <b>FAQ</b></a>
 <li><a href="/pages/contact.html">How to <b>Contact</b> or join BAMCA</a>
 <li><a href="/pages/about.php"><b>About</b> This Website</a>
 <li><a href="/pages/club.php"><b>History</b> of BAMCA</a>
 <li><a href="/cgi-bin/calendar.cgi">The BAMCA <b>Calendar</b></a>
 <li><a href="/cgi-bin/biblio.cgi?page=bayarea">A list of places to find die-cast in the <b>Bay Area</b></a>
 </ul>

<li>Information about Matchbox Toys
 <ul>
 <li style="margin: 3px 0 3px 0"><a class="database" href="/database.php">Matchbox Model <b>Database</b></a>
 <li><a href="/pages/lsm.php">Matchbox Model Pages for <b>Large Scale</b> Ranges
 <li><a href="/convoy/">Matchbox <b>Convoy</b> Project
 <li><a href="/cgi-bin/ads.cgi">Matchbox <b>Advertisements</b> from over the years</a>
 <li><a href="/cgi-bin/errors.cgi">Matchbox <b>Errors</b> in packaging and manufacturing</a>
 <li><a href="/cgi-bin/boxart.cgi">Matchbox <b>Box</b> Art</a>
 <li><a href="/cgi-bin/package.cgi?page=blister">Matchbox <b>Blister</b> Packs</a>
 <li><a href="/pages/mbhistory.html"><b>History</b> of Matchbox</a>
 </ul>

<li>Other Toy Information
 <ul>
 <li><a href="/pages/glossary.php">A <b>Glossary</b> of Toy Collecting Terms</a>
 <li><a href="/cgi-bin/biblio.cgi">A <b>Bibliography</b> of Toy Collecting Books</a>
 <li><a href="/cgi-bin/links.cgi?page=clubs">Information on <b>Other</b> Clubs</a>
 <li><a href="/cgi-bin/links.cgi">Dean's Awesome Toy <b>Links</b> Pages</a> -
     <a href="/cgi-bin/addlink.cgi"><b>Suggest</b> a Link!</a>
 </ul>
</ul>
</td></tr></table>

</td>
<td width="50">&nbsp;</td>
<td width="200" valign="top">

<?php
$pf = array_merge(glob('.' . $IMG_DIR_MAN . "/s_*.jpg"), glob('.' . $IMG_DIR_MAN . "/var/s_*.jpg"), glob('.' . $IMG_DIR_BOX . "/s_*.jpg"));
$pics = array_rand($pf, 3);
foreach ($pics as $r)
    echo '<img src="' . $pf[$r] . '" vspace="8">
';
echo '<br><center>3 of ' . count($pf) . " pictures</center>\n";
?> 

</td>
</tr>

<tr><td colspan=3>
<center><table bgcolor="#000000" border=1 width=100% height=64><tr><td>
<center><font color=#FFFFFF>
BAMCA is a private club and is not affiliated with Tyco Toys, Inc. or
Matchbox Toys (USA) Ltd.<br>
Matchbox&reg; and the Matchbox logo are registered trademarks
of Matchbox International Ltd. and are used with permission.
</font></center>
</td></tr></table></center>
</td><td>
<?php DoTextButtonLink('comment on<br>this page', "pages/comment.php?page==index"); ?>
</td></tr></table>
<p>
<table class="loginbar" width=1024><tr><td>
<iframe src="http://www.facebook.com/plugins/like.php?href=http%3A%2F%2Fwww.bamca.org%2F&amp;layout=button_count&amp;show_faces=false&amp;width=100&amp;action=like&amp;font=arial&amp;colorscheme=light&amp;height=24" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:90px; height:24px; vertical-align: middle;" allowTransparency="true"></iframe>
<a name="fb_share" type="button" class="textbutton share" href="http://www.facebook.com/sharer.php">Share</a><script src="http://static.ak.fbcdn.net/connect.php/js/FB.Share" type="text/javascript"></script>
<a href="http://facebook.com/pages/Bay-Area-Matchbox-Collectors-Association/106213056100271"><img src="/pic/gfx/fb_visit.gif" border="0" /></a>
<?php DoTextButtonLink('see_the_faq', "/pages/faq.php", "textbutton see_the_faq"); ?>
</td></tr></table>

<?php
DoPageFooter($pif);
DoFoot($pif);
?>
</html>
