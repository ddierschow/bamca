<?php // DONE
$subtitle = 'CY029A';
// CY-29-A MACK AIRCRAFT TRANSPORTER, issued 1991
$desc = "Mack Aircraft Transporter";
$year = '1991';

$defaults = ['mod' => $subtitle, 'cab' => 'MB202', 'tlr' => 'CYT12'];

$models = [
// 1. Red cab, black chassis, white carriage with black trailer, red plane with "Red Rebels" tampo 
    ['var' => '01a', 'mfg' => 'Thailand', 'liv' => 'Red Rebels', 'cod' => '1',
	'cdt' => 'red, black chassis', 'cva' => '10',
	'tdt' => 'black with white carriage, red plane with RED REBELS tampo',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
