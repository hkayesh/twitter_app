# CryptoBEx Core NLP Application

The CryptoBEx NLP frameworks enables automated training, validation and deployment of text classification models in order to incrementally improve performance of the CBEx News Feed.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Before installing the application make sure your system has the following packages installed. If you do not have these 
packages installed please follow the _Setup Environment_ section below otherwise you can skip the next section. 

```
1. >= Python 3.6.3 
2. NLTK Data: stopwords, punkt, and wordnet
2. >= Mysql 5.7.21 
```

### Setup Environment
The instructions below are only specific to the Fedora 27/26/25 Operating System. 

#### Install Python 3.6
Follow three three steps below to install the latest version of python 3:

* To be able to compile Python Source, you will need few packages. Open terminal and execute this command.
   
```
$ yum install openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel
```
        
* Download latest release of Python. Please refer to the [python download page](http://www.python.org/download/releases) to ensure the latest source is used.   

```
$ wget http://www.python.org/ftp/python/3.x/Python-3.x.tar.bz2
```

* Extract and move to the extracted directory.

```
$ tar -xjf Python-3.xtar.bz2 cd Python-3.x
```

*  Configure the build with a prefix (install dir) of /opt/python3, compile, and install.

```
$ ./configure --prefix=/opt/python3 
$ make 
$ sudo make install
```

Python 3 will now be installed to /opt/python3.

#### Download NLTK Data
Follow the steps below to download NLTK data to your system: 

* If you have the NLTK python module installed then install it, otherwise please skip this step.
    
``` 
$ pip install nltk
```

* Start the python command line.
    
```
$ mysql
```

* Run the following commands to download 'stopwords', 'punkt' and 'wordnet'.

```
> import nltk
> nltk.download('stopwords')
> nltk.download('punkt')
> nltk.download('wordnet')
```

#### Install MySQL 5.7 
To install MySQL community version on Fedora 25/26/27 follow the steps below:

* Install MySQL Community package 
    
```
$ sudo dnf install mysql-community-server
```
    
* Start MySQL server and autostart MySQL on boot
    
```
$ sudo systemctl start mysqld.service
$ sudo systemctl enable mysqld.service
```
    
* Get the auto generate random root password:
    
```
$ sudo grep 'A temporary password is generated for root@localhost' /var/log/mysqld.log |tail -1
```

Example Output:
    
```
2015-11-20T21:11:44.229891Z 1 [Note] A temporary password is generated for root@localhost: -et)QoL4MLid
```
    
And root password is: -et)QoL4MLid
    
* Run the following command and follow instructions to reset the random root password and to set other security options.
    
```
$ sudo /usr/bin/mysql_secure_installation
```
    
* Connect to the mysql database

``` 
mysql -u root -p
```

### Clone Repository

Run the following series of commands in sequence to get the `cbex-core-nlp` code repository downloaded into your current directory.

```
$ git init
$ git clone https://<username>@bitbucket.org/cryptobex/cbex-nlp-core.git
$ cd cbex-nlp-core
$ git checkout <branch_name>
```

## Setup Database

### Dump Existing Dabase
To deploy the application from one server to another, you need to copy data in the database along with the database structure to the new server. 
Run the following the command to dump the database as an `.sql` file.

```
mysqldump -u <user> -p cbex_dataset > cbex_dataset.sql
```
Replace `<user>` by the user name of the databse, e.g. 'root'. This 
will export the database to `cbex_dataset.sql`, which then should be copied to the new server.

### Import Databse to New Server
On the new server, login to the mysql command prompt by executing the following command:

```
$ mysql -u <user> -p
```

Now create a database named `cbex_dataset`, and set the character encoding to `utf8mb4_unicode_ci`. Run the following MySQL commands 
to do create the database with the specified character encoding. 

```
> create database cbex_dataset;
> ALTER DATABASE cbex_dataset CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
> exit;
```

After creating the database, the last command (`exit;`) will logout the from the mysql command prompt.
Now import the dumped database file (`cbex_dataset.sql`) into the new database by running the command below:

```
$ mysql -u <user> -p cbex_dataset < cbex_dataset.sql
```

When the database import is complete, remove the dumped database file using the command:

```
$ rm cbex_dataset.sql
```

### Update Database Configuration
Finally, update only the database username and password, in the database config file located at `src/main/python/required_files/db_config.py`.


```python
db_config = {
    'user': '<username>',
    'password': '<password>',
    'database_name': 'cbex_dataset',

    'host': 'localhost',  # No need to change the host name unless database is located on a remote server
    'port': '3306',  # Change port number only if not using default setting
    'charset': 'utf8mb4'  # Do not change the charset
}
```

