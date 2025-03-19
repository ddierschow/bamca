lexamples = [
    ('WW-E', 'prod/lrw/1969u11'),
    ('WW-GBB', 'prod/lsf/1970u25'),
]

core = [
    ['WW', 'Worldwide Standard Packs 1963-1970', [
        [('D', 'red with yellow arrow (with D type box included) (1963-64)')],
        [('E', 'red, yellow and black (with D, E, or F type box included) (1964-69)')],
        [('F', 'blue and white border, blue background (no box included) (1969)'),
         ('illustration', [
             ('A', 'individual picture of model contained'),
             ('B', 'Matchbox Motorway M2 scene with bridge (without "Superfast")'),
             ('C', 'Matchbox Motorway M2 scene with bridge (with large "Superfast")'),
             ('D', 'Matchbox Motorway M2 scene with bridge (with small and large "Superfast")')])],
        [('G', 'blue border, yellow and white background (1969-70)'),
         ('box included', [
             ('A', 'yes'),
             ('B', 'no')]),
         ('illustration', [
             ('A', 'MB21 Foden Cement Truck & MB25 Ford Cortina (without "Superfast")'),
             ('B', 'MB5 Lotus Europa & MB20 Lamborghini Marzal (with "Superfast")'),
             ('C', 'MB26 GMC Tipper & MB58 DAF Girder Truck (with "Superfast")')]),
         ('backpage', [
             ('A', '"Fred Bronner Corporation - A Division of Lesney Products & Co. Ltd"'),
             ('B', '"Lesney Products Corporation - Formerly Fred Bronner Corporation"'),
             ('C', 'blue printed MB68 Porsche and MB52 Dodge illustration; '
                   'lettering in English, German, Italian and French'),
             ('D', 'blue printed illustration; lettering in English, French, and Swedish'),
             ('E', 'blue printed track setup illustration; lettering in English, German, Italian and French')]),
         'Note: After 1970 different blisterpack designs were used in the US market and elsewhere.'],
    ]],

    ['EU', 'European Standard Packs 1971-2007', [
        [('H', 'red border, yellow background (1971-73)'),
         ('lettering', [
             ('A', '"New MATCHBOX" with wheel, "Superfast" small, with "TESTED" logo (1971)'),
             ('B', 'New "MATCHBOX" with wheel, no "Superfast", with "TESTED" text (1973)'),
             ('C', '"MATCHBOX" without wheel, "Superfast" large, without "TESTED" (1972)')]),
         ('illustration', [
             ('A', 'MB33 Lamborghini Miura'),
             ('B', 'MB10 Pipe Truck'),
             ('C', 'MB19 Lotus Grand Prix'),
             ('D', 'MB19 Road Dragster'),
             ('E', 'MB48 Dodge Dump Truck')])],

        [('I', 'white border, yellow background (1972-74)'),
         ('illustration', [
             ('A', '"Superfast", MB66 Mazda RX 500 & MB44 Refrigerator Truck'),
             ('B', '"Superfast", MB31 Volks Dragon & MB44 Boss Mustang'),
             ('C', '"Superfast", K34 Thunderclap & K35 Lightning'),
             ('D', '"Rola-matics", MB67 Hot Rocker, MB69 Turbo Fury, MB47 Beach Hopper & MB57 Wildlife Truck')])],

        [('J', 'white border, "MATCHBOX" in oval (1975-79)'),
         ('illustration', [
             ('A', '"Superfast", MB63 Tanker, MB62 Renault 17 TL & MB48 Pi-eyed Piper'),
             ('B', '"Rola-matics", MB47 Beach Hopper, MB16 Badger & MB67 Hot Rocker'),
             ('C', '"Streakers", MB66 Mazda RX 500, MB41 Siva Spyder & MB33 Datsun 126 X'),
             ('D', 'railroad, MB43 Steam Loco, MB44 Passenger Coach, MB25 Flat Car & MB24 Diesel Shunter'),
             ('E', '"NEW MODEL"')]),
         'regional issues in similar style: Canada A, Japan A'],

        [('L', 'arrow (1980-83)'),
         ('color', [
             ('A', '"MATCHBOX" red, arrow red'),
             ('B', '"MATCHBOX" red, arrow yellow'),
             ('C', '"MATCHBOX" red, arrow green'),
             ('D', '"MATCHBOX" red, arrow blue'),
             ('E', '"MATCHBOX" black, arrow blue (1983)')]),
         ('arrow direction', [
             ('A', 'lower right to upper left'),
             ('B', 'lower left to upper right'),
             ('C', 'upper right to lower left'),
             ('D', 'upper left to lower right')]),
         ('lettering', [
             ('A', 'name of model and number missing'),
             ('B', 'name of model printed (with or without detail drawing)'),
             ('C', 'name of model stamped'),
             ('D', 'number of model printed or stamped')]),
         ('language of lettering', [
             ('A', 'name of model in English'),
             ('B', 'name of model in English and French'),
             ('C', 'name of model in English, German and French')])],

        [('M', 'blue with yellow & red stripe (1984-87)'),
         ('lettering', [
             ('A', 'name of model printed'),
             ('B', 'no model name')]),
         ('additional text', [
             ('A', 'none'),
             ('B', '"Sammelbild 100 JAHRE AUTO" (1986)'),
             ('C', '"Sammelbild Die Legend&auml;ren Porsche" (1987)')]),
         'regional issues in similar style: China A, Japan B'],

        [('N', 'dark blue with light blue grid (1988-93)'),
         ('format', [
             ('A', 'long (1988)'),
             ('B', 'short, dark blue background (1989-91)'),
             ('C', 'short, light blue background (1992-93)')]),
         ('lettering', [
             ('A', 'model number and name'),
             ('B', 'model number only'),
             ('C', 'none (1991)'),
             ('D', '"OLYMPIA COMIC" (1992)')])],

        [('O', 'orange and yellow with Fast Lane logo (1994-96), short card'),
         ('additional text', [
             ('A', 'none'),
             ('B', '"SUPERFAST"')]),
         'regional issue in similar style: Bulgaria C'],

        [('P', 'orange and yellow with number in yellow rectangle (1997), short card'),
         ('additional text', [
             ('A', 'none'),
             ('B', '"SUPERFAST"'),
             ('C', '"SUPERFAST" and "New Model"')])],

        [('Q', 'orange and white, Ford Explorer, short card, model name in differently colored stripe '
               'according to sub-series'),
         ('format', [
             ('A', 'small "#", no sub-series logo, small "Mattel Wheels" at bottom, '
                   '"Matchbox Toys Ltd." on back (early 1998)'),
             ('B', 'same as a, with additional "FRANCE 98" logo (Opel Calibra ITC only)'),
             ('C', 'small "#", small sub-series logo, large "Mattel Wheels" at bottom, "Mattel, Inc." on back (late 1998)'),
             ('D', 'same as c, with additional "FRANCE 98" logo (Opel Calibra ITC only)'),
             ('E', 'large "#", large sub-series logo, large "Mattel Wheels" at bottom, "Mattel, Inc." on back (1999)'),
             ('F', 'small "#", large sub-series logo, large "Mattel Wheels" at bottom, "Mattel, Inc." on back (2000)')])],

        [('R', 'dark orange and white with new oval Matchbox logo and "Mattel Wheels" at bottom (2001), short card'),
         'Note: During 2002 and 2003 blisterpacks were no longer available in Europe, '
         'with all models being sold in window boxes.'],

        [('S', 'orange with new Matchbox logo, black and white curved stripe along left side, short card'),
         ('main logo on card', [
             ('A', '"HERO CITY"'),
             ('B', '"BONUS!"')]),
         ('model name and number', [
             ('A', 'in yellow banner over model'),
             ('B', 'along right side next to model')]),
         ('graphic behind model', [
             ('A', 'cityscape with sunburst'),
             ('B', 'smudgy white space')])],

        [('T', 'orange and yellow with older Matchbox logo, short card (late 2005 on)', [
            'purple rectangle, "READY FOR ACTION", "MBX METAL"',
            'black and white curved stripe on left side']),
         ('model name and number', [
             ('A', 'number written vertically on right side of card'),
             ('B', 'number written horizontally on right side of card')])],
    ]],

    ['US', 'US Standard Packs 1971-2006', [
        [('H', '''white and blue, "'71 SUPERFAST" (1971)''')],

        [('I', 'blue border, yellow background, blue stripe (1972-74)'),
         ('illustration', [
             ('A', 'racing and sports cars type 1 (with drag parachute)'),
             ('B', 'racing and sports cars type 2 (with checkered flag)'),
             ('C', 'trucks and construction vehicles'),
             ('D', 'no illustration, no border, white background, black text')]),
         ('additional text', [
             ('A', '"SUPERFAST"'),
             ('B', '"Rola-matics"')]),
         ('corners', [
             ('A', 'angled'),
             ('B', 'rounded')]),
         ('color of stamped model numbers, names and "Rola-matics"', [
             ('A', 'black'),
             ('B', 'orange-red'),
             ('C', 'none')]),
         ('color of printed illustration and lettering on backpage', [
             ('A', 'blue "Matchbox" Collectors Club, Woodridge, NJ'),
             ('B', 'black and red "Matchbox" Collectors Club, Woodridge, NJ'),
             ('C', 'black and red "Superfast"; Lesney Products Corporation, Moonachie, NJ'),
             ('D', 'blue "Superfast"; Lesney Products Corporation, Moonachie, NJ')])],

        [('J', 'yellow background, "MATCHBOX" in oval (1975-79)'),
         ('format', [
             ('A', 'blue border'),
             ('B', 'light blue and white border'),
             ('C', 'blue and white border')]),
         ('illustration and color of lettering', [
             ('A', '"Superfast" in light blue, MB63 Tanker, MB62 Renault 17 TL & MB48 Pi-eyed Piper'),
             ('B', '"Superfast" in blue, MB63 Tanker, MB62 Renault 17 TL & MB48 Pi-eyed Piper'),
             ('C', '"Rola-matics", MB47 Beach Hopper, MB16 Badger & MB67 Hot Rocker'),
             ('D', '"Streakers", MB66 Mazda RX 500 & MB41 Siva Spyder')]),
         ('text on top', [
             ('A', 'white on blue'),
             ('B', 'white on light blue'),
             ('C', 'black on yellow'),
             ('D', 'black on blue and yellow'),
             ('E', 'black on light blue')]),
         ('backpage', [
             ('A', 'blue illustration and lettering'),
             ('B', 'black and red illustration and lettering')])],

        [('L', 'red border, yellow background, "MATCHBOX" in oval (1980-82)'),
         ('illustration', [
             ('A', 'Chevrolet Corvette'),
             ('B', 'Peterbilt truck'),
             ('C', 'Jeep'),
             ('D', '"LONDON HOLIDAY"')]),
         ('additional text', [
             ('A', 'none'),
             ('B', '"LIMITED EDITION MODELS"')]),
         ('lower corners', [
             ('A', 'angled'),
             ('B', 'rounded')])],

        [('M', 'orange and yellow with red grid (1983-88)'),
         ('format', [
             ('A', 'black border, "The Original Collectibles", made in England, China, or Macao (1983-85)'),
             ('B', 'no black border, "THE AUTOMOTIVE SUPERSTARS", made in China, Macao, or China and Macao (1986-88)')]),
         ('lettering', [
             ('A', 'name of model printed'),
             ('B', 'name of model printed on white background'),
             ('C', 'no model name')]),
         ('additional text', [
             ('A', 'none'),
             ('B', '"MOVING PARTS"'),
             ('C', '"NEW COLOR SCHEME"'),
             ('D', '"NEW MODEL"')]),
         ('backpage', [
             ('A', 'multicolored picture on orange background'),
             ('B', 'variable black illustration and lettering on white background'),
             ('C', 'variable black illustration and lettering on gray background')]),
         'regional issues in similar style: Canada B, China B'],

        [('N', 'orange and yellow with red grid, number in wheel (1989-93)'),
         ('additional text', [
             ('A', 'none'),
             ('B', '"MOVING PARTS" red on yellow'),
             ('C', '"NEW COLOR" yellow on red'),
             ('D', '"NEW MODEL" yellow on dark blue'),
             ('E', '"NEW MODEL" yellow on light blue')]),
         ('text in upper left corner', [
             ('A', '"DIE-CAST METAL"'),
             ('B', '"LIGHTNING RACER OFFER"')]),
         ('color', [
             ('A', '"MATCHBOX" red'),
             ('B', '"MATCHBOX" black')]),
         'regional issues in similar style: Canada C, China C'],

        [('O', 'orange and yellow, "GET IN THE FAST LANE" (1994-96)'),
         ('additional text', [
             ('A', 'none'),
             ('B', '"MOVING PARTS" yellow (1994-95)'),
             ('C', '"NEW COLOR" yellow (1994-95)'),
             ('D', '"NEW MODEL" yellow (1994-95)'),
             ('E', '"MOVING PARTS" red (1996)'),
             ('F', '"NEW LOOK" red (1996)'),
             ('G', '"NEW MODEL" red (1996)')]),
         ('text in upper left corner', [
             ('A', 'none'),
             ('B', '"SUPERFAST"'),
             ('C', '"WARNING - CHOKING HAZARD"')]),
         ('text under model', [
             ('A', 'none'),
             ('B', '"As seen on the Viper TV show" (Dodge Viper model only)'),
             ('C', '"Warning: This set contains small parts ..."')]),
         'regional issues in similar style: Brazil, China D'],

        [('P', 'orange and yellow with number in yellow rectangle (1997)'),
         ('text beside model name', [
             ('A', 'none'),
             ('B', '"MOVING PARTS!" white on red'),
             ('C', '"NEW LOOK!" white on red'),
             ('D', '"NEW LOOK! white on orange'),
             ('E', '"NEW MODEL! " white on red'),
             ('F', '"NEW MODEL 1997" white on red'),
             ('G', '"NEW MODEL 1997" white on orange')]),
         ('text in upper left corner', [
             ('A', 'none'),
             ('B', '"Warning - Choking Hazard"')]),
         ('text above model name', [
             ('A', 'none'),
             ('B', '"SUPERFAST"')])],

        [('Q', 'orange and white with Ford Explorer depicted and sub-series logo (1998-2000)', [
         'model name in differently colored stripe according to sub-series']),
         ('format', [
             ('A', 'no "Mattel Wheels" at bottom, standing Ford Explorer, "of 75 vehicles" below number (early 1998)'),
             ('B', '"Mattel Wheels" at bottom, moving Ford Explorer, "of 75 vehicles" below number (late 1998)'),
             ('C', '"Mattel Wheels" at bottom, moving Ford Explorer, "of 100 vehicles" below number (1999-2000)'),
             ('D', 'Explorer replaced with picture of model, number next to model name, "Mattel Wheels" at bottom '
                   '(1998 limited)')]),
         ('text beside model name', [
             ('A', 'none'),
             ('B', '"MOVING PARTS!" black'),
             ('C', '"NEW DECO!" black'),
             ('D', '"NEW MODEL!" black')]),
         ('text in upper left corner', [
             ('A', '"Guaranteed for life"'),
             ('B', '"Warning - Choking Hazard"'),
             ('C', '"Chevrolet"'),
             ('D', '"Ford Motor Company"'),
             ('E', '"FRANCE 98" logo (Opel Calibra ITC only)')]),
         ('text under model name', [
             ('A', 'none'),
             ('B', '"First Edition"')])],

        [('R', 'dark orange and white with generic fire engine depicted and new oval Matchbox logo (2000-2002)', [
         'sub-series name right of model name in differently colored field',
         'Mattel Wheels" at bottom']),
         ('format', [
             ('A', 'number "of 100" in upper right corner, fire engine grille without Matchbox logo (late 2000)'),
             ('B', 'number "of 75" in upper right corner, fire engine grille without Matchbox logo (2001)'),
             ('C', 'number "of 75" in upper right corner, fire engine grille with Matchbox logo, '
                   'additional "50" logo in upper left corner (2002)'),
             ('D', 'number "of 75" in upper right corner, fire engine grille with Matchbox logo, '
                   'no "50" logo (late 2002)')]),
         ('text in upper left corner', [
             ('A', 'none'),
             ('B', '"Warning - Choking Hazard" ("50" logo if present moved to the right below Matchbox logo)')]),
         'Note: For 2003 the US market received the same international blisterpack design as other American countries.'],

        [('S', 'orange with new Matchbox logo, black and white curved stripe along left side'),
         ('main logo on card', [
             ('A', '"HERO CITY", "COLLECTION - COLECCION"'),
             ('B', '"HERO CITY", "COLLECTION - COLECCION" with choking hazard warning'),
             ('C', '"BONUS PRIZE INSIDE!"'),
             ('D', '"TREASURE INSIDE!"'),
             ('E', 'Matchbox logo only')]),
         ('model name and number', [
             ('A', 'no name, number in upper right corner with sub-series logo'),
             ('B', 'in yellow banner over model'),
             ('C', 'along right side next to model')]),
         ('graphic behind model', [
             ('A', 'rectangular white space'),
             ('B', 'cityscape with sunburst'),
             ('C', 'smudgy white space'),
             ('D', 'orange background')])],

        [('T', 'orange and yellow with older Matchbox logo (late 2005 on)', [
         'purple rectangle, "READY FOR ACTION", "MBX METAL"',
         'black and white curved stripe on left side']),
         ('drawing on vehicle(s) on card', [
             ('A', 'big-wheel SUV'),
             ('B', 'dump truck, convertible, SUV')]),
         ('model name and number', [
             ('A', 'number written vertically on right side of card'),
             ('B', 'number written horizontally on right side of card')])],
    ]],

    ['CA', 'Canadian Standard Packs 1978-1997', [
        [('J', 'white border, "MATCHBOX" in oval (1978-82)', [
         'similar to European J type, but with different illustration and both English and French lettering',
         'illustration shows a red & white truck and a blue sports car']),
         ('additional text', [
             ('A', '"Printed and made in England - Imprime et Fabrique en Angleterre"'),
             ('B', 'none')])],

        [('M', 'orange and yellow with red grid (1983-88)', [
         'similar to US M type, but with both English and French lettering']),
         ('addional text and illustration in upper right corner', [
             ('A', '"Irwin Toy"'),
             ('B', '"IRWIN"'),
             ('C', '"Charan Toy"')])],

        [('N', 'orange and yellow with red grid, number in wheel (1989-93)', [
         'similar to US N type, but with both English and French lettering'])],

        [('O', 'orange and yellow, "GET IN THE FAST LANE" (1994-96)', [
         'similar to US O type, but with both English and French lettering'])],

        [('P', 'orange and yellow with number in yellow rectangle (1997)', [
         'similar to US P type, but with both English and French lettering',
         'Note: After 1997 the Canadian market received the same international blisterpack design as other American '
         'countries except the USA.'])]
    ]],

    ['INT', 'International Standard Packs since 1998', [
        [('Q', 'orange and white with Ford Explorer depicted and sub-series logo (1998-2000)'),
         'similar to US Q type, but with lettering in English, French, Spanish and Portuguese',
         'no "of xx vehicles" below number'],

        [('R', 'dark orange and white with generic fire engine depicted and new oval Matchbox logo (2000-2002)'),
         'similar to US R type, but with lettering in English, French, Spanish and Portuguese',
         'no "vehicle - of" above and below number'],

        [('S', 'dark orange and white with Matchbox Hero City logo (since 2002)'),
         'lettering in up to seven languages']]],

    ['BR', 'Brazil Regional', [
        [('O', 'type - orange and yellow, "GET IN THE FAST LANE" (1994-96)'),
         'identical to US O type, but with Portuguese labels']]],

    ['BG', 'Bulgaria Regional', [
        [('A', 'blue with yellow arrow (1983-90)')],
        [('B', 'white with blue grid (1991-96)')],
        [('C', 'orange and yellow with Fast Lane logo (since 1997)'),
         'similar to European O type, but without number and model name']]],

    ['CN', 'China Regional', [
        [('A', 'blue with yellow & red stripe (1986-87)', [
         'similar to European M type, but with Chinese lettering']),
         ('illustration', [
             ('A', 'group of models in stripes type 1'),
             ('B', 'group of models in stripes type 2'),
             ('C', 'no models in stripes')])],
        [('B', 'orange and yellow with red grid (1988)', [
         'similar to US M type, but with Chinese lettering'])],
        [('C', 'orange and yellow with red grid, number in wheel (1989-93)', [
         'identical to US N type, but with white labels on blister card']),
         ('with small paper labels with "Matchbox" and Chinese lettering inside of blister', [
             ('A', 'yes'),
             ('B', 'no')])],
        [('D', 'orange and yellow, "GET IN THE FAST LANE" (1994-96)'),
         'identical to US O type, but with Chinese labels']]],

    ['FR', 'France Regional', [
        [('A', 'plinth with orange border (1979-81)'),
         'scheduled for all of Europe, but issued only in France']]],

    ['HU', 'Hungary Regional', [
        [('A', 'blue with white grid, yellow background (1987-88)')],
        [('B', 'blue with car illustrations, yellow background (1987-88)'),
         'cars illustrated: Dacia 1300, Skoda 120, Lada Niva, Zastava 1100']]],

    ['JP', 'Japan Regional', [
        [('A', 'red border, yellow background, "MATCHBOX" with wheel (1971-73)'),
         ('illustration', [
             ('A', 'generic white & red sports car and blue sedan'),
             ('B', 'generic truck')])],

        [('B', 'white border, "MATCHBOX" (Japanese) in oval (1977-79)', [
         'similar to European J type, but with different illustrations and Japanese lettering']),
         ('illustration', [
             ('A', 'MB45 BMW 3.0 CSL, MB51 Citroen SM, MB17 The Londoner'),
             ('B', 'MB36 Formula 5000, MB56 Hi-Tailer, MB27 Lamborghini Countach')])],

        [('C', 'blue with yellow & red stripe (1984-87)'),
         'similar to European M type, but stripe goes in opposite direction']]],

    ['CH', 'Switzerland Regional', [
        [('A', 'white with red grid, "Swiss Collection" (1989-90)')],
        [('B', 'silver with yellow, red & blue stripe (1991)')]]],
]

