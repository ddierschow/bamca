<?php // DONE
$subtitle = 'CY013A';
// CY-13-A PETERBILT FIRE ENGINE, issued 1984
$desc = "Articulated Fire Ladder";
$year = '1984';

$defaults = ['mod' => $subtitle,
	    'cab' => 'MI724', 'tlr' => 'CYT13', 'mfg' => 'England',
	    'liv' => 'Fire Dept.', 'cod' => '1',
];

include "cypage.php";

function body() {
    show_table([
// 1. MB106 cab in red, red trailer with white lettered "8" and "Fire Dept." tampo, white ladder, England
	['var' => '01a', 'cab' => 'MB106', 'mfg' => 'England', 'liv' => 'Fire Dept.',
            'cdt' => 'red',
            'tdt' => 'red with white lettered 8 and FIRE DEPT. tampo, white ladder',
	],
// 2. MB045 cab in red with "Denver" label, red trailer with white lettered "8" and "Fire Dept." tampo, white ladder, England
	['var' => '02a', 'cab' => 'MB045', 'mfg' => 'England', 'liv' => 'Fire Dept.',
            'cdt' => 'red, DENVER label',
            'tdt' => 'red with white lettered 8 and FIRE DEPT. tampo, white ladder',
	],
// 3. MI724 in red, red trailer with white lettered "8" and "Fire Dept." tampo, white ladder, Macau
	['var' => '03a', 'mfg' => 'Macau', 'liv' => 'Fire Dept.',
            'cdt' => 'red',
            'tdt' => 'red with white lettered 8 and FIRE DEPT. tampo, white ladder',
	],
// 4. MI724 in red, red trailer with yellow lettered "8" and "Fire Dept." tampo, white ladder, Macau
	['var' => '04a', 'mfg' => 'Macau', 'liv' => 'Fire Dept.',
            'cdt' => 'red',
            'tdt' => 'red with yellow lettered 8 and FIRE DEPT. tampo, white ladder',
	],
// 5. MI724 in red, red trailer with white lettered "8" and yellow lettered "Fire Dept." tampo, white ladder, Macau
	['var' => '05a', 'mfg' => 'Macau', 'liv' => 'Fire Dept.',
            'cdt' => 'red',
            'tdt' => 'red with white lettered 8 and yellow lettered FIRE DEPT. tampo, white ladder',
	],
// 6. MI724 in red, red trailer with white lettered "8" and "Fire Dept." tampo, white ladder, Thailanc
	['var' => '06a', 'mfg' => 'Thailand', 'liv' => 'Fire Dept.',
            'cdt' => 'red',
            'tdt' => 'red with white lettered 8 and FIRE DEPT. tampo, white ladder',
	],
// 7. MI724 in florescent orange, florescent orange trailer with "City Fire Dept. 15" and checkers temoa white ladder, Thailand (EM)
	['var' => '07a', 'mfg' => 'Thailand', 'liv' => 'Fire Dept.',
            'cdt' => 'florescent orange',
            'tdt' => 'florescent orange with CITY FIRE DEPT. 15 and checkers tampo, white ladder',
	],
// 8. MI724 in red, red trailer with white lettered "8" and "Fire Dept." tampo, white ladder, China
	['var' => '08a', 'mfg' => 'China', 'liv' => 'Fire Dept.',
            'cdt' => 'red',
            'tdt' => 'red with white lettered 8 and FIRE DEPT. tampo, white ladder',
	],
// 9. MI724 in red, red trailer with white lettered "6" and white design tampo, dark gray ladder, China (ROW)
	['var' => '09a', 'mfg' => 'China', 'liv' => 'Fire Dept.',
            'cdt' => 'red',
            'tdt' => 'red with white lettered 8 and FIRE DEPT. tampo, dark gray ladder',
	],
    ]);
}
?>
