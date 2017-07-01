<?php // DONE
$subtitle = 'CY018B';
// CY-18-B FORD AEROMAX DOUBLE CONTAINER TRUCK, issued 1993
$desc = "Ford Aeromax Double Container Truck";
$year = '1993';

$defaults = ['mod' => $subtitle, 'tlr' => 'CYT02', 'cod' => '1'];

include "cypage.php";

function body() {
    show_table([
// 1. Black cab and chassis, black flatbed with black containers, "Charitoys 1993" tampo, 8-spoke wheels, Thailand (WR)
	['var' => '01a', 'cab' => 'MB214', 'mfg' => 'Thailand', 'liv' => 'Charitoys', 'cod' => '2',
            'cdt' => 'black, black chassis',
            'tdt' => 'black flatbed with black containers, CHARITOYS 1993 tampo, 8-spoke wheels',
	    'nts' => 'Manufactured for White Rose',
	],
// 2. White cab with black chassis, blue flatbed with white containers, "American Airlines" tampo, antennas cast, rubber tires, China (PC)
	['var' => '02a', 'cab' => 'MB308', 'mfg' => 'China', 'liv' => 'American Airlines',
            'cdt' => 'white, black chassis',
            'tdt' => 'blue flatbed, white containers, AMERICAN AIRLINES tampo',
	],
// 3. Orange cab with black chassis, black flatbed with white containers, "U-Haul" labels, antennas cast, rubber tires, China (PC)
	['var' => '03a', 'cab' => 'MB308', 'mfg' => 'China', 'liv' => 'U-Haul',
            'cdt' => 'orange, black chassis',
            'tdt' => 'black flatbed, white containers, U-HAUL labels',
	],
    ]);
}
?>
