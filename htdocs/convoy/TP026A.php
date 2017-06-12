<?php // DONE
$subtitle = 'TP026A';
// TP26-A BOAT TRANSPORTER, issued 1981
$desc = "Leyland Boat Transporters";
$year = '1981';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Blue cab, green windows, silver-gray trailer, beige & red boat
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'T9CO', 'tlr' => 'Boat Transporter', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'blue cab, green windows',
            'tdt' => 'silver-gray trailer, beige and red boat',
	],
// 2. Blue cab, amber windows, silver-gray trailer, beige & rec boat
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'T9CO', 'tlr' => 'Boat Transporter', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'blue cab, amber windows',
            'tdt' => 'silver-gray trailer, beige and rec boat',
	],
    ]);
}
?>
