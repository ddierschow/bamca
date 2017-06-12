<?php // DONE
$subtitle = 'CY005A';
// CY-5-A PETERBILT COVERED TRUCK, issued 1982
$desc = "Kenworth or Peterbilt with Covered Trailer";
$year = '1982';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. MB43-D cab in white, chrome exhausts, amber windows, green cover, white trailer, "Interstate Trucking" labels, England
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB106', 'tlr' => 'Covered', 'mfg' => 'England',
	    'liv' => 'Interstate', 'cod' => '1', 'rar' => '',
	    'cdt' => 'white, clear windows, chrome exhausts',
	    'tdt' => 'white, green cover, INTERSTATE TRUCKING labels',
	],
// 2. MB43-D cab in white, chrome exhausts, clear windows, green cover, white trailer, "Interstate Trucking" labels, England
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB106', 'tlr' => 'Covered', 'mfg' => 'England',
	    'liv' => 'Interstate', 'cod' => '1', 'rar' => '',
	    'cdt' => 'white, amber windows, chrome exhausts',
	    'tdt' => 'white, green cover, INTERSTATE TRUCKING labels',
	],
// 3. MB41-D cab in green, chrome exhausts, clear windows, green cover, white trailer, "Interstate Trucking" labels, England
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB103', 'tlr' => 'Covered', 'mfg' => 'England',
	    'liv' => 'Interstate', 'cod' => '1', 'rar' => '',
	    'cdt' => 'green, clear windows, chrome exhausts',
	    'tdt' => 'white, green cover, INTERSTATE TRUCKING labels',
	],
// 4. MB43-D cab in green, chrome exhausts, clear windows, green cover, white trailer, "Interstate Trucking" tempa, Macau
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB106', 'tlr' => 'Covered', 'mfg' => 'Macau',
	    'liv' => 'Interstate', 'cod' => '1', 'rar' => '',
	    'cdt' => 'green, clear windows, chrome exhausts',
	    'tdt' => 'white, green cover, INTERSTATE TRUCKING tampo',
	],
	['mod' => $subtitle, 'var' => '04b',
	    'cab' => 'MB106', 'tlr' => 'Covered', 'mfg' => 'Macau',
	    'liv' => 'Interstate', 'cod' => '1', 'rar' => '',
	    'cdt' => 'white, amber windows, chrome exhausts',
	    'tdt' => 'white, green cover, INTERSTATE TRUCKING labels',
	],
// 5. MB43-D cab in yellow, chrome exhausts, clear windows, yellow cover, pearly silver trailer, "Michelin" tempa, Macau
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'MB106', 'tlr' => 'Covered', 'mfg' => 'Macau',
	    'liv' => 'Michelin', 'cod' => '1', 'rar' => '',
	    'cdt' => 'yellow, clear windows, chrome exhausts',
	    'tdt' => 'pearly silver, yellow cover, MICHELIN tampo',
	],
// 6. MB43-D cab in orange, chrome exhausts, clear windows, light gray cover, pearly silver trailer, "Walt's Fresh Farm Produce" tempa, Macau
	['mod' => $subtitle, 'var' => '06a',
	    'cab' => 'MB106', 'tlr' => 'Covered', 'mfg' => 'Macau',
	    'liv' => "Walt's", 'cod' => '1', 'rar' => '',
	    'cdt' => 'orange, clear windows, chrome exhausts',
	    'tdt' => "pearly silver, light gray cover, WALT'S FRESH FARM PRODUCE tampo",
	],
	['mod' => $subtitle, 'var' => '06b',
	    'cab' => 'MB106', 'tlr' => 'Covered', 'mfg' => 'Macau',
	    'liv' => "Walt's", 'cod' => '1', 'rar' => '',
	    'cdt' => 'orange, clear windows, chrome exhausts',
	    'tdt' => "pearly silver, yellow cover, WALT'S FRESH FARM PRODUCE tampo",
	],
	['mod' => $subtitle, 'var' => '06c',
	    'cab' => 'MB106', 'tlr' => 'Covered', 'mfg' => 'Thailand',
	    'liv' => "Walt's", 'cod' => '1', 'rar' => '',
	    'cdt' => 'orange, clear windows, chrome exhausts',
	    'tdt' => "pearly silver, yellow cover, WALT'S FRESH FARM PRODUCE tampo",
	],
// 7. MB43-D cab in orange, gray exhausts, clear windows, light gray cover, pearly silver trailer, "Walt's Fresh Farm Produce" tempa, Macau
	['mod' => $subtitle, 'var' => '07a',
	    'cab' => 'MB106', 'tlr' => 'Covered', 'mfg' => 'Macau',
	    'liv' => "Walt's", 'cod' => '1', 'rar' => '',
	    'cdt' => 'orange, clear windows, gray exhausts',
	    'tdt' => "pearly silver, light gray cover, WALT'S FRESH FARM PRODUCE tampo",
	],
// 8. MB43-D cab in orange, gray exhausts, clear windows, light gray cover, pearly silver trailer, "Walt's Fresh Farm Produce" tempa, Thailand
	['mod' => $subtitle, 'var' => '08a',
	    'cab' => 'MB106', 'tlr' => 'Covered', 'mfg' => 'Thailand',
	    'liv' => "Walt's", 'cod' => '1', 'rar' => '',
	    'cdt' => 'orange, clear windows, gray exhausts',
	    'tdt' => "pearly silver, light gray cover, WALT'S FRESH FARM PRODUCE tampo",
	],
    ]);
}
?>
