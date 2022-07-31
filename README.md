Project focus
------------
This project is implementation of one of the popular task in Data Engineer interviews. 

Task:
We have a very large file with numbers.
Need to sort numbers and store to the another single file.
Main restrictions: size of the RAM is very small.
For example, size of the input file equals to 3Gb, available RAM equals to 20Mb.

This task was resolved using [External sorting algo](https://en.wikipedia.org/wiki/External_sorting).

Requirements
------------
* Python >= 3.6.x

Installation
------------
```shell
git clone 
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
