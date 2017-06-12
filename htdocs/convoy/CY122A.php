<?php // DONE
$subtitle = 'CY122A';
$desc = "DAF Space Cab with Flatbed";
$year = '20??';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB702', 'tlr' => 'Box', 'mfg' => 'Macau',
	    'liv' => 'Cargo', 'cod' => '1', 'rar' => '',
            'cdt' => 'maroon',
            'tdt' => 'silver-gray, containers, CARGO',
	],
    ]);
}
?>
