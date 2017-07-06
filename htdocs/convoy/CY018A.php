<?php // DONE
$subtitle = 'CY018A';
// CY-18-A SCANIA DOUBLE CONTAINER TRUCK, issued 1986
$desc = "Scania Double Container Truck";
$year = '1986';

$defaults = ['mod' => $subtitle, 'cab' => 'MB147', 'tlr' => 'CYT02', 'cod' => '1'];

$models = [
// 1. Blue cab with black interior, yellow chassis, dark blue containers, yellow trailer base, "Varta Batteries" tampo
    ['var' => '01a', 'mfg' => 'Macau', 'liv' => 'Varta',
	'cdt' => 'blue with black interior, yellow chassis', 'cva' => '07',
	'tdt' => 'dark blue containers, yellow base, VARTA BATTERIES tampo',
    ],
// 2. Blue cab with gray interior, yellow chassis, dark blue containers, yellow trailer base, "Varta Batteries" tampo
    ['var' => '02a', 'mfg' => 'Macau', 'liv' => 'Varta',
	'cdt' => 'blue with gray interior, yellow chassis', 'cva' => '06',
	'tdt' => 'dark blue containers, yellow base, VARTA BATTERIES tampo',
    ],
// 3. White cab, dark blue chassis, white containers, dark blue trailer base, "Wall's Ice Cream" tampo (UK)
    ['var' => '03a', 'mfg' => 'Macau', 'liv' => "Wall's",
	'cdt' => 'white cab, dark blue chassis', 'cva' => '14',
	'tdt' => "white containers, dark blue base, WALL'S ICE CREAM tampo",
    ],
// 4. Red cab and chassis, red containers, red trailer base, "Kit Kat" tampo (UK)
    ['var' => '04a', 'mfg' => 'Macau', 'liv' => 'Kit Kat',
	'cdt' => 'red, red chassis', 'cva' => '12',
	'tdt' => 'red containers, red base, KIT KAT tampo',
    ],
// 5. Orange cab, brown chassis, orange containers, brown trailer base, "Breakaway" tampo (UK)
    ['var' => '05a', 'mfg' => 'Macau', 'liv' => 'Breakaway',
	'cdt' => 'orange, brown chassis', 'cva' => '18',
	'tdt' => 'orange containers, brown base, BREAKAWAY tampo',
    ],
// 6. White cab, green chassis, white containers, green trailer base, "7 Up" tampo (UK)
    ['var' => '06a', 'mfg' => 'Macau', 'liv' => '7 Up',
	'cdt' => 'white, green chassis', 'cva' => '23',
	'tdt' => 'white containers, green base, 7 UP tampo',
    ],
// 7. Red cab, black chassis, red containers, black trailer base, "Beefeater Steak Houses" tampo (UK)
    ['var' => '07a', 'mfg' => 'Macau', 'liv' => 'Beefeater',
	'cdt' => 'red, black chassis', 'cva' => '27',
	'tdt' => 'red containers, black base, BEEFEATER STEAK HOUSES tampo',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
