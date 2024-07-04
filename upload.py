from tiktok_uploader.upload import upload_video
from tiktok_uploader.auth import AuthBackend
import os

upload_video(os.path.join('output', 'english.mp4'), cookies='www.tiktok.com_cookies.txt')