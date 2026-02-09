def double(x):
   breakpoint()
   return x * 2

val = 3
print(f"{val} * 2 is {double(val)}")

"""
➜ python pdb-breakpoint.py 
> pdb-breakpoint.py(2)double()
-> breakpoint()
(Pdb) ll
  1  	def double(x):
  2  ->	   breakpoint()
  3  	   return x * 2

  (Pdb) n
> pdb-breakpoint.py(3)double()
-> return x * 2

(Pdb) p x
3

(Pdb) q

"""