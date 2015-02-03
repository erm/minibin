from minibin import create_app
from minibin.config import ProductionConfig

app = create_app(ProductionConfig)

if __name__ == '__main__':
    app.run()
