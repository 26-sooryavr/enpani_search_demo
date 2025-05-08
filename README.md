# EnPani Search

> A simple semantic search app for [EnPani episodes](https://m.youtube.com/playlist?list=PLhrdHlkOIj-W8D_Rj76-4Z0J9d0cjoIuI) for anyone looking to learn more from Sri U Ve Velukkudi Krishnan Swamy. 
> This was attempted as a Proof Of Concept so episodes before 1245 and after 3506 are not searchable yet.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)


### Prerequisites

Please ensure you have Python 3.x installed. This project was tested with Python 3.11 but lower versions may be compatible too.

## Installation

Clone the repository and install dependencies in a python virtual env:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
```
python -m venv venv

.\venv\Scripts\activate        # on Windows
source venv/bin/activate       # On macOS/Linux

pip install -r requirements.txt
```

## Configuration

Add the following 3 variables into a `.env` file in this project root directory where this `README.md` file is found.

```text
MILVUS_DB_PATH="enpani.db"
RETURN_K_RESULTS=10
DB_COLLECTION_NAME="demo_collection_on_en_text"
```
options for `DB_COLLECTION_NAME` are:
* demo_collection_on_en_text (works best for now)
* demo_collection_on_title
* demo_collection

These collections have used different information about each episode to embed each episode into a dense vector for semantic search.

## Usage

Activate the venv from the installation step and run the following command. Open this [link](http://localhost:8501) on **Google Chrome** browser (safari does not work as of writing)

```bash
streamlit run streamlit_app.py
```

### Please note: 
Upon the first startup of the app, the `load_model` method pulls the [bge_m3 model](https://milvus.io/docs/embed-with-bgm-m3.md) and can take *up to an hour* depending on internet speed. Subsequent startups will complete in less than a minute.

## Contributing

Author has a long way to go in terms of proficiency (both technically and spiritually) so any feedback is most welcome 🙏 
Please forgive any mistakes and feel free to raise a pull request, thank you! 🙏

