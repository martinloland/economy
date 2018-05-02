from economy import Economy

econ = Economy('forbruk.csv')
econ.add_cat(
    'mat',
    ['rema', 'bunnpris', 'coop prix', 'lykke nyborg', 'meny', 'kiwi', 'obs',
     'coop mega', 'ica', 'coop konsum'])
econ.add_cat(
    'fritid',
    ['www coop', 'paypal', 'amazon', 'komplett.no', 'gamezone', 'netonnet',
     'multicom', 'bauhaus', 'biltema', 'elkjøp', 'thepihut',
     'batteriexperten'])
econ.add_cat(
    'oppussing',
    ['staypro', 'maxmaling', 'jula', 'proshop', 'elektroimportoeren',
     'megaflis'])
econ.add_cat(
    'ferie',
    ['norwegian', 'airbnb', 'nabobil', 'vinjerock', 'billettservice',
     'hotell', 'skistar'])
econ.add_cat(
    'sprit',
    ['vinmonopolet', 'duty-free', 'dyty-free', 'systembolaget'])
econ.add_cat(
    'uteliv',
    ['7 - eleven', 'shell', 'kiosk', 'super hero', 'serveringsgjeng', 'kafe',
     'restaurant', 'szechuan', 'quick bar', 'narvesen', 'havnekroa',
     'diskoteket', 'kebab', 'dolly dimple', '7-eleven', 'o learys',
     'lounge/club', 'olavshallen', 'circle k', 'solsiden', 'cafe', 'uka-17',
     'peppes', 'big bite', 'kino', 'nova billett', 'espresso', 'roen bar',
     'yx', 'sushi', 'light pub', 'subway', 'hell grill', 'kaffe',
     'upper crust', 'dattera til hagen', 'prinsen billett', 'tag garderobe',
     "o'learys", 'nordisk film', 'verandan are', 'bar circus', 'pizzabakeren',
     'cowsea'])
econ.add_cat(
    'transport',
    ['flybussen', 'nsb', 'taxi', 'ruter', 'flytoget', 'buss', 'atb',
     'trønderbilene'])
econ.add_cat(
    'media',
    ['telia', 'google', 'curiositystream', 'publications'])
econ.add_cat(
    'veldedighet',
    ['kirkens'])
econ.add_cat(
    'helse',
    ['frisør', 'apotek'])
econ.add_cat(
    'spleising',
    ['vipps'])
econ.add_cat(
    'husholdning',
    ['clas ohl', 'nille', 'kid interiø'])
econ.add_cat(
    'gave',
    ['blomster', 'euroflorist', 'japan photo', 'mcompany', 'jernia'])
econ.add_cat(
    'klær',
    ['xxl', 'g-sport', 'helsport', 'fjellsport', 'anton sport',
     'selected byhaven', 'intersport'])

econ.calculate()
econ.print_results()
econ.print_uncat()
