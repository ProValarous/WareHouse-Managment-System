# imports 
from flask import Flask, render_template, request, redirect, url_for
import json

# Making a empty diction for warehouse
WAREHOUSE = {}
MIN_COUNT = 10

# Saing data locally as warehouse.json
def saveData():
    if WAREHOUSE:
        with open("warehouse.json", "w") as file:
            json.dump(WAREHOUSE, file)

# loading data from warehouse.json
def loadDictionary():
    global WAREHOUSE
    with open("warehouse.json", "r") as file:
        WAREHOUSE = json.load(file)
    return WAREHOUSE
    
# adding item to queue
def addToQueue(queue, item):
    return queue.append(item)

# merge sort algorithm
def mergeSort(arr):
    if len(arr) > 1:
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]
        mergeSort(L)
        mergeSort(R)
        i = j = k = 0
 
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
 
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
 
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr 

# ? @@ ADD - UPDATE - DELETE - FETCH || PRODUCTS
def addToWarehouse(name, colors, description, location, category, count):
    if category not in getCategories():
        addCategory(category)
    newProduct = {
        "name": name,
        "colors": colors, 
        "description": description, 
        "location": location,
        "category": category,
        "count": count,
        "newName": ""
    }
    WAREHOUSE["products"][name] = newProduct
    saveData()
    
def updateProductInWarehouse(name, updatedName, updatedColors, updatedDescription, updatedLocation, updatedCategory, updatedCount):
    if name in WAREHOUSE["products"]:
        if updatedCount:
            WAREHOUSE["products"][name]["count"] = updatedCount
        if updatedName != "":
            WAREHOUSE["products"][name]["newName"] = updatedName
        if updatedColors:
            WAREHOUSE["products"][name]["colors"] = updatedColors
        if updatedDescription != "":
            WAREHOUSE["products"][name]["description"] = updatedDescription
        if updatedLocation != "":
            WAREHOUSE["products"][name]["location"] = updatedLocation
        if updatedCategory != "":
            if updatedCategory not in getCategories():
                addCategory(updatedCategory)
            WAREHOUSE["products"][name]["category"] = updatedCategory
            
    else:
        return "Product Not Found !!"
    saveData()

def deleteProductFromWarehouse(name):
    if name in WAREHOUSE["products"]:
        del WAREHOUSE["products"][name]
    else:
        return "Product Not Found !!"
    saveData()

def getProductWithLowerCount(minCount):
    resultProducts = []
    for productKey in WAREHOUSE["products"]:
        product = WAREHOUSE["products"][productKey]
        if product["count"] < minCount:
            resultProducts.append(productKey)
    return resultProducts

def fetchProductsFromWarehouse():
    products = mergeSort(list(WAREHOUSE["products"].keys()))
    sortedProducts = {}
    for product in products:
        sortedProducts[product] = WAREHOUSE["products"][product]
    return sortedProducts

def fetchProductsByName(name):
    return WAREHOUSE["products"][name]

# ? @@ ADD - UPDATE - DELETE - FETCH || CATEGORIES
def addCategory(name):
    queue = WAREHOUSE["categories"]
    addToQueue(queue, name)

def updateCategory(name, updatedName):
    queue = WAREHOUSE["categories"]
    for index, data in enumerate(queue):
        data = queue[index]
        if data == name:
            queue[index] = updatedName

def removeCategory(name):
    queue = WAREHOUSE["categories"]
    for index, data in enumerate(queue):
        data = queue[index]
        if data == name:
            queue.pop(index)

def getCategories():
    return WAREHOUSE["categories"]

# increasing product count by 1 
def increaseProductCount(name):
    if name in WAREHOUSE["products"]:
        WAREHOUSE["products"][name]["count"] += 1
    else:
        return "Product Not Found !!"
    saveData()

