<?php // DONE
$subtitle = 'CY012A';
// CY-12-A KENWORTH PLANE TRANSPORTER, issued 1984
$desc = "Kenworth Airplane Transporter";
$year = '1984';

$defaults = ['mod' => $subtitle, 'cab' => 'MB045', 'tlr' => 'CYT12',
	    'liv' => 'none', 'cod' => '1',
	];

$models = [
// 1. White cab with blue and dark green tampo, silver-gray trailer, blue plane with "Darts" tampo, England casting 
    ['var' => '01a', 'mfg' => 'England',
	'cdt' => 'white cab with blue and dark green tampo', 'cva' => '015',
	'tdt' => 'silver-gray, blue plane with DARTS tampo',
    ],
// 2. White cab with blue and brown tampo, silver-gray trailer, blue plane with "Darts" tampo, England casting 
    ['var' => '02a', 'mfg' => 'England',
	'cdt' => 'white cab with blue and brown tampo', 'cva' => '036',
	'tdt' => 'silver-gray, blue plane with DARTS tampo',
    ],
// 3. White cab with 2-tone blue tampo, pearly silver trailer, blue plane with "Darts" tampo, Macau casting 
    ['var' => '03a', 'mfg' => 'Macau',
	'cdt' => 'white cab with 2-tone blue tampo', 'cva' => '018',
	'tdt' => 'pearly silver, blue plane with DARTS tampo',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
