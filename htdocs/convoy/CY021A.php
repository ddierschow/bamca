<?php // DONE
$subtitle = 'CY021A';
// CY-21-A DAF AIRCRAFT TRANSPORTER, issued 1987
$desc = "DAF Airplane Transporter ";
$year = '1987';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. White cab, blue chassis with "Space Cab" tampo, dark blue trailer, orange plane with "Airtrainer" tampo, Macau
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB183', 'tlr' => 'Airplane Transporter', 'mfg' => 'Macau',
	    'liv' => 'none', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white, blue chassis with SPACE CAB tampo',
            'tdt' => 'dark blue, orange plane with AIRTRAINER tampo',
	],
// 2. White cab, dark blue chassis with "Red Rebels" tampo, white trailer, red plane with "Red Rebels" tampo, Macau (MC)
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB183', 'tlr' => 'Airplane Transporter', 'mfg' => 'Macau',
	    'liv' => 'none', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white, dark blue chassis, RED REBELS tampo',
            'tdt' => 'white, red plane, RED REBELS tampo',
	],
// 3. Black cab, gray chassis with "AC102" tampo, black trailer, black plane with "AC102" tampo, Macau (CM)
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB183', 'tlr' => 'Airplane Transporter', 'mfg' => 'Macau',
	    'liv' => 'none', 'cod' => '1', 'rar' => '3',
            'cdt' => 'black, gray chassis, AC102 tampo',
            'tdt' => 'black, black plane, AC102 tampo',
	    'nts' => 'Part of a Commando Series Multi Pack',
	],
// 4. White cab and chassis with no tampo, white trailer, white plane with no tampo, Thailand (GF)(GS)
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB183', 'tlr' => 'Airplane Transporter', 'mfg' => 'Thailand',
	    'liv' => 'none', 'cod' => '1', 'rar' => '4',
            'cdt' => 'white',
            'tdt' => 'white, no tampo',
	    'nts' => 'Graffic Traffic',
	],
// 5. White cab, red chassis with "Acrobatic Team" and "Flying Aces" tampo, red trailer, blue plane with "Flying Aces" tampo, Thailand
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'MB183', 'tlr' => 'Airplane Transporter', 'mfg' => 'Thailand',
	    'liv' => 'none', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white, red chassis, ACROBATIC TEAM and FLYING ACES tampo',
            'tdt' => 'red, blue plane, FLYING ACES tampo',
	],
// 6. White cab, dark blue chassis with "Red Rebels" tampo, white trailer, red plane with "Red Rebels" tampo, Thailand
	['mod' => $subtitle, 'var' => '06a',
	    'cab' => 'MB183', 'tlr' => 'Airplane Transporter', 'mfg' => 'Thailand',
	    'liv' => 'none', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white, dark blue chassis, RED REBELS tampo',
            'tdt' => 'white, red plane, RED REBELS tampo',
	],
// 7. White cab, red chassis with "Aerobatic Team" and "Flying Aces" tampo, red trailer, blue plane with "Flying Aces" tampo, China
	['mod' => $subtitle, 'var' => '07a',
	    'cab' => 'MB183', 'tlr' => 'Airplane Transporter', 'mfg' => 'China',
	    'liv' => 'none', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white, red chassis, ACROBATIC TEAM and FLYING ACES tampo',
            'tdt' => 'red, blue plane, FLYING ACES tampo',
	],
    ]);
}
?>
