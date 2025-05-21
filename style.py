def load_custom_css():
    return """
    <style>
        html, body {
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f6f9;
            color: #2c3e50;
        }

        .stApp {
            padding: 2rem;
            background-color: #f4f6f9;
        }

        .product-card {
            max-width: 260px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .product-card-img {
            width: 100%;
            aspect-ratio: 1 / 1;
            object-fit: cover;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .product-card .product-title {
            font-weight: bold;
            font-size: 1rem;
            color: #333;
            margin-top: 10px;
            text-align: center;
        }

        .stButton > button {
            background-color: #007acc;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-size: 14px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .stButton > button:hover {
            background-color: #005fa3;
        }

        .scroll-button {
            background: transparent;
            border: none;
            color: #007acc;
            font-size: 2rem;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: color 0.3s ease;
        }

        .scroll-button:hover {
            color: #005fa3;
        }

        .scroll-container {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 300px;
        }
    </style>
    """
