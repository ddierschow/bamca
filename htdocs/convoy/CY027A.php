<?php // DONE
$subtitle = 'CY027A';
// CY-27-A MACK CONTAINER TRUCK, issued 1990
$desc = "Mack Container Truck";
$year = '1990';

$defaults = ['mod' => $subtitle, 'cab' => 'MB202', 'tlr' => 'Box', 'cod' => '1'];

include "cypage.php";

function body() {
// NOTE: All models with 8-spoke wheels and no antennas cast unless otherwise noted.
    show_table([
// 1. White cab, black chassis, white container with black base, "The Greatest Name In Trucks-Mack" labels, Macau
	['var' => '01a', 'mfg' => 'Macau', 'liv' => 'Mack',
            'cdt' => 'white, black chassis',
            'tdt' => 'white container with black base, THE GREATEST NAME IN TRUCKS-MACK labels',
	],
// 2. Chrome plated cab, black chassis, black container with black base, "Celebrating A Decade of Matchbox Conventions 1991" labels, Macau (C2)
	['var' => '02a', 'mfg' => 'Macau', 'liv' => 'none', 'cod' => '2',
            'cdt' => 'chrome plated, black chassis',
            'tdt' => 'black container with black base, CELEBRATING A DECADE OF MATCHBOX CONVENTIONS 1991 labels',
	],
// 3. Black cab and chassis, black container with black base, "Body Glove" labels, Thailand
	['var' => '03a', 'mfg' => 'Thailand', 'liv' => 'Body Glove',
            'cdt' => 'black, black chassis',
            'tdt' => 'black container with black base, BODY GLOVE labels',
	],
// 4. Black cab, blue chassis, blue container with black base, "Oreo" labels, Thailand
	['var' => '04a', 'mfg' => 'Thailand', 'liv' => 'Oreo',
            'cdt' => 'black cab, blue chassis',
            'tdt' => 'blue container with black base, OREO labels',
	],
// 5. White cab, black chassis, white container with white base, "Nothing Else Is A Pepsi" labels, Thailand
	['var' => '05a', 'mfg' => 'Thailand', 'liv' => 'Pepsi',
            'cdt' => 'white, black chassis',
            'tdt' => 'white container with white base, NOTHING ELSE IS A PEPSI labels',
	],
// 6. White cab, black chassis, white container with white base, "Fed Ex" labels, Thailand
	['var' => '06a', 'mfg' => 'Thailand', 'liv' => 'Fed Ex',
            'cdt' => 'white, black chassis',
            'tdt' => 'white container with white base, FED EX labels',
	],
// 7. Blue cab and chassis, blue container with blue base, "Planters" labels, China
	['var' => '07a', 'mfg' => 'Thailand', 'liv' => 'Planters',
            'cdt' => 'blue, blue chassis',
            'tdt' => 'blue container with blue base, PLANTERS labels',
	],

	['var' => '08a', 'mfg' => 'China', 'liv' => 'Planters',
            'cdt' => 'blue, black chassis',
            'tdt' => 'blue container with blue base, PLANTERS labels',
	],
	['var' => '09a', 'cab' => 'MB311', 'mfg' => 'China', 'liv' => 'Haagen-Daz',
            'cdt' => '',
            'tdt' => '',
	],
	['var' => '10a', 'mfg' => 'China', 'liv' => 'Matchbox',
            'cdt' => '',
            'tdt' => '',
	],
	['var' => '11a', 'mfg' => 'China', 'liv' => 'Ringling Bros',
            'cdt' => '',
            'tdt' => '',
	],

	['var' => '12a', 'mfg' => 'China', 'liv' => 'Ben and Jerry',
            'cdt' => '',
            'tdt' => '',
	],
	['var' => '13a', 'mfg' => 'China', 'liv' => 'Kroger',
            'cdt' => '',
            'tdt' => '',
	],
	['var' => '14a', 'mfg' => 'China', 'liv' => 'Safeway',
            'cdt' => '',
            'tdt' => '',
	],
	['var' => '15a', 'mfg' => 'China', 'liv' => 'Lucky',
            'cdt' => '',
            'tdt' => '',
	    'add' => [['Other side', '<img src="/pic/set/convoy/m_cy027a_15a2.jpg">']],
	],
	['var' => '16a', 'mfg' => 'China', 'liv' => 'Smiths',
            'cdt' => '',
            'tdt' => '',
	],
	['var' => '17a', 'mfg' => 'China', 'liv' => 'Coca-Cola',
            'cdt' => '',
            'tdt' => '',
	],
	['var' => '19a', 'mfg' => 'China', 'liv' => 'Medle',
            'cdt' => '',
            'tdt' => '',
	],
	['var' => '21a', 'mfg' => 'China', 'liv' => 'Ben and Jerry',
            'cdt' => '',
            'tdt' => '',
	    'nts' => "Available only from Ben and Jerry's",
	],
    ]);
}
?>
