<?php // DONE
$subtitle = 'CY028A';
// CY-28-A MACK DOUBLE CONTAINER TRUCK, issued 1990
$desc = "Mack Double Container Truck";
$year = '1990';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. White cab, black chassis, white containers with black trailer, "Big Top Circus" tampo
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB202', 'tlr' => 'Double Container', 'mfg' => 'Macau',
	    'liv' => 'Big Top Circus', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, black chassis',
            'tdt' => 'black, white containers, BIG TOP CIRCUS tampo',
	],
// 2. White cab, blue chassis, white container with blue trailer, "Big Top Circus" tampo
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB202', 'tlr' => 'Double Container', 'mfg' => 'Macau',
	    'liv' => 'Big Top Circus', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, blue chassis',
            'tdt' => 'blue, white container, BIG TOP CIRCUS tampo',
	],
// 3. White cab, black chassis, white containers with black trailer, "DHL Worldwide Express" tampo (TC)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB202', 'tlr' => 'Double Container', 'mfg' => 'Macau',
	    'liv' => 'DHL', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, black chassis',
            'tdt' => 'black, white containers, DHL WORLDWIDE EXPRESS tampo',
	],
// 4. Red cab, black chassis, white containers with red trailer, "Big Top Circus" tampo
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB202', 'tlr' => 'Double Container', 'mfg' => 'Macau',
	    'liv' => 'Big Top Circus', 'cod' => '1', 'rar' => '',
            'cdt' => 'red, black chassis',
            'tdt' => 'red, white containers, BIG TOP CIRCUS tampo',
	],
    ]);
}
?>
