<?php // DONE
$subtitle = 'CY121A';
$desc = "Flat Bed";
$year = '2008';

$defaults = ['mod' => $subtitle, 'cab' => 'MB725', 'tlr' => 'CYT30', 'cod' => '1'];

$models = [
    ['var' => '01a', 'mfg' => 'Thailand',
	'cdt' => 'yellow and orange', 'cva' => '01',
	'tdt' => 'silver-gray',
    ],
    ['var' => '02a', 'mfg' => 'Thailand',
	'cdt' => 'white and blue', 'cva' => '',
	'tdt' => 'blue',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
