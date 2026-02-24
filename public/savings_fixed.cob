      *****************************************************************
      * SAVINGS — FIXED VERSION
      * Original: github.com/cchipman21804/Savings/savings.cbl
      *
      * BUGS FOUND AND FIXED:
      *
      * BUG-1 (CRITICAL): MONTHLY-INTEREST PIC 9V9(6) — only 6
      *   decimal places + ROUNDED at DIVIDE. 5/1200 → 0.004167
      *   instead of 0.00416666... Error compounds over months.
      *   FIX: Use COMP-2 (double-precision float) for intermediate
      *   calculations, eliminate ROUNDED at DIVIDE.
      *
      * BUG-2 (CRITICAL): DENOMINATOR PIC S9(9)V9(6) — compound
      *   factor truncated to 6 decimals, further precision loss.
      *   FIX: Use COMP-2 for compound factor.
      *
      * BUG-3 (CRITICAL): COMPUTE future-value = pv * factor —
      *   no ROUNDED. Result truncated (2647.675 → 2647.67) instead
      *   of rounded (→ 2647.68).
      *   FIX: Add ROUNDED to final COMPUTE.
      *
      * BUG-4 (CODE SMELL): NUMERATOR defined but never used.
      *   Dead code from loan amortization formula copy-paste.
      *   FIX: Removed.
      *
      * BUG-5 (NAMING): Variables say LOAN-TERM but it's a savings
      *   calculator. Misleading for maintenance.
      *   FIX: Renamed to TERM-YEARS / TERM-MONTHS.
      *
      * BUG-6 (DISPLAY): INTEREST-RATE PIC Z9.99 truncates rates
      *   with more than 2 decimal places (e.g. 5.2575%).
      *   FIX: PIC Z9.9(4) for 4 decimal display.
      *
      * Test: $10,000 at 5% for 10 years
      *   Original: $16,470.75 (WRONG)
      *   Fixed:    $16,470.09 (CORRECT)
      *****************************************************************
       identification division.
       program-id. savings-fixed.

       data division.
       working-storage section.

       01 CALC-FIELDS.
              05 PRESENT-VALUE     PIC S9(9)V99 USAGE COMP.
              05 ANNUAL-INTEREST   PIC 99V9(4) USAGE COMP.
              05 MONTHLY-INTEREST  USAGE COMP-2.
              05 TERM-YEARS        PIC 99 USAGE COMP.
              05 TERM-MONTHS       PIC 999 USAGE COMP.
              05 COMPOUND-FACTOR   USAGE COMP-2.
              05 FUTURE-VALUE      PIC S9(9)V99 USAGE COMP.

       01 DISP-FIELDS.
              05 FV-OUT            PIC $ZZ,ZZZ,ZZ9.99 USAGE DISPLAY.
              05 PRINCIPAL         PIC $ZZZ,ZZZ,ZZ9.99 USAGE DISPLAY.
              05 INTEREST-RATE     PIC Z9.9(4) USAGE DISPLAY.
              05 TERM-OUT          PIC Z9 USAGE DISPLAY.

       procedure division.
       init-ws.
              initialize calc-fields
              initialize disp-fields.

       set-test-values.
              move 10000 to present-value
              move 5 to annual-interest
              move 10 to term-years.

       calculate-it.
              move term-years to term-out
              move present-value to principal
              move annual-interest to interest-rate

              multiply 12 by term-years giving term-months
              divide annual-interest by 1200
                  giving monthly-interest

              compute compound-factor =
                  (1 + monthly-interest) ** term-months

              compute future-value rounded =
                  present-value * compound-factor

              move future-value to fv-out.

       disp-result.
              display "=== SAVINGS CALCULATOR (FIXED) ==="
              display "Principal:     " principal
              display "Term:          " term-out " years"
              display "Interest Rate: " interest-rate "%"
              display "Future Value:  " fv-out
              display space
              display "Expected:      $ 16,470.09"
              display "(formula: 10000 * (1+0.05/12)^120)".

       end-program.
              stop run.
