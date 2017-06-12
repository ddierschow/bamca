<!DOCTYPE html>
<html>
<?php
chdir('..');
include "bin/basics.php";
include "config.php";
$pif = GetPageInfo("convoy");
$pif['title'] = $pif['title'] . ' - ' . $subtitle;
DoHead($pif);
?>
  <meta name="author" content="John Baum and Dean Dierschow">
  <meta name="description" content="<?php echo $desc; ?>">
<?php
DoPageHeader($pif);

function show($array, $key) {
    echo arr_get($array, $key, '');
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
    echo '<a href="/cgi-bin/single.cgi?id=' . $mod . '">' . $mod . '</a>';
}

function start_table() {
    echo "<table class=\"outertable\">\n  <tbody>\n";
}

function show_convoy($cy) {
?>
  <tr><td><table class="cytable">
    <tr>
      <td class="enthead">Variation</td><td class="entval"><?php echo $cy['var']; ?></td>
      <td class="entpic" rowspan="7"><?php show_pic($cy['mod'], $cy['var'], arr_get($cy, 'crd', '')); ?></td>
    </tr>
    <tr>
      <td class="enthead">Cab</td><td class="entval"><?php show_cab($cy['cab']); ?></a></td>
    </tr>
    <tr>
      <td class="enthead">Trailer</td><td class="entval"><?php echo $cy['tlr']; ?></td>
    </tr>
    <tr>
      <td class="enthead">Manufacture</td><td class="entval"><?php show($cy, 'mfg'); ?></td>
    </tr>
    <tr>
      <td class="enthead">Livery</td><td class="entval"><?php show($cy, 'liv'); ?></td>
    </tr>
    <tr>
      <td class="enthead">Code</td><td class="entval"><?php show($cy, 'cod'); ?></td>
    </tr>
    <tr>
      <td class="enthead">Rarity</td><td class="entval"><?php show($cy, 'rar'); ?></td>
    </tr>
    <tr>
      <td class="enthead">Cab Detail</td><td class="entval" colspan="2"><?php show($cy, 'cdt'); ?></td>
    </tr>
    <tr>
      <td class="enthead">Trailer Detail</td><td class="entval" colspan="2"><?php show($cy, 'tdt'); ?></td>
    </tr>
<?php if (arr_get($cy, 'nts', '')) { ?>
    <tr>
      <td class="enthead">Notes</td><td class="entval" colspan="2"><?php show($cy, 'nts'); ?></td>
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
?>

<body>
The Matchbox Convoy Project - <?php echo $subtitle; ?> - Under Construction<br>
<br>

<div class="title"><?php echo $subtitle; ?><br>
<?php echo $desc; ?>
</div>
<div class="description"><?php echo $year; ?></div>

<?php body(); ?>

<?php include "convoy/comments.php"; ?>
<br>
<div class="backlink">
<?php DoTextButtonLink('back', '/convoy/series.php'); ?> to the Convoy Index Page
</div>
</body>
</html>
