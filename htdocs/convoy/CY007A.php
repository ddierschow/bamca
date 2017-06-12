<?php // DONE
$subtitle = 'CY007A';
// CY-7-A PETERBILT GAS TANKER, issued 1982
// NOTE: All models with 8-spoke wheels and no antennas cast unless otherwise noted.
$desc = "Peterbilt &amp; Kenworth Tanker Trailer";
$year = '1982';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. MB43-D cab in black with yellow and orange "Supergas" tempa, amber windows, yellow tank, black trailer base, "Supergas" labels, England
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB106', 'tlr' => 'Tanker', 'mfg' => 'England',
	    'liv' => 'SuperGas', 'cod' => '1', 'rar' => '',
	    'cdt' => 'black with yellow and orange SUPERGAS tampo, amber windows',
	    'tdt' => 'black base, yellow tank, SUPERGAS labels',
	],
// 2. MB43-D cab in black with white and red "Super" tempa, amber windows, yellow tank, black trailer base, "Supergas" labels, England
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB106', 'tlr' => 'Tanker', 'mfg' => 'England',
	    'liv' => 'SuperGas', 'cod' => '1', 'rar' => '',
	    'cdt' => 'black with white and red SUPER tampo, amber windows',
	    'tdt' => 'black base, yellow tank, SUPERGAS labels',
	],
// 3. MB43-D cab in black with white and red "Super" tempa, clear windows, yellow tank, black trailer base, "Supergas" labels, England
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB106', 'tlr' => 'Tanker', 'mfg' => 'England',
	    'liv' => 'SuperGas', 'cod' => '1', 'rar' => '',
	    'cdt' => 'black with white and red SUPER tampo, clear windows',
	    'tdt' => 'black base, yellow tank, SUPERGAS labels',
	],
// 4. MB41-D cab in black with red and gray stripes tempa, amber windows, yellow tank, black trailer base, "Supergas" labels, England
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB103', 'tlr' => 'Tanker', 'mfg' => 'England',
	    'liv' => 'SuperGas', 'cod' => '1', 'rar' => '',
	    'cdt' => 'black with red and gray stripes tampo, amber windows',
	    'tdt' => 'black base, yellow tank, SUPERGAS labels',
	],
// 5. MB41-D cab in black with red and gray stripes tempa, clear windows, yellow tank, black trailer base, "Supergas" labels, England
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'MB103', 'tlr' => 'Tanker', 'mfg' => 'England',
	    'liv' => 'SuperGas', 'cod' => '1', 'rar' => '',
	    'cdt' => 'black with red and white stripes tampo, clear windows',
	    'tdt' => 'black trailer base, yellow tank, SUPERGAS labels',
	],
// 6. MB45-C cab in white with red and yellow stripes tempa, amber windows, yellow tank, black trailer base, "Supergas" labels, England
	['mod' => $subtitle, 'var' => '06a',
	    'cab' => 'MB045', 'tlr' => 'Tanker', 'mfg' => 'England',
	    'liv' => 'SuperGas', 'cod' => '1', 'rar' => '',
	    'cdt' => 'white with red and yellow stripes tampo, amber windows',
	    'tdt' => 'black trailer base, yellow tank, SUPERGAS labels',
	],
// 7. MB43-D cab in white with no tempa, light amber windows, white tank, black trailer base, "Supergas" labels, England
	['mod' => $subtitle, 'var' => '07a',
	    'cab' => 'MB106', 'tlr' => 'Tanker', 'mfg' => 'England',
	    'liv' => 'SuperGas', 'cod' => '1', 'rar' => '',
	    'cdt' => 'white, light amber windows',
	    'tdt' => 'black trailer base, white tank, SUPERGAS labels',
	],
	['mod' => $subtitle, 'var' => '07b',
	    'cab' => 'MB106', 'tlr' => 'Tanker', 'mfg' => 'England',
	    'liv' => 'SuperGas', 'cod' => '1', 'rar' => '',
	    'cdt' => 'white with red and yellow stripes tampo, amber windows',
	    'tdt' => 'white trailer base, yellow tank, SUPERGAS labels',
	],
// 8. MB43-D cab in black with yellow and red "Z" tempa, clear windows, orange-yellow tank, black trailer base, "Supergas" tempa, Macau
	['mod' => $subtitle, 'var' => '08a',
	    'cab' => 'MB106', 'tlr' => 'Tanker', 'mfg' => 'Macau',
	    'liv' => 'SuperGas', 'cod' => '1', 'rar' => '',
	    'cdt' => 'black with yellow and red Z tampo, clear windows',
	    'tdt' => 'black trailer base, orange yellow tank, SUPERGAS tampo',
	],
// 9. MB43-D cab in red with "Getty" tempa, clear windows, chrome tank, pearly silver trailer base, "Getty" tempa, Macau
	['mod' => $subtitle, 'var' => '09a',
	    'cab' => 'MB106', 'tlr' => 'Tanker', 'mfg' => 'Macau',
	    'liv' => 'Getty', 'cod' => '1', 'rar' => '',
	    'cdt' => 'red with GETTY tampo, clear windows',
	    'tdt' => 'pearly silver trailer base, chrome tank, GETTY tampo',
	],
// 10. MB43-D cab in silver-gray with "Arco" tempa, clear windows, chrome tank, silver-gray trailer base, "Arco" tempa, China, rubber tires, antennas cast (PC)
	['mod' => $subtitle, 'var' => '10a',
	    'cab' => 'MB307', 'tlr' => 'Tanker', 'mfg' => 'China (PC)',
	    'liv' => 'Arco', 'cod' => '1', 'rar' => '',
	    'cdt' => 'silver-gray with ARCO tampo, clear windows',
	    'tdt' => 'silver-gray trailer, chrome tank, ARCO tampo',
	],
    ]);
}
?>
