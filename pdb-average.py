def average(nums):
    total = 0
    for n in nums:
        total += n
    return total / len(nums)

print(average([]))

"""
➜ python pdb-average.py    
Traceback (most recent call last):
  File "pdb-average.py", line 7, in <module>
    print(average([]))
          ~~~~~~~^^^^
  File "pdb-average.py", line 5, in average
    return total / len(nums)
           ~~~~~~^~~~~~~~~~~
ZeroDivisionError: division by zero


➜ python -m pdb pdb-average.py
> pdb-average.py(1)<module>()
-> def average(nums):

(Pdb) n
> pdb-average.py(7)<module>()
-> print(average([]))

(Pdb) s
--Call--
> pdb-average.py(1)average()
-> def average(nums):

(Pdb) ll
  1  ->	def average(nums):
  2  	    total = 0
  3  	    for n in nums:
  4  	        total += n
  5  	    return total / len(nums)

  (Pdb) n
> pdb-average.py(2)average()
-> total = 0

(Pdb) n
> pdb-average.py(3)average()
-> for n in nums:

(Pdb) n
> pdb-average.py(5)average()
-> return total / len(nums)

(Pdb) args
nums = []

(Pdb) nums = [1]

(Pdb) n
--Return--
> pdb-average.py(5)average()->0.0
-> return total / len(nums)

(Pdb) n
0.0
--Return--
> pdb-average.py(7)<module>()->None
-> print(average([]))

(Pdb) q
"""