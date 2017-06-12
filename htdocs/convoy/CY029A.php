<?php // DONE
$subtitle = 'CY029A';
// CY-29-A MACK AIRCRAFT TRANSPORTER, issued 1991
$desc = "Mack Aircraft Transporter";
$year = '1991';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Red cab, black chassis, white carriage with black trailer, red plane with "Red Rebels" tampo 
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB202', 'tlr' => 'Aircraft Transporter', 'mfg' => 'Thailand',
	    'liv' => 'Red Rebels', 'cod' => '1', 'rar' => '',
            'cdt' => 'red, black chassis',
            'tdt' => 'black with white carriage, red plane with RED REBELS tampo',
	],
    ]);
}
?>
