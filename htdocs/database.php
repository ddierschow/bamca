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
$answer = Fetch("select min(year), max(year) from lineup_model", $pif);
$YEAR_START = $answer[0][0];
$YEAR_END = $answer[0][1];

$sections = array();
$sections[] = array("tag" => "id", "name" => "Specific Model ID", "fn" => 'SectionID', "scr" => "msearch.cgi");
$sections[] = array("tag" => "year", "name" => "Year", "fn" => 'SectionYear', "scr" => "lineup.cgi");
$sections[] = array("tag" => "rank", "name" => "Lineup Number", "fn" => 'SectionRank', "scr" => "lineup.cgi");
$sections[] = array("tag" => "manno", "name" => "MAN Number", "fn" => 'SectionManno', "scr" => "manno.cgi");
$sections[] = array("tag" => "mack", "name" => "Mack Number", "fn" => 'SectionMack', "scr" => "mack.cgi");
$sections[] = array("tag" => "makes", "name" => "Make", "fn" => 'SectionMakes', "scr" => "makes.cgi");
$sections[] = array("tag" => "search", "name" => "Text Search", "fn" => 'SectionSearch', "scr" => "msearch.cgi");
$sections[] = array("tag" => "vsearch", "name" => "Variation Text Search", "fn" => 'SectionVSearch', "scr" => "vsearch.cgi");
$sections[] = array("tag" => "packs", "name" => "Multi-Model Packs", "fn" => 'SectionPacks', "scr" => "packs.cgi");
$sections[] = array("tag" => "sets", "name" => "Special Sets", "fn" => 'SectionSets', "scr" => "matrix.cgi");
$sections[] = array("tag" => "boxes", "name" => "Lesney Era Boxes", "fn" => 'SectionBoxes', "scr" => "boxart.cgi");

DoResetJavascript();
DoIncDecJavascript();
DoPageHeader($pif);

echo '<ul class="header-links">' . "\n";
foreach ($sections as $sec)
{
    echo '<li class="header-link-item"><a href="#' . $sec['tag'] . '">By ' . $sec['name'] . "</a></li>\n";
}
echo "</ul>

<table width=\"100%\">
";

foreach ($sections as $sec)
{
    Section($sec);
}

echo "</table>\n<hr>\n";

DoButtonLink("back", $IMG_DIR_ART, '/');
?>
to the index.
<a href="comment.php?page=database"><img src="../pic/gfx/but_comment_on_this_page.gif" alt="COMMENT" onmouseover="this.src='../pic/gfx/hov_comment_on_this_page.gif';" onmouseout="this.src='../pic/gfx/but_comment_on_this_page.gif';" class="comment"></a>

<?php
DoPageFooter($pif);
echo "</body>\n</html>\n";

//---- support functions -----------------------------------------

