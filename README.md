#Knesset Protocol Analysis Tools
This repository contains tools for preprocessing and analyzing Israeli Knesset (Parliament) protocols, with a focus on identifying and processing hurmful discourse.
#Data Collection and Preprocessing
Step 1: Collecting Knesset Protocols
File: collect_protocols.py
This script collects Knesset committee protocols from the official OKnesset repository. It:

Crawls the Knesset website for protocol text files
Filters protocols containing harmful language or calls to order
Saves relevant protocols locally with UTF-8 encoding
Handles Hebrew text and special characters appropriately
