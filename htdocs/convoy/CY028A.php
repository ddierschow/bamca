<?php // DONE
$subtitle = 'CY028A';
// CY-28-A MACK DOUBLE CONTAINER TRUCK, issued 1990
$desc = "Mack Double Container Truck";
$year = '1990';

$defaults = ['mod' => $subtitle, 'cab' => 'MB202', 'tlr' => 'CYT02', 'cod' => '1'];

$models = [
// 1. White cab, black chassis, white containers with black trailer, "Big Top Circus" tampo
    ['var' => '01a', 'mfg' => 'Macau', 'liv' => 'Big Top Circus',
	'cdt' => 'white, black chassis', 'cva' => '05',
	'tdt' => 'black, white containers, BIG TOP CIRCUS tampo',
    ],
// 2. White cab, blue chassis, white container with blue trailer, "Big Top Circus" tampo
    ['var' => '02a', 'mfg' => 'Macau', 'liv' => 'Big Top Circus',
	'cdt' => 'white, blue chassis', 'cva' => '05',
	'tdt' => 'blue, white container, BIG TOP CIRCUS tampo',
    ],
// 3. White cab, black chassis, white containers with black trailer, "DHL Worldwide Express" tampo (TC)
    ['var' => '03a', 'mfg' => 'Macau', 'liv' => 'DHL',
	'cdt' => 'white, black chassis', 'cva' => '07',
	'tdt' => 'black, white containers, DHL WORLDWIDE EXPRESS tampo',
    ],
// 4. Red cab, black chassis, white containers with red trailer, "Big Top Circus" tampo
    ['var' => '04a', 'mfg' => 'Thailand', 'liv' => 'Big Top Circus',
	'cdt' => 'red, black chassis', 'cva' => '12',
	'tdt' => 'red, white containers, BIG TOP CIRCUS tampo',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
