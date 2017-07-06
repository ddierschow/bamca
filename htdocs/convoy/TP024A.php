<?php // DONE
$subtitle = 'TP024A';
// TP24-A CONTAINER TRUCK, issued 1979
$desc = "Peterbilt Container Truck";
$year = '1979';

$defaults = ['mod' => $subtitle, 'cab' => 'T9CC', 'tlr' => 'CYT04', 'mfg' => 'England', 'cod' => '1'];

include "cypage.php";

function body() {
    show_table([
// 1. Red cab, solid lettered "Firestone" labels
	['var' => '01a', 'liv' => 'Firestone',
            'cdt' => 'red', 'cva' => '03',
            'tdt' => 'solid lettered FIRESTONE labels',
	],
// 2. Red cab, outlined lettered "Firestone" labels
	['var' => '02a', 'liv' => 'Firestone',
            'cdt' => 'red', 'cva' => '03',
            'tdt' => 'outlined lettered FIRESTONE labels',
	],
// 3. Red cab, "Matchbox" (towards rear) labels
	['var' => '03a', 'liv' => 'Firestone',
            'cdt' => 'red', 'cva' => '03',
            'tdt' => 'MATCHBOX (towards rear) labels',
	],
// 4. Red cab, "Matchbox" (towards front) labels
	['var' => '04a', 'liv' => 'Firestone',
            'cdt' => 'red', 'cva' => '03',
            'tdt' => 'MATCHBOX (towards front) labels',
	],
// 5. Yellow cab, "Matchbox" (towards front) labels
	['var' => '05a', 'liv' => 'Firestone',
            'cdt' => 'yellow', 'cva' => '07',
            'tdt' => 'MATCHBOX (towards front) labels',
	],
    ]);
}
?>
