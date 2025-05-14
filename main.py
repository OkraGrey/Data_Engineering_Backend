from endpoints import search
from logging_config import setup_logging

#Setting Up my LOGGER with Logging Level Info

LOGGER = setup_logging()(__name__)

if __name__ == "__main__":

    LOGGER.info("Calling Search Endpoint")
    result =search('bar','San Bernardino')
    print(result)