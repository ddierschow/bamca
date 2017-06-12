<?php // DONE
$subtitle = 'CY023A';
// CY-23-A SCANIA COVERED TRUCK, issued 1988
$desc = "Scania Covered Truck";
$year = '1988';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Yellow cab, blue chassis with chrome base, yellow canopy with blue sides on pearly silver base, "Michelin" tempa 
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB147', 'tlr' => 'Covered Trailer', 'mfg' => 'Macau',
	    'liv' => 'Michelin', 'cod' => '1', 'rar' => '',
            'cdt' => 'yellow, blue chassis with chrome base',
            'tdt' => 'yellow canopy with blue sides on pearly silver base, MICHELIN tampo', 
	],
// 2. Yellow cab, blue chassis with black base, yellow canopy with blue sides on pearly silver trailer, "Michelin" tempa 
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB147', 'tlr' => 'Covered Trailer', 'mfg' => 'Macau',
	    'liv' => 'Michelin', 'cod' => '1', 'rar' => '',
            'cdt' => 'yellow, blue chassis with black base',
            'tdt' => 'yellow canopy with blue sides on pearly silver base, MICHELIN tampo', 
	],
    ]);
}
?>
