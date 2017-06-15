<?php // DONE
$subtitle = 'CY032B';
// CY-32-B PETERBILT LOWLOADER WITH BULLDOZER, issued 1998
$desc = "Peterbilt with Lowboy trailer";
$year = '1998';

$defaults = ['mod' => $subtitle, 'cab' => 'MB307', 'tlr' => 'Lowboy with Bulldozer', 'cod' => '1'];

include "cypage.php";

function body() {
    show_table([
// 1. Orange-yellow cab with "Matchbox" tampo, orange-yellow trailer, antennas cast, rubber tires, includes MB64-D36 Caterpillar Bulldozer (PC)
	['var' => '01a', 'mfg' => 'China', 'liv' => 'Matchbox', 'rar' => '2',
            'cdt' => 'orange-yellow with MATCHBOX tampo',
            'tdt' => 'orange-yellow with MB064 Caterpillar bulldozer',
	],
// 2. Yellow cab with "CAT" tampo, yellow trailer, antennas cast, rubber tires, includes MB64-D38 Caterpillar Bulldozer (PC)
	['var' => '02a', 'mfg' => 'China', 'liv' => 'Caterpillar', 'rar' => '2',
            'cdt' => 'yellow with CAT tampo',
            'tdt' => 'yellow with MB64D Caterpillar bulldozer',
	],
    ]);
}
?>
