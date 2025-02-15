<?php // DONE
$subtitle = 'CY032A';
// CY-32-A MACK SHOVEL TRANSPORTER, issued 1992
$desc = "Mack with Lowboy trailer";
$year = '1992';

$defaults = ['mod' => $subtitle, 'cab' => 'MB202', 'tlr' => 'CYT07', 'cod' => '1'];

$models = [
// 1. Orange-yellow cab, red chassis, red trailer, MB029 Tractor Shovel in yellow with red shovel (CS)
    ['var' => '01a', 'mfg' => 'Thailand', 'liv' => 'none', 'rar' => '3',
	'cdt' => 'orange-yellow, red chassis', 'cva' => '15',
	'tdt' => 'red, MB029 Tractor Shovel in yellow with red shovel',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