## Deploy

Execute the following commands (assuming that you are in the immediate parent directory of the `cbex-nlp-core` directory):

```
$ mkdir virtualenvs
$ cd virtualenvs
$ python3.6 -m venv cbex_py36
$ source cbex_py36/bin/activate
$ pip install pybuilder
$ cd ../cbex-nlp-core
$ pyb
```

The application will be deployed in the directory `target/dist/cbex-nlp-app-1.0.dev0`. Run the following following command to 
navigate to that directory:

```
$ cd target/dist/cbex-nlp-app-1.0.dev0 
```


## Run the Application
The CBEx Core NLP app has two main parts: automatic experiment to choose the best model and processing new articles by passing through 
the Core NLP workflow. 

### Experiment
Before running the experiment, setting up the experiment configuration is required. Create experiment configurations as below, 
where two configurations are shown (experiment id: exp_1 and exp_2). You can create more configurations under the dictionary 
`experiments`. Finally, save it to a python file, e.g. `config.py`.

```python
experiments = {
    'exp_1': {
        'clf_config': {
            'class_type': 'sentiment',
            'preprocessing_steps': ['lower', 'stemming'],
            'alter_class': [('neutral', 'negative')],
            'vectorizer': ['tfidf', 'dict_vect'],
            'vectorizer__dict_vect': {
                    'dictionary_path': 'required_files/dictionary_sentiment.py',
                },
            'vectorizer__tfidf': {'ngram_range': (1, 1)},
            'classifier': ['lr'],
        },
        'eval_config': {
            'train_test_split': [0.7, 0.3],  # only applies for grid search params
            'cv_times': 1,
            'cv': 5,
            'average': 'macro',
            'score': 'f1_score',
            'random_state': 11
        }
    },
    'exp_2': {
        'clf_config': {
            'class_type': 'title_sentiment',
            'preprocessing_steps': ['lower', 'stemming'],
            'alter_class': [('neutral', 'negative')],
            'vectorizer': ['tfidf', 'dict_vect'],
            'vectorizer__dict_vect': {
                    'dictionary_path': 'required_files/dictionary_sentiment.py',
                },
            'vectorizer__tfidf': {'ngram_range': (1, 1)},
            'classifier': ['lr'],
            'feature_selector': 'kbest',
            'feature_selector__kbest': {'k': 1700}
        },
        'eval_config': {
            'train_test_split': [0.7, 0.3],  # only applies for grid search params
            'cv_times': 1,
            'cv': 5,
            'average': 'macro',
            'score': 'f1_score',
            'random_state': 11
        }
    },
}
```

### Configure Experiments
Experiment configuration file can be configured using different options. There are three main configuration options: 
`'clf_config'`, `'grid_config'`, and `'eval_config'`.

* `'clf_config'`: This option in the configuration script can be used to configure preprocessig, vectorizer, and classifier.

  - `'class_type'`: The value for this option should be a string e.g. `'title_sentiment'`. The available values 
