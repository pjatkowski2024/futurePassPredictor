#!/bin/bash
python3 futurePassPredictor.py >passes.html
scp passes.html rover:auto137/passes.html
