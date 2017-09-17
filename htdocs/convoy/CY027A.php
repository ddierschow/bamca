<?php // DONE
$subtitle = 'CY027A';
// CY-27-A MACK CONTAINER TRUCK, issued 1990
$desc = "Mack Container Truck";
$year = '1990';

$defaults = ['mod' => $subtitle, 'cab' => 'MB202', 'tlr' => 'CYT04', 'cod' => '1'];

// NOTE: All models with 8-spoke wheels and no antennas cast unless otherwise noted.
$models = [
// 1. White cab, black chassis, white container with black base, "The Greatest Name In Trucks-Mack" labels, Macau
    ['var' => '01a', 'mfg' => 'Macau', 'liv' => 'Mack',
	'cdt' => 'white, black chassis', 'cva' => '01',
	'tdt' => 'white container with black base, THE GREATEST NAME IN TRUCKS-MACK labels',
    ],
// 2. Chrome plated cab, black chassis, black container with black base, "Celebrating A Decade of Matchbox Conventions 1991" labels, Macau (C2)
    ['var' => '02a', 'mfg' => 'Macau', 'liv' => 'none', 'cod' => '2',
	'cdt' => 'chrome plated, black chassis', 'cva' => '06',
	'tdt' => 'black container with black base, CELEBRATING A DECADE OF MATCHBOX CONVENTIONS 1991 labels',
    ],
// 3. Black cab and chassis, black container with black base, "Body Glove" labels, Thailand
    ['var' => '03a', 'mfg' => 'Thailand', 'liv' => 'Body Glove',
	'cdt' => 'black, black chassis', 'cva' => '29',
	'tdt' => 'black container with black base, BODY GLOVE labels',
    ],
// 4. Black cab, blue chassis, blue container with black base, "Oreo" labels, Thailand
    ['var' => '04a', 'mfg' => 'Thailand', 'liv' => 'Oreo',
	'cdt' => 'black cab, blue chassis', 'cva' => '31',
	'tdt' => 'blue container with black base, OREO labels',
    ],
// 5. White cab, black chassis, white container with white base, "Nothing Else Is A Pepsi" labels, Thailand
    ['var' => '05a', 'mfg' => 'Thailand', 'liv' => 'Pepsi',
	'cdt' => 'white, black chassis', 'cva' => '25',
	'tdt' => 'white container with white base, NOTHING ELSE IS A PEPSI labels',
    ],
// 6. White cab, black chassis, white container with white base, "Fed Ex" labels, Thailand
    ['var' => '06a', 'mfg' => 'Thailand', 'liv' => 'Fed Ex',
	'cdt' => 'white, black chassis', 'cva' => '27',
	'tdt' => 'white container with white base, FED EX labels',
    ],
// 7. Blue cab and chassis, blue container with blue base, "Planters" labels, China
    ['var' => '07a', 'mfg' => 'Thailand', 'liv' => 'Planters',
	'cdt' => 'blue, blue chassis', 'cva' => '33',
	'tdt' => 'blue container with blue base, PLANTERS labels',
    ],

    ['var' => '08a', 'mfg' => 'China', 'liv' => 'Planters',
	'cdt' => 'blue, black chassis', 'cva' => '35',
	'tdt' => 'blue container with blue base, PLANTERS labels',
    ],
    ['var' => '09a', 'cab' => 'MB311', 'mfg' => 'China', 'liv' => 'Haagen-Daz',
	'cdt' => '', 'cva' => '36',
	'tdt' => '',
    ],
    ['var' => '10a', 'mfg' => 'China', 'liv' => 'Matchbox',
	'cdt' => '', 'cva' => '39',
	'tdt' => '',
    ],
    ['var' => '11a', 'mfg' => 'China', 'liv' => 'Ringling Bros',
	'cdt' => '', 'cva' => '42',
	'tdt' => '',
    ],

    ['var' => '12a', 'mfg' => 'China', 'liv' => 'Ben and Jerry',
	'cdt' => '', 'cva' => '41',
	'tdt' => '',
    ],
    ['var' => '13a', 'mfg' => 'China', 'liv' => 'Kroger',
	'cdt' => '', 'cva' => '40',
	'tdt' => '',
    ],
    ['var' => '14a', 'mfg' => 'China', 'liv' => 'Safeway',
	'cdt' => '', 'cva' => '46',
	'tdt' => '',
    ],
    ['var' => '15a', 'mfg' => 'China', 'liv' => 'Lucky',
	'cdt' => '', 'cva' => '45',
	'tdt' => '',
	'add' => [['Other side', '<img src="/pic/set/convoy/m_cy027a-15a2.jpg">']],
    ],
    ['var' => '16a', 'mfg' => 'China', 'liv' => 'Smiths',
	'cdt' => '', 'cva' => '',
	'tdt' => '',
    ],
    ['var' => '17a', 'mfg' => 'China', 'liv' => 'Coca-Cola',
	'cdt' => '', 'cva' => '47',
	'tdt' => '',
    ],
    ['var' => '19a', 'mfg' => 'China', 'liv' => 'Medle',
	'cdt' => '', 'cva' => '',
	'tdt' => '',
    ],
    ['var' => '21a', 'mfg' => 'China', 'liv' => 'Ben and Jerry',
	'cdt' => '', 'cva' => '',
	'tdt' => '',
	'nts' => "Available only from Ben and Jerry's",
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
