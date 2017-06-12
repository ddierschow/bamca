<?php // DONE
$subtitle = 'CY117A';
$desc = "Kenworth Box Truck";
$desc = "Tractor Cab with Tanker V2";
$year = '20??';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB664', 'tlr' => 'Tanker V2', 'mfg' => 'Thailand',
	    'liv' => 'D.U.M.P.', 'cod' => '1', 'rar' => '',
            'cdt' => 'matte orange',
            'tdt' => 'matte orange, D.U.M.P.',
	],
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB664', 'tlr' => 'Tanker V2', 'mfg' => 'Thailand',
	    'liv' => '76', 'cod' => '1', 'rar' => '',
            'cdt' => 'red',
            'tdt' => 'silver-gray, 76',
	],
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB664', 'tlr' => 'Tanker V2', 'mfg' => 'Thailand',
	    'liv' => 'Philips 66', 'cod' => '1', 'rar' => '',
            'cdt' => 'black',
            'tdt' => 'silver-gray, PHILIPS 66',
	],
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB664', 'tlr' => 'Tanker V2', 'mfg' => 'Thailand',
	    'liv' => 'Air Products', 'cod' => '1', 'rar' => '',
            'cdt' => 'green',
            'tdt' => 'green, AIR PRODUCTS',
	],
    ]);
}
?>
