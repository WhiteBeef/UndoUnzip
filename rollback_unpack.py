import zipfile
import hashlib
import os
import sys
import tempfile

def file_hash(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def remove_empty_dirs(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                try:
                    os.rmdir(dir_path)
                    print(f"[✓] Удалена пустая директория: {dir_path}")
                except Exception as e:
                    print(f"[!] Не удалось удалить директорию {dir_path}: {e}")

def rollback_zip(zip_path):
    base_dir = os.path.dirname(zip_path)
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)
        
        for root, _, files in os.walk(tmpdir):
            for name in files:
                rel_path = os.path.relpath(os.path.join(root, name), tmpdir)
                extracted_file = os.path.join(root, name)
                target_file = os.path.join(base_dir, rel_path)

                if os.path.exists(target_file):
                    if file_hash(extracted_file) == file_hash(target_file):
                        try:
                            os.remove(target_file)
                            print(f"[✓] Удалён: {rel_path}")
                        except Exception as e:
                            print(f"[!] Не удалось удалить {rel_path}: {e}")
        
        remove_empty_dirs(base_dir)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Передайте путь к архиву.")
        sys.exit(1)
    rollback_zip(sys.argv[1])