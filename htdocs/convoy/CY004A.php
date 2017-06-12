<?php // DONE
$subtitle = 'CY004A';
// CY-4-A KENWORTH BOAT TRANSPORTER, issued 1982
$desc = "Peterbilt Boat";
$year = '1982';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Light orange cab, boat with light orange hull & green windows, silver-gray trailer, England casting 
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB103', 'tlr' => 'Lowboy', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'light orange',
	    'tdt' => 'silver-gray, boat with light orange hull and green windows',
	],
// 2. Light orange cab, boat with dark orange hull & green windows, silver-gray trailer, England casting 
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB103', 'tlr' => 'Lowboy', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'light orange',
	    'tdt' => 'silver-gray, boat with dark orange hull and green windows',
	    'crd' => 'Keith Borden',
	],
// 3. Dark orange cab, boat with dark orange hull & green windows, silver-gray trailer, England casting 
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB103', 'tlr' => 'Lowboy', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'dark orange',
	    'tdt' => 'silver-gray, boat with dark orange hull and green windows',
	],
// 4. Dark orange cab, boat with light orange hull & green windows, silver-gray trailer, England casting 
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB103', 'tlr' => 'Lowboy', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'dark orange',
	    'tdt' => 'silver-gray, boat with light orange hull and green windows',
	],
// 5. Dark orange cab, boat with dark orange hull & red windows, silver-gray trailer, England casting 
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'MB103', 'tlr' => 'Lowboy', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
	    'crd' => 'Keith Borden',
            'cdt' => 'dark orange',
	    'tdt' => 'silver-gray, boat with dark orange hull and red windows',
	],
// 6. Dark orange cab, boat with dark orange hull & clear windows, silver-gray trailer, England casting 
	['mod' => $subtitle, 'var' => '06a',
	    'cab' => 'MB103', 'tlr' => 'Lowboy', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'dark orange',
	    'tdt' => 'silver-gray, boat with dark orange hull and clear windows',
	],
// 7. Dark orange cab, boat with dark orange hull & green windows, pearly silver trailer, Macau casting 
	['mod' => $subtitle, 'var' => '07a',
	    'cab' => 'MB103', 'tlr' => 'Lowboy', 'mfg' => 'Macau',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'dark orange',
	    'tdt' => 'pearly silver, boat with dark orange hull and green windows',
	],
// 8. Very light orange cab, boat with dark orange hull & green windows, pearly silver trailer, Macau casting (S6-8)
	['mod' => $subtitle, 'var' => '08a',
	    'cab' => 'MB103', 'tlr' => 'Lowboy', 'mfg' => 'Macau',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'very light orange',
	    'tdt' => 'pearly silver, boat with dark orange hull and green windows',
	],
    ]);
}
?>
