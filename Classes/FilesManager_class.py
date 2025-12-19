import dill



class FilesManager():

    def __init__(self):
        pass

    #   S A V E   B I N A R Y   F I L E
    def save_to_binaryFile(self, obj, filename, path=''):
        '''
            Save object to a file

            Input:
                obj         :   object to save (e.g. object form class, list, np.array, dict, ...)
                    object

                filename    :   file name
                    str
                    
                path        :   path where file is saved
                    str
        '''

        name = path + filename
        file = open(name, "wb")
        dill.dump( obj, file)  # file
        file.close()

    
    #   L O A D   B I N A R Y   F I L E
    def load_from_binaryFile(self, filename, path=''):
        '''
            Save object to file

            Input:
                filename    :   file name
                    str
                
                path        :   path where file is saved
                    str
        '''

        name = path+filename
        file =  open( name, 'rb')
        obj = dill.load(file)
        file.close()

        return obj


    #   S A V E   T E X T   F I L E
    def save_to_textFile(self, txt, filename, path=''):
        '''
            Save object to file

            Input:
                txt         :   text to save
                    object
                filename    :   file name
                    str
                
                path        :   path where file is saved
                    str
        '''

        with open(path+filename, 'w') as f:
            print(txt, file=f)



    #   L O A D   T E X T   F I L E
    def load_from_textFile(self, filename, path=''):
        '''
            Save object to file

            Input:
                filename    :   file name
                    str
                
                path        :   path where file is saved
                    str
        '''

        name = path+filename
        file =  open( name, 'r')
        data = file.read()
        file.close()

        return data