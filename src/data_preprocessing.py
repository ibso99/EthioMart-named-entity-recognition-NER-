from functools import reduce, wraps 
import pandas as pd
import re
import matplotlib.pyplot as plt
from collections import Counter
import matplotlib.font_manager as fm
from datetime import datetime
import os
from functools import wraps
from contextlib import contextmanager
import time

# ==============================================
# Decorators for enhanced functionality
# ==============================================

def log_execution_time(func):
    """Decorator to log function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def handle_errors(func):
    """Decorator to handle exceptions gracefully"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {str(e)}")
            return None
    return wrapper

# ==============================================
# Context Managers
# ==============================================

@contextmanager
def setup_font(font_path):
    """Set up the font for matplotlib"""
    try:
        if os.path.exists(font_path):
            # Add the font to matplotlib
            font_prop = fm.FontProperties(fname=font_path)
            plt.rcParams['font.family'] = font_prop.get_name()
            print(f"Using font: {font_prop.get_name()}")
            return True
        else:
            print(f"Font file not found at {font_path}. Using default font.")
            return False
    except Exception as e:
        print(f"Error loading font: {e}")
        return False

@contextmanager
def csv_manager(file_path, mode='r'):
    """Context manager for CSV file handling"""
    file = None
    try:
        file = open(file_path, mode, encoding='utf-8', newline='')
        yield file
    finally:
        if file is not None:
            file.close()

# ==============================================
# Functional Programming Components
# ==============================================

def compose(*functions):
    """Functional programming composition helper"""
    if not functions:
        return lambda x: x
    return lambda x: reduce(lambda v, f: f(v), functions, x)

def text_processing_pipeline():
    """Create text processing pipeline using functional composition"""
    return compose(
        lambda text: text.lower(),
        lambda text: re.sub(
            r'[^\w\s\u1200-\u137F]',  # Ethiopic Unicode range
            '', 
            text,
            flags=re.UNICODE
        ),
        lambda text: text.strip()
    )

# ==============================================
# Generator for batched processing
# ==============================================

def message_generator(df, batch_size=100):
    """Generator for batched message processing"""
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        yield batch

# ==============================================
# Main Processing Functions
# ==============================================

@log_execution_time
@handle_errors
def preprocess_telegram_data(file_path):
    """Preprocess Telegram data with enhanced functionality"""
    # Functional pipeline setup
    process_text = text_processing_pipeline()
    
    with csv_manager(file_path) as file:
        df = pd.read_csv(file)
    
    # Convert all message data to string type
    df['Message'] = df['Message'].astype(str)
    
    # Rest of the processing remains the same
    required_columns = {'Message', 'Channel Title', 'Channel Username'}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        raise ValueError(f"Missing columns: {missing}")
    
    # Convert Date column to datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    else:
        df['Date'] = pd.to_datetime(datetime.today().date())
    
    # Generator-based processing
    processed_data = []
    for batch in message_generator(df):
        batch = batch.copy()
        batch['Cleaned_Message'] = batch['Message'].apply(process_text)
        batch['Tokens'] = batch['Cleaned_Message'].str.split()
        processed_data.append(batch)
    
    structured_data = pd.concat(processed_data)
    
    # Save using context manager
    output_path = "C:/Users/ibsan/Desktop/TenX/week-5/data/cleaned_telegram_data.csv"
    with csv_manager(output_path, 'w') as file:
        structured_data.to_csv(file, index=False)
    
    return structured_data

# ==============================================
# Visualization Components with Metaprogramming
# ==============================================

class Plotter:
    """Class-based plotter with registry pattern"""
    _plots = {}
    
    @classmethod
    def register(cls, name):
        """Decorator factory for plot registration"""
        def decorator(func):
            cls._plots[name] = func
            return func
        return decorator
    
    @classmethod
    def execute_plots(cls, data):
        """Execute all registered plots"""
        for name, plot_func in cls._plots.items():
            try:
                plot_func(data)
            except Exception as e:
                print(f"Error in plot '{name}': {str(e)}")

@Plotter.register('word_frequency')
def plot_word_frequency(data):
    """Plot word frequency distribution"""
    all_tokens = data['Tokens'].explode()
    common_words = all_tokens.value_counts().head(10)
    
    plt.figure(figsize=(10, 6))
    common_words.plot.bar(color='skyblue')
    plt.title('Top 10 Most Common Words')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.show()

@Plotter.register('message_length')
def plot_message_length(data):
    """Plot message length distribution"""
    data['Message_Length'] = data['Tokens'].str.len()
    
    plt.figure(figsize=(10, 6))
    data['Message_Length'].plot.hist(bins=20, color='lightgreen', edgecolor='black')
    plt.title('Distribution of Message Lengths')
    plt.xlabel('Number of Words')
    plt.ylabel('Frequency')
    plt.show()

@Plotter.register('time_series')
def plot_time_series(data):
    """Plot messages over time"""
    if 'Date' in data.columns:
        # Ensure Date column is datetime
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
        # Drop rows with invalid dates
        data = data.dropna(subset=['Date'])
        
        # Set index and resample
        time_series = data.set_index('Date').resample('D').size()
        
        plt.figure(figsize=(12, 6))
        time_series.plot(color='orange')
        plt.title('Messages Over Time')
        plt.xlabel('Date')
        plt.ylabel('Message Count')
        plt.grid(True)
        plt.show()
    else:
        print("Skipping 'Messages Over Time' plot: 'Date' column not found.")
# ==============================================
# Main Execution
# ==============================================

if __name__ == "__main__":
    input_path = "C:/Users/ibsan/Desktop/TenX/week-5/data/telegram_data.csv"
    font_path = 'C:/Users/ibsan/Desktop/TenX/week-5/data/fonts/AbyssinicaSIL-Regular.ttf'
    
    # Set up font before plotting
    font_setup_success = setup_font(font_path)
    
    cleaned_data = preprocess_telegram_data(input_path)
    
    if cleaned_data is not None:
        Plotter.execute_plots(cleaned_data)