<?php // DONE
$subtitle = 'CY118A';
$desc = "DAF XF95 with Tanker V2";
$year = '20??';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Red cab, red container, yellow trailer, "Linfox" tempa, Macau casting (AU)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB702', 'tlr' => 'Tanker V2', 'mfg' => 'Thailand',
	    'liv' => 'Jet', 'cod' => '1', 'rar' => '',
            'cdt' => 'yellow',
            'tdt' => 'yellow, JET',
	],
    ]);
}
?>
