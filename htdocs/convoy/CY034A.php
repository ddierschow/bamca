<?php // DONE
$subtitle = 'CY034A';
// CY-34-A PETERBILT EMERGENCY CENTER, issued 1992
$desc = "Peterbilt Emergency Center";
$year = '1992';

$defaults = ['mod' => $subtitle];

include "cypage.php";

function body() {
    show_table([
// 1. Florescent orange cab, florescent orange trailer with gray roof & white boom, "Rescue" with checkers tampo (EM)
	['var' => '01a', 'cab' => 'MB106', 'tlr' => 'CYT20', 'mfg' => 'Thailand',
	    'liv' => 'Rescue', 'cod' => '1', 'rar' => '2',
            'cdt' => 'florescent orange',
            'tdt' => 'florescent orange with gray roof and white boom, RESCUE with checkers tampo',
	],
    ]);
}
?>
