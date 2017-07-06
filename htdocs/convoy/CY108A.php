<?php // DONE
$subtitle = 'CY108A';
// CY-108-A DAF AIRCRAFT TRANSPORTER, issued 1992
$desc = "DAF Modified Airplane Transporter";
$year = '1992';

$defaults = ['mod' => $subtitle];

$models = [
// 1. Red cab, red carriage with red trailer base; SB37-A Hawk with roundels & white stripe livery 
    ['var' => '01a', 'cab' => 'MB183', 'tlr' => 'CYT19', 'mfg' => 'Thailand',
	'liv' => 'Royal Air Force', 'cod' => '1', 'rar' => '3',
	'cdt' => 'red', 'cva' => '34',
	'tdt' => 'red carriage with red trailer base, SB37A Hawk with roundels and white stripe livery',
	'nts' => 'Issued as "give-a-way" without airplane (RAF BAe Hawk T MK1)',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
