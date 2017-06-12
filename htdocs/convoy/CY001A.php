<?php // DONE
$subtitle = 'CY001A';
// CY-1-A KENWORTH CAR TRANSPORTER, issued 1982
$desc = "Kenworth COE Auto Transporters";
$year = '1982';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. Red cab with white/yellow/blue stripes, chrome exhc-?~^ red trailer with beige ramp & white stripes, England casting 
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB045', 'tlr' => 'Car Transporter', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'red with white/yellow/blue stripes tampo, chrome exhausts',
            'tdt' => 'red with beige ramp, white stripes tampo',
	],
// 2. Red cab with black/blue/white stripes, chrome exha^s:-red trailer with beige ramp & white stripes, England casting 
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB045', 'tlr' => 'Car Transporter', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'red with black/blue/white stripes tampo, chrome exhausts',
            'tdt' => 'red with beige ramp, white stripes tampo',
	],
// 3. Red cab with black/blue/white stripes, chrome exha^s:; red trailer with beige ramp & white stripes, England casting 
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB045', 'tlr' => 'Car Transporter', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'red with black/blue/white stripes tampo, chrome exhausts',
            'tdt' => 'red with beige ramp, white stripes tampo',
	],
// 4. Red cab with black/blue/white stripes & "4" roof label, chrome exhausts, red trailer with beige ramp & no stripes, England casting 
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB045', 'tlr' => 'Car Transporter', 'mfg' => 'England',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'red with black/blue/white stripes tampo and 4 roof label, chrome exhausts',
            'tdt' => 'red with beige ramp',
	],
// 5. Red cab with white/yellow/black stripes, chrome exhausts, red trailer with beige ramp & no stripes, Macau casting 
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'MB045', 'tlr' => 'Car Transporter', 'mfg' => 'Macau',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'red with white/yellow/black stripes tampo, chrome exhausts',
            'tdt' => 'red with beige ramp',
	],
// 6. Red cab with white/yellow/black stripes, chrome exhausts, red trailer with beige ramp with stripes Macau casting 
	['mod' => $subtitle, 'var' => '06a',
	    'cab' => 'MB045', 'tlr' => 'Car Transporter', 'mfg' => 'Macau',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'red with white/yellow/black stripes tampo, chrome exhausts',
            'tdt' => 'red with beige ramp, stripes tampo',
	],
// 7. Yellow cab with blue & purple tempa, chrome exhaust, dark blue trailer with yellow ramp, Macau casting 
	['mod' => $subtitle, 'var' => '07a',
	    'cab' => 'MB045', 'tlr' => 'Car Transporter', 'mfg' => 'Macau',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'yellow with blue &amp; purple tampo, chrome exhausts',
            'tdt' => 'dark blue with yellow ramp',
	],
// 8. Yellow cab with blue & purple tempa, gray exhausts, dark blue trailer with yellow ramp, Macau casting 
	['mod' => $subtitle, 'var' => '08a',
	    'cab' => 'MB045', 'tlr' => 'Car Transporter', 'mfg' => 'Macau',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'yellow with blue &amp; purple tampo, gray exhausts',
            'tdt' => 'dark blue with yellow ramp',
	],
// 9. Yellow cab with blue & purple tempa, gray exhausts, dark blue trailer with yellow ramp, Thailand casting 
	['mod' => $subtitle, 'var' => '09a',
	    'cab' => 'MB045', 'tlr' => 'Car Transporter', 'mfg' => 'Thailand',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'yellow with blue &amp; purple tampo, gray exhausts',
            'tdt' => 'dark blue with yellow ramp',
	],
// 10. Blue cab with yellow & orange tempa, chrome exhausts, blue trailer with yellow ramp, Thailand casting 
	['mod' => $subtitle, 'var' => '10a',
	    'cab' => 'MB045', 'tlr' => 'Car Transporter', 'mfg' => 'Thailand',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'blue with yellow &amp; orange tampo, chrome exhausts',
            'tdt' => 'blue with yellow ramp',
	],
// 11. Blue cab with yellow & orange tempa, chrome exhausts, blue trailer with yellow ramp, China casting 
	['mod' => $subtitle, 'var' => '11a',
	    'cab' => 'MB045', 'tlr' => 'Car Transporter', 'mfg' => 'China',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => 'blue with yellow &amp; orange tampo, chrome exhausts',
            'tdt' => 'blue with yellow ramp',
	],
    ]);
}
?>
