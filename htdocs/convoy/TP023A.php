<?php // DONE
$subtitle = 'TP023A';
// TP23-A COVERED CONTAINER TRUCK, issued 1979
$desc = "Peterbilt Covered Container Truck";
$year = '1979';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Red cab, amber windows, solid lettered "Firestone" labels
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'TYCC', 'tlr' => 'Covered Container', 'mfg' => 'England',
	    'liv' => 'Firestone', 'cod' => '1', 'rar' => '',
            'cdt' => 'red, amber windows',
            'tdt' => 'red and white, solid lettered FIRESTONE labels',
	],
// 2. Red cab, amber windows, outlined lettered "Firestone" labels
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'TYCC', 'tlr' => 'Covered Container', 'mfg' => 'England',
	    'liv' => 'Firestone', 'cod' => '1', 'rar' => '',
            'cdt' => 'red, amber windows',
            'tdt' => 'red and white, outline lettered FIRESTONE labels',
	],
// 3. Red cab, no windows, outlined lettered "Firestone" labels
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'TYCC', 'tlr' => 'Covered Container', 'mfg' => 'England',
	    'liv' => 'Firestone', 'cod' => '1', 'rar' => '',
            'cdt' => 'red, no windows',
            'tdt' => 'red and white, outline lettered FIRESTONE labels',
	],
    ]);
}
?>
