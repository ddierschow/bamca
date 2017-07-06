<?php // DONE
$subtitle = 'CY116A';
$desc = "Ford Aeromax with Tanker V2";
$year = '2006';

$defaults = ['mod' => $subtitle, 'cab' => 'MB214', 'tlr' => 'CYT29', 'cod' => '1'];

$models = [
    ['var' => '01a', 'mfg' => 'Thailand', 'liv' => 'Shell',
	'cdt' => 'silver-gray', 'cva' => '',
	'tdt' => 'silver-gray, SHELL',
    ],
    ['var' => '02a', 'mfg' => 'Thailand', 'liv' => 'Conoco',
	'cdt' => 'white', 'cva' => '116',
	'tdt' => 'gray, CONOCO',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
