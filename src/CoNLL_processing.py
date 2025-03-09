import pandas as pd
import re
from functools import lru_cache
from contextlib import contextmanager
import time

class CoNLLFormatter:
    def __init__(self):
        """Initialize entity flags and entity lists."""
        self.inside_product = False
        self.inside_location = False
        self.inside_price = False
        self._locations = self._load_entities('locations')
        self._products = self._load_entities('products')
        self._price_indicators = self._load_entities('price_indicators')

    @staticmethod
    def _load_entities(entity_type):
        """Load entity lists for locations, products, and price indicators."""
        entities = {
            'locations': [
                'አዲስ', 'አበባ', 'ቦሌ', 'ፒያሳ', 'ድሬዳዋ', 'አደባባይ', 'መሰረት', 
                'ሞል', 'ኦሮሚያ', 'ጀሞ', 'ጉርድ', 'ሾላ', 'ፎቅ', 'ቢሮ', 'ቱንባባ', 
                'ቀርንጫፍ', 'መገናኛ', 'ኮሜርስ', 'ጊዮርጊስ', 'ደፋር', 'ገርጂ'
            ],
            'products': [
                'ሽንኩርት', 'ጫማ', 'ቦርሳ', 'ተጣጣፊ', 'ፑሽ', 'አፕ', 'መሳሪያ', 
                'ኦርጂናል', 'ነንስቲክ', 'ብረት', 'ድስት', 'ዕቃ', 'ታብሌቱ', 'ቤት', 
                'ፀጉር', 'መተኮሻ', 'ቴፕ', 'ለልጅዎ', 'እርሳስ', 'ጫማዎች', 
                'ተለጣፊ', 'ፕላስተር', 'ቴብል', 'ማት', 'የህፃናት', 'መመገቢያ', 
                'ጡጦ', 'ሀርቪ', 'ስቲከር', 'ዘይት', 'ምግብ', 'ማብሰያ', 'ሳቺ', 
                'ምድጃ', 'ስቶቭ', 'ሲኒዎች', 'ኪችን', 'ጄል', 'ኮፍያ', 'ጋርመንት', 
                'ስቲመር', 'ማጂክ', 'መወልወያ', 'ኦቭን', 'ሙቀት', 'መቆጣጠሪያ', 
                'መድረቂያ', 'ካፕ', 'ኬክ', 'ፍራፍሬ', 'አትክልት', 'ፔርሙዝ', 
                'ጆግ', 'ማንቆርቆሪያ', 'ጀርባ', 'ዶናት', 'ሩቢክስ', 'ኪዩብን', 
                'ቲሸርቶች', 'ሱሪም', 'ቱታ', 'ብረት', 'ውሀ', 'ቅባት', 'ብርጭቆወች', 
                'መጠጫ', 'ስትሮ', 'እሳት', 'ካቢኔት', 'ግርግዳ', 'ፍሪጆች', 
                'ማጠቢያ', 'ላውንደሪዎች', 'ጎማዎች', 'መጋዝ', 'መቀስ', 'መክተፊያ'
            ],
            'price_indicators': [
                'ዋጋ', 'ብር', 'ሚሊዮን', 'ሺህ', 'ኪሎ', 'ግራም', 'ሜትር'
            ]
        }
        return set(entities.get(entity_type, []))

    @lru_cache(maxsize=1000)
    def tokenize_message(self, message):
        """Tokenize the input message into individual words."""
        return re.findall(r'\S+', message)

    def _reset_flags(self):
        """Reset entity flags for a new message."""
        self.inside_product = False
        self.inside_location = False
        self.inside_price = False

    def label_token(self, token):
        """Label a token based on entity rules."""
        if token in self._locations:
            return self._handle_entity(token, 'LOC')
        elif token in self._products:
            return self._handle_entity(token, 'PRODUCT')
        elif token in self._price_indicators or token.isdigit():
            return self._handle_entity(token, 'PRICE')
        return f"{token} O"

    def _handle_entity(self, token, entity_type):
        """Handle entity labeling with proper prefix (B- or I-)."""
        # Map entity type to the corresponding flag
        flag_map = {
            'LOC': 'location',
            'PRODUCT': 'product',
            'PRICE': 'price'
        }
        flag_name = flag_map.get(entity_type)
        
        if flag_name is None:
            return f"{token} O"
        
        # Determine prefix (B- or I-)
        prefix = "B" if not getattr(self, f"inside_{flag_name}") else "I"
        
        # Update flags
        for flag in ['product', 'location', 'price']:
            setattr(self, f"inside_{flag}", flag == flag_name)
        
        return f"{token} {prefix}-{entity_type}"

    def label_message(self, message):
        """Label all tokens in a message in CoNLL format."""
        self._reset_flags()
        return "\n".join(self.label_token(token) for token in self.tokenize_message(message))

    def process_messages(self, messages):
        """Process a list of messages and return CoNLL formatted output."""
        return "\n\n".join(self.label_message(msg) for msg in messages)

    @contextmanager
    def file_handler(self, file_path, mode='w'):
        """Context manager for file handling."""
        file = None
        try:
            file = open(file_path, mode, encoding='utf-8')
            yield file
        finally:
            if file is not None:
                file.close()

    def save_to_txt(self, labeled_messages, file_path):
        """Save labeled messages to a file in CoNLL format."""
        with self.file_handler(file_path) as file:
            file.write(labeled_messages)

def main():
    """Main function to execute the program."""
    start_time = time.time()
    
    try:
        # Load the dataset
        input_file_path = "C:/Users/ibsan/Desktop/TenX/week-5/data/cleaned_telegram_data.csv"
        df = pd.read_csv(input_file_path, encoding='utf-8')

        # Select the "Message" column
        messages = df['Message'].dropna().tolist()[:50]  # Process 50 messages

        # Process the messages
        formatter = CoNLLFormatter()
        labeled_messages = formatter.process_messages(messages)

        # Save the labeled messages
        output_file_path = "C:/Users/ibsan/Desktop/TenX/week-5/data/labeled_messages.conll"
        formatter.save_to_txt(labeled_messages, output_file_path)

        print(f"Labeled messages saved successfully to {output_file_path}")
        print(f"Execution time: {time.time() - start_time:.2f} seconds")

    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()