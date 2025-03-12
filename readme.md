# Amharic NER for Ethiopian Telegram E-commerce

## Overview
This repository contains my work for developing a Named Entity Recognition (NER) system for Amharic text from Ethiopian-based Telegram e-commerce channels. The objective is to identify entities like products, prices, and locations within messages shared in these channels.

## Challenge Goals

The primary objective of this repo is to analyze Amharic text data to:
1. **Identify entities**: Extract entities such as products, prices, and locations from Telegram messages.
2. **Fine-tune NER models**: Fine-tune and compare multiple NER models on the preprocessed and labeled dataset.
3. **Evaluate model performance**: Evaluate the performance of the fine-tuned models and compare their accuracy.

## Data Source
The data is collected from Ethiopian Telegram e-commerce channels. The dataset includes both raw and labeled messages.

## Structure

The repository is organized into the following folders and branches (following naming conventions).

- **`data/`**: Contains the raw and processed data files.
- **`notebooks/`**: Jupyter notebooks documenting the Exploratory Data Analysis (EDA), Data version control, hypothesis testing, statistical modeling, and analysis processes.
- **`src/`**: Contains Python scripts used for data preprocessing, model building, and evaluation.
- **`reports/`**: Contains the interim and final reports.
- `**task-1**: Branch for data scraping.
- `**task-2**: Branch for EDA & Statistics.
- `**task-3**: Branch for fine-tuning models.
- `**task-4**: Branch for model comparison.
- `**task-5**: Branch for model interpretability.

## Key Tasks

The work is divided into several key tasks, each with specific objectives.

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
    git clone https://github.com/ibso99/EthioMart-named-entity-recognition-NER-.git
    cd EthioMart-named-entity-recognition-NER-
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