are `'coin'`, `'sentiment'`, `'tense'`, and `'title_sentiment'`. 
The system will load respective evaluation dataset based on the input.
    
  - `'preprocessing_steps'`: The input is a list of preprocessing steps e.g. `['lower', 'stemming']` or `None`. 
    The available values are: `'lower'`, `'remove_stopwords'` , `'remove_coin_names'`, `'remove_punctuation'`,
    `'lemmatize'`, `'stemming'`, and `'abstraction'`.
    
  - `'vectorizer'`: This option is used to specify the vectorizer algorithms. The value is a list of 
    vectorizer(s) e.g. `['tfidf']`. The availale values are `'tfidf'`
    ([Tfidf Vectorizer](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)), 
    `'count'`([Count Vectorizer](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html)), 
    `'hashing'`([Hashing Vectorizer](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.HashingVectorizer.html)) 
    and `'dict_vect'`([Dictionary-based Feature Extractor](core_nlp/dict_feature_extractor.py)). 
    To set any parameters to any of these vectorizers, a new configuration option should be specified by the option key 
    `'vectorizer__<vectorizer_key>'`. Please replace `<vectorizer_key>` by the desired vectorizer key. The value to 
    this option must be dictionary. An example is given below:
    ```
    'clf_config': {
        ...
        'vectorizer': ['tfidf', 'dict_vect'],
        'vectorizer__tfidf': {'ngram_range': (1, 1)},
        'vectorizer__dict_vect': {
            'dictionary_path': 'required_files/dictionary_sentiment.py',
            'case_sensitive': False,
            'longest_match': True
        },
        ...
     },
    ```
    _Note: If you use the DictFeatureExtractor, you must specify the dictionary file path otherwise the default coin 
    dictionary(located at `required_files/dictionary_coins.py`) will be used._ 

  - `'classifier'`: This option is used to specify the classifier. The value to this option must be a list of 
    classifier(s) e.g. `['lr', 'rf']`. The available values are 
    `'lr'`([Logistic Regression](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)), 
    `'rf'`([Random Forest](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)), 
    `'svm'`([Support Vector Machine](http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html)), 
    `'sgd`([Stochastic Gradient Descent ](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html)), 
    `'nb'`([Multinomial Naive Bayes](http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html)), 
    `'nn`([Neural Network](http://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)), 
    and `'dict_clf'` ([Dictionary-based Classifier](core_nlp/dictionary_based_classifier.py)). Please note, more than one item in the 
    value list will apply an Ensemble of the given classifier. Parameters to the individual classifiers can be set using 
    the option `'classifier__<classifier_key>'`, where the value to this option must be a dictionary. An example is 
    given below:
    
    ```
    'clf_config': {
        ...
        'classifier': ['lr', 'dict_clf'],
        'classifier__ensemble': {'voting': 'soft', weight': [0.1, 0.9]},
        'classifier__dict_clf': {
            'dictionary_path': 'required_files/dictionary_sentiment.py',
            'default_label': 'None',
            'class_weight': {'positive': 0.8, 'negative': 0.2}
        }
        ...
     },
    ```
    
    _Note: the dictionary path for the Dictioanry-based Classifier must be specified, otherwise the default Coin dictionary 
    (located at `required_files/dictionary_coins.py`) will be used_. 
  - `'feature_selector'`: The name of preprocessor algorithm. The available option is `'kbest'`([SelectKBest](http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectKBest.html)).
  - `'feature_selector__<feature_selector_key>'`: Parameters to configure the feature selector algorithm. `'<feature_selector_key>'` should be replaced by the feature selector key.
  
* `'grid_config'`: This configuration option is used to configure the grid search parameters. Any parameters 
offered by the vectorizers and classifiers can be configured. For vectorizers the configiration option key is 
`vectorizer__<vectorizer_key>__<parameter_key>` and for classifiers the option key is 
`classifier__<classifier_key>__<parameter_key>`. The values for each type of option must be a list of valid possible 
values offered by the respective algorithms. An example is given below:
  ```
  'grid_config': {
    'vectorizer__tfidf__ngram_range': [(1, 2), (1, 3)],
      'classifier__lr__penalty': ['l1', 'l2']
    },
  ``` 

* `'eval_config'`: This option is used to adjust the evaluation parameters. 

  - `'train_test_split'`: This option is used to specify the size of train and test data in every fold of a 
    k-fold cross-validation. The option must be a list of two float values where the first item in the list indicates 
    the size of train data and the other item is for test data size e.g. [0.7, 0.3]. _Note: This option is only applied when 
    performing Grid Search._
    
  - `'cv_times'`: This option is used to specify the number of times the k-fold cross-validation experiment should 
    run. The value must be a positive integer. 
    
  - `'cv'`: Specify the number of folds in a k-fold cross-validation. The value must be a positive integer.  
    
  - `'average'`: Define the averaging technique. The available options are `'micro'`, `'macro'`, `'weighted'`, and `'binary'`.
    
  - `'score'`: Specify the scoring type e.g. 'f1_score'. The vailable options are `'accuracy'`, `'precision'`, `'recall'`, `'f1-score'`
    
  - `'random_state'`: the random state to value to be applied to the experiment so that the results can be reproduced. 
    The value must be a positive integer number. 

### Run Experiment
Having the configuration file created, run the following the command to perform the experiment and update the best model.

```
$ python main.py --config config.py --output_dir <path to output files> --save_model yes --update_best_model yes
```

Replace the `<path to output files>` by the path to the directory output files will be saved. The options `--save_model`
and `--update_best_model` can be removed from the command or set to `no` if you want to just run the esperiment but not
to update the best model.  

When the experiment is complete, a directory is created 
on the name of the `class_type` in the configuration e.g. 'sentiment' and four types output items are be created in that directory:

1. `output.csv`, where results of each experient is be saved
2. `best_model_log.csv`, which contains the best model names and deployment dates
3. `tmp_models/`, the sub-directory where models from each experiment is temporarily saved. After choosing the best 
model all the rest of the models are removed from this directory
4. `models/`, the sub-directory where the best models are stored

The above experiment configuration and experiment was created for the Sentiment classification. A similar experiment 
should be configured and executed for the Tense classification before running the core NLP workflow. No experiment is needed for the 
Coin classification, because the coin classification is performed using the dictionary matching technique. The dictionary 
used in this classification is located at `required_files/dictionary.py`.

### Workflow

The Core NLP workflow reads articles saved as XML files after collecting from the RSS feed, applies saved best models for sentiment, tense etc., and finally insert information to the database. Execute the following the command to run the workflow:

```
python workflow_main.py --articles_base_dir <path/to/the/articles/base/dir/> --models_base_dir <path/to/the/models/base/dir/>
```
The command takes two directory paths, one is the base directory of RSS articles and the another one is the bese directory of saved 
models. If the RSS feed reader application is not configured yet, follow the 'RSS Article Collection' section to run the application. 

## RSS Article Collection
RSS article collection application is a separate application that collects live articles and download then to a specified 
directory as XML files. 

Open a new command prompt terminal and go to the root folder of your working directory (immediate parent directory of the `cbex-nlp-core/` directory). Run the commands below 
sequentially to download the app code repository. 

```
$ git clone https://hkayesh@bitbucket.org/cryptobex/cbex-news-retrieval.git
$ cd cbex-news-retrieval
$ git pull origin develop
```
Having the repository downloaded, run the following commands to deploy the application (assuming that you are in the immediate parent directory of the `cbex-news-retrieval` directory).

``` 
$ cd virtualenvs
$ python3.6 -m venv cbex_rss_py36
$ source cbex_rss_py36/bin/activate
$ pip install pybuilder
$ cd ../cbex-news-retrieval
$ pyb
```
The application is deployed to the directory `target/dist/cbex-annotation-task-1.0.dev0/`. Now move to that directory 
and run the following command:

```
$ python main.py --source_urls_file <path/to/rss_urls.txt> --articles_base_dir <path/to/articles/base/directory/>
```

The `--source_urls_file` option takes path to a text file that contains RSS feed source URLs (one URL per line). The 
other option `--articles_base_dir` take path to a directory where the downloaded articles are saved. 


## Setup Cron Jobs

### Run the RSS Feed Collection 
Some tasks might need to be run repeatedly, for example RSS article collection might 
need to run every 2 minutes. To configure that cron job, open the cron job setting file by executing:

``` 
$ crontab -e
```
Now append the following line to the opened file, which will run the article collection every 2 minutes and save the 
console output to the log file `rss_collection.log`. 

``` 
* * * * */2 cd <path/to/the/application/directory/> && ../../../../virtualenvs/cbex_rss_py36/bin/python main.py --source_urls_file <path/to/rss_urls.txt> --articles_base_dir <path/to/articles/base/directory/> >> rss_collection.log
```
The `<path/to/the/application/directory/>` refers to the absolute path from system root to the deployed code directory

### Run the Workflow
To run the workflow command repeatedly (every 5 minutes for example) append the following line:

```
* * * * */5 cd <path/to/the/application/directory/> && ../../../../virtualenvs/cbex_py36/bin/python workflow_main.py --articles_base_dir <path/to/the/articles/base/dir/> --models_base_dir <path/to/the/models/base/dir/> >> workflow.log
```
## Run Experiment from XML files

If you have a directory of MAE compatible xml files, you can run experiment on the XML data using the following command.
To run the experiment you should be in the root directory of the deployed application i.e. `target/dist/cbex-nlp-app-1.0.dev0/`.
Please remember to activate the appropriate virtual environment for this project before the experiment.

```
python xml_main.py --xml_dir <path/to/the/directory/of/xml/files/> --config <path/to/the/config/file/> --output <output/csv/file/path>
```
If you do not specify the output file path, the output will be saved to a file named `output.csv` in the current directory. 


## Authors

* **Humayun Kayesh**
* **Azad Dehghan** 
* **Arash Dehghan**

## License

All rights reserved by *DeepCognito Ltd*.

Module Licenses:
1. Matplotlib - license page URL: https://github.com/matplotlib/matplotlib/blob/master/LICENSE/LICENSE. Notable sesction 
from the licensing page: "_In the event Licensee prepares a derivative work that is based on or
incorporates matplotlib or any part thereof, and wants to
make the derivative work available to others as provided herein, then
Licensee hereby agrees to include in any such work a brief summary of
the changes made to matplotlib._"





## Acknowledgments

* Thanks to...

## Disclaimer
This project uses [pickle](https://docs.python.org/3/library/pickle.html) python object serialization module to save and load classifier models. This strategy 
of serializing and deserializing models have a potential drawback. A saved model might produce 
unexpected results if the model is saved in one version of sklearn but loaded in other version.

Read more about this issue [here](http://scikit-learn.org/stable/modules/model_persistence.html#security-maintainability-limitations). 


