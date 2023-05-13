import getpass 
import sys
import bcrypt
from base64 import b64encode
from base64 import b64decode


def hash_password(password, salt):
    '''
    print("salt: ", salt)
    print("salt_type: ", type(salt))
    '''
    password_bytes = password.encode('utf-8')
    '''
    print("password_bytes: ", password_bytes)
    '''
    bcrypt_hash = bcrypt.kdf(password_bytes, salt, 32, 1000) 
    return bcrypt_hash




def ucitajKorisnike():
    korisnici = {}
    with open('korisnici.txt', 'r+') as dat:
        #Provjeri je li datoteka prazna
        if dat.seek(0, 2) == 0:
            return korisnici
        
        #Dođi na početak datoteke
        dat.seek(0)
        
        #Procitaj svaku liniju datoteke
        for linija in dat:
            #Provjeri sadrzi li linija :
            if ':' not in linija:
                continue
            
            #Splitaj liniju na username i ostale podatke sa :
            podaci = linija.strip().split(':')
            korisnici[podaci[0]] = {'lozinkaHash': podaci[1], 'salt': podaci[2], 'force': podaci[3] == 'True'}
            
    return korisnici


def upisiKorisnike(korisnici): 
    with open('korisnici.txt', 'w+') as dat:
        for korisnik, podaci in korisnici.items():
            korisnickoIme = korisnik
            lozinkaHash = podaci['lozinkaHash']
            salt = podaci['salt']
            force = podaci['force']
            dat.write('{}:{}:{}:{}\n'.format(korisnickoIme, lozinkaHash, salt, force))




def main():
    naredba = sys.argv[1]
    korisnickoIme = sys.argv[2]

    
    if naredba == 'add':
        korisnici = ucitajKorisnike()
        if korisnickoIme in korisnici.keys():
            print(f"User {korisnickoIme} already exists.")
            return
        else:
            lozinka = getpass.getpass()
            if len(lozinka) < 8:
                exit("Password too short.")
            ponoviLozinka = getpass.getpass(prompt='Repeat Password: ')
            if lozinka == ponoviLozinka:
                salt = bcrypt.gensalt()
                lozinkaHash = hash_password(lozinka, salt)
                korisnici[korisnickoIme] = {'lozinkaHash': lozinkaHash, 'salt': salt.decode('utf-8'), 'force': False}
                upisiKorisnike(korisnici)
                '''
                print("helper_type1_salt: ", type(salt))
                print("helper_type2: ", type(korisnici[korisnickoIme]['salt']))
                print("salt: ", korisnici[korisnickoIme]['salt'])
                '''
                print('User {} successfully added.'.format(korisnickoIme))
                return
            else:
                print('User add failed. Password mismatch.')
                return

            
    if naredba == 'passwd':
        korisnici = ucitajKorisnike()
        if korisnickoIme not in korisnici.keys():
            print(f'User {korisnickoIme} does not exist.')
            return
        else:
            lozinka = getpass.getpass()
            ponoviLozinka = getpass.getpass(prompt='Repeat Password: ')
            salt = korisnici[korisnickoIme]['salt']
            trenutnaLozinkaHash = korisnici[korisnickoIme]['lozinkaHash']
            noviLozinkaHash = hash_password(lozinka, salt.encode('utf-8'))
            if str(noviLozinkaHash) == trenutnaLozinkaHash:
                print('New password must be different from existing one.')
                return
            
            if lozinka == ponoviLozinka:
                korisnici[korisnickoIme]['lozinkaHash'] = noviLozinkaHash
                upisiKorisnike(korisnici)
                print(f'Password for user {korisnickoIme} successfully updated.')
                return
            else:
                print('Password change failed. Password mismatch.')
                return


    
    if naredba == 'forcepass':
        korisnici = ucitajKorisnike()
        if korisnickoIme not in korisnici.keys():
            print(f'User {korisnickoIme} does not exist.')
            return
        else:
            korisnici[korisnickoIme]['force'] = True
            upisiKorisnike(korisnici)
            print(f'User {korisnickoIme} will be requested to change password on next login.')
            return

        
    if naredba == 'del':
        korisnici = ucitajKorisnike()
        if korisnickoIme not in korisnici.keys():
            print('User {} does not exist.'.format(korisnickoIme))
            return
        else:
            odgovor = input('Are you sure you want to delete user {}? (y/n)'.format(korisnickoIme))
            if odgovor.lower() == 'y':
                del korisnici[korisnickoIme]
                upisiKorisnike(korisnici)
                print('User {} successfully deleted.'.format(korisnickoIme))
                return
            else:
                print('User deletion cancelled.')
                return



    print('Unknown command: {}'.format(naredba))
    return



if __name__ == '__main__':
    main()
