<?php // DONE
$subtitle = 'CY002B';
// CY-2-B KENWORTH T2000 ROCKET TRANSPORTER, issued 1999
$desc = "Kenworth T2000 Rocket Transporters";
$year = '1999';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Black cab with white tempa with clear windows & chrome base, chrome plastic rocket, black trailer, 8-spoke wheels, China casting (GR)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB432', 'tlr' => 'Rocket Transporter', 'mfg' => 'China',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'black, white stripes, silver base, exhaust, and trim',
            'tdt' => 'black with chrome rocket',
	],
    ]);
}
?>
