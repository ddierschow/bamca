<?php // DONE
$subtitle = 'CY008A';
// CY-8-A KENWORTH BOX TRUCK, issued 1982
$desc = "Kenworth COE Box Trailer";
$year = '1982';

$defaults = ['mod' => $subtitle, 'cab' => 'MB045', 'tlr' => 'Box',
	    'mfg' => 'England', 'cod' => '1',
];
include "cypage.php";

function body() {
    show_table([
// 1. MB45-C cab in white with red & yellow tampo, red container with white roof & doors, "Matchbox" labels, England
	['var' => '01a', 'mfg' => 'England', 'liv' => 'Matchbox',
            'cdt' => 'white with red and yellow tampo',
            'tdt' => 'red container with white roof and doors, MATCHBOX labels',
	],
// 2. MB45-C cab in white with red and yellow tampo, red container with white roof and doors, "Redcap" labels, England
	['var' => '02a', 'mfg' => 'England', 'liv' => 'Redcap',
            'cdt' => 'white with red and yellow tampo',
            'tdt' => 'red container with white roof and doors, REDCAP labels',
	],
// 3. MB45-C cab in white with brown and blue tampo, red container with white roof and doors, "Redcap" labels, England
	['var' => '03a', 'mfg' => 'England', 'liv' => 'Redcap',
            'cdt' => 'white with brown and blue tampo',
            'tdt' => 'red container with white roof and doors, REDCAP labels',
	],
// 4. MB41-D cab in red with black and white tampo, red container with white roof and doors, "Redcap" labels, England
	['var' => '04a', 'cab' => 'MB103', 'mfg' => 'England', 'liv' => 'Redcap',
            'cdt' => 'red with black and white tampo',
            'tdt' => 'red container with white roof and doors, REDCAP labels',
	],
// 5. MB41-D cab in red with black and white tampo, red container with white roof and black doors, "Redcap" labels, England
	['var' => '05a', 'cab' => 'MB103', 'mfg' => 'England', 'liv' => 'Redcap',
            'cdt' => 'red with black and white tampo',
            'tdt' => 'red container with white roof and black doors, REDCAP labels',
	],
// 6. MB41-D cab in red with black and white tampo, red container with black roof and doors, "Redcap" labels, England
	['var' => '06a', 'cab' => 'MB103', 'mfg' => 'England', 'liv' => 'Redcap',
            'cdt' => 'red with black and white tampo',
            'tdt' => 'red container with black roof and doors, REDCAP labels',
	],
// 7. MB41-D cab in red with black and white tampo, red container with black roof and white doors, "Redcap" labels, England
	['var' => '07a', 'cab' => 'MB103', 'mfg' => 'England', 'liv' => 'Redcap',
            'cdt' => 'red with black and white tampo',
            'tdt' => 'red container with black roof and white doors, REDCAP labels',
	],
// 8. MB45-C cab in white with brown and blue tampo, red container with white roof and doors, "Ski Fruit Yogurt" labels, England (AU)(C2)
	['var' => '08a', 'mfg' => 'England', 'liv' => 'Ski Fruit Yogurt', 'cod' => '2',
            'cdt' => 'white with brown and blue tampo',
            'tdt' => 'red container with white roof and doors, SKI FRUIT YOGURT labels',
	    'nts' => 'Australian release',
	],
// 9. MB45-C cab in white with orange and yellow tampo, red container with white roof and doors, "Ski Fruit Yogurt" labels, England (AU)(C2)
	['var' => '09a', 'mfg' => 'England', 'liv' => 'Ski Fruit Yogurt', 'cod' => '2',
            'cdt' => 'white with orange and yellow tampo',
            'tdt' => 'red container with white roof and doors, SKI FRUIT YOGURT labels',
	    'nts' => 'Australian release',
	],
// 10. MB45-C cab in white with orange and yellow tampo, red container with white roof and doors, "Redcap" labels, England
	['var' => '10a', 'mfg' => 'England', 'liv' => 'Redcap',
            'cdt' => 'white with orange and yellow tampo',
            'tdt' => 'red container with white roof and doors, REDCAP labels',
	],
// 11. MB45-C cab in silver-gray/blue with yellow and red tampo, silver-gray container with blue roof and doors, "Matchbox Showliner" labels, Macau (UK)
	['var' => '11a', 'mfg' => 'Macau', 'liv' => 'Matchbox',
            'cdt' => 'silver-gray/blue with yellow and red tampo',
            'tdt' => 'silver-gray container with blue roof and doors, "MATCHBOX SHOWLINER labels',
	],
	['var' => '11b', 'mfg' => 'Macau', 'liv' => 'Matchbox',
            'cdt' => 'white with yellow and red tampo',
            'tdt' => 'silver-gray container with blue roof and doors, "MATCHBOX SHOWLINER labels',
	],
// 12. MB45-C cab in white with red band tampo, white container with white roof and doors, "K-Line" tampo, Macau (US)
	['var' => '12a', 'mfg' => 'Macau', 'liv' => 'K-Line',
            'cdt' => 'white with red band tampo',
            'tdt' => 'white container with white roof and doors, K-LINE tampo',
	],
// 13. MB45-C cab in white with yellow/red/blue tampo, white container with white roof and doors, "Matchbox" tampo, Macau
	['var' => '13a', 'mfg' => 'Macau', 'liv' => 'Matchbox',
            'cdt' => 'white with yellow/red/blue tampo',
            'tdt' => 'white container with white roof and doors, MATCHBOX tampo',
	],
// 14. MB45-C cab in white with yellow/red/blue tampo, white container with white roof and doors, "Matchbox" tampo with "This Truck Delivers 1988" roof label, Macau (UK)
	['var' => '14a', 'mfg' => 'Macau', 'liv' => 'Matchbox',
            'cdt' => 'white with yellow/red/blue tampo',
            'tdt' => 'white container with white roof and doors, MATCHBOX tampo with THIS TRUCK DELIVERS 1988 roof label',
	    'nts' => 'Sales sample',
	],
// 15. MB45-C cab in white with yellow/red/blue tampo, white container with white roof and doors, "Matchbox" tampo with "This Truck Delivers 1989" roof label, Macau (HK)
	['var' => '15a', 'mfg' => 'Macau', 'liv' => 'Matchbox',
            'cdt' => 'white with yellow/red/blue tampo',
            'tdt' => 'white container with white roof and doors, MATCHBOX tampo with THIS TRUCK DELIVERS 1989 roof label',
	    'nts' => 'Sales sample',
	],
// 16. MB45-C cab in white with red band tampo, red container with red roof and doors, "K-Line" tampo, Macau (US)
	['var' => '16a', 'mfg' => 'Macau', 'liv' => 'K-Line',
            'cdt' => 'white with red band tampo',
            'tdt' => 'red container with red roof and doors, K-LINE tampo',
	],
// 17. MB45-C cab in black with "Harley-Davidson" tampo, black container with black roof and doors, "Harley-Davidson" labels, Macau (HD)
	['var' => '17a', 'mfg' => 'Macau', 'liv' => 'Harey-Davidson',
            'cdt' => 'black with HARLEY-DAVIDSON tampo',
            'tdt' => 'black container with black roof and doors, HARLEY-DAVIDSON labels',
	],
// 18. MB45-C cab in red with white band tampo, red container with red roof and doors, Thailand, "Nintendo" tampo
	['var' => '18a', 'mfg' => 'Thailand', 'liv' => 'Nintendo',
            'cdt' => 'red with white band tampo',
            'tdt' => 'red container with red roof and doors, NINTENDO tampo',
	],
// NOTE: Above model was originally a preproduction in 1990, but with Macau.
	['var' => '18p', 'mfg' => 'Macau', 'liv' => 'Nintendo', 'cod' => 'PP',
            'cdt' => 'red with white band tampo',
            'tdt' => 'red container with red roof and doors, NINTENDO tampo',
	],
// 19. MB45-C cab in white with "KFC" tampo, white container, roof and doors, Thailand, "KFC" labels
	['var' => '19a', 'mfg' => 'Thailand', 'liv' => 'KFC',
            'cdt' => 'white with KFC tampo',
            'tdt' => 'white container, roof and doors, Thailand, KFC labels',
	],
	['var' => '19b', 'mfg' => 'Thailand', 'liv' => 'KFC',
            'cdt' => 'red with KFC tampo',
            'tdt' => 'white container, roof and doors, Thailand, KFC labels',
	],
// 20. MB45-C cab in red with "Pizza Hut" tampo, white container, roof and doors, Thailand, "Pizza Hut" labels
	['var' => '20a', 'mfg' => 'Thailand', 'liv' => 'Pizza Hut',
            'cdt' => 'red with PIZZA HUT tampo',
            'tdt' => 'white container, roof and doors, Thailand, PIZZA HUT labels',
	],
// 21. MB45-C cab in white with "Matchbox" tampo, white container with white roof and doors, Thailand, "Matchbox/Universal Group" tampo (HK)
	['var' => '21a', 'mfg' => 'Thailand', 'liv' => 'Matchbox', 'rar' => '5',
            'cdt' => 'white with MATCHBOX tampo',
            'tdt' => 'white container with white roof and doors, MATCHBOX/UNIVERSAL GROUP tampo',
	    'add' => [['Other side', '<img src="/pic/set/convoy/m_cy008a_21a2.jpg">']],
	],
// 22. MB45-C cab in white with "K" tampo, red container, roof and doors with black base, Thailand, "K-Line" tampo (US)
	['var' => '22a', 'mfg' => 'Thailand', 'liv' => 'K-Line',
            'cdt' => 'white with K tampo',
            'tdt' => 'red container, roof and doors with black base, K-LINE tampo',
	],
// 23. MB45-C cab in black with "Pizza Hut" tampo, white container, roof and doors with black base, Thailand, "Pizza Hut" labels
	['var' => '23a', 'mfg' => 'Thailand', 'liv' => 'Pizza Hut',
            'cdt' => 'black with PIZZA HUT tampo',
            'tdt' => 'white container, roof and doors with black base, Thailand, PIZZA HUT labels',
	],
// 24. MB45-C cab in black with "Pizza Hut" tampo, white container, roof and doors with black base, China, "Pizza Hut" labels
	['var' => '24a', 'mfg' => 'China', 'liv' => 'Pizza Hut',
            'cdt' => 'black with PIZZA HUT tampo',
            'tdt' => 'white container, roof and doors with black base, Thailand, PIZZA HUT labels',
	],
// 25. MB45-C cab in blue with "Matchbox" tampo, blue container, roof, doors, and base, China, "Matchbox Action System" labels
	['var' => '25a', 'mfg' => 'China', 'liv' => 'Matchbox',
            'cdt' => 'blue with "Matchbox" tampo',
            'tdt' => 'blue container, roof, doors, and base, MATCHBOX ACTION SYSTEM labels',
	],
// 26. MB45-C cab in white with "B and L" tampo, white container, roof, doors and base, China, "Baldwin and Lyons Inc." labels (US)
	['var' => '26a', 'mfg' => 'China', 'liv' => 'Baldwin and Lyons', 'cod' => '2',
            'cdt' => 'white with "B and L" tampo',
            'tdt' => 'white container, roof, doors and base, BALDWIN AND LYONS INC. labels',
	],
// 27. MB45-C cab in yellow with "Nintendo" tampo, yellow container, roof, doors and base, China, "Super Mario 64-Nintendo" labels
	['var' => '27a', 'mfg' => 'China', 'liv' => 'Nintendo',
            'cdt' => 'yellow with NINTENDO tampo',
            'tdt' => 'yellow container, roof, doors and base, SUPER MARIO 64-NINTENDO" labels',
	],
// 28. MB45-C cab in white with no tampo, white container, roof, doors and base, China, no labels (ASAP blank)
	['var' => '28a', 'mfg' => 'China', 'liv' => 'none',
            'cdt' => 'white with no tampo',
            'tdt' => 'white container, roof, doors and base, no labels',
	    'nts' => 'ASAP blank',
	],
// 29. MB45-C cab in black with no tampo, white container, roof, doors and base, China, no labels (ASAP blank)
	['var' => '29a', 'mfg' => 'China', 'liv' => 'none',
            'cdt' => 'black with no tampo',
            'tdt' => 'white container, roof, doors and base, no labels',
	    'nts' => 'ASAP blank',
	],
// NOTE: Versions 30 B 31 with "Matchbox International" or "Mattel" bases.
// 30. MB45-C cab in white with "CAT" tampo, white container, roof, doors and base, China, "CAT" labels
	['var' => '30a', 'mfg' => 'China', 'liv' => 'Caterpillar',
            'cdt' => 'white with CAT tampo',
            'tdt' => 'white container, roof, doors and base, CAT labels',
	],
// 31. MB45-C cab in dark red with "Lifesavers" tampo, blue container, roof and doors, white base, China, "Lifesavers Five Flavor" labels
	['var' => '31a', 'mfg' => 'China', 'liv' => 'Lifesavers',
            'cdt' => 'dark red with LIFESAVERS tampo',
            'tdt' => 'blue container, roof and doors, white base, LIFESAVERS FIVE FLAVOR labels',
	],
// 32. MB45-C cab in red with "Ralphs" tampo, white container, roof, doors and base, China , "Ralphs" labels (HH)
	['var' => '32a', 'mfg' => 'China', 'liv' => 'Ralphs',
            'cdt' => 'red with RALPHS tampo',
            'tdt' => 'white container, roof, doors and base, RALPHS labels',
	],
// 33. MB45-C cab in blue with "Kellogg's" tampo, white roof, container, doors and base, China and "Mattel", "Kellogg's Frosted Flakes" tampo
	['var' => '33a', 'mfg' => 'China', 'liv' => "Kellogg's",
            'cdt' => "blue with KELLOGG'S tampo",
            'tdt' => "white roof, container, doors and base, China and MATTEL, KELLOGG'S FROSTED FLAKES tampo",
	],
// 34. MB45-C cab in white with none tampo, white roof, container, doors and base, China and "Mattel", "Zobau" labels (C2)
	['var' => '34a', 'mfg' => 'China', 'liv' => 'Zobau', 'cod' => '2',
            'cdt' => 'white',
            'tdt' => 'white roof, container, doors and base, China and MATTEL, ZOBAU labels',
	],
// NOTE: Below model is mounted to a wooden plinth base by two screws.
// 35. MB45-C cab in white with none tampo, white roof, container, doors and base, China, "Transamerica Leasing NA International" tampo (ASAP)
	['var' => '35a', 'mfg' => 'China', 'liv' => 'Transamerica', 'cod' => '2',
            'cdt' => 'white',
            'tdt' => 'white roof, container, doors and base, TRANSAMERICA LEASING NA INTERNATIONAL tampo',
	    'nts' => 'mounted to a wooden plinth base by two screws; ASAP',
	],
// 36. MB45-C cab in white with none tampo, white roof, container, doors and base, China, "The Pepsi Bottling Company" (white background) labels (ASAP)
	['var' => '36a', 'mfg' => 'China', 'liv' => 'Pepsi', 'cod' => '2',
            'cdt' => 'white',
            'tdt' => 'white roof, container, doors and base, THE PEPSI BOTTLING COMPANY (white background) labels',
	    'nts' => 'ASAP',
	],
// 37. MB45-C cab in white with none tampo, white roof, container, doors and base, China, "Acco" labels  (ASAP)
	['var' => '37a', 'mfg' => 'China', 'liv' => 'Acco', 'cod' => '2',
            'cdt' => 'white',
            'tdt' => 'white roof, container, doors and base, ACCO labels',
	    'nts' => 'ASAP',
	],
// 38. MB45-C cab in white with none tampo, white roof, container, doors and base, China, "Nestle Carnation Coffee-Mate" labels (ASAP)
	['var' => '38a', 'mfg' => 'China', 'liv' => 'Nestle', 'cod' => '2',
            'cdt' => 'white',
            'tdt' => 'white roof, container, doors and base, NESTLE CARNATION COFFEE-MATE labels',
	    'nts' => 'ASAP',
	],
// 39. MB45-C cab in white with none tampo, white roof, container, doors and base, China, "Celebrating 20 Years 1980-2000 PGT" labels (ASAP)
	['var' => '39a', 'mfg' => 'China', 'liv' => 'PGT', 'cod' => '2',
            'cdt' => 'white',
            'tdt' => 'white roof, container, doors and base, CELEBRATING 20 YEARS 1980-2000 PGT labels',
	    'nts' => 'ASAP',
	],

	['var' => 'D01a', 'mfg' => 'China', 'liv' => 'Burger King',
            'cdt' => 'red, BURGER KING',
            'tdt' => 'white roof, container, doors and base, CELEBRATING 20 YEARS 1980-2000 PGT labels',
	],
	['var' => 'D02a', 'mfg' => 'China', 'liv' => 'Polinas', 'cod' => '2',
            'cdt' => 'black, P',
            'tdt' => 'black roof, container, doors and base, POLINAS labels',
	],
	['var' => 'D03a', 'mfg' => 'China', 'liv' => 'Human Rights Campaign', 'cod' => '2',
            'cdt' => 'white',
            'tdt' => "white roof, container, doors and base, GEORGE W. BUSH YOU'RE FIRED labels",
	],
	['var' => 'D04a', 'mfg' => 'China', 'liv' => "Guida's", 'cod' => '2',
            'cdt' => 'white',
            'tdt' => "white roof, container, doors and base, GUIDA'S labels",
	],
    ]);
}
?>
