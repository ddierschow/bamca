<?php // DONE
$subtitle = 'CY002A';
// CY-2-A KENWORTH ROCKET TRANSPORTER, issued 1982
$desc = "Kenworth Rocket Transporters";
$year = '1982';

$defaults = ['mod' => $subtitle, 'cab' => 'MB045', 'tlr' => 'CYT10', 'liv' => 'none', 'cod' => '1'];

include "cypage.php";

function body() {
    show_table([
// 1. Silver-gray cab with tempa on front, chrome exhausts, white SB-SB Space Shuttle, England casting (GS)
	['var' => '01a', 'mfg' => 'England',
	    'tlr' => 'CYT07',
	    'cdt' => 'silver-gray cab with tampo on front, chrome exhausts',
	    'tdt' => 'white Skybusters Space Shuttle',
	],
// 2. Silver-gray cab with tempa on front, chrome exhausts, white plastic rocket, England casting 
	['var' => '02a', 'mfg' => 'England',
	    'cdt' => 'silver-gray cab with tampo on front, chrome exhausts',
	    'tdt' => 'white plastic rocket',
	],
// 3. Silver-gray cab without tempa on front, chrome exhausts, white plastic rocket, England casting 
	['var' => '03a', 'mfg' => 'England',
	    'cdt' => 'silver-gray cab without tampo on front, chrome exhausts',
	    'tdt' => 'white plastic rocket',
	],
// 4. Pearly silver cab, chrome exhausts, white plastic rocket, Macau casting 
	['var' => '04a', 'mfg' => 'Macau',
	    'cdt' => 'pearly silver, chrome exhausts',
	    'tdt' => 'white plastic rocket',
	],
// 5. White cab, chrome exhausts, white plastic rocket, Macau casting 
	['var' => '05a', 'mfg' => 'Macau',
	    'cdt' => 'white, chrome exhausts',
	    'tdt' => 'white plastic rocket',
	],
// 6. White cab, gray exhausts, white plastic rocket, Macau casting 
	['var' => '06a', 'mfg' => 'Macau',
	    'cdt' => 'white, gray exhausts',
	    'tdt' => 'white plastic rocket',
	],
// 7. White cab, gray exhausts, white plastic rocket, Thailand casting 
	['var' => '07a', 'mfg' => 'Thailand',
	    'cdt' => 'white, gray exhausts',
	    'tdt' => 'white plastic rocket',
	],
// 8. White cab, gray exhausts, chrome plastic rocket, Thailand casting 
	['var' => '08a', 'mfg' => 'Thailand',
	    'cdt' => 'white, gray exhausts',
	    'tdt' => 'chrome plastic rocket',
	],
// 9. White cab, gray exhausts, chrome plastic rocket, China casting 
	['var' => '09a', 'mfg' => 'China',
	    'cdt' => 'white, gray exhausts',
	    'tdt' => 'chrome plastic rocket',
	],
    ]);
}
?>
