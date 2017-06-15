<?php // DONE
$subtitle = 'CY106A';
// CY-106-A PETERBILT ARTICULATED TIPPER, issued 1990 (AU)
$desc = "Peterbilt Tipper";
$year = '1990';

$defaults = ['mod' => $subtitle];

include "cypage.php";

function body() {
    show_table([
// 1. Pink cab, gray tipper with black base, "Readymix" tempa (AU)
	['var' => '01a',
	    'cab' => 'MB106', 'tlr' => 'Tipper', 'mfg' => 'Thailand',
	    'liv' => 'Readymix', 'cod' => '1', 'rar' => '2',
            'cdt' => 'pink',
            'tdt' => 'gray tipper with black base, READYMIX tampo',
	],
    ]);
}
?>
