<?php // DONE
$subtitle = 'CY026A';
// CY-26-A DAF DOUBLE CONTAINER TRUCK, issued 1989
$desc = "DAF Double Container Truck";
$year = '1989';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Powder blue cab, black chassis, dark blue containers with black trailer, "P and 0" tempa, Macau casting 
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB183', 'tlr' => 'Double Container', 'mfg' => 'Macau',
	    'liv' => 'P and O', 'cod' => '1', 'rar' => '',
            'cdt' => 'powder blue, black chassis',
            'tdt' => 'black, dark blue containers, P AND 0 tampo',
	],
// 2. Powder blue cab, black chassis, dark blue containers with black trailer, "P and 0" tempa, Thailand casting 
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB183', 'tlr' => 'Double Container', 'mfg' => 'Thailand',
	    'liv' => 'P and O', 'cod' => '1', 'rar' => '',
            'cdt' => 'powder blue, black chassis',
            'tdt' => 'black, dark blue containers, P AND 0 tampo',
	],
// 3. Powder blue cab, black chassis, dark blue containers with black trailer, "P and 0" tempa, China casting 
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB183', 'tlr' => 'Double Container', 'mfg' => 'China',
	    'liv' => 'P and O', 'cod' => '1', 'rar' => '',
            'cdt' => 'powder blue, black chassis',
            'tdt' => 'black, dark blue containers, P AND 0 tampo',
	],
    ]);
}
?>
