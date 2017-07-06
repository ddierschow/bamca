<?php // DONE
$subtitle = 'CY007A';
// CY-7-A PETERBILT GAS TANKER, issued 1982
// NOTE: All models with 8-spoke wheels and no antennas cast unless otherwise noted.
$desc = "Peterbilt &amp; Kenworth Tanker Trailer";
$year = '1982';

$defaults = ['mod' => $subtitle,
	    'cab' => 'MB106', 'tlr' => 'CYT06', 'mfg' => 'England',
	    'liv' => 'SuperGas', 'cod' => '1',
	    'cdt' => 'black with yellow and orange SUPERGAS tampo, amber windows',
	    'tdt' => 'black base, yellow tank, SUPERGAS labels',
	];

$models = [
// 1. MB43-D cab in black with yellow and orange "Supergas" tempa, amber windows, yellow tank, black trailer base, "Supergas" labels, England
    ['var' => '01a', 'mfg' => 'England', 'liv' => 'SuperGas',
	'cdt' => 'black with yellow and orange SUPERGAS tampo, amber windows', 'cva' => '03AA',
	'tdt' => 'black base, yellow tank, SUPERGAS labels',
    ],
// 2. MB43-D cab in black with white and red "Super" tempa, amber windows, yellow tank, black trailer base, "Supergas" labels, England
    ['var' => '02a', 'mfg' => 'England', 'liv' => 'SuperGas',
	'cdt' => 'black with white and red SUPER tampo, amber windows', 'cva' => '05AA',
	'tdt' => 'black base, yellow tank, SUPERGAS labels',
    ],
// 3. MB43-D cab in black with white and red "Super" tempa, clear windows, yellow tank, black trailer base, "Supergas" labels, England
    ['var' => '03a', 'mfg' => 'England', 'liv' => 'SuperGas',
	'cdt' => 'black with white and red SUPER tampo, clear windows', 'cva' => '06AA',
	'tdt' => 'black base, yellow tank, SUPERGAS labels',
    ],
// 4. MB41-D cab in black with red and gray stripes tempa, amber windows, yellow tank, black trailer base, "Supergas" labels, England
    ['var' => '04a', 'cab' => 'MB103', 'mfg' => 'England', 'liv' => 'SuperGas',
	'cdt' => 'black with red and gray stripes tampo, amber windows', 'cva' => '003',
	'tdt' => 'black base, yellow tank, SUPERGAS labels',
    ],
// 5. MB41-D cab in black with red and gray stripes tempa, clear windows, yellow tank, black trailer base, "Supergas" labels, England
    ['var' => '05a', 'cab' => 'MB103', 'mfg' => 'England', 'liv' => 'SuperGas',
	'cdt' => 'black with red and white stripes tampo, clear windows', 'cva' => '004',
	'tdt' => 'black trailer base, yellow tank, SUPERGAS labels',
    ],
// 6. MB45-C cab in white with red and yellow stripes tempa, amber windows, yellow tank, black trailer base, "Supergas" labels, England
    ['var' => '06a', 'cab' => 'MB045', 'mfg' => 'England', 'liv' => 'SuperGas',
	'cdt' => 'white with red and yellow stripes tampo, amber windows', 'cva' => '004',
	'tdt' => 'black trailer base, yellow tank, SUPERGAS labels',
    ],
// 7. MB43-D cab in white with no tempa, light amber windows, white tank, black trailer base, "Supergas" labels, England
    ['var' => '07a', 'mfg' => 'England', 'liv' => 'SuperGas',
	'cdt' => 'white, light amber windows', 'cva' => '',
	'tdt' => 'black trailer base, white tank, SUPERGAS labels',
    ],
    ['var' => '07b', 'mfg' => 'England', 'liv' => 'SuperGas',
	'cdt' => 'white with red and yellow stripes tampo, amber windows', 'cva' => '',
	'tdt' => 'white trailer base, yellow tank, SUPERGAS labels',
    ],
// 8. MB43-D cab in black with yellow and red "Z" tempa, clear windows, orange-yellow tank, black trailer base, "Supergas" tempa, Macau
    ['var' => '08a', 'mfg' => 'Macau', 'liv' => 'SuperGas',
	'cdt' => 'black with yellow and red Z tampo, clear windows', 'cva' => '',
	'tdt' => 'black trailer base, orange yellow tank, SUPERGAS tampo',
    ],
// 9. MB43-D cab in red with "Getty" tempa, clear windows, chrome tank, pearly silver trailer base, "Getty" tempa, Macau
    ['var' => '09a', 'mfg' => 'Macau', 'liv' => 'Getty',
	'cdt' => 'red with GETTY tampo, clear windows', 'cva' => '',
	'tdt' => 'pearly silver trailer base, chrome tank, GETTY tampo',
    ],
// 10. MB43-D cab in silver-gray with "Arco" tempa, clear windows, chrome tank, silver-gray trailer base, "Arco" tempa, China, rubber tires, antennas cast (PC)
    ['var' => '10a', 'cab' => 'MB307', 'mfg' => 'China (PC)', 'liv' => 'Arco',
	'cdt' => 'silver-gray with ARCO tampo, clear windows', 'cva' => '',
	'tdt' => 'silver-gray trailer, chrome tank, ARCO tampo',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
