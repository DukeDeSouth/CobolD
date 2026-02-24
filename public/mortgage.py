"""COBOL mortgage.cob translated to Python."""

from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN

TWO_PLACES = Decimal("0.01")


def format_pic_dollar(value, int_digits=5):
    """Format value as COBOL PIC $ZZ,ZZ9.99."""
    abs_val = abs(value)
    int_part = int(abs_val)
    frac_cents = int(round((abs_val - int_part) * 100))

    overflow = int_part >= 10 ** int_digits
    int_part = int_part % (10 ** int_digits)

    int_str = f"{int_part:0{int_digits}d}"

    # PIC $ZZ,ZZ9.99 for 5 digits: "XX,XXX"
    digits_with_comma = int_str[0:2] + "," + int_str[2:5]
    result = list(digits_with_comma)

    if not overflow:
        suppressing = True
        for i in range(len(result) - 1):
            if not suppressing:
                break
            if result[i] == "0":
                result[i] = " "
            elif result[i] == ",":
                result[i] = " "
            else:
                suppressing = False

    return "$" + "".join(result) + "." + f"{frac_cents:02d}"


def rounded_2(value):
    """Round to 2 decimal places."""
    return value.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)


def truncate_2(value):
    """COBOL COMPUTE without ROUNDED — truncation."""
    return value.quantize(TWO_PLACES, rounding=ROUND_DOWN)


def main():
    # --- DATA DIVISION / WORKING-STORAGE ---
    balance_start = Decimal("100000.00")
    years = 30
    repayment = Decimal("500.00")
    interest_rate = Decimal("5.50")

    # --- PROCEDURE DIVISION / MAIN-PARA ---
    print("MORTGAGE PAYMENT CALCULATOR")
    print(f"BALANCE: {balance_start:09.2f}")
    print(f"YEARS:   {years:02d}")
    print(f"MONTHLY: {repayment:06.2f}")
    print(f"RATE:    {interest_rate:05.2f}")
    print(" ")
    print(" YEAR    START         INTEREST      END")

    # --- PERFORM CALCULATE-INTEREST VARYING WS-YEAR ---
    for ws_year in range(1, years + 1):
        interest = rounded_2(balance_start * interest_rate / Decimal("100"))
        balance_end = truncate_2(
            balance_start + interest - 12 * repayment
        )

        bs_out = format_pic_dollar(balance_start)
        int_out = format_pic_dollar(interest)
        be_out = format_pic_dollar(balance_end)
        print(f"  {ws_year:02d}  {bs_out}  {int_out}  {be_out}")

        balance_start = balance_end


if __name__ == "__main__":
    main()
