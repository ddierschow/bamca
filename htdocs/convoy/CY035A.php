<?php // DONE
$subtitle = 'CY035A';
// CY-35-A MACK TANKER, issued 1992
$desc = "Mack Tanker";
$year = '1992';

$defaults = ['mod' => $subtitle, 'cab' => 'MB202', 'tlr' => 'CYT06', 'cod' => '1'];

$models = [
// 1. White and florescent green cab, florescent green chassis, chrome base, chrome tank with florescent green base, "Orange Juice" tampo, no antennas cast, 8-spoke wheels, Thailand
    ['var' => '01a', 'mfg' => 'Thailand', 'liv' => '',
	'cdt' => 'white and florescent green, florescent green chassis, chrome base', 'cva' => '11',
	'tdt' => 'chrome tank with florescent green base, ORANGE JUICE tampo, 8-spoke wheels',
    ],
// 2. White and florescent green cab, florescent green chassis, gray base, chrome tank with florescent green base, "Orange Juice" tampo, no antennas cast, 8-spoke wheels, Thailand
    ['var' => '02a', 'mfg' => 'Thailand', 'liv' => '',
	'cdt' => 'white and florescent green, florescent green chassis, gray base', 'cva' => '16',
	'tdt' => 'chrome tank with florescent green base, ORANGE JUICE tampo, 8-spoke wheels',
    ],
// 3. Yellow cab with black chassis, chrome base, chrome tank with dark green base, "Shell" tampo, antennas cast, rubber tires, China (PC)
    ['var' => '03a', 'cab' => 'MB311', 'mfg' => 'China', 'liv' => '',
	'cdt' => 'yellow with black chassis, chrome base', 'cva' => '',
	'tdt' => 'chrome tank with dark green base, SHELL tampo',
    ],
// 4. White cab with gray chassis, gray base, white tank with gray base, "Shell" tampo, 8-spoke wheels, "Mattel" and China (ROW)
    ['var' => '04a', 'mfg' => 'China, MATTEL', 'liv' => '',
	'cdt' => 'white with gray chassis, gray base', 'cva' => '49',
	'tdt' => 'white tank with gray base, SHELL tampo, 8-spoke wheels',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
