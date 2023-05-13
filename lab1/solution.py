import sys
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad



def izvediKljuc(lozinka, salt):
    return scrypt(lozinka, salt, 16, N=2**14, r=8, p=1) #vraća string(ključ) za sigurno spremanje lozinki


def sifrirajLozinku(glavnaLozinka, mapaLozinki):        #za pohranjivanje mape lozinki(svaka lozinka ima svoju stranicu) u datoteku
    tekst = ""
    for stranica in mapaLozinki:                        #prolazi se kroz sve lozinke koje se sve zajedno šifrirane upisuju u datoteku
        tekst += f'{stranica} {mapaLozinki[stranica]}\n'
    upisi(glavnaLozinka, str.encode(tekst))



def desifrirajLozinku(glavnaLozinka):                   #za čitanje i dešifriranje mape lozinki pohranjenih u datoteci
    mapaLozinki = {}

    with open('datoteka', 'rb') as datoteka:            #pročitaj datoteku
        podaci = datoteka.read()
    
    sol = podaci[:32]       #nasumični niz bajtova koji se koristi kao dodatna vrijednost pri izračunu ključa
    nonce = podaci[32:44]   #broj za generiranje šifre
    tag = podaci[44:60]     #kod za provjeru autentičnosti i integriteta teksta
    sifrat = podaci[60:]    #šifrirani tekst sa lozinkama
    
    kljuc = izvediKljuc(glavnaLozinka, sol)             #izvodi se ključ
    sifra = AES.new(kljuc, AES.MODE_GCM, nonce)         #novi AES objekt sa ključem i brojem za generiranje šifre
    poruka = sifra.decrypt_and_verify(sifrat, tag)      #spremanje dešifriranog teksta
    poruka = unpad(poruka, AES.block_size)              #makni padding sa poruke

    zapisi = poruka.decode('utf-8').split('\n')[:-1]    #decode - za pretvorbu u string, split - razdvojit u novi red da se lakše čitaju vrijednosti
    for zapis in zapisi:
        stranica, lozinka = zapis.split(' ')            #svaki zapis u mapi odvoji razmakom
        mapaLozinki[stranica] = lozinka                 #dodaj zapis u mapu koju si gore inicijalizirao
    
    return mapaLozinki




def upisi(glavnaLozinka, podatak):
    with open('datoteka', 'wb') as datoteka:
        
        sol = get_random_bytes(32)                      #slučajni salt od 32 bajta - da šifriranje bude složenije
        nonce = get_random_bytes(12)                    #slučajni nonce od 12 bajtova - dodatni ulaz u šifriranje
        kljuc = izvediKljuc(glavnaLozinka, sol)         #izvodimo ključ 
        podatak = pad(podatak, AES.block_size)          #dodaj padding na poruku
        sifra = AES.new(kljuc, AES.MODE_GCM, nonce)     #taj ključ i nonce se koriste za aes objekt
        sifrat, tag = sifra.encrypt_and_digest(podatak) #provodimo šifriranje

        datoteka.write(sol + nonce + tag + sifrat)      #upisujemo šifrat(šifrirani podatak), sol, nonce i tag upisujemo zbog dešifriranja kasnije





def main():
    naredba = sys.argv[1]
    glavnaLozinka = sys.argv[2]

    if naredba == 'init':
        upisi(glavnaLozinka, b"Password manager")    #upisujemo glavnu lozinku u password manager
        print("Password manager initialized.")       #poruka o uspješnosti
        return

    if naredba == 'put':
        stranica = sys.argv[3]
        lozinka = sys.argv[4]
        mapaLozinki = desifrirajLozinku(glavnaLozinka)      #dešifriramo trenutni sadržaj datoteke 
        mapaLozinki[stranica] = lozinka                     #postavljamo lozinku za određenu stranicu u mapu lozinki
        sifrirajLozinku(glavnaLozinka, mapaLozinki)         #šifriramo ažuriranu mapu lozinki
        print('Stored password for {}'.format(stranica))    #poruka korisniku o uspješnosti
        return

    
    if naredba == 'get':
        stranica = sys.argv[3]
        mapaLozinki = desifrirajLozinku(glavnaLozinka)              #dešifriramo trenutni sadržaj datoteke 
        lozinka = mapaLozinki[stranica]                             #dohvaćamo traženu lozinku iz mape u datoteci
        print('Password for {} is: {}'.format(stranica, lozinka))   #poruka korisniku o uspješnosti
        return


if __name__ == "__main__":
    main()
