from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import random
from typing import List

class Szoba(ABC):
    
    def __init__(self, szobaszam: int, ar: float):
        self._szobaszam = szobaszam
        self._ar = ar
        self._foglalasok = []

    @abstractmethod
    def __str__(self):
        pass

    @property
    def szobaszam(self) -> int:
        return self._szobaszam
    @property
    def ar(self) -> float:
        return self._ar

    def szabad(self, kezdo_datum: datetime, vegso_datum: datetime):
        return all(foglalas.vegso_datum < kezdo_datum or foglalas.kezdo_datum > vegso_datum for foglalas in self._foglalasok)  
    

    def foglal(self, kezdo_datum: datetime, vegso_datum: datetime):
        if self.szabad(kezdo_datum, vegso_datum):
            self._foglalasok.append(Foglalas(kezdo_datum, vegso_datum))  
            return f"Szoba {self._szobaszam} lefoglalva {kezdo_datum.strftime('%Y-%m-%d')} és {vegso_datum.strftime('%Y-%m-%d')} között. A fizetendő {self.ar*((vegso_datum-kezdo_datum).days)} a {(vegso_datum-kezdo_datum).days} napra"
        else:
            return f"Szoba {self._szobaszam} már foglalt ebben az időszakban."
        

    def foglalasok_listaja(self):
        foglalasok_str = [str(f) for f in self._foglalasok]
        return ", ".join(foglalasok_str) if foglalasok_str else "Nincsenek foglalások"
    

class EgyagyasSzoba(Szoba):
    def __str__(self):
        return (f"Egyágyas szoba. Szám: {self.szobaszam}, Ár: {self.ar}, "
                f"Foglalások: {self.foglalasok_listaja()}")

class KetagyasSzoba(Szoba):
    def __str__(self):
        return (f"Kétágyas szoba. Szám: {self.szobaszam}, Ár: {self.ar}, "
                f"Foglalások: {self.foglalasok_listaja()}")

class Foglalas:  
    def __init__(self, kezdo_datum: datetime, vegso_datum: datetime):
        self.kezdo_datum = kezdo_datum
        self.vegso_datum = vegso_datum

    def __repr__(self):
        return f"{self.kezdo_datum.strftime('%Y-%m-%d')} - {self.vegso_datum.strftime('%Y-%m-%d')}"

class Szalloda:
    def __init__(self, nev: str):
        self.nev = nev
        self._szobak: List[Szoba] = []
    def szoba_hozzaadas(self, szoba: Szoba):
        self._szobak.append(szoba)
    
    def foglalas_torles(self, szobaszam: int, kezdo_datum_be: datetime):
       szoba = next((s for s in self._szobak if s.szobaszam == szobaszam), None)
       if szoba:
           eredeti_meret = len(szoba._foglalasok)
           for foglalas in szoba._foglalasok:
               if (foglalas.kezdo_datum.strftime('%Y-%m-%d') == kezdo_datum_be.strftime('%Y-%m-%d')):
                    szoba._foglalasok.remove(foglalas)
           if len(szoba._foglalasok) < eredeti_meret:
               return f"Szoba {szobaszam} foglalása törölve a megadott dátummal: {kezdo_datum_be.strftime('%Y-%m-%d')}"
           else:
               return f"Nincs ilyen kezdő dátumú foglalás: {kezdo_datum_be.strftime('%Y-%m-%d')} a szoba {szobaszam} számára."
       else:
           return "Szoba nem található."

       
    def foglalasok_listazasa(self) -> str:
        return '\n'.join(str(szoba) for szoba in self._szobak)

    def szoba_foglal(self, szobaszam: int, kezdo_datum: datetime, vegso_datum: datetime) -> str:
        szoba = next((s for s in self._szobak if s.szobaszam == szobaszam), None)
        if szoba:
            return szoba.foglal(kezdo_datum, vegso_datum)
        return "Szoba nem található."

    def adatok_inicializalasa(self):
        #3 szoba létrehozása
        self.szoba_hozzaadas(EgyagyasSzoba(1, 20000))
        self.szoba_hozzaadas(KetagyasSzoba(2, 30000))
        self.szoba_hozzaadas(KetagyasSzoba(3, 50000))
        #5 foglalás feltöltése
        i = 0
        max_range = 5
        while i < max_range:    
            szobaszam = random.randint(1, 3) 
            kezdo_datum = datetime.now() + timedelta(days=random.randint(0,90))  
            vegso_datum = kezdo_datum + timedelta(days=random.randint(0,20))
            if(self.szoba_foglal( szobaszam, kezdo_datum, vegso_datum) == f"Szoba {szobaszam} már foglalt ebben az időszakban."):
                max_range += 1
            i += 1

def foglalasi_folyamat(szalloda: Szalloda):
    #adat inicializálás
    szalloda.adatok_inicializalasa()
    #felhasználói felület
    while True:
        tevekenyseg = input("Mit szeretne tenni? (1. foglalások, 2. foglal, 3. lemondás, 4. kilépés): ")
        if tevekenyseg.lower() == "foglalások" or tevekenyseg.startswith('1'):
            print(szalloda.foglalasok_listazasa())
        elif tevekenyseg.lower() == "foglal" or tevekenyseg.startswith('2'):
            szobaszam = int(input("Melyik szobát foglalná: "))
            kezdo_datum_str = input("Adja meg a foglalás kezdő dátumot (ééééhhnn): ")
            vegso_datum_str = input("Adja meg a foglalás végső dátumot (ééééhhnn): ")
            kezdo_datum = datetime.strptime(kezdo_datum_str, '%Y%m%d')
            vegso_datum = datetime.strptime(vegso_datum_str, '%Y%m%d')
            if (kezdo_datum > vegso_datum or kezdo_datum < datetime.now()):
                print("Érvénytelen dátumok")
                continue
            print(szalloda.szoba_foglal(szobaszam, kezdo_datum, vegso_datum))
        elif tevekenyseg.lower() == "lemondás" or tevekenyseg.startswith('3'):
            szobaszam = int(input("Melyik szobát mondaná le: "))
            kezdo_datum_str = input("Adja meg a lemondani kívánt szoba kezdő dátumát (ééééhhnn): ")
            kezdo_datum_be = datetime.strptime(kezdo_datum_str, '%Y%m%d')
            print(szalloda.foglalas_torles(szobaszam, kezdo_datum_be))
        elif tevekenyseg.lower() == "kilépés" or tevekenyseg.startswith('4'):
            print("Viszlát!")
            break
        else:
            print("Kérem a felsorolt választásokból válasszon.")
szalloda = Szalloda("Calipso")
foglalasi_folyamat(szalloda)