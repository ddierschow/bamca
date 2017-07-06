<?php // DONE
$subtitle = 'CY033A';
// CY-33-A MACK HELICOPTER TRANSPORTER, issued 1992
$desc = "Mack Helicopter Transporter";
$year = '1992';

$defaults = ['mod' => $subtitle, 'cab' => 'MB202', 'tlr' => 'CYT21', 'cod' => '1'];

$models = [
// 1. White cab, blue chassis, white carriage with blue base, "Police" tampo; MB153 Mission Helicopter in white & dark blue (EM)
    ['var' => '01a', 'mfg' => 'Thailand', 'liv' => 'Police', 'rar' => '3',
	'crd' => 'Simon Rogers - AU',
	'cdt' => 'white, blue chassis', 'cva' => '',
	'tdt' => 'white carriage with blue base, POLICE tampo, MB153 Mission Helicopter in white and dark blue',
    ],
// 2. White cab, green chassis, green carriage with silver-gray base, "Polizei" tampo; MB153 Mission Helicopter in green and white (EM)
    ['var' => '02a', 'mfg' => 'Thailand', 'liv' => 'Polizei', 'rar' => '3',
	'crd' => 'Simon Rogers - AU',
	'cdt' => 'white, green chassis', 'cva' => '',
	'tdt' => 'green carriage with silver-gray base, POLIZEI tampo, MB153 Mission Helicopter in green and white',
    ],
// 3. White cab, black chassis, white carriage with black base, "Police" tampo; MB153 Mission Helicopter in black and white (EM)
    ['var' => '03a', 'mfg' => 'Thailand', 'liv' => 'Police', 'rar' => '3',
	'crd' => 'Simon Rogers - AU',
	'cdt' => 'white, black chassis', 'cva' => '',
	'tdt' => 'white carriage with black base, POLICE tampo, MB153 Mission Helicopter in black and white',
    ],
// 4. White cab, black chassis, white carriage with black base, "Rijkspolitie" tampo; MB153 Mission Helicopter in white and neon orange (DU)(EM)
    ['var' => '04a', 'mfg' => 'Thailand', 'liv' => 'Rijkspolitie', 'rar' => '3',
	'crd' => 'Simon Rogers - AU',
	'cdt' => 'white, black chassis', 'cva' => '',
	'tdt' => 'white carriage with black base, RIJKSPOLITIE tampo, MB153 Mission Helicopter in white and neon orange',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
