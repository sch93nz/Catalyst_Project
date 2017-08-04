"""This is used to parse arguments """
import argparse
import MySQLdb

def create_tables(db):
    """Creates the tables in the database"""
    command = 'create table users (name VARCHAR(20),surname'\
                'VARCHAR(20),email VARChAR(30) UNIQUE);'
    if not DRY_RUN:
        db.query(command)
        db.commit()
    else:
        print command
    print "Table Created"
    quit()


def check_email(email):
    """This will return true if the email conforms to requirements"""
    
    return False

def main(args):
    """Main function of this file"""
    open_file = open(args.file, 'r')
    open_file.readline() # this just spits out the headers
    for line in open_file:
        split=line.split(",")
        split[0] = split[0].capitalize()
        split[1] = split[1].capitalize()
        check = check_email(split[2])
        if check:
            print split
        

if __name__ == "__main__":

    PARSER = argparse.ArgumentParser(description='Reads a CSV file and adds it to a database.')
    PARSER.add_argument('--file', type=str, help='This is the name of the CSV to be parsed.'
                        , dest='file', required=True)
    PARSER.add_argument('--create_table', action='store_true', help='This will cause the MySQL'
                                                                    ' users table to be built(and '
                                                                    'no further action will be taken)')
    PARSER.add_argument('--dry_run', action='store_true', help='This will be used with the --file'
                                                                'directive in the instance that we'
                                                                ' want to run the script but not '
                                                                'insert into the DB. All other '
                                                                'functions will be executed, but '
                                                                "the database won't be altered.")
    PARSER.add_argument('-u', type=str, action='store', help='MySQL username', dest='user', required=True)
    PARSER.add_argument('-p', type=str, action='store', help='MySQL password', dest='password', required=True)
    PARSER.add_argument('-host', type=str, help='MySQL host', action='store', dest='host', required=True)

    ARGUMENTS = PARSER.parse_args()
    global DRY_RUN
    DRY_RUN = ARGUMENTS.dry_run

    if ARGUMENTS.create_table:
        DATABASE = None
        if not DRY_RUN:
            DATABASE = MySQLdb.connect(host=ARGUMENTS.host, user=ARGUMENTS.user, passwd=ARGUMENTS.password)
        else:
            print "MysQLdb.connect(host="ARGUMENTS.host" , user="ARGUMENTS.user" , passwd="ARGUMENTS.password" )"
        create_tables(DATABASE)

    main(ARGUMENTS)
