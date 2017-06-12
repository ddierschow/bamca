<?php // DONE
$subtitle = 'CY203A';
// CY-203-A CONSTRUCTION LOW LOADER, issued 1989
$desc = "Construction Low Loader";
$year = '1989';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Yellow cab, pearly silver trailer, MB032 Excavator, Macau castings (MC)
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB724', 'tlr' => 'Lowboy', 'mfg' => 'Macau',
	    'liv' => 'Pace', 'cod' => '1', 'rar' => '3',
            'cdt' => 'yellow',
            'tdt' => 'pearly silver, with MB032 Excavator',
	    'nts' => 'Issued as part of Construction Sets',
	],
// 2. Yellow cab, pearly silver trailer, MB032 Excavator, Thailand castings (MC)
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB724', 'tlr' => 'Lowboy', 'mfg' => 'Thailand',
	    'liv' => 'Pace', 'cod' => '1', 'rar' => '3',
            'cdt' => 'yellow',
            'tdt' => 'pearly silver, with MB032 Excavator',
	],
    ]);
}
?>
