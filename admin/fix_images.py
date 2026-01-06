from app import create_app, db, Product

app = create_app()

with app.app_context():
    # Get all products and set image_filename to None for non-existent files
    products = Product.query.all()
    for product in products:
        if product.image_filename:
            print(f"Product: {product.name}, Image: {product.image_filename}")
            # Set to None since the referenced files don't exist
            product.image_filename = None
    
    db.session.commit()
    print("Updated all products to have no image references")