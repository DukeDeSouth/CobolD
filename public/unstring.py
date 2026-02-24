"""COBOL unstring.cob translated to Python.

Emulates COBOL UNSTRING statement as a state machine with 7 sub-mechanics:
pointer, tallying, count, delimiter capture, overflow, ALL, multiple delimiters.
"""

import sys


def display(*parts):
    """COBOL DISPLAY: concatenate all parts, append newline."""
    out = b""
    for p in parts:
        if isinstance(p, (bytes, bytearray)):
            out += bytes(p)
        else:
            out += str(p).encode("latin-1")
    sys.stdout.buffer.write(out + b"\n")


def pic_x(value, width):
    """MOVE to PIC X(n) — left-justified, space-padded."""
    if isinstance(value, str):
        return value.ljust(width)[:width]
    return value.decode("latin-1").ljust(width)[:width]


def pic_9(value, width):
    """MOVE to PIC 9(n) — right-justified, zero-padded."""
    s = str(int(value))
    return s.zfill(width)[-width:]


def pic_9_comp(value, width):
    """DISPLAY PIC 9(n) COMP — same as PIC 9 display."""
    return f"{value:0{width}d}"


def format_index(value):
    """INDEX display format: sign + 9 digits."""
    return f"{value:+010d}"


def format_pic_dollar(value):
    """PIC $999,999.99 — fixed insertion, no zero suppression."""
    int_part = int(value)
    frac_part = int(round((abs(value) - abs(int_part)) * 100))
    digits = f"{int_part:06d}"
    return f"${digits[:3]},{digits[3:]}.{frac_part:02d}"


def cobol_unstring(source, delimiters, destinations, *,
                   pointer=None, tallying=None, use_all=False):
    """COBOL UNSTRING emulation.

    Args:
        source: source string (PIC X)
        delimiters: list of delimiter strings
        destinations: list of dicts with keys:
            'value_width': int (PIC X width for dest)
            'value_numeric_width': int or None (PIC 9 width if numeric dest)
            'delim_width': int or None (DELIMITER IN PIC width)
            'count_width': int or None (COUNT IN PIC 9 width)
        pointer: initial pointer value (1-indexed) or None
        tallying: initial tallying value or None
        use_all: if True, DELIMITED BY ALL

    Returns:
        dict with:
            'overflow': bool
            'pointer': int (1-indexed)
            'tallying': int
            'results': list of dicts {value, delimiter, count}
    """
    pos = (pointer or 1) - 1
    src_len = len(source)
    tally = tallying or 0
    results = []

    for dest in destinations:
        if pos >= src_len:
            results.append({
                "value": " " * dest.get("value_width", 1),
                "delimiter": " " * dest.get("delim_width", 1) if dest.get("delim_width") else "",
                "count": 0,
            })
            continue

        found_delim = None
        found_pos = None

        for i in range(pos, src_len):
            for d in delimiters:
                if source[i:i + len(d)] == d:
                    found_delim = d
                    found_pos = i
                    break
            if found_delim is not None:
                break

        if found_delim is not None:
            segment = source[pos:found_pos]
            count = len(segment)
            new_pos = found_pos + len(found_delim)

            if use_all:
                while new_pos + len(found_delim) <= src_len and \
                        source[new_pos:new_pos + len(found_delim)] == found_delim:
                    new_pos += len(found_delim)

            pos = new_pos
        else:
            segment = source[pos:]
            count = len(segment)
            found_delim = ""
            pos = src_len

        vw = dest.get("value_width", 15)
        nw = dest.get("value_numeric_width")
        dw = dest.get("delim_width")
        cw = dest.get("count_width")

        if nw:
            val = pic_9(segment.strip() if segment.strip() else "0", nw)
        else:
            val = pic_x(segment, vw)

        delim_out = pic_x(found_delim, dw) if dw else found_delim

        count_val = count
        if cw:
            count_val = int(pic_9(count, cw))

        tally += 1
        results.append({
            "value": val,
            "delimiter": delim_out,
            "count": count_val,
        })

    overflow = (pos < src_len)

    return {
        "overflow": overflow,
        "pointer": pos + 1,
        "tallying": tally,
        "results": results,
    }


