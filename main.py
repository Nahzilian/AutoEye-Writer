from google.oauth2.credentials import Credentials

from modules.google_func import get_files_id, get_google_cred, get_file_by_id

from modules.google_object import GoogleDoc

def main() -> None:
    cred: Credentials = get_google_cred()
    files = get_files_id(cred)
    # print(files[0]) #Print first file ID (only need 1)
    # Get file by id
    
    test_file = get_file_by_id(files[0], cred) 
    
    # Assign with new class (GoogleDoc)
    # print(test_file)
    document = GoogleDoc(test_file)
    
    document.extract()
    document.write_to_html()


if __name__ == '__main__':
    main()