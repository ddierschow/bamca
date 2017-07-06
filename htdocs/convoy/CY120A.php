<?php // DONE
$subtitle = 'CY120A';
$desc = "DAF Space Cab with Fishbelly";
$year = '2007';

$defaults = ['mod' => $subtitle, 'cab' => 'MB702', 'tlr' => 'CYT28', 'mfg' => 'Thailand', 'cod' => '1'];

$models = [
    ['var' => '01a', 'liv' => 'Wheaties',
	'cdt' => 'white', 'cva' => '02',
	'tdt' => 'white',
    ],
    ['var' => '02a', 'liv' => 'Simpson Racing',
	'cdt' => 'red', 'cva' => '04',
	'tdt' => 'silver-gray',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
