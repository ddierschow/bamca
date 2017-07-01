<?php // DONE
$subtitle = 'CY104A';
// CY-104-A KENWORTH SUPERSTAR TRANSPORTER, issued 1989
$desc = "Kenworth Superstar Transporter";
$year = '1989';

$defaults = ['mod' => $subtitle, 'cab' => 'MB103', 'tlr' => 'CYT18', 'cod' => '2'];

include "cypage.php";

function body() {
    show_table([
// 1. White cab with "STP" logo, white container, black base, "Richard Petty/STP" labels (WR)
	['var' => '01a', 'mfg' => 'Macau', 'liv' => 'STP',
            'cdt' => 'white, STP logo',
            'tdt' => "white container, black base, RICHARD PETTY/STP labels",
	    'nts' => 'Manufactured for White Rose',
	],
// 2. White cab, white container, black base, "Neil Bonnett/Citgo" labels (WR)
	['var' => '02a', 'mfg' => 'Macau', 'liv' => 'Citgo',
            'cdt' => 'white',
            'tdt' => "white container, black base, NEIL BONNETT/CITGO labels",
	    'nts' => 'Manufactured for White Rose',
	],
// 3. White cab, white container, black base, "Hardee's Racing" labels (WR)
	['var' => '03a', 'mfg' => 'Macau', 'liv' => "Hardees",
            'cdt' => 'white',
            'tdt' => "white container, black base, HARDEE'S RACING labels",
	    'nts' => 'Manufactured for White Rose',
	],
// 4. Black cab, black container, silver-gray base, "Good-wrench Racing Team" labels (WR)
	['var' => '04a', 'mfg' => 'Macau', 'liv' => 'Goodwrench',
            'cdt' => 'black',
            'tdt' => "black container, silver-gray base, GOOD-WRENCH RACING TEAM labels",
	    'nts' => 'Manufactured for White Rose',
	],
// 5. White cab, dark blue container, black base, "Goodyear Racing" labels 
	['var' => '05a', 'mfg' => 'Macau', 'liv' => 'Goodyear', 'cod' => '1',
            'cdt' => 'white',
            'tdt' => "dark blue container, black base, GOODYEAR RACING labels",
	],
// 6. Black cab, black container, black base, "Exxon 51" labels (DT)
	['var' => '06a', 'mfg' => 'Macau', 'liv' => 'Exxon', 'cod' => '1',
            'cdt' => 'black',
            'tdt' => "black container, black base, EXXON 51 labels",
            'nts' => 'Days of Thunder',
	],
// 7. Black and green cab, black container, black base, "Mello Yello 51" labels (DT)
	['var' => '07a', 'mfg' => 'Macau', 'liv' => 'Mello Yello', 'cod' => '1',
            'cdt' => 'black and green',
            'tdt' => "black container, black base, MELLO YELLO 51 labels",
            'nts' => 'Days of Thunder',
	],
// 8. Orange cab, orange container, black base, "Hardees 18" labels (DT)
	['var' => '08a', 'mfg' => 'Macau', 'liv' => 'Hardees', 'cod' => '1',
            'cdt' => 'orange',
            'tdt' => "orange container, black base, HARDEES 18 labels",
            'nts' => 'Days of Thunder',
	],
// 9. Pink cab, white container, black base, "Superflo 46" labels (DT)
	['var' => '09a', 'mfg' => 'Macau', 'liv' => 'Superflo', 'cod' => '1',
            'cdt' => 'pink',
            'tdt' => "white container, black base, SUPERFLO 46 labels",
            'nts' => 'Days of Thunder',
	],
// 10. White cab, white container, black base, "City Chevrolet" labels (DT)
	['var' => '10a', 'mfg' => 'Macau', 'liv' => 'City Chevrolet', 'cod' => '1',
            'cdt' => 'white',
            'tdt' => "white container, black base, CITY CHEVROLET labels",
            'nts' => 'Days of Thunder',
	],
// 11. White cab with red and blue tampo, white container, black base, "Richard Petty/STP" labels (WR)
	['var' => '11a', 'mfg' => 'Macau', 'liv' => 'STP',
            'cdt' => 'white, red and blue tampo',
            'tdt' => "white container, black base, RICHARD PETTY/STP labels",
	    'nts' => 'Manufactured for White Rose',
	],
// 12. Black cab, black container, black base, "Goodwrench Racing Team" labels (WR)
	['var' => '12a', 'mfg' => 'Thailand', 'liv' => 'Goodwrench',
            'cdt' => 'black',
            'tdt' => "black container, black base, GOODWRENCH RACING TEAM labels",
	    'nts' => 'Manufactured for White Rose',
	],
// 13. Gold cab without "6" on doors, gold container, black base, "Folgers" labels (WR)
	['var' => '13a', 'mfg' => 'Thailand', 'liv' => 'Folgers',
            'cdt' => 'gold without 6 on doors',
            'tdt' => "gold container, black base, FOLGERS labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 14. White cab, white container, black base, "Trop Artie" with "Dick Trickle" labels (WR)
	['var' => '14a', 'mfg' => 'Thailand', 'liv' => 'Trop Artic',
            'cdt' => 'white',
            'tdt' => "white container, black base, TROP ARTIC with DICK TRICKLE labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 15. White and blue cab, white container, black base, "Valvoline" labels (IN)
	['var' => '15a', 'mfg' => 'Thailand', 'liv' => 'Valvoline', 'cod' => '1',
            'cdt' => 'white and blue',
            'tdt' => "white container, black base, VALVOLINE labels",
        ],
// 16. Yellow cab, yellow container, black base, "Pennzoil 4" labels (IN)
	['var' => '16a', 'mfg' => 'Thailand', 'liv' => 'Pennzoil', 'cod' => '1',
            'cdt' => 'yellow',
            'tdt' => "yellow container, black base, PENNZOIL 4 labels",
        ],
// 17. Gold cab with "6" on doors, gold container, black base, "Folgers" labels (WR)
	['var' => '17a', 'mfg' => 'Thailand', 'liv' => 'Folgers',
            'cdt' => 'gold cab with 6 on doors',
	    'tdt' => "gold container, black base, FOLGERS labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 18. Black cab, black container, black base, "Goodwrench Racing Team" with team car depicted on sides labels (WR)
	['var' => '18a', 'mfg' => 'Thailand', 'liv' => 'Goodwrench',
            'cdt' => 'black',
            'tdt' => "black container, black base, GOODWRENCH RACING TEAM with team car depicted on sides labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 19. Dark blue cab, dark blue container, black base, "94 Sunoco" without "Sterling Marlin" on labels (WR)
	['var' => '19a', 'mfg' => 'Thailand', 'liv' => 'Sunoco',
            'cdt' => 'dark blue',
            'tdt' => "dark blue container, black base, 94 SUNOCO without STERLING MARLIN on labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 20. Dark blue cab, dark blue container, black base, "94 Sunoco" with "Sterling Marlin" on labels (WR)
	['var' => '20a', 'mfg' => 'Thailand', 'liv' => 'Sunoco',
            'cdt' => 'dark blue',
            'tdt' => "dark blue container, black base, 94 SUNOCO with STERLING MARLIN on labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 21. White cab, white container, black base, "Crown Moroso" labels (WR)
	['var' => '21a', 'mfg' => 'Thailand', 'liv' => 'Crown',
            'cdt' => 'white',
            'tdt' => "white container, black base, CROWN MOROSO labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 22. Black cab, black container, black base, "Texaco Havoline/Davey Allison" labels (WR)
	['var' => '22a', 'mfg' => 'Thailand', 'liv' => 'Texaco',
            'cdt' => 'black',
            'tdt' => "black container, black base, TEXACO HAVOLINE/DAVEY ALLISON labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 23. White cab, white container, black base, "Richard Petty" with portrait labels (WR)
	['var' => '23a', 'mfg' => 'Thailand', 'liv' => 'Richard Petty',
            'cdt' => 'white',
            'tdt' => "white container, black base, RICHARD PETTY with portrait labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 24. Dark blue cab, white container, black base, "Penn State 1855-1991" labels (WR)
	['var' => '24a', 'mfg' => 'Thailand', 'liv' => 'Penn State',
            'cdt' => 'dark blue',
            'tdt' => "white container, black base, PENN STATE 1855-1991 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 25. White cab, white container, black base, "Trop Artie" with "Lake Speed" labels (WR)
	['var' => '25a', 'mfg' => 'Thailand', 'liv' => 'Trop Artic',
            'cdt' => 'white',
            'tdt' => "white container, black base, TROP ARTIC with LAKE SPEED labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 26. Blue cab, blue container, black base, "Maxwell House Racing" labels (WR)
	['var' => '26a', 'mfg' => 'Thailand', 'liv' => 'Maxwell House',
            'cdt' => 'blue',
            'tdt' => "blue container, black base, MAXWELL HOUSE RACING labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 27. White cab, white container, black base, "Ken Schraeder 25" labels (WR)
	['var' => '27a', 'mfg' => 'Thailand', 'liv' => 'Ken Schraeder',
            'cdt' => 'white',
            'tdt' => "white container, black base, KEN SCHRAEDER 25 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 28. Orange-yellow cab, orange-yellow container, black base, "Kodak Racing" labels (WR)
	['var' => '28a', 'mfg' => 'Thailand', 'liv' => 'Kodak',
            'cdt' => 'orange-yellow',
            'tdt' => "orange-yellow container, black base, KODAK RACING labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 29. White cab, white container, black base, "Purolator" with red car labels (WR)
	['var' => '29a', 'mfg' => 'Thailand', 'liv' => 'Purolator',
            'cdt' => 'white',
            'tdt' => "white container, black base, PUROLATOR with red car labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 30. White cab, white container, black base, "Purolator" with orange car labels (WR)
	['var' => '30a', 'mfg' => 'Thailand', 'liv' => 'Purolator',
            'cdt' => 'white',
            'tdt' => "white container, black base, PUROLATOR with orange car labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 31. White cab, white container, black base, "Western Auto 17" labels (WR)
	['var' => '31a', 'mfg' => 'Thailand', 'liv' => 'Western Auto',
            'cdt' => 'white',
            'tdt' => "white container, black base, WESTERN AUTO 17 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 32. White cab, white container, black base, "Country Time" labels (WR)
	['var' => '32a', 'mfg' => 'Thailand', 'liv' => 'Country Time',
            'cdt' => 'white',
            'tdt' => "white container, black base, COUNTRY TIME labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 33. Black cab, black container, black base, "MAC Tools" labels (WR)
	['var' => '33a', 'mfg' => 'Thailand', 'liv' => 'MAC Tools',
            'cdt' => 'black',
            'tdt' => "black container, black base, MAC TOOLS labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 34. Black cab, black container, black base, "Mello Yello 42" labels (WR)
	['var' => '34a', 'mfg' => 'Thailand', 'liv' => 'Mello Yello',
            'cdt' => 'black',
            'tdt' => "black container, black base, MELLO YELLO 42 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 35. Black cab, black container, black base, "Alliance" labels (WR)
	['var' => '35a', 'mfg' => 'Thailand', 'liv' => 'Alliance',
            'cdt' => 'black',
            'tdt' => "black container, black base, ALLIANCE labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 36. Yellow cab, yellow container, black base, "Pennzoil 2" labels (IN)
	['var' => '36a', 'mfg' => 'Thailand', 'liv' => 'Pennzoil', 'cod' => '1',
            'cdt' => 'yellow',
            'tdt' => "yellow container, black base, PENNZOIL 2 labels",
        ],
// 37. White cab, white container, black base, "Panasonic" labels (IN)
	['var' => '37a', 'mfg' => 'Thailand', 'liv' => 'Panasonic', 'cod' => '1',
            'cdt' => 'white',
            'tdt' => "white container, black base, PANASONIC labels",
        ],
// 38. White cab, white container, black base, "K-Mart/Havoline" labels
	['var' => '38a', 'mfg' => 'Thailand', 'liv' => 'K-Mart',
            'cdt' => 'white',
            'tdt' => "white container, black base, K-MART/HAVOLINE labels",
        ],
// 39. Yellow cab, yellow container, black base, "Pennzoil" (Waltrip) labels (WR)
	['var' => '39a', 'mfg' => 'Thailand', 'liv' => 'Pennzoil',
            'cdt' => 'yellow',
            'tdt' => "yellow container, black base, PENNZOIL (Waltrip) labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 40. White cab, white container, black base, "STP-Richard Petty Fan Appreciation Tour 1992" labels (WR)
	['var' => '40a', 'mfg' => 'Thailand', 'liv' => 'STP',
            'cdt' => 'white',
            'tdt' => "white container, black base, STP-RICHARD PETTY FAN APPRECIATION TOUR 1992 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 41. White cab, white container, black base, "Baby Ruth Racing" labels 
	['var' => '41a', 'mfg' => 'Thailand', 'liv' => 'Baby Ruth',
            'cdt' => 'white',
            'tdt' => "white container, black base, BABY RUTH RACING labels",
        ],
// 42. Black cab, black container, black base, "Goodwrench Racing Team" with checkered flags labels (WR)
	['var' => '42a', 'mfg' => 'Thailand', 'liv' => 'Goodwrench',
            'cdt' => 'black',
            'tdt' => "black container, black base, GOODWRENCH RACING TEAM with checkered flags labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 43. Metallic blue body, blue container, black base, "Raybestos" labels (WR)
	['var' => '43a', 'mfg' => 'Thailand', 'liv' => 'Raybestos',
            'cdt' => 'metallic blue',
	    'tdt' => "blue container, black base, RAYBESTOS labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 44. Black cab, red container, black base, "Slim Jim Racing Team" labels (WR)
	['var' => '44a', 'mfg' => 'Thailand', 'liv' => 'Slim Jim',
            'cdt' => 'black',
            'tdt' => "red container, black base, SLIM JIM RACING TEAM labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 45. White and green cab, white container, black base, "Quaker State" labels (WR)
	['var' => '45a', 'mfg' => 'Thailand', 'liv' => 'Quaker State',
            'cdt' => 'white and green',
            'tdt' => "white container, black base, QUAKER STATE labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 46. Blue and white cab, blue container, black base, "Evinrude 89" labels (WR)
	['var' => '46a', 'mfg' => 'Thailand', 'liv' => 'Evinrude',
            'cdt' => 'blue and white',
            'tdt' => "blue container, black base, EVINRUDE 89 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 47. White cab, white container, black base, "Jasper Engines 55" labels (WR)
	['var' => '47a', 'mfg' => 'Thailand', 'liv' => 'Jasper Engines',
            'cdt' => 'white',
            'tdt' => "white container, black base, JASPER ENGINES 55 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 48. Black cab, black container, black base, "MAC Tools Racing" (Harry Gant) labels (WR)
	['var' => '48a', 'mfg' => 'Thailand', 'liv' => 'MAC Tools',
            'cdt' => 'black',
            'tdt' => "black container, black base, MAC TOOLS RACING (Harry Gant) labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 49. Black cab, black container, black base, "Martin Birrane-Team Ireland" labels 
	['var' => '49a', 'mfg' => 'Thailand', 'liv' => 'Team Ireland',
            'cdt' => 'black',
            'tdt' => "black container, black base, MARTIN BIRRANE-TEAM IRELAND labels",
        ],
// 50. White cab, white container, black base, "Penn State Nittany Lions-Happy Valley Express" labels (WR)
	['var' => '50a', 'mfg' => 'Thailand', 'liv' => 'Penn State',
            'cdt' => 'white',
            'tdt' => "white container, black base, PENN STATE NITTANY LIONS-HAPPY VALLEY EXPRESS labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 51. Black cab, black container, black base, "Chevrolet Racing" (bowtie) labels (WR)
	['var' => '51a', 'mfg' => 'Thailand', 'liv' => 'Chevrolet',
            'cdt' => 'black',
            'tdt' => "black container, black base, CHEVROLET RACING (bowtie) labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 52. Black cab, black container, black base, "Moly Black Gold 98 Racing" labels (WR)
	['var' => '52a', 'mfg' => 'Thailand', 'liv' => 'Molly Black Gold',
            'cdt' => 'black',
            'tdt' => "black container, black base, MOLY BLACK GOLD 98 RACING labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 53. Blue cab, blue container, black base, "Sunoco Ultra 98" (LaBonte) labels (WR)
	['var' => '53a', 'mfg' => 'Thailand', 'liv' => 'Sunoco',
            'cdt' => 'blue',
            'tdt' => "blue container, black base, SUNOCO ULTRA 98 (LaBonte) labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 54. White cab, white container, black base, "Baby Ruth Racing" (Burton) labels (WR)
	['var' => '54a', 'mfg' => 'Thailand', 'liv' => 'Baby Ruth',
            'cdt' => 'white',
            'tdt' => "white container, black base, BABY RUTH RACING (Burton) labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 55. White cab, white container, black base, "Mackenzie Indy Racing" labels (IN)
	['var' => '55a', 'mfg' => 'Thailand', 'liv' => 'Mackenzie', 'cod' => '1',
            'cdt' => 'white',
            'tdt' => "white container, black base, MACKENZIE INDY RACING labels",
        ],
// 56. White and blue cab, white container, black base, "Valvoline Racing" with "Goodyear" labels (IN)
	['var' => '56a', 'mfg' => 'Thailand', 'liv' => 'Valvoline', 'cod' => '1',
            'cdt' => 'white and blue',
            'tdt' => "white container, black base, VALVOLINE RACING with GOODYEAR labels",
        ],
// 57. Black cab, black container, black base, "Alliance 59" (2nd issue) labels (WR)
	['var' => '57a', 'mfg' => 'Thailand', 'liv' => 'Alliance',
            'cdt' => 'black',
            'tdt' => "black container, black base, ALLIANCE 59 (2nd issue) labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 58. Black cab, black container, black base, "Dirt Devil" labels (WR)
	['var' => '58a', 'mfg' => 'Thailand', 'liv' => 'Dirt Devil',
            'cdt' => 'black',
            'tdt' => "black container, black base, DIRT DEVIL labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 59. Metallic blue cab, blue container, black base, "Dupont Racing Team 24" labels (WR)
	['var' => '59a', 'mfg' => 'Thailand', 'liv' => 'Dupont',
            'cdt' => 'metallic blue',
            'tdt' => "blue container, black base, DUPONT RACING TEAM 24 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 60. Red cab, red container, black base, "Dentyne Racing" labels (WR)
	['var' => '60a', 'mfg' => 'Thailand', 'liv' => 'Dentyne',
            'cdt' => 'red',
            'tdt' => "red container, black base, DENTYNE RACING labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 61. Black cab, black container, black base, "Meineke Racing Team 12" labels (WR)
	['var' => '61a', 'mfg' => 'Thailand', 'liv' => 'Meineke',
            'cdt' => 'black',
            'tdt' => "black container, black base, MEINEKE RACING TEAM 12 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 62. Orange cab, orange container, black base, "Reithoffer's Antique Carousel" labels (WR)(GS)
	['var' => '62a', 'mfg' => 'Thailand', 'liv' => "Reithoffer's", 'cod' => '1',
            'cdt' => 'orange',
            'tdt' => "orange container, black base, REITHOFFER'S ANTIQUE CAROUSEL labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 63. Blue cab, blue container, black base, "Maxwell House" (B. LaBonte) labels 
	['var' => '63a', 'mfg' => 'Thailand', 'liv' => 'Maxwell House',
            'cdt' => 'blue',
            'tdt' => "blue container, black base, MAXWELL HOUSE (B. LaBonte) labels",
        ],
// 64. Black cab, black container, black base, "Mac Tools/Davey Allison" labels (WR)
	['var' => '64a', 'mfg' => 'Thailand', 'liv' => 'MAC Tools',
            'cdt' => 'black',
            'tdt' => "black container, black base, MAC TOOLS/DAVEY ALLISON labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 65. Red cab, red container, black base, "King of Speed-Mac Tools" labels (WR)
	['var' => '65a', 'mfg' => 'Thailand', 'liv' => 'MAC Tools',
            'cdt' => 'red',
            'tdt' => "red container, black base, KING OF SPEED-MAC TOOLS labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 66. Red cab, white container, black base, "Indiana University-Go Big Red" labels (WR)
	['var' => '66a', 'mfg' => 'Thailand', 'liv' => 'Indiana University',
            'cdt' => 'red',
            'tdt' => "white container, black base, INDIANA UNIVERSITY-GO BIG RED labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 67. White cab, blue container, black base, "Raybestos 8" labels (WR)
	['var' => '67a', 'mfg' => 'Thailand', 'liv' => 'Raybestos',
            'cdt' => 'white',
            'tdt' => "blue container, black base, RAYBESTOS 8 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 68. Orange-red cab, black container, black base, "Staff America Racing" labels (WR)
	['var' => '68a', 'mfg' => 'Thailand', 'liv' => 'Staff America',
            'cdt' => 'orange-red',
            'tdt' => "black container, black base, STAFF AMERICA RACING labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 69. Black cab, black container, black base, "Bojangles Racing Team" labels (WR)
	['var' => '69a', 'mfg' => 'Thailand', 'liv' => 'Bojangles',
            'cdt' => 'black',
            'tdt' => "black container, black base, BOJANGLES RACING TEAM labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 70. Gold and blue cab, dark blue container, black base, "Penn State 1993" labels (WR)
	['var' => '70a', 'mfg' => 'Thailand', 'liv' => 'Penn State',
            'cdt' => 'gold and blue',
            'tdt' => "dark blue container, black base, PENN STATE 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 71. White cab, white container, black base, "Dupont 99" labels (WR)
	['var' => '71a', 'mfg' => 'Thailand', 'liv' => 'Dupont',
            'cdt' => 'white',
            'tdt' => "white container, black base, DUPONT 99 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 72. Red cab, red container, black base, "Nastrak" labels (WR)(GS)
	['var' => '72a', 'mfg' => 'Thailand', 'liv' => 'Nastrak', 'cod' => '1',
            'cdt' => 'red',
            'tdt' => "red container, black base, NASTRAK labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 73. Blue cab, yellow container, black base, "Mannheim" labels (WR)
	['var' => '73a', 'mfg' => 'Thailand', 'liv' => 'Mannheim',
            'cdt' => 'blue',
            'tdt' => "yellow container, black base, MANNHEIM labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 74. White cab, white container, black base, "Veh Vereinigte Getran-keebetriebe Cottbus" labels (C2)
	['var' => '74a', 'mfg' => 'Thailand', 'liv' => '',
            'cdt' => 'white',
            'tdt' => "white container, black base, VEH VEREINIGTE GETRAN-KEEBETRIEBE COTTBUS labels",
        ],
// 75. White cab, white container, black base, "8th European MICA Convention" labels (C2)
	['var' => '75a', 'mfg' => 'Thailand', 'liv' => 'MICA',
            'cdt' => 'white',
            'tdt' => "white container, black base, 8TH EUROPEAN MICA CONVENTION labels",
        ],
    ]);
}
?>
