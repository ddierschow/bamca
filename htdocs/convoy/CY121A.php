<?php // DONE
$subtitle = 'CY121A';
$desc = "Flat Bed";
$year = '20??';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB725', 'tlr' => 'Flat Bed V2', 'mfg' => 'Thailand',
	    'liv' => '', 'cod' => '1', 'rar' => '',
            'cdt' => '',
            'tdt' => '',
	],
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB725', 'tlr' => 'Flat Bed V2', 'mfg' => 'Thailand',
	    'liv' => '', 'cod' => '1', 'rar' => '',
            'cdt' => '',
            'tdt' => '',
	],
    ]);
}
?>
