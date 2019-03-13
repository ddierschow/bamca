<!DOCTYPE html>
<html>
<?php
include "bin/basics.php";
include "config.php";
$pif = GetPageInfo("database");
DoHead($pif);
$isadmin = CheckPerm('a');
$pif['isadmin'] = $isadmin;
//$isadmin = 0;
$pif['hierarchy'][0] = ['/', 'Home'];
$pif['hierarchy'][1] = ['/database.php', 'Database'];
$answer = Fetch("select min(year), max(year), max(number) from lineup_model", $pif);
$LINE_YEAR_START = $answer[0]['min(year)'];
$LINE_YEAR_END = $answer[0]['max(year)'];
$MAX_NUMBER = $answer[0]['max(number)'];
$answer = Fetch("select min(first_year), max(first_year) from base_id", $pif);
$MAN_YEAR_START = $answer[0]['min(first_year)'];
$MAN_YEAR_END = $answer[0]['max(first_year)'];

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
if ($pif['isadmin'])
    $sections[] = array("tag" => "pubs", "name" => "Publications", "fn" => 'SectionPubs', "scr" => "pub.cgi");
$sections[] = array("tag" => "sets", "name" => "Special Sets", "fn" => 'SectionSets', "scr" => "matrix.cgi");
$sections[] = array("tag" => "cats", "name" => "Categories", "fn" => 'SectionCats', "scr" => "cats.cgi");
$sections[] = array("tag" => "boxes", "name" => "Lesney Era Boxes", "fn" => 'SectionBoxes', "scr" => "boxart.cgi", 'reset' => 'boxExample();');
$sections[] = array("tag" => "code2", "name" => "Code 2 Models", "fn" => 'SectionCode2', "scr" => "code2.cgi");
$sections[] = array("tag" => "plants", "name" => "Location of Manufacture", "fn" => 'SectionPlant', "scr" => "plants.cgi");
$sections[] = array("tag" => "other", "name" => "Other Database Pages", "fn" => 'SectionOther');

$pages = array();
$pages[] = array("title" => "About", "desc" => "About this website", "url" => '/pages/about.php');
$pages[] = array("title" => "Toy Links", "desc" => "Links to other sites of interest", "url" => '/cgi-bin/links.cgi');
$pages[] = array("title" => "Bibliograpy", "desc" => "Books relevant to collectors", "url" => '/cgi-bin/biblio.cgi');
$pages[] = array("title" => "Comparisons", "desc" => "Between various Matchbox castings", "url" => '/cgi-bin/compare.cgi');
$pages[] = array("title" => "Errors", "desc" => "Matchbox manufacturing errors", "url" => '/cgi-bin/errors.cgi');
$pages[] = array("title" => "Ads", "desc" => "Matchbox advertising", "url" => '/cgi-bin/ads.cgi');
$pages[] = array("title" => "Customizations", "desc" => "Customizaed Matchbox toys", "url" => '/cgi-bin/custom.cgi');
$pages[] = array("title" => "Photographers", "desc" => "Contributors to this site", "url" => '/cgi-bin/photogs.cgi');
$pages[] = array("title" => "Other Products", "desc" => "A few other products from Matchbox", "url" => '/pages/other.php');
//prepro.cgi pub.cgi library.cgi package.cgi

DoResetJavascript();
DoShowHideJavascript('+', '-');
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

DoFoot($pif);

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
    echo "  <td class=\"updown\">\n";
    echo "   <select name=\"$name\" id=\"$id\"";
    echo ">\n";
    $yr = $max;
    while ($yr >= $min) {
	echo "   <option value=\"" . $yr . "\"";
	if ($yr == $defval)
	    echo " selected";
	echo ">" . $yr . "\n";
	$yr = $yr - 1;
    }
    echo "   </select>\n";
    incrsel($id, -1, '');
    echo "  </td>\n";
}


