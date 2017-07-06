<?php // DONE
$subtitle = 'CY010A';
// CY-10-A RACING TRANSPORTER, issued 1983
$desc = "Kenworth Racing Transporter";
$year = '1983';

$defaults = ['mod' => $subtitle, 'cab' => 'CY010', 'tlr' => 'CY010', 'mfg' => '', 'cod' => '1'];

$models = [
// 1. White body, "Tyrone Malone" tampo, MB66-D Super Boss with green windows
    ['var' => '01a', 'liv' => 'Tyrone Malone',
	'cdt' => 'white, TYRONE MALONE tampo', 'cva' => '',
	'tdt' => 'white MB066 Super Boss with green windows',
    ],
// 2. White body, "Tyrone Malone" tampo, MB66-D Super Boss with red windows 
    ['var' => '02a', 'liv' => 'Tyrone Malone',
	'cdt' => 'white, TYRONE MALONE tampo', 'cva' => '',
	'tdt' => 'white MB066 Super Boss with red windows',
    ],

    ['var' => 'c3a', 'liv' => 'none',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white MB066 Super Boss with green windows',
	'nts' => 'Assembled from two different Graffic Traffic Sets',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
