from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    host = "http://127.0.0.1:5000/"
    @task
    def home(self):
        self.client.get("")

    @task
    def display_summary_page(self):
        email = "john@simplylift.co"
        self.client.post("showSummary", data={"email": email})

    @task
    def display_clubs_page(self):
        self.client.get("clubs")

    @task
    def purchase_places_page(self):
        club = "Simply Lift"
        competition = "Spring Festival"
        points = 1
        self.client.post("purchasePlaces", data={
            "club": club,
            "competition": competition,
            "places": points})

    @task
    def book_competition_club_page(self):
        self.client.get("book/Spring%20Festival/Simply%20Lift")

    @task
    def logout_page(self):
        self.client.get("logout")