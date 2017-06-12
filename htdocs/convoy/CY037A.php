<?php // DONE
$subtitle = 'CY037A';
// CY-37-A FORD AEROMAX TRANSPORTER, issued 1993
$desc = "Ford Aeromax Transporter";
$year = '1993';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Yellow cab, black chassis, yellow container, "Radical Cams" labels, 8-spoke wheels 
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB214', 'tlr' => 'Racing Transporter', 'mfg' => 'Macau',
	    'liv' => 'Radical Cams', 'cod' => '1', 'rar' => '',
            'cdt' => 'yellow, black chassis',
            'tdt' => 'yellow container, RADICAL CAMS labels, 8-spoke wheels',
	],
// 2. Red cab, black chassis, yellow container, "RTF-Safety Information" labels, 8-spoke wheels (AU)(C2)
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB214', 'tlr' => 'Racing Transporter', 'mfg' => 'Macau',
	    'liv' => 'RTF', 'cod' => '2', 'rar' => '',
            'cdt' => 'red, black chassis',
            'tdt' => 'yellow container, RTF-SAFETY INFORMATION labels, 8-spoke wheels',
	],
// 3. White cab, black chassis, white container, "North American" tampo, rubber tires, antennas cast (PC)
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB308', 'tlr' => 'Racing Transporter', 'mfg' => 'Macau',
	    'liv' => 'North American', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, black chassis',
            'tdt' => 'white container, NORTH AMERICAN tampo',
	],
    ]);
}
?>
