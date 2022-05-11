import os
from datetime import datetime

class FileManager:
    """
    In the system post directory, a photo should be saved like this:
    '1-Post text'
    '2-Post text'
    '{n-9}-Post text...'
    
    FileManager will recognize priority by the first number in file name, wich must be one character.
    FileManager will recognize text after 'number + hyphen' as text to be posted with the photo.
    """
    def __init__(self, base_dir=f"{os.getcwd()}"):
        self.base_dir=f"{base_dir}\\posts\\"
        self.photos=sorted(os.listdir(self.base_dir))
        
    def _get_first_file_name(self):
        return self.photos[0]
        
    def get_photo_path(self):
        return self.base_dir+self._get_first_file_name()
    
    def get_post_text(self):
        return self._get_first_file_name()[0][2:]
    
    def rename_posted_photo(self, photo=None):
        photo = photo or self._get_first_file_name()
        os.rename(self.base_dir+photo,self.base_dir+f"[{datetime.today().strftime('%Y-%m-%d')}, 'POSTED']"+photo)