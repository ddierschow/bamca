<?php // DONE
$subtitle = 'CY002B';
// CY-2-B KENWORTH T2000 ROCKET TRANSPORTER, issued 1999
$desc = "Kenworth T2000 Rocket Transporters";
$year = '1999';

$defaults = ['mod' => $subtitle];

$models = [
// 1. Black cab with white tempa with clear windows & chrome base, chrome plastic rocket, black trailer, 8-spoke wheels, China casting (GR)
    ['var' => '01a', 'cab' => 'MB432', 'tlr' => 'CYT10', 'mfg' => 'China',
	'liv' => 'none', 'cod' => '1', 'rar' => '',
	'cdt' => 'black, white stripes, silver base, exhaust, and trim', 'cva' => '',
	'tdt' => 'black with chrome rocket',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
