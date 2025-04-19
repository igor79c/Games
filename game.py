import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtMultimedia import QSound
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt

class SubtractionGame(QWidget):
    def __init__(self):
        super().__init__()
        self.question_count = 0
        self.total_questions = 12
        self.current_correct = None

        # Load background image once.
        self.pixmap = QPixmap("pr.jpg")

        self.initUI()
        self.generate_question()
        
    def initUI(self):
        self.setWindowTitle("Subtraction Game for Valentino")
        # Set window size to 1200x800.
        self.setGeometry(100, 100, 1200, 800)
        
        # Set the background image scaled to the window size.
        palette = QPalette()
        scaled_pixmap = self.pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
        self.setPalette(palette)
        
        # Main vertical layout.
        self.v_layout = QVBoxLayout()
        
        # Add a top label with "VALENTINO CRACK ON !!"
        self.top_label = QLabel("VALENTINO CRACK ON !!")
        self.top_label.setStyleSheet("font-size: 64px; font-weight: bold; color: blue; background-color: transparent;")
        self.top_label.setAlignment(Qt.AlignCenter)
        self.v_layout.addWidget(self.top_label, alignment=Qt.AlignCenter)
        
        # Create a question button (used as a label) with fixed size,
        # black background, red text.
        self.question_button = QPushButton("")
        self.question_button.setStyleSheet("font-size: 64px; font-weight: bold; color: red; background-color: black;")
        self.question_button.setEnabled(False)
        self.question_button.setFixedSize(200, 133)
        self.v_layout.addWidget(self.question_button, alignment=Qt.AlignCenter)
        
        # Horizontal layout for the answer buttons.
        self.h_layout = QHBoxLayout()
        self.answer_buttons = []
        for i in range(3):
            btn = QPushButton("")
            btn.setStyleSheet("font-size: 64px; font-weight: bold; background-color: orange; color: black;")
            btn.setFixedSize(150, 100)
            btn.clicked.connect(self.check_answer_wrapper)
            self.answer_buttons.append(btn)
            self.h_layout.addWidget(btn)
        self.v_layout.addLayout(self.h_layout)
        
        # Create a Start Again button, hidden initially.
        self.start_again_button = QPushButton("Start Again")
        self.start_again_button.setStyleSheet("font-size: 28px; font-weight: bold; background-color: green; color: white;")
        self.start_again_button.setFixedSize(200, 60)
        self.start_again_button.clicked.connect(self.start_again)
        self.start_again_button.hide()
        self.v_layout.addWidget(self.start_again_button, alignment=Qt.AlignCenter)
        
        self.setLayout(self.v_layout)
        
    def resizeEvent(self, event):
        # Scale the background image to fit the new window size.
        scaled_pixmap = self.pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
        self.setPalette(palette)
        super().resizeEvent(event)
        
    def generate_question(self):
        if self.question_count >= self.total_questions:
            self.finish_game()
            return
        
        # Generate two random numbers ensuring a non-negative result.
        a = random.randint(1, 10)
        b = random.randint(1, a)
        self.current_correct = a - b
        self.question_button.setText(f"{a} - {b}")
        
        # Prepare distractor answers.
        possible_answers = list(range(0, 11))
        if self.current_correct in possible_answers:
            possible_answers.remove(self.current_correct)
        distractors = random.sample(possible_answers, 2)
        
        # Combine the correct answer with distractors and shuffle them.
        choices = [self.current_correct] + distractors
        random.shuffle(choices)
        
        # Update each answer button with a choice.
        for btn, val in zip(self.answer_buttons, choices):
            btn.setText(str(val))
            btn.setEnabled(True)
            btn.show()
            
        # Hide the Start Again button if visible.
        self.start_again_button.hide()
            
    def check_answer_wrapper(self):
        btn = self.sender()
        selected_answer = int(btn.text())
        self.check_answer(selected_answer)
        
    def check_answer(self, selected_answer):
        if selected_answer == self.current_correct:
            self.question_count += 1
            self.generate_question()
        else:
            # Play the wrong answer sound (ensure 'wrong.wav' exists in the same directory).
            QSound.play("wrong.wav")
            
    def finish_game(self):
        self.question_button.setText("Game Over!")
        for btn in self.answer_buttons:
            btn.setEnabled(False)
            btn.hide()
        self.start_again_button.show()
        
    def start_again(self):
        self.question_count = 0
        for btn in self.answer_buttons:
            btn.show()
        self.generate_question()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = SubtractionGame()
    game.show()
    sys.exit(app.exec_())