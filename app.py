from flask import Flask, request, render_template, session
import csv
import os
from fileinput import filename
import pandas as pd
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
# Configure upload file path flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'This is your secret key to utilize session in Flask'


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files.get('file')
        # data_filename = "product_data.csv"
        data_filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], data_filename))
        session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], data_filename)
        return render_template('index.html')
    return render_template("index.html")


@app.route("/csv", methods=['GET', 'POST'])
def home():
    data = []
    if request.method == 'POST':
        url = request.form['shop_url']
        print(url)
        # Open WooCommerce CSV file for reading
        with open('woocommerce_csv', 'r') as woocommerce_file:
            woocommerce_reader = csv.DictReader(woocommerce_file)

            # Create Shopify CSV file and write header row
            with open('shopify_csv', 'w', newline='') as shopify_file:
                shopify_writer = csv.writer(shopify_file)
                shopify_writer.writerow(
                    ['Handle', 'Title', 'Body (HTML)', 'Vendor', 'Type', 'Tags', 'Published', 'Option1 Name',
                     'Option1 Value', 'Option2 Name', 'Option2 Value', 'Option3 Name', 'Option3 Value', 'Variant SKU',
                     'Variant Grams', 'Variant Inventory Tracker', 'Variant Inventory Qty', 'Variant Inventory Policy',
                     'Variant Fulfillment Service', 'Variant Price', 'Variant Compare At Price',
                     'Variant Requires Shipping', 'Variant Taxable', 'Variant Barcode', 'Image Src', 'Image Position',
                     'Image Alt Text', 'Gift Card'])

                # Loop through each row in WooCommerce CSV file and write to Shopify CSV file
                for woocommerce_row in woocommerce_reader:
                    # Create Shopify CSV row with necessary fields
                    shopify_row = []
                    shopify_row.append(woocommerce_row['Slug'])
                    shopify_row.append(woocommerce_row['Name'])
                    shopify_row.append(woocommerce_row['Description'])
                    shopify_row.append(woocommerce_row['Brand'])
                    shopify_row.append(woocommerce_row['Category'])
                    shopify_row.append(woocommerce_row['Tags'])
                    shopify_row.append('TRUE' if woocommerce_row['Status'] == 'publish' else 'FALSE')
                    shopify_row.append('Title')
                    shopify_row.append(woocommerce_row['Attribute 1 name'])
                    shopify_row.append(woocommerce_row['Attribute 1 value'])
                    shopify_row.append('Title')
                    shopify_row.append('')
                    shopify_row.append('Variant')
                    shopify_row.append(woocommerce_row['SKU'])
                    shopify_row.append(woocommerce_row['Weight'])
                    shopify_row.append('shopify')
                    shopify_row.append(woocommerce_row['Stock'])
                    shopify_row.append('deny')
                    shopify_row.append('manual')
                    shopify_row.append(woocommerce_row['Price'])
                    shopify_row.append('')
                    shopify_row.append('TRUE')
                    shopify_row.append('TRUE')
                    shopify_row.append(woocommerce_row['Barcode'])
                    shopify_row.append(woocommerce_row['Image URL'])
                    shopify_row.append('')
                    shopify_row.append(woocommerce_row['Name'])

                    # Write Shopify CSV row to file
                    shopify_writer.writerow(shopify_row)

    return render_template('index.html', data=data)


@app.route("/etsy")
def etsy():
    data_list = []
    with open('etsy-ursl.csv', mode='r') as csv_file, \
            open('etsy_product_data.csv', mode='w', newline='') as output_file:

        writer = csv.writer(output_file)
        writer.writerow(
            ["SL", "Title", "Description", "Price", "Price SKU", "QUANTITY", "TAGS", "MATERIALS", "Image",
             "Variation 1 Type",
             "Variation 1 Name", "Variation 1 Values", "Variation 2 Type", "Variation 2 Name", "Variation 2 Values",
             "SKU Data Listing ID", "Price SKU", "Product URL"])

        reader = csv.reader(csv_file)
        # Loop through each row in the Etsy CSV file and convert it to Shopify format
        for csvrow in reader:
            # Skip the header row
            if reader.line_num == 1:
                continue

            # The URL of the product page to scrape
            print(csvrow[0], reader.line_num)
            url = csvrow[0]

    return render_template('product-list.html', data=data_list)
