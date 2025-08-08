import os
import sys
import types
from unittest.mock import MagicMock


class SessionState(dict):
    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self[key] = value

# Ensure the application module is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Stub external dependencies before importing the app module
streamlit_stub = MagicMock()
streamlit_stub.session_state = SessionState()
streamlit_stub.selectbox.return_value = 'u2net'
streamlit_stub.file_uploader.return_value = []
streamlit_stub.button.return_value = False
sys.modules['streamlit'] = streamlit_stub
sys.modules['streamlit_image_comparison'] = MagicMock()

rembg_stub = types.ModuleType("rembg")
rembg_stub.remove = MagicMock()
rembg_bg_stub = types.ModuleType("rembg.bg")
rembg_bg_stub.new_session = MagicMock()
rembg_stub.bg = rembg_bg_stub
sys.modules['rembg'] = rembg_stub
sys.modules['rembg.bg'] = rembg_bg_stub

from app import process_image


def test_process_image_naming(monkeypatch):
    """Ensure processed images are named correctly."""

    # Replace heavy functions with lightweight stubs
    def fake_new_session(model_name):
        return None

    def fake_remove(image, session=None):
        return image

    monkeypatch.setattr('app.new_session', fake_new_session)
    monkeypatch.setattr('app.remove', fake_remove)

    from PIL import Image
    from io import BytesIO

    # Create an in-memory JPEG image
    img = Image.new('RGB', (10, 10), color='red')
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    buffer.name = 'sample.jpg'
    buffer.seek(0)

    result = process_image(buffer, 'u2net')

    assert result['name'].endswith('_no_bg.png')
    base, ext = os.path.splitext(buffer.name)
    assert f"{ext}_no_bg" not in result['name']
