<?php

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

function Checks($input, $tag, $name, $values, $sep='<br>') {
    foreach ($values as $val) {
	$id = $tag . '_' . $name . $val[0];
	echo "   <input id=\"$id\" type=\"$input\" name=\"$name\" value=\"$val[0]\"";
	if (arr_get($val, 2, 0))
	    echo " checked";
	echo "> <label for=\"$id\">$val[1]</label>$sep\n";
    }
}

function YNMCell($pif, $arr, $pref, $sec) {
    echo "  <td class=\"tdleft\"><b>$arr[1]</b></td>\n";
    echo "  <td class=\"tdright\">";
    Checks('radio', $sec, $pref . $arr[0], [['y', 'yes'], ['n', 'no'], ['m', 'maybe', 1]], '');
    echo "  </td>\n";
}

function YNMTable($pif, $sec, $tableid, $with_admin=0) {
    $vt_a = [
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
    $vt_b = [
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
    $vt_c = [
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
    $vt_d = [
        11 => ['s', 'small'],
        12 => ['m', 'medium'],
        13 => ['l', 'large'],
    ];

    echo "<table class=\"types\" id=\"" . $tableid . "\">";
    echo " <tr>\n  <td class=\"tdboth\" colspan=\"2\">Every vehicle has one of these.</td>\n";
    echo "  <td class=\"tdboth\" colspan=\"2\">Vehicle may have up to two of these.</td>\n";
    if ($with_admin)
       echo "  <td class=\"tdboth\" colspan=\"2\"><i>Filter by picture type.</i></td>\n";
    echo " </tr>";
    foreach(array_keys($vt_a) as $k) {
	echo(" <tr>\n");
	YNMCell($pif, $vt_a[$k], 'type_', $sec);
	YNMCell($pif, $vt_b[$k], 'type_', $sec);
	if ($with_admin) {
	    if (isset($vt_c[$k]))
		YNMCell($pif, $vt_c[$k], 'add_', $sec);
	    else
		YNMCell($pif, $vt_d[$k], 'pic_', $sec);
	}
	echo(" </tr>\n");
    }
    echo "</table>\n";
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
    echo "<td colspan=\"2\">Note that Australian dealers might carry either USA or International assortments after 2001.</td>\n";
}

function SelectPlant($blank, $sec) {
    $sl = [
	['flags' => 64, 'val' => '', 'title' => $blank],
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
    Select('plant', $sec, $sl);
}

function SimpleText($label, $name, $colspan=1) {
    echo "<tr><td>" . $label . "</td><td";
    if ($colspan > 1) {
        echo ' colspan=' . $colspan;
    }
    echo "><input type=\"text\" name=\"" . $name . "\"></td></tr>\n";
}

?>
