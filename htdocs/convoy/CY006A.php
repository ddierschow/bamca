<?php // DONE
$subtitle = 'CY006A';
// CY-6-A KENWORTH HORSE BOX, issued 1982
$desc = "Kenworth Horse Box";
$year = '1982';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Green cab with yellow and black stripes, beige trailer, green doors, silver-gray base, "Blue Grass Farms" tempa, England
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB103', 'tlr' => 'Horse Box', 'mfg' => 'England',
	    'liv' => 'Blue Grass Farms', 'cod' => '1', 'rar' => '',
            'cdt' => 'green with yellow and black stripes',
            'tdt' => 'beige, silver-gray base, green doors, BLUE GRASS FARMS tampo',
	],
// 2. Green cab with white and black stripes, beige trailer, green doors, silver-gray base, "Blue Grass Farms" tempa, England
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB103', 'tlr' => 'Horse Box', 'mfg' => 'England',
	    'liv' => 'Blue Grass Farms', 'cod' => '1', 'rar' => '',
            'cdt' => 'green with white and black stripes',
            'tdt' => 'beige, silver-gray base, green doors, BLUE GRASS FARMS tampo',
	],
// 3. Green cab with white and black stripes, beige trailer, green doors, silver-gray base, "Blue Grass" tempa, England
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB103', 'tlr' => 'Horse Box', 'mfg' => 'England',
	    'liv' => 'Blue Grass', 'cod' => '1', 'rar' => '',
            'cdt' => 'green with white and black stripes',
            'tdt' => 'beige, silver-gray base, green doors, BLUE GRASS tampo',
	],
// 4. Green cab with white and black stripes, tan trailer, green doors, silver-gray base, no tempa, England
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB103', 'tlr' => 'Horse Box', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'green with white and black stripes',
            'tdt' => 'tan, silver-gray base, green doors',
	],
	['mod' => $subtitle, 'var' => '04b',
	    'cab' => 'MB103', 'tlr' => 'Horse Box', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'green with white and black stripes',
            'tdt' => 'cream, silver-gray base, green doors',
	],
// 5. Green cab with white and black stripes, beige trailer, green doors, pearly silver base, "Blue Grass Farms" tempa, Macau
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'MB103', 'tlr' => 'Horse Box', 'mfg' => 'Macau',
	    'liv' => 'Blue Grass Farms', 'cod' => '1', 'rar' => '',
            'cdt' => 'green with white and black stripes',
            'tdt' => 'beige, pearly silver base, green doors, BLUE GRASS FARMS tampo',
	],
// 6. Green cab with white and black stripes, beige trailer, white doors, pearly silver base, "Blue Grass Farms" tempa, Macau
	['mod' => $subtitle, 'var' => '06a',
	    'cab' => 'MB103', 'tlr' => 'Horse Box', 'mfg' => 'Macau',
	    'liv' => 'Blue Grass Farms', 'cod' => '1', 'rar' => '',
            'cdt' => 'green with white and black stripes',
            'tdt' => 'beige, pearly silver base, white doors, BLUE GRASS FARMS tampo',
	],
// 7. Green cab with orange and yellow stripes, beige trailer, green door, pearly silver trailer base, Thailand, green and orange stripes with horse silhouette tempa (FM)
	['mod' => $subtitle, 'var' => '07a',
	    'cab' => 'MB103', 'tlr' => 'Horse Box', 'mfg' => 'Thailand',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'green with orange and yellow stripes',
            'tdt' => 'beige, pearly silver base, green doors, orange and green stripes with horse silhouette tampo',
	],
	['mod' => $subtitle, 'var' => '07b',
	    'cab' => 'MB103', 'tlr' => 'Horse Box', 'mfg' => 'Thailand',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'green with white and orange stripes',
            'tdt' => 'cream, silver-gray base, green doors, orange and green stripes with horse silhouette tampo',
	],
    ]);
}
?>
