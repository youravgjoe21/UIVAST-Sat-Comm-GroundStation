from datetime import datetime
import psycopg

DSN = 'dbname=SatComm user=vast password=A61C9fL4elJuMq8WUvoz'

class DatabaseManager():
    activeTable = 'test'
    
    def __init__(self):
        self.verifyDBStructure()

    def verifyDBStructure(self):
        '''Verifies that the database contains the tables required to run'''
        with psycopg.connect(DSN) as conn:
            # Register cursor
            cur = conn.cursor()

            # Queary the database for the list of tables, and check whether or not it exists
            cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables where table_name=%s)", ('test',))

        # Returns a boolean representing whether or not the Persons table exists
        # If the table is not found, create it
            if not cur.fetchone()[0]:
                self.createLaunchTable("test")

    def createLaunchTable(self,name: str):
        '''Creates a new table with the defined layout. This allow us to create a separate table for each launch, meaning we don't have to split our data into launches later.'''
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                            CREATE TABLE {name} (
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

    def writeRow(self,timestamp, xcoord, ycoord, altitude, modulestatus, sensordata):
        '''Inserts a new entry into the database'''
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                            INSERT INTO {self.activeTable} (timereceived, positionx, positiony, altitude, modulestatus, sensordata) VALUES (%s,%s,%s,%s,%s,%s)
                            """,
                            (timestamp, xcoord, ycoord, altitude, modulestatus, sensordata))
                
                # Make the changes to the database persistent
                conn.commit()