import dill # Libreria per serializzare e deserializzare oggetti Python: viene usato per caricare i dati binari salvati dal radar.
import os # Libreria per interagire con il sistema operativo, ad esempio per gestire i percorsi dei file.


class fileReader():
    def __init__(self):
        pass


    def load_data(self, name, filepath):
        """
        Carica i dati binari salvati con dill.
        
        :param filepath: Percorso del file binario
        :return: Oggetto deserializzato
        """
        with open(os.path.join(filepath, name), 'rb') as file:
            obj = dill.load(file) # Usa dill per caricare l'oggetto salvato nel file
        return obj # Restituisce l'oggetto caricato