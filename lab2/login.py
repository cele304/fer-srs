import getpass 
import sys
import bcrypt
from base64 import b64encode
from base64 import b64decode

from usermgmt import hash_password
from usermgmt import ucitajKorisnike
from usermgmt import upisiKorisnike


def main():
    naredba = sys.argv[1]
    korisnickoIme = sys.argv[2]

    if naredba == 'login':
        korisnici = ucitajKorisnike()
        if korisnickoIme not in korisnici.keys():
            print('User {} does not exist.'.format(korisnickoIme))
            return
        else:
            if korisnici[korisnickoIme]['force']:
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
                    korisnici[korisnickoIme]['force'] = False
                    upisiKorisnike(korisnici)
                    print(f'Password for user {korisnickoIme} successfully updated.')
                    return
                else:
                    print('Password change failed. Password mismatch.')
                    return

            else:
                lozinka = getpass.getpass()
                lozinkaHash = korisnici[korisnickoIme]['lozinkaHash']
                salt = korisnici[korisnickoIme]['salt']
                '''
                print(lozinka)
                print(salt)
                print("SALT: ", type(salt))
                print("LOZINKA_HASH: ", lozinkaHash)
                print("LOZINKA: ", lozinka)
                print("SALT_ENCODE: ", salt.encode('utf-8'))
                '''
                hash_lozinke = hash_password(lozinka, salt.encode('utf-8'))
                '''
                print("HASH_LOZINKE: ", hash_lozinke)
                print("hash_lozinke_type: ", type(hash_lozinke))
                print("LOZINKA_HASH: ", lozinkaHash)
                print("lozinka_hash_type: ", type(lozinkaHash))
                '''
                '''
                print(type(lozinkaHash))
                print(lozinkaHash)
                print(type(hash_lozinke))
                print(hash_lozinke)
                '''
                if lozinkaHash == str(hash_lozinke):
                    print(f'Login for user {korisnickoIme} successful.')
                else:
                    print('Greška.')




if __name__ == '__main__':
    main()
