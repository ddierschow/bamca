<?php // DONE
$subtitle = 'CY020A';
// CY-20-A ARTICULATED DUMP TRUCK, issued 1987
$desc = "Kenworth &amp; Scania Tipper";
$year = '1987';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. MB45-C cab in yellow, chrome exhausts, yellow trailer with black base, "Taylor Woodrow" tampo, Macau casting 
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB045', 'tlr' => 'Tipper', 'mfg' => 'Macau',
	    'liv' => 'Taylor Woodrow', 'cod' => '1', 'rar' => '',
	    'cdt' => 'yellow, chrome exhausts',
	    'tdt' => 'yellow trailer with black base, TAYLOR WOODROW tampo',
	],
// 2. MB8-F cab in pink with chrome base, pink trailer with black base, "Readymix" tampo, Macau casting (AU)
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB147', 'tlr' => 'Tipper', 'mfg' => 'Macau',
	    'liv' => 'Readymix', 'cod' => '1', 'rar' => '',
	    'cdt' => 'pink with chrome base',
	    'tdt' => 'pink trailer with black base, READYMIX tampo',
	],
// 3. MB45-C cab in yellow, chrome exhausts, yellow trailer with black base, "Eurobran" tampo, Macau casting (S6-8)
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB045', 'tlr' => 'Tipper', 'mfg' => 'Macau',
	    'liv' => 'Eurobran', 'cod' => '1', 'rar' => '',
	    'cdt' => 'yellow, chrome exhausts',
	    'tdt' => 'yellow trailer with black base, EUROBRAN tampo',
	],
// 4. MB45-C cab in yellow, chrome exhausts, yellow trailer with black base, black & white road design tampo, Macau casting 
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB045', 'tlr' => 'Tipper', 'mfg' => 'Macau',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
	    'cdt' => 'yellow, chrome exhausts',
	    'tdt' => 'yellow trailer with black base, black and white road design tampo',
	],
// 5. MB45-C cab in green, chrome exhausts, yellow trailer with black base, "Eurobran" tampo, Macau casting (S6-8)
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'MB045', 'tlr' => 'Tipper', 'mfg' => 'Macau',
	    'liv' => 'Eurobran', 'cod' => '1', 'rar' => '',
	    'cdt' => 'green, chrome exhausts',
	    'tdt' => 'yellow trailer with black base, EUROBRAN tampo',
	],
// 6. MB45-C cab in green, gray exhausts, yellow trailer with black base, "Eurobran" tampo, Macau casting (MC)
	['mod' => $subtitle, 'var' => '06a',
	    'cab' => 'MB045', 'tlr' => 'Tipper', 'mfg' => 'Macau',
	    'liv' => 'Eurobran', 'cod' => '1', 'rar' => '',
	    'crd' => 'Charles Linsenbarth',
	    'cdt' => 'green, gray exhausts',
	    'tdt' => 'yellow trailer with black base, EUROBRAN tampo',
	],
// 7. MB45-C cab in yellow, gray exhausts, yellow trailer with black base, "Taylor Woodrow" tampo, Macau casting 
	['mod' => $subtitle, 'var' => '07a',
	    'cab' => 'MB045', 'tlr' => 'Tipper', 'mfg' => 'Macau',
	    'liv' => 'Taylor Woodrow', 'cod' => '1', 'rar' => '',
	    'crd' => 'Simon Rogers',
	    'cdt' => 'yellow, gray exhausts',
	    'tdt' => 'yellow trailer with black base, TAYLOR WOODROW tampo',
	],
// 8. MB8-F cab in pink with black base, pink trailer with black base, "Readymix" tampo, Macau casting (AU)
	['mod' => $subtitle, 'var' => '08a',
	    'cab' => 'MB147', 'tlr' => 'Tipper', 'mfg' => 'Macau',
	    'liv' => 'Readymix', 'cod' => '1', 'rar' => '',
	    'cdt' => 'pink with black base',
	    'tdt' => 'pink trailer with black base, READYMIX" tampo',
	],
// 9. MB45-C cab in green, gray exhausts, yellow trailer with black base, "Eurobran" tampo, Thailand casting 
	['mod' => $subtitle, 'var' => '09a',
	    'cab' => 'MB045', 'tlr' => 'Tipper', 'mfg' => 'Thailand',
	    'liv' => 'Eurobran', 'cod' => '1', 'rar' => '',
	    'cdt' => 'green, gray exhausts',
	    'tdt' => 'yellow trailer with black base, EUROBRAN tampo',
	],
// 10. MB45-C cab in red, gray exhausts, yellow trailer with black base, red design tampo, Thailand casting (CS)
	['mod' => $subtitle, 'var' => '10a',
	    'cab' => 'MB045', 'tlr' => 'Tipper', 'mfg' => 'Thailand',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
	    'cdt' => 'red, gray exhausts',
	    'tdt' => 'yellow trailer with black base, red design tampo',
	],
    ]);
}
?>
