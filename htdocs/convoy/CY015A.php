<?php // DONE
$subtitle = 'CY015A';
// CY-15-A PETERBILT TRACKING VEHICLE, issued 1985
$desc = "Peterbilt Tracking";
$year = '1985';

$defaults = ['mod' => $subtitle,
	    'cab' => 'MB106', 'tlr' => 'Tracking', 'mfg' => 'Macau',
	    'liv' => 'NASA', 'cod' => '1', 'rar' => '2',
	];
include "cypage.php";

function body() {
    show_table([
// 1. White cab with "NASA" tampo, chrome exhausts, white container with pearly silver base, "NASA" tampo, Macau
	['var' => '01a', 'mfg' => 'Macau', 'liv' => 'NASA', 'rar' => '2',
            'cdt' => 'white with NASA tampo, chrome exhausts',
            'tdt' => 'white container with pearly silver base, NASA tampo',
	],
// 2. Yellow cab with no tampo, chrome exhausts, yellow container with pearly silver base, "British Telecom" tampo, Macau (GS)
	['var' => '02a', 'mfg' => 'Macau', 'liv' => 'British Telecom', 'rar' => '2',
            'cdt' => 'yellow with no tampo, chrome exhausts',
            'tdt' => 'yellow container with pearly silver base, BRITISH TELECOM tampo',
	],
// 3. Powder blue cab with "Satellite TV" and bolt tampo, chrome exhausts, powder blue container with pearly silver base, "MB TV News" tampo, Macau
	['var' => '03a', 'mfg' => 'Macau', 'liv' => 'Matchbox', 'rar' => '3',
            'cdt' => 'powder blue with SATELLITE TV and bolt tampo, chrome exhausts',
            'tdt' => 'powder blue container with pearly silver base, MB TV NEWS tampo',
	    'add' =>
[['The only difference between variations 03 and 04 is the tampo on the hood of the cab.',
'<img src="/pic/set/convoy/m_cy015a_03a1.jpg">']],
	],
// 4. Powder blue cab with "Peterbilt" and bolt tampo, chrome exhausts, powder blue container with pearly silver base, "MB TV News" tampo, Macau
	['var' => '04a', 'mfg' => 'Macau', 'liv' => 'Matchbox', 'rar' => '2',
            'cdt' => 'powder blue with PETERBILT and bolt tampo, chrome exhausts',
            'tdt' => 'powder blue container with pearly silver base, MB TV NEWS tampo',
	],
// 5.  Powder blue cab with "Peterbilt" and bolt tampo, gray exhausts, powder blue container with pearly silver base, "MB TV News" tampo, Macau
	['var' => '05a', 'mfg' => 'Macau', 'liv' => 'Matchbox', 'rar' => '2',
            'cdt' => 'powder blue with PETERBILT and bolt tampo, gray exhausts',
            'tdt' => 'powder blue container with pearly silver base, MB TV NEWS tampo',
	],
// 6. Olive cab with "Strike Team" tampo, black base and exhausts, olive container with olive base, "LS2009" tampo, Macau (CM)
	['var' => '06a', 'mfg' => 'Macau', 'liv' => 'none', 'rar' => '3',
            'cdt' => 'olive with STRIKE TEAM tampo, black base and exhausts',
            'tdt' => 'olive container with olive base, LS2009 tampo',
	    'nts' => 'Commando',
	],
// 7. Dark blue cab with "Peterbilt" and bolt tampo, gray exhausts, dark blue container with pearly silver base, "MB TV News" tampo, Macau
	['var' => '07a', 'mfg' => 'Macau', 'liv' => 'Matchbox', 'rar' => '2',
            'cdt' => 'dark blue with PETERBILT and bolt tampo, gray exhausts',
            'tdt' => 'dark blue container with pearly silver base, MB TV NEWS tampo',
	],
// 8. Dark blue cab with "Peterbilt" and bolt tampo, gray exhausts, dark blue container with pearly silver base, "MB TV News" tampo, Thailand
	['var' => '08a', 'mfg' => 'Thailand', 'liv' => 'Matchbox', 'rar' => '2',
            'cdt' => 'dark blue with PETERBILT and bolt tampo, gray exhausts',
            'tdt' => 'dark blue container with pearly silver base, MB TV NEWS tampo',
	],
// 9. Powder blue cab with "Peterbilt" and bolt tampo, gray exhausts, powder blue container with pearly silver base, "MB TV News" tampo, Thailand
	['var' => '09a', 'mfg' => 'Thailand', 'liv' => 'Matchbox', 'rar' => '2',
            'cdt' => 'powder blue with PETERBILT and bolt tampo, gray exhausts',
            'tdt' => 'powder blue container with pearly silver base, MB TV NEWS tampo',
	],
// 10. White cab with "Sky TV" tampo, gray exhausts, white container with pearly silver base, "Sky Satellite TV" tampo, Thailand
	['var' => '10a', 'mfg' => 'Thailand', 'liv' => 'Sky TV', 'rar' => '2',
            'cdt' => 'white cab with SKY TV tampo, gray exhausts',
            'tdt' => 'white container with pearly silver base, SKY SATELLITE TV tampo',
	],
// 11. White cab with "Sky TV" tampo, chrome exhausts, white container with pearly silver base, "Sky Satellite TV" tampo, Thailand
	['var' => '11a', 'mfg' => 'Thailand', 'liv' => 'Sky TV', 'rar' => '2',
            'cdt' => 'white cab with SKY TV tampo, chrome exhausts',
            'tdt' => 'white container with pearly silver base, SKY SATELLITE TV tampo',
	],
    ]);
}
?>
