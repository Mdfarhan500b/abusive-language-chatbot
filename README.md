# **Abusive Language Detection Chatbot**

A machine learning-based chatbot that detects offensive or abusive language in messages. It is trained using the **Support Vector Machine (SVM)** model and can handle multilingual input, including **English**, **Roman Hindi**, and **Roman Bengali**.

---

## **Project Structure**

```
/abusive-language-detection-chatbot
│
├── /data                          # Dataset files
│   ├── labeled_data.csv            # Labeled data for training
│   ├── offensive_words_bengali.txt # Bengali offensive words
│   ├── offensive_words_english.txt # English offensive words
│   ├── offensive_words_hindi.txt   # Hindi offensive words
│   ├── processed_train_data.csv    # Preprocessed training data
│   └── train_data3v2.csv           # Another dataset used for training
│
├── /static                        # Static files (CSS, JS, images)
│   ├── function.js                # JavaScript functions
│   └── style.css                  # CSS styles for the chatbot UI
│
├── /templates                      # HTML files for the web interface
│   └── index.html                 # Main HTML file for the chatbot UI
│
├── app.py                          # Flask application for the chatbot
├── model.pkl                       # Trained model file (SVM)
├── preprocess_data.py              # Script for data preprocessing
├── README.md                       # Project README
├── train_model.py                  # Script for training the machine learning model
└── vectorizer.pkl                  # TF-IDF vectorizer file
```

---

## **Features**

* **Offensive Language Detection**: The chatbot detects whether a given message contains abusive or offensive language.
* **Multilingual Support**: Supports multiple languages, including **English**, **Roman Hindi**, and **Roman Bengali**.
* **Real-time Response**: Provides real-time feedback on whether a message is classified as offensive or non-offensive.
* **Web Interface**: A simple web-based interface using Flask.

---

## **Technologies Used**

* **Machine Learning**:

  * **Support Vector Machine (SVM)** with **LinearSVC** for classification.
  * **TF-IDF Vectorizer** to convert text data into numerical features.

* **Backend**:

  * **Flask**: Python web framework for serving the chatbot application.

* **Frontend**:

  * **HTML/CSS**: Basic web interface to interact with the chatbot.
  * **JavaScript**: For dynamic interaction on the front end.

* **Libraries**:

  * **scikit-learn**: For machine learning algorithms and text vectorization.
  * **pandas**: For managing and processing data.
  * **pickle**: For saving and loading the trained model.

---

## **Setup Instructions**

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/abusive-language-detection-chatbot.git
cd abusive-language-detection-chatbot
```

### 2. Install Dependencies

Make sure you have Python installed. You can create a virtual environment and install the necessary libraries:

```bash
pip install -r requirements.txt
```

### 3. Prepare the Dataset

Ensure that your dataset files are available in the `/data` folder. The file `processed_train_data.csv` should contain the following columns:

* `tweet`: The input text data (messages).
* `label`: The target column (0 for non-offensive, 1 for offensive).

### 4. Train the Model

To train the model using **Support Vector Machine (SVM)**, run the following command:

```bash
python train_model.py
```

This will train the SVM model and save the trained model (`model.pkl`) and the vectorizer (`vectorizer.pkl`).

### 5. Run the Chatbot

Run the Flask server to interact with the chatbot:

```bash
python app.py
```

The chatbot will be accessible at `http://127.0.0.1:5000/`.

### 6. Test the Chatbot

Once the server is running, open a web browser and type a message to check if it is classified as **offensive** or **non-offensive**.

---

## **Folder Structure Breakdown**

### `/data`

Contains all dataset files, including:

* **labeled\_data.csv**: The main labeled dataset for training.
* **offensive\_words\_bengali.txt**: List of Bengali offensive words.
* **offensive\_words\_english.txt**: List of English offensive words.
* **offensive\_words\_hindi.txt**: List of Hindi offensive words.
* **processed\_train\_data.csv**: Cleaned and preprocessed dataset for training.
* **train\_data3v2.csv**: Another dataset used for training.

### `/static`

Holds static files such as CSS, JS, and images:

* **function.js**: JavaScript functions for interactivity.
* **style.css**: CSS styles for the chatbot UI.

### `/templates`

Contains the main HTML template:

* **index.html**: The HTML file for the chatbot interface.

### Python Scripts

* **app.py**: The main Flask application for handling requests and responses.
* **train\_model.py**: Script for training the model.
* **preprocess\_data.py**: Script for preprocessing data before training.

### Saved Files

* **model.pkl**: The trained model file (SVM).
* **vectorizer.pkl**: The TF-IDF vectorizer used for text transformation.

---

## **License**

This project is open-source and available under the MIT License.


