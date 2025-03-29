import drawsvg as draw
from datetime import datetime
import yaml
from dataclasses import dataclass

DATE_FORMAT = "%Y-%m"

NOW = datetime.strptime(datetime.now().strftime(DATE_FORMAT), DATE_FORMAT)


class Position:
    start_date: datetime
    end_date: datetime

    def _parse_dates(self):
        if self.end_date == "present":
            self.end_date = NOW
        else:
            self.end_date = datetime.strptime(self.end_date, DATE_FORMAT)

        self.start_date = datetime.strptime(self.start_date, DATE_FORMAT)

    def get_timespan(self) -> str:
        return f"{self.start_date.strftime(DATE_FORMAT)} - {self.end_date.strftime(DATE_FORMAT)}"


@dataclass
class Experience(Position):
    company: str
    website: str
    position: str
    contract_type: str
    location: str
    start_date: datetime
    end_date: datetime

    def __init__(self, experience_dict: dict[float]):
        for key, value in experience_dict.items():
            setattr(self, key, value)
        self._parse_dates()


@dataclass
class Education(Position):
    institution: str
    website: str
    position: str
    degree: str
    area: str
    location: str
    start_date: datetime
    end_date: datetime

    def __init__(self, experience_dict: dict[float]):
        for key, value in experience_dict.items():
            setattr(self, key, value)
        self._parse_dates()


class Timeline():
    def __init__(self, cv_path):
        with open(cv_path, 'r') as stream:
            my_yaml = yaml.safe_load(stream)
            self.educations = [Education(education) for education in my_yaml['cv']['sections']['education']]
            self.experiences = [Experience(experience) for experience in my_yaml['cv']['sections']['experience']]

    def draw_experiences(self):
        d = draw.Drawing(800, 400)

        # Définir les dimensions de la frise (date de début et date de fin)
        dates = [date for experience in self.experiences for date in [experience.start_date, experience.end_date]]
        min_date = min(dates)
        max_date = max(dates)

        # Calcul de l'échelle des dates pour les adapter à l'espace horizontal
        def position_x(date):
            return 50 + (date - min_date).days / (max_date - min_date).days * 700

        # Parcourir les postes et ajouter les rectangles
        for i, experience in enumerate(self.experiences):

            # Calcul des positions des rectangles
            start_x = position_x(experience.start_date)
            end_x = position_x(experience.end_date)

            # Ajouter le rectangle pour chaque poste
            d.append(draw.Rectangle(start_x, 80 + i * 50, end_x - start_x, 30, fill="lightblue", stroke="black"))

            # Ajouter le texte pour le nom de l'entreprise et les dates
            d.append(draw.Text(f'{experience.company} ({experience.get_timespan()})',
                     10, start_x + 5, 80 + i * 50 + 15, fill="black"))

        # Afficher la frise SVG
        d.save_svg("frise_chronologique.svg")


if __name__ == "__main__":
    timeline = Timeline("Marion_FABRE_CV.yaml")
    timeline.draw_experiences()
