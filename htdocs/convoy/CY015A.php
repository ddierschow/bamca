<?php // DONE
$subtitle = 'CY015A';
// CY-15-A PETERBILT TRACKING VEHICLE, issued 1985
$desc = "Peterbilt Tracking";
$year = '1985';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. White cab with "NASA" tampo, chrome exhausts, white container with pearly silver base, "NASA" tampo, Macau
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB106', 'tlr' => 'Tracking', 'mfg' => 'Macau',
	    'liv' => 'NASA', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white with NASA tampo, chrome exhausts',
            'tdt' => 'white container with pearly silver base, NASA tampo',
	],
// 2. Yellow cab with no tampo, chrome exhausts, yellow container with pearly silver base, "British Telecom" tampo, Macau (GS)
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB106', 'tlr' => 'Tracking', 'mfg' => 'Macau',
	    'liv' => 'British Telecom', 'cod' => '1', 'rar' => '2',
            'cdt' => 'yellow with no tampo, chrome exhausts',
            'tdt' => 'yellow container with pearly silver base, BRITISH TELECOM tampo',
	],
// 3. Powder blue cab with "Satellite TV" and bolt tampo, chrome exhausts, powder blue container with pearly silver base, "MB TV News" tampo, Macau
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB106', 'tlr' => 'Tracking', 'mfg' => 'Macau',
	    'liv' => 'Matchbox', 'cod' => '1', 'rar' => '3',
            'cdt' => 'powder blue with SATELLITE TV and bolt tampo, chrome exhausts',
            'tdt' => 'powder blue container with pearly silver base, MB TV NEWS tampo',
	],
// 4. Powder blue cab with "Peterbilt" and bolt tampo, chrome exhausts, powder blue container with pearly silver base, "MB TV News" tampo, Macau
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB106', 'tlr' => 'Tracking', 'mfg' => 'Macau',
	    'liv' => 'Matchbox', 'cod' => '1', 'rar' => '2',
            'cdt' => 'powder blue with PETERBILT and bolt tampo, chrome exhausts',
            'tdt' => 'powder blue container with pearly silver base, MB TV NEWS tampo',
	],
// 5.  Powder blue cab with "Peterbilt" and bolt tampo, gray exhausts, powder blue container with pearly silver base, "MB TV News" tampo, Macau
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'MB106', 'tlr' => 'Tracking', 'mfg' => 'Macau',
	    'liv' => 'Matchbox', 'cod' => '1', 'rar' => '2',
            'cdt' => 'powder blue with PETERBILT and bolt tampo, gray exhausts',
            'tdt' => 'powder blue container with pearly silver base, MB TV NEWS tampo',
	],
// 6. Olive cab with "Strike Team" tampo, black base and exhausts, olive container with olive base, "LS2009" tampo, Macau (CM)
	['mod' => $subtitle, 'var' => '06a',
	    'cab' => 'MB106', 'tlr' => 'Tracking', 'mfg' => 'Macau',
	    'liv' => 'none', 'cod' => '1', 'rar' => '3',
            'cdt' => 'olive with STRIKE TEAM tampo, black base and exhausts',
            'tdt' => 'olive container with olive base, LS2009 tampo',
	    'nts' => 'Commando',
	],
// 7. Dark blue cab with "Peterbilt" and bolt tampo, gray exhausts, dark blue container with pearly silver base, "MB TV News" tampo, Macau
	['mod' => $subtitle, 'var' => '07a',
	    'cab' => 'MB106', 'tlr' => 'Tracking', 'mfg' => 'Macau',
	    'liv' => 'Matchbox', 'cod' => '1', 'rar' => '2',
            'cdt' => 'dark blue with PETERBILT and bolt tampo, gray exhausts',
            'tdt' => 'dark blue container with pearly silver base, MB TV NEWS tampo',
	],
// 8. Dark blue cab with "Peterbilt" and bolt tampo, gray exhausts, dark blue container with pearly silver base, "MB TV News" tampo, Thailand
	['mod' => $subtitle, 'var' => '08a',
	    'cab' => 'MB106', 'tlr' => 'Tracking', 'mfg' => 'Thailand',
	    'liv' => 'Matchbox', 'cod' => '1', 'rar' => '2',
            'cdt' => 'dark blue with PETERBILT and bolt tampo, gray exhausts',
            'tdt' => 'dark blue container with pearly silver base, MB TV NEWS tampo',
	],
// 9. Powder blue cab with "Peterbilt" and bolt tampo, gray exhausts, powder blue container with pearly silver base, "MB TV News" tampo, Thailand
	['mod' => $subtitle, 'var' => '09a',
	    'cab' => 'MB106', 'tlr' => 'Tracking', 'mfg' => 'Thailand',
	    'liv' => 'Matchbox', 'cod' => '1', 'rar' => '2',
            'cdt' => 'powder blue with PETERBILT and bolt tampo, gray exhausts',
            'tdt' => 'powder blue container with pearly silver base, MB TV NEWS tampo',
	],
// 10. White cab with "Sky TV" tampo, gray exhausts, white container with pearly silver base, "Sky Satellite TV" tampo, Thailand
	['mod' => $subtitle, 'var' => '10a',
	    'cab' => 'MB106', 'tlr' => 'Tracking', 'mfg' => 'Thailand',
	    'liv' => 'Sky TV', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white cab with SKY TV tampo, gray exhausts',
            'tdt' => 'white container with pearly silver base, SKY SATELLITE TV tampo',
	],
// 11. White cab with "Sky TV" tampo, chrome exhausts, white container with pearly silver base, "Sky Satellite TV" tampo, Thailand
	['mod' => $subtitle, 'var' => '11a',
	    'cab' => 'MB106', 'tlr' => 'Tracking', 'mfg' => 'Thailand',
	    'liv' => 'Sky TV', 'cod' => '1', 'rar' => '2',
            'cdt' => 'white cab with SKY TV tampo, chrome exhausts',
            'tdt' => 'white container with pearly silver base, SKY SATELLITE TV tampo',
	],
    ]);
}
?>
