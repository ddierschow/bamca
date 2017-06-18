<?php // DONE
$subtitle = 'CY019A';
// CY-19-A PETERBILT BOX TRUCK, issued 1987
$desc = "PeterbiltBox Truck";
$year = '1987';

$defaults = ['mod' => $subtitle];
include "cypage.php";

function body() {
    show_table([
// 1. White cab, white container with pearly silver base, "Ansett Wridgways" tempa 
	['var' => '01a', 'cab' => 'MB106', 'tlr' => 'Box', 'mfg' => 'Macau',
	    'liv' => 'Ansett Wridgways', 'cod' => '1', 'rar' => '',
            'cdt' => 'white',
            'tdt' => 'white container with pearly silver base, ANSETT WRIDGWAYS tampo',
	],
    ]);
}
?>