def main():
    ws_source_str = pic_x("Hello World", 30)
    ws_part_1 = pic_x("", 15)
    ws_part_2 = pic_x("", 15)
    ws_delimiter = "|"

    ws_single_fields_filled = 0
    ws_single_dest_str = pic_x("", 5)
    ws_single_delimiter = " "
    ws_single_char_count = 0

    ws_multi_fields_filled = 0
    ws_multi_dest_str = [pic_x("", 5) for _ in range(6)]
    ws_multi_char_count = [0] * 6
    ws_multi_delimiter = [" "] * 6

    ws_pointer = 0
    ws_source_num = ""
    ws_dest_num = ["000"] * 3

    # EX 1
    display(b" ")
    display(b"=================================================")
    display(b"EX 1 : SIMPLE UNSTRING")
    display(b" ")
    display(b"SOURCE STRING: ", ws_source_str.encode("latin-1"))

    res = cobol_unstring(ws_source_str, [" "],
                         [{"value_width": 15}, {"value_width": 15}])
    ws_part_1 = res["results"][0]["value"]
    ws_part_2 = res["results"][1]["value"]

    display(b"PART1: ", ws_part_1.encode("latin-1"))
    display(b"PART2: ", ws_part_2.encode("latin-1"))

    # EX 2
    ws_pointer = 1

    display(b" ")
    display(b"=================================================")
    display(b"EX 2 : UNSTRING MULTIPLE TIMES INTO SAME DEST.")

    display(b" ")
    display(b"SOURCE STRING: ", ws_source_str.encode("latin-1"))

    for _ in range(2):
        res = cobol_unstring(ws_source_str, [" "],
                             [{"value_width": 15}],
                             pointer=ws_pointer, use_all=True)
        ws_part_1 = res["results"][0]["value"]
        ws_pointer = res["pointer"]

        if res["overflow"]:
            display(b"ERROR: OVERFLOW")
        else:
            display(b"Successfully unstrung.")

        display(b"PART VALUE: ", ws_part_1.encode("latin-1"))
        display(b"POINTER: ", pic_9_comp(ws_pointer, 5).encode("latin-1"))

    # EX 3
    display(b" ")
    display(b"=================================================")
    display(b"EX 3 : UNSTRING INTO EXPLICIT FIELDS")

    ws_pointer = 1

    display(b" ")
    display(b"SOURCE STRING: ", ws_source_str.encode("latin-1"))

    res = cobol_unstring(ws_source_str, [" "],
                         [{"value_width": 15}, {"value_width": 15}],
                         pointer=ws_pointer, use_all=True)
    ws_part_1 = res["results"][0]["value"]
    ws_part_2 = res["results"][1]["value"]
    ws_pointer = res["pointer"]

    if res["overflow"]:
        display(b"ERROR: OVERFLOW")
    else:
        display(b"Successfully unstrung.")

    display(b"PART1: ", ws_part_1.encode("latin-1"))
    display(b"PART2: ", ws_part_2.encode("latin-1"))
    display(b"POINTER: ", pic_9_comp(ws_pointer, 5).encode("latin-1"))

    # EX 4
    display(b" ")
    display(b"=================================================")
    display(b"EX 4 : UNSTRING WITH MULTIPLE DELIMITERS ")

    ws_pointer = 1
    ws_source_str = pic_x("A E%FG!HIJ|KL!MN>OP#QR!ST", 30)
    ws_single_fields_filled = 0

    display(b" ")
    display(b"SOURCE STRING: ", ws_source_str.encode("latin-1"))

    while ws_pointer <= len(ws_source_str):
        res = cobol_unstring(
            ws_source_str, ["<", ">", "!", ws_delimiter],
            [{"value_width": 5, "delim_width": 1, "count_width": 1}],
            pointer=ws_pointer, tallying=ws_single_fields_filled,
            use_all=True)

        r = res["results"][0]
        ws_single_dest_str = r["value"]
        ws_single_delimiter = r["delimiter"]
        ws_single_char_count = r["count"]
        ws_pointer = res["pointer"]
        ws_single_fields_filled = res["tallying"]

        display(b" ")
        display(b"VALUE: ", ws_single_dest_str.encode("latin-1"))
        display(b"DELIMITER: ", ws_single_delimiter.encode("latin-1"))
        display(b"CHAR COUNT:", pic_9(ws_single_char_count, 1).encode("latin-1"))
        display(b"CURRENT POINTER: ", pic_9_comp(ws_pointer, 5).encode("latin-1"))
        display(b"TOTAL FIELDS FILLED: ",
                pic_9(ws_single_fields_filled, 2).encode("latin-1"))
        display(b"-------------------------------------------")

    # EX 5
    display(b" ")
    display(b"=================================================")
    display(b"EX 5 : UNSTRING WITH MULTIPLE DELIMITERS "
            b"INTO MULTIPLE DESTINATIONS")

    ws_source_str = pic_x("A EFG!HIJ|KLMN>O", 30)
    ws_multi_fields_filled = 0

    display(b" ")
    display(b"SOURCE STRING: ", ws_source_str.encode("latin-1"))

    dests = [{"value_width": 5, "delim_width": 1, "count_width": 1}
             for _ in range(6)]

    res = cobol_unstring(
        ws_source_str, ["<", ">", "!", ws_delimiter],
        dests, tallying=ws_multi_fields_filled, use_all=True)

    ws_multi_fields_filled = res["tallying"]
    for i in range(6):
        ws_multi_dest_str[i] = res["results"][i]["value"]
        ws_multi_delimiter[i] = res["results"][i]["delimiter"]
        ws_multi_char_count[i] = res["results"][i]["count"]

    for idx in range(6):
        display(b" ")
        display(b"STRING NUMBER: ", format_index(idx + 1).encode("latin-1"))
        display(b"VALUE: ", ws_multi_dest_str[idx].encode("latin-1"))
        display(b"DELIMITER: ", ws_multi_delimiter[idx].encode("latin-1"))
        display(b"CHAR COUNT:", pic_9(ws_multi_char_count[idx], 1).encode("latin-1"))
        display(b"-------------------------------------------")

    display(b"TOTALS: ")
    display(b"FIELDS FILLED: ", pic_9(ws_multi_fields_filled, 2).encode("latin-1"))

    # EX 6
    display(b" ")
    display(b"=================================================")
    display(b"EX 6 : UNSTRING FORMATTED NUMBER")
    display(b" ")

    ws_source_num = format_pic_dollar(123456.12)
    display(b"SOURCE VALUE: ", ws_source_num.encode("latin-1"))

    ref_mod = ws_source_num[1:]

    res = cobol_unstring(
        ref_mod, [",", "."],
        [{"value_width": 3, "value_numeric_width": 3},
         {"value_width": 3, "value_numeric_width": 3},
         {"value_width": 3, "value_numeric_width": 3}])

    ws_dest_num[0] = res["results"][0]["value"]
    ws_dest_num[1] = res["results"][1]["value"]
    ws_dest_num[2] = res["results"][2]["value"]

    display(b"PART 1: ", ws_dest_num[0].encode("latin-1"))
    display(b"PART 2: ", ws_dest_num[1].encode("latin-1"))
    display(b"PART 3: ", ws_dest_num[2].encode("latin-1"))
    display(b" ")


if __name__ == "__main__":
    main()
