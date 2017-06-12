<?php // DONE
$subtitle = 'CY032B';
// CY-32-B PETERBILT LOWLOADER WITH BULLDOZER, issued 1998
$desc = "Peterbilt with Lowboy trailer";
$year = '1998';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Orange-yellow cab with "Matchbox" tampo, orange-yellow trailer, antennas cast, rubber tires, includes MB64-D36 Caterpillar Bulldozer (PC)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB307', 'tlr' => 'Lowboy', 'mfg' => 'China',
	    'liv' => 'Matchbox', 'cod' => '1', 'rar' => '2',
            'cdt' => 'orange-yellow with MATCHBOX tampo',
            'tdt' => 'orange-yellow with MB064 Caterpillar bulldozer',
	],
// 2. Yellow cab with "CAT" tampo, yellow trailer, antennas cast, rubber tires, includes MB64-D38 Caterpillar Bulldozer (PC)
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB307', 'tlr' => 'Lowboy', 'mfg' => 'China',
	    'liv' => 'Caterpillar', 'cod' => '1', 'rar' => '2',
            'cdt' => 'yellow with CAT tampo',
            'tdt' => 'yellow with MB64D Caterpillar bulldozer',
	],
    ]);
}
?>
