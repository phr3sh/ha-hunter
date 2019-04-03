''' 
Courtesy of your phr3sh neighbor.
This script takes in a file with domain names and
generates all possible homographs
then makes a Whois query to find if the original domain and the homographs have already been registered or not.
Finally, the script writes a file with the results.

Run it like:
python3 hhunter.py target_domains.txt

Where target_domains.txt contains the domains you want to test, one per line.

Problem? github.com/phr3sh/ha-hunter/

'''


import sys
import itertools
import whois

fname=sys.argv[1]

## define the dictionary
d_confusables = {"a" : "а", "b" : "Ь", "c" : "с", "d" : "ԁ", "e" : "е", "h" : "һ", "i" : "і", "j" : "ј", "k" : "ҟ", "l" : "ӏ", "m" : "м", "n" : "п", "o" : "о", "p" : "р", "q" : "ԛ", "r" : "г", "s" : "ѕ", "u" : "џ", "w" : "ԝ", "x" : "х", "y" : "у"}



## read the domain names from the txt file.
with open(fname) as f:
    content = f.readlines()

content = [x.strip() for x in content]

## prepare the writable file for the results
output_path = "homograph_domain_results.txt"
output_file = open(output_path, 'w')

## split the domain name and the tld
for domainname in content:
	domains_registered = []
	domains_unregistered = []
	name, tld = domainname.split('.')
	print("\n \n >>>>>> Processing domain name", domainname, file=output_file)
	name_letters = list(name)
	## identify the indexes of the letters that we can replace found in the dictionary.
	locations = []
	for i in range(len(name_letters)):
		if name_letters[i] in d_confusables:
			locations.append(i)

	#print(locations)
	## count how many letters we can replace and make masks of the appropriate size to give us all combinations
	locations_count = len(locations)
	masks = list(itertools.product([0,1], repeat=locations_count))
#	print(masks)
	print("Generating homographs for", domainname)
	## apply the masks to our locations array to determine the indexes of the characters to be replaced in each run.
	for mask in masks:
		filtered = itertools.compress(locations, mask)
		places = list(filtered)
		#print("The letters of this domain name are\n", name_letters)
		#print("And we will replace the ones at positions\n", places)
		
		replaced_letters = name_letters.copy()
		
		## replace the glyphs in each domain name based on their place in the letters list. Join the list into a string.  
		for symbol in places:
			#print("Symbol", symbol)
			replaced_letters[symbol] = d_confusables.get(name_letters[symbol])
			#print(name_letters)
		#print(type(replaced_letters))
		homograph = ''.join(replaced_letters)

		## Add the tld and then make a whois query of this domain. Catch the 'not found' exception or grab the Registrar.
		homodomain = homograph + "." + tld
		#print("Querying whois for", homodomain)
		try:
			w = whois.whois(homodomain)
		except whois.parser.PywhoisError as e:
			who_message = str(e).split('\n',1)[0]
			domains_unregistered.append(homodomain + ", " + who_message)
		else:
			#print("Found registrar info" w.registrar)
			e_homodomain = homodomain.encode("idna").decode("ascii")
			domains_registered.append(homodomain + " (" + e_homodomain + ") , " + w.registrar)

	## Write write write it to the file file file!
	print("\nDomains Registered=======================================================", file=output_file)
	print('\n'.join(domains_registered), file=output_file)
	print("\nDomains NOT registered===================================================", file=output_file)
	print('\n'.join(domains_unregistered), file=output_file)

output_file.close()