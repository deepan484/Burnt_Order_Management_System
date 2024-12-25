from flask import Flask, render_template, request 
from functions import backend , calculate_order_summary
import uuid
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_input():
    user_input = request.form['grocery_input']
    
    # Get results from backend
    results = backend(user_input)
    
    
    # Handle errors
    if "error" in results:
        return render_template('index.html', error=results["error"])
    
    # Pass results to the template
    return render_template('index.html', results=results)

@app.route('/place_order', methods=['POST'])
def place_order():
    # Get the order details from the form
    order_details = request.form.getlist('order_details')
    
    order, total_price = calculate_order_summary(order_details)
    order_id = str(uuid.uuid4())
    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Pass the order summary to the template
    return render_template('new.html', order=order, order_id = order_id, order_date = order_date, total_price=total_price)

if __name__ == '__main__':
    app.run(debug = True, use_reloader = False)
