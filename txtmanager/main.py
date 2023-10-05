import sys
import os
import webbrowser
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QComboBox, QLineEdit, QVBoxLayout, QFileDialog, QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Помощник с txt')
        #self.setStyleSheet(open('dark/dracula.css').read()) # Добавь сам свою тему. 

        self.layout = QVBoxLayout()
        self.setWindowIcon(QIcon(resource_path('res/icon.ico')))

        self.function_selector = QComboBox()
        self.function_selector.addItem('Выберите нужное действие')
        self.function_selector.addItem('Объединить файлы')
        self.function_selector.addItem('Разделить файл')
        self.function_selector.addItem('Проверить на дубли')
        self.function_selector.addItem('Добавить URL')
        self.function_selector.addItem('Добавить пароли к почтам')
        self.function_selector.currentIndexChanged.connect(self.toggle_function)

        self.layout.addWidget(self.function_selector)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(QWidget())

        self.merge_widget = self.create_merge_widget()
        self.stacked_widget.addWidget(self.merge_widget)

        self.split_widget = self.create_split_widget()
        self.stacked_widget.addWidget(self.split_widget)

        self.check_duplicates_widget = self.create_check_duplicates_widget()
        self.stacked_widget.addWidget(self.check_duplicates_widget)

        self.add_url_widget = self.create_add_url_widget()
        self.stacked_widget.addWidget(self.add_url_widget)

        self.add_password_widget = self.create_add_password_widget()
        self.stacked_widget.addWidget(self.add_password_widget)

        self.layout.addWidget(self.stacked_widget)

        self.run_button = QPushButton('Выполнить')
        self.run_button.clicked.connect(self.execute_action)
        self.author_button = QPushButton('Автор')
        self.author_button.clicked.connect(self.open_author_page)

        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 20px;")
        self.layout.addWidget(self.result_label)

        self.layout.addWidget(self.run_button)
        self.layout.addWidget(self.author_button)

        self.setLayout(self.layout)

        self.setFixedSize(300, 200)

    def toggle_function(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def open_author_page(self):
        webbrowser.open('https://zelenka.guru/sataraitsme/')

    def create_merge_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.merge_files_count = QComboBox()
        self.merge_files_count.addItems(['2', '3', '4'])
        self.merge_files_count.setCurrentIndex(0)

        layout.addWidget(QLabel('Выберите количество файлов для объединения:'))
        layout.addWidget(self.merge_files_count)

        return widget

    def create_split_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.split_line_count = QLineEdit()

        layout.addWidget(QLabel('Укажите количество строк в файле:'))
        layout.addWidget(self.split_line_count)

        return widget

    def create_check_duplicates_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.check_duplicates_file_count = QComboBox()
        self.check_duplicates_file_count.addItems(['2', '3', '4'])
        self.check_duplicates_file_count.setCurrentIndex(0)

        layout.addWidget(QLabel('Выберите сколько файлов проверится на дубли:'))
        layout.addWidget(self.check_duplicates_file_count)

        return widget

    def create_add_url_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('Введите URL')

        layout.addWidget(QLabel('Введите URL:'))
        layout.addWidget(self.url_input)

        return widget

    def execute_action(self):
        action = self.function_selector.currentIndex()
        if action == 0:
            self.result_label.setText('Пожалуйста, выберите функцию.')
            return

        if action == 1:
            files_count = int(self.merge_files_count.currentText())
            result = self.merge_files(files_count)
        elif action == 2:
            line_count = int(self.split_line_count.text())
            result = self.split_file(line_count)
        elif action == 3:
            files_count = int(self.check_duplicates_file_count.currentText())
            result = self.check_duplicates(files_count)
        elif action == 4:
            url = self.url_input.text()
            result = self.add_url_to_database(url)
        elif action == 5:
            result = self.add_password_to_emails()

        self.result_label.setText(result)

    def merge_files(self, files_count):
        try:
            file_paths = QFileDialog.getOpenFileNames(self, 'Выберите файлы для объединения')[0]
            if len(file_paths) < files_count:
                return 'Недостаточно файлов для объединения.'

            contents = []
            for file_path in file_paths:
                with open(file_path, 'r') as file:
                    contents.append(file.read())

            merged_content = '\n'.join(contents)

            with open('merged_file.txt', 'w') as output_file:
                output_file.write(merged_content)

            return 'Файлы успешно объединены.'
        except Exception as e:
            return f'Ошибка при объединении файлов: {e}'

    def split_file(self, line_count):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл для разделения')
            with open(file_path, 'r') as file:
                lines = file.readlines()
                total_lines = len(lines)
                chunk_size = total_lines // line_count
                for i in range(line_count):
                    start = i * chunk_size
                    end = (i + 1) * chunk_size if i < line_count - 1 else total_lines
                    with open(f'split_file_{i+1}.txt', 'w') as output_file:
                        output_file.writelines(lines[start:end])
            return f'Файл успешно разделен на {line_count} части.'
        except Exception as e:
            return f'Ошибка при разделении файла: {e}'

    def check_duplicates(self, files_count):
        try:
            file_paths = QFileDialog.getOpenFileNames(self, 'Выберите файлы для проверки на дубли')[0]
            if len(file_paths) < files_count:
                return 'Недостаточно файлов для проверки на дубли.'

            lines_sets = []
            for file_path in file_paths:
                with open(file_path, 'r') as file:
                    lines = set(file.readlines())
                    lines_sets.append(lines)

            all_lines = set.union(*lines_sets)
            duplicates = [line for line in all_lines if sum(line in lines_set for lines_set in lines_sets) > 1]

            percent_duplicates = (len(duplicates) / len(all_lines)) * 100

            result = f'Процент дублей: {percent_duplicates:.2f}%\nДублирующие строки:\n' + '\n'.join(duplicates)
            return result
        except Exception as e:
            return f'Ошибка при проверке на дубли: {e}'

    def add_url_to_database(self, url):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл для добавления URL')
            with open(file_path, 'r') as file:
                lines = file.readlines()

            modified_lines = [f'{url}:{line.strip()}\n' for line in lines]

            output_file_path = os.path.join(os.path.dirname(file_path), f'modified_{os.path.basename(file_path)}')

            with open(output_file_path, 'w') as output_file:
                output_file.writelines(modified_lines)

            return f'URL успешно добавлен к содержимому базы.'
        except Exception as e:
            return f'Ошибка при добавлении URL: {e}'

        
    def create_add_password_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Введите новый пароль')

        layout.addWidget(QLabel('Введите новый пароль:'))
        layout.addWidget(self.password_input)

        return widget
    
    def add_password_to_emails(self):
        try:
            password = self.password_input.text().strip()

            if not password:
                return 'Пожалуйста, введите пароль.'

            file_path, _ = QFileDialog.getOpenFileName(self, 'Выберите файл с почтами')
            if not file_path:
                return 'Пожалуйста, выберите файл с почтами.'

            with open(file_path, 'r') as file:
                emails = file.readlines()

            modified_emails = [f'{email.strip()}:{password}\n' for email in emails]

            with open('modified_emails.txt', 'w') as output_file:
                output_file.writelines(modified_emails)

            return 'Пароли успешно добавлены к email/login.'
        except Exception as e:
            return f'Ошибка при добавлении пароля: {e}'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())