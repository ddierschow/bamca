<?php // DONE
$subtitle = 'CY116A';
$desc = "Ford Aeromax with Tanker V2";
$year = '20??';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB214', 'tlr' => 'Tanker V2', 'mfg' => 'Thailand',
	    'liv' => 'Shell', 'cod' => '1', 'rar' => '',
            'cdt' => 'silver-gray',
            'tdt' => 'silver-gray, SHELL',
	],
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB214', 'tlr' => 'Tanker V2', 'mfg' => 'Thailand',
	    'liv' => 'Conoco', 'cod' => '1', 'rar' => '',
            'cdt' => 'white',
            'tdt' => 'gray, CONOCO',
	],
    ]);
}
