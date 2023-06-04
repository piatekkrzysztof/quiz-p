import pandas as pd
import psycopg2


def get_connection():
    host = 'localhost'
    port = 5432
    user = 'postgres'
    password = 'coderslab'
    dbname = 'quizp'
    connection = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=dbname)
    connection.autocommit = True
    return connection


def cursor():
    connection = get_connection()
    c = connection.cursor()
    return c


class SaveToDb:
    def __init__(self, path):
        self.path = path
        self.db = self.create_db()

    def path(self):
        return self.path

    def show_db(self):
        return self.db.to_string()

    def show_db_item(self, index):
        return self.db.loc[index]

    def saving(self):
        category = int(input("Insert id of category"))
        for x in range(self.db.__len__()):
            pyt = self.db.loc[x]['PYT']
            a_ans = self.db.loc[x]['A']
            b_ans = self.db.loc[x]['B']
            c_ans = self.db.loc[x]['C']
            d_ans = self.db.loc[x]['D']
            good_ans = self.db.loc[x]['GOOD']
            pgsql = f"""INSERT INTO quizp_question(contents,ans_A,ans_B, ans_C, ans_D,correct, category_id)
                  VALUES (%s,%s,%s,%s,%s,%s,%s)"""
            c = cursor()
            c.execute(pgsql, (pyt, a_ans, b_ans, c_ans, d_ans, good_ans, category))
        return print("Data added!")

    def create_db(self):
        data = pd.read_csv(f"{self.path}")
        data.drop_duplicates(inplace=True)
        return data


def create_path():
    path = input('HERE')
    while True:
        if path.lower() == 'exit':
            exit()
        else:
            try:
                pd.read_csv(f"{path}")
                return path
            except FileNotFoundError:
                print("File not found! try again by put your path")
                path = input('write HERE:')


def adding_to_database():
    print("Welcome to our software,at first Add a path to your file or type exit to leave:")
    path = create_path()
    print("What do you want to do now?")
    x = 69
    while x != 0:
        x = int(input("""
1.Show All items from file
2.Show indicated item from file(by id)
3.Change path
4.Save file to db
0.Exit
    """))
        if x == 1:
            print(SaveToDb(path).show_db())
        if x == 2:
            item_id = int(input("Write index you want to see"))
            print(SaveToDb(path).show_db_item(item_id))
        if x == 3:
            path = create_path()
        if x == 4:
            SaveToDb(path).saving()
        if x not in range(5):
            print("There is not option like this")


adding_to_database()
# path = r"C:\Users\krzys\Desktop\quiz-p\quiz\data\polska.csv"
