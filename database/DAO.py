from database.DB_connect import DBConnect
from model.Constructor import Constructor
from model.arco import Arco


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllCostruttori(anno1,anno2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct c.*
from results r ,races r2 , constructors c 
where r.raceId = r2.raceId and r2.`year` between %s and %s
and r.`position` is not null and c.constructorId =r.constructorId """

        cursor.execute(query,(anno1,anno2))

        for row in cursor:
            results.append(Constructor(**row))

        cursor.close()
        conn.close()
        return results

    #Due nodi sono connessi da un arco se e solo se i due costruttori hanno condiviso almeno un pilota durante il
    # periodo selezionato (campo driverId della tabella results). Un pilota si considera "condiviso" se ha corso per
    # entrambi i costruttori in gare diverse all'interno del range di anni selezionato. Il peso dell'arco è pari al
    # numero di piloti distinti che hanno corso per entrambi i costruttori nel periodo considerato. Si considerino
    # solo le gare in cui il pilota ha correttamente tagliato il traguardo


    @staticmethod
    def getAllEdges(anno1, anno2, idMapCostruttori):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select r1.constructorId as id1, r2.constructorId as id2, count(distinct r1.driverId) as numPiloti
from results r1 , results r2, races r3 , races r4
where r1.raceId = r3.raceId and  r3.year between %s and %s
and r2.raceId = r4.raceId and  r4.year between %s and %s and r1.position is not null and r2.position is not null
and r1.driverId = r2.driverId and r1.constructorId < r2.constructorId
group by r1.constructorId, r2.constructorId """

        cursor.execute(query, (anno1, anno2,anno1,anno2))

        for row in cursor:
            results.append(Arco(idMapCostruttori[row["id1"]], idMapCostruttori[row["id2"]], row["numPiloti"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getVeteranoFrom(anno1, anno2,idMapConstruttori):
        conn = DBConnect.get_connection()
        results = []


        cursor = conn.cursor(dictionary=True)
        query = """select r.constructorId as idC ,min(d.dob) as oldestDob
from results r , races r2 , drivers d 
where r.raceId = r2.raceId and r2.`year` between %s and %s and d.dob is not null 
and r.position is not null 
and d.driverId =r.driverId 
GROUP BY r.constructorId
 """


        cursor.execute(query, ( anno1, anno2))

        for row in cursor:
            results.append((idMapConstruttori[row["idC"]], row["oldestDob"]))

        cursor.close()
        conn.close()
        return results
