<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<?php
include "bin/basics.php";
include "config.php";
$pif = GetPageInfo("database");
DoHead($pif);
$isadmin = CheckPerm('a');
$pif['hier'][0] = array('/', 'Home');
$pif['hier'][1] = array('/database.php', 'Database');
if ($pif['fake'])
{
    $yearstart = 1953;
    $yearend = 2011;
}
else
{
    $answer = Fetch("select min(year), max(year) from lineup_model", $pif);
    $yearstart = $answer[0][0];
    $yearend = $answer[0][1];
}

function SelectYear($name, $id, $defval, $min, $max)
{
    echo '<select name="' . $name . '" id="' . $id . '">' . "\n";
    $yr = $max;
    while ($yr >= $min)
    {
	$sel = '';
	if ($yr == $defval)
	    $sel = ' selected';
	echo ' <option value="' . $yr . '"' . $sel . '>' . $yr . "</option>\n";
	$yr = $yr - 1;
    }
    echo "</select><br>\n";
    incrsel($id, -1);
    echo "<br>\n";
}

DoResetJavascript();
DoIncDecJavascript();
DoPageHeader($pif);
echo "<!-- done page header -->";

function SectionHeader($sect, $cgi, $title)
{
    echo "
<tr><td><br></td></tr>
<tr><td class=\"" . $sect . "_head sel_head\">
<a name=\"" . $sect . "\"></a>
<center><h2>" . $title . "</h2></center>
</td></tr>
<tr><td class=\"spacer\"></td></tr>

<tr><td class=\"" . $sect . "_body sel_body\">
Select what kind of Matchbox lineup you would like, then click \"SEE THE MODELS\".<p>

<form action=\"/cgi-bin/" . $cgi . "\" method=\"get\" name=\"" . $sect . "\">
";
}

function SectionTail($sect)
{
    echo "<br>\n";
    //echo '<input type="image" name="submit" id="' . $sect . 'Submit" src="../pic/gfx/but_see_the_models.gif" alt="SEE THE MODELS" onmouseover="this.src=\'../pic/gfx/hov_see_the_models.gif\';" onmouseout="this.src=\'../pic/gfx/but_see_the_models.gif\';" class="button"> - ';
    DoButtonSubmit("see_the_models", "../pic/gfx", "submit");
    #echo '<img src="../pic/gfx/but_reset.gif" onmouseover="this.src=\'../pic/gfx/hov_reset.gif\';" onmouseout="this.src=\'../pic/gfx/but_reset.gif\';" border="0" onClick="ResetForm(document.' . $sect . ')" alt="RESET" class="button">';
    DoButtonReset("../pic/gfx", $sect);
    echo "\n</form>\n\n</td></tr>\n";
}

function ChooseRegion($nrows)
{
?>
<td valign=top rowspan="<?php echo $nrows;?>">Region:</td>
<td valign=top rowspan="<?php echo $nrows;?>">
<input type="radio" name="region" value="U" checked> USA<br>
<input type="radio" name="region" value="R"> International<br>
<input type="radio" name="region" value="L"> Latin America (2008-2011)<br>
<input type="radio" name="region" value="B"> UK (2000, 2001)<br>
<input type="radio" name="region" value="D"> Germany (1999-2001)<br>
<input type="radio" name="region" value="A"> Australia (2000, 2001)<br>
Note that Australian dealers might carry either USA or International assortments after 2001.</td>
<?php
}
?> 

<center>
<!--The Interactive Matchbox Lineup-->
<a href="#id">By Specific MAN ID</a> -
<a href="#year">By Year</a> -
<a href="#rank">By Lineup Number</a> -
<a href="#manno">By MAN Number</a> -
<a href="#mack">By Mack Number</a> -
<a href="#makes">By Make</a> -
<a href="#search">By Text Search</a> -
<a href="#sets">By Special Sets</a>
</center>

<table width="100%">

<?php
SectionHeader("id", "msearch.cgi", "Specific Manufacturing ID");
?>
<table>
<tr>
<td>See specific manufacturing ID:</td><td><input type="text" name="id" id="idId" value="" size="12"></td></tr>
</table>

<?php
SectionTail('id');

SectionHeader("year", "lineup.cgi", "Models by Year");
?>
<table><tr>
<td valign=top>Year: </td>
<td valign=top class="updown">
<?php SelectYear('year', 'yearYear', $yearend, $yearstart, $yearend); ?>

</td>

<td width=20></td>
<?php
ChooseRegion(1);

if ($isadmin)
{
    echo '<td width=20></td><td>';
    echo '<i>Number of years: <input type="text" name="nyears" value="" size="2">' . "\n";
    echo '<p><input type="checkbox" name="unroll" value="1"> Unroll' . "\n";
    echo '<p><input type="checkbox" name="large" value="1"> Large' . "\n";
    echo '<p><input type="checkbox" name="verbose" value="1"> Verbose</i>' . "\n";
}
?>
</tr>
</table>

