<?php // DONE
$subtitle = 'CY025A';
// CY-25-A DAF CONTAINER TRUCK, issued 1989
$desc = "DAF Container Truck";
$year = '1989';

$defaults = ['mod' => $subtitle, 'cab' => 'MB183', 'tlr' => 'CYT04', 'cod' => '1'];

$models = [
// 1. Yellow cab and chassis, yellow container with yellow base, "IPEC" tampo, Macau (AU issued as CY-9)
    ['var' => '01a', 'mfg' => 'Macau', 'liv' => 'IPEC',
	'cdt' => 'yellow, yellow chassis', 'cva' => '01',
	'tdt' => 'yellow container with yellow base, IPEC tampo',
	'nts' => 'Also produced as CY009A Var 12a',
    ],
// 2. Blue cab and chassis, blue container with blue base, "Crooke's Healthcare" tampo, Macau (UK)
    ['var' => '02a', 'mfg' => 'Macau', 'liv' => "Crooke's Healthcare",
	'cdt' => 'blue, blue chassis', 'cva' => '04',
	'tdt' => "blue container with blue base, CROOKE'S HEALTHCARE tampo",
    ],
// 3. White and orange cab, black chassis, white container with black base, "Unigate" tampo, Macau (UK)
    ['var' => '03a', 'mfg' => 'Macau', 'liv' => 'Unigate',
	'cdt' => 'white and orange, black chassis', 'cva' => '11',
	'tdt' => 'white container with black base, UNIGATE tampo',
    ],
// 4. Red cab, black chassis, red container with black base, "Royal Mail Parcels" tampo, Macau (UK)
    ['var' => '04a', 'mfg' => 'Macau', 'liv' => 'Royal Mail Parcels',
	'cdt' => 'red, black chassis', 'cva' => '10',
	'tdt' => 'red container with black base, ROYAL MAIL PARCELS tampo',
    ],
// 5. Blue cab and chassis, blue container with blue base, "Comma Performance Oil" tampo, Macau (UK)
    ['var' => '05a', 'mfg' => 'Macau', 'liv' => 'Comma Performance Oil',
	'cdt' => 'blue, blue chassis', 'cva' => '15',
	'tdt' => 'blue container with blue base, COMMA PERFORMANCE OIL tampo',
    ],
// 6. White cab, bright blue chassis, white container with bright blue base, "Leisure World" tampo, Macau (UK)
    ['var' => '06a', 'mfg' => 'Macau', 'liv' => 'Leisure World',
	'cdt' => 'white, bright blue chassis', 'cva' => '13',
	'tdt' => 'white container with bright blue base, LEISURE WORLD tampo',
    ],
// 7. White cab, blue chassis, white container with black chassis, "Pepsi Team Suzuki" tampo, Macau 
    ['var' => '07a', 'mfg' => 'Macau', 'liv' => 'Pepsi Team Suzuki',
	'cdt' => 'white, blue chassis', 'cva' => '16',
	'tdt' => 'white container with black chassis, PEPSI TEAM SUZUKI tampo',
    ],
// 8. White and orange cab, orange chassis, white container with orange base, "TNT IPEC" tampo, Macau (TC)
    ['var' => '08a', 'mfg' => 'Macau', 'liv' => 'TNT IPEC',
	'cdt' => 'white and orange, orange chassis', 'cva' => '07',
	'tdt' => 'white container with orange base, TNT IPEC tampo',
    ],
// 9. White cab, blue chassis, white container with blue base, "Pioneer" labels, Macau (UK)
    ['var' => '09a', 'mfg' => 'Macau', 'liv' => 'Pioneer',
	'cdt' => 'white, blue chassis', 'cva' => '19',
	'tdt' => 'white container with blue base, PIONEER labels',
    ],
// 10. Metallic gold cab and chassis, black container with black base, "Duracell" tampo (UK)
    ['var' => '10a', 'mfg' => 'Macau', 'liv' => 'Duracell',
	'cdt' => 'metallic gold cab and chassis', 'cva' => '18',
	'tdt' => 'black container with black base, DURACELL tampo',
    ],
// 11. Yellow container, black chassis, yellow container with black base, "Zweifel Pomy Chips" tampo
    ['var' => '11a', 'mfg' => 'Macau', 'liv' => 'Zweifel Pomy Chips',
	'cdt' => 'yellow, black chassis', 'cva' => '21',
	'tdt' => 'yellow container with black base, ZWEIFEL POMY CHIPS tampo',
    ],
// 12. Green cab and chassis, white container with black base, "M" and orange stripe tampo, Macau (SW)
    ['var' => '12a', 'mfg' => 'Macau', 'liv' => 'M',
	'cdt' => 'green, green chassis', 'cva' => '20',
	'tdt' => 'white container with black base, M and orange stripe tampo',
    ],
// 13. White cab, red chassis, white container with red base, "Toblerone" tampo, Macau 
    ['var' => '13a', 'mfg' => 'Macau', 'liv' => 'Toblerone',
	'cdt' => 'white, red chassis', 'cva' => '25',
	'tdt' => 'white container with red base, TOBLERONE tampo',
    ],
// 14. White cab, black chassis, white container with black base, "Pirelli Gripping Stuff" tampo, Macau (TC)
    ['var' => '14a', 'mfg' => 'Macau', 'liv' => 'Pirelli Gripping Stuff',
	'cdt' => 'white, black chassis', 'cva' => '23',
	'tdt' => 'white container with black base, PIRELLI GRIPPING STUFF tampo',
    ],
// 15. White cab, black chassis, white container with black base, "XP" tampo, Macau (TC)
    ['var' => '15a', 'mfg' => 'Macau', 'liv' => 'XP',
	'cdt' => 'white, black chassis', 'cva' => '22',
	'tdt' => 'white container with black base, XP tampo',
    ],
// 16. White cab, red chassis, white container with red base, "Toblerone" tampo, Thailand 
    ['var' => '16a', 'mfg' => 'Thailand', 'liv' => 'Toblerone',
	'cdt' => 'white, red chassis', 'cva' => '35',
	'tdt' => 'white container with red base, TOBLERONE tampo',
    ],
// 17. White cab, yellow chassis, white container with yellow base, "HB Racing" tampo, Thailand (AS)
    ['var' => '17a', 'mfg' => 'Thailand', 'liv' => 'HB Racing',
	'cdt' => 'white, yellow chassis', 'cva' => '36',
	'tdt' => 'white container with yellow base, HB RACING tampo',
    ],
// 18. White cab, green chassis, white container with green base, "Garden Festival Wales" tampo, Thailand (WL)(GS)
    ['var' => '18a', 'mfg' => 'Thailand', 'liv' => 'Garden Festival Wales',
	'cdt' => 'white, green chassis', 'cva' => '39',
	'tdt' => 'white container with green base, GARDEN FESTIVAL WALES tampo',
	'nts' => 'Part of Special Gift Set',
    ],
// 19. Brown cab, black chassis, light gray container with black chassis, "United Parcel Service" tampo, Thailand (UK)
    ['var' => '19a', 'mfg' => 'Thailand', 'liv' => 'United Parcel Service',
	'cdt' => 'brown, black chassis', 'cva' => '40',
	'tdt' => 'light gray container with black chassis, UNITED PARCEL SERVICE tampo',
    ],
// 20. Blue cab, black chassis, red container with white chassis, "World Cup" labels, China 
// NOTE: Version 20 with either "Matchbox International" or "Mattel Inc." cast cab. All versions below with "Mattel" only.
    ['var' => '20a', 'mfg' => 'China', 'liv' => 'World Cup',
	'cdt' => 'blue, black chassis', 'cva' => '50',
	'tdt' => 'red container with white chassis, WORLD CUP labels',
    ],
// 21. White cab, blue chassis, blue container and chassis, "Kellogg's" and cartoon characters labels, China (ROW)
    ['var' => '21a', 'mfg' => 'China, MATTEL', 'liv' => "Kellogg's",
	'cdt' => 'white, blue chassis', 'cva' => '54',
	'tdt' => "blue container and chassis, KELLOGG'S and cartoon characters labels",
    ],
// 22. Red cab, black chassis, white container and chassis, "McDonald's" labels, China (ROW)
    ['var' => '22a', 'mfg' => 'China, MATTEL', 'liv' => "McDonald's",
	'cdt' => 'red, black chassis', 'cva' => '55',
	'tdt' => "white container and chassis, MCDONALD'S labels",
    ],
// 23. Red cab, black chassis, white container and base, "Melde" labels, China (C2)
    ['var' => '23a', 'mfg' => 'China, MATTEL', 'liv' => 'Melde', 'cod' => '2', 'rar' => '4',
	'cdt' => 'red, black chassis', 'cva' => '10',
	'tdt' => 'white container and base, MELDE labels',
    ],
// 24. Red cab, black chassis, red container and base, "At Home, Too! Coca Cola" labels, China and "Mattel", antennas cast, chrome disc with rubber tires (PC)
    ['var' => '24a', 'cab' => 'MB340', 'mfg' => 'China, MATTEL', 'liv' => 'Coca-Cola',
	'cdt' => 'red, black chassis', 'cva' => '',
	'tdt' => 'red container and base, AT HOME, TOO! COCA COLA labels',
    ],

    ['var' => '25a', 'mfg' => 'China', 'liv' => 'Coca-Cola',
	'cdt' => 'red, black chassis, painted windows', 'cva' => '',
	'tdt' => 'black container, ENJOY THE REAL THING',
    ],
    ['var' => '26a', 'cab' => 'MB340', 'mfg' => 'China', 'liv' => 'Coca-Cola',
	'cdt' => 'white, red chassis', 'cva' => '',
	'tdt' => 'COCA COLA CALENDAR GIRLS JAN/FED',
    ],
    ['var' => '27a', 'cab' => 'MB340', 'mfg' => 'China', 'liv' => 'Coca-Cola',
	'cdt' => 'white, gray chassis', 'cva' => '',
	'tdt' => 'COCA COLA CALENDAR GIRLS JULY/AUGUST',
    ],
    ['var' => 'C3a', 'mfg' => 'Macau', 'liv' => 'Royal Mail', 'cod' => '3',
	'cdt' => 'red, black chassis', 'cva' => '',
	'tdt' => 'red container, ROYAL MAIL PARCEL FORCE',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
