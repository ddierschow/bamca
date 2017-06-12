<?php // DONE
$subtitle = 'CY119A';
$desc = "Tractor Cab with Flat Bed V2";
$year = '20??';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB664', 'tlr' => 'Flat Bed V2', 'mfg' => 'Thailand',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'green-gold',
            'tdt' => 'silver-gray, pipes',
	],
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB664', 'tlr' => 'Flat Bed V2', 'mfg' => 'Thailand',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'black',
            'tdt' => 'silver-gray, containers, CARGO',
	],
    ]);
}
?>
