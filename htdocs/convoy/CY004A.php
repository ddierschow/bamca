<?php // DONE
$subtitle = 'CY004A';
// CY-4-A KENWORTH BOAT TRANSPORTER, issued 1982
$desc = "Peterbilt Boat";
$year = '1982';

$defaults = ['mod' => $subtitle,
	    'cab' => 'MB103', 'tlr' => 'CYT08', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1',
];

$models = [
// 1. Light orange cab, boat with light orange hull & green windows, silver-gray trailer, England casting 
    ['var' => '01a', 'mfg' => 'England',
	'cdt' => 'light orange', 'cva' => '005B',
	'tdt' => 'silver-gray, boat with light orange hull and green windows',
    ],
// 2. Light orange cab, boat with dark orange hull & green windows, silver-gray trailer, England casting 
    ['var' => '02a', 'mfg' => 'England',
	'cdt' => 'light orange', 'cva' => '005B',
	'tdt' => 'silver-gray, boat with dark orange hull and green windows',
    ],
// 3. Dark orange cab, boat with dark orange hull & green windows, silver-gray trailer, England casting 
    ['var' => '03a', 'mfg' => 'England',
	'cdt' => 'dark orange', 'cva' => '006B',
	'tdt' => 'silver-gray, boat with dark orange hull and green windows',
    ],
// 4. Dark orange cab, boat with light orange hull & green windows, silver-gray trailer, England casting 
    ['var' => '04a', 'mfg' => 'England',
	'cdt' => 'dark orange', 'cva' => '006B',
	'tdt' => 'silver-gray, boat with light orange hull and green windows',
    ],
// 5. Dark orange cab, boat with dark orange hull & red windows, silver-gray trailer, England casting 
    ['var' => '05a', 'mfg' => 'England',
	'cdt' => 'dark orange', 'cva' => '006B',
	'tdt' => 'silver-gray, boat with dark orange hull and red windows',
    ],
// 6. Dark orange cab, boat with dark orange hull & clear windows, silver-gray trailer, England casting 
    ['var' => '06a', 'mfg' => 'England',
	'cdt' => 'dark orange', 'cva' => '006B',
	'tdt' => 'silver-gray, boat with dark orange hull and colorless windows',
    ],
// 7. Dark orange cab, boat with dark orange hull & green windows, pearly silver trailer, Macau casting 
    ['var' => '07a', 'mfg' => 'Macau',
	'cdt' => 'dark orange', 'cva' => '006B',
	'tdt' => 'pearly silver, boat with dark orange hull and green windows',
    ],
// 8. Very light orange cab, boat with dark orange hull & green windows, pearly silver trailer, Macau casting (S6-8)
    ['var' => '08a', 'mfg' => 'Macau',
	'cdt' => 'very light orange', 'cva' => '016BA',
	'tdt' => 'pearly silver, boat with dark orange hull and green windows',
    ],
    ['var' => '08b', 'mfg' => 'Macau',
	'cdt' => 'very light orange', 'cva' => '016BA',
	'tdt' => 'pearly silver, boat with dark orange hull and colorless windows',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
