<!DOCTYPE html>
<html>
<?php
include "bin/basics.php";
include "config.php";
$pif = GetPageInfo("database");
DoHead($pif);
$isadmin = CheckPerm('a');
//$isadmin = 0;
$pif['hierarchy'][0] = ['/', 'Home'];
$pif['hierarchy'][1] = ['/database.php', 'Database'];
$answer = Fetch("select min(year), max(year), max(number) from lineup_model", $pif);
$LINE_YEAR_START = $answer[0][0];
$LINE_YEAR_END = $answer[0][1];
$MAX_NUMBER = $answer[0][2];
$answer = Fetch("select min(first_year), max(first_year) from base_id", $pif);
$MAN_YEAR_START = $answer[0][0];
$MAN_YEAR_END = $answer[0][1];

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
$sections[] = array("tag" => "boxes", "name" => "Lesney Era Boxes", "fn" => 'SectionBoxes', "scr" => "boxart.cgi", 'reset' => 'boxExample();');
$sections[] = array("tag" => "code2", "name" => "Code 2 Models", "fn" => 'SectionCode2', "scr" => "code2.cgi");
$sections[] = array("tag" => "other", "name" => "Other Database Pages", "fn" => 'SectionOther');

$pages = array();
$pages[] = array("title" => "About", "desc" => "About this website.", "url" => '/pages/about.php');
$pages[] = array("title" => "Toy Links", "desc" => "Links to other sites of interest", "url" => '/cgi-bin/links.cgi');
$pages[] = array("title" => "Bibliograpy", "desc" => "Books relevant to collectors", "url" => '/cgi-bin/biblio.cgi');
$pages[] = array("title" => "Comparisons", "desc" => "Between various Matchbox castings", "url" => '/cgi-bin/compare.cgi');
$pages[] = array("title" => "Errors", "desc" => "Matchbox manufacturing errors", "url" => '/cgi-bin/errors.cgi');
$pages[] = array("title" => "Ads", "desc" => "Matchbox advertising", "url" => '/cgi-bin/ads.cgi');
//prepro.cgi pub.cgi library.cgi package.cgi

DoResetJavascript();
DoIncDecJavascript();
DoPageHeader($pif);

echo "<hr><p>\n";
echo "<div class=\"maintable\"><center><ul class=\"header-links\">\n";
foreach ($sections as $sec) {
    echo " <li class=\"header-link-item\"><a href=\"#$sec[tag]\" class=\"textbutton\">&nbsp;By $sec[name]&nbsp;</a></li>\n";
}
echo "</ul></center></div>

<table class=\"maintable\">
";

foreach ($sections as $sec) {
    Section($sec);
}

echo "</table>\n";
PageFooter();

echo "</body>\n";

//---- support functions -----------------------------------------

function HorzSpacer($rowspan) {
    if ($rowspan > 1)
	echo "  <td rowspan=\"$rowspan\" class=\"hspacer\"></td>\n";
    else
	echo "  <td class=\"hspacer\"></td>\n";
    echo "\n";
}

function ChooseNum($name, $id, $width, $minval, $maxval, $defval='', $js="", $cl="") {
    echo "  <td class=\"updown\">\n<input type=\"text\" name=\"$name\" size=\"$width\" id=\"$id\"";
    if ($defval)
	echo " value=\"$defval\"";
    if ($js)
	echo " $js";
    echo ">\n";
    incrnum($id, $minval, $maxval, $cl);
    echo "  </td>\n";
}

function SelectYear($name, $id, $defval, $min, $max) {
    $sl = [];
    $yr = $max;
    while ($yr >= $min) {
	$sel = 0;
	if ($yr == $defval)
	    $sel = 64;
	$sl[] = [$sel, $yr, $yr];
	$yr = $yr - 1;
    }
    echo "  <td class=\"updown\">\n";
    Select($name, $id, $sl);
    echo "  </td>\n";
}

function Select($name, $id, $sl, $select_js="", $cl="") {
    echo "   <select name=\"$name\" id=\"$id\"";
    if ($select_js)
	echo " $select_js";
    echo ">\n";
    foreach ($sl as $ent) {
	if (!($ent[0] & 1)) {
	    echo "   <option value=\"" . trim($ent[1]) . "\"";
	    if ($ent[0] & 64) {
		echo " selected";
	    }
	    echo ">$ent[2]";
	    if (arr_get($ent, 3, '')) {
		echo " - $ent[3]";
	    }
	    echo "\n";
	}
    }
    echo "   </select>\n";
    incrsel($id, -1, $cl);
}

