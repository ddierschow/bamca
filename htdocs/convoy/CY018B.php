<?php // DONE
$subtitle = 'CY018B';
// CY-18-B FORD AEROMAX DOUBLE CONTAINER TRUCK, issued 1993
$desc = "Ford Aeromax Double Container Truck";
$year = '1993';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Black cab and chassis, black flatbed with black containers, "Charitoys 1993" tampo, 8-spoke wheels, Thailand (WR)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB214', 'tlr' => 'Box', 'mfg' => 'Thailand',
	    'liv' => 'Charitoys', 'cod' => '2', 'rar' => '',
            'cdt' => 'black, black chassis',
            'tdt' => 'black flatbed with black containers, CHARITOYS 1993 tampo, 8-spoke wheels',
	],
// 2. White cab with black chassis, blue flatbed with white containers, "American Airlines" tampo, antennas cast, rubber tires, China (PC)
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB308', 'tlr' => 'Box', 'mfg' => 'China',
	    'liv' => 'American Airlines', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, black chassis',
            'tdt' => 'blue flatbed, white containers, AMERICAN AIRLINES tampo',
	],
// 3. Orange cab with black chassis, black flatbed with white containers, "U-Haul" labels, antennas cast, rubber tires, China (PC)
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB308', 'tlr' => 'Box', 'mfg' => 'China',
	    'liv' => 'U-Haul', 'cod' => '1', 'rar' => '',
            'cdt' => 'orange, black chassis',
            'tdt' => 'black flatbed, white containers, U-HAUL labels',
	],
    ]);
}
?>
