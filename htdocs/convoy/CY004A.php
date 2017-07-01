<?php // DONE
$subtitle = 'CY004A';
// CY-4-A KENWORTH BOAT TRANSPORTER, issued 1982
$desc = "Peterbilt Boat";
$year = '1982';

$defaults = ['mod' => $subtitle,
	    'cab' => 'MB103', 'tlr' => 'CYT08', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1',
];

include "cypage.php";

function body() {
    show_table([
// 1. Light orange cab, boat with light orange hull & green windows, silver-gray trailer, England casting 
	['var' => '01a', 'mfg' => 'England',
            'cdt' => 'light orange',
	    'tdt' => 'silver-gray, boat with light orange hull and green windows',
	],
// 2. Light orange cab, boat with dark orange hull & green windows, silver-gray trailer, England casting 
	['var' => '02a', 'mfg' => 'England', 'crd' => 'Keith Borden',
            'cdt' => 'light orange',
	    'tdt' => 'silver-gray, boat with dark orange hull and green windows',
	],
// 3. Dark orange cab, boat with dark orange hull & green windows, silver-gray trailer, England casting 
	['var' => '03a', 'mfg' => 'England',
            'cdt' => 'dark orange',
	    'tdt' => 'silver-gray, boat with dark orange hull and green windows',
	],
// 4. Dark orange cab, boat with light orange hull & green windows, silver-gray trailer, England casting 
	['var' => '04a', 'mfg' => 'England',
            'cdt' => 'dark orange',
	    'tdt' => 'silver-gray, boat with light orange hull and green windows',
	],
// 5. Dark orange cab, boat with dark orange hull & red windows, silver-gray trailer, England casting 
	['var' => '05a', 'mfg' => 'England', 'crd' => 'Keith Borden',
            'cdt' => 'dark orange',
	    'tdt' => 'silver-gray, boat with dark orange hull and red windows',
	],
// 6. Dark orange cab, boat with dark orange hull & clear windows, silver-gray trailer, England casting 
	['var' => '06a', 'mfg' => 'England',
            'cdt' => 'dark orange',
	    'tdt' => 'silver-gray, boat with dark orange hull and clear windows',
	],
// 7. Dark orange cab, boat with dark orange hull & green windows, pearly silver trailer, Macau casting 
	['var' => '07a', 'mfg' => 'Macau',
            'cdt' => 'dark orange',
	    'tdt' => 'pearly silver, boat with dark orange hull and green windows',
	],
// 8. Very light orange cab, boat with dark orange hull & green windows, pearly silver trailer, Macau casting (S6-8)
	['var' => '08a', 'mfg' => 'Macau',
            'cdt' => 'very light orange',
	    'tdt' => 'pearly silver, boat with dark orange hull and green windows',
	],
    ]);
}
?>
