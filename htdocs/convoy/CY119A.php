<?php // DONE
$subtitle = 'CY119A';
$desc = "Tractor Cab with Flat Bed V2";
$year = '2007';

$defaults = ['mod' => $subtitle, 'cab' => 'MB664', 'tlr' => 'Flat Bed V2', 'mfg' => 'Thailand',
	    'liv' => 'none', 'cod' => '1', 'rar' => ''];

include "cypage.php";

function body() {
    show_table([
	['var' => '01a',
            'cdt' => 'green-gold',
            'tdt' => 'silver-gray, pipes',
	],
	['var' => '02a',
            'cdt' => 'black',
            'tdt' => 'silver-gray, containers, CARGO',
	],
    ]);
}
?>
