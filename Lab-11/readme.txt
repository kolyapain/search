run Biword Indexes from folder "Lab-11" using command 
	python3 Positional_Indexes.py

scripts looking books in "./samples"

change request :

s.search('words /n to *s*e*a*r*c*h*')
word /n - levenstein distance <= n

Note: in lab 4 also can be used * in request

Note 2: BSBI uses memory mapping. I tested it only on Windows 10 Pro x64

Note 3: In lab 5 - BSBI books takes from "./samples" as here

Note 4: To add book, add it in BSBI.reload() function