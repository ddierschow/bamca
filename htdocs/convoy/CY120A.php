<?php // DONE
$subtitle = 'CY120A';
$desc = "DAF Space Cab with Fishbelly";
$year = '20??';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB702', 'tlr' => 'Fishbelly', 'mfg' => 'Thailand',
	    'liv' => 'Wheaties', 'cod' => '1', 'rar' => '',
            'cdt' => 'white',
            'tdt' => 'white',
	],
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB702', 'tlr' => 'Fishbelly', 'mfg' => 'Thailand',
	    'liv' => 'Simpson Racing', 'cod' => '1', 'rar' => '',
            'cdt' => 'red',
            'tdt' => 'silver-gray',
	],
    ]);
}
?>
