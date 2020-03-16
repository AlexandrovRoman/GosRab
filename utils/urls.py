# View only file
from app import app
from Flask_DJ import urls

_path = urls.Path(app)
add_absolute_path = _path.add_absolute_path
add_relative_path = _path.add_relative_path
relative_path = _path.relative_path
include = urls.include
