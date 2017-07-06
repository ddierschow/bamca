<?php

function show_header($header, $id='') {
?>
    <tr align="center" <?php if ($id) echo ' id="' . $id . '"'; ?>>
      <td valign="top" colspan="2">
	<b><font face="Arial"><?php echo $header; ?></font></b>
      </td>
    </tr>
<?php
}

function show_note_row($text) {
    echo '<tr><td class="cytable enthead" colspan="2">';
    echo $text;
    echo "</td></tr>\n";
}

function show($array, $key, $defaults) {
    echo arr_get2($array, $key, $defaults, '');
}

function show_pic($mod, $var, $pfx, $crd='') {
    $filename = strtolower("/pic/set/convoy/" . $pfx . "_" . $mod . "-" . $var . ".jpg");
    echo strtolower('<a href="/cgi-bin/upload.cgi?d=lib/set/convoy&n=' . $mod . '-' . $var . '">');
    if (file_exists('.' . $filename)) {
	echo '<img src="' . $filename . '">';
	if ($crd) {
	    echo '<br>Photo credit: ' . $crd;
	}
    }
    else {
	echo "picture needed";
	//echo "<br>" . $filename;
    }
    echo '</a>';
    echo "\n";
}

function show_cab($mod, $var) {
    $cabs = [
	'MB425' => 'Mercedes-Benz Actros',
	'MB725' => 'Mercedes-Benz Actros',
	'MB214' => 'Ford Aeromax',
	'MB308' => 'Ford Aeromax Premiere',
	'MB045' => 'Kenworth Cabover Aerodyne',
	'MB309' => 'Kenworth Cabover Aerodyne Premiere',
	'MB103' => 'Kenworth Aerodyne Conventional Cab',
	'MB310' => 'Kenworth Aerodyne Conventional Cab Premiere',
	'MB106' => 'Peterbilt Conventional Sleeper Cab',
	'MB307' => 'Peterbilt Conventional Sleeper Cab Premiere',
	'MB724' => 'Peterbilt Conventional Cab with rooftop lights',
	'MB147' => 'Scania T 142 Cab',
	'MB341' => 'Scania T 142 Cab Premiere',
	'MB183' => 'DAF 3300 Space Cab',
	'MB340' => 'DAF 3300 Space Cab Premiere',
	'MB702' => 'DAF XB95 Space Cab',
	'MB202' => 'Mack CH 600 Cab',
	'MB311' => 'Mack CH 600 Cab Premiere',
	'MB432' => 'Kenworth T2000 Cab',
	'MB318' => 'Kenworth T2000 Cab Premiere',
	'MB664' => 'Generic Tractor Cab',
	'MI724' => 'Peterbilt Conventional Cab with roof lights',
	'CY112' => 'Kenworth T600 Cab',
	'T9CC' => 'Peterbilt Conventional Cab',
	'T9CO' => 'Leyland Cabover',
    ];
    echo '<a href="/cgi-bin/single.cgi?id=' . $mod . '">' . $mod . '</a>';
    if ($var) {
	echo '-<a href="/cgi-bin/vars.cgi?mod=' . $mod . '&var=' . $var . '">' . $var . '</a>';
    }
    if (isset($cabs[$mod])) {
	echo ' - ' . $cabs[$mod];
    }
}

function show_trailer($mod) {
    $trailers = [
//	'MB425' => 'Mercedes-Benz Actros',
	'CYT01' => 'Flat Bed',
	'CYT02' => 'Double Container',
	'CYT03' => 'Covered',
	'CYT04' => 'Container',
	'CYT05' => 'Pipe Transporter',
	'CYT06' => 'Tanker',
	'CYT07' => 'Low Loader',
	'CYT08' => 'Low Loader with Boat',
	'CYT09' => 'Auto Transporter',
	'CYT10' => 'Rocket Transporter',
	'CYT11' => 'Horse Box',
	'CYT12' => 'Airplane Transporter',
	'CYT13' => 'Fire Ladder',
	'CYT14' => 'Boat Transporter',
	'CYT15' => 'Tracking',
	'CYT16' => 'Tipper',
	'CYT17' => 'Racing Transporter',
	'CYT18' => 'Superstar Transporter',
	'CYT19' => 'Airplane Transporter V2',
	'CYT20' => 'Emergency Center',
	'CYT21' => 'Helicopter Transporter',
	'CYT22' => 'Ultra Container',
	'CYT23' => 'Ultra Tanker',
	'CYT24' => 'Racing Cooler',
	'CYT25' => 'Short Container',
	'CYT26' => 'Dinky Heritage Box',
	'CYT27' => "Real Talkin' Box",
	'CYT28' => 'Fishbelly',
	'CYT29' => 'Tanker V2',
	'CYT30' => 'Flat Bed V2',
	'CY010' => 'Racing transporter, part of cab casting',
	'CY030' => 'none',
	'CY047' => 'none',
    ];
//    echo '<a href="/cgi-bin/single.cgi?id=' . $mod . '">' . $mod . '</a>';
//    if (isset($cabs[$mod])) {
//	echo ' - ' . $cabs[$mod];
//    }
    echo arr_get($trailers, $mod, $mod);
}

