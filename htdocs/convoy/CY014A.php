<?php // DONE
$subtitle = 'CY014A';
// CY-14-A KENWORTH BOAT TRANSPORTER, issued 1985
$desc = "Kenworth COE Boat Transporter";
$year = '1985';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. White cab, white boat, pearly silver trailer with brown cradle 
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB045', 'tlr' => 'Boat transporter', 'mfg' => 'Macau',
	    'liv' => 'none', 'cod' => '1', 'rar' => '3',
            'cdt' => 'white',
            'tdt' => 'pearly silver trailer with brown cradle, white boat',
	],
    ]);
}
?>
