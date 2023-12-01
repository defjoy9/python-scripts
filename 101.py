import os
import zipfile
import datetime
import logging

def zip_directory(input_path, output_path, current_date, log_file):
    output_zip = os.path.join(output_path, f"Backupy-Account-{current_date}.7z") # specifies where to create and what name should 7z file have 
    
    print("Please stand by... script is running in the background")

    # Configuration of how logs should look in log.txt
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # checks if 7z file already exists
    if os.path.exists(output_zip) and zipfile.is_zipfile(output_zip):
        print("This 7z file already exists! Exiting...")
        logging.error(f"{output_zip} file already exists! failed to run the script")
        return 
    
    # creates 7z file
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        file_names = [] # list of all files/directories
        zipped_file_names = [] # list of zipped files/directories

        for root, dirs, files in os.walk(input_path):
            # checks every file in a given path
            for file in files:
                # adds files to a list 
                file_names.append(file)
                # checks if the file matches today's date
                if current_date in file:
                    # if yes, adds it to the 7z file and creates a log
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, input_path)
                    zipf.write(file_path, arcname=arcname)
                    zipped_file_names.append(file)
                    logging.info(f"Added: {file}")
                else:
                    # if not, skips the file and creates a log
                    logging.info(f"Skipped: {file} (Does not contain current date)")
            # checks every directory in a given path
            for dir in dirs:
                file_names.append(dir)
                # checks if the directory matches today's date
                if current_date in dir:
                    # if yes, adds it to the 7z file and creates a log
                    dir_path = os.path.join(root, dir)
                    arcname = os.path.relpath(dir_path, input_path)
                    zipf.write(dir_path, arcname=arcname)
                    zipped_file_names.append(dir)
                    logging.info(f"Added: {dir}")
                else:
                    # if not, skips the directory and creates a log
                    logging.info(f"Skipped: {dir} (Does not contain current date)")
        # Creates a Summary in log with most important information
        logging.info(f"All names of files in {input_path}: {file_names}")
        logging.info(f"Count of all names of files in {input_path}: {len(file_names)}")
        logging.info(f"All names of files that are zipped: {zipped_file_names}")
        logging.info(f"Count of all names of files that are zipped: {len(zipped_file_names)}")
    
    # Removes files and directories that are zipped in a given path
    for item in zipped_file_names:
        item_path = os.path.join(input_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
            logging.info(f"Deleted: {item_path}")
        elif os.path.isdir(item_path):
            os.rmdir(item_path)
            logging.info(f"Deleted directory: {item_path}")

if __name__ == "__main__": # Code that should only be executed when the Python file is run as the main program

    # All variables:
    input_path = "C:\\Users\\User\\Documents\\vsc\\script-add_to_zip" # Path of files/directories to be zipped
    current_date = datetime.datetime.now().strftime("%Y%m%d") # Stores current time in given format
    output_path = "C:\\Users\\User\\Desktop"  # Where to create 7z file
    log_file = "zip_log.txt" # Name of log file
    
    # Calling the function and displaying the final message
    zip_directory(input_path, output_path, current_date, log_file)
    print(f"All files and directories containing {current_date} in {input_path} added to {output_path}. Check {log_file} for details.")
