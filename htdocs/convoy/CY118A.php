<?php // DONE
$subtitle = 'CY118A';
$desc = "DAF XF95 with Tanker V2";
$year = '2006';

$defaults = ['mod' => $subtitle];

$models = [
// 1. Red cab, red container, yellow trailer, "Linfox" tempa, Macau casting (AU)
    ['var' => '01a', 'cab' => 'MB702', 'tlr' => 'CYT29', 'mfg' => 'Thailand',
	'liv' => 'Jet', 'cod' => '1', 'rar' => '',
	'cdt' => 'yellow', 'cva' => '05',
	'tdt' => 'yellow, JET',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
