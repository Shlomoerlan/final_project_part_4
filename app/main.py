from threading import Thread
from flask import Flask
from app.routes.search_routes import search_routes
from app.service.fetch_service import process_news_every_2_min
from app.service.init_elastic import create_index
from app.utills.utills_functions import import_historic_data

app = Flask(__name__)
app.register_blueprint(search_routes)


if __name__ == '__main__':
    create_index()
    Thread(target=process_news_every_2_min, daemon=True).start()
    app.run(port=5002, debug=True)

    import_historic_data(
        main_csv_path='./data/globalterrorismdb_1000.csv',
        secondary_csv_path='./data/RAND_Database_5000.csv'
    )

