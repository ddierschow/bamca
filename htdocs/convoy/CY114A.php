<?php // DONE
$subtitle = 'CY114A';
$desc = "Tractor Cab with Finshbelly";
$year = '2005';

$defaults = ['mod' => $subtitle, 'cab' => 'MB664', 'tlr' => 'CYT28', 'cod' => '1'];

$models = [
    ['var' => '01a', 'mfg' => 'China', 'liv' => 'Jeep',
	'cdt' => 'black', 'cva' => '04',
	'tdt' => 'black, JEEP',
	'nts' => '2005 Convoy Wheels',
    ],
    ['var' => '02a', 'mfg' => 'China', 'liv' => 'Sonic',
	'cdt' => 'pearly white', 'cva' => '03',
	'tdt' => 'pearly white, SONIC',
	'nts' => '2005 Convoy Wheels',
    ],
    ['var' => '03a', 'mfg' => 'China', 'liv' => 'Yu-Gi-Oh',
	'cdt' => 'dark blue', 'cva' => '05',
	'tdt' => 'dark blue, YU-GI-OH',
	'nts' => '2005 Convoy Wheels',
    ],
    ['var' => '04a', 'mfg' => 'Thailand', 'liv' => 'Yamaha',
	'cdt' => 'black', 'cva' => '10',
	'tdt' => 'black, YAMAHA',
	'nts' => '2006 Convoy Wheels',
    ],
    ['var' => '05a', 'mfg' => 'Thailand', 'liv' => 'Good Year',
	'cdt' => 'lemon', 'cva' => '09',
	'tdt' => 'dark blue, JEEP',
	'nts' => '2006 Convoy Wheels',
    ],
    ['var' => '06a', 'mfg' => 'Thailand', 'liv' => 'Mario Kart',
	'cdt' => 'red', 'cva' => '08',
	'tdt' => 'yellow, MARIOKART',
	'nts' => '2006 Convoy Wheels',
    ],
    ['var' => '07a', 'mfg' => 'Thailand', 'liv' => 'Land Rover',
	'cdt' => 'black', 'cva' => '10',
	'tdt' => 'black, LAND ROVER G4',
	'nts' => '2006 Convoy Wheels',
    ],
    ['var' => '08a', 'mfg' => 'Thailand', 'liv' => 'Matchbox',
	'cdt' => 'black, tan chassis', 'cva' => '07',
	'tdt' => 'black, MATCHBOX',
	'nts' => "2005 Convoy Wheels - Mummy's Gold Set",
    ],
    ['var' => '09a', 'mfg' => 'Thailand', 'liv' => '"M" Construction',
	'cdt' => 'dark yellow', 'cva' => '11',
	'tdt' => 'dark yellow, M CONSTRUCTION',
	'nts' => '2005 Convoy Wheels - Construction Set',
    ],
    ['var' => '10a', 'mfg' => 'Thailand', 'liv' => 'McDonalds',
	'cdt' => 'red', 'cva' => '08',
	'tdt' => 'red, MCDONALDS',
    ],
    ['var' => '11a', 'mfg' => 'Thailand', 'liv' => 'Yamaha',
	'cdt' => 'blue', 'cva' => '05',
	'tdt' => 'blue, YAMAHA',
    ],
    ['var' => '12a', 'mfg' => 'Thailand', 'liv' => 'McDonalds',
	'cdt' => 'lemon', 'cva' => '09',
	'tdt' => 'blue, MCDONALDS',
    ],
    ['var' => '13a', 'mfg' => 'Thailand', 'liv' => 'Matchbox',
	'cdt' => 'beige', 'cva' => '22',
	'tdt' => 'dark green, MATCHBOX',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
