<?php // DONE
$subtitle = 'CY017A';
// CY-17-A SCANIA PETROL TANKER, issued 1985
$desc = "Scania Tanker";
$year = '1985';

$defaults = ['mod' => $subtitle, 'cab' => 'MB147', 'tlr' => 'CYT06', 'cod' => '1'];

include "cypage.php";

function body() {
    show_table([
// 1. White cab, blue chassis with chrome base, white tank with blue base, "Amoco" tampo, Macau casting 
	['var' => '01a', 'mfg' => 'Macau', 'liv' => 'Amoco',
            'cdt' => 'white, blue chassis, chrome base',
            'tdt' => 'white tank with blue base, AMOCO tampo',
	],
// 2. Red cab and chassis with chrome base, red tank with red base, "Tizer" tampo, Macau (UK)
	['var' => '02a', 'mfg' => 'Macau', 'liv' => 'Tizer',
            'cdt' => 'red, red chassis, chrome base',
            'tdt' => 'red tank with red base, TIZER tampo',
	],
// 3. White cab, green chassis with chrome base, white tank with green base, "Diet 7 Up" tampo, Macau (UK)
	['var' => '03a', 'mfg' => 'Macau', 'liv' => 'Diet 7-Up',
            'cdt' => 'white, green chassis, chrome base',
            'tdt' => 'white tank with green base, DIET 7 UP tampo',
	],
// 4. Orange cab and chassis with chrome base, orange tank with white base, "Cadbury's Fudge" tampo, Macau (UK)
	['var' => '04a', 'mfg' => 'Macau', 'liv' => 'Cadbury',
            'cdt' => 'orange, orange chassis, chrome base',
            'tdt' => "orange tank with white base, CADBURY'S FUDGE tampo",
	],
// 5. White cab, dark gray chassis with chrome base, chrome tank with dark gray base, "Shell" tampo, Macau
	['var' => '05a', 'mfg' => 'Macau', 'liv' => 'Shell',
            'cdt' => 'white, dark gray chassis, chrome base',
            'tdt' => 'chrome tank with dark gray base, SHELL tampo',
	],
// 6. White cab, dark gray chassis with black base, chrome tank with dark gray base, "Shell" tampo, Macau
	['var' => '06a', 'mfg' => 'Macau', 'liv' => 'Shell',
            'cdt' => 'white, dark gray chassis, black base',
            'tdt' => 'chrome tank with dark gray base, SHELL tampo',
	],
// 7. White cab, dark gray chassis with black base, chrome tank with dark gray base, "Shell" tampo, Thailand
	['var' => '07a', 'mfg' => 'Thailand', 'liv' => 'Shell',
            'cdt' => 'white, dark gray chassis, black base',
            'tdt' => 'chrome tank with dark gray base, SHELL tampo',
	],
// 8. White cab, dark gray chassis with black base, white tank with dark gray base, "Feoso" tampo, Thailand (CHI)
	['var' => '08a', 'mfg' => 'Thailand', 'liv' => 'Feoso',
            'cdt' => 'white, dark gray chassis, black base',
            'tdt' => 'white tank, dark gray base, FEOSO tampo',
	    'add' => [['Other side', '<img src="/pic/set/convoy/m_cy017a-08a2.jpg">']],
	],

	['var' => 'P01', 'mfg' => 'Thailand', 'liv' => 'none', 'cdt' => 'PP',
            'tdt' => '',
	    'nts' => 'preproduction',
	],
    ]);
}
?>
