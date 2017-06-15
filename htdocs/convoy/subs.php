<?php
function show($array, $key, $defaults) {
    echo arr_get2($array, $key, $defaults, '');
}

function show_pic($mod, $var, $crd='') {
    $filename = strtolower("/pic/convoy/m_" . $mod . "_" . $var . ".jpg");
    echo strtolower('<a href="/cgi-bin/upload.cgi?d=lib/convoy&n=' . $mod . '_' . $var . '">');
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

function show_cab($mod) {
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
	'CY112' => 'Kenworth T600 Cab',
	'T9CC' => 'Peterbilt Conventional Cab',
	'T9CO' => 'Leyland Cabover',
    ];
    echo '<a href="/cgi-bin/single.cgi?id=' . $mod . '">' . $mod . '</a>';
    if (isset($cabs[$mod])) {
	echo ' - ' . $cabs[$mod];
    }
}

function start_table() {
    echo "<table class=\"outertable\">\n  <tbody>\n";
}

function show_convoy($cy) {
    global $defaults;
?>
  <tr><td><table class="cytable">
    <tr>
      <td class="enthead">Variation</td><td class="entval"><?php echo $cy['var']; ?></td>
      <td class="entpic" rowspan="7"><?php show_pic(arr_get2($cy, 'mod', $defaults), $cy['var'], arr_get($cy, 'crd', '')); ?></td>
    </tr>
    <tr>
      <td class="enthead">Cab</td><td class="entval"><?php show_cab(arr_get2($cy, 'cab', $defaults)); ?></td>
    </tr>
    <tr>
      <td class="enthead">Trailer</td><td class="entval"><?php echo arr_get2($cy, 'tlr', $defaults); ?></td>
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

function end_table() {
    echo "  </tbody>\n</table>\n";
}

function show_table($models) {
    start_table();
    foreach ($models as $model) {
	show_convoy($model);
    }
    end_table();
}

function link_if_exists($fn, $text='', $dir='convoy/') {
    if (!$text)
	$text = $fn;
    if (file_exists($dir . $fn . '.php')) {
	echo '<a href="' . $fn . '.php">' . $text . '</a>';
    }
    else {
	echo '<i>' . $text . '</i>';
    }
}
?>
