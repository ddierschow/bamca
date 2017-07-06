<?php // DONE
$subtitle = 'TP025A';
// TP25-A PIPE TRUCK, issued 1979
$desc = "Peterbilt Pipe Truck";
$year = '1979';

$defaults = ['mod' => $subtitle, 'cab' => 'T9CC', 'tlr' => 'CYT05', 'mfg' => 'England', 'cod' => '1'];

include "cypage.php";

function body() {
    show_table([
// 1. Yellow cab, amber windows, silver-gray flatbed, orange pipes
	['var' => '01a', 'liv' => 'none',
            'cdt' => 'yellow, amber windows', 'cva' => '07',
            'tdt' => 'silver-gray flatbed, orange pipes',
	],
// 2. Yellow cab, amber windows, black flatbed, orange pipes
	['var' => '02a', 'liv' => 'none',
            'cdt' => 'yellow, amber windows', 'cva' => '07',
            'tdt' => 'black flatbed, orange pipes',
	],
// 3. Dark green cab, amber windows, silver-gray flatbed, orange pipes
	['var' => '03a', 'liv' => 'none',
            'cdt' => 'dark green, amber windows', 'cva' => '05',
            'tdt' => 'silver-gray flatbed, orange pipes',
	],
// 4. Dark green cab, amber windows, black flatbed, orange pipes
	['var' => '04a', 'liv' => 'none',
            'cdt' => 'dark green, amber windows', 'cva' => '05',
            'tdt' => 'black flatbed, orange pipes',
	],
// 5. Dark green cab, no windows, black flatbed, orange pipes
	['var' => '05a', 'liv' => 'none',
            'cdt' => 'dark green, no windows', 'cva' => '05',
            'tdt' => 'black flatbed, orange pipes',
	],
// 6. Bronze cab, amber windows, black flatbed, orange pipes
	['var' => '06a', 'liv' => 'none',
            'cdt' => 'bronze, amber windows', 'cva' => '01',
            'tdt' => 'black flatbed, orange pipes',
	],
    ]);
}
?>
