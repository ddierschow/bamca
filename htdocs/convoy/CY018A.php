<?php // DONE
$subtitle = 'CY018A';
// CY-18-A SCANIA DOUBLE CONTAINER TRUCK, issued 1986
$desc = "Scania Double Container Truck";
$year = '1986';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Blue cab with black interior, yellow chassis, dark blue containers, yellow trailer base, "Varta Batteries" tampo
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB183', 'tlr' => 'Double Container', 'mfg' => 'Macau',
	    'liv' => 'Varta', 'cod' => '1', 'rar' => '',
            'cdt' => 'blue with black interior, yellow chassis',
            'tdt' => 'dark blue containers, yellow base, VARTA BATTERIES tampo',
	],
// 2. Blue cab with gray interior, yellow chassis, dark blue containers, yellow trailer base, "Varta Batteries" tampo
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB183', 'tlr' => 'Double Container', 'mfg' => 'Macau',
	    'liv' => 'Varta', 'cod' => '1', 'rar' => '',
            'cdt' => 'blue with gray interior, yellow chassis',
            'tdt' => 'dark blue containers, yellow base, VARTA BATTERIES tampo',
	],
// 3. White cab, dark blue chassis, white containers, dark blue trailer base, "Wall's Ice Cream" tampo (UK)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB183', 'tlr' => 'Double Container', 'mfg' => 'Macau',
	    'liv' => "Wall's", 'cod' => '1', 'rar' => '',
            'cdt' => 'white cab, dark blue chassis',
            'tdt' => "white containers, dark blue base, WALL'S ICE CREAM tampo",
	],
// 4. Red cab and chassis, red containers, red trailer base, "Kit Kat" tampo (UK)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB183', 'tlr' => 'Double Container', 'mfg' => 'Macau',
	    'liv' => 'Kit Kat', 'cod' => '1', 'rar' => '',
            'cdt' => 'red, red chassis',
            'tdt' => 'red containers, red base, KIT KAT tampo',
	],
// 5. Orange cab, brown chassis, orange containers, brown trailer base, "Breakaway" tampo (UK)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB183', 'tlr' => 'Double Container', 'mfg' => 'Macau',
	    'liv' => 'Breakaway', 'cod' => '1', 'rar' => '',
            'cdt' => 'orange, brown chassis',
            'tdt' => 'orange containers, brown base, BREAKAWAY tampo',
	],
// 6. White cab, green chassis, white containers, green trailer base, "7 Up" tampo (UK)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB183', 'tlr' => 'Double Container', 'mfg' => 'Macau',
	    'liv' => '', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, green chassis',
            'tdt' => 'white containers, green base, 7 UP tampo',
	],
// 7. Red cab, black chassis, red containers, black trailer base, "Beefeater Steak Houses" tampo (UK)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB183', 'tlr' => 'Double Container', 'mfg' => 'Macau',
	    'liv' => 'Beefeater', 'cod' => '1', 'rar' => '',
            'cdt' => 'red, black chassis',
            'tdt' => 'red containers, black base, BEEFEATER STEAK HOUSES tampo',
	],
    ]);
}
?>
