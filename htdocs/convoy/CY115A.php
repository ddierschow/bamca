<?php // DONE
$subtitle = 'CY115A';
$desc = "Ford Aeromax with Fishbelly";
$year = '2005';

$defaults = ['mod' => $subtitle, 'cab' => 'MB214', 'tlr' => 'Fishbelly', 'cod' => '1'];

include "cypage.php";

function body() {
    show_table([
	['var' => '01a', 'mfg' => 'Macau', 'liv' => 'DHL ',
            'cdt' => 'yellow',
            'tdt' => 'yellow, DHL',
	    'nts' => '2005 Convoy Wheels ',
	],
	['var' => '02a', 'mfg' => 'Macau', 'liv' => 'Michelin',
            'cdt' => 'dark blue',
            'tdt' => 'dark blue, MICHELIN',
	    'nts' => '2005 Convoy Wheels',
	],
	['var' => '03a', 'mfg' => 'Macau', 'liv' => 'McDonalds',
            'cdt' => 'red',
            'tdt' => 'red, MCDONALDS',
	    'nts' => '2005 Convoy Wheels ',
	],
	['var' => '04a', 'mfg' => 'Macau', 'liv' => 'DHL ',
            'cdt' => 'yellow',
            'tdt' => 'yellow, DHL',
	    'nts' => '2006 Convoy Wheels ',
	],
	['var' => '05a', 'mfg' => 'Macau', 'liv' => 'Michelin',
            'cdt' => 'dark blue',
            'tdt' => 'dark blue, MICHELIN',
	    'nts' => '2006 Convoy Wheels',
	],
	['var' => '06a', 'mfg' => 'Thailand', 'liv' => 'McDonalds',
            'cdt' => 'red',
            'tdt' => 'red, MCDONALDS',
	    'nts' => '2006 Convoy Wheels',
	],
	['var' => '07a', 'mfg' => 'Thailand', 'liv' => 'Land Rover G4',
            'cdt' => 'white',
            'tdt' => 'white, LAND ROVER G4 CHALLENGE',
	    'nts' => '2006 Convoy Wheels',
	],
	['var' => '08a', 'mfg' => 'Thailand', 'liv' => 'Honey Nut Cherrios',
            'cdt' => '',
            'tdt' => '',
	    'nts' => '2006 Convoy Wheels',
	],
	['var' => '09a', 'mfg' => 'China', 'liv' => 'Firestone Racing',
            'cdt' => 'white',
            'tdt' => 'white, FIRESTONE RACING',
	    'nts' => '2006 Convoy Wheels',
	],
    ]);
}
?>
