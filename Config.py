from configparser import ConfigParser

class Config:
    _instance = None
    def __init__(self, filePath):
        self.config = ConfigParser()
        self.config.read(filePath)
        pass

    def getInstance():
        if __class__._instance is None:
            __class__._instance = __class__('conf.ini')

        return __class__._instance

    def get(key: str):
        section, key = key.split('.')
        conf = __class__.getInstance()
        return conf.config[section][key]

if __name__ == '__main__':
    pass
