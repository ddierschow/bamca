<?php // DONE
$subtitle = 'CY030A';
// CY-30-A GROVE CRANE, issued 1992
$desc = "Grove AT1000 Crane";
$year = '1992';

$defaults = ['mod' => $subtitle, 'cab' => 'CY030', 'tlr' => 'CY030', 'cod' => '1'];

$models = [
// 1. Orange-yellow body, red crane cab, yellow boom, red hook, "AT1100" tampo (CS)
    ['var' => '01a', 'mfg' => 'Thailand', 'liv' => 'Grove', 'rar' => '3',
	'cdt' => 'orange-yellow body', 'cva' => '',
	'tdt' => 'red crane cab, yellow boom, red hook, AT1100 tampo',
    ],
// 2. Orange-yellow body, red crane cab, yellow boom, maroon hook, "AT1100" tampo (CS)
    ['var' => '02a', 'mfg' => 'Thailand', 'liv' => 'Grove', 'rar' => '3',
	'cdt' => 'orange-yellow body', 'cva' => '',
	'tdt' => 'red crane cab, yellow boom, maroon hook, AT1100 tampo',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
