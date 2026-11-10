# SE Lab 7 - Fuzzing for Input Validation Bugs (shopping cart)

Student: Dhruv Rajagopalan, PES1UG24AM086, Section B.

The first commit holds the assigned Lab 7 starter files, copied unchanged from
https://github.com/SETAPESU26/L6_L7_23_shopping_cart (folder "Lab 7"). That repo has no license file; all rights to those two files stay with the course/instructor.
The handout calls them processor.py / test_processor.py; the assigned repo names them shopping_cart.py / test_shopping_cart.py, so those names are kept.

Later commits add the Hypothesis fuzz tests, the hardened `shopping_cart.py`, and a PDF of terminal screenshots.
The tests and fixes were prepared with AI assistance and run on a separate Linux computer, not the student's laptop.

Run:
    pip install hypothesis pytest
    python shopping_cart.py
    python -m pytest test_shopping_cart.py

Hardening choices (see the header comment in shopping_cart.py): invalid input returns None, cart prices/quantities are whole ASCII-digit numbers,
promo codes are OFF0-OFF100 (an assumption: the original accepted any number), pincodes are 6 digits starting 1-8 (the ZONES table has no 0 or 9).
