<!DOCTYPE html>
<html>
<?php
include "bin/basics.php";
include "config.php";
include "bin/forms.php";
$pif = GetPageInfo("database", 1);
DoHead($pif);
$pif['isadmin'] = CheckPerm($pif, 'a');
$pif['hierarchy'][0] = ['/', 'Home'];
$pif['hierarchy'][1] = ['/database.php', 'Database'];
$pif['ncols'] = 1;

$sections = [
    ["sep" => "t"],
    ["tag" => "ss", "name" => "<a href=\"search.php\">Super Search is now available!</a>", "fn" => ''],
    ["tag" => "id", "name" => "Specific Model ID", "fn" => 'SectionID', "scr" => "msearch.cgi"],
    ["tag" => "year", "name" => "Year", "fn" => 'SectionYear', "scr" => "lineup.cgi"],
    ["tag" => "rank", "name" => "Lineup Number", "fn" => 'SectionRank', "scr" => "lineup.cgi"],
    ["tag" => "manno", "name" => "MAN Number", "fn" => 'SectionManno', "scr" => "manno.cgi"],
    ["tag" => "mack", "name" => "Mack Number", "fn" => 'SectionMack', "scr" => "mack.cgi"],
    ["tag" => "makes", "name" => "Make", "fn" => 'SectionMakes', "scr" => "makes.cgi"],
    ["sep" => "c"],
    ["tag" => "search", "name" => "Text Search", "fn" => 'SectionSearch', "scr" => "msearch.cgi"],
    ["tag" => "vsearch", "name" => "Variation Text Search", "fn" => 'SectionVSearch', "scr" => "vsearch.cgi"],
    ["tag" => "packs", "name" => "Multi-Model Packs", "fn" => 'SectionPacks', "scr" => "packs.cgi"],
    ["tag" => "pubs", "name" => "Publications", "fn" => 'SectionPubs', "scr" => "pub.cgi", "perm" => $pif['isadmin']],
    ["tag" => "sets", "name" => "Special Sets", "fn" => 'SectionSets', "scr" => "matrix.cgi"],
    ["tag" => "cats", "name" => "Categories", "fn" => 'SectionCats', "scr" => "cats.cgi"],
    ["tag" => "boxes", "name" => "Lesney Era Boxes", "fn" => 'SectionBoxes', "scr" => "boxart.cgi", 'reset' => 'boxExample();'],
    ["tag" => "code2", "name" => "Code 2 Models", "fn" => 'SectionCode2', "scr" => "code2.cgi"],
    ["tag" => "plants", "name" => "Location of Manufacture", "fn" => 'SectionPlant', "scr" => "plants.cgi"],
    ["sep" => "b"],
    ["tag" => "other", "name" => "Other Database Pages", "fn" => 'SectionOther'],
    ["sep" => "e"],
];

$pages = [
    ["title" => "About", "desc" => "About this website", "url" => '/pages/about.php'],
    ["title" => "Toy Links", "desc" => "Links to other sites of interest", "url" => '/cgi-bin/links.cgi'],
    ["title" => "Bibliograpy", "desc" => "Books relevant to collectors", "url" => '/cgi-bin/biblio.cgi'],
    ["title" => "Comparisons", "desc" => "Between various Matchbox castings", "url" => '/cgi-bin/compare.cgi'],
    ["title" => "Errors", "desc" => "Matchbox manufacturing errors", "url" => '/cgi-bin/errors.cgi'],
    ["title" => "Ads", "desc" => "Matchbox advertising", "url" => '/cgi-bin/ads.cgi'],
    ["title" => "Customizations", "desc" => "Customizaed Matchbox toys", "url" => '/cgi-bin/custom.cgi'],
    ["title" => "Photographers", "desc" => "Contributors to this site", "url" => '/cgi-bin/photogs.cgi'],
    ["title" => "Other Products", "desc" => "A few other products from Matchbox", "url" => '/pages/other.php'],
];
//prepro.cgi pub.cgi library.cgi package.cgi

DoResetJavascript();
DoShowHideJavascript('+', '-');
DoIncDecJavascript();
DoPageHeader($pif);

