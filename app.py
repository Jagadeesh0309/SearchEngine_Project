from flask import Flask, request, render_template
from VectorSpaceModel import VectorSpaceModel
from WebCrawler import WebsiteCrawler

app = Flask(__name__)

URLMap = WebsiteCrawler("https://ku.edu/", 10)
In = VectorSpaceModel()
In.IndexBuilding(URLMap)
print("Server Ready !")

@app.route('/')
def index():
    return render_template('SearchPage.html')

@app.route('/search')
def search():
    query = request.args.get('q')
    In.QueryIndex(query)
    results = In.SearchResultsRanking()
    return render_template('ResultsPage.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)
