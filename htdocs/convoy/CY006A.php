<?php // DONE
$subtitle = 'CY006A';
// CY-6-A KENWORTH HORSE BOX, issued 1982
$desc = "Kenworth Horse Box";
$year = '1982';

$defaults = ['mod' => $subtitle, 'cab' => 'MB103', 'tlr' => 'CYT11', 'cod' => '1',
            'cdt' => 'green with yellow and black stripes',
            'tdt' => 'beige, silver-gray base, green doors, BLUE GRASS FARMS tampo',
];

$models = [
// 1. Green cab with yellow and black stripes, beige trailer, green doors, silver-gray base, "Blue Grass Farms" tempa, England
    ['var' => '01a', 'mfg' => 'England', 'liv' => 'Blue Grass Farms',
	'cdt' => 'green with yellow and black stripes', 'cva' => '007A',
	'tdt' => 'beige, silver-gray base, green doors, BLUE GRASS FARMS tampo',
    ],
// 2. Green cab with white and black stripes, beige trailer, green doors, silver-gray base, "Blue Grass Farms" tempa, England
    ['var' => '02a', 'mfg' => 'England', 'liv' => 'Blue Grass Farms',
	'cdt' => 'green with white and black stripes', 'cva' => '008A',
	'tdt' => 'beige, silver-gray base, green doors, BLUE GRASS FARMS tampo',
    ],
// 3. Green cab with white and black stripes, beige trailer, green doors, silver-gray base, "Blue Grass" tempa, England
    ['var' => '03a', 'mfg' => 'England', 'liv' => 'Blue Grass',
	'cdt' => 'green with white and black stripes', 'cva' => '008A',
	'tdt' => 'beige, silver-gray base, green doors, BLUE GRASS tampo',
    ],
// 4. Green cab with white and black stripes, tan trailer, green doors, silver-gray base, no tempa, England
    ['var' => '04a', 'mfg' => 'England', 'liv' => 'none',
	'cdt' => 'green with white and black stripes', 'cva' => '008A',
	'tdt' => 'tan, silver-gray base, green doors',
    ],
    ['var' => '04b', 'mfg' => 'England', 'liv' => 'none',
	'cdt' => 'green with white and black stripes', 'cva' => '008A',
	'tdt' => 'cream, silver-gray base, green doors',
    ],
// 5. Green cab with white and black stripes, beige trailer, green doors, pearly silver base, "Blue Grass Farms" tempa, Macau
    ['var' => '05a', 'mfg' => 'Macau', 'liv' => 'Blue Grass Farms',
	'cdt' => 'green with white and black stripes', 'cva' => '008A',
	'tdt' => 'beige, pearly silver base, green doors, BLUE GRASS FARMS tampo',
    ],
// 6. Green cab with white and black stripes, beige trailer, white doors, pearly silver base, "Blue Grass Farms" tempa, Macau
    ['var' => '06a', 'mfg' => 'Macau', 'liv' => 'Blue Grass Farms',
	'cdt' => 'green with white and black stripes', 'cva' => '008A',
	'tdt' => 'beige, pearly silver base, white doors, BLUE GRASS FARMS tampo',
    ],
// 7. Green cab with orange and yellow stripes, beige trailer, green door, pearly silver trailer base, Thailand, green and orange stripes with horse silhouette tempa (FM)
    ['var' => '07a', 'mfg' => 'Thailand', 'liv' => 'none',
	'cdt' => 'green with orange and yellow stripes', 'cva' => '102',
	'tdt' => 'beige, pearly silver base, green doors, orange and green stripes with horse silhouette tampo',
    ],
    ['var' => '07b', 'mfg' => 'Thailand', 'liv' => 'none',
	'cdt' => 'green with white and orange stripes', 'cva' => '',
	'tdt' => 'cream, silver-gray base, green doors, orange and green stripes with horse silhouette tampo',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