function HorzSpacer($rowspan) {
    if ($rowspan > 1)
	echo '<td rowspan="' . $rowspan . '" class="hspacer"></td>';
    else
	echo '<td class="hspacer"></td>';
    echo "\n";
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

function Section($args)
{
    echo "
<tr><td><br></td></tr>
<a name=\"" . $args['tag'] . "\"></a>
<tr><td class=\"" . $args['tag'] . "_head sel_head\">
<center><h2>" . $args['name'] . "</h2></center>
</td></tr>
<tr><td class=\"spacer\"></td></tr>

<tr><td class=\"" . $args['tag'] . "_body sel_body\">
Select what kind of Matchbox lineup you would like to see, then click \"SEE THE MODELS\".<p>

<form action=\"/cgi-bin/" . $args['scr'] . "\" method=\"get\" name=\"" . $args['tag'] . "\">
";
    call_user_func($args['fn']);
    echo "<br>\n";
    DoButtonSubmit("see_the_models", "../pic/gfx", "submit");
    DoButtonReset("../pic/gfx", $args['tag']);
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
Note that Australian dealers might carry either<br>USA or International assortments after 2001.</td>
<?php
}

//---- beginning of sections -------------------------------------

function SectionID()
{
?>
<table>
 <tr>
  <td>See specific manufacturing ID:</td><td><input type="text" name="id" id="idId" value="" size="12"></td>
 </tr>
</table>
<?php
}

function SectionYear()
{
    global $YEAR_START, $YEAR_END, $isadmin;
?>
<table>
 <tr>
  <td valign=top>Year: </td>
  <td valign=top class="updown">
<?php SelectYear('year', 'yearYear', $YEAR_END, $YEAR_START, $YEAR_END); ?>
  </td>
<?php
HorzSpacer(1);
ChooseRegion(1);
?>
  </td>
<?php HorzSpacer(1); ?>
<td valign="top">
<input type="checkbox" name="lty" value="man" checked>Main line models<br>
<input type="checkbox" name="lty" value="series" checked>Series<br>
<input type="checkbox" name="lty" value="ks" checked>Larger Scale Models<br>
<input type="checkbox" name="lty" value="acc" checked>Accessories<br>
<input type="checkbox" name="lty" value="yy" checked>Yesteryears and Matchbox Collectibles<br>
<input type="checkbox" name="lty" value="pack" checked>Packs and Gift Sets<br>
<input type="checkbox" name="lty" value="bld" checked>Buildings<br>
<input type="checkbox" name="lty" value="pub" checked>Publications<br>
</td>
<?php
if ($isadmin)
{
    HorzSpacer(1);
    echo '<td valign="top">';
    echo '<i>Number of years: <input type="text" name="nyears" value="" size="2">' . "\n";
    echo '<p><input type="checkbox" name="unroll" value="1"> Unroll' . "\n";
    echo '<p><input type="checkbox" name="large" value="1"> Large' . "\n";
    echo '<p><input type="checkbox" name="verbose" value="1"> Verbose</i>' . "\n";
}
?>
</tr>
</table>
<?php
}

function SectionRank()
{
    global $YEAR_START, $YEAR_END, $isadmin;
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
<?php HorzSpacer(1); ?>
<td style="text-align: right;" valign=top>
Start year:
</td>
<td valign=top class="updown">
<?php SelectYear('syear', 'rankSyear', $YEAR_START, $YEAR_START, $YEAR_END); ?>
</td>
<?php
HorzSpacer(2);
ChooseRegion(2);
if ($isadmin)
{
    HorzSpacer(2);
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
<?php
HorzSpacer(1);
}
else
{
    echo "<td colspan=3></td>\n";
}
?>
<td style="text-align: right;" valign=top>
End year:
</td><td class="updown">
<?php SelectYear('eyear', 'rankEyear', $YEAR_END, $YEAR_START, $YEAR_END); ?>
</td>
</table>
<?php
}

function SectionManno()
{
    global $YEAR_START, $YEAR_END, $isadmin, $pif;
?>
<table>
<tr><td colspan=7>
<select name="section" id="manSection">
<option value="" selected>Please select a range
<?php
if ($isadmin)
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
HorzSpacer(1);
?>
<td valign=top>
Start year:
</td>
<td valign=top class="updown">
<?php SelectYear('syear', 'manSyear', $YEAR_START, $YEAR_START, $YEAR_END + 1); ?>
</td>
<?php
}
?>
</tr>
<tr><td>
List type:
<select name="listtype">
<option value="" selected>Normal
<option value="ckl">Checklist
<option value="thm">Thumbnails
<option value="csv">CSV
<option value="jsn">JSON
<?php
if ($isadmin)
{
?>
<option value="adl">Admin List
<option value="pxl">Picture List
<option value="vtl">Vehicle Type
<?php
}
?>
</select><br>
</td><td></td><td valign="top">ending at:</td><td valign="top"><input type="text" name="end" id="manEnd" value="999" size="4" onFocus="document.manno.range[1].checked=true;">
<?php incrnum('manEnd', "document.getElementById('manStart').value", 999, 'document.manno.range[1].checked=true;'); ?>
</td>
<?php
if ($isadmin)
{
HorzSpacer(1);
?>
<td valign=top>
End year:
</td>
<td valign=top class="updown">
<?php SelectYear('eyear', 'manEyear', $YEAR_END + 1, $YEAR_START, $YEAR_END + 1); ?>
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
function YNMCell($arr, $verb)
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
    YNMCell($a[$k], $isadmin);
    YNMCell($b[$k], $isadmin);
    echo("</tr>\n");
}
echo "</table>\n";
}

