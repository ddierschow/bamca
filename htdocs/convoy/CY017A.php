<?php // DONE
$subtitle = 'CY017A';
// CY-17-A SCANIA PETROL TANKER, issued 1985
$desc = "Scania Tanker";
$year = '1985';
include "cypage.php";

function body() {
    global $subtitle;

    show_table([
// 1. White cab, blue chassis with chrome base, white tank with blue base, "Amoco" tampo, Macau casting 
	['mod' => $subtitle, 'var' => '01a',
	    'cab' => 'MB147', 'tlr' => 'Tanker', 'mfg' => 'Macau',
	    'liv' => 'Amoco', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, blue chassis, chrome base',
            'tdt' => 'white tank with blue base, AMOCO tampo',
	],
// 2. Red cab and chassis with chrome base, red tank with red base, "Tizer" tampo, Macau (UK)
	['mod' => $subtitle, 'var' => '02a',
	    'cab' => 'MB147', 'tlr' => 'Tanker', 'mfg' => 'Macau',
	    'liv' => 'Tizer', 'cod' => '1', 'rar' => '',
            'cdt' => 'red, red chassis, chrome base',
            'tdt' => 'red tank with red base, TIZER tampo',
	],
// 3. White cab, green chassis with chrome base, white tank with green base, "Diet 7 Up" tampo, Macau (UK)
	['mod' => $subtitle, 'var' => '03a',
	    'cab' => 'MB147', 'tlr' => 'Tanker', 'mfg' => 'Macau',
	    'liv' => 'Diet 7-Up', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, green chassis, chrome base',
            'tdt' => 'white tank with green base, DIET 7 UP tampo',
	],
// 4. Orange cab and chassis with chrome base, orange tank with white base, "Cadbury's Fudge" tampo, Macau (UK)
	['mod' => $subtitle, 'var' => '04a',
	    'cab' => 'MB147', 'tlr' => 'Tanker', 'mfg' => 'Macau',
	    'liv' => 'Cadbury', 'cod' => '1', 'rar' => '',
            'cdt' => 'orange, orange chassis, chrome base',
            'tdt' => "orange tank with white base, CADBURY'S FUDGE tampo",
	],
// 5. White cab, dark gray chassis with chrome base, chrome tank with dark gray base, "Shell" tampo, Macau
	['mod' => $subtitle, 'var' => '05a',
	    'cab' => 'MB147', 'tlr' => 'Tanker', 'mfg' => 'Macau',
	    'liv' => 'Shell', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, dark gray chassis, chrome base',
            'tdt' => 'chrome tank with dark gray base, SHELL tampo',
	],
// 6. White cab, dark gray chassis with black base, chrome tank with dark gray base, "Shell" tampo, Macau
	['mod' => $subtitle, 'var' => '06a',
	    'cab' => 'MB147', 'tlr' => 'Tanker', 'mfg' => 'Macau',
	    'liv' => 'Shell', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, dark gray chassis, black base',
            'tdt' => 'chrome tank with dark gray base, SHELL tampo',
	],
// 7. White cab, dark gray chassis with black base, chrome tank with dark gray base, "Shell" tampo, Thailand
	['mod' => $subtitle, 'var' => '07a',
	    'cab' => 'MB147', 'tlr' => 'Tanker', 'mfg' => 'Thailand',
	    'liv' => 'Shell', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, dark gray chassis, black base',
            'tdt' => 'chrome tank with dark gray base, SHELL tampo',
	],
// 8. White cab, dark gray chassis with black base, white tank with dark gray base, "Feoso" tampo, Thailand (CHI)
	['mod' => $subtitle, 'var' => '08a',
	    'cab' => 'MB147', 'tlr' => 'Tanker', 'mfg' => 'Thailand',
	    'liv' => 'Feoso', 'cod' => '1', 'rar' => '',
            'cdt' => 'white, dark gray chassis, black base',
            'tdt' => 'white tank, dark gray base, FEOSO tampo',
	],

	['mod' => $subtitle, 'var' => 'P01',
	    'cab' => 'MB147', 'tlr' => 'Tanker', 'mfg' => 'Thailand',
	    'liv' => 'none', 'cod' => '1', 'rar' => '',
            'cdt' => '',
            'tdt' => '',
	    'nts' => 'preproduction',
	],
    ]);
}
?>
