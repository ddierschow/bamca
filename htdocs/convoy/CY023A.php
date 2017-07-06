<?php // DONE
$subtitle = 'CY023A';
// CY-23-A SCANIA COVERED TRUCK, issued 1988
$desc = "Scania Covered Truck";
$year = '1988';

$defaults = ['mod' => $subtitle, 'cab' => 'MB147', 'tlr' => 'CYT03', 'mfg' => 'Macau', 'cod' => '1'];

$models = [
// 1. Yellow cab, blue chassis with chrome base, yellow canopy with blue sides on pearly silver base, "Michelin" tempa 
    ['var' => '01a', 'liv' => 'Michelin',
	'cdt' => 'yellow, blue chassis with chrome base', 'cva' => '24',
	'tdt' => 'yellow canopy with blue sides on pearly silver base, MICHELIN tampo', 
    ],
// 2. Yellow cab, blue chassis with black base, yellow canopy with blue sides on pearly silver trailer, "Michelin" tempa 
    ['var' => '02a', 'liv' => 'Michelin',
	'cdt' => 'yellow, blue chassis with black base', 'cva' => '35',
	'tdt' => 'yellow canopy with blue sides on pearly silver base, MICHELIN tampo', 
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
