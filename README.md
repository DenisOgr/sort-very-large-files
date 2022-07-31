Project focus
------------
This project implements one of the prevalent tasks in Data Engineer interviews. 

Task:
We have a very large file with numbers.
Need to sort numbers and store another single file.
Main restrictions: the size of the RAM is very small.
For example, the size of the input file equals to 3Gb, available RAM equals to 20Mb.

This task was resolved using [External sorting algo](https://en.wikipedia.org/wiki/External_sorting).

Results
------------
This application was tested using a 3Gb input file and 20Mb of memory limits. 
It takes 10 minutes for sorting file.
With 100 Mb of memory limits, it takes ~ 3min.


Requirements
------------
* Python >= 3.6.x

Installation
------------
```shell
git clone git@github.com:DenisOgr/sort-very-large-files.git
```

Run
------------
1. Put large file to directory data/input. This file should consist of numbers divided by newstring (\n)
For example:
```
123
321
321
12
3
4
```
2. Run command:
```shell
python main filename --mem_limit 20
```