function FetchSelect($name, $id, $thing, $query, $extra=[], $select_js="") {
    global $pif;

    Select($name, $id, array_merge(
	[[64, '', 'Please select a ' . $thing . '.', '']],
	Fetch($query, $pif),
	$extra), $select_js);
}

function Checks($input, $name, $values, $sep='<br>') {
    foreach ($values as $val) {
	echo "   <input type=\"$input\" name=\"$name\" value=\"$val[0]\"";
	if (arr_get($val, 2, 0))
	    echo " checked";
	echo "> $val[1]$sep\n";
    }
}

// required: fn tag scr name  optional: reset
function Section($args) {
    global $isadmin;

    echo "\n<tr><td><br></td></tr>\n<tr>\n  <td class=\"$args[tag]_head sel_head\">\n";
    if (isset($args['scr'])) {
	echo "<form action=\"/cgi-bin/$args[scr]\" method=\"get\" name=\"$args[tag]\" id=\"$args[tag]\">\n";
    }
    else {
	echo "<i id=\"$args[tag]\"></i>\n";
    }
    echo "   <center><h2>$args[name]</h2></center>\n  </td>\n </tr>\n";
    echo " <tr><td class=\"spacer\"></td></tr>\n\n <tr><td class=\"$args[tag]_body sel_body\">\n";
    if (isset($args['scr'])) {
	echo "Select what kind of Matchbox lineup you would like to see, then click \"SEE THE MODELS\".<p>\n\n";
	call_user_func($args['fn']);
	echo "<br>\n";
	DoTextButtonSubmit("SEE THE MODELS", "submit");
	DoTextButtonReset($args['tag'], arr_get($args, 'reset', ''));
	if ($isadmin)
	    Checks('checkbox', 'verbose', [['1', '<i>Verbose</i>']], ''); 
	echo "\n</form>\n\n";
    }
    else
	call_user_func($args['fn']);
    echo "  </td>\n </tr>\n";
}

function ChooseRegion($nrows) {
    $regions = [
	    ['U', 'USA', 1],
	    ['R', 'International'],
	    ['L', 'Latin America (2008-2011)'],
	    ['B', 'UK (2000, 2001)'],
	    ['D', 'Germany (1999-2001)'],
	    ['A', 'Australia (2000, 2001)']
	];
    echo "    <td rowspan=\"$nrows\">Region:</td>\n";
    echo "    <td rowspan=\"$nrows\">\n";
    Checks('radio', 'region', $regions);
    echo "</td>\n";
}

function RegionNote() {
    echo "<td colspan=\"2\">Note that Australian dealers might carry either<br>USA or International assortments after 2001.</td>\n";
}

//---- beginning of sections -------------------------------------

function SectionID() {
    echo "\n<table>\n <tr>\n";
    echo "  <td class=\"idtab\">See specific manufacturing ID:</td><td><input type=\"text\" name=\"id\" id=\"idId\" value=\"\" size=\"12\"></td>\n";
    echo " </tr><tr>\n";
    echo "  <td class=\"idtab\">See specific variation ID:</td><td><input type=\"text\" name=\"var\" id=\"idVar\" value=\"\" size=\"12\"> (optional)";
    echo "</td>\n </tr>\n</table>\n";
}

function SectionYear() {
    global $LINE_YEAR_START, $LINE_YEAR_END, $isadmin;

    echo "\n<table>\n <tr>\n  <td>Year: </td>\n";
    SelectYear('year', 'yearYear', $LINE_YEAR_END, $LINE_YEAR_START, $LINE_YEAR_END);
    HorzSpacer(3);
    ChooseRegion(2);
    echo "  </td>\n";
    HorzSpacer(3);
    echo "  <td rowspan=\"3\">\n";
    $ptypes = [
	["man", "Main line models", 1],
	["series", "Series", 1],
	["ks", "Larger Scale Models", 1],
	["acc", "Accessories", 1],
	["yy", "Yesteryears and Matchbox Collectibles", 1],
	["pack", "Packs and Gift Sets", 1],
	["bld", "Buildings", 1],
	["pub", "Publications", 1]
    ];
    Checks('checkbox', 'lty', $ptypes);
    echo "  </td>\n</tr>\n<tr><td colspan=\"2\" rowspan=\"2\">\n";
    if ($isadmin) {
	echo "<p>\n<i>Number of years: <input type=\"text\" name=\"nyears\" value=\"\" size=\"2\">\n<p>\n";
	Checks('checkbox', 'unroll', [['1', 'Unroll']], '<p>');
	Checks('checkbox', 'large', [['1', 'Large']], '');
    }
    echo " </td></tr>\n<tr>";
    RegionNote();
    echo " </tr>\n</table>\n";
}

