<?php // DONE
$subtitle = 'CY002A';
// CY-2-A KENWORTH ROCKET TRANSPORTER, issued 1982
$desc = "Kenworth Rocket Transporters";
$year = '1982';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Silver-gray cab with tempa on front, chrome exhausts, white SB-SB Space Shuttle, England casting (GS)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB045', 'tlr' => 'Rocket Transporter', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
	    'cdt' => 'silver-gray cab with tampo on front, chrome exhausts',
	    'tdt' => 'white Skybusters Space Shuttle',
	],
// 2. Silver-gray cab with tempa on front, chrome exhausts, white plastic rocket, England casting 
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB045', 'tlr' => 'Rocket Transporter', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
	    'cdt' => 'silver-gray cab with tampo on front, chrome exhausts',
	    'tdt' => 'white plastic rocket',
	],
// 3. Silver-gray cab without tempa on front, chrome exhausts, white plastic rocket, England casting 
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB045', 'tlr' => 'Rocket Transporter', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
	    'cdt' => 'silver-gray cab without tampo on front, chrome exhausts',
	    'tdt' => 'white plastic rocket',
	],
// 4. Pearly silver cab, chrome exhausts, white plastic rocket, Macau casting 
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB045', 'tlr' => 'Rocket Transporter', 'mfg' => 'Macau',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
	    'cdt' => 'pearly silver, chrome exhausts',
	    'tdt' => 'white plastic rocket',
	],
// 5. White cab, chrome exhausts, white plastic rocket, Macau casting 
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'MB045', 'tlr' => 'Rocket Transporter', 'mfg' => 'Macau',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
	    'cdt' => 'white, chrome exhausts',
	    'tdt' => 'white plastic rocket',
	],
// 6. White cab, gray exhausts, white plastic rocket, Macau casting 
	['mod' => $subtitle, 'var' => '06a',
	    'cab' => 'MB045', 'tlr' => 'Rocket Transporter', 'mfg' => 'Macau',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
	    'cdt' => 'white, gray exhausts',
	    'tdt' => 'white plastic rocket',
	],
// 7. White cab, gray exhausts, white plastic rocket, Thailand casting 
	['mod' => $subtitle, 'var' => '07a',
	    'cab' => 'MB045', 'tlr' => 'Rocket Transporter', 'mfg' => 'Thailand',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
	    'cdt' => 'white, gray exhausts',
	    'tdt' => 'white plastic rocket',
	],
// 8. White cab, gray exhausts, chrome plastic rocket, Thailand casting 
	['mod' => $subtitle, 'var' => '08a',
	    'cab' => 'MB045', 'tlr' => 'Rocket Transporter', 'mfg' => 'Thailand',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
	    'cdt' => 'white, gray exhausts',
	    'tdt' => 'chrome plastic rocket',
	],
// 9. White cab, gray exhausts, chrome plastic rocket, China casting 
	['mod' => $subtitle, 'var' => '09a',
	    'cab' => 'MB045', 'tlr' => 'Rocket Transporter', 'mfg' => 'China',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
	    'cdt' => 'white, gray exhausts',
	    'tdt' => 'chrome plastic rocket',
	],
    ]);
}
?>
