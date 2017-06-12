<?php // DONE
$subtitle = 'CY106B';
// CY-106-B PETERBILT CONTAINER TRUCK, issued 1997
$desc = "Peterbilt Container Truck";
$year = '1997';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. White cab, chrome base, white container and base, "Quad Graphics" labels, 8 spoke wheels (US)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB106', 'tlr' => 'Container', 'mfg' => 'China',
	    'liv' => 'Quad Graphics', 'cod' => '1', 'rar' => '3',
            'cdt' => 'white, chrome base',
            'tdt' => 'white container and base, QUAD GRAPHICS labels, 8 spoke wheels',
	],
// 2. Grape cab, chrome base, yellow container with grape base, "Nickelodeon" labels, 8 spoke wheels, China casting 
// NOTE: Version 2 cab base can be cast "Matchbox International" or "Mattel Inc."
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB106', 'tlr' => 'Container', 'mfg' => 'China',
	    'liv' => 'Nickelodeon', 'cod' => '1', 'rar' => '2',
            'cdt' => 'grape, chrome base',
            'tdt' => 'yellow container with grape base, NICKELODEON labels, 8 spoke wheels',
	],
// 3. Orange cab, chrome base, orange container with black base, "Matchbox Premiere Collection" labels, rubber tires, antennas cast, China casting , China casting (PC)
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB307', 'tlr' => 'Container', 'mfg' => 'China',
	    'liv' => 'Matchbox', 'cod' => '1', 'rar' => '2',
            'cdt' => 'orange, chrome base',
            'tdt' => 'orange container with black base, MATCHBOX PREMIERE COLLECTION labels',
	],
// 4. White cab, chrome base, white container and base, "Parcel Direct" labels, China casting (US)
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB106', 'tlr' => 'Container', 'mfg' => 'China',
	    'liv' => 'Parcel Direct', 'cod' => '1', 'rar' => '3',
            'cdt' => 'white, chrome base',
            'tdt' => 'white container and base, PARCEL DIRECT labels',
	],
// 5. Red cab, chrome base, red container and base, "Coca Cola" labels, "Mattel" and China casting (ROW)
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'MB106', 'tlr' => 'Container', 'mfg' => 'China, MATTEL',
	    'liv' => 'Coca-Cola', 'cod' => '1', 'rar' => '2',
            'cdt' => 'red, chrome base',
            'tdt' => 'red container and base, COCA COLA labels',
	],
    ]);
}
?>
