import os
from view import app

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0",
            # app.run(debug=True, host="127.0.0.1",
            port=int(os.environ.get("PORT", 5000)))
