import flet
from flet import *
import random
import time


class GenerateGrid(UserControl):
    def __init__(self, difficulty):
        self.grid = Column(opacity=1, animate_opacity=300)
        self.blue_tiles: int = 0
        self.correct: int = 0
        self.incorrect: int = 0
        self.difficulty: int = difficulty
        super().__init__()

    def show_color(self, e):
        if e.control.data == '#4cbbb5':
            e.control.bgcolor = '#4cbbb5'
            e.control.opacity = 1
            e.control.update()

            self.correct += 1
            e.page.update()
        else:
            e.control.bgcolor = '#982c33'
            e.control.opacity = 1
            e.control.update()

            self.incorrect += 1
            e.page.update()

    def build(self):
        rows: list = [
            Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Container(
                        width=54,
                        height=54,
                        animate=300,
                        border=border.all(1, 'black'),
                        on_click=lambda e: self.show_color(e),
                    )
                    for _ in range(5)
                ]
            )
            for _ in range(5)
        ]
        colors: list = ['#5c443b', '#4cbbb5']

        for row in rows:
            for container in row.controls[:]:
                container.bgcolor = random.choices(
                    colors,
                    weights=[10, self.difficulty]
                )[0]
                container.data = container.bgcolor
                if container.bgcolor == '#4cbbb5':
                    self.blue_tiles += 1

        self.grid.controls = rows
        return self.grid



def main(page: Page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'

    stage = Text(size=13, color='black', weight='bold')
    result = Text(size=16, color='black', weight='bold')

    start_button = Container(
        content=ElevatedButton(
            on_click=lambda e: start_game(e, GenerateGrid(2)),
            content=Text('Start!', size=13, weight='bold'),
            style=ButtonStyle(
                shape={'': RoundedRectangleBorder(radius=8)},
                color={'': 'white'},
                bgcolor=colors.AMBER
            ),
            height=45,
            width=255
        )
    )

    def start_game(e, level):
        grid = level
        page.controls.insert(3, grid)
        page.update()

        grid.grid.opacity = 1
        grid.grid.update()

        stage.value = f'Stage: {grid.difficulty - 1}'
        stage.update()

        start_button.disabled = True
        start_button.update()

        time.sleep(1.5)

        for rows in grid.controls[0].controls[:]:
            for container in rows.controls[:]:
                if(container.bgcolor == '#4cbbb5'):
                    container.bgcolor = '#5c443b'
                    container.update()

        while True:
            if grid.correct == grid.blue_tiles:
                grid.grid.disabled: bool = True
                grid.grid.update()

                result.value: str = 'GOOD JOB! You got all the tiles!'
                result.color = colors.GREEN_700
                result.update()

                time.sleep(2)
                result.value = ''
                page.controls.remove(grid)
                page.update()

                start_game(e, GenerateGrid(grid.difficulty + 1))

            if grid.incorrect == 3:
                result.value = 'Sorry, you ran out of tries, Try again!'
                result.color = colors.RED_700
                result.update()
                time.sleep(2)

                page.controls.remove(grid)
                page.update()
                result.value = ''
                result.update()
                del grid
                start_button.disabled = False
                start_button.update()
                break

    page.add(
        Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Text(
                    'Memory Matrix',
                    size=22,
                    weight='bold'
                )
            ]
        ),
        Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[result]
        ),
        Divider(height=10, color='transparent'),
        Divider(height=10, color='transparent'),
        Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[stage]
        ),
        Divider(height=10, color='transparent'),
        Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[start_button]
        )
    )
    page.update()


if __name__ == '__main__':
    flet.app(target=main)