echo "<hr><p>\n";
echo "<div class=\"maintable\"><center><ul class=\"header-links\">\n";
foreach ($sections as $sec) {
    if (array_key_exists("fn", $sec) && $sec['fn'] && (!array_key_exists("perm", $sec) || $sec["perm"]))
        echo " <li class=\"header-link-item\"><a href=\"#{$sec['tag']}\" class=\"textbutton\">";
        echo "&nbsp;By {$sec['name']}&nbsp;</a></li>\n";
}
echo "</ul></center></div>\n\n";

foreach ($sections as $sec) {
    if (array_key_exists("perm", $sec)) {
        $sec['name'] = "<i>{$sec['name']}</i>";
    }
    if (!array_key_exists("sep", $sec)) {
        if (!array_key_exists("perm", $sec) || $sec["perm"])
            Section($pif, $sec);
    }
    else if ($sec["sep"] == 't') {
        echo "<table width=\"100%\"><tr><td width=\"" . (100 / $pif['ncols']) . "%\">\n<table>\n";
    }
    else if ($sec["sep"] == 'c' && $pif['ncols'] == 2) {
        echo "</table>\n</td>\n<td width=\"50%\">\n<table>\n";
    }
    else if ($sec["sep"] == 'b' && $pif['ncols'] == 2) {
        echo "</table>\n</td></tr>\n<tr><td colspan=\"2\">\n<table>\n";
    }
    else if ($sec["sep"] == 'e') {
        echo "</table>\n</td></tr></table>\n";
    }
}

PageFooter("database");
DoPageFooter($pif);
DoFoot($pif);

//---- support functions -----------------------------------------

function HorzSpacer($rowspan) {
    echo '  <td class="hspacer"';
    if ($rowspan > 1)
	echo ' rowspan="' . $rowspan . '"';
    echo "></td>\n\n";
}

function FetchSelect($pif, $name, $id, $thing, $query, $extra=[], $select_js="") {
    Select($name, $id, array_merge(
	[['flags' => 64, 'val' => '', 'title' => 'Please select a ' . $thing . '.']],
	Fetch($query, $pif),
	$extra), $select_js);
}

