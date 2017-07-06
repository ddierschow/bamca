<?php // DONE
$subtitle = 'CY104B';
// CY-104-B SCANIA BOX TRUCK, issued 1997 (AU)
$desc = "Scania Box Truck";
$year = '1997';

$defaults = ['mod' => $subtitle, 'cab' => 'MB147', 'tlr' => 'CYT04', 'cod' => '1'];

// NOTE: All models with black interior, clear windows, black cab, 8 trailer chassis.
$models = [
// 1. Dark blue and white cab, dark blue container, "Carlton Blue Go Blues!" labels (AU)
    ['var' => '01a', 'mfg' => 'China', 'liv' => "Carlton Blue Go Blues!",
	'cdt' => 'dark blue and white', 'cva' => 'F02',
	'tdt' => "dark blue container, CARLTON BLUE GO BLUES! labels",
    ],
// 2. Dark blue and white cab, dark blue container, "Geelong Cats Go Cats!" labels (AU)
    ['var' => '02a', 'mfg' => 'China', 'liv' => "Geelong Cats Go Cats!",
	'cdt' => 'dark blue and white', 'cva' => 'F03',
	'tdt' => "dark blue container, GEELONG CATS GO CATS! labels",
    ],
// 3. Black and white cab, black container, "Collingwood Magpies Go Pies!" labels (AU)
    ['var' => '03a', 'mfg' => 'China', 'liv' => "Collingwood Magpies Go Pies!",
	'cdt' => 'black and white', 'cva' => 'F04',
	'tdt' => "black container, COLLINGWOOD MAGPIES GO PIES! labels",
    ],
// 4. Black and yellow cab, black container, "Richmond Tigers Go Tigers!" labels (AU)
    ['var' => '04a', 'mfg' => 'China', 'liv' => "Richmond Tigers Go Tigers!",
	'cdt' => 'black and yellow', 'cva' => 'F05',
	'tdt' => "black container, RICHMOND TIGERS GO TIGERS! labels",
    ],
// 5. Turquoise and white cab, turquoise container, "Port Power Go Power!" labels (AU)
    ['var' => '05a', 'mfg' => 'China', 'liv' => "Port Power Go Power!",
	'cdt' => 'turquoise and white', 'cva' => 'F06',
	'tdt' => "turquoise container, PORT POWER GO POWER! labels",
    ],
// 6. Red and black cab, red container, "Essendon Bombers Go Bombers!" labels (AU)
    ['var' => '06a', 'mfg' => 'China', 'liv' => "Essendon Bombers Go Bombers!",
	'cdt' => 'red and black', 'cva' => 'F07',
	'tdt' => "red container, ESSENDON BOMBERS GO BOMBERS! labels",
    ],
// 7. Red and white cab, red container, "Sydney Swans Go Swans!" labels (AU)
    ['var' => '07a', 'mfg' => 'China', 'liv' => "Sydney Swans Go Swans!",
	'cdt' => 'red and white', 'cva' => 'F08',
	'tdt' => "red container, SYDNEY SWANS GO SWANS! labels",
    ],
// 8. Dark blue and white cab, dark blue container, "Blues 1998" labels (AU)
    ['var' => '08a', 'mfg' => 'China', 'liv' => "Blues 1998",
	'cdt' => 'dark blue and white', 'cva' => 'F09',
	'tdt' => "dark blue container, BLUES 1998 labels",
    ],
// 9. Dark blue and white cab, dark blue container, "Cats 1998" labels (AU)
    ['var' => '09a', 'mfg' => 'China', 'liv' => "Cats 1998",
	'cdt' => 'dark blue and white', 'cva' => 'F10',
	'tdt' => "dark blue container, CATS 1998 labels",
    ],
// 10. Dark blue and white cab, dark blue container, "Crows 1998" labels (AU)
    ['var' => '10a', 'mfg' => 'China', 'liv' => "Crows 1998",
	'cdt' => 'dark blue and white', 'cva' => 'F11',
	'tdt' => "dark blue container, CROWS 1998 labels",
    ],
// 11. Dark blue and white cab, blue container, "Eagles 1998" labels (AU)
    ['var' => '11a', 'mfg' => 'China', 'liv' => "Eagles 1998",
	'cdt' => 'dark blue and white', 'cva' => 'F12',
	'tdt' => "blue container, EAGLES 1998 labels",
    ],
// 12. Blue and white cab, blue container, "Demons 1998" labels (AU)
    ['var' => '12a', 'mfg' => 'China', 'liv' => "Demons 1998",
	'cdt' => 'blue and white', 'cva' => 'F13',
	'tdt' => "blue container, DEMONS 1998 labels",
    ],
// 13. Blue and white cab, blue container, "Kangaroos 1998" labels (AU)
    ['var' => '13a', 'mfg' => 'China', 'liv' => "Kangaroos 1998",
	'cdt' => 'blue and white', 'cva' => 'F14',
	'tdt' => "blue container, KANGAROOS 1998 labels",
    ],
// 14. Blue and white cab, blue container, "Bulldogs 1998" labels (AU)
    ['var' => '14a', 'mfg' => 'China', 'liv' => "Bulldogs 1998",
	'cdt' => 'blue and white', 'cva' => 'F15',
	'tdt' => "blue container, BULLDOGS 1998 labels",
    ],
// 15. Turquoise and white cab, turquoise container, "Power 1998" labels (AU)
    ['var' => '15a', 'mfg' => 'China', 'liv' => "Power 1998",
	'cdt' => 'turquoise and white', 'cva' => 'F16',
	'tdt' => "turquoise container, POWER 1998 labels",
    ],
// 16. Black and white cab, black container, "Tigers 1998" labels (AU)
    ['var' => '16a', 'mfg' => 'China', 'liv' => "Tigers 1998",
	'cdt' => 'black and white', 'cva' => 'F17',
	'tdt' => "black container, TIGERS 1998 labels",
    ],
// 17. Black and white cab, black container, "Magpies 1998" labels (AU)
    ['var' => '17a', 'mfg' => 'China', 'liv' => "Magpies 1998",
	'cdt' => 'black and white', 'cva' => 'F18',
	'tdt' => "black container, MAGPIES 1998 labels",
    ],
// 18. Brown and white cab, brown container, "Hawks 1998" labels (AU)
    ['var' => '18a', 'mfg' => 'China', 'liv' => "Hawks 1998",
	'cdt' => 'brown and white', 'cva' => 'F19',
	'tdt' => "brown container, HAWKS 1998 labels",
    ],
// 19. Green and white cab, green container, "Fremantle 1998" labels (AU)
    ['var' => '19a', 'mfg' => 'China', 'liv' => "Fremantle 1998",
	'cdt' => 'green and white', 'cva' => 'F20',
	'tdt' => "green container, FREMANTLE 1998 labels",
    ],
// 20. Red and white cab, red container, "Saints 1998" labels (AU)
    ['var' => '20a', 'mfg' => 'China', 'liv' => "Saints 1998",
	'cdt' => 'red and white', 'cva' => 'F21',
	'tdt' => "red container, SAINTS 1998 labels",
    ],
// 21. Red and white cab, red container, "Swans 1998" labels (AU)
    ['var' => '21a', 'mfg' => 'China', 'liv' => "Swans 1998",
	'cdt' => 'red and white', 'cva' => 'F22',
	'tdt' => "red container, SWANS 1998 labels",
    ],
// 22. Red and white cab, red container, "Brisbane 1998" labels (AU)
    ['var' => '22a', 'mfg' => 'China', 'liv' => "Brisbane 1998",
	'cdt' => 'red and white', 'cva' => 'F24',
	'tdt' => "red container, BRISBANE 1998 labels",
    ],
// 23. Red and white cab, red container, "Bombers 1998" labels (AU)
    ['var' => '23a', 'mfg' => 'China', 'liv' => "Bombers 1998",
	'cdt' => 'red and white', 'cva' => 'F23',
	'tdt' => "red container, BOMBERS 1998 labels",
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
