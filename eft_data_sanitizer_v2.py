import os
import csv
import re

security_name = None
start_date = None
end_date = None

input_dir = 'input'


class Record:
    def __init__(self, date, value):
        self.date = date
        self.value = value

    def is_empty(self):
        if not (self.date.strip() and self.value.strip()):
            return True
        else:
            return False


def get_security_info(field_name, value):
    global security_name
    global start_date
    global end_date

    if security_name is None and field_name.lower() == "security":
        security_name = value
    elif field_name.lower() == "start date":
        start_date = value
    elif field_name.lower() == "end date":
        end_date = value


def remove_empty_columns_from_csv(all_columns):
    final_columns = []

    for column in all_columns:
        if column:
            final_columns.append(column)

    return final_columns


def get_field_names(top_row):
    name_list = []

    for i in range(1, len(top_row), 2):
        name_list.append(top_row[i])

    return name_list


def find_all_common_dates(all_columns):
    all_common_dates = []

    for ref_entry in all_columns[0]:
        matches_found = 0

        for i in range(1, len(all_columns)):
            for entry in all_columns[i]:
                if entry.date == ref_entry.date or entry.is_empty or entry is None:
                    matches_found += 1
                    break

        if matches_found == len(all_columns) - 1:
            all_common_dates.append(ref_entry.date)

    return all_common_dates


def remove_extra_dates(column, all_common_dates):
    new_column = []
    for entry in column:
        if entry.date in all_common_dates:
            new_column.append(entry)

    return new_column


def fix_dates_with_error(all_dates):
    for i in range(len(all_dates)):
        if not re.search(r"\d+\/\d+\/\d+", all_dates[i]):
            next_date = all_dates[i + 1]
            next_day = next_date.split("/")[1]
            next_month = next_date.split("/")[0]
            next_year = next_date.split("/")[2]
            fixed_date = next_month + "/" + str(int(next_day) - 1) + "/" + next_year
            all_dates[i] = fixed_date


def get_full_row_for_this_date(date, all_columns):
    full_row = [""] * (len(all_columns) + 1)

    for i in range(len(all_columns)):
        for entry in all_columns[i]:
            if entry.date == date:
                full_row[i] = entry.value
                break

    return full_row


def get_all_csv_files():
    filelist = []

    if not os.path.isdir(input_dir):
        os.mkdir(input_dir)
    for file in os.listdir(input_dir):
        if file.endswith(".csv"):
            filelist.append(file)

    return filelist


def output_sanitized_csv(raw_csv_file):
    all_records = []
    field_names = []

    is_first_row = True
    with open(os.path.join(input_dir, raw_csv_file), newline="") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        for row in csv_reader:
            get_security_info(row[0], row[1])
            if is_first_row:
                field_names = get_field_names(row[2:])
                for i in range(len(field_names)):
                    records_for_single_field = []
                    all_records.append(records_for_single_field)

            else:
                for i in range(len(field_names)):
                    new_record = Record(row[2 * i + 2], row[2 * i + 3])
                    if not new_record.is_empty():
                        all_records[i].append(new_record)

            is_first_row = False

    all_records = remove_empty_columns_from_csv(all_records)
    all_common_dates = find_all_common_dates(all_records)

    for i in range(len(all_records)):
        all_records[i] = remove_extra_dates(all_records[i], all_common_dates)

    # output_filename = os.path.join("output",  security_name + " " + start_date + " to " + end_date + ".csv")
    output_filename = "output" + os.path.sep + security_name + ".csv"
    if not os.path.isdir("output"):
        os.mkdir("output")

    with open(output_filename, mode="w", newline="") as output_file:
        output_writer = csv.writer(output_file, delimiter=",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(["Date"] + field_names)

        csv_output_data = []

        for date in all_common_dates:
            csv_output_data.append(get_full_row_for_this_date(date, all_records))

        fix_dates_with_error(all_common_dates)

        for i in range(len(all_common_dates)):
            output_writer.writerow([all_common_dates[i]] + csv_output_data[i])


csv_filelist = get_all_csv_files()

for file in csv_filelist:
    print("Fixing file: " + file + "...")
    security_name = None
    output_sanitized_csv(file)
    print(file + " sanitized successfully.")
