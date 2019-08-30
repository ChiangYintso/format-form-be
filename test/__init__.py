import os
from application import Application

OPEN_ID = 'ouQQw5cwnNTsk1gFmztEVlMljK_8'

cur_dir = os.path.dirname(__file__)

app = Application(__name__, root_path=os.path.dirname(cur_dir))
client = app.test_client()