// flags val title desc
function Select($name, $id, $sl, $select_js="", $cl="") {
    echo "   <select name=\"$name\" id=\"$id\"";
    if ($select_js)
	echo " $select_js";
    echo ">\n";
    foreach ($sl as $ent) {
	if (!($ent['flags'] & 1)) {
	    echo "   <option value=\"" . trim($ent['val']) . "\"";
	    if ($ent['flags'] & 64) {
		echo " selected";
	    }
	    echo ">" . $ent['title'];
	    if (arr_get($ent, 'descr', '')) {
		echo " - " . $ent['descr'];
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
	[['flags' => 64, 'val' => '', 'title' => 'Please select a ' . $thing . '.']],
	Fetch($query, $pif),
	$extra), $select_js);
}

function Checks($input, $tag, $name, $values, $sep='<br>') {
    foreach ($values as $val) {
	$id = $tag . '_' . $name . $val[0];
	echo "   <input id=\"$id\" type=\"$input\" name=\"$name\" value=\"$val[0]\"";
	if (arr_get($val, 2, 0))
	    echo " checked";
	echo "> <label for=\"$id\">$val[1]</label>$sep\n";
    }
}

// required: fn tag scr name  optional: reset
function Section($args) {
    global $pif;

    echo "\n<tr><td>";
    echo "\n<br></td></tr>\n<tr id=\"{$args['tag']}\">\n  <td class=\"{$args['tag']}_head sel_head\">\n";
    echo "   <center><h2>{$args['name']}</h2></center>\n  </td>\n </tr>\n";
    echo " <tr><td class=\"spacer\"></td></tr>\n\n <tr><td class=\"{$args['tag']}_body sel_body\">\n";
    if (isset($args['scr'])) {
	echo "<form action=\"/cgi-bin/{$args['scr']}\" method=\"get\" name=\"{$args['tag']}\">\n";
    }
    else {
	echo "<i id=\"{$args['tag']}\"></i>\n";
    }
    if (isset($args['scr'])) {
	echo "Select what kind of Matchbox lineup you would like to see, then click \"SEE THE MODELS\".\n";
	echo "<p>\n";
	call_user_func($args['fn'], $pif);
	echo "<br>\n";
	DoTextButtonSubmit("SEE THE MODELS", "submit");
	DoTextButtonReset($args['tag'], arr_get($args, 'reset', ''));
	if ($pif['isadmin'])
	    Checks('checkbox', $args['tag'], 'verbose', [['1', '<i>Verbose</i>']], ''); 
    }
    else
	call_user_func($args['fn'], $pif);
    if (isset($args['scr'])) {
	echo "\n</form>\n\n";
    }
    echo "  </td>\n </tr>\n";
}

function ChooseRegion($nrows, $tag) {
    $regions = [
	    ['U', 'USA', 1],
	    ['R', 'International'],
	    ['J', 'Japan (1977-1992)'],
	    ['L', 'Latin America (2008-2011)'],
	    ['B', 'UK (2000, 2001)'],
	    ['D', 'Germany (1999-2001)'],
	    ['A', 'Australia (1981, 1987, 1991-1993, 1997, 2000, 2001)']
	];
    echo "    <td rowspan=\"$nrows\">Region:</td>\n";
    echo "    <td rowspan=\"$nrows\">\n";
    Checks('radio', $tag, 'region', $regions);
    echo "</td>\n";
}

function RegionNote() {
    echo "<td colspan=\"2\">Note that Australian dealers might carry either<br>USA or International assortments after 2001.</td>\n";
}

//---- beginning of sections -------------------------------------

function SectionID($pif) {
    echo "\n<table>\n <tr>\n";
    echo "  <td class=\"idtab\">See specific manufacturing ID:</td><td><input type=\"text\" name=\"id\" id=\"idId\" value=\"\" size=\"12\"></td>\n";
    echo " </tr><tr>\n";
    echo "  <td class=\"idtab\">See specific variation ID:</td><td><input type=\"text\" name=\"var\" id=\"idVar\" value=\"\" size=\"12\"> (optional)";
    echo "</td>\n </tr>\n</table>\n";
}

function SectionYear($pif) {
    global $LINE_YEAR_START, $LINE_YEAR_END;

    echo "\n<table>\n <tr>\n  <td>Year: </td>\n";
    SelectYear('year', 'yearYear', $LINE_YEAR_END, $LINE_YEAR_START, $LINE_YEAR_END);
    HorzSpacer(4);
    ChooseRegion(3, 'year');
    #echo "  </td>\n";
    HorzSpacer(4);
    echo "  <td rowspan=\"4\">\n";
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
    Checks('checkbox', 'year', 'lty', $ptypes);
    echo "  </td>\n</tr>\n<tr><td>\n";
    if ($pif['isadmin']) {
	echo " List type:</td><td width=\"180\">\n";
	$sl = [['flags' => 64, 'val' => '', 'title' => 'Normal'],
		['flags' => 0, 'val' => 'txt', 'title' => 'Text'],
		['flags' => 0, 'val' => 'ckl', 'title' => 'Checklist'],
		['flags' => 0, 'val' => 'csv', 'title' => 'CSV'],
		['flags' => 0, 'val' => 'jsn', 'title' => 'JSON']];
	if ($pif['isadmin'])
	    $sl[] = ['flags' => 0, 'val' => 'lrg', 'title' => 'Large'];
	    $sl[] = ['flags' => 0, 'val' => 'myr', 'title' => 'Multi-Year'];
	Select('listtype', 'yrList', $sl);
    } else {
	echo " </td><td width=\"180\">\n";
    }
    echo "  </td>\n</tr>\n<tr><td colspan=\"2\" rowspan=\"2\">\n";
    if ($pif['isadmin']) {
	echo "<p>\n<i>";
	#echo "Number of years: <input type=\"text\" name=\"nyears\" value=\"\" size=\"2\">\n<p>\n";
	Checks('checkbox', 'year', 'unroll', [['1', 'Unroll']], '<p>');
	Checks('checkbox', 'year', 'multi', [['1', 'Multi Only']], '');
	echo "</i>";
    }
    echo " </td></tr>\n<tr>";
    RegionNote();
    echo " </tr>\n</table>\n";
}

function SectionRank($pif) {
    global $LINE_YEAR_START, $LINE_YEAR_END, $MAX_NUMBER;

    echo "<input type=\"hidden\" name=\"byrank\" value=\"1\">";
    echo "<table>\n <tr>\n  <td height=\"32\">Lineup number:<br>(1-$MAX_NUMBER)\n  </td>";
    ChooseNum('num', 'rankSNum', 3, 1, $MAX_NUMBER);
    HorzSpacer(1);
    echo "  <td style=\"text-align: right;\">\nStart year:\n  </td>\n";
    SelectYear('syear', 'rankSyear', $LINE_YEAR_START, $LINE_YEAR_START, $LINE_YEAR_END);
    HorzSpacer(2);
    ChooseRegion(3, 'rank');
    echo "</tr><tr>\n<td>\n";
    if ($pif['isadmin']) {
	echo "<i>Ending number:<br>\n(1-$MAX_NUMBER)</i>\n";
    }
    echo "  </td>\n";
    if ($pif['isadmin'])
	ChooseNum('enum', 'rankENum', 3, 1, $MAX_NUMBER);
    else
	echo "  <td></td>\n";
    HorzSpacer(1);
    echo "  <td style=\"text-align: right;\">End year:</td>\n";
    SelectYear('eyear', 'rankEyear', $LINE_YEAR_END, $LINE_YEAR_START, $LINE_YEAR_END);
    echo " </tr>\n <tr>\n  <td colspan=\"6\" rowspan=\"2\">\n";
    if ($pif['isadmin']) {
	echo "<br><i>\n";
	Checks('checkbox', 'rank', 'large', [['1', 'Large']]);
	Checks('checkbox', 'rank', 'prodpic', [['1', 'Product Pics']], '');
	echo "</i>\n";
    }
    echo "  </td>\n </tr>\n <tr>";
    RegionNote();
    echo " </tr>\n</table>";
}

function SectionManno($pif) {
    global $MAN_YEAR_START, $MAN_YEAR_END;
    echo "<table>\n <tr>\n  <td colspan=\"7\">\n";
    if ($pif['isadmin'])
	$q = "select 0 as flags, id as val, name as title from section where page_id like 'man%' order by display_order";
    else
	$q = "select 0 as flags, id as val, name as title from section where page_id='manno' order by display_order";
    FetchSelect('section', 'manSection', 'range', $q, [['flags' => 0, 'val' => 'all', 'title' => 'All Ranges']]);
    if ($pif['isadmin']) {
	echo "<i>\n";
	Checks('checkbox', 'manno', 'nodesc', [['1', 'No Notes']], ' ');
	Checks('checkbox', 'manno', 'revised', [['1', 'Revised Only']]);
	echo "</i>\n";
    }
    echo "</td><td rowspan=\"3\">\n";
    echo "\n</td></tr><tr>\n<td>";
    Checks('radio', 'manno', 'range', [['all', 'All numbers', 1]]);
    echo "</td>\n<td>";
    Checks('radio', 'manno', 'range', [['some', 'Some numbers']]);
    echo "</td>\n<td>starting at:</td>\n";
    ChooseNum("start", "manStart", 4, 1, "document.getElementById('manEnd').value", 1, 'onFocus="document.manno.range[1].checked=true;"', "document.manno.range[1].checked=true;");

    if ($pif['isadmin']) {
	HorzSpacer(1);
	echo "   <td>Start year:</td>\n";
	SelectYear('syear', 'manSyear', $MAN_YEAR_START, $MAN_YEAR_START, $MAN_YEAR_END);
    }
    echo " </tr>\n <tr><td colspan=\"2\">";
    if ($pif['isadmin']) {
	echo "<i>";
	Checks('checkbox', 'manno', 'large', [['1', 'Large']], '');
	echo "</i>";
    }
    echo "</td>\n";
    echo "  <td>ending at:</td>\n";
    ChooseNum("end", "manEnd", 4, "document.getElementById('manStart').value", 1499, 1499, 'onFocus="document.manno.range[1].checked=true;"', "document.manno.range[1].checked=true;");

    if ($pif['isadmin']) {
	HorzSpacer(1);
	echo "<td>End year:</td>\n";
	SelectYear('eyear', 'manEyear', $MAN_YEAR_END + 1, $MAN_YEAR_START, $MAN_YEAR_END);
    }
    echo " </tr>\n <tr><td colspan=\"4\">List type:\n";
    $sl = [['flags' => 64, 'val' => '', 'title' => 'Normal'],
	   ['flags' => 0, 'val' => 'ckl', 'title' => 'Checklist'],
	   ['flags' => 0, 'val' => 'thm', 'title' => 'Thumbnails'],
	   ['flags' => 0, 'val' => 'csv', 'title' => 'CSV'],
	   ['flags' => 0, 'val' => 'jsn', 'title' => 'JSON']];
    if ($pif['isadmin']) {
	$sl = array_merge($sl, [
		['flags' => 0, 'val' => 'adl', 'title' => 'Admin List'],
		['flags' => 0, 'val' => 'pxl', 'title' => 'Picture List'],
		['flags' => 0, 'val' => 'lnl', 'title' => 'Links List'],
		['flags' => 0, 'val' => 'vtl', 'title' => 'Vehicle Type']]);
	$sl[] = ['flags' => 0, 'val' => 'txt', 'title' => 'Text List'];
    }
    Select('listtype', 'selList', $sl);

    echo "  </td>\n </tr>\n</table>\n";
    echo '<button type="submit" value="+" name="+" class="textbutton" style="width: 16px;" onclick="toggle_visibility(\'ynm\',\'ynm_l\'); return false;" id="ynm_l">+</button>';
    echo " Filter by vehicle type:\n<table class=\"types\" id=\"ynm\">";
    echo " <tr>\n  <td class=\"tdboth\" colspan=\"2\">Every vehicle has one of these.</td>\n";
    echo "  <td class=\"tdboth\" colspan=\"2\">Vehicle may have up to two of these.</td>\n";
    if ($pif['isadmin'])
	echo "  <td class=\"tdboth\" colspan=\"2\"><i>Filter by picture type.</i></td>\n";
    echo " </tr>";

    function YNMCell($arr, $pref) {
	global $pif;

	echo "  <td class=\"tdleft\"><b>$arr[1]</b></td>\n";
//        echo "  <td class=\"tdmiddle\">";
//	if ($pif['isadmin'])
//	    echo "<i>$arr[0]</i>";
//	echo "  </td>\n";
	echo "  <td class=\"tdright\">";
	Checks('radio', 'manno', $pref . $arr[0], [['y', 'yes'], ['n', 'no'], ['m', 'maybe', 1]], '');
	echo "  </td>\n";
    }
    $a = [
	["a", "aircraft"],
	["o", "boat"],
	["n", "building"],
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
	["q", "horse-drawn"],
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
	['x', 'box'],
	['g', 'group']
    ];
    $d = [
	11 => ['s', 'small'],
	12 => ['m', 'medium'],
	13 => ['l', 'large'],
    ];
    foreach(array_keys($a) as $k) {
	echo(" <tr>\n");
	YNMCell($a[$k], 'type_');
	YNMCell($b[$k], 'type_');
	if ($pif['isadmin']) {
	    if (isset($c[$k]))
		YNMCell($c[$k], 'add_');
	    else
		YNMCell($d[$k], 'pic_');
	}
	echo(" </tr>\n");
    }
    echo "</table>\n";
}

function SectionMack($pif) {
    global $MAX_NUMBER;

    echo "<table>\n <tr>\n  <td>\n";
    Checks('radio', 'mack', 'sect', [['all', 'Both sections', 1]]);
    echo "  </td>\n";
    HorzSpacer(3);
    echo "  <td>\n";
    Checks('radio', 'mack', 'range', [['all', 'All numbers', 1]]);
    echo "  </td>\n";
    echo "  <td></td><td></td>\n";
    echo "  <td>Show</td><td>\n";
    Checks('radio', 'mack', 'text', [['pic', 'with pictures', 1], ]);
    echo "  </td>\n </tr>\n <tr>\n  <td>\n";
    Checks('radio', 'mack', 'sect', [['rw', 'Regular Wheels']]);
    echo "  </td>\n  <td>\n";
    Checks('radio', 'mack', 'range', [['some', 'Only numbers']]);
    echo "  </td>\n  <td>starting at:</td>\n";
    ChooseNum('start', 'mackStart', 3, 1, "document.getElementById('mackEnd').value", 1, 'onFocus="document.mack.range[1].checked=true;"', 'document.mack.range[1].checked=true;');
    echo "  <td></td><td>\n";
    Checks('radio', 'mack', 'text', [['txt', 'as text list']]);
    echo " </tr>\n <tr>\n  <td>\n";
    Checks('radio', 'mack', 'sect', [['sf', 'SuperFast']]);
    echo "  </td>\n  <td></td>\n  <td>ending at:</td>\n";
    ChooseNum('end', 'mackEnd', 3, "document.getElementById('mackStart').value", $MAX_NUMBER, $MAX_NUMBER, 'onFocus="document.mack.range[1].checked=true;"', 'document.mack.range[1].checked=true;');
    echo " </tr>\n</table>\n";
}

function SectionMakes($pif) {
    echo "Choose a make:<br>\n<table><tr><td>\n";
    Checks('radio', 'makes', 'make', [['unk', 'unknown', 1], ['unl', 'unlicensed']]);
    Checks('radio', 'makes', 'make', [['text', 'Specific make:']], '');
    echo "<input type=\"text\" name=\"text\" onFocus=\"document.makes.make[2].checked=true;\">\n  </td>\n";
    echo "  <td>Or, <a href=\"../cgi-bin/makes.cgi\">choose from a list!</a></td>\n";
    echo " </tr></table>\n";
}

function SectionSearch($pif) {
    global $MAN_YEAR_START, $MAN_YEAR_END;
    echo "<table><tr><td>\n";
    echo "Search the casting information for:</td><td><input type=\"text\" name=\"query\">\n";
    echo " </td>";
    echo "<tr>\n";
    echo " <tr><td style=\"text-align: right;\">\nStart year:\n  </td>\n";
    SelectYear('syear', 'searchSyear', $MAN_YEAR_START, $MAN_YEAR_START, $MAN_YEAR_END);
    echo " <tr>\n";
    echo " <tr><td style=\"text-align: right;\">End year:</td>\n";
    SelectYear('eyear', 'searchEyear', $MAN_YEAR_END, $MAN_YEAR_START, $MAN_YEAR_END);
    echo "</tr></table>\n";
}

function SectionVSearch($pif) {
    echo "Search the variation information for models containing the following.<p>\n";
    echo "<table><tr>\n";
    HorzSpacer(2);
    echo "<td>\n";
    echo "<table><tr>\n";
    echo "<td>Casting name:</td><td><input type=\"text\" name=\"casting\"></td><td width=\"16\">\n";
    echo "<td>\n";
    Checks('checkbox', 'vsearch', 'codes', [['1', 'Code 1 Models', 1]], '');
    echo "</td></tr>\n";
    echo "<tr><td>Body:</td><td><input type=\"text\" name=\"body\"></td><td></td>\n";
    echo "<td>\n";
    Checks('checkbox', 'vsearch', 'codes', [['2', 'Code 2 Models', 1]], '');
    echo "</td></tr></table>\n";
    echo "</td></tr>\n";
    echo "<tr><td>\n";
    echo '<button type="submit" value="+" name="vsct" class="textbutton" style="width: 16px;" onclick="toggle_visibility(\'vsc\',\'vsc_l\'); return false;" id="vsc_l">+</button>';
    echo "\nOther search criteria:<br>\n";
    echo "<table id=\"vsc\">\n";
    echo "<tr><td>Base:</td><td><input type=\"text\" name=\"base\"></td></tr>\n";
    echo "<tr><td>Interior:</td><td><input type=\"text\" name=\"interior\"></td></tr>\n";
    echo "<tr><td>Wheels:</td><td><input type=\"text\" name=\"wheels\"></td></tr>\n";
    echo "<tr><td>Windows:</td><td><input type=\"text\" name=\"windows\"></td></tr>\n";
    echo "<tr><td>Text:</td><td><input type=\"text\" name=\"text\"></td></tr>\n";
    echo "<tr><td>With:</td><td><input type=\"text\" name=\"with\"></td></tr>\n";
    if ($pif['isadmin']) {
	echo "<tr><td><i>Area:</i></td><td><input type=\"text\" name=\"area\"></td></tr>\n";
	echo "<tr><td><i>Category:</i></td><td><input type=\"text\" name=\"cat\"></td></tr>\n";
	echo "<tr><td><i>Date:</i></td><td><input type=\"text\" name=\"date\"></td></tr>\n";
	echo "<tr><td><i>Note:</i></td><td><input type=\"text\" name=\"note\"></td></tr>\n";
    }
    echo "</table>\n";
    echo "</td></tr></table>\n";
}

function SectionPacks($pif) {
    echo "<table><tr><td>\n";
    FetchSelect('sec', 'packPage', 'pack type', "select flags, id as val, name as title from section where page_id like 'packs.%' and not (flags & 1) order by name");
    echo "</td></tr><tr><td>\n";
    echo "Search the titles for: <input type=\"text\" name=\"title\">\n";
    echo "</td></tr></table>\n";
}

function SectionPubs($pif) {
    echo "<table><tr><td>\n";
    FetchSelect('ty', 'pubPage', 'publication type', "select flags, category as val, name as title from section where page_id like 'pub.%' and not (flags & 1) order by name");
    echo "</td></tr><tr><td>\n";
    echo "Search the titles for: <input type=\"text\" name=\"title\">\n";
    echo "</td></tr></table>\n";
}

function SectionSets($pif) {
    echo "<table><tr><td>\n";
    FetchSelect('page', 'setsPage', 'set', "select flags, id as val, title, description as descr from page_info where format_type='matrix' order by descr");
    if ($pif['isadmin']) {
	echo "  </td>\n";
	echo "  <td>\n";
	Checks('checkbox', 'sets', 'large', [['1', '<i>Large</i>']], '');
    }
    echo "</td></tr></table>\n";
}

function SectionCats($pif) {
    echo "<table><tr><td>\n";
    FetchSelect('cat', 'catsPage', 'category', "select flags, id as val, name as title from category where flags & 4 order by name");
    echo "</td></tr></table>\n";
}


function Quote($x) { return "'" . $x . "'"; }
function SectionBoxes($pif) {
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
	document.getElementById("boxImg").src = "/pic/pub/box/s_" + examples[sel.charCodeAt(0) - 65] + '-' + sel.toLowerCase() +  '.jpg';
	document.getElementById("boxImg").setAttribute('class', "shown");
    }
}
document.addEventListener("DOMContentLoaded", boxExample, false);
</script>
EOT;

    echo "\n<table>\n <tr>\n  <td>Series:</td>\n  <td>";
    Checks('radio', 'boxes', 'series', [['', 'All', 1]], '');
    echo "</td>\n";
    HorzSpacer(1);
    echo "  <td>Model Numbers:</td>\n  <td>Starting at number:</td>\n";
    ChooseNum('start', 'boxStart', 3, 1, 75, 1);
    HorzSpacer(1);
    echo "  <td rowspan=\"5\" id=\"foo\"><img src=\"/pic/pub/box/s_rw01a-a.jpg\" class=\"hidden\" id=\"boxImg\"></td>\n";
    echo " </tr>\n <tr>\n  <td></td>\n  <td>\n";
    Checks('radio', 'boxes', 'series', [['RW', 'Regular Wheels']], '');
    echo "  </td>\n  <td></td>\n  <td></td>\n  <td>Ending at number:</td>\n";
    ChooseNum('end', 'boxEnd', 3, 1, 75, 75);
    echo " </tr>\n <tr>\n  <td></td>\n  <td>\n";
    Checks('radio', 'boxes', 'series', [['SF', 'SuperFast']], '');
    echo "  </td>\n </tr>\n <tr>\n  <td>&nbsp;\n";
    echo "  </td>\n </tr>\n <tr>\n  <td>Styles:</td>\n  <td colspan=\"4\">\n";

    $sl = [['flags' => 64, 'val' => '', 'title' => 'Please select a box style.']];
    foreach ($examples as $ty => $pic) {
	$sl[] = ['flags' => 0, 'val' => $ty, 'title' => $ty . ' type'];
    }
    $sl[] = ['flags' => 0, 'val' => 'all', 'title' => 'All'];
    Select('style', 'boxStyle', $sl, 'onkeyup="boxExample();" onchange="boxExample();" onmouseup="boxExample();"', "boxExample();");
    echo "  </td>\n";
    if ($pif['isadmin']) {
	echo "  <td>\n";
	Checks('checkbox', 'boxes', 'c', [['1', '<i>Compact</i>']], '');
	echo "  </td>\n  <td></td>";
    }
    echo " </tr>\n</table>\n";
}

