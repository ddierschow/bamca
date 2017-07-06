<?php // DONE
$subtitle = 'CY119A';
$desc = "Tractor Cab with Flat Bed V2";
$year = '2007';

$defaults = ['mod' => $subtitle, 'cab' => 'MB664', 'tlr' => 'CYT30', 'mfg' => 'Thailand',
	    'liv' => 'none', 'cod' => '1', 'rar' => ''];

$models = [
    ['var' => '01a',
	'cdt' => 'green-gold', 'cva' => '16',
	'tdt' => 'silver-gray, pipes',
    ],
    ['var' => '02a',
	'cdt' => 'black', 'cva' => '18',
	'tdt' => 'silver-gray, containers, CARGO',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
