<?php // DONE
$subtitle = 'CY036A';
// CY-36-A KEN WORTH TRANSPORTER, issued 1992
$desc = "Kenworth Transporter";
$year = '1992';
include "cypage.php";

function body() {
    global $subtitle;

// NOTE: All models with 8-spoke wheels 8 no antennas cast unless otherwise noted.
    show_table([
// 1. White cab, white container with black base, "Charitoys" labels, Thailand casting (US)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB103', 'tlr' => 'Racing Transporter', 'mfg' => 'Thailand',
	    'liv' => 'Charitoys', 'cod' => '1', 'rar' => '',
            'cdt' => 'white',
            'tdt' => 'white container with black base, CHARITOYS labels',
	],
// 2. Orange cab, black container with black base, "Trick Truckin" labels, Thailand casting 
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB103', 'tlr' => 'Racing Transporter', 'mfg' => 'Thailand',
	    'liv' => 'Trick Truckin', 'cod' => '1', 'rar' => '',
            'cdt' => 'orange',
            'tdt' => 'black container with black base, TRICK TRUCKIN labels',
	],
// 3. Fluorescent orange cab, yellow container with black base, "Matchbox-Get in the Fast Lane" labels, Thailand casting 
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB103', 'tlr' => 'Racing Transporter', 'mfg' => 'Thailand',
	    'liv' => 'Matchbox', 'cod' => '1', 'rar' => '',
            'cdt' => 'fluorescent orange',
            'tdt' => 'yellow container with black base, MATCHBOX-GET IN THE FAST LANE labels',
	],
// 4. Fluorescent orange cab, yellow container with black base, "Matchbox-Get in the Fast Lane" labels, China casting 
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB103', 'tlr' => 'Racing Transporter', 'mfg' => 'China',
	    'liv' => 'Matchbox', 'cod' => '1', 'rar' => '',
            'cdt' => 'fluorescent orange',
            'tdt' => 'yellow container with black base, MATCHBOX-GET IN THE FAST LANE labels',
	],
// 5. Powder blue cab, powder blue container with black base, "RTF-Safety Information" labels, Thailand casting (AU)
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'MB103', 'tlr' => 'Racing Transporter', 'mfg' => 'Thailand',
	    'liv' => 'RTF', 'cod' => '1', 'rar' => '',
            'cdt' => 'powder blue',
            'tdt' => 'powder blue container with black base, RTF-SAFETY INFORMATION labels',
	],
// 6. Dark blue cab, dark blue container with black base, "Heritage Design" labels, China casting, rubber tires, antennas cast (GS)
	['mod' => $subtitle, 'var' => '06a',
	    'cab' => 'MB310', 'tlr' => 'Racing Transporter', 'mfg' => 'China',
	    'liv' => 'Heritage Design', 'cod' => '1', 'rar' => '',
            'cdt' => 'dark blue',
            'tdt' => 'dark blue container with black base, HERITAGE DESIGN labels',
	],
    ]);
}
?>
