<?php // DONE
$subtitle = 'TP025A';
// TP25-A PIPE TRUCK, issued 1979
$desc = "Peterbilt Pipe Truck";
$year = '1979';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Yellow cab, amber windows, silver-gray flatbed, orange pipes
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'T9CC', 'tlr' => 'Pipe Trailer', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'yellow cab, amber windows',
            'tdt' => 'silver-gray flatbed, orange pipes',
	],
// 2. Yellow cab, amber windows, black flatbed, orange pipes
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'T9CC', 'tlr' => 'Pipe Trailer', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'yellow cab, amber windows',
            'tdt' => 'black flatbed, orange pipes',
	],
// 3. Dark green cab, amber windows, silver-gray flatbed, orange pipes
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'T9CC', 'tlr' => 'Pipe Trailer', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'dark green cab, amber windows',
            'tdt' => 'silver-gray flatbed, orange pipes',
	],
// 4. Dark green cab, amber windows, black flatbed, orange pipes
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'T9CC', 'tlr' => 'Pipe Trailer', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'dark green cab, amber windows',
            'tdt' => 'black flatbed, orange pipes',
	],
// 5. Dark green cab, no windows, black flatbed, orange pipes
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'T9CC', 'tlr' => 'Pipe Trailer', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'dark green cab, no windows',
            'tdt' => 'black flatbed, orange pipes',
	],
// 6. Bronze cab, amber windows, black flatbed, orange pipes
	['mod' => $subtitle, 'var' => '06a',
	    'cab' => 'T9CC', 'tlr' => 'Pipe Trailer', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'bronze cab, amber windows',
            'tdt' => 'black flatbed, orange pipes',
	],
    ]);
}
?>
