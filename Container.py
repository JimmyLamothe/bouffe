from JsonObject import JsonObject

class Container(JsonObject):
    def __init__(self, name):
        super().__init__(name)
        if not self.file_exists(): #Generates json file on first creation
            #define self.properties
            self.save_dict()
