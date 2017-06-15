<?php // DONE
$subtitle = 'CY803A';
// CY-803-A SCANIA LOW LOADER WITH DODGE TRUCK, issued 1992 (DU)
$desc = "Scan Low Loader";
$year = '1992';

$defaults = ['mod' => $subtitle, 'cab' => 'MB147', 'tlr' => 'Lowboy with Cargo Truck', 'cod' => '1'];

include "cypage.php";

function body() {
    show_table([
// 1. Red cab with silver-gray trailer; MB072 Dodge Truck with "Wigwam" tempa (DU)
	['var' => '01a', 'mfg' => 'Thailand', 'liv' => 'Wigwam', 'rar' => '3',
            'cdt' => 'red',
            'tdt' => 'silver-gray, includes MB072 Dodge Truck with WIGWAM tampo',
	    'nts' => 'Dutch promotional issue',
	],
    ]);
}
?>
