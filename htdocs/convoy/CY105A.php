<?php // DONE
$subtitle = 'CY105A';
// CY-105-A KENWORTH GAS TRUCK, issued 1989
$desc = "Kenworth Gas Truck";
$year = '1989';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. MB41-D cab in white, white tank with black base, gold & black stripes tampo, Macau casting (JB)(GS)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB103', 'tlr' => 'Box', 'mfg' => 'Macau',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'white',
            'tdt' => 'white tank with black base, gold and black stripes tampo',
	    'nts' => 'From James Bond Set',
	],
// 2. MB41-D cab in white, white tank with matt gray base, "Shell" tampo, China casting (GS)
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB103', 'tlr' => 'Box', 'mfg' => 'China',
	    'liv' => 'Shell', 'cod' => '1', 'rar' => '',
            'cdt' => 'white',
            'tdt' => 'white tank with matt gray base, SHELL tampo',
	    'nts' => 'From Motor City MC-801 Set',
	],
// 3. MB45-C cab in white, white tank with matt gray base, "Shell" tampo, China casting (GS)
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB045', 'tlr' => 'Box', 'mfg' => 'China',
	    'liv' => 'Shell', 'cod' => '1', 'rar' => '',
            'cdt' => 'white',
            'tdt' => 'white tank with matt gray base, SHELL tampo',
	    'nts' => 'From Motor City MC-801 Set',
	],
    ]);
}
?>
