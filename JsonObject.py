import os, json

class JsonObject:
    def __init__(self, name): #name = str
        self.name = name
        try: #Load from JSON if file exists
            print('check1')
            with open(self.get_filepath(), 'r') as json_file:
                self.__dict__ = json.load(json_file)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            print('check2')
            pass

    def get_filename(self):
        return self.name + '.json'

    def get_directory(self): #Override for subdirectories
        return 'json/'

    def get_filepath(self):
        return self.get_directory() + self.get_filename()
        
    def file_exists(self):
        if os.path.exists(self.get_filepath()):
            return True
        return False

    def save_dict(self):
        with open(self.get_filepath(), 'w') as json_file:
            json.dump(self.__dict__, json_file)
                              
    def reset(self):
        if self.file_exists():
            os.remove(self.get_filepath())
        for key in self.__dict__:
            self.__dict__[key] = None

    def __repr__(self):
        return str(self.__dict__)
