import argparse

def main():


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Reads a CSV file and adds it to a database.')
    
    parser.add_argument('--file',type=str, help='This is the name of the CSV to be parsed.')
    parser.add_argument('--create_table',action='store_true',help='This will cause the MySQL users table to be built(and nofurther action will be taken)')
    parser.add_argument('--dry_run', action='store_true',help='This will be used with the --file
     'directive in the instance that we want to run the '
     "script but not insert into the DB. All other functions will be executed, but the database won't be altered.")
    parser.add_argument('-u', type=str, help='MySQL username')
    parser.add_argument('-p', type=str, help='MySQL password')
    parser.add_argument('-h', type=str, help='MySQL host')
    args = parser.parse_args()

    main()