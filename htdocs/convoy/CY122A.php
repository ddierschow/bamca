<?php // DONE
$subtitle = 'CY122A';
$desc = "DAF Space Cab with Flatbed";
$year = '2008';

$defaults = ['mod' => $subtitle];

include "cypage.php";

function body() {
    show_table([
	['var' => '01a',
	    'cab' => 'MB702', 'tlr' => 'CYT30', 'mfg' => 'Macau',
	    'liv' => 'Cargo', 'cod' => '1', 'rar' => '',
            'cdt' => 'maroon',
            'tdt' => 'silver-gray, containers, CARGO',
	],
    ]);
}
?>
