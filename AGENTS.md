# Project Context
This is an internal Hotel and Restaurant Management System built with Python and Django. 

The system handles back-office operations for staff:
1. Hotel Module: Room types, room availability, guest check-ins, and room billing.
2. Restaurant Module: Menu items, tables, dining orders, and the ability to charge restaurant receipts directly to a guest's room folio.
3. Restaurant Stock Module: Allows the manager to input a daily opening quota of available plates for each menu item every morning. Automatically counts down as plates are sold, blocks orders when stock hits zero, and generates an end-of-day reconciliation report comparing portions sold against expected revenue.
