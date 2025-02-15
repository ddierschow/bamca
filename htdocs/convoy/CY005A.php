<?php // DONE
$subtitle = 'CY005A';
// CY-5-A PETERBILT COVERED TRUCK, issued 1982
$desc = "Kenworth or Peterbilt with Covered Trailer";
$year = '1982';

$defaults = ['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB106', 'tlr' => 'CYT03', 'cod' => '1',
];

$models = [
// 1. MB43-D cab in white, chrome exhausts, amber windows, green cover, white trailer, "Interstate Trucking" labels, England
    ['var' => '01a', 'mfg' => 'England', 'liv' => 'Interstate',
	'cdt' => 'white, colorless windows, chrome exhausts', 'cva' => '09BA',
	'tdt' => 'white, green cover, INTERSTATE TRUCKING labels',
    ],
// 2. MB43-D cab in white, chrome exhausts, clear windows, green cover, white trailer, "Interstate Trucking" labels, England
    ['var' => '02a', 'mfg' => 'England', 'liv' => 'Interstate',
	'cdt' => 'white, amber windows, chrome exhausts', 'cva' => '07CA',
	'tdt' => 'white, green cover, INTERSTATE TRUCKING labels',
    ],
// 3. MB41-D cab in green, chrome exhausts, clear windows, green cover, white trailer, "Interstate Trucking" labels, England
    ['var' => '03a', 'cab' => 'MB103', 'mfg' => 'England', 'liv' => 'Interstate',
	'cdt' => 'green, colorless windows, chrome exhausts', 'cva' => '007A',
	'tdt' => 'white, green cover, INTERSTATE TRUCKING labels',
    ],
// 4. MB43-D cab in green, chrome exhausts, clear windows, green cover, white trailer, "Interstate Trucking" tempa, Macau
// believe this to be a white cab.
    ['var' => '04a', 'mfg' => 'Macau', 'liv' => 'Interstate',
	'cdt' => 'white, amber windows, chrome exhausts', 'cva' => '18A',
	'tdt' => 'white, green cover, INTERSTATE TRUCKING labels',
    ],
// 5. MB43-D cab in yellow, chrome exhausts, clear windows, yellow cover, pearly silver trailer, "Michelin" tempa, Macau
    ['var' => '05a', 'mfg' => 'Macau', 'liv' => 'Michelin',
	'cdt' => 'yellow, colorless windows, chrome exhausts', 'cva' => '29A',
	'tdt' => 'pearly silver, yellow cover, MICHELIN tampo',
    ],
// 6. MB43-D cab in orange, chrome exhausts, clear windows, light gray cover, pearly silver trailer, "Walt's Fresh Farm Produce" tempa, Macau
    ['var' => '06a', 'mfg' => 'Macau', 'liv' => "Walt's",
	'cdt' => 'orange, colorless windows, chrome exhausts', 'cva' => '37',
	'tdt' => "pearly silver, light gray cover, WALT'S FRESH FARM PRODUCE tampo",
    ],
    ['var' => '06b', 'mfg' => 'Macau', 'liv' => "Walt's",
	'cdt' => 'orange, colorless windows, chrome exhausts', 'cva' => '37',
	'tdt' => "pearly silver, yellow cover, WALT'S FRESH FARM PRODUCE tampo",
    ],
    ['var' => '06c', 'mfg' => 'Thailand', 'liv' => "Walt's",
	'cdt' => 'orange, colorless windows, chrome exhausts', 'cva' => '37',
	'tdt' => "pearly silver, yellow cover, WALT'S FRESH FARM PRODUCE tampo",
    ],
// 7. MB43-D cab in orange, gray exhausts, clear windows, light gray cover, pearly silver trailer, "Walt's Fresh Farm Produce" tempa, Macau
    ['var' => '07a', 'mfg' => 'Macau', 'liv' => "Walt's",
	'cdt' => 'orange, colorless windows, gray exhausts', 'cva' => '47',
	'tdt' => "pearly silver, light gray cover, WALT'S FRESH FARM PRODUCE tampo",
    ],
// 8. MB43-D cab in orange, gray exhausts, clear windows, light gray cover, pearly silver trailer, "Walt's Fresh Farm Produce" tempa, Thailand
    ['var' => '08a', 'mfg' => 'Thailand', 'liv' => "Walt's",
	'cdt' => 'orange, colorless windows, gray exhausts', 'cva' => '47',
	'tdt' => "pearly silver, light gray cover, WALT'S FRESH FARM PRODUCE tampo",
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
