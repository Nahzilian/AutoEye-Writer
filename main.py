from google.oauth2.credentials import Credentials

from modules.google_func import get_files_id, get_google_cred, get_file_by_id
import json

def main() -> None:
    cred: Credentials = get_google_cred()
    files = get_files_id(cred)
    print(files[0])
    test_file_data = get_file_by_id(files[0], cred)
    with open('./assets/data/temp.json', 'w') as f:
        # f.write(test_file_data)
        json.dump(test_file_data, f)

    

if __name__ == '__main__':
    main()