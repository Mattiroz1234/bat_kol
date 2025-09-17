import hashlib
from common.logger import Logger

logger = Logger.get_logger(name=__name__)

class CreateHash:
    def __init__(self):
        self.hash_code = None


    def made_a_hash(self,massage):
        try:
            combined_string = "".join(massage)
            encoded_string = combined_string.encode('utf-8')
            hasher = hashlib.sha256()
            hasher.update(encoded_string)
            self.hash_code = hasher.hexdigest()
            return self.hash_code

        except Exception as e:
            logger.error(f"made id error: {e}")