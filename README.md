# TCP File Integrity Verifier

> A real-time, TCP/IP-based file integrity verification web system utilizing MD5 hashing to monitor and detect unauthorized local file modifications.

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/TCP%2FSockets-000000?style=for-the-badge&logo=data&logoColor=white" alt="TCP/IP" />
  <img src="https://img.shields.io/badge/MD5_Hashing-FF6F00?style=for-the-badge&logo=security&logoColor=white" alt="MD5" />
</div>

---

## 🧠 The Core Concept: What the System Actually Does

First, it is important to clarify a crucial detail: the system does not actually "share" or transfer files. Instead, it is a file metadata and integrity tracker. If actual files were transferred, it would be a massive security risk and a heavy load on the server. 

Instead, the system calculates an MD5 "hash"—a unique digital fingerprint—for a file on the user's local computer. It then sends only that fingerprint, along with the file's name and location, to the server. If a hacker or malware changes even a single letter in that local file, the file's fingerprint will change entirely. The system tracks these fingerprints to alert users to unauthorized changes.

## 🌊 The Workflow: Flowing Step-by-Step

**Step 1: The Web System and Authentication**
The journey begins on the web interface. A user visits the website, registers, and logs into their dashboard. Behind the scenes, the web server verifies their identity and issues a secure token, ensuring that any data they view or transmit belongs strictly to them.

**Step 2: Preparing the Connection**
When the user is ready to scan their local files, they go to the "Connect Info" section on their dashboard. Because multiple users might be using the system at the same time, the server needs a way to keep everyone's data traffic separated. To do this, the backend API dynamically creates a temporary, dedicated "lane" (a network port) specifically for this user. The web interface then gives the user a unique connection string and a downloadable Python script.

**Step 3: The Local Script Execution**
The user opens their local computer terminal and runs the provided script using the connection string. This script acts as the engine. It quietly scans the files on the user's local machine and calculates the MD5 hash (the fingerprint) for each one. 

**Step 4: The TCP/IP Socket Transmission**
As the script calculates these hashes, it opens a direct TCP/IP socket connection to the server using the dedicated port assigned in Step 2. It begins streaming the data—file names, folder paths, and MD5 hashes—directly to the backend. Because this happens via a socket connection in the background, the web server is not blocked. The user is completely free to continue clicking around the website, reading guides, or adjusting their profile while the transmission happens invisibly.

**Step 5: Real-Time Resolution and Storage**
As the backend receives this stream of data, it saves it into the database. Because the frontend dashboard is linked to this database, the user's web interface updates in real-time. Once the script finishes sending all the data, the backend closes the dedicated port to free up system resources. 

**Step 6: The Integrity Check (The Re-Scan)**
The true value of the system happens days or weeks later. The user runs a "Re-Scan" using the same script. The script calculates fresh hashes for the local files and sends them to the server. The server instantly compares the new incoming hashes against the original "baseline" hashes saved in Step 5. If the hashes match, the file is safe. If they do not match, the system flags the file as altered or corrupted.

## ⚙️ System Functionalities Breakdown

Here is how the user interacts with the results of that workflow through the dashboard features:

* 🔌 **Connect Info:** The gateway feature. This is where the user gets their script and the dynamically generated port address to establish the TCP/IP connection.
* 📊 **LastScan:** A real-time view. While the baseline scan is running, or immediately after it finishes, this screen shows the live data (file paths and their original MD5 hashes) as it is saved to the database.
* 📁 **ScanJobs:** The archive. Since a user might want to monitor different folders at different times, this acts as a history book, listing all the initial baseline scans they have ever performed.
* 🔍 **GetScan:** The retrieval tool. If a user wants to look back at the original hashes of a specific baseline scan, they use this feature to pull up that exact data.
* 🚨 **LastReScan:** The alert center. After a user runs a secondary check, this screen displays the comparative results. It highlights any discrepancies between the old hashes and the new hashes, instantly showing the user which files have been tampered with.
* 🕰️ **GetReScan:** The historical comparison tool. Just like GetScan, this allows the user to pull up the results of any old re-scan they performed in the past.
* 🗑️ **Delete features (DeleteScan / DeleteReScan):** Data management. Users can cleanly erase a specific re-scan report if they no longer need it, or delete an entire baseline scan (which automatically wipes out any re-scans associated with it to keep the database clean).

## 🔒 The Security Mechanism: Identity and Anti-Hijacking

A system monitoring file integrity must itself be heavily secured. The architecture employs a multi-layered defense model to guarantee that only the genuine user can trigger scans or view their sensitive local file structures.

* 🔑 **The Foundation (OAuth 2.0 & JWT):** When a user successfully authenticates, the FastAPI backend generates a JSON Web Token (JWT). This acts as a digital passport. The Django frontend securely stores this JWT inside a session cookie, allowing the user to navigate the application without having to log in on every single page load.
* 🛡️ **The Custom Anti-Hijacking Layer:** Standard cookie-based authentication carries a specific risk: if a malicious actor manages to copy or steal the user's session cookie, they could theoretically bypass the login screen (a technique known as Session Hijacking). To neutralize this threat, a custom validation layer was engineered directly into Django. 
* ✅ **Active Credential Verification:** Even if an attacker injects a stolen JWT cookie into their browser, the system will reject them. The custom security layer dictates that the system can *only* be accessed if the current session state proves the user actively and explicitly logged in using their manual username and password credentials. The stolen token is rendered completely useless without the accompanying, verified active login event.

## 📸 System Snapshots

### 1. Web Work Flow

<img width="801" height="786" alt="image3" src="https://github.com/user-attachments/assets/817031e3-acaf-4e37-8d5b-c6f281b29a96" />

### 2. Core Architecture

<img width="802" height="667" alt="image2" src="https://github.com/user-attachments/assets/9d4cd175-e2e8-43ea-9e40-8f99394afd6f" />

### 3. API Structure


<img width="541" height="501" alt="image5" src="https://github.com/user-attachments/assets/f19e1ef9-c30d-444e-b0c9-04f52c2f6ae7" />

---

## 🎥 Web System Walkthrough

[![Web System Walkthrough](https://img.youtube.com/vi/Fb5hqY5pbBU/hqdefault.jpg)](https://www.youtube.com/playlist?list=PLEGGwbX6woRl8fk_Fyb844V0y6c92zs_J)

*Click the image above to watch the full system walkthrough playlist on YouTube.*
