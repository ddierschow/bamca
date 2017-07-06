<?php // DONE
$subtitle = 'CY039A';
// CY-39-A FORD AEROMAX BOX TRUCK, issued 1994
$desc = "Aeromax Box Trailer";
$year = '1994';

$defaults = ['mod' => $subtitle, 'cab' => 'MB214', 'tlr' => 'CYT04', 'cod' => '1'];

// NOTE: All models with 8-spoke wheels, no antennas cast unless otherwise noted
$models = [
// 1. White cab with black chassis, white container with white base, "Pepsi/Diet Pepsi" labels
    ['var' => '001a', 'mfg' => 'Thailand', 'liv' => 'Pepsi', 'rar' => '2',
	'cdt' => 'white, black chassis', 'cva' => '057',
	'tdt' => 'white container, white base, PEPSI/DIET PEPSI labels',
    ],
// 2. Yellow cab with black chassis, yellow container with yellow base, "Cheerios" labels
    ['var' => '002a', 'mfg' => 'Thailand', 'liv' => 'Cheerios', 'rar' => '2',
	'cdt' => 'yellow, black chassis', 'cva' => '058',
	'tdt' => 'yellow container, yellow base, CHEERIOS labels ',
    ],
// 3. Red cab with red chassis, red container with red base, "Heinz Tomato Ketchup Squeezable!" labels (UK)
    ['var' => '003a', 'mfg' => 'Thailand', 'liv' => 'Heinz', 'rar' => '2',
	'cdt' => 'red', 'cva' => '059',
	'tdt' => 'red container, red base, HEINZ TOMATO KETCHUP SQUEEZABLE! labels',
    ],
// 4. Blue cab with blue chassis, blue container with blue base, "Oreo" labels, Thailand
    ['var' => '004a', 'mfg' => 'Thailand', 'liv' => 'Oreo', 'rar' => '2',
	'cdt' => 'blue', 'cva' => '062',
	'tdt' => 'blue container, blue base, OREO labels',
    ],
// 5. Dark blue cab with dark blue chassis, dark blue container and base, "Hawaiian Punch" labels, Thailand
    ['var' => '005a', 'mfg' => 'Thailand', 'liv' => 'Hawaiian Punch', 'rar' => '2',
	'cdt' => 'dark blue', 'cva' => '061',
	'tdt' => 'dark blue container and base, HAWAIIAN PUNCH labels',
    ],
// 6. Orange cab with black chassis, orange container and base, "Honey Nut Cheerios" labels, Thailand
    ['var' => '006a', 'mfg' => 'Thailand', 'liv' => 'Cheerios', 'rar' => '2',
	'cdt' => 'orange, black chassis', 'cva' => '060',
	'tdt' => 'orange container and base, HONEY NUT CHEERIOS labels',
    ],
// 7. Silver/gray cab with black chassis, white container and base, "Pepsi/Diet Pepsi" labels, Thailand
    ['var' => '007a', 'mfg' => 'Thailand', 'liv' => 'Pepsi', 'rar' => '2',
	'cdt' => 'silver-gray, black chassis', 'cva' => '066',
	'tdt' => 'white container and base, PEPSI/DIET PEPSI labels',
    ],
// 8. White cab with black chassis, orange container with white chassis, "Honey Nut Cheerios" labels, Thailand
    ['var' => '008a', 'mfg' => 'Thailand', 'liv' => 'Cheerios', 'rar' => '2',
	'cdt' => 'white, black chassis', 'cva' => '065',
	'tdt' => 'orange container, white chassis, HONEY NUT CHEERIOS labels',
    ],
// 9. White cab with blue chassis, blue container with white chassis, "Hawaiian Punch" labels, Thailand
    ['var' => '009a', 'mfg' => 'Thailand', 'liv' => 'Hawaiian Punch', 'rar' => '2',
	'cdt' => 'white, blue chassis', 'cva' => '064',
	'tdt' => 'blue container, white chassis, HAWAIIAN PUNCH labels',
    ],
// 10. Black cab with blue chassis, blue container with black base, "Oreo" labels, Thailand
    ['var' => '010a', 'mfg' => 'Thailand', 'liv' => 'Oreo', 'rar' => '2',
	'cdt' => 'black, blue chassis', 'cva' => '067',
	'tdt' => 'blue container, black base, OREO labels',
    ],
// 11. White cab with black chassis, white container and base, "Fed Ex" labels, Thailand
    ['var' => '011a', 'mfg' => 'Thailand', 'liv' => 'Fed Ex', 'rar' => '2',
	'cdt' => 'white, black chassis', 'cva' => '070',
	'tdt' => 'white container and base, FED EX labels',
    ],
// 12. White cab with black chassis, white container with black base, "Fed Ex" labels, China
    ['var' => '012a', 'mfg' => 'China', 'liv' => 'Fed Ex', 'rar' => '2',
	'cdt' => 'white, black chassis', 'cva' => '087',
	'tdt' => 'white container, black base, FED EX labels',
    ],
// 13. White cab and chassis, white container and base, "Nothing Else Is A Pepsi" labels, China
    ['var' => '013a', 'mfg' => 'China', 'liv' => 'Pepsi', 'rar' => '2',
	'cdt' => 'white', 'cva' => '088',
	'tdt' => 'white, NOTHING ELSE IS A PEPSI labels',
    ],
// 14. Black cab with blue chassis, blue container with black base, "Oreo" labels, China
    ['var' => '014a', 'mfg' => 'China', 'liv' => 'Oreo', 'rar' => '2',
	'cdt' => 'black, blue chassis', 'cva' => '085',
	'tdt' => 'blue container,black base, OREO labels',
    ],
// 15. Black cab and chassis, black container and base, "Body Glove" labels, China
    ['var' => '015a', 'mfg' => 'China', 'liv' => 'Body Glove Ex', 'rar' => '2',
	'cdt' => 'black', 'cva' => '086',
	'tdt' => 'black, BODY GLOVE labels',
    ],
// 16. Green cab, black chassis, green container and base, "Collector's Choice Upper Deck" labels, China
    ['var' => '016a', 'mfg' => 'China', 'liv' => 'Upper Deck', 'rar' => '2',
	'cdt' => 'green, black chassis', 'cva' => '092',
	'tdt' => "green, COLLECTOR'S CHOICE UPPER DECK labels",
    ],
// 17. White cab and chassis, white container and base, "Barnes Van Lines" tampo, China (ASAP)
    ['var' => '017a', 'mfg' => 'China', 'liv' => 'Barnes', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, BARNES VAN LINES tampo',
    ],
// 18. White cab and chassis, white container and base, "Oh What Those Oats Can Do!" labels, China (ASAP)
    ['var' => '018a', 'mfg' => 'China', 'liv' => '', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, OH WHAT THOSE OATS CAN DO! labels',
    ],
// 19. White cab and chassis, white container and base, "Ryder Transportation Services" tampo, China (ASAP)
    ['var' => '019a', 'mfg' => 'China', 'liv' => 'Ryder', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, RYDER TRANSPORTATION SERVICES tampo',
    ],
// 20. White cab and chassis, white container and base, "Pocahontas PFG" tampo, China (ASAP)
    ['var' => '020a', 'mfg' => 'China', 'liv' => 'Pocahontas', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, POCAHONTAS PFG tampo',
    ],
// 21. White cab and chassis, white container and base, no labels, China (ASAP blank)
    ['var' => '021a', 'mfg' => 'China', 'liv' => 'none', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, no labels',
    ],
// 22. White cab and chassis, white container and base, "Atlas Van Lines-Thomas of California" tampo, China (ASAP)
    ['var' => '022a', 'mfg' => 'China', 'liv' => 'Atlas Van Lines', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, ATLAS VAN LINES-THOMAS OF CALIFORNIA tampo',
    ],
// 23. White cab and chassis, white container and base, "International Airport Center 1-888-Lease-Us" tampo, China (ASAP)
    ['var' => '023a', 'mfg' => 'China', 'liv' => 'International Airport Center', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, INTERNATIONAL AIRPORT CENTER 1-888-LEASE-US tampo',
    ],
// 24. White cab and chassis, white container and base, "McLane Distribution Services" tampo, China (ASAP)
    ['var' => '024a', 'mfg' => 'China', 'liv' => 'McLane', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, MCLANE DISTRIBUTION SERVICES tampo',
    ],
// 25. White cab and chassis, white container and base, "Castle-berry's" tampo, China (ASAP)(OP)
    ['var' => '025a', 'mfg' => 'China', 'liv' => "Castleberry's", 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => "white, CASTLE-BERRY'S tampo",
    ],
// 26. White cab and chassis, white container and base, "Austex" tampo, China (ASAP)(OP)
    ['var' => '026a', 'mfg' => 'China', 'liv' => 'Austex', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, AUSTEX tampo',
    ],
// 27. Pale red cab, black chassis, red container, black base, "Coca-Cola" with Santa Claus labels, China, rubber tires (US)
    ['var' => '027a', 'cab' => 'MB308', 'mfg' => 'China', 'liv' => 'Coca-Cola', 'rar' => '2',
	'cdt' => 'pale red, black chassis', 'cva' => '094',
	'tdt' => 'red container, black base, COCA-COLA with Santa Claus labels',
    ],
// 28. White cab and chassis, white container and base, "Klockner Optima Waste-free Films" labels, China (ASAP)
    ['var' => '028a', 'mfg' => 'China', 'liv' => 'Klockner', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, KLOCKNER OPTIMA WASTE-FREE FILMS labels',
    ],
// 29. White cab, black chassis, white container and base, "K-B Toys" tampo, China, rubber tires, antennas cast (GC)
    ['var' => '029a', 'cab' => 'MB308', 'mfg' => 'China', 'liv' => 'K-B', 'rar' => '2',
	'cdt' => 'white, black chassis', 'cva' => '',
	'tdt' => 'white, K-B TOYS tampo',
    ],
// 30. White cab and chassis, white container and base, "Super Pretzel" labels, China (US)(OP)
    ['var' => '030a', 'mfg' => 'China', 'liv' => 'Super Pretzel', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, SUPER PRETZEL labels',
    ],
// 31. White cab, black chassis, white container and base, "Midas Auto Systems Experts" tampo, China, rubber tires, antennas cast (PC)
    ['var' => '031a', 'cab' => 'MB308', 'mfg' => 'China', 'liv' => 'Midas', 'rar' => '2',
	'cdt' => 'white, black chassis', 'cva' => '',
	'tdt' => 'white, MIDAS AUTO SYSTEMS EXPERTS tampo',
    ],
// 32. Blue cab, black chassis, blue container and base, "Goodyear #1 in Tires" tampo, China, rubber tires, antennas cast (PC)
    ['var' => '032a', 'cab' => 'MB308', 'mfg' => 'China', 'liv' => 'Goodyear', 'rar' => '2',
	'cdt' => 'blue, black chassis', 'cva' => '',
	'tdt' => 'blue, GOODYEAR #1 IN TIRES tampo',
    ],
// 33. White cab and chassis, white container and base, "Mobile Process Technology" tampo, China (ASAP)
    ['var' => '033a', 'mfg' => 'China', 'liv' => 'Mobile Process Technology', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, MOBILE PROCESS TECHNOLOGY tampo',
    ],
// 34. White cab and chassis, white container and base, "Metal Industries/Capitol" tampo, China (ASAP)
    ['var' => '034a', 'mfg' => 'China', 'liv' => 'Metal Indstries', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, METAL INDUSTRIES/CAPITOL tampo',
    ],
// 35. White cab, black chassis, powder blue container, white base, "Coca-Cola" with polar bear labels, China
    ['var' => '035a', 'mfg' => 'China', 'liv' => 'Coca-Cola', 'rar' => '2',
	'cdt' => 'white, black chassis', 'cva' => '',
	'tdt' => 'powder blue container, white base, COCA-COLA with polar bear labels',
    ],
// 36. White cab and chassis, white container and base, "PYA/ Monarch Foodservice Distributors" tampo, China (ASAP)
    ['var' => '036a', 'mfg' => 'China', 'liv' => 'PYA', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, PYA/ MONARCH FOODSERVICE DISTRIBUTORS tampo',
    ],
// 37. White cab and chassis, white container and base, "Monarch Foodservice Distributors" tampo, China (ASAP)
    ['var' => '037a', 'mfg' => 'China', 'liv' => 'Monarch', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, MONARCH FOODSERVICE DISTRIBUTORS tampo',
    ],
// 38. White cab and chassis, white container and base, "EFI-Set your ideas on Fiery" labels, China (ASAP)
    ['var' => '038a', 'mfg' => 'China', 'liv' => 'EFI', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, EFI-SET YOUR IDEAS ON FIERY labels',
    ],
// 39. White cab and chassis, white container and base, "Albertsons" labels, China (US)
    ['var' => '039a', 'mfg' => 'China', 'liv' => 'Albertsons', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, ALBERTSONS labels',
    ],
// 40. White cab and chassis, white container and base, "Rite Screen" tampo, China (ASAP)
    ['var' => '040a', 'mfg' => 'China', 'liv' => 'Rite Screen', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, RITE SCREEN tampo',
    ],
// 41. White cab and chassis, white container and base, "Ml Metals" tampo, China (ASAP)
    ['var' => '041a', 'mfg' => 'China', 'liv' => 'M1 Metals', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, ML METALS tampo',
    ],
// 42. White cab and chassis, white container and base, "Ml Plastics" tampo, China (ASAP)
    ['var' => '042a', 'mfg' => 'China', 'liv' => 'M1 Plastics', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, ML PLASTICS tampo',
    ],
// 43. White cab and chassis, white container and base, "Ml Home Products" tampo, China (ASAP)
    ['var' => '043a', 'mfg' => 'China', 'liv' => 'M1 Home Products', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, ML HOME PRODUCTS tampo',
    ],
// 44. Bright blue cab and chassis, bright blue container and base, "Toys R Us-50 Years Forever Fun" labels, China, rubber tires, antennas cast (TRU-PC)
    ['var' => '044a', 'cab' => 'MB308', 'mfg' => 'China', 'liv' => 'Toys R Us', 'rar' => '2',
	'cdt' => 'bright blue', 'cva' => '',
	'tdt' => 'bright blue, TOYS R US-50 YEARS FOREVER FUN labels',
    ],
// 45. Red cab, black chassis, red container and base, "Coca Cola" with Santa Claus labels, China (US)
    ['var' => '045a', 'mfg' => 'China', 'liv' => 'Coca-Cola', 'rar' => '2',
	'cdt' => 'red, black chassis', 'cva' => '',
	'tdt' => 'red, COCA COLA with Santa Claus labels',
    ],
// 46. White cab and chassis, white container and base, "Simplot" tampo, China (ASAP)
    ['var' => '046a', 'mfg' => 'China', 'liv' => 'Simplot', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, SIMPLOT tampo',
    ],
// 47. White cab, black chassis, white container and base, "Vons Seafood" labels, China (US)
    ['var' => '047a', 'mfg' => 'China', 'liv' => 'Vons', 'rar' => '2',
	'cdt' => 'white, black chassis', 'cva' => '',
	'tdt' => 'white, VONS SEAFOOD labels',
    ],
// 48. White cab, black chassis, powder blue container, white base, "Coca Cola" labels, China and "Mattel"
    ['var' => '048a', 'mfg' => 'China, MATTEL', 'liv' => 'Coca-Cola', 'rar' => '2',
	'cdt' => 'white, black chassis', 'cva' => '',
	'tdt' => 'powder blue container, white base, COCA COLA labels',
    ],
// 49. Dark purple body, white chassis, white container and chassis, "Taco Bell" labels, China and "Mattel"
    ['var' => '049a', 'mfg' => 'China, MATTEL', 'liv' => 'Taco Bell', 'rar' => '2',
	'cdt' => 'dark purple body, white chassis', 'cva' => '',
	'tdt' => 'white, TACO BELL labels',
    ],
// 50. White cab and chassis, blue container and chassis, "Kellogg's" and cartoon characters labels, China and "Mattel"
    ['var' => '050a', 'mfg' => 'China, MATTEL', 'liv' => "Kellogg's", 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => "blue, KELLOGG'S and cartoon characters labels",
    ],
// 51. Red cab, black chassis, red container, black chassis, "Coca Cola" and Santa labels, China and "Mattel" (US)
    ['var' => '051a', 'mfg' => 'China, MATTEL', 'liv' => 'Coca-Cola', 'rar' => '2',
	'cdt' => 'red, black chassis', 'cva' => '',
	'tdt' => 'red container, black chassis, COCA COLA and Santa labels',
    ],
// 52. White cab and chassis, white container and chassis, "Oh What those Oats can do!" tampo, China (ASAP)
    ['var' => '052a', 'mfg' => 'China', 'liv' => '', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, OH WHAT THOSE OATS CAN DO! tampo',
    ],
// 53. White cab and chassis, white container and chassis, "At A Glance-Millennium" labels, China (ASAP)
    ['var' => '053a', 'mfg' => 'China', 'liv' => '', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, AT A GLANCE-MILLENNIUM labels',
    ],
// 54. White cab and chassis, white container and chassis, "Ian Patrick Mullaney...has rolled in early" (right side only) tampo, China (ASAP)
    ['var' => '054a', 'mfg' => 'China', 'liv' => '', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, IAN PATRICK MULLANEY...HAS ROLLED IN EARLY (right side only) tampo',
    ],
// 55. White cab and chassis, white container and base, "Alaska Airlines" tampo, China (ASAP)
    ['var' => '055a', 'mfg' => 'China', 'liv' => 'Alaska Airlines', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, ALASKA AIRLINES tampo',
    ],
// 56. White cab and chassis, white container and base, "RCA-changing entertainment again" tampo, China (ASAP)
    ['var' => '056a', 'mfg' => 'China', 'liv' => 'RCA', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, RCA-CHANGING ENTERTAINMENT AGAIN tampo',
    ],
// 57. White cab and chassis, white container and base, "Mervyn's Community Closest" labels, China (ASAP)
    ['var' => '057a', 'mfg' => 'China', 'liv' => "Mervyn's", 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => "white, MERVYN'S COMMUNITY CLOSEST labels",
    ],
// 58. White cab and chassis, white container and base, "The Pepsi Bottling Company" (blue background) labels, China (ASAP)
    ['var' => '058a', 'mfg' => 'China', 'liv' => 'Pepsi', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, THE PEPSI BOTTLING COMPANY (blue background) labels',
    ],
// 59. White cab and chassis, white container and base, "The Pepsi Bottling Company" (white background) labels, China (ASAP)
    ['var' => '059a', 'mfg' => 'China', 'liv' => 'Pepsi', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, THE PEPSI BOTTLING COMPANY (white background) labels',
    ],
// 60. White cab and chassis, white container and base, "Ceco Door Products" labels, China (ASAP)
    ['var' => '060a', 'mfg' => 'China', 'liv' => 'Ceco', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, CECO DOOR PRODUCTS labels',
    ],
// 61. White cab and chassis, white container and base, "Parcel Direct" labels, China (ASAP)
    ['var' => '061a', 'mfg' => 'China', 'liv' => 'Parcel Direct', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, PARCEL DIRECT labels',
    ],
// 62. White cab and chassis, white container and base, "Black Dog DVD Express" (left side only) tampo, China (ASAP)
    ['var' => '062a', 'mfg' => 'China', 'liv' => 'Black Dog', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, BLACK DOG DVD EXPRESS (left side only) tampo',
    ],
// 63. Orange and blue cab, blue chassis, white container and base, "Roadway" tampo, China (ASAP)
    ['var' => '063a', 'mfg' => 'China', 'liv' => 'Roadway', 'cod' => '2', 'rar' => '2',
	'cdt' => 'orange and blue, blue chassis', 'cva' => '',
	'tdt' => 'white, ROADWAY tampo',
    ],
// 64. White cab and chassis, white container and base, "The Celebrity Train" tampo, China (ASAP)
    ['var' => '064a', 'mfg' => 'China', 'liv' => 'Celebrity Train', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, THE CELEBRITY TRAIN tampo',
    ],
// 65. White cab and chassis, white container and base, "Klondike Good Humor Popsicle" labels, China (ASAP)
    ['var' => '065a', 'mfg' => 'China', 'liv' => 'Klondike', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, KLONDIKE GOOD HUMOR POPSICLE labels',
    ],
// 66. White cab and chassis, white container and base, "Matchbox Books" labels, China (CLR)
    ['var' => '066a', 'mfg' => 'China', 'liv' => 'Matchbox Books', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, MATCHBOX BOOKS labels',
    ],
// 67. White cab and chassis, white container and base, "Sanford Shelbeyville Distribution Center" (left side only) tampo, China (ASAP)
    ['var' => '067a', 'mfg' => 'China', 'liv' => 'Sanford Shelbyville Distribution Center', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, SANFORD SHELBEYVILLE DISTRIBUTION CENTER (left side only) tampo',
    ],
// 68. White cab and chassis, white container and base, "Ship McQuaide" tampo, China (ASAP)
    ['var' => '068a', 'mfg' => 'China', 'liv' => 'Ship McQuaide', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, SHIP MCQUAIDE tampo',
    ],
// 69. White cab and chassis, white container and base, "Fieldbrook Farms" tampo, China (ASAP)
    ['var' => '069a', 'mfg' => 'China', 'liv' => 'Fieldbrook Farms', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, FIELDBROOK FARMS tampo',
    ],
// 70. White cab and chassis, white container and base, "Another Load of Express Cargo- Alaska Airlines" tampo, China (ASAP)
    ['var' => '070a', 'mfg' => 'China', 'liv' => 'Alaska Airlines', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, ANOTHER LOAD OF EXPRESS CARGO- ALASKA AIRLINES tampo',
    ],
// 71. Orange and blue cab, blue chassis, white container and base, none labels, China (ASAP blank)
    ['var' => '071a', 'mfg' => 'China', 'liv' => 'none', 'cod' => '2', 'rar' => '2',
	'cdt' => 'orange and blue, blue chassis', 'cva' => '',
	'tdt' => 'white, none labels',
    ],
// 72. Orange and blue cab, blue chassis, white container and base, "We've Scored! 20th Annual Matchbox USA Convention and Toy Show" tampo, China (CLR)
    ['var' => '072a', 'mfg' => 'China', 'liv' => '', 'rar' => '2',
	'cdt' => 'orange and blue, blue chassis', 'cva' => '',
	'tdt' => "white, WE'VE SCORED! 20TH ANNUAL MATCHBOX USA CONVENTION AND TOY SHOW tampo",
    ],
// 73. White cab and chassis, white container and base, "Nazareth Pallet Co." tampo, China (ASAP)
    ['var' => '073a', 'mfg' => 'China', 'liv' => 'Nazareth Pallet Co.', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, NAZARETH PALLET CO. tampo',
    ],
// 74. White cab and chassis, white container and base, "CIA Truck Adjusting...for the long haul" tampo, China (ASAP)
    ['var' => '074a', 'mfg' => 'China', 'liv' => 'CIA Truck Adjusting', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, CIA TRUCK ADJUSTING...FOR THE LONG HAUL tampo',
    ],
// 75. White cab and chassis, white container and base, "Guida's Milk and Ice Cream" tampo, China (ASAP)
    ['var' => '075a', 'mfg' => 'China', 'liv' => "Guida's", 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => "white, GUIDA'S MILK AND ICE CREAM tampo",
    ],
// 76. White cab and chassis, white container and base, "Bulldog Castor Co." tampo, China (ASAP)
    ['var' => '076a', 'mfg' => 'China', 'liv' => 'Bulldog', 'cod' => '2', 'rar' => '2',
	'cdt' => 'white', 'cva' => '',
	'tdt' => 'white, BULLDOG CASTOR CO. tampo',
    ],
];

include "cypage.php";

function body() {
    global $models;
    show_table($models);
}
?>
