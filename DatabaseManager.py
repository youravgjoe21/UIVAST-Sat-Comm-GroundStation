import psycopg

DSN = 'dbname=SatComm user=vast password=A61C9fL4elJuMq8WUvoz'

class DatabaseManager():
    activeTable = 'test'
    
    def __init__(self):
        pass

    def createLaunchTable(self,name):
        '''Creates a new table with the defined layout. This allow us to create a separate table for each launch, meaning we don't have to split our data into launches later.'''
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                # Create data table
                cur.execute(f"""
                            CREATE TABLE \"{name}\" (
                                timereceived timestamp PRIMARY KEY,
                                positionx numeric,
                                positiony numeric,
                                altitude numeric,
                                modulestatus jsonb,
                                sensordata jsonb
                            )
                            """)
                # Make the changes to the database persistent
                conn.commit()

        self.activeTable = name

    def getTableNames(self):
        '''Returns a list containing all table names'''
        names = []
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
                for table in cur.fetchall():
                    names.append(table[0])

        return names

    def writeRow(self,timestamp, xcoord, ycoord, altitude, modulestatus, sensordata):
        '''Inserts a new entry into the database'''
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                            INSERT INTO \"{self.activeTable}\" (timereceived, positionx, positiony, altitude, modulestatus, sensordata) VALUES (%s,%s,%s,%s,%s,%s)
                            """,
                            (timestamp, xcoord, ycoord, altitude, modulestatus, sensordata))
                
                # Make the changes to the database persistent
                conn.commit()