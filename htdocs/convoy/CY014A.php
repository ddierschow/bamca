<?php // DONE
$subtitle = 'CY014A';
// CY-14-A KENWORTH BOAT TRANSPORTER, issued 1985
$desc = "Kenworth COE Boat Transporter";
$year = '1985';

$defaults = ['mod' => $subtitle];

include "cypage.php";

function body() {
    show_table([
// 1. White cab, white boat, pearly silver trailer with brown cradle 
	['var' => '01a',
	    'cab' => 'MB045', 'tlr' => 'CYT14', 'mfg' => 'Macau',
	    'liv' => 'none', 'cod' => '1', 'rar' => '3',
            'cdt' => 'white',
            'tdt' => 'pearly silver trailer with brown cradle, white boat',
	],
    ]);
}
?>