<?php
SectionTail('year');

SectionHeader("rank", "lineup.cgi", "Models by Lineup Number");
?>
<input type="hidden" name="n" value="1">
<table><tr>
<td valign=top>
Lineup number:<br>
(1-120)
</td>
<td valign=top class="updown">
<input type="text" name="num" size="3" id="rankNum"><br>
<?php incrnum('rankNum', 1, 120, ''); ?>
</td>
<td width=16></td>
<td style="text-align: right;" valign=top>
Start year:
</td>
<td valign=top class="updown">
<?php SelectYear('syear', 'rankSyear', $yearstart, $yearstart, $yearend); ?>
</td>

<td width=16 rowspan=2></td>
<?php
ChooseRegion(2);

if ($isadmin)
{
    echo '<td width=16 rowspan=2></td>';
    echo '<td valign="top" rowspan=2><i>';
    echo '<input type="checkbox" name="large" value="1"> Large<p>' . "\n";
    echo '<input type="checkbox" name="verbose" value="1"> Verbose<p>' . "\n";
    echo '<input type="checkbox" name="prodpic" value="1"> Product Pics</i></td>' . "\n";
}
?>
</tr><tr>
<?php
if ($isadmin)
{
?>
<td valign=top>
<i>Ending number:<br>
(1-120)</i>
</td>
<td valign=top class="updown">
<input type="text" name="enum" size="3" id="rankNum"><br>
<?php incrnum('rankNum', 1, 120, ''); ?>
</td>
<td width=16></td>
<?php
}
else
{
    echo "<td colspan=3></td>\n";
}
?>
<td style="text-align: right;" valign=top>
End year:
</td><td class="updown">
<?php SelectYear('eyear', 'rankEyear', $yearend, $yearstart, $yearend); ?>
</td>
</table>

<?php
SectionTail('rank');

SectionHeader("manno", "manno.cgi", "Manufacturing Numbers");
?>
<table>
<tr><td colspan=7>
<select name="section" id="manSection">
<option value="" selected>Please select a range
<?php
if ($pif['fake'])
{
?>
<option value="man">Main 1-75 Line
<option value="rwr">Real Working Rigs
<option value="mi">Older Matchbox International Castings
<option value="orig">Matchbox Originals
<option value="promo">Promotional Models
<option value="wr">White Rose Only
<option value="fea">Featured and Collectibles Castings
<option value="sf">Superfast Models 1970-1981
<option value="rn">Roman Numeral Models
<option value="rw">Regular Wheel Models
<?php
}
else if ($isadmin)
{
    $sl = Fetch("select id, name from section where page_id like 'man%' order by display_order", $pif);
    foreach ($sl as $ent)
	echo '<option value="' . $ent[0] . '">' . $ent[1] . "\n";
}
else
{
    $sl = Fetch("select id, name from section where page_id='manno' order by display_order", $pif);
    foreach ($sl as $ent)
	echo '<option value="' . $ent[0] . '">' . $ent[1] . "\n";
}
?>
<option value="all">All Ranges
</select>
<?php incrsel('manSection', -1); ?>
</td><td rowspan=3>
<?php
if ($isadmin)
{
?>
<i>
List type:
<select name="listtype">
<option value="" selected>Normal
<option value="ckl">Checklist
<option value="thm">Thumbnails
<option value="adl">Admin List
<option value="pxl">Picture List
<option value="vtl">Vehicle Type
</select><br>
<nobr><input type="checkbox" name="verbose" value="1"> Verbose</nobr><br>
<input type="checkbox" name="nodesc" value="1"> No Notes<br>
</i>
<?php
}
?>
</td></tr><tr>
<td valign="top"><input type="radio" name="range" value="all" checked> All numbers</td>
<td valign="top"><input type="radio" name="range" value="some"> Some numbers</td>
<td valign="top">starting at:</td><td valign="top"><input type="text" name="start" id="manStart" value="1" size="4" onFocus="document.manno.range[1].checked=true;">
<?php incrnum('manStart', 1, "document.getElementById('manEnd').value", 'document.manno.range[1].checked=true;'); ?>
</td>
<?php
if ($isadmin)
{
?>
<td width=16 style="text-align: right;"></td>
<td valign=top>
Start year:
</td>
<td valign=top class="updown">
<?php SelectYear('syear', 'manSyear', $yearstart, $yearstart, $yearend + 1); ?>
</td>
<?php
}
?>
</tr>
<tr><td></td><td></td><td valign="top">ending at:</td><td valign="top"><input type="text" name="end" id="manEnd" value="999" size="4" onFocus="document.manno.range[1].checked=true;">
<?php incrnum('manEnd', "document.getElementById('manStart').value", 999, 'document.manno.range[1].checked=true;'); ?>
</td>
<?php
if ($isadmin)
{
?>
<td width=16 style="text-align: right;"></td>
<td valign=top>
End year:
</td>
<td valign=top class="updown">
<?php SelectYear('eyear', 'manEyear', $yearend + 1, $yearstart, $yearend + 1); ?>
</td>
<?php
}
?>
</tr>
</table>

