<?php // DONE
$subtitle = 'CY026A';
// CY-26-A DAF DOUBLE CONTAINER TRUCK, issued 1989
$desc = "DAF Double Container Truck";
$year = '1989';

$defaults = ['mod' => $subtitle, 'cab' => 'MB183', 'tlr' => 'CYT02', 'cod' => '1'];

$models = [
// 1. Powder blue cab, black chassis, dark blue containers with black trailer, "P and 0" tempa, Macau casting 
    ['var' => '01a', 'mfg' => 'Macau', 'liv' => 'P and O',
	'cdt' => 'powder blue, black chassis', 'cva' => '09',
	'tdt' => 'black, dark blue containers, P AND 0 tampo',
    ],
// 2. Powder blue cab, black chassis, dark blue containers with black trailer, "P and 0" tempa, Thailand casting 
    ['var' => '02a', 'mfg' => 'Thailand', 'liv' => 'P and O',
	'cdt' => 'powder blue, black chassis', 'cva' => '28',
	'tdt' => 'black, dark blue containers, P AND 0 tampo',
    ],
// 3. Powder blue cab, black chassis, dark blue containers with black trailer, "P and 0" tempa, China casting 
    ['var' => '03a', 'mfg' => 'China', 'liv' => 'P and O',
	'cdt' => 'powder blue, black chassis', 'cva' => '49',
	'tdt' => 'black, dark blue containers, P AND 0 tampo',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
