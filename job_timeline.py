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
    keywords: list[str]

    def __init__(self, experience_dict: dict[float]):
        for key, value in experience_dict.items():
            setattr(self, key, value)
        self._parse_dates()
        self.keywords = self.keywords.split(', ')


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

    def set_companies(self):
        self.companies = {}
        self.min_date = NOW
        self.max_date = NOW
        for experience in self.experiences:
            if experience.start_date < self.min_date:
                self.min_date = experience.start_date
            if experience.company in self.companies:
                if experience.start_date < self.companies[experience.company][0]:
                    self.companies[experience.company][0] = experience.start_date
                if experience.end_date > self.companies[experience.company][1]:
                    self.companies[experience.company][1] = experience.end_date
            else:
                self.companies[experience.company] = [experience.start_date, experience.end_date]

    def draw_experiences(self):
        self.set_companies()
        WIDTH = 1200
        WM = 10
        BOX_HEIGHT = 50
        HM = 10
        HEIGHT = BOX_HEIGHT * 5 + HM * 6

        FONT_SIZE = 10
        LIGHT_GREEN = "#a9d6e5"
        GREEN = "#468faf"
        DARK_GREEN = "#012a4a"

        d = draw.Drawing(WIDTH, HEIGHT)

        def position_x(date):
            return WM + (date - self.min_date).days / (self.max_date - self.min_date).days * (WIDTH-2*WM)

        for company, dates in self.companies.items():
            start_x = position_x(dates[0])
            end_x = position_x(dates[1])

            y = BOX_HEIGHT + HM
            d.append(draw.Rectangle(start_x, y, end_x - start_x,
                     3*BOX_HEIGHT + 3*HM, fill=LIGHT_GREEN, rx='10', ry='10'))

            d.append(draw.Text(f'{company}', FONT_SIZE,
                     x=(end_x + start_x)/2, y=y+(BOX_HEIGHT)/2,
                     fill=DARK_GREEN, center=True))

        for i, experience in enumerate(self.experiences):
            start_x = position_x(experience.start_date)
            end_x = position_x(experience.end_date)

            position_y = 2*BOX_HEIGHT + 2*HM
            keywords_y = 3*BOX_HEIGHT + 3*HM
            if i % 2 == 1:
                temp = keywords_y
                keywords_y = position_y
                position_y = temp

            width = end_x - start_x

            d.append(draw.Rectangle(start_x + WM, position_y, width - 2*WM,
                     BOX_HEIGHT, fill=GREEN, rx='10', ry='10'))

            position_text = experience.position
            keyword_text = ", ".join(experience.keywords)
            text_size = len(position_text)
            if text_size*5 > width:
                position_text = position_text.replace(" ", "\n")
                keyword_text = ('\n').join(experience.keywords)

            d.append(draw.Text(f'{position_text}', FONT_SIZE,
                     x=(end_x + start_x)/2, y=position_y+(BOX_HEIGHT)/2,
                     fill=DARK_GREEN, center=True))

            d.append(draw.Text(f'{keyword_text}', FONT_SIZE,
                     x=(end_x + start_x)/2, y=keywords_y+(BOX_HEIGHT)/2,
                     fill=DARK_GREEN, center=True))

        d.append(draw.Line(
            WM,
            3*BOX_HEIGHT + 5/2*HM,
            WIDTH - WM,
            3*BOX_HEIGHT + 5/2*HM,
            stroke=DARK_GREEN))

        # Afficher la frise SVG
        d.save_svg("rendercv_output/frise_chronologique.svg")


if __name__ == "__main__":
    timeline = Timeline("Marion_FABRE_CV.yaml")
    timeline.draw_experiences()
