"""imports for this program"""
import argparse
import MySQLdb

def create_tables(db):
    """Creates the tables in the database then quits
    If The table already exist my through a error which
    will be printed to standard out"""

    command = 'CREATE TABLE users ( name VARCHAR(20) , surname'\
                'VARCHAR(20), email VARCHAR(256) UNIQUE);'
    if not DRY_RUN:
        try:
            db.query(command)
            db.commit()
        except MySQLdb.Error, error:# MySql Error handling only
            print str(error)
            quit()
    else:
        print command
    print "Table Created"
    quit()

def print_invalid_email(first, surname, email):
    """This will just handles the print out as it will be used alot."""
    print "Email is not of legal format ( ",
    print "First= "+first+" surname= "+surname+" email= "+email + " )"

def check_email(email, first, surname):
    """This will return true if the email conforms to requirements
    As more checks are thought of they will be put here"""
    if email.count("@") != 1 or len(email) > 256 or email.count('..') != 0:
        print_invalid_email(first, surname, email)
        return False

    parts = email.split('@')
    if parts[1] == 'localhost':
        print_invalid_email(first, surname, email)
        return False
    return True

def main(args, db):
    """Main function of this file"""
    open_file = open(args.file, 'r')
    open_file.readline() # this just spits out the headers
    for line in open_file:
        split = line.split(",")
        if len(split[0]) > 0 and len(split[1]) > 0 and len(split[2]) > 2: # So this is here to stop empty fields from being inserted
            split[0] = split[0].capitalize().strip() # capitalizing the first letter and lower casing the rest
            split[1] = split[1].capitalize().strip() # capitalizing the first letter and lower casing the rest
            split[2] = split[2].lower().strip() #making the email lower case
            check = check_email(split[2], split[0], split[1])
            if check:
                value = "INSERT INTO users (name , surname, email ) VALUES ( '"  + split[0] + "', '" + split[1] + "', '" + split[2] +"' );"
                if not DRY_RUN:
                    try:
                        db.query(value)
                        db.commit()
                    except MySQLdb.Error, error:# MySql Error handling only
                        print "First= " + split[0] + " surname= " + split[1] + " email= " + split[2] 
                        print str(error)
                else:
                    print value
        else:
            print "One of the feilds is to small"
            print split

if __name__ == "__main__":
    # argument passing
    PARSER = argparse.ArgumentParser(description='Reads a CSV file and adds it to a database.')
    PARSER.add_argument('--file', type=str, help='This is the name of the CSV to be parsed.'
                        , dest='file')
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
    # I am using a global variable because it is less confusing then
    # always passing a extra argument to every meathod
    DRY_RUN = ARGUMENTS.dry_run
    DATABASE = None
    if not DRY_RUN:
        try:
            print "connecting to database at host="+ARGUMENTS.host
            DATABASE = MySQLdb.connect(host=ARGUMENTS.host, user=ARGUMENTS.user, passwd=ARGUMENTS.password)
        except MySQLdb.Error, error: # MySql Error handling only
            print str(error)
            quit()
    else:
        print "MysQLdb.connect(host=" + ARGUMENTS.host + " , u"\
        "ser=" +ARGUMENTS.user + " , passwd=" + ARGUMENTS.password + " )"
    if ARGUMENTS.create_table:
        create_tables(DATABASE)

    main(ARGUMENTS, DATABASE)
