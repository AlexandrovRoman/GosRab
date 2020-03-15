# View only file
from app import app
from Flask_DJ import urls

path = urls.Path(app)
add_absolute_path = path.add_absolute_path
add_relative_path = path.add_relative_path
relative_path = path.relative_path
include = urls.include
