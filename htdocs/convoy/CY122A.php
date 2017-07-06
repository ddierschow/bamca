<?php // DONE
$subtitle = 'CY122A';
$desc = "DAF Space Cab with Flatbed";
$year = '2008';

$defaults = ['mod' => $subtitle];

$models = [
    ['var' => '01a',
	'cab' => 'MB702', 'tlr' => 'CYT30', 'mfg' => 'Macau',
	'liv' => 'Cargo', 'cod' => '1', 'rar' => '',
	'cdt' => 'maroon', 'cva' => '03',
	'tdt' => 'silver-gray, containers, CARGO',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