function SectionRank() {
    global $LINE_YEAR_START, $LINE_YEAR_END, $MAX_NUMBER, $isadmin;

    echo "<input type=\"hidden\" name=\"n\" value=\"1\">";
    echo "<table>\n <tr>\n  <td height=\"32\">Lineup number:<br>(1-$MAX_NUMBER)\n  </td>";
    ChooseNum('num', 'rankSNum', 3, 1, $MAX_NUMBER);
    HorzSpacer(1);
    echo "  <td style=\"text-align: right;\">\nStart year:\n  </td>\n";
    SelectYear('syear', 'rankSyear', $LINE_YEAR_START, $LINE_YEAR_START, $LINE_YEAR_END);
    HorzSpacer(2);
    ChooseRegion(3);
    echo "</tr><tr>\n<td>\n";
    if ($isadmin) {
	echo "<i>Ending number:<br>\n(1-$MAX_NUMBER)</i>\n";
    }
    echo "  </td>\n";
    if ($isadmin)
	ChooseNum('enum', 'rankENum', 3, 1, $MAX_NUMBER);
    else
	echo "  <td></td>\n";
    HorzSpacer(1);
    echo "  <td style=\"text-align: right;\">End year:</td>\n";
    SelectYear('eyear', 'rankEyear', $LINE_YEAR_END, $LINE_YEAR_START, $LINE_YEAR_END);
    echo " </tr>\n <tr>\n  <td colspan=\"6\" rowspan=\"2\">\n";
    if ($isadmin) {
	echo "<br><i>\n";
	Checks('checkbox', 'large', [['1', 'Large']]);
	Checks('checkbox', 'prodpic', [['1', 'Product Pics']], '');
	echo "</i>\n";
    }
    echo "  </td>\n </tr>\n <tr>";
    RegionNote();
    echo " </tr>\n</table>";
}

