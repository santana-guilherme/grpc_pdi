class Database:

    def __init__(self, conn) -> None:
        self.conn = conn

    def execute_statement(self, statement: str):
        with self.conn:
            resp = self.conn.execute(statement)
        return resp

    def init_database(self):
        init_db_statement = "create table if not exists scraped_websites(url text unique, html text not null);"
        self.execute_statement(init_db_statement)

    def insert_website(self, url: str, html: str):
        html = html.replace("'", "''")
        insert_website_statement = f"insert into scraped_websites values ('{url}', '{html}');"
        print(insert_website_statement)
        return self.execute_statement(insert_website_statement)

    def fetch_all_websites(self):
        resp = self.execute_statement("select * from scraped_websites;")
        return resp.fetchall()
