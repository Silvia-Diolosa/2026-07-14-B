from database.DB_connect import DBConnect
from model.movie import Movie


class DAO:
    @staticmethod
    def getAllMovies():
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select * \
                from movie m """

        cursor.execute(query)

        for row in cursor:
            results.append(row)

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllGenre():
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT  DISTINCT g.genre as gg
                    FROM genre as g
                    ORDER BY g.genre """

        cursor.execute(query)

        for row in cursor:
            results.append(row["gg"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(genere):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT distinct m.id, m.title, m.year, ra.avg_rating
                    FROM movie m, genre g, role_mapping r, ratings ra
                    WHERE m.id = g.movie_id
                    AND g.genre = %s
                    AND m.id = r.movie_id
                    AND m.id = ra.movie_id"""

        cursor.execute(query, (genere,))

        for row in cursor:
            results.append(Movie(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getFilmAttore(genere):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT m.id as movieId, r.name_id as actorId
                    FROM movie m, genre g, role_mapping r, ratings ra
                    WHERE m.id = g.movie_id
                    AND g.genre = %s
                    AND m.id = r.movie_id
                    AND m.id = ra.movie_id"""

        cursor.execute(query, (genere,))

        for row in cursor:
            results.append((row["movieId"], row["actorId"]))

        cursor.close()
        conn.close()
        return results


