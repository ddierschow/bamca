<?php // DONE
$subtitle = 'CY007B';
// CY-7-B FORD AEROMAX GAS TANKER, issued 1998
$desc = "Ford Aeromax Tanker";
$year = '1998';

$defaults = ['mod' => $subtitle,
	    'cab' => 'MB308', 'tlr' => 'Tanker', 'mfg' => 'China',
	    'liv' => 'none', 'cod' => '1',
	];

include "cypage.php";

function body() {
    show_table([
// 1. Bright blue cab with black chassis, chrome tank with blue chassis, "Exxon" tempa, antennas cast, rubber tires (PC)
	['var' => '01a', 'liv' => 'Exxon', 'rar' => '2',
            'cdt' => 'blue with black chassis',
            'tdt' => 'blue with chrome tank, EXXON tampo',
	],
// 2. White cab with white chassis, white tank with white chassis, no tempa, no antennas cast, 8-spoke wheels (ASAP blank)
	['var' => '02a', 'liv' => 'none', 'cod' => '2', 'rar' => '3',
            'cdt' => 'white',
            'tdt' => 'white',
	    'nts' => 'ASAP blank',
	],
	['var' => '03a', 'liv' => 'MOPAC', 'cod' => '2', 'rar' => '4',
            'cdt' => 'white',
            'tdt' => 'white, MOPAC',
	],
	['var' => '04a', 'liv' => 'J &amp; S Oil', 'cod' => '2', 'rar' => '4',
            'cdt' => 'white',
            'tdt' => 'white, J &amp; S Oil',
	],
    ]);
}
?>
