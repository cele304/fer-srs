#pokreni napisani password manager
chmod +x solution.py



#inicijaliziraj glavnu zaporku, echo - za ispis praznog novog redka
echo 'init masterPassword'
python solution.py init masterPassword
echo



#dodaj lozinke u password manager
echo 'put masterPassword www.fer.unizg.hr NTFmc47kpe'
python solution.py put masterPassword www.fer.unizg.hr NTFmc47kpe
echo

echo 'put masterPassword www.zaba.hr 1234'
python solution.py put masterPassword www.zaba.hr 1234
echo



#dohvati lozinku od www.fer.unizg.hr
echo 'get masterPassword www.fer.unizg.hr'
python solution.py get masterPassword www.fer.unizg.hr
echo

echo 'get masterPassword www.zaba.hr'
python solution.py get masterPassword www.zaba.hr
echo



#završi izvršavanje bash skripte
echo "Uspješan kraj."
read -p "Pritisni Enter za izlaz iz skripte."