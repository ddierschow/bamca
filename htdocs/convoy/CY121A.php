<?php // DONE
$subtitle = 'CY121A';
$desc = "Flat Bed";
$year = '2008';

$defaults = ['mod' => $subtitle, 'cab' => 'MB725', 'tlr' => 'CYT30', 'cod' => '1'];

include "cypage.php";

function body() {
    show_table([
	['var' => '01a', 'mfg' => 'Thailand',
            'cdt' => '',
            'tdt' => '',
	],
	['var' => '02a', 'mfg' => 'Thailand',
            'cdt' => '',
            'tdt' => '',
	],
    ]);
}
?>
