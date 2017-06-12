<?php // DONE
$subtitle = 'CY012A';
// CY-12-A KENWORTH PLANE TRANSPORTER, issued 1984
$desc = "Kenworth Airplane Transporter";
$year = '1984';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. White cab with blue and dark green tampo, silver-gray trailer, blue plane with "Darts" tampo, England casting 
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB045', 'tlr' => 'Airplane transporter', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'white cab with blue and dark green tampo',
            'tdt' => 'silver-gray, blue plane with DARTS tampo',
	],
// 2. White cab with blue and brown tampo, silver-gray trailer, blue plane with "Darts" tampo, England casting 
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB045', 'tlr' => 'Airplane transporter', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'white cab with blue and brown tampo',
            'tdt' => 'silver-gray, blue plane with DARTS tampo',
	],
// 3. White cab with 2-tone blue tampo, pearly silver trailer, blue plane with "Darts" tampo, Macau casting 
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB045', 'tlr' => 'Airplane transporter', 'mfg' => 'Macau',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'white cab with 2-tone blue tampo',
            'tdt' => 'pearly silver, blue plane with DARTS tampo',
	],
    ]);
}
?>
