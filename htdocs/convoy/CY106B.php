<?php // DONE
$subtitle = 'CY106B';
// CY-106-B PETERBILT CONTAINER TRUCK, issued 1997
$desc = "Peterbilt Container Truck";
$year = '1997';

$defaults = ['mod' => $subtitle, 'cab' => 'MB106', 'tlr' => 'CYT04', 'cod' => '1'];

$models = [
// 1. White cab, chrome base, white container and base, "Quad Graphics" labels, 8 spoke wheels (US)
    ['var' => '01a', 'mfg' => 'China', 'liv' => 'Quad Graphics', 'rar' => '3',
	'cdt' => 'white, chrome base', 'cva' => '61',
	'tdt' => 'white container and base, QUAD GRAPHICS labels, 8 spoke wheels',
    ],
// 2. Grape cab, chrome base, yellow container with grape base, "Nickelodeon" labels, 8 spoke wheels, China casting 
// NOTE: Version 2 cab base can be cast "Matchbox International" or "Mattel Inc."
    ['var' => '02a', 'mfg' => 'China', 'liv' => 'Nickelodeon', 'rar' => '2',
	'cdt' => 'grape, chrome base', 'cva' => '66',
	'tdt' => 'yellow container with grape base, NICKELODEON labels, 8 spoke wheels',
    ],
// 3. Orange cab, chrome base, orange container with black base, "Matchbox Premiere Collection" labels, rubber tires, antennas cast, China casting , China casting (PC)
    ['var' => '03a', 'cab' => 'MB307', 'mfg' => 'China', 'liv' => 'Matchbox', 'rar' => '2',
	'cdt' => 'orange, chrome base', 'cva' => '',
	'tdt' => 'orange container with black base, MATCHBOX PREMIERE COLLECTION labels',
    ],
// 4. White cab, chrome base, white container and base, "Parcel Direct" labels, China casting (US)
    ['var' => '04a', 'mfg' => 'China', 'liv' => 'Parcel Direct', 'rar' => '3',
	'cdt' => 'white, chrome base', 'cva' => '',
	'tdt' => 'white container and base, PARCEL DIRECT labels',
    ],
// 5. Red cab, chrome base, red container and base, "Coca Cola" labels, "Mattel" and China casting (ROW)
    ['var' => '05a', 'mfg' => 'China, MATTEL', 'liv' => 'Coca-Cola', 'rar' => '2',
	'cdt' => 'red, chrome base', 'cva' => '71',
	'tdt' => 'red container and base, COCA COLA labels',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