other = [
    ('special', 'Special Packs (for standard models)', [
        ('spect', 'Spec T (USA 1968)'),
        ('brroomstick', 'Brroomstick (1970)'),
        ('zingo', 'Zingomatic (1970)'),
        ('specialusa', 'Special USA (F 1984)'),
        ('highriders', 'High Riders (1985-86)'),
        ('cardriver', 'Car and Driver (1990)'),
        ('freewheel', 'Die Cast Metal - Free Wheel Action (USA 1992)'),
        ('vending', 'Vending machine packs (USA 1998)'),
    ]),

    ('promo', 'Packs for Promotional Models', [
        ('jubilee', 'Silver Jubilee Bus (1977)'),
        ('pauls', 'Pauls (GB 1984)'),
        ('bp', 'BP (NL 1987)'),
        ('unichem', 'UniChem (GB 1987)'),
        ('whiterose', 'White Rose Collectibles (various, USA 1990-97)'),
        ('belgomine', 'Belgomine - Avia (B 1993)'),
        ('burnfoundation', 'Burnfoundation (USA 1994)'),
        ('nutmeg', 'Nutmeg Collectibles (USA 1995)'),
        ('caviper', 'California Viper Owners (USA 1995)'),
        ('mitre10', 'Mitre 10 (NZ 1995)'),
        ('shenandoah', 'Shenandoah Apple Blossom Festival (USA 1996-99)'),
        ('viewmaster', 'ViewMaster (USA 1996)'),
        ('patsycline', 'Patsy Cline (USA 1996)'),
        ('fredmeyer', 'Fred Meyer (USA 1997)'),
        ('', 'Taco Bell (USA 1998-99)', [
            ('tacobell1', '1998'),
            ('tacobell2', '1999')]),
        ('whites', "White's Guide (USA 1999)"),
        ('copamustang', 'Copa Mustang (MEX 1999)'),
        ('target', 'Target Glitter Bug (USA 2000)'),
        ('aalracing', 'AAL Racing (USA 2001)'),
        ('hilti', 'Hilti (USA 2001)'),
        ('liberty', 'Jeep Liberty Limited Edition (USA 2001)'),
        ('911emergency', '911 Emergency (USA 2001)'),
        ('76ers', '76ers on Fire (USA 2002)'),
        ('mdm', 'MDM Special Edition (USA 2002)'),
        ('nybday', 'New York Birthday Party Special Edition (USA 2002)'),
        ('dunbar', 'Dunbar Armored (USA 2003)'),
    ]),

    ('spinoff', 'Packs for Spin-off Ranges', [
        ('codered', 'Code Red (USA 1982)'),
        ('superfast', 'Superfast (USA 1986-91)'),
        ('supergt', 'Super GT (1986-89)'),
        ('dinky', 'Dinky (GB 1987)'),
        ('roadblasters', 'Roadblasters / Motor Lords (1987-88)'),
        ('laserwheels', 'Laser Wheels (1987-91)'),
        ('colorchangers', 'Color Changers (1989)'),
        ('commando', 'Commando (1989-90)'),
        ('', 'World Class (1989-95)', [
            ('worldclass1', 'A - red with gold grid'),
            ('worldclass2', 'B - yellow and orange')]),
        ('daysofthunder', 'Days of Thunder (USA 1990-91)'),
        ('lasertronic', 'Lasertronic (1990-91)'),
        ('sirenforce', 'Siren Force  (1990-91)'),
        ('rescue911', 'Rescue 911 (1990-91)'),
        ('actionpack', 'Action Pack (USA 1991)'),
        ('lightning', 'Lightning (1991-92)'),
        ('indy500', 'Indy (USA 1991-93)'),
        ('tripleheat', 'Triple Heat (USA 1992)'),
        ('hotstocks', 'Hot Stocks (USA 1992)'),
        ('harleydavidson', 'Harley-Davidson (1992-96)'),
        ('originals', 'Matchbox Originals (1992-96)'),
        ('supertrucks', 'Super Trucks (USA 1993)'),
        ('formula1', 'Formula 1 (1994-97)'),
        ('proracers', 'Looney Tunes Pro Racers (USA 1995)'),
        ('matchcaps', 'Matchcaps (USA 1995)'),
        ('', 'Premiere Collection (1996-99)', [
            ('premiere1', 'A - yellow and orange border'),
            ('premiere2', 'B - orange border'),
            ('premiere3', 'C - orange border with base under box')]),
        ('lightsound', 'Light & Sound (1996-98)'),
        ('challenge', '75 Challenge (USA 1996-98)'),
        ('starcar', 'Star Cars (USA 1998-99)'),
        ('nba', 'NBA Collection (USA 1998-99)'),
        ('collectibles', 'Matchbox Collectibles (USA since 2000)'),
        ('dare', 'D.A.R.E. (USA 2001)'),
        ('acrossamer', 'Across America (USA 2002)'),
        ('birthdayhunt', 'Birthday Hunt (CDN/MEX 2002)'),
    ]),
]
