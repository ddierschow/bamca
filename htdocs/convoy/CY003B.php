<?php // DONE
$subtitle = 'CY003B';
// CY-3-B KENWORTH BOX TRUCK, issued 1985 (AU)
$desc = "Kenworth Box Truck";
$year = '1985';

$defaults = ['mod' => $subtitle];

include "cypage.php";

function body() {
    show_table([
// 1. Red cab, red container, yellow trailer, "Linfox" tempa, Macau casting (AU)
	['var' => '01a',
	    'cab' => 'MB045', 'tlr' => 'CYT04', 'mfg' => 'Macau',
	    'liv' => 'Linfox', 'cod' => '1', 'rar' => '',
            'cdt' => 'red',
            'tdt' => 'yellow, red container, LINFOX tampo',
	],
    ]);
}
?>
