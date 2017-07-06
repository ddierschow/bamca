<?php // DONE
$subtitle = 'CY115A';
$desc = "Ford Aeromax with Fishbelly";
$year = '2005';

$defaults = ['mod' => $subtitle, 'cab' => 'MB214', 'tlr' => 'CYT28', 'cod' => '1'];

$models = [
    ['var' => '01a', 'mfg' => 'Macau', 'liv' => 'DHL ',
	'cdt' => 'yellow', 'cva' => '101',
	'tdt' => 'yellow, DHL',
	'nts' => '2005 Convoy Wheels ',
    ],
    ['var' => '02a', 'mfg' => 'Macau', 'liv' => 'Michelin',
	'cdt' => 'dark blue', 'cva' => '',
	'tdt' => 'dark blue, MICHELIN',
	'nts' => '2005 Convoy Wheels',
    ],
    ['var' => '03a', 'mfg' => 'Macau', 'liv' => 'McDonalds',
	'cdt' => 'red', 'cva' => '',
	'tdt' => 'red, MCDONALDS',
	'nts' => '2005 Convoy Wheels ',
    ],
    ['var' => '04a', 'mfg' => 'Macau', 'liv' => 'DHL ',
	'cdt' => 'yellow', 'cva' => '',
	'tdt' => 'yellow, DHL',
	'nts' => '2006 Convoy Wheels ',
    ],
    ['var' => '05a', 'mfg' => 'Macau', 'liv' => 'Michelin',
	'cdt' => 'dark blue', 'cva' => '',
	'tdt' => 'dark blue, MICHELIN',
	'nts' => '2006 Convoy Wheels',
    ],
    ['var' => '06a', 'mfg' => 'Thailand', 'liv' => 'McDonalds',
	'cdt' => 'red', 'cva' => '',
	'tdt' => 'red, MCDONALDS',
	'nts' => '2006 Convoy Wheels',
    ],
    ['var' => '07a', 'mfg' => 'Thailand', 'liv' => 'Land Rover G4',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, LAND ROVER G4 CHALLENGE',
	'nts' => '2006 Convoy Wheels',
    ],
    ['var' => '08a', 'mfg' => 'Thailand', 'liv' => 'Honey Nut Cherrios',
	'cdt' => '', 'cva' => '',
	'tdt' => '',
	'nts' => '2006 Convoy Wheels',
    ],
    ['var' => '09a', 'mfg' => 'China', 'liv' => 'Firestone Racing',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, FIRESTONE RACING',
	'nts' => '2006 Convoy Wheels',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
