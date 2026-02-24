      *****************************************************************
      * SAVINGS — VERIFICATION: 3 test cases, original vs fixed
      *****************************************************************
       identification division.
       program-id. savings-verify.

       data division.
       working-storage section.

       01 ORIG-FIELDS.
              05 O-PV     PIC S9(9)V99 USAGE COMP.
              05 O-AI     PIC 99V9(4) USAGE COMP.
              05 O-MI     PIC 9V9(6) USAGE COMP.
              05 O-MONTHS PIC 999 USAGE COMP.
              05 O-DENOM  PIC S9(9)V9(6) USAGE COMP.
              05 O-FV     PIC S9(9)V99 USAGE COMP.

       01 FIXED-FIELDS.
              05 F-PV     PIC S9(9)V99 USAGE COMP.
              05 F-AI     PIC 99V9(4) USAGE COMP.
              05 F-MI     USAGE COMP-2.
              05 F-MONTHS PIC 999 USAGE COMP.
              05 F-CF     USAGE COMP-2.
              05 F-FV     PIC S9(9)V99 USAGE COMP.

       01 DISP.
              05 D-ORIG   PIC $ZZZ,ZZZ,ZZ9.99.
              05 D-FIXED  PIC $ZZZ,ZZZ,ZZ9.99.

       procedure division.
       main-procedure.
           display "=== SAVINGS BUG-FIX VERIFICATION ==="

           display space
           display "TEST 1: $10,000 at 5.00% for 10 years"
           display "Expected:         $    16,470.09"
           perform calc-original-1
           perform calc-fixed-1

           display space
           display "TEST 2: $50,000 at 8.50% for 25 years"
           display "Expected:         $   415,520.65"
           perform calc-original-2
           perform calc-fixed-2

           display space
           display "TEST 3: $1,000 at 3.25% for 30 years"
           display "Expected:         $     2,647.68"
           perform calc-original-3
           perform calc-fixed-3

           stop run.

       calc-original-1.
           move 10000 to O-PV
           move 5 to O-AI
           multiply 12 by 10 giving O-MONTHS
           divide O-AI by 1200 giving O-MI rounded
           compute O-DENOM = (1 + O-MI) ** O-MONTHS
           compute O-FV = O-PV * O-DENOM
           move O-FV to D-ORIG
           display "Original:         " D-ORIG.

       calc-fixed-1.
           move 10000 to F-PV
           move 5 to F-AI
           multiply 12 by 10 giving F-MONTHS
           divide F-AI by 1200 giving F-MI
           compute F-CF = (1 + F-MI) ** F-MONTHS
           compute F-FV rounded = F-PV * F-CF
           move F-FV to D-FIXED
           display "Fixed:            " D-FIXED.

       calc-original-2.
           move 50000 to O-PV
           move 8.5 to O-AI
           multiply 12 by 25 giving O-MONTHS
           divide O-AI by 1200 giving O-MI rounded
           compute O-DENOM = (1 + O-MI) ** O-MONTHS
           compute O-FV = O-PV * O-DENOM
           move O-FV to D-ORIG
           display "Original:         " D-ORIG.

       calc-fixed-2.
           move 50000 to F-PV
           move 8.5 to F-AI
           multiply 12 by 25 giving F-MONTHS
           divide F-AI by 1200 giving F-MI
           compute F-CF = (1 + F-MI) ** F-MONTHS
           compute F-FV rounded = F-PV * F-CF
           move F-FV to D-FIXED
           display "Fixed:            " D-FIXED.

       calc-original-3.
           move 1000 to O-PV
           move 3.25 to O-AI
           multiply 12 by 30 giving O-MONTHS
           divide O-AI by 1200 giving O-MI rounded
           compute O-DENOM = (1 + O-MI) ** O-MONTHS
           compute O-FV = O-PV * O-DENOM
           move O-FV to D-ORIG
           display "Original:         " D-ORIG.

       calc-fixed-3.
           move 1000 to F-PV
           move 3.25 to F-AI
           multiply 12 by 30 giving F-MONTHS
           divide F-AI by 1200 giving F-MI
           compute F-CF = (1 + F-MI) ** F-MONTHS
           compute F-FV rounded = F-PV * F-CF
           move F-FV to D-FIXED
           display "Fixed:            " D-FIXED.