function SectionMack()
{
    global $isadmin;
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
}

function SectionMakes()
{
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
}

function SectionSearch()
{
?>
Search the casting information for: <input type="text" name="query"><br>
<?php
}

function SectionVSearch()
{
    global $isadmin;
?>
Search the variation information for models containing the following.<p>
<table><tr>
<?php HorzSpacer(6); ?>
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
}

function SectionPacks()
{
    global $isadmin, $pif;
?>
<select name="page" id="packsPage">
<option value="" selected>Please select a pack type.
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
}

function SectionSets()
{
    global $isadmin, $pif;
?>
<select name="page" id="setsPage">
<option value="" selected>Please select a set.
<?php
$sl = Fetch("select id, flags, title, description from page_info where format_type='matrix' order by description", $pif);
foreach ($sl as $ent)
    if (!($ent[1] & 1))
	echo '<option value="' . trim($ent[0]) . '">' . $ent[2] . " - " . $ent[3] . "\n";
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
}

function Quote($x) { return "'" . $x . "'"; }
function SectionBoxes()
{
    global $isadmin, $pif;

    $examples = array('A' => 'rw01a', 'B' => 'rw02a', 'C' => 'rw03b', 'D' => 'rw04c', 'E' => 'rw05d', 'F' => 'rw06d',
		      'G' => 'sf11a', 'H' => 'sf13b', 'I' => 'sf15b', 'J' => 'sf16a', 'K' => 'sf19c', 'L' => 'sf21c');
?>

<script  language="Javascript">
function boxExample() {
    var sel = document.getElementById("boxStyle").value;
    var examples = [<?php echo implode(', ', array_map("Quote", array_values($examples))); ?>];
    if (sel == 'all') {
	document.getElementById("boxImg").setAttribute('class', "hidden");
    }
    else {
	document.getElementById("boxImg").src = "pic/box/s_" + examples[sel.charCodeAt(0) - 65] + '-' + sel.toLowerCase() +  '.jpg';
	document.getElementById("boxImg").setAttribute('class', "shown");
    }
}
document.addEventListener("DOMContentLoaded", boxExample, false);
</script>

<table>
 <tr>
  <td>Series:</td>
  <td><input type="radio" name="series" checked value=""> All</td>
<?php HorzSpacer(1); ?>
  <td>Model Numbers:</td>
  <td>Starting at number:</td>
  <td><input type="text" name="start" size="3" value="1" id="boxStart">
  <?php incrnum('boxStart', 1, 75, ''); ?>
  </td>
<?php HorzSpacer(1); ?>
  <td rowspan="5" id="foo"><img src="pic/box/s_rw01a-a.jpg" class="hidden" id="boxImg"></td>
 </tr>
 <tr>
  <td></td>
  <td><input type="radio" name="series" value="RW"> Regular Wheels</td>
  <td></td>
  <td></td>
  <td>Ending at number:</td>
  <td><input type="text" name="end" size="3" value="75" id="boxEnd">
  <?php incrnum('boxEnd', 1, 75, ''); ?>
  </td>
 </tr>
 <tr>
  <td></td>
  <td><input type="radio" name="series" value="SF"> Superfast</td>
 </tr>
 <tr>
  <td>&nbsp;</td>
  <td></td>
<?php if ($isadmin) { ?>
  <td></td>
  <td></td>
  <td><i>Verbose:</i></td>
  <td><input type="checkbox" name="verbose" value="1"></td>
<?php } ?>
 </tr>
 <tr>
  <td>Styles:</td>
  <td>
<select name="style" id="boxStyle" onkeyup="boxExample();" onchange="boxExample();" onmouseup="boxExample();" 
>
<option value="all" selected>All
<?php
foreach ($examples as $ty => $pic) {
    echo '<option value="' . $ty . '">' . $ty . " type\n";
}
?>
</select>
<?php incrsel('boxStyle', -1, " boxExample();"); ?>
  </td>
<?php if ($isadmin) { ?>
  <td></td>
  <td></td>
  <td><i>Compact:</i></td>
  <td><input type="checkbox" name="c" value="1"></td>
  <td></td>
<?php } ?>
 </tr>
</table>

<?php
}

//---- end of sections -------------------------------------------
?>
