"""These Are the Modules that will be used.

:import argparse: Used for parsing the arguemnts
:import csv: Used to handle the parsing of CSV files
:import MySQLdb: Used to handle the conenction to mySQL
:import validate_email: Used to handly the validation of the email address.
"""
import argparse
import csv
import MySQLdb
import validate_email

def create_tables(db):
    """Creates the tables in the database then quits
    If The table already exist my through a error which
    will be printed to standard out.

    :param db: The Database object
    :return: This will return nothing
    """
    table_removal = """DROP TABLE IF EXISTS users;"""
    command = """CREATE TABLE users (
        id MEDIUMINT(8) UNSIGNED NOT NULL AUTO_INCREMENT,
        name VARCHAR(20) , 
        surname VARCHAR(20), 
        email VARCHAR(256) UNIQUE,
        PRIMARY KEY(id)
        );"""
    if not DRY_RUN:
        try:
            db.query(table_removal)
            db.commit()
            db.query(command)
            db.commit()
        except MySQLdb.Error, error:# MySql Error handling only
            db.rollback()
            db.close()
            print "Error " + str(error)
            return
    else:
        print table_removal
        print command
    print "Table Created"
    return

def print_invalid_email(first, surname, email):
    """This will just handles the print out as it will be used repetitively.

    :param email: This is the email that is to be checked
    :param first: This is the First name for the entry
    :param surname: this is the surname for the entry

    """
    print "Email is not of legal format ( ",
    print "First= "+first+" surname= "+surname+" email= "+email + " )"

def check_email(email, first, surname):
    """This will return true if the email conforms to requirements.
    As more checks are thought of they will be put here. This
    email checker will not check to see if the emails are real
    as i am unsure that the emails supplied are real so i didn't
    turn that on in the check statement

    :param email: This is the email that is to be checked
    :param first: This is the First name for the entry
    :param surname: this is the surname for the entry
    :return: This will return true or false
    """
    # if you want this to check the domain and weather the email is real
    # Uncomment the line below and comment and comment the line below that
    # is_valid = validate_email.validate_email(email ,check_mx=True ,verify=True)
    is_valid = validate_email.validate_email(email)
    if not is_valid:
        print_invalid_email(first, surname, email)
        return False
    split = email.split('@')
    if 'localhost' in split[1]:
        print_invalid_email(first, surname, email)
        return False
    return True

def parsing_file(args, db):
    """Main function of this file this is were
    the passing of each line will be done

    :param args: A argument object that holds all data
    :param db: This is the connection to the MySQL database
    :return: This returns nothing
    """
    if args.file is None:
        print "No File was Supplied."
        return
    try:
        with open(args.file, 'r') as open_file:
            open_file.readline() # this just spits out the headers
            reader = csv.reader(open_file)
            for line in reader:
                split = line
                if len(split[0]) > 0 and len(split[1]) > 0 and len(split[2]) > 2:
                    # So this is here to stop empty fields from being inserted
                    split[0] = split[0].capitalize().strip() # first name
                    # capitalizing the first letter and lower casing the rest
                    split[1] = split[1].capitalize().strip() # last name
                    # capitalizing the first letter and lower casing the rest

                    split[2] = split[2].lower().strip() #making the email lower case
                    check = check_email(split[2], split[0], split[1])
                    if check:
                        value = 'INSERT INTO users (name , surname, email ) VALUES ' \
                        '( "'  + split[0] + '", "' + split[1] + '", "' + split[2] +'" );'
                        if not DRY_RUN:
                            try:
                                db.query(value)
                                db.commit()
                            except MySQLdb.Error, error:# MySql Error handling only
                                db.rollback()
                                print "First= " + split[0] + " surn"\
                                      "ame= " + split[1] + " email= " + split[2]
                                print "Error " + str(error)
                        else:
                            print value
                else:
                    print "One of the feilds is to small " + str(split)
    except IOError,er:
        print er

def main(arg):
    """This is the main meathod and will handle all the
    different paths the program will take

    :param arg: holds all the arguments
    """
    database = None
    if not DRY_RUN:
        try:
            print "connecting to database at host=" + arg.host
            database = MySQLdb.connect(host=arg.host,
                                       user=arg.user,
                                       passwd=arg.password, db="catalyst")
            if arg.create_table:
                create_tables(database)
            else:
                parsing_file(arg, database)
            database.close()
        except MySQLdb.Error, error: # MySql Error handling only
            print "Error " + str(error)
    else:
        print "MysQLdb.connect(host=" + arg.host + " , u"\
        "ser=" +arg.user + " , passwd=" + arg.password + " db='catalyst' )"
        if arg.create_table:
            create_tables(database)
        else:
            parsing_file(arg, database)

if __name__ == "__main__":
    # argument passing
    PARSER = argparse.ArgumentParser(description='Reads a CSV file and adds it to a database.')
    PARSER.add_argument('--file', type=str, help='This is the name of the CSV to be parsed.'
                        , dest='file')
    PARSER.add_argument('--create_table', action='store_true', help='This will cause the MySQL'\
                                                                    ' users table to be built ( and '\
                                                                    'no further action will be '\
                                                                    'taken). This will Drop the'\
                                                                    'if the table aready exist')
    PARSER.add_argument('--dry_run', action='store_true', help='This will be used with the --file'\
                                                                'directive in the instance that we'\
                                                                ' want to run the script but not '\
                                                                'insert into the DB. All other '\
                                                                'functions will be executed, but '\
                                                                "the database won't be altered.")
    PARSER.add_argument('-u', type=str, action='store', help='MySQL username', dest='user',
                        required=True)
    PARSER.add_argument('-p', type=str, action='store', help='MySQL password', dest='password',
                        required=True)
    PARSER.add_argument('-host', type=str, help='MySQL host', action='store', dest='host',
                        required=True)

    ARGUMENTS = PARSER.parse_args()
    global DRY_RUN
    # I am using a global variable because it is less confusing then
    # always passing a extra argument to every meathod
    DRY_RUN = ARGUMENTS.dry_run
    main(ARGUMENTS)
