<?php // DONE
$subtitle = 'CY033A';
// CY-33-A MACK HELICOPTER TRANSPORTER, issued 1992
$desc = "Mack Helicopter Transporter";
$year = '1992';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. White cab, blue chassis, white carriage with blue base, "Police" tampo; MB153 Mission Helicopter in white & dark blue (EM)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB202', 'tlr' => 'Helicopter Transporter', 'mfg' => 'Thailand',
	    'liv' => 'Police', 'cod' => '1', 'rar' => '3',
	    'crd' => 'Simon Rogers - AU',
            'cdt' => 'white, blue chassis',
            'tdt' => 'white carriage with blue base, POLICE tampo, MB153 Mission Helicopter in white and dark blue',
	],
// 2. White cab, green chassis, green carriage with silver-gray base, "Polizei" tampo; MB153 Mission Helicopter in green and white (EM)
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB202', 'tlr' => 'Helicopter Transporter', 'mfg' => 'Thailand',
	    'liv' => 'Polizei', 'cod' => '1', 'rar' => '3',
	    'crd' => 'Simon Rogers - AU',
            'cdt' => 'white, green chassis',
            'tdt' => 'green carriage with silver-gray base, POLIZEI tampo, MB153 Mission Helicopter in green and white',
	],
// 3. White cab, black chassis, white carriage with black base, "Police" tampo; MB153 Mission Helicopter in black and white (EM)
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB202', 'tlr' => 'Helicopter Transporter', 'mfg' => 'Thailand',
	    'liv' => 'Police', 'cod' => '1', 'rar' => '3',
	    'crd' => 'Simon Rogers - AU',
            'cdt' => 'white, black chassis',
            'tdt' => 'white carriage with black base, POLICE tampo, MB153 Mission Helicopter in black and white',
	],
// 4. White cab, black chassis, white carriage with black base, "Rijkspolitie" tampo; MB153 Mission Helicopter in white and neon orange (DU)(EM)
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB202', 'tlr' => 'Helicopter Transporter', 'mfg' => 'Thailand',
	    'liv' => 'Rijkspolitie', 'cod' => '1', 'rar' => '3',
	    'crd' => 'Simon Rogers - AU',
            'cdt' => 'white, black chassis',
            'tdt' => 'white carriage with black base, RIJKSPOLITIE tampo, MB153 Mission Helicopter in white and neon orange',
	],
    ]);
}
?>
