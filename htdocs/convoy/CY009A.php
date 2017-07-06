<?php // DONE
$subtitle = 'CY009A';
// CY-9-A KENWORTH BOX TRUCK, issued 1982
// NOTE: All models with amber windows, 8-spoke wheels, no antennas, and chrome exhausts unless otherwise noted.
$desc = "Kenworth Conventional Box Trailer";
$year = '1982';

$defaults = ['mod' => $subtitle,
	    'cab' => 'MB103', 'tlr' => 'CYT04', 'mfg' => 'England', 'cod' => '1',
];

$models = [
// 1. MB103 cab in black, black container, "Midnight X-Press" labels, England
    ['var' => '01a', 'mfg' => 'England', 'liv' => 'Midnight X-Press',
	'cdt' => 'black', 'cva' => '003',
	'tdt' => "black container, MIDNIGHT X-PRESS labels",
    ],
// 2. MB103 cab in black, clear windows, black container, "Midnight X-Press" labels, England
    ['var' => '02a', 'mfg' => 'England', 'liv' => 'Midnight X-Press',
	'cdt' => 'black, clear windows', 'cva' => '004',
	'tdt' => "black container, MIDNIGHT X-PRESS labels",
    ],
    ['var' => '02b', 'mfg' => 'England', 'liv' => 'Midnight X-Press',
	'cdt' => 'black, clear windows', 'cva' => '004',
	'tdt' => "black container, MIDNIGHT X-PRESS labels (reversed)",
    ],
// 3. MB045 cab in black, amber windows, black container, "Midnight X-Press" tampo, England
    ['var' => '03a', 'cab' => 'MB045', 'mfg' => 'England', 'liv' => 'Midnight X-Press',
	'cdt' => 'black, amber windows', 'cva' => '012',
	'tdt' => "black container, MIDNIGHT X-PRESS tampo",
    ],
// 4. MB103 cab in black, black container, "Midnight X-Press" tampo, Macau
    ['var' => '04a', 'mfg' => 'Macau', 'liv' => 'Midnight X-Press',
	'cdt' => 'black', 'cva' => '004',
	'tdt' => "black container, MIDNIGHT X-PRESS tampo",
    ],
// 5. MB103 cab in black, black container, "Moving In New Directions" tampo, Macau (AU)
    ['var' => '05a', 'mfg' => 'Macau', 'liv' => '', 'rar' => '4',
	'cdt' => 'black', 'cva' => '026AA',
	'tdt' => "black container, MOVING IN NEW DIRECTIONS tampo",
    ],
// 6. MB103 cab in black, black container, "Moving In New Directions" tampo with "Personal Contact Is Barry Oxford" roof label, Macau (AU)
    ['var' => '06a', 'mfg' => 'Macau', 'liv' => '', 'rar' => '5',
	'cdt' => 'black', 'cva' => '026AA',
	'tdt' => "black container, MOVING IN NEW DIRECTIONS tampo with PERSONAL CONTACT IS BARRY OXFORD roof label",
    ],
// 7. MB103 cab in black, black container, "Moving In New Directions" tampo with "Personal Contact Is Anita Jones" roof label, Macau (AU)
    ['var' => '07a', 'mfg' => 'Macau', 'liv' => '', 'rar' => '5',
	'cdt' => 'black', 'cva' => '026AA',
	'tdt' => "black container, MOVING IN NEW DIRECTIONS tampo with PERSONAL CONTACT IS ANITA JONES roof label",
    ],
// 8. MB103 cab in black, black container, "Moving In New Directions" tampo with "Personal Contact Is Keith Mottram" roof label, Macau (AU)
    ['var' => '08a', 'mfg' => 'Macau', 'liv' => '', 'rar' => '5',
	'cdt' => 'black', 'cva' => '026AA',
	'tdt' => "black container, MOVING IN NEW DIRECTIONS tampo with PERSONAL CONTACT IS KEITH MOTTRAM roof label",
    ],
// 9. MB103 cab in black, black container, "Moving In New Directions" tampo with "Personal Contact Is Terry Blyton" roof label (AU)
    ['var' => '09a', 'mfg' => 'Macau', 'liv' => '', 'rar' => '5',
	'cdt' => 'black', 'cva' => '026AA',
	'tdt' => "black container, MOVING IN NEW DIRECTIONS tampo with PERSONAL CONTACT IS TERRY BLYTON roof label",
    ],
// 10. MB103 cab in black, black container, "Moving In New Directions" tampo with "Personal Contact Is Jenny Brindley" roof label (AU)
    ['var' => '10a', 'mfg' => 'Macau', 'liv' => '', 'rar' => '5',
	'cdt' => 'black', 'cva' => '026AA',
	'tdt' => "black container, MOVING IN NEW DIRECTIONS tampo with PERSONAL CONTACT IS JENNY BRINDLEY roof label",
    ],
// 11. MB103 cab in black, yellow container, "Stanley" tampo, Macau (US)(OP)
    ['var' => '11a', 'mfg' => 'Macau', 'liv' => 'Stanley',
	'cdt' => 'black', 'cva' => '025A',
	'tdt' => "yellow container, STANLEY tampo",
    ],
// 12. DAF cab in yellow, yellow container, "IPEC" tampo, Macau (AU)
    ['var' => '12a', 'cab' => 'MB183', 'mfg' => 'Macau', 'liv' => 'IPEC',
	'cdt' => 'yellow', 'cva' => '01',
	'tdt' => "yellow container, IPEC tampo",
    ],
// 13. MB103 cab in white, white container, "Paul Arpin Van Lines" tampo, Macau (US)
    ['var' => '13a', 'mfg' => 'Macau', 'liv' => 'Paul Arpin',
	'cdt' => 'white', 'cva' => '027A',
	'tdt' => "white container, PAUL ARPIN VAN LINES tampo",
    ],
// 14. MB103 cab in white, white container, "Matchbox/ Compliments Macau Diecast Co. Ltd.," Macau
    ['var' => '14a', 'mfg' => 'Macau', 'liv' => 'Matchbox', 'rar' => '5',
	'cdt' => 'white', 'cva' => '028A',
	'tdt' => "white container, MATCHBOX/ COMPLIMENTS MACAU DIECAST CO. LTD., Macau",
    ],
// 15. MB103 cab in white, white container, "Matchbox-ln Celebration of Universal Group's 20th Anniversary" tampo, Macau
    ['var' => '15a', 'mfg' => 'Macau', 'liv' => 'Matchbox', 'rar' => '5',
	'cdt' => 'white', 'cva' => '028A',
	'tdt' => "white container, MATCHBOX-LN CELEBRATION OF UNIVERSAL GROUP'S 20TH ANNIVERSARY tampo",
    ],
// 16. MB103 cab in white, white container, "Canadian Tire" tampo, Macau (CN)
    ['var' => '16a', 'mfg' => 'Macau', 'liv' => 'Canadian Tire',
	'cdt' => 'white', 'cva' => '032A',
	'tdt' => "white container, CANADIAN TIRE tampo",
    ],
// 17. MB103 cab in white, white container, "Merry Christmas 1988 MICA Members" with calendar roof label (C2)
    ['var' => '17a', 'mfg' => 'Macau', 'liv' => 'MICA', 'cod' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => "white container, MERRY CHRISTMAS 1988 MICA MEMBERS with calendar roof label",
    ],
// 18. MB103 cab in blue, blue container, "Mitre 10" tampo, Macau (AU)
    ['var' => '18a', 'mfg' => 'Macau', 'liv' => 'Mitre 10',
	'cdt' => 'blue', 'cva' => '034A',
	'tdt' => "blue container, MITRE 10 tampo",
    ],
// 19. MB103 cab in blue, white container, "Spaulding" tampo, Macau (US)
    ['var' => '19a', 'mfg' => 'Macau', 'liv' => 'Spaulding',
	'cdt' => 'blue', 'cva' => '042A',
	'tdt' => "white container, SPAULDING tampo",
    ],
// 20. MB103 cab in white, white container, "Merry Christmas MICA Members 1990" labels with calendar roof label (C2)
    ['var' => '20a', 'mfg' => 'Macau', 'liv' => 'MICA', 'cod' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => "white container, MERRY CHRISTMAS MICA MEMBERS 1990 labels with calendar roof label",
    ],
// 21. MB103 cab in black, black container, "Midnight X-Press" tampo, Thailand
    ['var' => '21a', 'mfg' => 'Thailand', 'liv' => 'Midnight X-Press',
	'cdt' => 'black', 'cva' => '050A',
	'tdt' => "black container, MIDNIGHT X-PRESS tampo, Thailand",
    ],
// 22. MB103 cab in black, black container, "Cool Paint Co." labels, Thailand
    ['var' => '22a', 'mfg' => 'Thailand', 'liv' => 'Cool Paint',
	'cdt' => 'black', 'cva' => '083',
	'tdt' => "black container, COOL PAINT CO. labels, Thailand",
    ],
// 23. MB103 cab in black, black container, Thailand, "Cool Paint Co." labels applied over "Midnight X-Press"
    ['var' => '23a', 'mfg' => 'Thailand', 'liv' => 'Cool Paint',
	'cdt' => 'black', 'cva' => '083',
	'tdt' => "black container, Thailand, COOL PAINT CO. labels applied over MIDNIGHT X-PRESS",
    ],
// 24. MB103 cab in white, white container, Thailand, "Truckin' USA" labels
    ['var' => '24a', 'mfg' => 'Thailand', 'liv' => "Truckin' USA",
	'cdt' => 'white', 'cva' => '101',
	'tdt' => "white container, Thailand, TRUCKIN' USA labels",
    ],
// 25. MB103 cab in white, white container, Thailand, "Hershey's" labels
    ['var' => '25a', 'mfg' => 'Thailand', 'liv' => "Hershey's",
	'cdt' => 'white', 'cva' => '126',
	'tdt' => "white container, Thailand, HERSHEY'S labels",
    ],
// 26. MB103 cab in white, white container, Thailand, "Paul Arpin Van Lines" with "NFL" logo
    ['var' => '26a', 'mfg' => 'Thailand', 'liv' => 'Paul Arpin',
	'cdt' => 'white', 'cva' => '118A',
	'tdt' => "white container, Thailand, PAUL ARPIN VAN LINES with NFL logo",
    ],
// 27. MB103 cab in white, white container and base, Thailand, "Hershey's" (with small candy bar) labels
    ['var' => '27a', 'mfg' => 'Thailand', 'liv' => "Hershey's",
	'cdt' => 'white', 'cva' => '126',
	'tdt' => "white container and base, Thailand, HERSHEY'S (with small candy bar) labels",
    ],
// 28. MB103 cab in orange, orange container and base, Thailand, "Reese's" labels
    ['var' => '28a', 'mfg' => 'Thailand', 'liv' => "Reese's",
	'cdt' => 'orange', 'cva' => '129',
	'tdt' => "orange container and base, Thailand, REESE'S labels",
    ],
// 29. MB103 cab in red, red container and base, Thailand, "Skittles" labels
    ['var' => '29a', 'mfg' => 'Thailand', 'liv' => 'Skittles',
	'cdt' => 'red', 'cva' => '128',
	'tdt' => "red container and base, Thailand, SKITTLES labels",
    ],
// 30. MB103 cab in silver/gray, orange container, silver/gray base, Thailand, "Skittles" labels
    ['var' => '30a', 'mfg' => 'Thailand', 'liv' => 'Skittles',
	'cdt' => 'silver-gray', 'cva' => '130',
	'tdt' => "orange container, silver-gray base, Thailand, SKITTLES labels",
    ],
// 31. MB103 cab in white, red container, white base, Thailand, "Skittles" labels
    ['var' => '31a', 'mfg' => 'Thailand', 'liv' => 'Skittles',
	'cdt' => 'white', 'cva' => '131',
	'tdt' => "red container, white base, Thailand, SKITTLES labels",
    ],
// 32. MB103 cab in yellow, yellow container and base, Thailand, "M and M's" labels
    ['var' => '32a', 'mfg' => 'Thailand', 'liv' => "M&amp;M's",
	'cdt' => 'yellow', 'cva' => '132',
	'tdt' => "yellow container and base, Thailand, M&amp;M'S labels",
    ],
// 33. MB103 cab in black, black container and base, Thailand, "Roller Blade" labels
    ['var' => '33a', 'mfg' => 'Thailand', 'liv' => 'Roller Blade',
	'cdt' => 'black', 'cva' => '133',
	'tdt' => "black container and base, Thailand, ROLLER BLADE labels",
    ],
// 34. MB103 cab in black, black container and base, China, "Roller Blade" labels
    ['var' => '34a', 'mfg' => 'China', 'liv' => 'Roller Blade',
	'cdt' => 'black', 'cva' => '133',
	'tdt' => "black container and base, ROLLER BLADE labels",
    ],
// 35. MB103 cab in yellow, yellow container and base, China, "M and M's" labels
    ['var' => '35a', 'mfg' => 'China', 'liv' => "M&amp;M's",
	'cdt' => 'yellow', 'cva' => '136',
	'tdt' => "yellow container and base, M&amp;M'S labels",
    ],
// 36. MB103 cab in bright blue, red container and base, China, "Kellogg's Froot Loops" labels
    ['var' => '36a', 'mfg' => 'China', 'liv' => "Kellog's",
	'cdt' => 'bright blue', 'cva' => '141',
	'tdt' => "red container and base, KELLOGG'S FROOT LOOPS labels",
    ],
// 37. MB103 cab in lemon, lemon container, black base, China, "Stop. Go. Pennzoil" tampo, rubber tires, antennas cast (PC)
    ['var' => '37a', 'cab' => 'MB310', 'mfg' => 'China', 'liv' => 'Pennzoil',
	'cdt' => 'lemon', 'cva' => '',
	'tdt' => "lemon container, black base, STOP. GO. PENNZOIL tampo",
    ],
// 38. MB103 cab in red, red container, black base, China, "Coca-Cola" with sideways bottle tampo, rubber tires, antennas cast (PC)
    ['var' => '38a', 'cab' => 'MB310', 'mfg' => 'China', 'liv' => 'Coca-Cola',
	'cdt' => 'red', 'cva' => '',
	'tdt' => "red container, black base, COCA-COLA with sideways bottle tampo",
    ],
// 39. MB103 cab in blue, red container and base, China, "Kellogg's Froot Loops!" labels
    ['var' => '39a', 'mfg' => 'China', 'liv' => "Kellog's",
	'cdt' => 'blue', 'cva' => '141',
	'tdt' => "red container and base, KELLOGG'S FROOT LOOPS! labels",
    ],
// 40. MB103 cab in white, green container, yellow base, China and "Mattel", "Kellogg's Corn Flakes" labels (ROW)
    ['var' => '40a', 'mfg' => 'China, MATTEL', 'liv' => "Kellog's", 'rar' => '4',
	'cdt' => 'white', 'cva' => '',
	'tdt' => "green container, yellow base, KELLOGG'S CORN FLAKES labels",
    ],
// 41. MB103 cab in black, black container and base, China, "18th Annual Matchbox USA Convention and Toy Show" labels (C2)
    ['var' => '41a', 'mfg' => 'China', 'liv' => 'Matchbox USA', 'cod' => '2',
	'cdt' => 'black', 'cva' => '',
	'tdt' => "black container and base, 18TH ANNUAL MATCHBOX USA CONVENTION AND TOY SHOW labels",
    ],
];
// NOTE: Versions 36 and 39 with either "Matchbox International" or "Mattel Inc." cab casting.

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
