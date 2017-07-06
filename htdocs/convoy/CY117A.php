<?php // DONE
$subtitle = 'CY117A';
$desc = "Tractor Cab with Tanker V2";
$year = '2006';

$defaults = ['mod' => $subtitle, 'cab' => 'MB664', 'tlr' => 'CYT29', 'cod' => '1'];

$models = [
    ['var' => '01a', 'mfg' => 'Thailand', 'liv' => 'D.U.M.P.',
	'cdt' => 'matte orange', 'cva' => '12',
	'tdt' => 'matte orange, D.U.M.P.',
    ],
    ['var' => '02a', 'mfg' => 'Thailand', 'liv' => '76',
	'cdt' => 'red', 'cva' => '08',
	'tdt' => 'silver-gray, 76',
    ],
    ['var' => '03a', 'mfg' => 'Thailand', 'liv' => 'Philips 66',
	'cdt' => 'black', 'cva' => '10',
	'tdt' => 'silver-gray, PHILIPS 66',
    ],
    ['var' => '04a', 'mfg' => 'Thailand', 'liv' => 'Air Products',
	'cdt' => 'green', 'cva' => '14',
	'tdt' => 'green, AIR PRODUCTS',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
