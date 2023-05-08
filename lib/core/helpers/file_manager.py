import shutil


class FileManager:

    @staticmethod
    def clear_path(path):
        return path[:-1] if path.endswith('/') else path

    @staticmethod
    def copy_file(source_folder, target_folder, filename):
        source_folder = FileManager.clear_path(source_folder)
        target_folder = FileManager.clear_path(target_folder)
        shutil.copyfile(f'{source_folder}/{filename}', f'{target_folder}/{filename}')