function SectionCode2($pif) {
    echo "<table><tr><td>\n";
    echo "Choose a type of Code 2 model:\n";
    FetchSelect('section', 'code2Section', 'range', "select flags, id as val, name as title from section where page_id='code2' order by display_order", [['flags' => 0, 'val' => '', 'title' => 'All Sections']]);
    echo "</td></tr></table>\n";
}

function SectionPlant($pif) {
    echo "<table><tr><td>\n";
    echo "Choose a location of manufacture:\n";
    $sl = [
	['flags' => 64, 'val' => '', 'title' => 'Please select a location'],
	['flags' => 0,  'val' => 'BR', 'title' => 'Brazil'],
	['flags' => 0,  'val' => 'BG', 'title' => 'Bulgaria'],
	['flags' => 0,  'val' => 'CN', 'title' => 'China'],
	['flags' => 0,  'val' => 'GB', 'title' => 'England'],
	['flags' => 0,  'val' => 'HK', 'title' => 'Hong Kong'],
	['flags' => 0,  'val' => 'HU', 'title' => 'Hungary'],
	['flags' => 0,  'val' => 'JP', 'title' => 'Japan'],
	['flags' => 0,  'val' => 'MO', 'title' => 'Macau'],
	['flags' => 0,  'val' => 'TH', 'title' => 'Thailand'],
	['flags' => 0,  'val' => 'none', 'title' => 'no origin'],
	['flags' => 0,  'val' => 'unset', 'title' => 'location unknown or not yet set']
    ];
    Select('id', 'plant', $sl);
    echo "</td></tr></table>\n";
}

function SectionOther($pif) {
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
    global $IMG_DIR_ICON;
    echo "<hr>\n";
    echo "<div class=\"bottombar\">\n";
    echo "<div class=\"bamcamark\"><img src=\"$IMG_DIR_ICON/l_bamca-5.gif\"></div>\n";
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
