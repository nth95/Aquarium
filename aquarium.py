from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QTransform
from PyQt5.QtCore import QTimer, Qt
import sys
import random
import math

class Fish(QLabel):
    def __init__(self, parent, pixmap_path):
        super().__init__(parent)
        self.original_pixmap = QPixmap(pixmap_path)
        self.setPixmap(self.original_pixmap)

        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(2, 5)
        self.setGeometry(random.randint(0, 1130), random.randint(0, 660), 150, 150)
        self.update_image()

    def update_image(self):
        transform = QTransform()
        transform.rotate(math.degrees(self.angle))

        if math.cos(self.angle) < 0:
            transform.scale(1, -1)

        transformed_pixmap = self.original_pixmap.transformed(transform, mode=Qt.SmoothTransformation)
        self.setPixmap(transformed_pixmap)

    def move_fish(self):
        self.angle += random.uniform(-0.05, 0.05)  # Légère modification de l'angle
        self.speed += random.randint(1, 4)  # Légère modification de la vitesse
        self.speed = max(1, min(self.speed, 8))

        dx = math.cos(self.angle) * self.speed
        dy = math.sin(self.angle) * self.speed

        x, y = self.x() + dx, self.y() + dy

        fish_width = self.pixmap().width()
        fish_height = self.pixmap().height()

        max_x = 1280 - fish_width
        max_y = 720 - fish_height

        # Ajuster les conditions de rebondissement
        if x < 0:
            self.angle = math.pi - self.angle
            x = 0
        elif x > max_x:
            self.angle = math.pi - self.angle
            x = max_x

        if y < 0:
            self.angle = -self.angle
            y = 0
        elif y > max_y:
            self.angle = -self.angle
            y = max_y

        self.move(int(x), int(y))
        self.update_image()

class Fish2(Fish):
    def __init__(self, parent):
        super().__init__(parent, "fish2.png")

class Fish3(Fish):
    def __init__(self, parent):
        super().__init__(parent, "fish3.png")

class Aquarium(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aquarium")
        background = QPixmap("fond_marin.png")
        self.setFixedSize(background.size())
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(background))
        self.setPalette(palette)

        self.fish_count = random.randint(5,8)
        self.fishes = [Fish(self, "fish1.png") for _ in range(self.fish_count)]
        self.fishes += [Fish2(self) for _ in range(self.fish_count)]
        self.fishes += [Fish3(self) for _ in range(self.fish_count)]

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_fishes)
        self.timer.start(50)

    def move_fishes(self):
        for fish in self.fishes:
            fish.move_fish()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = Aquarium()
    mainWin.show()
    sys.exit(app.exec_())
