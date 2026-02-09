import pdb

def double(x):
   pdb.set_trace()
   return x * 2

val = 3
print(f"{val} * 2 is {double(val)}")

"""
➜ python pdb-set_trace.py 
> pdb-set_trace.py(4)double()
-> pdb.set_trace()
(Pdb) ll
  3  	def double(x):
  4  ->	   pdb.set_trace()
  5  	   return x * 2

  (Pdb) p x
3

(Pdb) x * 2
6

(Pdb) c
3 * 2 is 6

"""