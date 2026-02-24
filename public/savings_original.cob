      *****************************************************************
      * SAVINGS — ORIGINAL CODE from github.com/cchipman21804/Savings
      * Adapted to batch (ACCEPT replaced with hardcoded test values)
      * to enable automated verification.
      *
      * Test case: $10,000 at 5% annual for 10 years
      * Expected: $10,000 * (1 + 0.05/12)^120 = $16,470.09
      *****************************************************************
       identification division.
       program-id. savings-orig.

       data division.
       working-storage section.

       01 CALC-FIELDS.
              05 PRESENT-VALUE     PIC S9(9)V99 USAGE COMP.
              05 ANNUAL-INTEREST   PIC 99V9(4) USAGE COMP.
              05 MONTHLY-INTEREST  PIC 9V9(6) USAGE COMP.
              05 LOAN-TERM-YEARS   PIC 99 USAGE COMP.
              05 LOAN-TERM-MONTHS  PIC 999 USAGE COMP.
              05 NUMERATOR         PIC S9(9)V9(6) USAGE COMP.
              05 DENOMINATOR       PIC S9(9)V9(6) USAGE COMP.
              05 FUTURE-VALUE      PIC S9(9)V99 USAGE COMP.

       01 DISP-FIELDS.
              05 FV-OUT            PIC $ZZ,ZZZ,ZZ9.99 USAGE DISPLAY.
              05 PRINCIPAL         PIC $ZZZ,ZZZ,ZZ9.99 USAGE DISPLAY.
              05 INTEREST-RATE     PIC Z9.99 USAGE DISPLAY.
              05 LOAN-TERM-OUT     PIC Z9 USAGE DISPLAY.

       procedure division.
       init-ws.
              initialize calc-fields
              initialize disp-fields.

       set-test-values.
              move 10000 to present-value
              move 5 to annual-interest
              move 10 to loan-term-years.

       calculate-it.
              move loan-term-years to loan-term-out
              move present-value to principal
              move annual-interest to interest-rate

              multiply 12 by loan-term-years giving loan-term-months
              divide annual-interest by 1200 giving monthly-interest
              rounded

              compute denominator = (1+monthly-interest) **
              loan-term-months

              compute future-value = present-value *
              denominator

              move future-value to fv-out.

       disp-result.
              display "=== SAVINGS CALCULATOR (ORIGINAL) ==="
              display "Principal:     " principal
              display "Term:          " loan-term-out " years"
              display "Interest Rate: " interest-rate "%"
              display "Future Value:  " fv-out
              display space
              display "Expected:      $ 16,470.09"
              display "(formula: 10000 * (1+0.05/12)^120)".

       end-program.
              stop run.
