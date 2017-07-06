<?php // DONE
$subtitle = 'CY203A';
// CY-203-A CONSTRUCTION LOW LOADER, issued 1989
$desc = "Construction Low Loader";
$year = '1989';

$defaults = ['mod' => $subtitle, 'cab' => 'MI724', 'tlr' => 'CYT07', 'cod' => '1'];

$models = [
// 1. Yellow cab, pearly silver trailer, MB032 Excavator, Macau castings (MC)
    ['var' => '01a', 'mfg' => 'Macau', 'liv' => 'Pace', 'rar' => '3',
	'cdt' => 'yellow', 'cva' => '02B',
	'tdt' => 'pearly silver, with MB032 Excavator',
	'nts' => 'Issued as part of Construction Sets',
    ],
// 2. Yellow cab, pearly silver trailer, MB032 Excavator, Thailand castings (MC)
    ['var' => '02a', 'mfg' => 'Thailand', 'liv' => 'Pace', 'rar' => '3',
	'cdt' => 'yellow', 'cva' => '02B',
	'tdt' => 'pearly silver, with MB032 Excavator',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
