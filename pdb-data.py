def load_data():
    return {"count": "12"}  # BUG: count should be int

def compute_total():
    data = load_data()
    return data["count"] + 5  # TypeError

def main():
    compute_total()

main()

"""
➜ python pdb-data.py 
Traceback (most recent call last):
  File "pdb-data.py", line 11, in <module>
    main()
    ~~~~^^
  File "pdb-data.py", line 9, in main
    compute_total()
    ~~~~~~~~~~~~~^^
  File "pdb-data.py", line 6, in compute_total
    return data["count"] + 5  # TypeError
           ~~~~~~~~~~~~~~^~~
TypeError: can only concatenate str (not "int") to str

➜ python -m pdb -c "b 6" pdb-data.py
Breakpoint 1 at pdb-data.py:6
> pdb-data.py(1)<module>()
-> def load_data():
(Pdb) ll
  1  ->	def load_data():
  2  	    return {"count": "12"}  # BUG: count should be int
  3  	
  4  	def compute_total():
  5  	    data = load_data()
  6 B	    return data["count"] + 5  # TypeError
  7  	
  8  	def main():
  9  	    compute_total()
 10  	
 11  	main()

(Pdb) c
> pdb-data.py(6)compute_total()
-> return data["count"] + 5  # TypeError

(Pdb) p data
{'count': '12'}

(Pdb) type(data['count'])
<class 'str'>

(Pdb) data['count'] = 12

(Pdb) ll
  4  	def compute_total():
  5  	    data = load_data()
  6 B->	    return data["count"] + 5  # TypeError

(Pdb) n
--Return--
> pdb-data.py(6)compute_total()->17
-> return data["count"] + 5  # TypeError

(Pdb) c
The program finished and will be restarted
> pdb-data.py(1)<module>()

(Pdb) q
"""