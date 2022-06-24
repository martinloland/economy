from economy import Economy

econ = Economy('./forbruk/bruk.csv', 'nordea')
econ.categories_from_file('categories.txt')
econ.calculate()
econ.print_results()
econ.print_uncat()
