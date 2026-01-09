from app import create_app, db, Product

app = create_app()

with app.app_context():
    # Clear existing products if any
    Product.query.delete()
    
    products = [
        Product(
            name="Organic Basmati Rice",
            category="Agricultural Products",
            description="Premium long-grain aged Basmati rice sourced from the foothills of the Himalayas. GMO-free, high aroma, and superior taste. Available in 10kg, 20kg bulk packing.",
            image_filename="basmati_rice.jpg"
        ),
        Product(
            name="Industrial Grade Steel Valves",
            category="Industrial Materials",
            description="High-pressure stainless steel ball valves for oil and gas applications. Certified ISO 9001. Corrosion resistant and durable under extreme temperatures.",
            image_filename="steel_valves.jpg"
        ),
        Product(
            name="Premium Combed Cotton Yarn",
            category="Textiles",
            description="100% organic combed cotton yarn for high-end apparel manufacturing. Soft texture, high tensile strength, and eco-friendly dyeing process.",
            image_filename="cotton_yarn.jpg"
        ),
        Product(
            name="Smart LED Driver Modules",
            category="Electronics",
            description="Advanced constant current LED drivers with surge protection and dimming capabilities. Ideal for commercial and industrial lighting solutions.",
            image_filename="led_driver.jpg"
        ),
        Product(
            name="Cold Pressed Virgin Coconut Oil",
            category="Agricultural Products",
            description="Pure, unrefined, and cold-pressed virgin coconut oil for culinary and cosmetic use. Sourced from certified organic coastal plantations.",
            image_filename="coconut_oil.jpg"
        ),
        Product(
            name="Precision CNC Machined Parts",
            category="Industrial Materials",
            description="Custom-engineered metal components using advanced CNC technology. High tolerance levels (up to +/- 0.005mm) for aerospace and automotive industries.",
            image_filename="cnc_parts.jpg"
        ),
        Product(
            name="Silk Jacquard Fabric",
            category="Textiles",
            description="Luxury silk jacquard fabric with intricate patterns. Perfect for high-fashion garments and premium upholstery. Hand-woven by master artisans.",
            image_filename="silk_fabric.jpg"
        ),
        Product(
            name="Industrial IoT Gateway",
            category="Electronics",
            description="Ruggedized IoT gateway for smart factory automation. Supports multiple protocols including MQTT, Modbus, and OPC-UA. Wide operating temperature range.",
            image_filename="iot_gateway.jpg"
        )
    ]

    db.session.bulk_save_objects(products)
    db.session.commit()

    print("Products inserted successfully into SQLite database")