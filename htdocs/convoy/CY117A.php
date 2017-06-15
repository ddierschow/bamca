<?php // DONE
$subtitle = 'CY117A';
$desc = "Tractor Cab with Tanker V2";
$year = '2006';

$defaults = ['mod' => $subtitle, 'cab' => 'MB664', 'tlr' => 'Tanker V2', 'cod' => '1'];

include "cypage.php";

function body() {
    show_table([
	['var' => '01a', 'mfg' => 'Thailand', 'liv' => 'D.U.M.P.',
            'cdt' => 'matte orange',
            'tdt' => 'matte orange, D.U.M.P.',
	],
	['var' => '02a', 'mfg' => 'Thailand', 'liv' => '76',
            'cdt' => 'red',
            'tdt' => 'silver-gray, 76',
	],
	['var' => '03a', 'mfg' => 'Thailand', 'liv' => 'Philips 66',
            'cdt' => 'black',
            'tdt' => 'silver-gray, PHILIPS 66',
	],
	['var' => '04a', 'mfg' => 'Thailand', 'liv' => 'Air Products',
            'cdt' => 'green',
            'tdt' => 'green, AIR PRODUCTS',
	],
    ]);
}
?>
