<?php // DONE
$subtitle = 'CY109A';
// CY-109-A FORD AEROMAX SUPERSTAR TRANSPORTER, issued 1991
$desc = "Ford Aeromax Superstar Transporter";
$year = '1991';

$defaults = ['mod' => $subtitle, 'cab' => 'MB214', 'tlr' => 'Superstar Transporter', 'cod' => '2'];

include "cypage.php";

function body() {
// NOTE: All models with 8-spoke wheels and no antennas cast unless otherwise noted.
    show_table([
// 1. Gold cab, gold container, "Folgers" labels (WR)
	['var' => '01a', 'mfg' => 'Macau', 'liv' => 'Folgiers',
	    'cdt' => 'gold',
            'tdt' => "gold container, FOLGERS labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 2. Blue cab, white container, "Bill Elliot 9" labels (WR)
	['var' => '02a', 'mfg' => 'Macau', 'liv' => 'Bill Elliot',
	    'cdt' => 'blue',
            'tdt' => "white container, BILL ELLIOT 9 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 3. White cab, white container, "Hooters Racing" labels (WR)
	['var' => '03a', 'mfg' => 'Macau', 'liv' => 'Hooters',
	    'cdt' => 'white',
            'tdt' => "white container, HOOTERS RACING labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 4. Black cab, black container, "Texaco Havoline/Davey Allison" labels (WR)
	['var' => '04a', 'mfg' => 'Macau', 'liv' => 'Texaco',
	    'cdt' => 'black',
            'tdt' => "black container, TEXACO HAVOLINE/DAVEY ALLISON labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 5. White cab, dark blue container, "Goodyear Racing" labels (WR)
	['var' => '05a', 'mfg' => 'Macau', 'liv' => 'Goodyear',
	    'cdt' => 'white',
            'tdt' => "dark blue container, GOODYEAR RACING labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 6. Red cab, red container, "Melling Performance 9" labels (WR)
	['var' => '06a', 'mfg' => 'Macau', 'liv' => 'Melling Performance',
	    'cdt' => 'red',
            'tdt' => "red container, MELLING PERFORMANCE 9 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 7. Red cab, red container, "Motorcraft" labels (WR)
	['var' => '07a', 'mfg' => 'Macau', 'liv' => 'Motorcraft',
	    'cdt' => 'red',
            'tdt' => "red container, MOTORCRAFT labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 8. White cab, dark blue container, "Penn State Nittany Lions" labels (WR)
	['var' => '08a', 'mfg' => 'Macau', 'liv' => 'Penn State',
	    'cdt' => 'white',
            'tdt' => "dark blue container, PENN STATE NITTANY LIONS labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 9. Red-brown cab, red-brown container, "Washington Redskins Super Bowl Champions" labels (WR)
	['var' => '09a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'red-brown',
            'tdt' => "red-brown container, WASHINGTON REDSKINS SUPER BOWL CHAMPIONS labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 10. White cab, white container, "Snickers Racing Team" labels (WR)
	['var' => '10a', 'mfg' => 'Macau', 'liv' => 'Snickers',
	    'cdt' => 'white',
            'tdt' => "white container, SNICKERS RACING TEAM labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 11. Black cab, black container, "Stanley Mechanic Tools 92" labels (WR)
	['var' => '11a', 'mfg' => 'Macau', 'liv' => 'Stanley',
	    'cdt' => 'black',
            'tdt' => "black container, STANLEY MECHANIC TOOLS 92 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 12. Green cab, red container, "Merry Christmas White Rose Collectibles 1992" labels (WR)
	['var' => '12a', 'mfg' => 'Macau', 'liv' => 'White Rose',
	    'cdt' => 'green',
            'tdt' => "red container, MERRY CHRISTMAS WHITE ROSE COLLECTIBLES 1992 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 13. Blue cab, blue container, "Matchbox 29 Racing" labels (WR)
	['var' => '13a', 'mfg' => 'Macau', 'liv' => 'Matchbox',
	    'cdt' => 'blue',
            'tdt' => "blue container, MATCHBOX 29 RACING labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 14. White cab, white container, "Purex" labels (WR)
	['var' => '14a', 'mfg' => 'Macau', 'liv' => 'Purex',
	    'cdt' => 'white',
            'tdt' => "white container, PUREX labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 15. Red cab, white container, "Wood Brothers-Citgo" labels (WR)
	['var' => '15a', 'mfg' => 'Macau', 'liv' => 'Citgo',
	    'cdt' => 'red',
            'tdt' => "white container, WOOD BROTHERS-CITGO labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 16. Yellow cab, yellow container, "Matchbox Hong Kong Men of the Years 1982-1992" tempa (HK)
	['var' => '16a', 'mfg' => 'Macau', 'liv' => 'Matchbox', 'cod' => '1',
	    'cdt' => 'yellow',
            'tdt' => "yellow container, MATCHBOX HONG KONG MEN OF THE YEARS 1982-1992 tempa",
        ],
// 17. Black cab, black container, "54th All Star Game" labels (WR)
	['var' => '17a', 'mfg' => 'Macau', 'liv' => 'MLB',
	    'cdt' => 'black',
            'tdt' => "black container, 54TH ALL STAR GAME labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 18. Black cab, turquoise container, "1993 Florida Marlins" labels (WR)
	['var' => '18a', 'mfg' => 'Macau', 'liv' => 'MLB',
	    'cdt' => 'black',
            'tdt' => "turquoise container, 1993 FLORIDA MARLINS labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 19. Black cab, purple container, "1993 Colorado Rockies" labels (WR)
	['var' => '19a', 'mfg' => 'Macau', 'liv' => 'MLB',
	    'cdt' => 'black',
            'tdt' => "purple container, 1993 COLORADO ROCKIES labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 20. Silver-gray cab, dark blue container, "Cowboys Super Bowl Champions" labels (WR)
	['var' => '20a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'silver-gray',
            'tdt' => "dark blue container, COWBOYS SUPER BOWL CHAMPIONS labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 21. Orange cab, orange container "Reithoffer's Thunderbolt" labels (WR)(GS)
	['var' => '21a', 'mfg' => 'Macau', 'liv' => "Reithoffer's",
	    'cdt' => 'orange',
            'tdt' => "orange container REITHOFFER'S THUNDERBOLT labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 22. Black cab, black container, "Virginia is for Lovers 25" labels (WR)
	['var' => '22a', 'mfg' => 'Macau', 'liv' => 'Virginia',
	    'cdt' => 'black',
            'tdt' => "black container, VIRGINIA IS FOR LOVERS 25 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 23. Black cab, red container, "Falcons 1993" labels (WR)
	['var' => '23a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'black',
            'tdt' => "red container, FALCONS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 24. Black cab, black container, "Steelers 1993" labels (WR)
	['var' => '24a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'black',
            'tdt' => "black container, STEELERS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 25. White cab, blue container, "Patriots 1993" labels (WR)
	['var' => '25a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'white',
            'tdt' => "blue container, PATRIOTS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 26. White cab, purple container, "Vikings 1993" labels (WR)
	['var' => '26a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'white',
            'tdt' => "purple container, VIKINGS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 27. White cab, red container, "Oilers 1993" labels (WR)
	['var' => '27a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'white',
            'tdt' => "red container, OILERS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 28. White cab, red container, "Buccaneers 1993" labels (WR)
	['var' => '28a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'white',
            'tdt' => "red container, BUCCANEERS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 29. White cab, orange container, "Broncos 1993" labels (WR)
	['var' => '29a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'white',
            'tdt' => "orange container, BRONCOS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 30. White cab, blue container, "Rams 1993" labels (WR)
	['var' => '30a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'white',
            'tdt' => "blue container, RAMS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 31. Orange cab, black container, "Bengals 1993" labels (WR)
	['var' => '31a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'orange',
            'tdt' => "black container, BENGALS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 32. Orange cab, brown container, "Browns 1993" labels (WR)
	['var' => '32a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'orange',
            'tdt' => "brown container, BROWNS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 33. Red cab, blue container, "Bills 1993" labels (WR)
	['var' => '33a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'red',
            'tdt' => "blue container, BILLS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 34. Red cab, yellow container, "KC Chiefs 1993" labels (WR)
	['var' => '34a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'red',
            'tdt' => "yellow container, KC CHIEFS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 35. Red-brown cab, yellow container, "Redskins 1993" labels (WR)
	['var' => '35a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'red-brown',
            'tdt' => "yellow container, REDSKINS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 36. Red-brown cab, white container, "Cardinals 1993" labels (WR)
	['var' => '36a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'red-brown',
            'tdt' => "white container, CARDINALS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 37. Green-gold cab, black container, "Saints 1993" labels (WR)
	['var' => '37a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'green-gold',
            'tdt' => "black container, SAINTS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 38. Gold cab, gold container, "49ers 1993" labels (WR)
	['var' => '38a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'gold',
            'tdt' => "gold container, 49ERS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 39. Blue-green cab, orange container, "Dolphins 1993" labels (WR)
	['var' => '39a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'blue-green',
            'tdt' => "orange container, DOLPHINS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 40. Green cab, black container, "Jets 1993" labels (WR)
	['var' => '40a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'green',
            'tdt' => "black container, JETS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 41. Green cab, white container, "Eagles 1993" labels (WR)
	['var' => '41a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'green',
            'tdt' => "white container, EAGLES 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 42. Dull green cab, yellow container, "Packers 1993" labels (WR)
	['var' => '42a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'dull green',
            'tdt' => "yellow container, PACKERS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 43. Blue cab, red container, "Giants 1993" labels (WR)
	['var' => '43a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'blue',
            'tdt' => "red container, GIANTS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 44. Blue cab, white container, "Colts 1993" labels (WR)
	['var' => '44a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'blue',
            'tdt' => "white container, COLTS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 45. Dark blue cab, orange container, "Bears 1993" labels (WR)
	['var' => '45a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'dark blue',
            'tdt' => "orange container, BEARS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 46. Dark blue cab, yellow container, "Chargers 1993" labels (WR)
	['var' => '46a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'dark blue',
            'tdt' => "yellow container, CHARGERS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 47. Silver-gray cab, green container, "Seahawks 1993" labels (WR)
	['var' => '47a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'silver-gray',
            'tdt' => "green container, SEAHAWKS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 48. Silver-gray cab, blue container, "Lions 1993" labels (WR)
	['var' => '48a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'silver-gray',
            'tdt' => "blue container, LIONS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 49. Silver-gray cab, dark blue container, "Cowboys 1993" labels (WR)
	['var' => '49a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'silver-gray',
            'tdt' => "dark blue container, COWBOYS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 50. Silver-gray cab, black container, "Raiders 1993" labels (WR)
	['var' => '50a', 'mfg' => 'Macau', 'liv' => 'NFL',
	    'cdt' => 'silver-gray',
            'tdt' => "black container, RAIDERS 1993 labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 51. Black and red cab, black container, "Cappio" labels (WR)
	['var' => '51a', 'mfg' => 'Macau', 'liv' => 'Cappio',
	    'cdt' => 'black and red',
            'tdt' => "black container, CAPPIO labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 52. Yellow cab, yellow container, "Dewalt 08-B. Dotter" labels (WR)
	['var' => '52a', 'mfg' => 'Macau', 'liv' => 'Dewalt',
	    'cdt' => 'yellow',
            'tdt' => "yellow container, DEWALT 08-B. DOTTER labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 53. White and blue cab, white container, "Valvoline" labels (WR)
	['var' => '53a', 'mfg' => 'Macau', 'liv' => 'Valvoline',
	    'cdt' => 'white and blue',
            'tdt' => "white container, VALVOLINE labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 54. Sea green cab, white container, "Matchbox Road Museum" labels (WR)
	['var' => '54a', 'mfg' => 'Macau', 'liv' => 'Matchbox',
	    'cdt' => 'sea green',
            'tdt' => "white container, MATCHBOX ROAD MUSEUM labels",
	    'nts' => 'Manufactured for White Rose',
        ],
// 55. Orange-red cab, orange-red container, "Parcel Post Australia" labels (AU)
	['var' => '55a', 'mfg' => 'Macau', 'liv' => 'Parcel Post', 'cod' => '1',
	    'cdt' => 'orange-red',
            'tdt' => "orange-red container, PARCEL POST AUSTRALIA labels",
        ],
// 56. White cab, white container, "Proball Paintball" labels (US)
	['var' => '56a', 'mfg' => 'Macau', 'liv' => 'Proball', 'cod' => '1',
	    'cdt' => 'white',
            'tdt' => "white container, PROBALL PAINTBALL labels",
        ],
// 57. White cab, white container, "Fastway Couriers" labels (AU)
	['var' => '57a', 'mfg' => 'Macau', 'liv' => 'Fastway', 'cod' => '1',
	    'cdt' => 'white',
            'tdt' => "white container, FASTWAY COURIERS labels",
        ],
// 58. White cab, white container, "Gold Coast Rollers" labels (AU)
	['var' => '58a', 'mfg' => 'Macau', 'liv' => 'NBL', 'cod' => '1',
	    'cdt' => 'white',
            'tdt' => "white container, GOLD COAST ROLLERS labels",
        ],
// 59. White cab, white container, "Newcastle Falcons" labels (AU)
	['var' => '59a', 'mfg' => 'Macau', 'liv' => 'NBL', 'cod' => '1',
	    'cdt' => 'white',
            'tdt' => "white container, NEWCASTLE FALCONS labels",
        ],
// 60. White cab, white container, "Wildcats" labels (AU)
	['var' => '60a', 'mfg' => 'Macau', 'liv' => 'NBL', 'cod' => '1',
	    'cdt' => 'white',
            'tdt' => "white container, WILDCATS labels",
        ],
// 61. White cab, white container, "Illawarra Hawks" labels (AU)
	['var' => '61a', 'mfg' => 'Macau', 'liv' => 'NBL', 'cod' => '1',
	    'cdt' => 'white',
            'tdt' => "white container, ILLAWARRA HAWKS labels",
        ],
// 62. White cab, white container, "Brisbane Bullets" labels (AU)
	['var' => '62a', 'mfg' => 'Macau', 'liv' => 'NBL', 'cod' => '1',
	    'cdt' => 'white',
            'tdt' => "white container, BRISBANE BULLETS labels",
        ],
// 63. White and purple cab, white container, "Sydney Kings" labels (AU)
	['var' => '63a', 'mfg' => 'Macau', 'liv' => 'NBL', 'cod' => '1',
	    'cdt' => 'white and purple',
            'tdt' => "white container, SYDNEY KINGS labels",
        ],
// 64. Orange cab, white container, "Townsville Suns" labels (AU)
	['var' => '64a', 'mfg' => 'Macau', 'liv' => 'NBL', 'cod' => '1',
	    'cdt' => 'orange',
            'tdt' => "white container, TOWNSVILLE SUNS labels",
        ],
// 65. Orange-red cab, orange-red container, "Canberra Cannons" labels (AU)
	['var' => '65a', 'mfg' => 'Macau', 'liv' => 'NBL', 'cod' => '1',
	    'cdt' => 'orange-red',
            'tdt' => "orange-red container, CANBERRA CANNONS labels",
        ],
// 66. Red cab, dark blue container, "Geelong Supercats" labels (AU)
	['var' => '66a', 'mfg' => 'Macau', 'liv' => 'NBL', 'cod' => '1',
	    'cdt' => 'red',
            'tdt' => "dark blue container, GEELONG SUPERCATS labels",
        ],
// 67. Green cab, green container, "Devils" labels (AU)
	['var' => '67a', 'mfg' => 'Macau', 'liv' => 'NBL', 'cod' => '1',
	    'cdt' => 'green',
            'tdt' => "green container, DEVILS labels",
        ],
// 68. Blue-green cab, blue-green container, "North Melbourne Giants" labels (AU)
	['var' => '68a', 'mfg' => 'Macau', 'liv' => 'NBL', 'cod' => '1',
	    'cdt' => 'blue-green',
            'tdt' => "blue-green container, NORTH MELBOURNE GIANTS labels",
        ],
// 69. Blue cab, blue container, "Adelaide 36ers" labels (AU)
	['var' => '69a', 'mfg' => 'Macau', 'liv' => 'NBL', 'cod' => '1',
	    'cdt' => 'blue',
            'tdt' => "blue container, ADELAIDE 36ERS labels",
        ],
// 70. Black cab, black container, "Magic" labels (AU)
	['var' => '70a', 'mfg' => 'Macau', 'liv' => 'NBL', 'cod' => '1',
	    'cdt' => 'black',
            'tdt' => "black container, MAGIC labels",
        ],
// 71. Black cab, black container, "Melbourne Tigers" labels (AU)
	['var' => '71a', 'mfg' => 'Macau', 'liv' => 'NBL', 'cod' => '1',
	    'cdt' => 'black',
            'tdt' => "black container, MELBOURNE TIGERS labels",
        ],
    ]);
}
?>
