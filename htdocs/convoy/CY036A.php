<?php // DONE
$subtitle = 'CY036A';
// CY-36-A KEN WORTH TRANSPORTER, issued 1992
$desc = "Kenworth Transporter";
$year = '1992';

$defaults = ['mod' => $subtitle, 'cab' => 'MB103', 'tlr' => 'CYT17', 'cod' => '1'];

include "cypage.php";

function body() {
// NOTE: All models with 8-spoke wheels 8 no antennas cast unless otherwise noted.
    show_table([
// 1. White cab, white container with black base, "Charitoys" labels, Thailand casting (US)
	['var' => '01a', 'mfg' => 'Thailand', 'liv' => 'Charitoys',
            'cdt' => 'white',
            'tdt' => 'white container with black base, CHARITOYS labels',
	],
// 2. Orange cab, black container with black base, "Trick Truckin" labels, Thailand casting 
	['var' => '02a', 'mfg' => 'Thailand', 'liv' => 'Trick Truckin',
            'cdt' => 'orange',
            'tdt' => 'black container with black base, TRICK TRUCKIN labels',
	],
// 3. Fluorescent orange cab, yellow container with black base, "Matchbox-Get in the Fast Lane" labels, Thailand casting 
	['var' => '03a', 'mfg' => 'Thailand', 'liv' => 'Matchbox',
            'cdt' => 'fluorescent orange',
            'tdt' => 'yellow container with black base, MATCHBOX-GET IN THE FAST LANE labels',
	],
// 4. Fluorescent orange cab, yellow container with black base, "Matchbox-Get in the Fast Lane" labels, China casting 
	['var' => '04a', 'mfg' => 'China', 'liv' => 'Matchbox',
            'cdt' => 'fluorescent orange',
            'tdt' => 'yellow container with black base, MATCHBOX-GET IN THE FAST LANE labels',
	],
// 5. Powder blue cab, powder blue container with black base, "RTF-Safety Information" labels, Thailand casting (AU)
	['var' => '05a', 'mfg' => 'Thailand', 'liv' => 'RTF',
            'cdt' => 'powder blue',
            'tdt' => 'powder blue container with black base, RTF-SAFETY INFORMATION labels',
	],
// 6. Dark blue cab, dark blue container with black base, "Heritage Design" labels, China casting, rubber tires, antennas cast (GS)
	['var' => '06a', 'cab' => 'MB310', 'mfg' => 'China', 'liv' => 'Heritage Design',
            'cdt' => 'dark blue',
            'tdt' => 'dark blue container with black base, HERITAGE DESIGN labels',
	],
    ]);
}
?>
