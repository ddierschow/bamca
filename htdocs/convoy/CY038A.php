<?php // DONE
$subtitle = 'CY038A';
// CY-38-A KENWORTH CONTAINER TRUCK, issued 1993
$desc = "Kenworth Container Truck";
$year = '1993';

$defaults = ['mod' => $subtitle];

    $models = [
// 1. MB45-C cab in black, black container, "Matchbox Racing 5" labels 
	['var' => '01a', 'cab' => 'MB045', 'tlr' => 'CYT17', 'mfg' => 'Macau',
	    'liv' => 'Matchbox', 'cod' => '1', 'rar' => '',
            'cdt' => 'black', 'cva' => '069',
            'tdt' => 'black container, MATCHBOX RACING 5 labels',
	],
    ];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
