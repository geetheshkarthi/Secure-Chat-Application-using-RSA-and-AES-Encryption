# 🔒 Secure Chat Application - Encrypted Messaging System

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![RSA Encryption](https://img.shields.io/badge/RSA-Encryption-critical)
![AES Encryption](https://img.shields.io/badge/AES-Encryption-success)
![Threading](https://img.shields.io/badge/Multithreading-Enabled-lightgrey)

---

Welcome to the **Secure Chat Application** — a lightweight, highly secure client-server messaging platform that uses hybrid encryption techniques (RSA + AES) to protect communication in real time.

Developed as a cybersecurity and network programming project, this application demonstrates how encryption and threading can be combined to create a secure and scalable messaging system.

---

## 📜 Table of Contents
- [About the Project](#about-the-project)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure and How to Run](#project-structure-and-how-to-run)
- [Communication Flow Diagram](#communication-flow-diagram)
- [Security Notes](#security-notes)

---

## 🎯 About the Project

The Secure Chat Application ensures that all communication between the server and multiple clients remains confidential and tamper-proof.

Key points:
- Asymmetric RSA encryption is used for safe AES key exchange.
- Symmetric AES encryption is used for efficient, continuous message exchange.
- Multi-client handling is achieved using Python's `threading` module.

---

## ✨ Features
- **Hybrid Encryption**: Combines RSA and AES for maximum security.
- **Multi-Client Support**: Server handles multiple clients concurrently.
- **Real-Time Messaging**: Secure and instant communication.
- **Encrypted Key Exchange**: RSA public-private key mechanism for AES key sharing.
- **Automatic AES Key Generation**: Each client generates a unique AES session key.
- **Error Handling**: Graceful handling of disconnections and encryption issues.

---

## 🛠 Technologies Used
- **Python 3.6+**
- **PyCryptodome** — Cryptographic functions (RSA, AES)
- **Socket Programming** — Network communication (TCP/IP)
- **Threading** — Handling multiple clients
---

## 🗂 Project Structure and How to Run
-📂 Project Files
- ├── server.py    # Server application (RSA key generation, AES key handling, multi-client communication)
- ├── client.py    # Client application (connects to server, exchanges keys, sends and receives encrypted messages)

-🚀 Running the Project
-  ├── python server.py   #The server will start listening for incoming client connections.
-  ├── python client.py   #You can run multiple clients in different terminals to simulate multiple users communicating securely.


---
🔐 Communication Flow Diagram
 - [Server]
 -   |
 -   |--- Sends Public RSA Key ---> [Client]
 -   |<--- Sends AES Key (RSA-Encrypted) ---
 -   |
- [Server & Client]
-    |
-    |--- (Secure AES Encrypted Communication) <--->
---
# 🏆 Thank you for visiting our project!
Give me like like such effective 
   


