<?php // DONE
$subtitle = 'CY014A';
// CY-14-A KENWORTH BOAT TRANSPORTER, issued 1985
$desc = "Kenworth COE Boat Transporter";
$year = '1985';

$defaults = ['mod' => $subtitle];

$models = [
// 1. White cab, white boat, pearly silver trailer with brown cradle 
    ['var' => '01a',
	'cab' => 'MB045', 'tlr' => 'CYT14', 'mfg' => 'Macau',
	'liv' => 'none', 'cod' => '1', 'rar' => '3',
	'cdt' => 'white, dark and light blue stripes', 'cva' => '022A',
	'tdt' => 'pearly silver trailer with brown cradle, white boat',
    ],
    ['var' => '01b',
	'cab' => 'MB045', 'tlr' => 'CYT14', 'mfg' => 'Macau',
	'liv' => 'none', 'cod' => '1', 'rar' => '3',
	'cdt' => 'white, medium and light blue stripes', 'cva' => '022B',
	'tdt' => 'pearly silver trailer with brown cradle, white boat',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