function SectionManno() {
    global $MAN_YEAR_START, $MAN_YEAR_END, $isadmin;

    echo "<table>\n <tr>\n  <td colspan=\"7\">\n";
    if ($isadmin)
	$q = "select 0, id, name from section where page_id like 'man%' order by display_order";
    else
	$q = "select 0, id, name from section where page_id='manno' order by display_order";
    FetchSelect('section', 'manSection', 'range', $q, [[0, 'all', 'All Ranges']]);
    if ($isadmin) {
	echo "<i>\n";
	Checks('checkbox', 'nodesc', [['1', 'No Notes']]);
	echo "</i>\n";
    }
    echo "</td><td rowspan=\"3\">\n";
    echo "\n</td></tr><tr>\n<td>";
    Checks('radio', 'range', [['all', 'All numbers', 1]]);
    echo "</td>\n<td>";
    Checks('radio', 'range', [['some', 'Some numbers']]);
    echo "</td>\n<td>starting at:</td>\n";
    ChooseNum("start", "manStart", 4, 1, "document.getElementById('manEnd').value", 1, 'onFocus="document.manno.range[1].checked=true;"', "document.manno.range[1].checked=true;");

    if ($isadmin) {
	HorzSpacer(1);
	echo "   <td>Start year:</td>\n";
	SelectYear('syear', 'manSyear', $MAN_YEAR_START, $MAN_YEAR_START, $MAN_YEAR_END);
    }
    echo " </tr>\n <tr><td colspan=\"2\">";
    if ($isadmin) {
	echo "<i>";
	Checks('checkbox', 'large', [['1', 'Large']], '');
	echo "</i>";
    }
    echo "</td>\n";
    echo "  <td>ending at:</td>\n";
    ChooseNum("end", "manEnd", 4, "document.getElementById('manStart').value", 1499, 1499, 'onFocus="document.manno.range[1].checked=true;"', "document.manno.range[1].checked=true;");

    if ($isadmin) {
	HorzSpacer(1);
	echo "<td>End year:</td>\n";
	SelectYear('eyear', 'manEyear', $MAN_YEAR_END + 1, $MAN_YEAR_START, $MAN_YEAR_END);
    }
    echo " </tr>\n <tr><td colspan=\"4\">List type:\n";
    $sl = [[64, '', 'Normal'], [0, 'ckl', 'Checklist'], [0, 'thm', 'Thumbnails'], [0, 'csv', 'CSV'], [0, 'jsn', 'JSON']];
    if ($isadmin) {
	$sl = array_merge($sl, [[0, 'adl', 'Admin List'], [0, 'pxl', 'Picture List'], [0, 'lnl', 'Links List'], [0, 'vtl', 'Vehicle Type']]);
    }
    Select('listtype', 'selList', $sl);

    echo "  </td>\n </tr>\n</table>\n";
    echo "Filter by vehicle type:\n<table class=\"types\">";
    echo " <tr>\n  <td class=\"tdboth\" colspan=\"2\">Every vehicle has one of these.</td>\n";
    echo "  <td class=\"tdboth\" colspan=\"2\">Vehicle may have up to two of these.</td>\n";
    if ($isadmin)
	echo "  <td class=\"tdboth\" colspan=\"2\"><i>Filter by picture type.</i></td>\n";
    echo " </tr>";

    function YNMCell($arr, $pref) {
	global $isadmin;

	echo "  <td class=\"tdleft\"><b>$arr[1]</b></td>\n";
//        echo "  <td class=\"tdmiddle\">";
//	if ($isadmin)
//	    echo "<i>$arr[0]</i>";
//	echo "  </td>\n";
	echo "  <td class=\"tdright\">";
	Checks('radio', $pref . $arr[0], [['y', 'yes'], ['n', 'no'], ['m', 'maybe', 1]], '');
	echo "  </td>\n";
    }
    $a = [
	["a", "aircraft"],
	["o", "boat"],
	["b", "bus"],
	["2", "coupe"],
	["e", "equipment"],
	["1", "motorcycle"],
	["r", "railroad"],
	["4", "sedan"],
	["u", "sport/utility"],
	["z", "trailer"],
	["t", "truck"],
	["v", "van"],
	["5", "wagon"]
    ];
    $b = [
	["9", "ambulance"],
	["c", "commercial"],
	["i", "construction"],
	["d", "convertible"],
	["j", "fantasy"],
	["g", "farm"],
	["f", "fire"],
	["m", "military"],
	["p", "pick-up"],
	["l", "police"],
	["8", "racer"],
	["h", "recreation"],
	["x", "taxi"]
    ];
    $c = [
	['f', 'advertisement'],
	['b', 'baseplate'],
	['z', 'comparison'],
	['a', 'custom'],
	['d', 'detail'],
	['e', 'error'],
	['i', 'interior'],
	['p', 'prototype'],
	['r', 'real'],
	['x', 'box']
    ];
    $d = [
	10 => ['s', 'small'],
	11 => ['m', 'medium'],
	12 => ['l', 'large'],
    ];
    foreach(array_keys($a) as $k) {
	echo(" <tr>\n");
	YNMCell($a[$k], 'type_');
	YNMCell($b[$k], 'type_');
	if ($isadmin) {
	    if (isset($c[$k]))
		YNMCell($c[$k], 'add_');
	    else
		YNMCell($d[$k], 'pic_');
	}
	echo(" </tr>\n");
    }
    echo "</table>\n";
}

