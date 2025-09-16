import hashlib
from common.kafka_consumer import Consumer
from common.config import settings

class Create_hash:
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
            print()

# c = Consumer(settings.TOPIC_PROFILES_CREATED,"hggggggg")
# c.listen()