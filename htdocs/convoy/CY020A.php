<?php // DONE
$subtitle = 'CY020A';
// CY-20-A ARTICULATED DUMP TRUCK, issued 1987
$desc = "Kenworth &amp; Scania Tipper";
$year = '1987';

$defaults = ['mod' => $subtitle, 'cab' => 'MB045', 'tlr' => 'Tipper', 'cod' => '1'];

include "cypage.php";

function body() {
    show_table([
// 1. MB45-C cab in yellow, chrome exhausts, yellow trailer with black base, "Taylor Woodrow" tampo, Macau casting 
	['var' => '01a', 'mfg' => 'Macau', 'liv' => 'Taylor Woodrow',
	    'cdt' => 'yellow, chrome exhausts',
	    'tdt' => 'yellow trailer with black base, TAYLOR WOODROW tampo',
	],
// 2. MB8-F cab in pink with chrome base, pink trailer with black base, "Readymix" tampo, Macau casting (AU)
	['var' => '02a', 'cab' => 'MB147', 'mfg' => 'Macau', 'liv' => 'Readymix',
	    'cdt' => 'pink with chrome base',
	    'tdt' => 'pink trailer with black base, READYMIX tampo',
	],
// 3. MB45-C cab in yellow, chrome exhausts, yellow trailer with black base, "Eurobran" tampo, Macau casting (S6-8)
	['var' => '03a', 'mfg' => 'Macau', 'liv' => 'Eurobran',
	    'cdt' => 'yellow, chrome exhausts',
	    'tdt' => 'yellow trailer with black base, EUROBRAN tampo',
	],
// 4. MB45-C cab in yellow, chrome exhausts, yellow trailer with black base, black & white road design tampo, Macau casting 
	['var' => '04a', 'mfg' => 'Macau', 'liv' => 'none',
	    'cdt' => 'yellow, chrome exhausts',
	    'tdt' => 'yellow trailer with black base, black and white road design tampo',
	],
// 5. MB45-C cab in green, chrome exhausts, yellow trailer with black base, "Eurobran" tampo, Macau casting (S6-8)
	['var' => '05a', 'mfg' => 'Macau', 'liv' => 'Eurobran',
	    'cdt' => 'green, chrome exhausts',
	    'tdt' => 'yellow trailer with black base, EUROBRAN tampo',
	],
// 6. MB45-C cab in green, gray exhausts, yellow trailer with black base, "Eurobran" tampo, Macau casting (MC)
	['var' => '06a', 'mfg' => 'Macau', 'liv' => 'Eurobran',
	    'crd' => 'Charles Linsenbarth',
	    'cdt' => 'green, gray exhausts',
	    'tdt' => 'yellow trailer with black base, EUROBRAN tampo',
	],
// 7. MB45-C cab in yellow, gray exhausts, yellow trailer with black base, "Taylor Woodrow" tampo, Macau casting 
	['var' => '07a', 'mfg' => 'Macau', 'liv' => 'Taylor Woodrow',
	    'crd' => 'Simon Rogers',
	    'cdt' => 'yellow, gray exhausts',
	    'tdt' => 'yellow trailer with black base, TAYLOR WOODROW tampo',
	],
// 8. MB8-F cab in pink with black base, pink trailer with black base, "Readymix" tampo, Macau casting (AU)
	['var' => '08a', 'cab' => 'MB147', 'mfg' => 'Macau', 'liv' => 'Readymix',
	    'cdt' => 'pink with black base',
	    'tdt' => 'pink trailer with black base, READYMIX" tampo',
	],
// 9. MB45-C cab in green, gray exhausts, yellow trailer with black base, "Eurobran" tampo, Thailand casting 
	['var' => '09a', 'mfg' => 'Thailand', 'liv' => 'Eurobran',
	    'cdt' => 'green, gray exhausts',
	    'tdt' => 'yellow trailer with black base, EUROBRAN tampo',
	],
// 10. MB45-C cab in red, gray exhausts, yellow trailer with black base, red design tampo, Thailand casting (CS)
	['var' => '10a', 'mfg' => 'Thailand', 'liv' => 'none',
	    'cdt' => 'red, gray exhausts',
	    'tdt' => 'yellow trailer with black base, red design tampo',
	],
    ]);
}
?>
