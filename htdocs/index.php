<!DOCTYPE html>
<html>
<?php
include "bin/basics.php";
include "config.php";
$pif = GetPageInfo("index");
$is_logged_in = CheckPerm('b');
DoHead($pif);
DoPageHeader($pif);
?> 

<div id="fb-root"></div>
<script>(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = 'https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.12';
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));</script>

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
<h2>Information about BAMCA, the Bay Area Matchbox Collectors Association</h2>
 <ul>
 <li><a href="/pages/faq.php">The BAMCA <b>FAQ</b></a>
 <li><a href="/pages/contact.html">How to <b>Contact</b> or join BAMCA</a>
 <li><a href="/pages/about.php"><b>About</b> This Website</a>
 <li><a href="/pages/club.php"><b>History</b> of BAMCA</a>
<?php
if ($is_logged_in) {
?>
 <li><a href="/cgi-bin/calendar.cgi">The BAMCA <b>Calendar</b></a>
 <li><a href="/cgi-bin/biblio.cgi?page=bayarea">A list of places to find die-cast in the <b>Bay Area</b></a>
 </ul>

<h2>Information about Matchbox Toys</h2>
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

<h2>Other Toy Information</h2>
 <ul>
 <li><a href="/pages/glossary.php">A <b>Glossary</b> of Toy Collecting Terms</a>
 <li><a href="/cgi-bin/biblio.cgi">A <b>Bibliography</b> of Toy Collecting Books</a>
 <li><a href="/cgi-bin/links.cgi?page=clubs">Information on <b>Other</b> Clubs</a>
 <li><a href="/cgi-bin/links.cgi">Dean's Awesome Toy <b>Links</b> Pages</a> -
     <a href="/cgi-bin/addlink.cgi"><b>Suggest</b> a Link!</a>
 </ul>
</td></tr></table>
<?php
} else {
?>
 </ul>
</td></tr></table>

<div class="login_or_register">
To discover more about Matchbox Toys, you will have to be a member of this website.<br><br>
You may
<?php DoTextButtonLink('log_in', "https://" . $pif['host'] . "/cgi-bin/login.cgi"); ?>
or
<?php DoTextButtonLink('register', "https://" . $pif['host'] . "/cgi-bin/signup.cgi"); ?>
.
</div>
<?php
}
?>

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

if ($is_logged_in) {
?> 
<br>

<div class="status">
<a href="/pages/status.php">Status of the Website</a>
</div>
<?php } ?>

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
<center><?php DoTextButtonLink('comment on<br>this page', "pages/comment.php?page==index"); ?></center>
</td></tr></table>
<p>
<table class="loginbar" width=1024><tr><td>
<div class="textbutton fb-like" data-href="http://facebook.com/pages/Bay-Area-Matchbox-Collectors-Association/106213056100271" data-width="100" data-layout="button_count" data-action="like" data-size="small" data-show-faces="false" data-share="false"></div>
<a href="http://facebook.com/pages/Bay-Area-Matchbox-Collectors-Association/106213056100271"><div class="textbutton facebook"><i class="fab fa-facebook-square"></i> FACEBOOK</div></a>
<a name="fb_share" type="button" class="textbutton facebook" href="http://www.facebook.com/sharer.php">Share</a><script src="http://static.ak.fbcdn.net/connect.php/js/FB.Share" type="text/javascript"></script>
<a href="/pages/faq.php"><div class="textbutton see_the_faq"><i class="fas fa-question-circle"></i> SEE THE FAQ</div></a>
<a href="http://blog.bamca.org/"><div class="textbutton"><i class="fab fa-blogger"></i> BLOG</div></a>
<?php if ($is_logged_in) { ?>
<a href="http://bamca.tumblr.com/"><div class="textbutton"><i class="fab fa-tumblr-square"></i> TUMBLR</div></a>
<a href="/pages/status.php"><div class="textbutton site_status"><i class="fas fa-clipboard-list"></i> SITE STATUS</div></a>
<?php } ?>
</td></tr></table>

<?php
DoPageFooter($pif);
DoFoot($pif);
?>
</html>
