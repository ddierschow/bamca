<?php // DONE
$subtitle = 'TP023A';
// TP23-A COVERED CONTAINER TRUCK, issued 1979
$desc = "Peterbilt Covered Container Truck";
$year = '1979';

$defaults = ['mod' => $subtitle, 'cab' => 'TYCC', 'tlr' => 'CYT03', 'mfg' => 'England', 'cod' => '1'];

include "cypage.php";

function body() {
    show_table([
// 1. Red cab, amber windows, solid lettered "Firestone" labels
	['var' => '01a', 'liv' => 'Firestone',
            'cdt' => 'red, amber windows', 'cva' => '03',
            'tdt' => 'red and white, solid lettered FIRESTONE labels',
	],
// 2. Red cab, amber windows, outlined lettered "Firestone" labels
	['var' => '02a', 'liv' => 'Firestone',
            'cdt' => 'red, amber windows', 'cva' => '03',
            'tdt' => 'red and white, outline lettered FIRESTONE labels',
	],
// 3. Red cab, no windows, outlined lettered "Firestone" labels
	['var' => '03a', 'liv' => 'Firestone',
            'cdt' => 'red, no windows',
            'tdt' => 'red and white, outline lettered FIRESTONE labels',
	],
    ]);
}
?>
