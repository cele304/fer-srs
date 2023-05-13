#pokreni napisane skripte
chmod +x usermgmt.py
chmod +x login.py


#dodaj korisnike, echo - za ispis praznog novog redka
echo 'python usermgmt.py add korisnik1 - upisi lozinka1'
python usermgmt.py add korisnik1
echo
echo 'python usermgmt.py add korisnik2 - upisi lozinka2'
python usermgmt.py add korisnik2
echo
echo 'python usermgmt.py add korisnik3 - upisi lozinka3'
python usermgmt.py add korisnik3
echo


#promjena lozinke korisnika
echo 'python usermgmt.py passwd korisnik2 - upisi 1qayxsw2'
python usermgmt.py passwd korisnik2
echo

#brisanje korisnika
echo 'python usermgmt.py del korisnik3'
python usermgmt.py del korisnik3
echo

#forsiranje promjene lozinke
echo 'python usermgmt.py forcepass korisnik1'
python usermgmt.py forcepass korisnik1
echo


#login bez promjene lozinke
echo 'python login.py login korisnik2 - bez forcepass - upisi 1qayxsw2'
python login.py login korisnik2
echo

#login kada je potrebno promijeniti lozinku
echo 'python login.py login korisnik1 - uz forcepass - upisi NTFmc47kpe'
python login.py login korisnik1 
echo



#pokušaj dodavanja korisnika koji već postoji
echo 'python usermgmt.py add korisnik1 - već postoji'
python usermgmt.py add korisnik1
echo

#neispravna lozinka
echo 'python login.py login korisnik2 - upiši neispravnu lozinku'
python login.py login korisnik2
echo




#završi izvršavanje bash skripte
echo "Uspješan kraj."
read -p "Pritisni Enter za izlaz iz skripte."