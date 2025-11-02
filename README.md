# Project CA2 – Operating System Scheduling Simulator

## Overview
This project simulates various CPU scheduling algorithms such as:
- First Come First Serve (FCFS)
- Shortest Job First (SJF)
- Priority Scheduling
- Round Robin

Developed for *CSE316 (Operating System)* CA2 submission.

## Modules
1. *Process Input Module* – accepts process ID, burst time, arrival time, priority  
2. *Algorithm Module* – runs FCFS, SJF, RR, Priority  
3. *Gantt Chart Module* – displays scheduling order  
4. *Performance Metrics Module* – calculates waiting & turnaround times  

## How to Run
If the project is in C language:
```bash
gcc main.c -o scheduler
./scheduler
