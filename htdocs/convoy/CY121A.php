<?php // DONE
$subtitle = 'CY121A';
$desc = "Flat Bed";
$year = '2008';

$defaults = ['mod' => $subtitle, 'cab' => 'MB725', 'tlr' => 'CYT30', 'cod' => '1'];

$models = [
    ['var' => '01a', 'mfg' => 'Thailand',
	'cdt' => '', 'cva' => '01',
	'tdt' => '',
    ],
    ['var' => '02a', 'mfg' => 'Thailand',
	'cdt' => '', 'cva' => '',
	'tdt' => '',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
