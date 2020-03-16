# View only file
from app import app
from flask_dj import urls

_path = urls.Path(app)
add_absolute_path = _path.add_absolute_path
add_relative_path = _path.add_relative_path  # Use in app/urls
relative_path = _path.relative_path  # Use in other apps
include = urls.include