function start_table() {
    echo "<table class=\"outertable\">\n  <tbody>\n";
}

function show_convoy_corner($cy) {
    global $defaults;
?>
  <tr><td><table class="cytable">
    <tr>
      <td class="enthead">Variation</td><td class="entval"><?php echo $cy['var']; ?></td>
      <td class="entpic" rowspan="7"><?php show_pic(arr_get2($cy, 'mod', $defaults), $cy['var'], 'm', arr_get($cy, 'crd', '')); ?></td>
    </tr>
    <tr>
      <td class="enthead">Cab</td><td class="entval"><?php show_cab(arr_get2($cy, 'cab', $defaults), arr_get($cy, 'cva', '')); ?></td>
    </tr>
    <tr>
      <td class="enthead">Trailer</td><td class="entval"><?php show_trailer(arr_get2($cy, 'tlr', $defaults)); ?></td>
    </tr>
    <tr>
      <td class="enthead">Manufacture</td><td class="entval"><?php show($cy, 'mfg', $defaults); ?></td>
    </tr>
    <tr>
      <td class="enthead">Livery</td><td class="entval"><?php show($cy, 'liv', $defaults); ?></td>
    </tr>
    <tr>
      <td class="enthead">Code</td><td class="entval"><?php show($cy, 'cod', $defaults); ?></td>
    </tr>
    <tr>
      <td class="enthead">Rarity</td><td class="entval"><?php show($cy, 'rar', $defaults); ?></td>
    </tr>
    <tr>
      <td class="enthead">Cab Detail</td><td class="entval" colspan="2"><?php show($cy, 'cdt', $defaults); ?></td>
    </tr>
    <tr>
      <td class="enthead">Trailer Detail</td><td class="entval" colspan="2"><?php show($cy, 'tdt', $defaults); ?></td>
    </tr>
<?php if (arr_get($cy, 'nts', '')) { ?>
    <tr>
      <td class="enthead">Notes</td><td class="entval" colspan="2"><?php show($cy, 'nts', $defaults); ?></td>
    </tr>
<?php } ?>
<?php foreach (arr_get($cy, 'add', []) as $add) { ?>
    <tr>
      <td class="entval"><?php echo $add[0]; ?></td><td class="entpic" colspan="2"><?php echo $add[1]; ?></td>
    </tr>
<?php } ?>
  </table></td></tr>
<?php
}

function show_convoy_wide($cy) {
    global $defaults;
?>
  <tr><td><table class="cytable">
    <tr>
      <td class="enthead">Variation</td><td class="entval"><?php echo $cy['var']; ?></td>
      <td class="enthead">Code</td><td class="entval"><?php show($cy, 'cod', $defaults); ?></td>
    </tr>
    <tr>
      <td class="entpic" colspan="4"><?php show_pic(arr_get2($cy, 'mod', $defaults), $cy['var'], 'h', arr_get($cy, 'crd', '')); ?></td>
    </tr>
    <tr>
      <td class="enthead">Cab</td><td class="entval"><?php show_cab(arr_get2($cy, 'cab', $defaults), arr_get($cy, 'cva', '')); ?></td>
      <td class="enthead">Cab Detail</td><td class="entval" colspan="2"><?php show($cy, 'cdt', $defaults); ?></td>
    </tr>
    <tr>
      <td class="enthead">Trailer</td><td class="entval"><?php show_trailer(arr_get2($cy, 'tlr', $defaults)); ?></td>
      <td class="enthead">Trailer Detail</td><td class="entval" colspan="2"><?php show($cy, 'tdt', $defaults); ?></td>
    </tr>
    <tr>
      <td class="enthead">Livery</td><td class="entval"><?php show($cy, 'liv', $defaults); ?></td>
      <td class="enthead">Manufacture</td><td class="entval"><?php show($cy, 'mfg', $defaults); ?></td>
    </tr>
<?php if (arr_get($cy, 'rar')) { ?>
    <tr>
      <td class="enthead">Rarity</td><td class="entval"><?php show($cy, 'rar', $defaults); ?></td>
      <td colspan="2"></td>
    </tr>
<?php } ?>
<?php if (arr_get($cy, 'nts', '')) { ?>
    <tr>
      <td class="enthead">Notes</td><td class="entval" colspan="3"><?php show($cy, 'nts', $defaults); ?></td>
    </tr>
<?php } ?>
<?php foreach (arr_get($cy, 'add', []) as $add) { ?>
    <tr>
      <td class="entval"><?php echo $add[0]; ?></td><td class="entpic" colspan="3"><?php echo $add[1]; ?></td>
    </tr>
<?php } ?>
  </table></td></tr>
<?php
}

