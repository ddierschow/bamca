<?php // DONE
$subtitle = 'CY003B';
// CY-3-B KENWORTH BOX TRUCK, issued 1985 (AU)
$desc = "Kenworth Box Truck";
$year = '1985';

$defaults = ['mod' => $subtitle];

$models = [
// 1. Red cab, red container, yellow trailer, "Linfox" tempa, Macau casting (AU)
    ['var' => '01a',
	'cab' => 'MB045', 'tlr' => 'CYT04', 'mfg' => 'Macau',
	'liv' => 'Linfox', 'cod' => '1', 'rar' => '039',
	'cdt' => 'red', 'cva' => '039',
	'tdt' => 'yellow, red container, LINFOX tampo',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