// required: fn tag scr name  optional: reset
function Section($pif, $args) {
    echo "\n<tr><td>\n<br></td></tr>\n";
    echo "<tr id=\"{$args['tag']}\">\n  <td class=\"{$args['tag']}_head sel_head\">\n";
    echo "   <center><h2>{$args['name']}</h2></center>\n  </td>\n </tr>\n";
    if (!$args['fn'])
        return;  // no fn means no body section
    echo " <tr><td class=\"spacer\"></td></tr>\n\n <tr><td class=\"{$args['tag']}_body sel_body\">\n";
    if (isset($args['scr'])) {
	echo "<form action=\"/cgi-bin/{$args['scr']}\" method=\"get\" name=\"{$args['tag']}\">\n";
    }
    else {   // no script means no form
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

//---- beginning of sections -------------------------------------

function SectionID($pif) {
    echo "\n<table>\n <tr>\n";
    echo "  <td class=\"idtab\">See specific manufacturing ID:</td>";
    echo "<td><input type=\"text\" name=\"id\" id=\"idId\" value=\"\" size=\"12\"></td>\n";
    echo " </tr><tr>\n";
    echo "  <td class=\"idtab\">See specific variation ID:</td>";
    echo "<td><input type=\"text\" name=\"var\" id=\"idVar\" value=\"\" size=\"12\"> (optional)";
    echo "</td>\n </tr>\n</table>\n";
}

function SectionYear($pif) {
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

    echo "\n<table>\n <tr>\n  <td>Year: </td>\n";
    SelectYear('year', 'yearYear', $pif['line_year_end'], $pif['line_year_start'], $pif['line_year_end']);
    HorzSpacer(4);
    ChooseRegion(3, 'year');
    echo "  </td>\n";
    // HorzSpacer(4);
    echo "</tr>\n<tr><td>\n";
    echo " List type:</td><td width=\"180\">\n";
    $sl = [['flags' => 64, 'val' => '', 'title' => 'Normal'],
            ['flags' => 0, 'val' => 'txt', 'title' => 'Text'],
            ['flags' => 0, 'val' => 'ckl', 'title' => 'Checklist'],
            ['flags' => 0, 'val' => 'csv', 'title' => 'CSV'],
            ['flags' => 0, 'val' => 'jsn', 'title' => 'JSON']];
    if ($pif['isadmin']) {
        $sl[] = ['flags' => 0, 'val' => 'lrg', 'title' => 'Large'];
        $sl[] = ['flags' => 0, 'val' => 'myr', 'title' => 'Multi-Year'];
    }
    Select('listtype', 'yrList', $sl);
    echo "  </td>\n</tr>\n<tr>"; //<td colspan=\"2\" rowspan=\"2\">\n";
    echo "  <td colspan=\"2\" rowspan=\"2\">\n";
    Checks('checkbox', 'year', 'lty', $ptypes);
    echo "  </td>\n";
    //echo " </td></tr>\n<tr>";
    /*if ($pif['isadmin']) {
	echo "<p>\n<i>";
	//echo "Number of years: <input type=\"text\" name=\"nyears\" value=\"\" size=\"2\">\n<p>\n";
	Checks('checkbox', 'year', 'unroll', [['1', 'Unroll']], '<p>');
	Checks('checkbox', 'year', 'multi', [['1', 'Multi Only']], '');
	echo "</i>";
    }*/
    echo "</tr><tr>";
    RegionNote();
    echo " </tr>\n</table>\n";
}

function SectionRank($pif) {
    $MAX_NUMBER = $pif['max_number'];

    echo "<input type=\"hidden\" name=\"byrank\" value=\"1\">";
    echo "<table>\n <tr>\n  <td height=\"32\">Lineup&nbsp;number:<br>(1-$MAX_NUMBER)\n  </td>";
    ChooseNum('num', 'rankSNum', 3, 1, $pif['max_number']);
    HorzSpacer(6);
    ChooseRegion(4, 'rank');
    echo "</tr><tr>\n<td>\n";
    if ($pif['isadmin']) {
	echo "<i>Ending&nbsp;number:<br>\n(1-$MAX_NUMBER)</i>\n";
    }
    echo "  </td>\n";
    if ($pif['isadmin'])
	ChooseNum('enum', 'rankENum', 3, 1, $pif['max_number']);
    else
	echo "  <td>&nbsp;</td>\n";
    echo "</tr><tr>\n";
    echo "  <td style=\"text-align: right;\">\nStart year:\n  </td>\n";
    SelectYear('syear', 'rankSyear', $pif['line_year_start'], $pif['line_year_start'], $pif['line_year_end']);
    echo "</tr><tr>\n";
    echo "  <td style=\"text-align: right;\">End year:</td>\n";
    SelectYear('eyear', 'rankEyear', $pif['line_year_end'], $pif['line_year_start'], $pif['line_year_end']);
    echo " </tr>\n <tr>\n  <td colspan=\"2\" rowspan=\"2\">\n";
    if ($pif['isadmin']) {
	echo "<i>\n";
	Checks('checkbox', 'rank', 'large', [['1', '<i>Large</i>']]);
	Checks('checkbox', 'rank', 'prodpic', [['1', '<i>Product Pics</i>']], '');
	echo "</i>\n";
    }
    echo "  </td>\n";
    RegionNote();
    echo " </tr>\n</table>";
}

function SectionManno($pif) {
    echo "<table>\n <tr>\n  <td colspan=\"7\">\n";
    if ($pif['isadmin'])
	$q = "select 0 as flags, id as val, name as title from section where page_id like 'man%' order by display_order";
    else
	$q = "select 0 as flags, id as val, name as title from section where page_id='manno' order by display_order";
    FetchSelect($pif, 'section', 'manSection', 'range', $q, [['flags' => 0, 'val' => 'all', 'title' => 'All Ranges']]);
    if ($pif['isadmin']) {
	Checks('checkbox', 'manno', 'nodesc', [['1', '<i>No Notes</i>']], ' ');
	Checks('checkbox', 'manno', 'revised', [['1', '<i>Revised Only</i>']]);
    }
    echo "</td><td rowspan=\"3\">\n";
    echo "\n</td></tr><tr>\n<td>";
    Checks('radio', 'manno', 'range', [['all', 'All numbers', 1]]);
    echo "</td>\n<td>";
    Checks('radio', 'manno', 'range', [['some', 'Some numbers']]);
    echo "</td>\n<td>starting at:</td>\n";
    ChooseNum("start", "manStart", 4, 1, "document.getElementById('manEnd').value", 1,
        'onFocus="document.manno.range[1].checked=true;"', "document.manno.range[1].checked=true;");

    if ($pif['isadmin']) {
	HorzSpacer(1);
	echo "   <td><i>Start year:</i></td>\n";
	SelectYear('syear', 'manSyear', $pif['man_year_start'], $pif['man_year_start'], $pif['man_year_end']);
    }
    echo " </tr>\n <tr><td colspan=\"2\">";
    echo "</td>\n";
    echo "  <td>ending at:</td>\n";
    ChooseNum("end", "manEnd", 4, "document.getElementById('manStart').value", 9999, 9999,
        'onFocus="document.manno.range[1].checked=true;"', "document.manno.range[1].checked=true;");

    if ($pif['isadmin']) {
        HorzSpacer(2);
        echo "<td><i>End year:</i></td>\n";
        SelectYear('eyear', 'manEyear', $pif['man_year_end'] + 1, $pif['man_year_start'], $pif['man_year_end']);
    }
    echo " </tr>\n <tr><td colspan=\"4\">List type:\n";
    $sl = [['flags' => 64, 'val' => '', 'title' => 'Normal'],
	   ['flags' => 0, 'val' => 'ckl', 'title' => 'Checklist'],
	   ['flags' => 0, 'val' => 'thm', 'title' => 'Thumbnails'],
	   ['flags' => 0, 'val' => 'csv', 'title' => 'CSV'],
	   ['flags' => 0, 'val' => 'jsn', 'title' => 'JSON'],
           ['flags' => 0, 'val' => 'vcs', 'title' => 'CSV with Variations']];
    if ($pif['isadmin']) {
	$sl = array_merge($sl, [
		['flags' => 0, 'val' => 'adl', 'title' => 'Admin List'],
		['flags' => 0, 'val' => 'pxl', 'title' => 'Picture List'],
		['flags' => 0, 'val' => 'lnl', 'title' => 'Links List'],
		['flags' => 0, 'val' => 'vtl', 'title' => 'Vehicle Type']]);
	$sl[] = ['flags' => 0, 'val' => 'txt', 'title' => 'Text List'];
    }
    Select('listtype', 'selList', $sl);
    echo "</td><td colspan=2>\n";
    if ($pif['isadmin']) {
	Checks('checkbox', 'manno', 'large', [['1', '<i>Large</i>']], '');
    }

    echo "  </td>\n </tr>\n</table>\n";
    echo '<button type="submit" value="+" name="+" class="textbutton" style="width: 16px;" ';
    echo 'onclick="toggle_visibility(\'ynm\',\'ynm_l\'); return false;" id="ynm_l">+</button>';
    echo " Filter by vehicle type:\n";
    YNMTable($pif, 'manno', 'ynm', $pif['isadmin']);
}

function SectionMack($pif) {
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
    ChooseNum('start', 'mackStart', 3, 1, "document.getElementById('mackEnd').value", 1,
        'onFocus="document.mack.range[1].checked=true;"', 'document.mack.range[1].checked=true;');
    echo "  <td></td><td>\n";
    Checks('radio', 'mack', 'text', [['txt', 'as text list']]);
    echo " </tr>\n <tr>\n  <td>\n";
    Checks('radio', 'mack', 'sect', [['sf', 'SuperFast']]);
    echo "  </td>\n  <td></td>\n  <td>ending at:</td>\n";
    ChooseNum('end', 'mackEnd', 3, "document.getElementById('mackStart').value", $pif['max_number'], $pif['max_number'],
        'onFocus="document.mack.range[1].checked=true;"', 'document.mack.range[1].checked=true;');
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
    echo "<table><tr><td>\n";
    echo "Search the casting information for:</td><td><input type=\"text\" name=\"query\">\n";
    echo " </td>";
    echo "<tr>\n";
    echo " <tr><td style=\"text-align: right;\">\nStart year:\n  </td>\n";
    SelectYear('syear', 'searchSyear', $pif['man_year_start'], $pif['man_year_start'], $pif['man_year_end']);
    echo " <tr>\n";
    echo " <tr><td style=\"text-align: right;\">End year:</td>\n";
    SelectYear('eyear', 'searchEyear', $pif['man_year_end'], $pif['man_year_start'], $pif['man_year_end']);
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
    echo '<button type="submit" value="+" name="vsct" class="textbutton" style="width: 16px;" ';
    echo 'onclick="toggle_visibility(\'vsc\',\'vsc_l\'); return false;" id="vsc_l">+</button>';
    echo "\nOther search criteria:<br>\n";
    echo "<table id=\"vsc\">\n";
    SimpleText('Base:', 'base');
    SimpleText('Interior:', 'Interior');
    SimpleText('Wheels:', 'Wheels');
    SimpleText('Windows:', 'windows');
    SimpleText('Text:', 'text');
    SimpleText('With:', 'with');
    if ($pif['isadmin']) {
        SimpleText('<i>Area:</i>', 'area');
        SimpleText('<i>Category:</i>', 'cat');
        SimpleText('<i>Date:</i>', 'date');
        SimpleText('<i>Note:</i>', 'note');
    }
    echo "</table>\n";
    echo "</td></tr></table>\n";
}

function SectionPacks($pif) {
    echo "<table><tr><td colspan=\"2\">\n";
    FetchSelect($pif, 'sec', 'packPage', 'pack type',
        "select flags, id as val, name as title from section where page_id like 'packs.%' and not (flags & 1) order by name");
    echo "</td></tr>\n";
    SimpleText("Search the titles for:", "title");
    echo "</table>\n";
}

function SectionPubs($pif) {
    echo "<table><tr><td colspan=\"2\">\n";
    FetchSelect($pif, 'ty', 'pubPage', 'publication type',
        "select flags, category as val, name as title from section where page_id like 'pub.%' and not (flags & 1) order by name");
    echo "</td></tr>\n";
    SimpleText("Search the titles for:", "title");
    echo "</table>\n";
}

function SectionSets($pif) {
    echo "<table><tr><td>\n";
    FetchSelect($pif, 'page', 'setsPage', 'set',
        "select flags, id as val, title, description as descr from page_info where format_type='matrix' order by descr");
    if ($pif['isadmin']) {
	echo "  </td>\n";
	echo "  <td>\n";
	Checks('checkbox', 'sets', 'large', [['1', '<i>Large</i>']], '');
    }
    echo "</td></tr></table>\n";
}

function SectionCats($pif) {
    echo "<table><tr><td>\n";
    FetchSelect($pif, 'cat', 'catsPage', 'category',
        "select flags, id as val, name as title from category where flags & 4 order by name");
    echo "</td></tr></table>\n";
}


function Quote($x) { return "'{$x}'"; }
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
    Select('style', 'boxStyle', $sl,
        'onkeyup="boxExample();" onchange="boxExample();" onmouseup="boxExample();"', "boxExample();");
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
    FetchSelect($pif, 'section', 'code2Section', 'range',
        "select flags, id as val, name as title from section where page_id='code2' order by display_order",
        [['flags' => 0, 'val' => '', 'title' => 'All Sections']]);
    echo "</td></tr></table>\n";
}

function SectionPlant($pif) {
    echo "<table><tr><td>\n";
    echo "Choose a location of manufacture:\n";
    SelectPlant('Please select a location', 'plants');
    echo "</td></tr></table>\n";
}

function SectionOther($pif) {
    global $IMG_DIR_ART, $pages;
    echo "<div class='paget'>\n";
    foreach ($pages as $page) {
	echo "<div class='pagec'><center>\n";
	echo "<div class='othertitle'>{$page['title']}";
	echo "<p><div class='otherdesc'>{$page['desc']}</div>\n";
	echo "</div>\n";
	DoTextButtonLink("VIEW THE PAGE", $page['url']);
	echo "</center></div>\n";
    }
    echo "</div>\n";
}

//---- end of sections -------------------------------------------

?>
</html>
