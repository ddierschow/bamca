<?php // DONE
$subtitle = 'CY031A';
// CY-31-A MACK PIPE TRUCK, issued 1992
$desc = "Mack CH600 Pipe Truck";
$year = '1992';

$defaults = ['mod' => $subtitle, 'cab' => 'MB202', 'tlr' => 'CYT05', 'cod' => '1'];

$models = [
// 1. Red cab, black chassis, red trailer with silver-gray sides, black trailer base, yellow plastic pipes (CS)
    ['var' => '01a', 'mfg' => 'Thailand', 'liv' => 'none', 'rar' => '3',
	'cdt' => 'red, black chassis', 'cva' => '17',
	'tdt' => 'red with silver-gray sides, black base, yellow plastic pipes',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
