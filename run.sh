python -u ./worker.py | awk '{printf "<br>%s\n",$ fflush()}' > worker.html
