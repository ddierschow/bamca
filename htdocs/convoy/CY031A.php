<?php // DONE
$subtitle = 'CY031A';
// CY-31-A MACK PIPE TRUCK, issued 1992
$desc = "Mack CH600 Pipe Truck";
$year = '1992';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Red cab, black chassis, red trailer with silver-gray sides, black trailer base, yellow plastic pipes (CS)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB202', 'tlr' => 'Pipe', 'mfg' => 'Thailand',
	    'liv' => 'none', 'cod' => '1', 'rar' => '3',
            'cdt' => 'red, black chassis',
            'tdt' => 'red with silver-gray sides, black base, yellow plastic pipes',
	],
    ]);
}
?>
