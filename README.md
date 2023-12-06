# File Exchange System - Developer's Guide

## Introduction
Welcome to the File Exchange System, the culminating project for this course. This system empowers developers to create a robust file-sharing mechanism using either TCP or UDP protocols. The project involves implementing both a server and a client application, with language options including C, Java, or Python. Grouping up to three (3) students for collaboration is encouraged.

## Client Application Specifications:

1. **User Interface (UI):** The client application serves as the UI for users interacting with the File Exchange System.

2. **Input Commands:**
   - Connect to the server application: `/join <server_ip_add> <port>` (e.g., `/join 192.168.1.1 12345`)
   - Disconnect from the server application: `/leave`
   - Register a unique handle or alias: `/register <handle>` (e.g., `/register User1`)
   - Send a file to the server with timestamp: `/store <filename>` (e.g., `/store Hello.txt`)
   - Request directory file list from the server: `/dir`
   - Fetch a file from the server: `/get <filename>` (e.g., `/get Hello.txt`)
   - Request command help: `/?` or `/help`

3. **Output Area:** The client application includes an output area displaying server status from other users and system messages.

4. **Chat Room Functionality:** Additionally, the client application implements chat room functionality, supporting both unicast and broadcast modes.
