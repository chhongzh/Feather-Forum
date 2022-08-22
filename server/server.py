# ---------------------------------------------------------------------------
from maps import post
from maps import user
from maps import other
from flask import Flask
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
app = Flask(__name__)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
app.register_blueprint(post.blueprint)
app.register_blueprint(user.blueprint)
app.register_blueprint(other.blueprint)


app.run(port=14524, debug=True)
