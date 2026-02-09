def process(items):
    for i, x in enumerate(items):
        if x < 0:
            raise ValueError(f"Negative value at index {i}")
        print(i, x)

process([1, 2, 3, -1, 5])


"""
➜ python -m pdb pdb-condition.py
> pdb-condition.py(1)<module>()
-> def process(items):
(Pdb) ll
  1  ->	def process(items):
  2  	    for i, x in enumerate(items):
  3  	        if x < 0:
  4  	            raise ValueError(f"Negative value at index {i}")
  5  	        print(i, x)
  6  	
  7  	process([1, 2, 3, -1, 5])

(Pdb) b 3, x<0
Breakpoint 1 at pdb-condition.py:3

(Pdb) ll
  1  ->	def process(items):
  2  	    for i, x in enumerate(items):
  3 B	        if x < 0:
  4  	            raise ValueError(f"Negative value at index {i}")
  5  	        print(i, x)
  6  	
  7  	process([1, 2, 3, -1, 5])

(Pdb) c
0 1
1 2
2 3
> pdb-condition.py(3)process()
-> if x < 0:

(Pdb) p x
-1

(Pdb) args
items = [1, 2, 3, -1, 5]

(Pdb) 

"""