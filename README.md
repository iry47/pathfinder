# Getting Started

TODO

For having more information about the project and the methodology, please see the document "Report.pdf" in the root of the project`

## The components

You can see all the three component necessary for the project in the folder `/docs/jupyter-components`
There you will have :

- Audio recorder

- NLP component

- Transcript component

- Pathfinder component

## Launch interface

The infrastructure is made in Python with Flask framework

1. First, you need to go to the infrastructure directory `cd /app/back`

2. Then, you need to install all dependencies `pip install -r requirements.txt`

3. Install all this module :
`pip install langdetect`
`pip install icecream`
`pip install spacy`
`python -m spacy download fr_core_news_md`

4. If you have any missing module during the installtion. Just run the command `pip install name_module`

5. After the project installation is complete, you can launch the app `python app.py`
