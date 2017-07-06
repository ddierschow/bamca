<?php // DONE
$subtitle = 'CY037A';
// CY-37-A FORD AEROMAX TRANSPORTER, issued 1993
$desc = "Ford Aeromax Transporter";
$year = '1993';

$defaults = ['mod' => $subtitle, 'cab' => 'MB214', 'tlr' => 'CYT17', 'cod' => '1'];

$models = [
// 1. Yellow cab, black chassis, yellow container, "Radical Cams" labels, 8-spoke wheels 
    ['var' => '01a', 'mfg' => 'Macau', 'liv' => 'Radical Cams',
	'cdt' => 'yellow, black chassis', 'cva' => '',
	'tdt' => 'yellow container, RADICAL CAMS labels, 8-spoke wheels',
    ],
// 2. Red cab, black chassis, yellow container, "RTF-Safety Information" labels, 8-spoke wheels (AU)(C2)
    ['var' => '02a', 'mfg' => 'Macau', 'liv' => 'RTF', 'cod' => '2',
	'cdt' => 'red, black chassis', 'cva' => '',
	'tdt' => 'yellow container, RTF-SAFETY INFORMATION labels, 8-spoke wheels',
    ],
// 3. White cab, black chassis, white container, "North American" tampo, rubber tires, antennas cast (PC)
    ['var' => '03a', 'cab' => 'MB308', 'mfg' => 'Macau', 'liv' => 'North American',
	'cdt' => 'white, black chassis', 'cva' => '',
	'tdt' => 'white container, NORTH AMERICAN tampo',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
