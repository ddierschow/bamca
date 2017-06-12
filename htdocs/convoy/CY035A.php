<?php // DONE
$subtitle = 'CY035A';
// CY-35-A MACK TANKER, issued 1992
$desc = "Mack Tanker";
$year = '1992';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. White and florescent green cab, florescent green chassis, chrome base, chrome tank with florescent green base, "Orange Juice" tampo, no antennas cast, 8-spoke wheels, Thailand
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB202', 'tlr' => 'Tanker', 'mfg' => 'Thailand',
	    'liv' => '', 'cod' => '1', 'rar' => '',
            'cdt' => 'white and florescent green, florescent green chassis, chrome base',
            'tdt' => 'chrome tank with florescent green base, ORANGE JUICE tampo, 8-spoke wheels',
	],
// 2. White and florescent green cab, florescent green chassis, gray base, chrome tank with florescent green base, "Orange Juice" tampo, no antennas cast, 8-spoke wheels, Thailand
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB202', 'tlr' => 'Tanker', 'mfg' => 'Thailand',
	    'liv' => '', 'cod' => '1', 'rar' => '',
            'cdt' => '',
            'tdt' => '',
            'cdt' => 'white and florescent green, florescent green chassis, gray base',
            'tdt' => 'chrome tank with florescent green base, ORANGE JUICE tampo, 8-spoke wheels',
	],
// 3. Yellow cab with black chassis, chrome base, chrome tank with dark green base, "Shell" tampo, antennas cast, rubber tires, China (PC)
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB311', 'tlr' => 'Tanker', 'mfg' => 'China',
	    'liv' => '', 'cod' => '1', 'rar' => '',
            'cdt' => 'yellow with black chassis, chrome base',
            'tdt' => 'chrome tank with dark green base, SHELL tampo',
	],
// 4. White cab with gray chassis, gray base, white tank with gray base, "Shell" tampo, 8-spoke wheels, "Mattel" and China (ROW)
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB202', 'tlr' => 'Tanker', 'mfg' => 'China, MATTEL',
	    'liv' => '', 'cod' => '1', 'rar' => '',
            'cdt' => 'white with gray chassis, gray base',
            'tdt' => 'white tank with gray base, SHELL tampo, 8-spoke wheels',
	],
    ]);
}
?>
