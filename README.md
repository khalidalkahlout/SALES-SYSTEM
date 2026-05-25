# Smart Store Management System (Full-Stack Application) 📱📦

A lightweight, functional Full-Stack application designed for real-time inventory and product management. The project demonstrates a seamless connection between a modern mobile/web frontend, a robust backend API, and a relational database.

## 🚀 Features
* **Dynamic Frontend:** Built with Flutter, featuring a clean user interface that displays products dynamically from the database.
* **Real-time Actions:** Includes a "Sell Item" (بيع قطعة) interactive feature that updates stock instantly.
* **RESTful API backend:** Built with Python Flask, handling client requests and state updates safely.
* **Persistent Storage:** Backed by an SQLite database for keeping track of product names, categories, prices, and stock levels.
* **Cross-Origin Enabled:** Integrated with Flask-CORS to support smooth communication with web clients (Chrome/Edge).

---

## 🛠️ Tech Stack & Architecture

The system follows a classic client-server data flow architecture:

```text
[ Flutter Web/App Client ] <───(HTTP / JSON)───> [ Flask API Server ] <───(SQL Queries)───> [ SQLite Database ]
