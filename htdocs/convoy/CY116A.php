<?php // DONE
$subtitle = 'CY116A';
$desc = "Ford Aeromax with Tanker V2";
$year = '2006';

$defaults = ['mod' => $subtitle, 'cab' => 'MB214', 'tlr' => 'Tanker V2', 'cod' => '1'];

include "cypage.php";

function body() {
    show_table([
	['var' => '01a', 'mfg' => 'Thailand', 'liv' => 'Shell',
            'cdt' => 'silver-gray',
            'tdt' => 'silver-gray, SHELL',
	],
	['var' => '02a', 'mfg' => 'Thailand', 'liv' => 'Conoco',
            'cdt' => 'white',
            'tdt' => 'gray, CONOCO',
	],
    ]);
}