Filter by vehicle type:
<table>
<tr>
<td class="tdboth" colspan=3>Every vehicle has one of these.</td>
<td class="tdboth" colspan=3>Vehicle may have up to two of these.</td>
</tr>

<?php
function ynmcell($arr, $verb)
{
    global $isadmin;
    echo('<td class="tdleft"><b>' . $arr[1] . "</b></td>");
    echo('<td class="tdmiddle">');
    if ($isadmin)
	echo($arr[0][0]);
    echo('</td>');
    echo('<td class="tdright">');
    echo('<input type="radio" name="type_' . $arr[0] . '" value="y">yes' . "\n");
    echo('<input type="radio" name="type_' . $arr[0] . '" value="n">no' . "\n");
    echo('<input type="radio" name="type_' . $arr[0] . '" value="m" checked>maybe' . "\n");
    echo("</td>\n");
}

$a = array();
$b = array();

$a[] = array("a", "aircraft");
$a[] = array("o", "boat");
$a[] = array("b", "bus");
$a[] = array("2", "coupe");
$a[] = array("e", "equipment");
$a[] = array("1", "motorcycle");
$a[] = array("r", "railroad");
$a[] = array("4", "sedan");
$a[] = array("u", "sport/utility");
$a[] = array("z", "trailer");
$a[] = array("t", "truck");
$a[] = array("v", "van");
$a[] = array("5", "wagon");

$b[] = array("9", "ambulance");
$b[] = array("c", "commercial");
$b[] = array("i", "construction");
$b[] = array("d", "convertible");
$b[] = array("j", "fantasy");
$b[] = array("g", "farm");
$b[] = array("f", "fire");
$b[] = array("m", "military");
$b[] = array("p", "pick-up");
$b[] = array("l", "police");
$b[] = array("8", "racer");
$b[] = array("h", "recreation");
$b[] = array("x", "taxi");

foreach(array_keys($a) as $k)
{
    echo("<tr>\n");
    ynmcell($a[$k], $isadmin);
    ynmcell($b[$k], $isadmin);
    echo("</tr>\n");
}

?>

</table>

<?php
SectionTail('manno');

SectionHeader("mack", "mack.cgi", '"Mack" Numbers');
?>
<table><tr>
<td><input type="radio" name="sect" value="all" checked> Both sections</td>
<td><input type="radio" name="range" value="all" checked> All numbers</td>
<?php
if ($isadmin)
{
    echo '<td colspan=2></td><td><nobr><i><input type="checkbox" name="verbose" value="1"> Verbose' . "</i></nobr></td>\n";
}
?>
</tr>
<tr>
<td><input type="radio" name="sect" value="rw"> Regular Wheels</td>
<td><input type="radio" name="range" value="some"> Only numbers</td>
<td>starting at:</td><td><input type="text" name="start" id="mackStart" value="1" size="3" onFocus="document.mack.range[1].checked=true;">
<?php incrnum('mackStart', 1, "document.getElementById('mackEnd').value", 'document.mack.range[1].checked=true;'); ?>
</td></tr>
<tr>
<td><input type="radio" name="sect" value="sf"> SuperFast</td>
<td></td><td>ending at:</td><td><input type="text" name="end" id="mackEnd" value="120" size="3" onFocus="document.mack.range[1].checked=true;">
<?php incrnum('mackEnd', "document.getElementById('mackStart').value", 120, 'document.mack.range[1].checked=true;'); ?>
</td></tr>
</table>

<?php
SectionTail('mack');

SectionHeader("makes", "makes.cgi", "Vehicle Makes");
?>
Choose a make:<br>
<table><tr><td valign="top">
<input type="radio" name="make" value="unk" checked> unknown<br>
<input type="radio" name="make" value="unl"> unlicensed<br>
<input type="radio" name="make" value="text"> Specific make: 
<input type="text" name="text" onFocus="document.makes.make[2].checked=true;">
</td>
<td valign="top">Or, <a href="../cgi-bin/makes.cgi">choose from a list!</a></td>
</tr></table>

<?php
SectionTail('makes');

SectionHeader("search", "msearch.cgi", "Text Search");
?>
Search the casting information for: <input type="text" name="query"><br>

<?php
SectionTail('search');

