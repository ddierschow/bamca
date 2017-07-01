<?php // DONE
$subtitle = 'CY120A';
$desc = "DAF Space Cab with Fishbelly";
$year = '2007';

$defaults = ['mod' => $subtitle, 'cab' => 'MB702', 'tlr' => 'CYT28', 'mfg' => 'Thailand', 'cod' => '1'];

include "cypage.php";

function body() {
    show_table([
	['var' => '01a', 'liv' => 'Wheaties',
            'cdt' => 'white',
            'tdt' => 'white',
	],
	['var' => '02a', 'liv' => 'Simpson Racing',
            'cdt' => 'red',
            'tdt' => 'silver-gray',
	],
    ]);
}
?>
