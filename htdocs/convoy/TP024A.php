<?php // DONE
$subtitle = 'TP024A';
// TP24-A CONTAINER TRUCK, issued 1979
$desc = "Peterbilt Container Truck";
$year = '1979';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Red cab, solid lettered "Firestone" labels
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'T9CC', 'tlr' => 'Container', 'mfg' => 'England',
	    'liv' => 'Firestone', 'cod' => '1', 'rar' => '',
            'cdt' => 'red',
            'tdt' => 'solid lettered FIRESTONE labels',
	],
// 2. Red cab, outlined lettered "Firestone" labels
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'T9CC', 'tlr' => 'Container', 'mfg' => 'England',
	    'liv' => 'Firestone', 'cod' => '1', 'rar' => '',
            'cdt' => 'red',
            'tdt' => 'outlined lettered FIRESTONE labels',
	],
// 3. Red cab, "Matchbox" (towards rear) labels
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'T9CC', 'tlr' => 'Container', 'mfg' => 'England',
	    'liv' => 'Firestone', 'cod' => '1', 'rar' => '',
            'cdt' => 'red',
            'tdt' => 'MATCHBOX (towards rear) labels',
	],
// 4. Red cab, "Matchbox" (towards front) labels
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'T9CC', 'tlr' => 'Container', 'mfg' => 'England',
	    'liv' => 'Firestone', 'cod' => '1', 'rar' => '',
            'cdt' => 'red',
            'tdt' => 'MATCHBOX (towards front) labels',
	],
// 5. Yellow cab, "Matchbox" (towards front) labels
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'T9CC', 'tlr' => 'Container', 'mfg' => 'England',
	    'liv' => 'Firestone', 'cod' => '1', 'rar' => '',
            'cdt' => 'yellow',
            'tdt' => 'MATCHBOX (towards front) labels',
	],
    ]);
}
?>
