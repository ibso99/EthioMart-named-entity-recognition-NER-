**Project README**
Amharic NER for Ethiopian Telegram E-commerce
This project involves developing a Named Entity Recognition (NER) system for Amharic text from Ethiopian-based Telegram e-commerce channels. The objective is to identify entities like products, prices, and locations within messages shared in these channels.

**Objectives**
Data Collection and Preprocessing: Set up a data ingestion system to fetch real-time messages (text, images, documents) from at least 5 Ethiopian Telegram e-commerce channels. Preprocess and clean the data for entity extraction.
Data Labeling: Label a subset of the dataset in CoNLL format, identifying entities such as products, prices, and locations.
Model Training and Comparison: Fine-tune and compare multiple NER models on the preprocessed and labeled dataset.

**Data Collection (Task-1)**
Use a custom scraper to identify and connect to at least 5 relevant Telegram channels for Ethiopian e-commerce.
Collect messages containing both text and images.
Preprocess text data, handle Amharic-specific linguistic features (e.g., normalization, tokenization), and clean it for entity extraction.
Store the cleaned data in a structured format for further analysis.

**Data Labeling (Task-2)**
Label the Amharic text data for entities such as products, prices, and locations.
Label a subset of the dataset in CoNLL format, which includes the following:

## Structure

The repository is organized into the following folders, and branches (following naming conventions).

- **`data/`**: Contains the raw and processed data files.
- **`notebooks/`**: Jupyter notebooks documenting the Exploratory Data Analysis (EDA), Data version control, hypothesis testing, statistical modeling, and analysis processes.

- **`src/`**: Contains Python scripts used for data preprocessing
- `**task-1**: Data scraping
- `**task-2**: (EDA & Statistics)
- `**task-3**: Fine Tuning
- `**task-4**: Model comparison
- `**task-5**: Branch for model interpreteability

# Project Overview

This project involves fine-tuning and comparing different transformer models for Named Entity Recognition (NER) tasks. The work is divided into several key tasks, each with specific objectives and deliverables.

## Key Tasks

### Task 1: Exploratory Data Analysis (EDA) & Stats

- **Objective**: Gain insights into the data through summarization, quality assessment, visualization, and statistical thinking.
- **Deliverables**:
    - Jupyter notebooks performing EDA.
    - Descriptive statistics summary.
    - Plots illustrating key insights.

### Task 2: Data Preparation

- **Objective**: Prepare the dataset for model training by parsing, tokenizing, and aligning labels.
- **Deliverables**:
    - Parsed dataset from `.conll` file.
    - Tokenized dataset with aligned labels.
    - Split dataset into training and testing sets.

### Task 3: Model Fine-Tuning

- **Objective**: Fine-tune transformer models (`xlm-roberta`, `distilbert`, and `mbert`) on the prepared dataset.
- **Deliverables**:
    - Fine-tuned models saved to the specified directory.
    - Training logs and checkpoints.
    - Evaluation metrics for each model.

### Task 4: Model Evaluation

- **Objective**: Evaluate the fine-tuned models using accuracy metrics and compare their performance.
- **Deliverables**:
    - Evaluation results for each model.
    - Accuracy metrics and comparison report.
    - Conclusions and findings reported.

## Technologies Used

- **Programming Language**: Python
- **Data Analysis Libraries**: Pandas, NumPy
- **Visualization Libraries**: Matplotlib, Seaborn
- **Transformer Libraries**: Hugging Face Transformers, Datasets
- **Evaluation Libraries**: Seqeval, Evaluate
- **Cloud**: GitHub
- **CI/CD**: GitHub Actions

## How to Run the Code

1. **Clone the Repository**:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Jupyter Notebooks**:
    - Open Jupyter Notebook:
        ```bash
        jupyter notebook
        ```
    - Navigate to the `notebooks` directory and open the following notebooks in order:
        - `EDA.ipynb`
        - `Fine_Tune_NER_Model.ipynb`
        - `Model_Comparistion.ipynb`
        - `Model_Interpritability.ipynb`

4. **Perform EDA**:
    - Run the cells in `EDA.ipynb` to perform exploratory data analysis and gain insights into the dataset.

5. **Fine-Tune Models**:
    - Run the cells in `Fine_Tune_NER_Model.ipynb` to fine-tune the transformer models on the prepared dataset.

6. **Compare Models**:
    - Run the cells in `Model_Comparistion.ipynb` to compare the performance of the fine-tuned models and evaluate their accuracy.

7. **Interpret Models**:
    - Run the cells in `Model_Interpritability.ipynb` to interpret the results and understand the model predictions.

By following these steps, you will be able to reproduce the results and gain insights into the performance of different transformer models for NER tasks.