function show_convoy_tall($cy) {
    global $defaults;

$rows = 9;
if (arr_get($cy, 'nts', '')) {
    $rows += 1;
}
$rows += count(arr_get($cy, 'add', []));
?>
  <tr><td><table class="cytable">
    <tr>
      <td class="enthead">Variation</td><td class="entval"><?php echo $cy['var']; ?></td>
      <td class="entpic" rowspan="<?php echo $rows; ?>"><?php show_pic(arr_get2($cy, 'mod', $defaults), $cy['var'], 'm', arr_get($cy, 'crd', '')); ?></td>
    </tr>
    <tr>
      <td class="enthead">Cab</td><td class="entval"><?php show_cab(arr_get2($cy, 'cab', $defaults), arr_get($cy, 'cva', '')); ?></td>
    </tr>
    <tr>
      <td class="enthead">Trailer</td><td class="entval"><?php show_trailer(arr_get2($cy, 'tlr', $defaults)); ?></td>
    </tr>
    <tr>
      <td class="enthead">Manufacture</td><td class="entval"><?php show($cy, 'mfg', $defaults); ?></td>
    </tr>
    <tr>
      <td class="enthead">Livery</td><td class="entval"><?php show($cy, 'liv', $defaults); ?></td>
    </tr>
    <tr>
      <td class="enthead">Code</td><td class="entval"><?php show($cy, 'cod', $defaults); ?></td>
    </tr>
    <tr>
      <td class="enthead">Rarity</td><td class="entval"><?php show($cy, 'rar', $defaults); ?></td>
    </tr>
    <tr>
      <td class="enthead">Cab Detail</td><td class="entval"><?php show($cy, 'cdt', $defaults); ?></td>
    </tr>
    <tr>
      <td class="enthead">Trailer Detail</td><td class="entval"><?php show($cy, 'tdt', $defaults); ?></td>
    </tr>
<?php if (arr_get($cy, 'nts', '')) { ?>
    <tr>
      <td class="enthead">Notes</td><td class="entval"><?php show($cy, 'nts', $defaults); ?></td>
    </tr>
<?php } ?>
<?php foreach (arr_get($cy, 'add', []) as $add) { ?>
    <tr>
      <td class="entval"><?php echo $add[0]; ?></td><td class="entpic"><?php echo $add[1]; ?></td>
    </tr>
<?php } ?>
  </table></td></tr>
<?php
}

function end_table() {
    echo "  </tbody>\n</table>\n";
}

function show_table($models) {
    start_table();
    foreach ($models as $model) {
	show_convoy_corner($model);
    }
    end_table();
}

function link_if_exists($fn, $text='', $hash='', $dir='convoy/') {
    if (!$text)
	$text = $fn;
    if (file_exists($dir . $fn . '.php')) {
	echo '<a href="' . $fn . '.php';
	if ($hash)
	    echo '#' . $hash;
	echo '">' . $text . '</a>';
    }
    else {
	echo '<i>' . $text . '</i>';
    }
}

function show_tmtc($prod) {
    show_header($prod['id'] . ' - ' . $prod['name'] . ' - ' . $prod['year'], $prod['id']);
    foreach ($prod['models'] as $model) {
	if (isset($model['note'])) {
	    show_note_row($model['note']);
	}
	else if ($prod['fmt'] == 'wide') {
	    show_convoy_wide($model);
	}
	else {
	    show_convoy_tall($model);
	}
    }
}
?>
