<?php // DONE
$subtitle = 'TP026A';
// TP26-A BOAT TRANSPORTER, issued 1981
$desc = "Leyland Boat Transporters";
$year = '1981';

$defaults = ['mod' => $subtitle, 'cab' => 'T9CO', 'tlr' => 'CYT08', 'mfg' => 'England', 'cod' => '1'];

include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Blue cab, green windows, silver-gray trailer, beige & red boat
	['var' => '01a', 'liv' => 'none',
            'cdt' => 'blue, green windows',
            'tdt' => 'silver-gray, beige and red boat',
	],
// 2. Blue cab, amber windows, silver-gray trailer, beige & rec boat
	['var' => '02a', 'liv' => 'none',
            'cdt' => 'blue, amber windows',
            'tdt' => 'silver-gray, beige and rec boat',
	],
    ]);
}
?>
