# example test cases
test_cases = [
   {
        "test_case_number": 1,
        "user_request": "Origin: Oslo, NO | Destination: Riga | Departure: October, any Friday | Duration: 2 nights",
        "selectedCityID": "oslo_no",
        "cabinClass": "economy",
        "travelers": {"adults": 1, "children": 0, "infants": 0}
    },
    {
        "test_case_number": 2,
        "user_request": "Origin: Stockholm, SE | Destination: Frankfurt | Departure: October 12th | Return: October 15th",
        "selectedCityID": "stockholm_se",
        "cabinClass": "economy",
        "travelers": {"adults": 1, "children": 0, "infants": 0}
    },
    {
        "test_case_number": 3,
        "user_request": "Origin: Copenhagen, DK | Destination: Best surfing spots in Portugal | Departure: Spring 2024 | Duration: 1 week",
        "selectedCityID": "copenhagen_dk",
        "cabinClass": "economy",
        "travelers": {"adults": 1, "children": 0, "infants": 0}
    },
    {
        "test_case_number": 4,
        "user_request": "Origin: Amsterdam, NL | Destination: Valencia, Spain | Departure: 1st September | Return: 7th September | Passengers: 2 adults",
        "selectedCityID": "amsterdam_nl",
        "cabinClass": "economy",
        "travelers": {"adults": 2, "children": 0, "infants": 0}
    },
    {
        "test_case_number": 5,
        "user_request": "Origin: Brussels, BE | Destination: Casablanca, Morocco | Departure: September 7th | Return: September 23rd | Passengers: 3 adults",
        "selectedCityID": "brussels_be",
        "cabinClass": "economy",
        "travelers": {"adults": 3, "children": 0, "infants": 0}
    },
    {
        "test_case_number": 6,
        "user_request": "Origin: Dublin, IE | Destination: East Coast US (Boston/Washington D.C.) | Departure: September-October | Duration: 12-16 days",
        "selectedCityID": "dublin_ie",
        "cabinClass": "economy",
        "travelers": {"adults": 1, "children": 0, "infants": 0}
    },
    {
        "test_case_number": 7,
        "user_request": "Origin: Paris, FR | Destination: Greek Isles | Departure: Flexible | Duration: 7-12 days",
        "selectedCityID": "paris_fr",
        "cabinClass": "economy",
        "travelers": {"adults": 1, "children": 0, "infants": 0}
    },
    {
        "test_case_number": 8,
        "user_request": "Origin: Berlin, DE | Destination: Tropical destination in Asia | Departure: Mid-November to December | Duration: Approx. 10 nights",
        "selectedCityID": "berlin_de",
        "cabinClass": "economy",
        "travelers": {"adults": 1, "children": 0, "infants": 0}
    },
    {
        "test_case_number": 9,
        "user_request": "Origin: Tampere, FI | Destination: City in Eastern Europe | Departure: Evening | Duration: 2 nights | Occasion: Bachelors party",
        "selectedCityID": "tampere_fi",
        "cabinClass": "economy",
        "travelers": {"adults": 1, "children": 0, "infants": 0}
    },
    {
        "test_case_number": 10,
        "user_request": "Origin: Madrid, ES | Destination: Tropical snorkeling destination | Departure: Before Summer 2024 | Duration: Approx. 1 week",
        "selectedCityID": "madrid_es",
        "cabinClass": "economy",
        "travelers": {"adults": 1, "children": 0, "infants": 0}
    },
    # test cases 2
    {
        "test_case_number": 11,
        "user_request": "Origin: Helsinki, FI | Destination: Lapland, FI | Departure: December 24th | Duration: 7 days | Occasion: Christmas holidays",
        "selectedCityID": "helsinki_fi",
        "cabinClass": "economy",
        "travelers": {"adults": 2, "children": 2, "infants": 1}
    },
    {
        "test_case_number": 12,
        "user_request": "Origin: Rome, IT | Destination: Tokyo, Japan | Departure: Spring 2024 | Duration: 3 weeks",
        "selectedCityID": "rome_it",
        "cabinClass": "economy",
        "travelers": {"adults": 1, "children": 0, "infants": 0}
    },
    {
        "test_case_number": 13,
        "user_request": "Origin: Warsaw, PL | Destination: New York, US | Departure: Any Wednesday of September | Duration: 5 nights",
        "selectedCityID": "warsaw_pl",
        "cabinClass": "economy",
        "travelers": {"adults": 2, "children": 0, "infants": 0}
    },
    {
        "test_case_number": 14,
        "user_request": "Origin: London, GB | Destination: Sydney, AU | Departure: Mid-February | Duration: 14 days",
        "selectedCityID": "london_gb",
        "cabinClass": "economy",
        "travelers": {"adults": 1, "children": 1, "infants": 0}
    },
    {
        "test_case_number": 15,
        "user_request": "Origin: Vienna, AT | Destination: Bangkok, Thailand | Departure: October 1st | Duration: 10 nights",
        "selectedCityID": "vienna_at",
        "cabinClass": "economy",
        "travelers": {"adults": 1, "children": 0, "infants": 0}
    },
    {
        "test_case_number": 16,
        "user_request": "Origin: Vienna, AT | Destination: Helsinki, FI | Departure: Early November | Duration: 7 nights",
        "selectedCityID": "vienna_at",
        "cabinClass": "economy",
        "travelers": {"adults": 0, "children": 1, "infants": 0}
    },
    {
        "test_case_number": 17,
        "user_request": "Origin: Lisbon, PT | Destination: Rio de Janeiro, Brazil | Departure: Carnival season | Duration: 5 days",
        "selectedCityID": "lisbon_pt",
        "cabinClass": "economy",
        "travelers": {"adults": 2, "children": 0, "infants": 0}
    },
    {
        "test_case_number": 18,
        "user_request": "Origin: Zurich, CH | Destination: Mount Everest Base Camp, Nepal | Departure: April 5th | Duration: 15 days | Occasion: Trekking",
        "selectedCityID": "zurich_ch",
        "cabinClass": "economy",
        "travelers": {"adults": 1, "children": 0, "infants": 0}
    },
    {
        "test_case_number": 19,
        "user_request": "Origin: Oslo, NO | Destination: Maldives | Departure: Honeymoon in June | Duration: 7 nights",
        "selectedCityID": "oslo_no",
        "cabinClass": "economy",
        "travelers": {"adults": 2, "children": 0, "infants": 0}
    },
    {
        "test_case_number": 20,
        "user_request": "Origin: Budapest, HU | Destination: Milan, IT | Departure: First week of March | Duration: 4 days | Occasion: Fashion week",
        "selectedCityID": "budapest_hu",
        "cabinClass": "business",
        "travelers": {"adults": 1, "children": 0, "infants": 0}
    },
    {
        "test_case_number": 21,
        "user_request": "Origin: Athens, GR | Destination: Bali, Indonesia | Departure: September 5th | Duration: 12 days",
        "selectedCityID": "athens_gr",
        "cabinClass": "economy",
        "travelers": {"adults": 2, "children": 1, "infants": 1}
    },
    {
        "test_case_number": 22,
        "user_request": "Origin: Prague, CZ | Destination: Shanghai, China | Departure: Spring 2024 | Duration: 10 days",
        "selectedCityID": "prague_cz",
        "cabinClass": "economy",
        "travelers": {"adults": 1, "children": 1, "infants": 0}
    },
    {
        "test_case_number": 23,
        "user_request": "Origin: Edinburgh, GB | Destination: African Safari | Departure: Summer 2024 | Duration: 2 weeks",
        "selectedCityID": "edinburgh_gb",
        "cabinClass": "premium_economy",
        "travelers": {"adults": 2, "children": 1, "infants": 0}
    },
    {
        "test_case_number": 24,
        "user_request": "Origin: Moscow, RU | Destination: Santa's Village, FI | Departure: December 24th | Duration: 3 days",
        "selectedCityID": "moscow_ru",
        "cabinClass": "business",
        "travelers": {"adults": 2, "children": 2, "infants": 0}
    },
    {
        "test_case_number": 25,
        "user_request": "Origin: Barcelona, ES | Destination: Tokyo Disneyland, Japan | Departure: Summer holidays | Duration: 10 days",
        "selectedCityID": "barcelona_es",
        "cabinClass": "economy",
        "travelers": {"adults": 2, "children": 2, "infants": 1}
    },
    {
        "test_case_number": 26,
        "user_request": "Origin: Belgrade, RS | Destination: Caribbean Cruises | Departure: Any time in 2024 | Duration: 15 days",
        "selectedCityID": "belgrade_rs",
        "cabinClass": "economy",
        "travelers": {"adults": 2, "children": 0, "infants": 0}
    },
    { 
        "test_case_number": 27,
        "user_request": "Origin: Riga, LV | Destination: Best wine regions in France | Departure: Autumn 2024 | Duration: 1 week", 
        "selectedCityID": "riga_lv", 
        "cabinClass": "economy", 
        "travelers": {"adults": 2, "children": 0, "infants": 0} 
    }, 
    { 
        "test_case_number": 28,
        "user_request": "Origin: Kiev, UA | Destination: Goa, India | Departure: New Year's Eve | Duration: 7 days", 
        "selectedCityID": "kiev_ua", 
        "cabinClass": "economy",
        "travelers": {"adults": 2, "children": 1, "infants": 1} 
    }, 
    { 
        "test_case_number": 29,
        "user_request": "Origin: Bucharest, RO | Destination: Major US cities | Departure: Summer 2024 | Duration: 20 days", 
        "selectedCityID": "bucharest_ro", 
        "cabinClass": "economy", 
        "travelers": {"adults": 1, "children": 0, "infants": 0} 
    }, 
    { 
        "test_case_number": 30,
        "user_request": "Origin: Sofia, BG | Destination: Ancient ruins in Peru | Departure: May 2024 | Duration: 15 days", 
        "selectedCityID": "sofia_bg", 
        "cabinClass": "economy", 
        "travelers": {"adults": 1, "children": 1, "infants": 0} 
    },
    # test cases 3
    { 
        "test_case_number": 31,
        "user_request": "Origin: Rome, IT | Destination: South of France | Departure: Anytime in July | Length: A weekend", 
        "selectedCityID": "rome_it", 
        "cabinClass": "economy", 
        "travelers": {"adults": 2, "children": 0, "infants": 0} 
    },
    { 
        "test_case_number": 32,
        "user_request": "From: Warsaw, PL | I want to explore: Beaches in Croatia or Greece | Departure: During summer holidays | Duration: 5 to 7 days | Passengers: Me and my partner", 
        "selectedCityID": "warsaw_pl", 
        "cabinClass": "economy", 
        "travelers": {"adults": 2, "children": 0, "infants": 0} 
    },
     { 
        "test_case_number": 33,
        "user_request": "Origin: Prague, CZ | Destination: Thailand | When: January or February | Stay: Roughly 2 weeks | Class: Business class please", 
        "selectedCityID": "prague_cz", 
        "cabinClass": "economy", 
        "travelers": {"adults": 1, "children": 0, "infants": 0} 
    },
    # This crashed the whole program
    #{ 
    #    "test_case_number": 33,
    #    "user_request": "Origin: Prague, CZ | Destination: Islands in Thailand | When: January or February | Stay: Roughly 2 weeks | Class: Business class please", 
    #    "selectedCityID": "prague_cz", 
    #    "cabinClass": "economy", 
    #    "travelers": {"adults": 1, "children": 0, "infants": 0} 
    #},
    { 
        "test_case_number": 34,
        "user_request": "Origin: Budapest, HU | Want to go to: Ski resorts in Switzerland or Austria | Travel dates: Any February weekend | Also, need space for my ski equipment", 
        "selectedCityID": "budapest_hu", 
        "cabinClass": "economy", 
        "travelers": {"adults": 1, "children": 0, "infants": 0} 
    },
    { 
        "test_case_number": 35,
        "user_request": "From: Vienna, AT | Destination: Spain but not the touristy parts | Preferably in: May | Duration: Around a week | We're a family of 4", 
        "selectedCityID": "vienna_at", 
        "cabinClass": "economy", 
        "travelers": {"adults": 2, "children": 2, "infants": 0} 
    },
    { 
        "test_case_number": 36,
        "user_request": "Origin: Helsinki, FI | Interested in: Bali or other Indonesian islands | Departure: When it's sunny | Trip length: 10-15 days | Prefer vegetarian meal options", 
        "selectedCityID": "helsinki_fi", 
        "cabinClass": "economy", 
        "travelers": {"adults": 1, "children": 0, "infants": 0} 
    },
    { 
        "test_case_number": 37,
        "user_request": "Origin: Reykjavik, IS | Destination: Any city in Arizona or New Mexico | Departure: March-April | Stay: 7-10 days", 
        "selectedCityID": "reykjavik_is", 
        "cabinClass": "economy", 
        "travelers": {"adults": 1, "children": 0, "infants": 0} 
    },
    { 
        "test_case_number": 38,
        "user_request": "From: Lisbon, PT | Destination: East Asian cities, considering Seoul or Tokyo | Leaving: June | Trip time: 9-11 days | We are 2 adults and 1 infant", 
        "selectedCityID": "lisbon_pt", 
        "cabinClass": "economy", 
        "travelers": {"adults": 2, "children": 0, "infants": 1} 
    },
    { 
        "test_case_number": 39,
        "user_request": "Origin: Athens, GR | I'd like to visit: Japan | Prefer traveling in: Cherry blossom season | Length of trip: 2 weeks max | Also, need WiFi on flight", 
        "selectedCityID": "athens_gr", 
        "cabinClass": "economy", 
        "travelers": {"adults": 1, "children": 0, "infants": 0} 
    },
    { 
        "test_case_number": 40,
        "user_request": "Origin: Sofia, BG | Destination: Adventure spots like Nepal or Peru | When: Before winter | Duration: Not sure, maybe 10 days? | Need to carry camping gear", 
        "selectedCityID": "sofia_bg", 
        "cabinClass": "economy", 
        "travelers": {"adults": 1, "children": 0, "infants": 0} 
    },
    { 
        "test_case_number": 41,
        "user_request": "From: Bratislava, SK | Destination: Australia's east coast | Departure: Avoid local holidays | Stay: A fortnight | Flying: Economy class", 
        "selectedCityID": "bratislava_sk", 
        "cabinClass": "economy", 
        "travelers": {"adults": 1, "children": 0, "infants": 0} 
    },
    { 
        "test_case_number": 42,
        "user_request": "Origin: Vilnius, LT | Destination: African countries for safari, like Kenya or Tanzania | Thinking of traveling in: August | Trip length: Roughly a week | Passengers: It's just me", 
        "selectedCityID": "vilnius_lt", 
        "cabinClass": "economy", 
        "travelers": {"adults": 1, "children": 0, "infants": 0} 
    },
    { 
        "test_case_number": 43,
        "user_request": "Origin: Riga, LV | Destination: London, UK or Dublin, IE | Preferably in: September | Duration: 5 nights", 
        "selectedCityID": "riga_lv", 
        "cabinClass": "economy", 
        "travelers": {"adults": 1, "children": 0, "infants": 0} 
    },
    { 
        "test_case_number": 44,
        "user_request": "From: Tallinn, EE | Interested in: Vietnam or Malaysia | Departure: Avoiding rainy seasons | Stay: 10 days maximum | Also, a window seat please", 
        "selectedCityID": "tallinn_ee", 
        "cabinClass": "economy", 
        "travelers": {"adults": 1, "children": 0, "infants": 0} 
    },
    { 
        "test_case_number": 45,
        "user_request": "Origin: Ljubljana, SI | Destination: Mexico's coastal cities | When: October-November | Length of trip: Around 1 week | No seafood meal preference", 
        "selectedCityID": "ljubljana_si", 
        "cabinClass": "economy", 
        "travelers": {"adults": 1, "children": 0, "infants": 0} 
    },
    { 
        "test_case_number": 46,
        "user_request": "Origin: Zagreb, HR | Destination: South Korea or Taiwan | Thinking of going in: Spring | Trip length: A week | Flying: Premium economy", 
        "selectedCityID": "zagreb_hr", 
        "cabinClass": "economy", 
        "travelers": {"adults": 1, "children": 0, "infants": 0} 
    },
    { 
        "test_case_number": 47,
        "user_request": "From: Belgrade, RS | Destination: Maldives or Seychelles | Best time to travel: Off-peak season | Duration: Not more than a week", 
        "selectedCityID": "belgrade_rs", 
        "cabinClass": "economy", 
        "travelers": {"adults": 1, "children": 0, "infants": 0} 
    },
    { 
        "test_case_number": 48,
        "user_request": "Origin: Sarajevo, BA | Destination: Chile or Argentina | Preferably in: Their dry season | Stay: 10-14 days | We're a group of 5 friends", 
        "selectedCityID": "sarajevo_ba", 
        "cabinClass": "economy", 
        "travelers": {"adults": 5, "children": 0, "infants": 0} 
    },
    { 
        "test_case_number": 49,
        "user_request": "From: Skopje, MK | Destination: New York or Toronto | When: Autumn months | Trip time: 5-7 nights | Class: Business, if there's a deal", 
        "selectedCityID": "skopje_mk", 
        "cabinClass": "economy", 
        "travelers": {"adults": 1, "children": 0, "infants": 0} 
    },
    { 
        "test_case_number": 50,
        "user_request": "Origin: Podgorica, ME | Destination: Moscow or St. Petersburg in Russia | Departure: June-July | Length of trip: Roughly a week | I'm traveling solo", 
        "selectedCityID": "podgorica_me", 
        "cabinClass": "economy", 
        "travelers": {"adults": 1, "children": 0, "infants": 0} 
    },
    { 
        "test_case_number": 51,
        "user_request": "Origin: Helsinki, FI; Destination: Vilna; Departure: October, any Friday; Duration: 2 nights", 
        "selectedCityID": "helsinki_fi", 
        "cabinClass": "economy", 
        "travelers": {"adults": 1, "children": 0, "infants": 0} 
    }
]