function SectionMack() {
    global $MAX_NUMBER;

    echo "<table>\n <tr>\n  <td>\n";
    Checks('radio', 'sect', [['all', 'Both sections', 1]]);
    echo "  </td>\n";
    HorzSpacer(3);
    echo "  <td>\n";
    Checks('radio', 'range', [['all', 'All numbers', 1]]);
    echo "  </td>\n </tr>\n <tr>\n  <td>\n";
    Checks('radio', 'sect', [['rw', 'Regular Wheels']]);
    echo "  </td>\n  <td>\n";
    Checks('radio', 'range', [['some', 'Only numbers']]);
    echo "  </td>\n  <td>starting at:</td>\n";
    ChooseNum('start', 'mackStart', 3, 1, "document.getElementById('mackEnd').value", 1, 'onFocus="document.mack.range[1].checked=true;"', 'document.mack.range[1].checked=true;');
    echo " </tr>\n <tr>\n  <td>\n";
    Checks('radio', 'sect', [['sf', 'SuperFast']]);
    echo "  </td>\n  <td></td>\n  </td><td>ending at:</td>\n";
    ChooseNum('end', 'mackEnd', 3, "document.getElementById('mackStart').value", $MAX_NUMBER, $MAX_NUMBER, 'onFocus="document.mack.range[1].checked=true;"', 'document.mack.range[1].checked=true;');
    echo " </tr>\n</table>\n";
}

function SectionMakes() {
    echo "Choose a make:<br>\n<table><tr><td>\n";
    Checks('radio', 'make', [['unk', 'unknown', 1], ['unl', 'unlicensed']]);
    Checks('radio', 'make', [['text', 'Specific make:']], '');
    echo "<input type=\"text\" name=\"text\" onFocus=\"document.makes.make[2].checked=true;\">\n  </td>\n";
    echo "  <td>Or, <a href=\"../cgi-bin/makes.cgi\">choose from a list!</a></td>\n";
    echo " </tr></table>\n";
}

function SectionSearch() {
    echo "<table><tr><td>\n";
    echo "Search the casting information for: <input type=\"text\" name=\"query\">\n";
    echo "</td></tr></table>\n";
}

function SectionVSearch() {
    global $isadmin;

    echo "Search the variation information for models containing the following.<p>\n";
    echo "<table><tr>\n";
    HorzSpacer(6);
    echo "<td>Casting name:</td><td><input type=\"text\" name=\"casting\"></td><td width=\"16\">\n";
    echo "<td>\n";
    Checks('checkbox', 'codes', [['1', 'Code 1 Models', 1]], '');
    echo "</td></tr>\n";
    echo "<tr><td>Base:</td><td><input type=\"text\" name=\"base\"></td><td></td>\n";
    echo "<td>\n";
    Checks('checkbox', 'codes', [['2', 'Code 2 Models', 1]], '');
    echo "</td></tr>\n";
    echo "<tr><td>Body:</td><td><input type=\"text\" name=\"body\"></td></tr>\n";
    echo "<tr><td>Interior:</td><td><input type=\"text\" name=\"interior\"></td></tr>\n";
    echo "<tr><td>Wheels:</td><td><input type=\"text\" name=\"wheels\"></td></tr>\n";
    echo "<tr><td>Windows:</td><td><input type=\"text\" name=\"windows\"></td></tr>\n";
    if ($isadmin) {
	echo "<tr><td></td><td><i>Area:</i></td><td><input type=\"text\" name=\"area\"></td></tr>\n";
	echo "<tr><td></td><td><i>Category:</i></td><td><input type=\"text\" name=\"cat\"></td></tr>\n";
	echo "<tr><td></td><td><i>Date:</i></td><td><input type=\"text\" name=\"date\"></td></tr>\n";
    }
    echo "</table>\n";
}

function SectionPacks() {
    echo "<table><tr><td>\n";
    FetchSelect('sec', 'packPage', 'pack type', "select flags, id, name from section where page_id like 'packs.%' and not (flags & 1) order by name");
    echo "</td></tr><tr><td>\n";
    echo "Search the titles for: <input type=\"text\" name=\"title\">\n";
    echo "</td></tr></table>\n";
}

function SectionSets() {
    echo "<table><tr><td>\n";
    FetchSelect('page', 'setsPage', 'set', "select flags, id, title, description from page_info where format_type='matrix' order by description");
    echo "</td></tr></table>\n";
}


