<?php // DONE
$subtitle = 'CY007C';
// CY-7-C DAF GAS TANKER, issued 2001 (ROW)
$desc = "DAF Tankers";
$year = '2001';

$defaults = ['mod' => $subtitle];

include "cypage.php";

function body() {
    show_table([
// 1. Green and white cab with silver-gray chassis, green and white tank with silver-gray chassis, "BP" tempa, 8-spoke wheels
	['var' => '01a',
	    'cab' => 'MB183', 'tlr' => 'CYT06', 'mfg' => 'China',
	    'liv' => 'BP', 'cod' => '1', 'rar' => '2',
            'cdt' => 'green and white, silver-gray chassis',
            'tdt' => 'silver-gray with green and white tank, 8 spoke wheels, BP tampo',
	],
    ]);
}
?>
