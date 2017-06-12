<?php // DONE
$subtitle = 'CY010A';
// CY-10-A RACING TRANSPORTER, issued 1983
$desc = "Kenworth Racing Transporter";
$year = '1983';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. White body, "Tyrone Malone" tampo, MB66-D Super Boss with green windows
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => '',
	    'liv' => 'Tyrone Malone', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, TYRONE MALONE tampo',
            'tdt' => 'white MB066 Super Boss with green windows',
	],
// 2. White body, "Tyrone Malone" tampo, MB66-D Super Boss with red windows 
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => '',
	    'liv' => 'Tyrone Malone', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, TYRONE MALONE tampo',
            'tdt' => 'white MB066 Super Boss with red windows',
	],

	['mod' => $subtitle, 'var' => 'c3a',
	    'cab' => 'CY010', 'tlr' => 'Racing transporter, part of cab casting', 'mfg' => '',
	    'liv' => 'none', 'cod' => '3', 'rar' => '',
            'cdt' => 'white',
            'tdt' => 'white MB066 Super Boss with green windows',
	    'nts' => 'Assembled from two different Graffic Traffic Sets',
	],
    ]);
}
?>
