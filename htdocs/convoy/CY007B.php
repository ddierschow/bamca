<?php // DONE
$subtitle = 'CY007B';
// CY-7-B FORD AEROMAX GAS TANKER, issued 1998
$desc = "Ford Aeromax Tanker";
$year = '1998';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Bright blue cab with black chassis, chrome tank with blue chassis, "Exxon" tempa, antennas cast, rubber tires (PC)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB308', 'tlr' => 'Tanker', 'mfg' => 'China',
	    'liv' => 'Exxon', 'cod' => '1', 'rar' => '2',
            'cdt' => 'blue with black chassis',
            'tdt' => 'blue with chrome tank, EXXON tampo',
	],
// 2. White cab with white chassis, white tank with white chassis, no tempa, no antennas cast, 8-spoke wheels (ASAP blank)
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB308', 'tlr' => 'Tanker', 'mfg' => 'China',
	    'liv' => 'none', 'cod' => '2', 'rar' => '3',
            'cdt' => 'white',
            'tdt' => 'white',
	    'nts' => 'ASAP blank',
	],
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB308', 'tlr' => 'Tanker', 'mfg' => 'China',
	    'liv' => 'MOPAC', 'cod' => '2', 'rar' => '4',
            'cdt' => 'white',
            'tdt' => 'white, MOPAC',
	],
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB308', 'tlr' => 'Tanker', 'mfg' => 'China',
	    'liv' => 'J &amp; S Oil', 'cod' => '2', 'rar' => '4',
            'cdt' => 'white',
            'tdt' => 'white, J &amp; S Oil',
	],
    ]);
}
?>
