<?php // DONE
$subtitle = 'CY032A';
// CY-32-A MACK SHOVEL TRANSPORTER, issued 1992
$desc = "Mack with Lowboy trailer";
$year = '1992';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Orange-yellow cab, red chassis, red trailer, MB029 Tractor Shovel in yellow with red shovel (CS)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB202', 'tlr' => 'Lowboy', 'mfg' => 'Thailand',
	    'liv' => 'none', 'cod' => '1', 'rar' => '3',
            'cdt' => 'orange-yellow, red chassis',
            'tdt' => 'red, MB029 Tractor Shovel in yellow with red shovel',
	],
    ]);
}
?>
