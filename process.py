from economy import Economy

econ = Economy('forbruk.csv')
econ.categories_from_file('categories.txt')
econ.calculate()
econ.print_results()
econ.print_uncat()
