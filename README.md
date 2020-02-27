# InsPlagiarism
InsPlagiarism 

In the first terminal, go inside the ui folder using cd ui.

yarn install
npm install -g serve
npm run build
serve -s build -l 3000


On the second terminal, move inside the service folder using cd service.

On Windows:

py -m venv env
.\env\Scripts\activate

pip install -r requirements.txt


set FLASK_APP=app
flask run