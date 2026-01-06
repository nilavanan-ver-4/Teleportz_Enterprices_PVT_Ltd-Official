from app import create_app, db, Product

app = create_app()

with app.app_context():
    # Clear existing products if any
    Product.query.delete()
    
    products = [
        Product(
            name="Moon Walker Massage Chair",
            category="body massager",
            description="""The Moon Walker Massage Chair combines futuristic design with advanced functionality.
It features individual leg movement, 7D full-body massage, ergonomic zero gravity positioning,
hand squeezing massage, SL track, AI body scan, and capsule design.""",
            image_filename="moon_walker.jpg"
        ),

        Product(
            name="RX-7 Massage Chair",
            category="body massager",
            description="""RX-7 offers a 7D massage with SL track system, zero gravity positioning,
Bluetooth speaker, heating therapy, airbag massage, AI body scan, and voice control.""",
            image_filename="rx7.jpg"
        ),

        Product(
            name="RX-5 Elite Massage Chair",
            category="body massager",
            description="""RX-5 Elite includes automatic leg stretching, tri-motion calf rubbing,
feet scraping, full-body stretching, 7D massage, SL track, and zero gravity positioning.""",
            image_filename="rx5_elite.jpg"
        ),

        Product(
            name="Coin Operated Massage Chair",
            category="body massager",
            description="""Commercial heavy-duty massage chair with coin and QR-UPI operation,
7D massage, SL track, zero gravity positioning, minimalist kiosk design.""",
            image_filename="coin_operated.jpg"
        ),

        Product(
            name="RX-3 Massage Chair",
            category="body massager",
            description="""RX-3 features dual SL track system, tri-motion calf rubbing,
7D full-body massage, zero gravity, AI body scan, and airbag massage.""",
            image_filename="rx3.jpg"
        ),

        Product(
            name="Q7 2.0 Massage Chair",
            category="body massager",
            description="""Q7 2.0 offers Android touchscreen, calves rubbing, TikTok/Reels controller,
7D massage, SL track, zero gravity, heating, and airbag massage.""",
            image_filename="q7_2.jpg"
        ),

        Product(
            name="Q5 Massage Chair",
            category="body massager",
            description="""Q5 provides 7D massage, SL track design, zero gravity positioning,
Bluetooth speaker, therapeutic heating, airbag massage, and AI body scan.""",
            image_filename="q5.jpg"
        ),

        Product(
            name="R10 Massage Chair",
            category="body massager",
            description="""R10 includes 7D massage, AI body scan, SL track system,
zero gravity positioning, Bluetooth speaker, heating, and voice control.""",
            image_filename="r10.jpg"
        ),

        Product(
            name="R9 Massage Chair",
            category="body massager",
            description="""R9 delivers 7D full-body massage, SL track, zero gravity,
Bluetooth speaker, heating therapy, airbag massage, and AI body scan.""",
            image_filename="r9.jpg"
        ),

        Product(
            name="R8 Pro Massage Chair",
            category="body massager",
            description="""R8 Pro features upgraded faux leather, thigh massage straps,
4D full-body massage, fixed roller system, zero gravity, and Bluetooth speaker.""",
            image_filename="r8_pro.jpg"
        ),

        Product(
            name="R7 Neo Massage Chair",
            category="body massager",
            description="""R7 Neo offers 4D full-body massage, strong metal frame,
zero gravity positioning, Bluetooth speakers, heating, and airbag massage.""",
            image_filename="r7_neo.jpg"
        ),

        Product(
            name="R6 Massage Chair",
            category="body massager",
            description="""R6 includes solid wooden frame, 4D massage system,
therapeutic heating, targeted thigh massage, and full-body relaxation.""",
            image_filename="r6.jpg"
        ),
    ]

    db.session.bulk_save_objects(products)
    db.session.commit()

    print("Products inserted successfully into SQLite database")