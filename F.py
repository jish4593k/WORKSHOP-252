import scrapy
import os
import urllib.request
from scrapy.crawler import CrawlerProcess
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

class PdfDownloader(scrapy.Spider):
    name = 'pdf_downloader'
    # domain URL
    allowed_domains = ['example.com']

    start_urls = ['http://example.com/slides/']

    def parse(self, response):
       
        selector = 'table tr td a[href$=".pdf"]::attr(href)'
        for href in response.css(selector).extract():
            yield scrapy.Request(
                url=response.urljoin(href),
                callback=self.save_pdf
            )

    def save_pdf(self, response):
       
        path = response.url.split('/')[-1]
        self.logger.info('Saving PDF %s', path)
        
        pdf_directory = os.path.join(os.getcwd(), 'PDFs')
        os.makedirs(pdf_directory, exist_ok=True)
        
        pdf_path = os.path.join(pdf_directory, path)
        
       
        with urllib.request.urlopen(response.url) as response_pdf, open(pdf_path, 'wb') as file:
            file.write(response_pdf.read())

        self.log(f"PDF saved at {pdf_path}")

def neural_network_example():

    model = Sequential()
    model.add(Dense(10, input_dim=1, activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.compile(optimizer='adam', loss='mean_squared_error')

   
    X = [1, 2, 3, 4, 5]
    y = [3, 4, 2, 5, 6]

    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    model.fit(X_train, y_train, epochs=10, verbose=0)

   
    new_data = [6, 7, 8]
    predictions = model.predict(new_data)

    print("Neural Network Predictions:", predictions)

if __name__ == "__main__":
 
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })

    process.crawl(PdfDownloader)
    process.start()

    
    neural_network_example()
