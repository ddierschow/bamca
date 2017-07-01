<?php // DONE
$subtitle = 'TP002C';
// TP 2-C ARTICULATED PETROL TANKER, issued 1981
$desc = "Leyland Articulated Petrol Tanker";
$year = '1981';

$defaults = ['mod' => $subtitle, 'cab' => 'T9CO', 'tlr' => 'CYT06', 'mfg' => 'England', 'cod' => '1'];

include "cypage.php";

function body() {
    show_table([
// 1. Red cab & trailer, white tank, green windows, "Exxon" labels
	['var' => '01a', 'liv' => 'Exxon',
            'cdt' => 'red, green windows',
            'tdt' => 'red, whtie tank, EXXON labels',
	],
// 2. Red cab & trailer, white tank, amber windows, "Exxon" labels
	['var' => '02a', 'liv' => 'Exxon',
            'cdt' => 'red, amber windows',
            'tdt' => 'red, whtie tank, EXXON labels',
	],
    ]);
}
?>
