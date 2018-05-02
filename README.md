# economy
Calculates your monthly money consumption in categories based on card use

## Example use

```python
from economy import Economy

econ = Economy('forbruk.csv')
econ.add_cat(
    'mat',
    ['rema', 'bunnpris', 'coop', 'meny', 'kiwi', 'obs'])
econ.add_cat(
    'transport',
    ['flybussen', 'nsb', 'taxi', 'ruter', 'flytoget', 'buss', 'atb'])
    
econ.calculate()
econ.print_results()
econ.print_uncat()
```

Or categories can be loaded from file:

```python
from economy import Economy

econ = Economy('forbruk.csv')
econ.categories_from_file('categories.txt')
econ.calculate()
econ.print_results()
econ.print_uncat()
```

**categories.txt**:

```
mat:rema,bunnpris,coop,meny,kiwi,obs
transport:flybussen,nsb,taxi,ruter,flytoget,buss,atb
```

## Example output

```
Money coverage: 0.93
Monthly average:

mat             -2949
ferie           -1566
fritid          -1459
uteliv          -1413
transport       -1298
spleising       -1085
oppussing       -999
klær            -813
sprit           -813
media           -340
gave            -295
husholdning     -287
veldedighet     -268
helse           -176

Total:          -13656


Uncategorized items:

  -1718.00   klarna/internetstores gmb                2017-09-21
   -799.00   trondheim livin haakon vii g trondheim   2017-08-31
   -700.00   atm klaebu sparebank   ter3645           2017-05-05
   -678.80   lovenskiold han fossegrenda  trondheim   2017-09-01
   -648.00   klarna * internetstores g                2017-09-22
```