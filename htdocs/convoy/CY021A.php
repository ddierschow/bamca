<?php // DONE
$subtitle = 'CY021A';
// CY-21-A DAF AIRCRAFT TRANSPORTER, issued 1987
$desc = "DAF Airplane Transporter ";
$year = '1987';

$defaults = ['mod' => $subtitle, 'cab' => 'MB183', 'tlr' => 'Airplane Transporter', 'cod' => '1'];

include "cypage.php";

function body() {
    show_table([
// 1. White cab, blue chassis with "Space Cab" tampo, dark blue trailer, orange plane with "Airtrainer" tampo, Macau
	['var' => '01a', 'mfg' => 'Macau', 'liv' => 'none', 'rar' => '2',
            'cdt' => 'white, blue chassis with SPACE CAB tampo',
            'tdt' => 'dark blue, orange plane with AIRTRAINER tampo',
	],
// 2. White cab, dark blue chassis with "Red Rebels" tampo, white trailer, red plane with "Red Rebels" tampo, Macau (MC)
	['var' => '02a', 'mfg' => 'Macau', 'liv' => 'none', 'rar' => '2',
            'cdt' => 'white, dark blue chassis, RED REBELS tampo',
            'tdt' => 'white, red plane, RED REBELS tampo',
	],
// 3. Black cab, gray chassis with "AC102" tampo, black trailer, black plane with "AC102" tampo, Macau (CM)
	['var' => '03a', 'mfg' => 'Macau', 'liv' => 'none', 'rar' => '3',
            'cdt' => 'black, gray chassis, AC102 tampo',
            'tdt' => 'black, black plane, AC102 tampo',
	    'nts' => 'Part of a Commando Series Multi Pack',
	],
// 4. White cab and chassis with no tampo, white trailer, white plane with no tampo, Thailand (GF)(GS)
	['var' => '04a', 'mfg' => 'Thailand', 'liv' => 'none', 'rar' => '4',
            'cdt' => 'white',
            'tdt' => 'white, no tampo',
	    'nts' => 'Graffic Traffic',
	],
// 5. White cab, red chassis with "Acrobatic Team" and "Flying Aces" tampo, red trailer, blue plane with "Flying Aces" tampo, Thailand
	['var' => '05a', 'mfg' => 'Thailand', 'liv' => 'none', 'rar' => '2',
            'cdt' => 'white, red chassis, ACROBATIC TEAM and FLYING ACES tampo',
            'tdt' => 'red, blue plane, FLYING ACES tampo',
	],
// 6. White cab, dark blue chassis with "Red Rebels" tampo, white trailer, red plane with "Red Rebels" tampo, Thailand
	['var' => '06a', 'mfg' => 'Thailand', 'liv' => 'none', 'rar' => '2',
            'cdt' => 'white, dark blue chassis, RED REBELS tampo',
            'tdt' => 'white, red plane, RED REBELS tampo',
	],
// 7. White cab, red chassis with "Aerobatic Team" and "Flying Aces" tampo, red trailer, blue plane with "Flying Aces" tampo, China
	['var' => '07a', 'mfg' => 'China', 'liv' => 'none', 'rar' => '2',
            'cdt' => 'white, red chassis, ACROBATIC TEAM and FLYING ACES tampo',
            'tdt' => 'red, blue plane, FLYING ACES tampo',
	],
    ]);
}
?>
