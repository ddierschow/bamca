<?php // DONE
$subtitle = 'CY021B';
// CY-21-B SCANIA PLANE TRANSPORTER, issued 2000 (ROW)
$desc = "Scania Plane Transporter";
$year = '2000';

$defaults = ['mod' => $subtitle];

include "cypage.php";

function body() {

    show_table([
// 1. Bright blue cab with black chassis and chrome base, blue trailer, yellow plane with three black jets tempa, "Mattel" & China (ROW)
	['var' => '01a', 'cab' => 'MB147', 'tlr' => 'CYT12', 'mfg' => 'China, MATTEL',
	    'liv' => 'none', 'cod' => '1', 'rar' => '3',
            'cdt' => 'bright blue with black chassis, chrome base',
            'tdt' => 'blue trailer, yellow plane with three black jets tempa',
	],
    ]);
}
?>
