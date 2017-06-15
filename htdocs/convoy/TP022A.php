<?php // DONE
$subtitle = 'TP022A';
// TP22-A DOUBLE CONTAINER TRUCK, issued 1979
$desc = "Peterbilt Double Container Truck";
$year = '1979';

$defaults = ['mod' => $subtitle, 'cab' => 'T9CC', 'tlr' => 'Double Container', 'mfg' => 'England', 'cod' => '1'];

include "cypage.php";

function body() {
    show_table([
// 1. Bronze cab, beige containers, amber windows, "OCL" labels
	['var' => '01a', 'liv' => 'OCL',
            'cdt' => 'bronze, amber windows',
            'tdt' => 'beige containers, OCL labels',
	],
// 2. Bronze cab, cream containers, amber windows, "OCL" labels
	['var' => '02a', 'liv' => 'OCL',
            'cdt' => 'bronze, amber windows',
            'tdt' => 'cream containers, OCL labels',
	],
// 3. Bronze cab, milky white containers, amber windows, "OCL" labels
	['var' => '03a', 'liv' => 'OCL',
            'cdt' => 'bronze, amber windows',
            'tdt' => 'milky white containers, OCL labels',
	],
// 4. Bronze cab, beige containers, no windows, "OCL" labels
	['var' => '04a', 'liv' => 'OCL',
            'cdt' => 'Bronze, no windows',
            'tdt' => 'beige containers, OCL labels',
	],
// 5. Red cab, beige containers, amber windows, "OCL" labels
	['var' => '05a', 'liv' => 'OCL',
            'cdt' => 'red, amber windows',
            'tdt' => 'beige containers, OCL labels',
	],
// 6. Red cab, light yellow containers, amber windows, "OCL" labels
	['var' => '06a', 'liv' => 'OCL',
            'cdt' => 'red, amber windows',
            'tdt' => 'light yellow containers, OCL labels',
	],
// 7. Red cab, milky white containers, amber windows, "OCL" labels
	['var' => '07a', 'liv' => 'OCL',
            'cdt' => 'red, amber windows',
            'tdt' => 'milky white containers, OCL labels',
	],
// 8. Red cab, light blue containers, amber windows, "Sealand" labels
	['var' => '08a', 'liv' => 'Sealand',
            'cdt' => 'red, amber windows',
            'tdt' => 'light blue containers, SEALAND labels',
	],
// 9. Red cab, red containers, amber windows, "IMYK" labels
	['var' => '09a', 'liv' => 'IMYK',
            'cdt' => 'red, amber windows',
            'tdt' => 'red containers, IMYK labels',
	],
// 10. Dark green cab, beige containers, amber windows, "OCL" labels
	['var' => '10a', 'liv' => 'OCL',
            'cdt' => 'dark green, amber windows',
            'tdt' => 'beige containers, OCL labels',
	],
// 11. Dark green cab, orange containers, amber windows, "OCL" labels
	['var' => '11a', 'liv' => 'OCL',
            'cdt' => 'dark green, amber windows',
            'tdt' => 'orange containers, OCL labels',
	],
    ]);
}
?>
