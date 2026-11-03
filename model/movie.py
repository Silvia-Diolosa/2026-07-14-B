from dataclasses import dataclass

@dataclass
class Movie:
    id: str
    title: str
    year: int
    avg_rating: float


    def __str__(self):
        return f"{self.id} {self.title} {self.year}"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


    def __post_init__(self):
        self.listActor = []



# oppure:
# @dataclass
# class Movie:
#     MovieId: int
#     Title: str
#     Year: int
#     AvgRating: float = 0.0
#     Actors: set = field(default_factory=set)
    # INIZIALIZZO LA LISTA DIRETTAMENTE NEL COSTRUTTORE
    # QUINDI Actors: set è UN PARAMETRO DI TIPO SET
    # = field(default_factory=set) INIZIALIZZATO AD UN SET VUOTO
    # Perché default_factory e non Actors: set = set()?
    # Con = set() il set verrebbe creato una volta sola, alla definizione della classe, e sarebbe condiviso da
    # tutti i film: aggiungere un attore a un film lo aggiungerebbe a tutti. Per questo il dataclass lo vieta
    # per i tipi mutabili (liste, set, dizionari) e dà errore. default_factory invece chiama la funzione a ogni
    # creazione di oggetto, quindi ogni film ha il suo set separato.

#
#     def __hash__(self):
#         return hash(self.MovieId)
#
#     def __eq__(self, other):
#         if not isinstance(other, Movie):
#             return False
#         return self.MovieId == other.MovieId
#
#     def __str__(self):
#         return f"{self.Title} ({self.Year})"
#
#     def get_num_actors(self):
#         return len(self.Actors)

    # E POI ACCEDO AL SET CON LA FUNZIONE GET