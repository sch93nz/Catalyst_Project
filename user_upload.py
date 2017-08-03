"""This is used to parse arguments """
import argparse
""" """
import MySQLdb

def Create_Tables(db):
    """Creates the tables in the database"""

    print "Creating Table"


def main(args):
    """Main function of this file"""
    if args.dry_run:
        print "dry run"
    if str(args.user) != "None":
        print "username=" + str(args.user)
    if str(args.password) != "None":
        print "password=" + str(args.password)
    if args.create_table:
        print "create_table"
    if str(args.file) != "None":
        print "file" + str(args.file)


if __name__ == "__main__":

    PARSER = argparse.ArgumentParser(description='Reads a CSV file and adds it to a database.')
    PARSER.add_argument('--file', type=str, help='This is the name of the CSV to be parsed.'
                        , dest='file')
    PARSER.add_argument('--create_table', action='store_true', help='This will cause the MySQL'
                                                                    ' users table to be built(and '
                                                                    'nofurther action will be taken)')
    PARSER.add_argument('--dry_run', action='store_true', help='This will be used with the --file'
                                                                'directive in the instance that we'
                                                                ' want to run the script but not '
                                                                'insert into the DB. All other '
                                                                'functions will be executed, but '
                                                                "the database won't be altered.")
    PARSER.add_argument('-u', type=str, action='store', help='MySQL username', dest='user')
    PARSER.add_argument('-p', type=str, action='store', help='MySQL password', dest='password')
    PARSER.add_argument('-host', type=str, help='MySQL host', action='store', dest='host')
    ARGUMENTS = PARSER.parse_args()
    DATABASE = MySQLdb.connect(host=ARGUMENTS.host, user=ARGUMENTS.user, passwd=ARGUMENTS.password, db="Catalyst")

    if ARGUMENTS.create_table:
        Create_Tables(DATABASE)

    main(ARGUMENTS)
