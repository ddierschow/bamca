<?php // DONE
$subtitle = 'TP002C';
// TP 2-C ARTICULATED PETROL TANKER, issued 1981
$desc = "Leyland Articulated Petrol Tanker";
$year = '1981';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Red cab & trailer, white tank, green windows, "Exxon" labels
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'T9CO', 'tlr' => 'Tanker', 'mfg' => 'England',
	    'liv' => 'Exxon', 'cod' => '1', 'rar' => '',
            'cdt' => 'red, green windows',
            'tdt' => 'red, whtie tank, EXXON labels',
	],
// 2. Red cab & trailer, white tank, amber windows, "Exxon" labels
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'T9CO', 'tlr' => 'Tanker', 'mfg' => 'England',
	    'liv' => 'Exxon', 'cod' => '1', 'rar' => '',
            'cdt' => 'red, amber windows',
            'tdt' => 'red, whtie tank, EXXON labels',
	],
    ]);
}
?>
