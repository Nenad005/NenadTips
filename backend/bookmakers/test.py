import os

def create_python_files():
    current_dir = os.getcwd()

    folders = [folder for folder in os.listdir(current_dir) if os.path.isdir(folder)]

    for folder in folders:
        file_path = os.path.join(current_dir, folder, folder.lower() + ".py")
        with open(file_path, 'w') as f:
            f.write(f"import sys\n")
            f.write(f"sys.path.insert(1, '../')\n")
            f.write(f"from bookmaker import Bookmaker\n\n")
            f.write(f"class {folder}(Bookmaker):\n")
            f.write(f"    def __init__(self):\n")
            f.write(f"        super().__init__('{folder}')\n\n")
            f.write(f"    def getAllMatchOdds():\n")
            f.write(f"        pass\n")
            f.write(f"        # Implement getAllMatchOdds method for {folder}\n")
            f.write(f"    def getMatchOdds(link):\n")
            f.write(f"        pass\n")
            f.write(f"        # Implement getMatchOdds method for {folder}\n")
    
if __name__ == "__main__":
    create_python_files()

# import datetime

# timestamp = 1707148800000
# date = datetime.datetime.utcfromtimestamp(timestamp / 1000)
# print(date.strftime('%Y-%m-%d %H:%M:%S')) 
