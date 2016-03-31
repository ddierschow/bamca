<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<?php
include "bin/basics.php";
include "config.php";
$pif = GetPageInfo("index");
DoHead($pif);
DoPageHeader($pif);
?> 

<table width="1024">
<tr><td colspan=4 width=1024>
<img src="pic/gfx/bamca-banner.gif">
</td></tr>

<tr><td width="50">&nbsp;</td>
<td valign="top">

<?php include "announce.php";?>

<ul>
<li>Information about BAMCA, the Bay Area Matchbox Collectors Association
 <ul>
 <li><a href="pages/faq.html">The BAMCA <b>FAQ</b></a>
 <li><a href="pages/contact.html">How to <b>Contact</b> or join BAMCA</a>
 <li><a href="pages/about.php"><b>About</b> This Website</a>
 <li><a href="cgi-bin/calendar.cgi">The BAMCA <b>Calendar</b></a>
 <li><a href="cgi-bin/biblio.cgi?page=bayarea">A list of places to find die-cast in the <b>Bay Area</b></a>
 </ul>

<li>Information about Matchbox Toys
 <ul>
 <li><span style="border-width: 1px; border-style: solid; padding: 4px 8px 2px 8px;"><a href="database.php">Matchbox Model <span style="font-size: x-large; font-weight: bold;">Database</span></a></span>
 <li><a href="models.html">Matchbox <b>Model</b> Pages for all ranges
 <li><a href="pic/ads/">Matchbox <b>Advertisements</b> from over the years</a>
 <li><a href="cgi-bin/errors.cgi">Matchbox <b>Errors</b> in packaging and manufacturing</a>
 <li><a href="cgi-bin/boxart.cgi">Matchbox <b>Box</b> Art</a>
 <li><a href="cgi-bin/package.cgi?page=blister">Matchbox <b>Blister</b> Packs</a>
 <li><a href="pages/mbhistory.html"><b>History</b> of Matchbox</a>
 </ul>

<li>Other Toy Information
 <ul>
 <li><a href="pages/glossary.html">A <b>Glossary</b> of Toy Collecting Terms</a>
 <li><a href="cgi-bin/biblio.cgi">A <b>Bibliography</b> of Toy Collecting Books</a>
 <li><a href="cgi-bin/links.cgi?page=clubs">Information on <b>Other</b> Clubs</a>
 <li><a href="cgi-bin/links.cgi">Dean's Awesome Toy <b>Links</b> Pages</a> -
     <a href="cgi-bin/addlink.cgi"><b>Suggest</b> a Link!</a>
 </ul>
</ul>

</td>
<td width="50">&nbsp;</td>
<td width="200" valign="top">

<?php
$pf = array_merge(glob($IMG_DIR_MAN . "/s_*.jpg"), glob($IMG_DIR_MAN . "/var/s_*.jpg"), glob($IMG_DIR_BOX . "/s_*.jpg"));
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
Matchbox® and the Matchbox logo are registered trademarks
of Matchbox International Ltd. and are used with permission.
</font></center>
</td></tr></table></center>
</td><td>
<a href="pages/comment.php?page=index"><img src="pic/gfx/but_comment_on_this_page.gif" alt="COMMENT" onmouseover="this.src='pic/gfx/hov_comment_on_this_page.gif';" onmouseout="this.src='pic/gfx/but_comment_on_this_page.gif';" class="comment"></a>
</td></tr></table>
<p>
<table class="loginbar" width=1024><tr><td>
<iframe src="http://www.facebook.com/plugins/like.php?href=http%3A%2F%2Fwww.bamca.org%2F&amp;layout=button_count&amp;show_faces=false&amp;width=100&amp;action=like&amp;font=arial&amp;colorscheme=light&amp;height=24" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:90px; height:24px; vertical-align: middle;" allowTransparency="true"></iframe>
<a name="fb_share" type="button" href="http://www.facebook.com/sharer.php">Share</a><script src="http://static.ak.fbcdn.net/connect.php/js/FB.Share" type="text/javascript"></script>
<a href="http://facebook.com/pages/Bay-Area-Matchbox-Collectors-Association/106213056100271"><img src="pic/gfx/fb_visit.gif" border="0" /></a>
<a href="pages/faq.html"><img src="pic/gfx/but_see_the_faq.gif" alt="SEE THE FAQ" onmouseover="this.src='pic/gfx/hov_see_the_faq.gif';" onmouseout="this.src='pic/gfx/but_see_the_faq.gif';"></a>
</td></tr></table>

<?php
DoPageFooter($pif);
?>

</body>
</html>