# decreasing product count by 1 
def decreaseProductCount(name):
    if name in WAREHOUSE["products"]:
        if WAREHOUSE["products"][name]["count"] > 0:
            WAREHOUSE["products"][name]["count"] -= 1
    else:
        return "Product Not Found !!"
    saveData()

# def 


# addCategory("name")
# print(getCategories())
# updateCategory("name", "category5")
# print(getCategories())
# removeCategory("category5")
# print(getCategories())

# print(fetchProductsFromWarehouse())
# addToWarehouse("item2", ["black"], "dadasdasd", "A", "category5")
# print(fetchProductsFromWarehouse())
# updateProductInWarehouse("item2", "item234", ["black"], "dadasd", "dasd", "category7")
# print(fetchProductsFromWarehouse())
# deleteProductFromWarehouse("item2")
# print(fetchProductsFromWarehouse())

# print(saveData())
# print(loadDictionary())

# ? Creating app with Flask
app = Flask(__name__)

# homePAge route
@app.route('/', methods=['GET'])
def index():
    loadDictionary()
    return render_template('index.html', products=fetchProductsFromWarehouse() )

# Get - transfer data from server(Code) to html
# Post - tranfer data from html form to server(Code)

# add product route
@app.route('/addproduct', methods=['GET', 'POST'])
def add_product():
    # POST with form data
    if request.method == "POST":
        name = request.form.get("name")
        colors = request.form.get("colors")
        colors = [color.strip().title() for color in colors.split()]
        description = request.form.get("description")
        # catogory = 
        count = int(request.form.get("count"))
        location = request.form.get("location")
        category = request.form.get("category")

        addToWarehouse(name, colors, description, location, category, count)
        return redirect(url_for("index"))
    # GET - return html page
    return render_template('add_product.html', categories=getCategories())

# delete product route
@app.route('/deleteproduct/<path:name>', methods=['GET'])
def delete_product(name):
    loadDictionary()
    print(deleteProductFromWarehouse(name))
    return redirect(url_for("index"))

# update product route
@app.route('/updateproduct/<path:name>', methods=['GET', "POST"])
def update_product(name):
    loadDictionary()
    # GET - to get data of current product
    if request.method == "GET":
        return render_template('update_product.html', data=fetchProductsByName(name), categories=getCategories())
    elif request.method == "POST":
        updatedName = request.form.get("name")
        updatedColors = request.form.get("colors")
        updatedColors = [color.strip().title() for color in updatedColors.split()]
        updatedDescription = request.form.get("description")
        updatedCount = int(request.form.get("count"))
        updatedLocation = request.form.get("location")
        updatedCategory = request.form.get("category")
        updateProductInWarehouse(name, updatedName, updatedColors, updatedDescription, updatedLocation, updatedCategory, updatedCount)
    return redirect(url_for("index"))

# product details route
@app.route('/product/<path:name>', methods=['GET'])
def productDetails(name):
    loadDictionary()
    return render_template('product_details.html', data=fetchProductsByName(name))

# increasing product count route
@app.route('/increaseCount/<path:name>', methods=['GET'])
def increaseCountOfProduct(name):
    loadDictionary()
    increaseProductCount(name)
    return redirect(url_for("productDetails", name=name))

# decreasing product count route
@app.route('/decreaseCount/<path:name>', methods=['GET'])
def decreaseCountOfProduct(name):
    loadDictionary()
    decreaseProductCount(name)
    return redirect(url_for("productDetails", name=name))
    
# searching prouct route
@app.route('/search', methods=['GET', "POST"])
def searchProduct():
    if request.method == "POST":
        name = request.form.get("search")
        loadDictionary()
        data = fetchProductsFromWarehouse()
        keys = list(data.keys())
        searchResults = {}
        for key in keys:
            print(name, keys)
            if name in key or name == key:
                searchResults[key] = data[key]
        print(searchResults)
        return render_template('search_results.html', data=searchResults, name=name)
    return redirect(url_for("index"))

# rrunning app on debug mode.  
if __name__ == "__main__": 
    app.run(debug=True)