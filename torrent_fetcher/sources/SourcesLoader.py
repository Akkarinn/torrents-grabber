import logging
import json
import os
from importlib import import_module

def initLogging():
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)

class SourcesLoader:

    @staticmethod
    def load(config_filepath):
        """
        Load sources modules from a configuration file.

        :param config_filepath:
            A configuration file where are listed the available sources implementation.
            File content format:
                { "name1" : "filepath_to_load1", "name2" : "filepath_to_load2" ... }
        :return: A collection of AbstractSource.
        """
        sources = []
        logging.info("[Config] Read sources configuration from '%s'" % (config_filepath))
        if os.path.exists(config_filepath):
            try:
               json_data = json.load(open(config_filepath))
               logging.info("[Config] Found %i declared source(s) to load..." % (len(json_data.items())))
               for name, module in json_data.items():
                    sources.append(SourcesLoader.__load(name, module))
            except:
                logging.error("[Config] Unexpected error while loading sources modules configuration files")
                raise
        else:
            logging.error("[Config] Error: Couldn't find file '%s'" % (config_filepath))

        return sources

    @staticmethod
    def __load(name, module):
        factory_method = getattr(import_module(module), "createSource")
        return factory_method()

if __name__ == "__main__":
    initLogging()
    sources = SourcesLoader.load("../../data/tests/sources_modules.plugins.json")
    for s in sources:
        print(s.getTorrentsUrls([".*dragon-ball-super.*vostfr-hdtv*"]))
