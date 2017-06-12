<?php // DONE
$subtitle = 'TP022A';
// TP22-A DOUBLE CONTAINER TRUCK, issued 1979
$desc = "Peterbilt Double Container Truck";
$year = '1979';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Bronze cab, beige containers, amber windows, "OCL" labels
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'T9CC', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'OCL', 'cod' => '1', 'rar' => '',
            'cdt' => 'bronze cab, amber windows',
            'tdt' => 'beige containers, OCL labels',
	],
// 2. Bronze cab, cream containers, amber windows, "OCL" labels
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'T9CC', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'OCL', 'cod' => '1', 'rar' => '',
            'cdt' => 'bronze cab, amber windows',
            'tdt' => 'cream containers, OCL labels',
	],
// 3. Bronze cab, milky white containers, amber windows, "OCL" labels
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'T9CC', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'OCL', 'cod' => '1', 'rar' => '',
            'cdt' => 'bronze cab, amber windows',
            'tdt' => 'milky white containers, OCL labels',
	],
// 4. Bronze cab, beige containers, no windows, "OCL" labels
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'T9CC', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'OCL', 'cod' => '1', 'rar' => '',
            'cdt' => 'Bronze cab, no windows',
            'tdt' => 'beige containers, OCL labels',
	],
// 5. Red cab, beige containers, amber windows, "OCL" labels
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'T9CC', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'OCL', 'cod' => '1', 'rar' => '',
            'cdt' => 'red cab, amber windows',
            'tdt' => 'beige containers, OCL labels',
	],
// 6. Red cab, light yellow containers, amber windows, "OCL" labels
	['mod' => $subtitle, 'var' => '06a',
	    'cab' => 'T9CC', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'OCL', 'cod' => '1', 'rar' => '',
            'cdt' => 'red cab, amber windows',
            'tdt' => 'light yellow containers, OCL labels',
	],
// 7. Red cab, milky white containers, amber windows, "OCL" labels
	['mod' => $subtitle, 'var' => '07a',
	    'cab' => 'T9CC', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'OCL', 'cod' => '1', 'rar' => '',
            'cdt' => 'red cab, amber windows',
            'tdt' => 'milky white containers, OCL labels',
	],
// 8. Red cab, light blue containers, amber windows, "Sealand" labels
	['mod' => $subtitle, 'var' => '08a',
	    'cab' => 'T9CC', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'Sealand', 'cod' => '1', 'rar' => '',
            'cdt' => 'red cab, amber windows',
            'tdt' => 'light blue containers, SEALAND labels',
	],
// 9. Red cab, red containers, amber windows, "IMYK" labels
	['mod' => $subtitle, 'var' => '09a',
	    'cab' => 'T9CC', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'IMYK', 'cod' => '1', 'rar' => '',
            'cdt' => 'red cab, amber windows',
            'tdt' => 'red containers, IMYK labels',
	],
// 10. Dark green cab, beige containers, amber windows, "OCL" labels
	['mod' => $subtitle, 'var' => '10a',
	    'cab' => 'T9CC', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'OCL', 'cod' => '1', 'rar' => '',
            'cdt' => 'dark green cab, amber windows',
            'tdt' => 'beige containers, OCL labels',
	],
// 11. Dark green cab, orange containers, amber windows, "OCL" labels
	['mod' => $subtitle, 'var' => '11a',
	    'cab' => 'T9CC', 'tlr' => 'Double Container', 'mfg' => 'England',
	    'liv' => 'OCL', 'cod' => '1', 'rar' => '',
            'cdt' => 'dark green cab, amber windows',
            'tdt' => 'orange containers, OCL labels',
	],
    ]);
}
?>
