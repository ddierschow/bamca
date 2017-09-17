<?php // DONE
$subtitle = 'CY009B';
// CY-9-B KENWORTH T2000 CONTAINER TRUCK, issued 2000
$desc = "Matchbox Kenworth T2000 Box";
$year = '2000';

$defaults = ['mod' => $subtitle, 'tlr' => 'CYT04', 'mfg' => 'China', 'cod' => '1'];

// NOTE: Below models with chrome interior, 8-spoke wheels, & China casting.
$models = [
// 1. Red cab with chrome base, clear windows, white container, roof & rear doors, white trailer chassis, "McDonald's" labels 
    ['var' => '01a', 'cab' => 'MB432', 'liv' => "McDonald's", 'rar' => '2',
	'cdt' => 'red with black chassis, chrome base and interior, clear windows', 'cva' => '07',
	'tdt' => "white container, chassis, roof and rear doors, MCDONALD'S labels",
    ],
// 2. Silver-gray cab with gray base, yellow windows, brown container, roof and rear doors, brown trailer chassis, "Hershey's King Size" labels 
    ['var' => '02a', 'cab' => 'MB432', 'liv' => "Hershey", 'rar' => '2',
	'cdt' => 'silver-gray with gray base, yellow windows', 'cva' => '06',
	'tdt' => "brown container, roof and rear doors, brown chassis, HERSHEY'S KING SIZE labels",
    ],
// 3. Red cab with black base, clear windows, black container and rear doors with red roof, black trailer chassis, "McDonald's" labels (ROW)
    ['var' => '03a', 'cab' => 'MB432', 'liv' => "McDonald's", 'rar' => '2',
	'cdt' => 'red with black base, clear windows', 'cva' => '07',
	'tdt' => "black container and rear doors with red roof, black chassis, MCDONALD'S labels",
    ],
// 4. Red cab with chrome base, clear windows, red container and rear doors with red roof, black trailer chassis, "The Pause that Refreshes-Coca Cola" tempa, chrome disc with rubber tires (PC)
    ['var' => '04a', 'cab' => 'MB318', 'liv' => "Coca-Cola", 'rar' => '2',
	'cdt' => 'red cab with chrome base, clear windows', 'cva' => '',
	'tdt' => 'red container and rear doors with red roof, black chassis, THE PAUSE THAT REFRESHES-COCA COLA" tampo',
    ],
    ['var' => '05a', 'cab' => 'MB318', 'liv' => "Coca-Cola", 'rar' => '2',
	'cdt' => 'green with black lower, black chassis, silver base and exhaust with black interior, clear windows, COCA COLA CALENDAR GIRLS tampo', 'cva' => '',
	'tdt' => 'black base, green box and doors, dark blue roof, MARCH AND APRIL 1947 calendar labels, nail head hitch pin',
    ],
    ['var' => '06a', 'cab' => 'MB318', 'liv' => "Coca-Cola", 'rar' => '2',
	'cdt' => 'red with white lower, white chassis, silver base and exhaust with white interior, clear windows. COCA COLA CALENDAR GIRLS tampo', 'cva' => '',
	'tdt' => 'white base and roof, red box and doors, "MAY and JUNE 1947 calendar lables, nail head hitch pin',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