function Quote($x) { return "'" . $x . "'"; }
function SectionBoxes() {
    global $isadmin;

    $examples = array('A' => 'rw01a', 'B' => 'rw02a', 'C' => 'rw03b', 'D' => 'rw04c', 'E' => 'rw05d', 'F' => 'rw06d',
		      'G' => 'sf11a', 'H' => 'sf13b', 'I' => 'sf15b', 'J' => 'sf16a', 'K' => 'sf19c', 'L' => 'sf21c');
    $qex = implode(', ', array_map("Quote", array_values($examples)));
    echo <<<EOT
<script  language="Javascript">
function boxExample() {
    var sel = document.getElementById("boxStyle").value;
    var examples = [$qex];
    if (sel == '' || sel == 'all') {
	document.getElementById("boxImg").setAttribute('class', "hidden");
    }
    else {
	document.getElementById("boxImg").src = "pic/box/s_" + examples[sel.charCodeAt(0) - 65] + '-' + sel.toLowerCase() +  '.jpg';
	document.getElementById("boxImg").setAttribute('class', "shown");
    }
}
document.addEventListener("DOMContentLoaded", boxExample, false);
</script>
EOT;

    echo "\n<table>\n <tr>\n  <td>Series:</td>\n  <td>";
    Checks('radio', 'series', [['', 'All', 1]], '');
    echo "</td>\n";
    HorzSpacer(1);
    echo "  <td>Model Numbers:</td>\n  <td>Starting at number:</td>\n";
    ChooseNum('start', 'boxStart', 3, 1, 75, 1);
    HorzSpacer(1);
    echo "  <td rowspan=\"5\" id=\"foo\"><img src=\"pic/box/s_rw01a-a.jpg\" class=\"hidden\" id=\"boxImg\"></td>\n";
    echo " </tr>\n <tr>\n  <td></td>\n  <td>\n";
    Checks('radio', 'series', [['RW', 'Regular Wheels']], '');
    echo "  </td>\n  <td></td>\n  <td></td>\n  <td>Ending at number:</td>\n";
    ChooseNum('end', 'boxEnd', 3, 1, 75, 75);
    echo " </tr>\n <tr>\n  <td></td>\n  <td>\n";
    Checks('radio', 'series', [['SF', 'SuperFast']], '');
    echo "  </td>\n </tr>\n <tr>\n  <td>&nbsp;\n";
    echo "  </td>\n </tr>\n <tr>\n  <td>Styles:</td>\n  <td colspan=\"4\">\n";

    $sl = [[64, '', 'Please select a box style.']];
    foreach ($examples as $ty => $pic) {
	$sl[] = [0, $ty, $ty . ' type'];
    }
    $sl[] = [0, 'all', 'All'];
    Select('style', 'boxStyle', $sl, 'onkeyup="boxExample();" onchange="boxExample();" onmouseup="boxExample();"', "boxExample();");
    echo "  </td>\n";
    if ($isadmin) {
	echo "  <td>\n";
	Checks('checkbox', 'c', [['1', '<i>Compact</i>']], '');
	echo "  </td>\n  <td></td>";
    }
    echo " </tr>\n</table>\n";
}

function SectionCode2() {
    echo "<table><tr><td>\n";
    echo "Choose a type of Code 2 model:\n";
    FetchSelect('section', 'code2Section', 'range', "select flags, id, name from section where page_id='code2' order by display_order", [[0, '', 'All Sections']]);
    echo "</td></tr></table>\n";
}

function SectionOther() {
    global $IMG_DIR_ART, $pages;
    echo "<div class='paget'>\n";
    foreach ($pages as $page) {
	echo "<div class='pagec'><center>\n";
	echo "<div class='othertitle'>" . $page['title'];
	echo "<p><div class='otherdesc'>" . $page['desc'] . "</div>\n";
	echo "</div>\n";
	DoTextButtonLink("VIEW THE PAGE", $page['url']);
	echo "</center></div>\n";
    }
    echo "</div>\n";
}

//---- end of sections -------------------------------------------

function PageFooter() {
    global $IMG_DIR_ART;
    echo "<hr>\n";
    echo "<div class=\"bottombar\">\n";
    echo "<div class=\"bamcamark\"><img src=\"$IMG_DIR_ART/bamca_sm.gif\"></div>\n";
    echo "<div class=\"footer\">\n";
    DoTextButtonLink("BACK", '/');
    echo " to the index.\n</div>\n";

    echo "<div class=\"comment_button\">\n";
    echo "<div class=\"comment_box\">\n";
    DoTextButtonLink("COMMENT ON<br>THIS PAGE", "/pages/comment.php?page=database", "textbutton");
    echo "</div>\n</div>\n</div>\n";
}

?>
</html>
