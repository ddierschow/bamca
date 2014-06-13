<html>
<?php
/* Release 5.0 published Sunday, 11 July 2010 at 12:01 AM PDT */
/* Release 5.1 published Monday, 12 April 2011 at 12:01 AM PDT */
/* Release 5.2 published Monday, 16 May 2011 at 12:01 AM PDT */
/* Release 5.3 published Monday, 01 August 2011 at 12:01 AM PDT */
/* Release 5.4 published Monday, 07 September 2011 at 12:01 AM PDT */
include "bin/basics.php";
include "config.php";
include "version.txt";
$pif = GetPageInfo("stuff");
$pif['title'] .= ' ' . $version;
DoHead($pif);
DoPageHeader($pif);

$retval = CheckPerm('a');
if (!$retval)
{
?> 

<script type="text/javascript">
<!--
window.location = "https://<?php echo $pif['host']; ?>/cgi-bin/login.cgi?dest=http://<?php echo $pif['host']; ?>/stuff.php";
//document.write("dumpout!");
//-->
</script>

<?php
}
else
{
?>

<table width=100% cellpadding=0 cellspacing=0>

<tr><td colspan=7 background="pic/gfx/red4x4.gif"><img src="pic/gfx/red4x4.gif"></td></tr>

<tr>
<td background="pic/gfx/red4x4.gif" width=4><img src="pic/gfx/red4x4.gif"></td>
<td width=19% valign=top>
<h3><ul>
<li><a href="index.php">index</a>
<li><a href="pages/about.php">about</a>
<li><a href="pages/contact.html">contact</a>
<li><a href="pages/faq.html">faq</a>
    <a href="new/txt/faqnew.html">new</a>
<li><a href="cgi-bin/compare.cgi">compare</a>
<li><a href="pages/mbhistory.html">mbhistory</a>
<li><a href="cgi-bin/biblio.cgi?page=bayarea">bayarea</a>
<li><a href="cgi-bin/biblio.cgi?page=biblio">biblio</a>
<li><a href="cgi-bin/calendar.cgi">calendar</a>
<li><a href="cgi-bin/package.cgi?page=blister">blister</a>
<li><a href="pic/box/">box</a>
</ul></h3>
</td>

<td width=19% valign=top>
<h3><ul>
<li><a href="cgi-bin/links.cgi">toylinks</a>
<li><a href="cgi-bin/links.cgi?page=dealers">dealers</a>
<li><a href="cgi-bin/links.cgi?page=mailorder">mailorder</a>
<li><a href="cgi-bin/links.cgi?page=manuf">manuf</a>
<li><a href="cgi-bin/links.cgi?page=clubs">clubs</a>
<li><a href="cgi-bin/addlink.cgi">addlink</a>
<li><a href="cgi-bin/links.cgi?page=rejects">rejects</a>
<li><a href="ads/">ads</a>
<li><a href="errors/">errors</a>
<li><a href="pages/">pages</a>
<li><a href="pages/glossary.html">glossary</a>
</ul></h3>
</td>

<td width=19% valign=top>
<h3><ul>
<li><a href="models.html">models</a>
<li><a href="cgi-bin/matrix.cgi">series</a>
<li><a href="pages/other.html">other</a>
<li><a href="cgi-bin/sets.cgi">sets</a>
<li><a href="cgi-bin/lineup.cgi">lineups</a>
<li><a href="cgi-bin/upload.cgi">upload</a>
<li><a href="cgi-bin/packs.cgi">packs</a>
<br>&nbsp;
<li><a href="database.php"><font size="+2">database</font></a>
</ul></h3>
</td>

<td width=19% valign=top>
<h3><ul>
<li><a href="lesney/">lesney</a>
<li><a href="man/">175</a>
<li><a href="cat/">cat</a>
<br>&nbsp;
<li><a href="cgi-bin/manno.cgi">manno</a>
    <a href="cgi-bin/manno.cgi?page=manls">ls</a>
<li><a href="cgi-bin/mack.cgi">mack</a>
<li><a href="cgi-bin/makes.cgi">makes</a>
</ul></h3>
</td>

<td width=24% valign=top bgcolor="#EEEEEE">
<h3><ul>
<li><a href="cgi-bin/traverse.cgi">traverse</a>
    <a href="cgi-bin/traverse.cgi?d=./tb">tb</a>
<li><a href="cgi-bin/editor.cgi">editor</a>
    <a href="cgi-bin/mass.cgi">mass</a>
<li><a href="cgi-bin/edlinks.cgi">links</a>
    <a href="cgi-bin/links.cgi?page=others&section=private">other</a>
<li><a href="cgi-bin/roam.cgi">roam</a>
<li><a href="cgi-bin/vedit.cgi">vedit</a>
    <a href="cgi-bin/vedit.cgi?d=src/vdat">dat</a>
    <a href="http://www.mbxforum.com/11-Catalogs/02-MB75/MB75-Documents/?C=M;O=D">docs</a>
<li><a href="cgi-bin/xbits.cgi">bits</a>
<li><a href="cgi-bin/stitch.cgi">stitch</a>
<li><a href="pic/flags/all.html">flags</a>
    <a href="pic/flags/iso">iso</a>
<li><a href="cgi-bin/xcars.cgi">cars</a>
    <a href="cgi-bin/tomica.cgi">tomica</a>
<li><a href="cgi-bin/sets.cgi?page=mine1&noignore=1">mine1</a>
    <a href="cgi-bin/sets.cgi?page=mine2&noignore=1">2</a>
    <a href="cgi-bin/sets.cgi?page=mine3&noignore=1">3</a>
<li><a href="cgi-bin/activity.cgi">activity</a>
</ul></h3>
</td>

<td background="pic/gfx/red4x4.gif" width=4><img src="pic/gfx/red4x4.gif"></td>
</tr>

<tr>
<td background="pic/gfx/red4x4.gif"><img src="pic/gfx/red4x4.gif"></td>

<td colspan=5 bgcolor="#DDFFDD"><center><b>
<?php
if ($pif['isbeta'])
    DoButtonLink('release', $imgdirArt, "http://www.bamca.org/stuff.php");
else
    DoButtonLink('beta', $imgdirArt, "http://beta.bamca.org/stuff.php");
DoButtonLink('log_in', $imgdirArt, "https://" . $pif['host'] . "/cgi-bin/login.cgi?dest=http://" . $pif['host'] . "/stuff.php");
DoButtonLink('log_out', $imgdirArt, "https://" . $pif['host'] . "/cgi-bin/logout.cgi");
DoButtonLink('change_password', $imgdirArt, "https://" . $pif['host'] . "/cgi-bin/chpass.cgi?dest=http://" . $pif['host'] . "/stuff.php");
DoButtonLink('register', $imgdirArt, "https://" . $pif['host'] . "/cgi-bin/signup.cgi?dest=http://" . $pif['host'] . "/stuff.php");
DoButtonLink('user_list', $imgdirArt, "https://" . $pif['host'] . "/cgi-bin/user.cgi");
DoButtonLink('test', $imgdirArt, "cgi-bin/xtest.cgi");
DoButtonLink('counters', $imgdirArt, "http://" . $pif['host'] . "/cgi-bin/counters.cgi");
?>

</b></center></td>

<td background="pic/gfx/red4x4.gif"><img src="pic/gfx/red4x4.gif"></td>
</tr>

<tr>
<td background="pic/gfx/red4x4.gif"><img src="pic/gfx/red4x4.gif"></td>
<td colspan=5><center><i>
<a href="http://vzone.virgin.net/sizzling.jalfrezi/">HTML</a> -
<a href="http://www.python.org/">python</a> -
<a href="http://www.areh.de/">AREH</a> -
<a href="http://www.mboxcommunity.com/cfalkens/">CF</a> -
<a href="http://matchbox.zsebehazy.com/">Dan</a> -
<a href="http://mb-db.co.uk/">MBDB</a> -
<a href="http://www.midlandsdiecast.com/col_mbxno.asp">MD</a> -
<a href="http://www.mbxforum.com/">MBXF</a> -
<a href="http://www.mboxcommunity.com/forums/">MCCH</a> -
<a href="http://www.hobbytalk.com/bbs1/forumdisplay.php?f=200">HT</a> -
<a href="http://bbs.52mbx.com/">52</a> -
<a href="http://search.ebay.com/ws/search/AdvSearch?sofocus=bs&satitle=&sacat=-1&catref=C5&from=R7&nojspr=y&fts=2&fsop=1&fsoo=1&fcl=3&frpp=50&sofindtype=1&pfid=">eBay</a> -
<a href="http://www.liveauctioneers.com/">LA</a> -
<a href="http://www.mercadolibre.com/">ML</a> -
<a href="http://www.taobao.com/">TB</a> -
<a href="http://www.publicsafetydiecast.com/Matchbox_MAN.htm">PSDC</a> -
<a href="http://www.vectis.co.uk/">Vectis</a>
</i></center></td>
<td background="pic/gfx/red4x4.gif"><img src="pic/gfx/red4x4.gif"></td>
</tr>

<tr><td colspan=7 background="pic/gfx/red4x4.gif"><img src="pic/gfx/red4x4.gif"></td></tr>
<tr><td bgcolor="#CCCCCC" colspan=7>&nbsp;</td></tr>
<tr><td colspan=7 background="pic/gfx/red4x4.gif"><img src="pic/gfx/red4x4.gif"></td></tr>
<tr>
<td background="pic/gfx/red4x4.gif"><img src="pic/gfx/red4x4.gif"></td>
<td colspan=5>
<table><tr><td>
<?php
$result = Fetch("select id,health from page_info where not health=0", $pif);
echo 'Errors found:</td><td><span class="warning">';
if (count($result) > 0)
{
    $errcounter = 0;
    foreach ($result as $ent)
	$errcounter = $errcounter + $ent[1];
    echo $errcounter . ' ';
}
echo "</span></td>";
echo '<td><span class="warning">';
DoButtonLink('see', $imgdirArt, "cgi-bin/editor.cgi");
DoButtonLink('clear', $imgdirArt, "cgi-bin/editor.cgi?clear=1");
if (count($result) > 0)
{
    foreach ($result as $ent)
	echo ' ' . $ent[0] . ' (' . $ent[1] . ')';
}
echo "</span></td>";
echo "</tr><tr><td>\n";

$result = Fetch("select name from user where state=1 and privs=''", $pif);
echo "New users:</td><td>";
echo '<span class="warning">';
if (count($result) > 0)
{
    foreach ($result as $ent)
	echo $ent[0] . ' ';
}
echo "</span></td><td>";
DoButtonLink('see', $imgdirArt, "https://" . $pif['host'] . "/cgi-bin/user.cgi");
echo "</td></tr><tr><td>\n";

$result = Fetch("select count(*) from link_line where ((flags&1)=1)", $pif);
echo 'New links:</td><td><span class="warning">';
if ($result[0][0])
    echo $result[0][0];
echo "</span></td><td>";
DoButtonLink('see', $imgdirArt, "cgi-bin/edlinks.cgi?sec=new");
echo "</td></tr><tr><td>\n";

$pf = glob("submitted/*");
echo 'New images:</td><td><span class="warning">';
if (count($pf) - 1)
    echo (count($pf) - 1);
echo "</span></td><td>";
DoButtonLink('see', $imgdirArt, "cgi-bin/traverse.cgi?d=./submitted");
echo "</td></tr><tr><td>\n";

$pf = glob("tb/comment.*");
echo 'New comments:</td><td><span class="warning">';
if (count($pf))
    echo count($pf);
echo "</span></td><td>";
DoButtonLink('see', $imgdirArt, "cgi-bin/traverse.cgi?d=./tb");
echo "</td></tr>\n";

?>
</table>
</td>
<td background="pic/gfx/red4x4.gif"><img src="pic/gfx/red4x4.gif"></td>
</tr>
<tr><td colspan=7 background="pic/gfx/red4x4.gif"><img src="pic/gfx/red4x4.gif"></td></tr>

</table>

<?php
}

DoPageFooter($pif);
?>
<img src="pic/gfx/hruler.gif">

</body>
</html>