SectionHeader("vsearch", "vsearch.cgi", "Variation Text Search");
?>
Search the variation information for models containing the following.<p>
<table><tr><td width=50 rowspan=6></td>
<td>Casting name:</td><td><input type="text" name="casting"></td><td width="16">
<td>Code 1 models</td><td><input type="checkbox" name="codes" value="1" checked></td></tr>
<tr><td>Base:</td><td><input type="text" name="base"></td><td></td>
<td>Code 2 models</td><td><input type="checkbox" name="codes" value="2" checked></td></tr>
<tr><td>Body:</td><td><input type="text" name="body"></td></tr>
<tr><td>Interior:</td><td><input type="text" name="interior"></td></tr>
<tr><td>Wheels:</td><td><input type="text" name="wheels"></td></tr>
<tr><td>Windows:</td><td><input type="text" name="windows"></td></tr>
<?php if ($isadmin) echo '<tr><td></td><td><i>Category:</i></td><td><input type="text" name="cat"></td></tr>'; ?>
</table>

<?php
SectionTail('vsearch');

SectionHeader("packs", "packs.cgi", "Multi-Model Packs");
?>
<select name="page" id="packsPage">
<option value="" selected>
<?php
$sl = Fetch("select id, flags, title from page_info where format_type='packs' order by title", $pif);
foreach ($sl as $ent)
    if (!($ent[1] & 1))
	echo '<option value="' . trim($ent[0]) . '">' . $ent[2] . "\n";
?>
</select>
<?php incrsel('packsPage', -1);
if ($isadmin)
{
    echo '<i><input type="checkbox" name="verbose" value="1"> Verbose' . "</i>\n";
}
?>
<br>

<?php
SectionTail('packs');

SectionHeader("sets", "matrix.cgi", "Special Sets");
?>
<select name="page" id="setsPage">
<option value="" selected>
<?php
if ($pif['fake'])
{
?>
<option value="matrix.character">Character Cars - 1979 through 2000
<option value="matrix.codered">Code Red TV Series - 1981
<option value="matrix.supergt">Budget Range Models - 1986
<option value="matrix.drt">Dragon Racing Team - 1986
<option value="matrix.sf">SuperFast - 1986-1990
<option value="matrix.scmw">Monster Trucks - 1986-1994
<option value="matrix.lasers">Laser Wheels - 1988
<option value="matrix.wclass">World Class Series - 1989-1995
<option value="matrix.orig">40th Anniversary Originals - 1993
<option value="matrix.cchoice">Collector's Choice - 1994
<option value="matrix.goldcoin">Gold Coin Series - 1995
<option value="matrix.nba">Matchbox NBA Collection - 1995-1998
<option value="matrix.chall">Challenge Series - 1997
<option value="matrix.starcars">Star Car Collection - 1998-1999
<option value="matrix.fastfood">Fast Food Toys - 1999 onward
<option value="matrix.germany">Germany Special Series - 2001-2009
<option value="matrix.hs">Heroes Series - 2002-2003
<option value="matrix.maa">Across America - 2003
<option value="matrix.sf1">Superfast - 2004
<option value="matrix.maw">Around the World - 2004
<option value="matrix.sf2">Superfast - 2005
<option value="matrix.sf3">Superfast - 2006
<option value="matrix.sf4">Superfast - 2007
<option value="matrix.bob07">Best of British - 2007
<option value="matrix.boi08">Best of International - 2008
<option value="matrix.bom08">Best of Muscle - 2008
<option value="matrix.bob08">Best of British - 2008
<option value="matrix.sf5">Superfast - 2008
<option value="matrix.sf6">Superfast 40th Anniversary - 2009
<option value="matrix.bob09">Best of British - 2009
<?php
}
else
{
    $sl = Fetch("select id, flags, title, description from page_info where format_type='matrix' order by description", $pif);
    foreach ($sl as $ent)
	if (!($ent[1] & 1))
	    echo '<option value="' . trim($ent[0]) . '">' . $ent[2] . " - " . $ent[3] . "\n";
}
?>
</select>
<?php incrsel('setsPage', -1);
if ($isadmin)
{
    echo '<i><input type="checkbox" name="verbose" value="1"> Verbose' . "</i>\n";
}
?>
<br>

<?php
SectionTail('sets');
?>

<tr><td><hr></td></tr>
</table>

<a href=".."><img src="../pic/gfx/but_back.gif" class="button" alt="BACK" onmouseover="this.src='../pic/gfx/hov_back.gif';" onmouseout="this.src='../pic/gfx/but_back.gif';" style="vertical-align: middle; color: #FFFFFF; border-width: 0px; padding: 1px;"> to the main index.</a>
<a href="comment.php?page=3inch"><img src="../pic/gfx/but_comment_on_this_page.gif" alt="COMMENT" onmouseover="this.src='../pic/gfx/hov_comment_on_this_page.gif';" onmouseout="this.src='../pic/gfx/but_comment_on_this_page.gif';" class="comment"></a>

<?php
DoPageFooter($pif);
?>

</body>
</html>
