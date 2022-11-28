import pandas as pd
import numpy as np
from time import strftime
import os
import openpyxl

out_diff = []
file_name_1 = ""
file_name_2 = ""

primary_key = "skcatalystid"
is_file_created = False


# Fetch the path of the given file
def path_file(folder, file_name):
    try:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', folder, file_name))
    except Exception as exception_message:
        raise ValueError(str(exception_message))


def get_values_dict(sam_dict):
    list_values = []
    for key, values in sam_dict.items():
        list_values.append(values)
    return list_values


def split_version_file(file_name):
    h = str(file_name).split("\\")[-1]
    j = str(h).split(".csv")[0].replace("_", "")
    print(j)
    # f =  str(file_name).split("master")[1].split(".csv")[0].replace("_", "")
    return j


# #print the catal id not exists
def validate_car_csv(file_name_1, file_name_2, is_excel_output):
    try:

        global tota_diff
        tota_diff = 0
        global total_no_columns
        total_no_columns = ''
        global col_names_has_difference
        col_names_has_difference = []

        file_name_v1 = file_name_1
        file_name_v2 = file_name_2

        # Read the file 1 csv file
        older_version_file = pd.read_csv(file_name_v1)
        older_version_file = older_version_file.drop(['lastmodified'], axis=1)
        # created_by', 'batch_id', 'created_dt

        # Read the file 2 csv file
        latest_version_file = pd.read_csv(file_name_v2)
        latest_version_file = latest_version_file.drop(['lastmodified'], axis=1)

        file_name_1 = split_version_file(file_name_v1)
        file_name_2 = split_version_file(file_name_v2)

        # Sort the values by the catalystid
        sorted_older_fil_data = older_version_file.sort_values(by=[primary_key], ascending=False)

        row_older = len(sorted_older_fil_data)
        sorted_latest_fil_data = latest_version_file.sort_values(by=[primary_key], ascending=False)
        row_latest = len(sorted_latest_fil_data)

        print("Total no.of columns in file 1 = " + str(len(sorted_older_fil_data.columns.tolist())))
        print("Total no.of columns in file 2 = " + str(len(sorted_latest_fil_data.columns.tolist())))

        sorted_older_columns = sorted([col.lower() for col in sorted_older_fil_data.columns.tolist()])
        sorted_latest_columns = sorted([col.lower() for col in sorted_latest_fil_data.columns.tolist()])

        # Find the difference between columns in two files
        columns_difference_older = list(set(sorted_older_columns) - set(sorted_latest_columns))
        columns_difference_latest = list(set(sorted_latest_columns) - set(sorted_older_columns))

        print("Total no.of columns difference File 1 = " + str(columns_difference_older))
        print("Total no.of columns difference File 2 = " + str(columns_difference_latest))

        columns_xtra_latest = ''
        columns_xtra_older = ''
        no_xtra_latest = 0
        no_xtra_older = 0

        # If file 1 columns are not there, then drop the file 2 extra columns
        if columns_difference_older != columns_difference_latest:

            if columns_difference_latest != [] and columns_difference_older != []:
                no_xtra_latest = len(columns_difference_latest)
                columns_xtra_latest = columns_difference_latest
                # #print(columns_xtra_latest)

                # Remove the xtra columnscolumns
                sorted_latest_fil_data = sorted_latest_fil_data.drop(columns=columns_xtra_latest, axis=1)

                # else:
                no_xtra_older = len(columns_difference_older)
                columns_xtra_older = columns_difference_older

                # Remove the xtra columns
                sorted_older_fil_data = sorted_older_fil_data.drop(columns=columns_xtra_older, axis=1)
            elif columns_difference_latest != []:
                no_xtra_latest = len(columns_difference_latest)
                columns_xtra_latest = columns_difference_latest
                # #print(columns_xtra_latest)

                # Remove the xtra columnscolumns
                sorted_latest_fil_data = sorted_latest_fil_data.drop(columns=columns_xtra_latest, axis=1)
            else:
                no_xtra_older = len(columns_difference_older)
                columns_xtra_older = columns_difference_older

                # Remove the xtra columns
                sorted_older_fil_data = sorted_older_fil_data.drop(columns=columns_xtra_older, axis=1)

        print(len(sorted_latest_fil_data.columns))
        print(len(sorted_older_fil_data.columns))

        print(len(sorted_latest_fil_data))
        print(len(sorted_older_fil_data))

        duplcated_catalystids_older = []
        duplcated_catalystids_latest = []
        boolean = sorted_older_fil_data.duplicated(subset=[primary_key]).any()
        if boolean == True:
            older_df = sorted_older_fil_data[sorted_older_fil_data[primary_key].duplicated() == True]

            duplcated_catalystids_older = list(set(older_df[primary_key].tolist()))
            sorted_older_fil_data = sorted_older_fil_data.drop_duplicates(subset=[primary_key], keep='first')

        boolean1 = sorted_latest_fil_data.duplicated(subset=[primary_key]).any()
        if boolean1 == True:
            latest_df = sorted_latest_fil_data[sorted_latest_fil_data[primary_key].duplicated() == True]
            duplcated_catalystids_latest = list(set(latest_df[primary_key].tolist()))
            sorted_latest_fil_data = sorted_latest_fil_data.drop_duplicates(subset=[primary_key], keep='first')

        # find the xtra catalyst ids in  and remove it
        catalyst_ids_xtra_older = filter_extra_catalyst_ids_older_version(sorted_latest_fil_data, sorted_older_fil_data)
        print(catalyst_ids_xtra_older)

        # Flter the extra catalyst id in latest version
        catalyst_ids_xtra_latest = filter_extra_catalystids_latest_version(sorted_latest_fil_data,
                                                                           sorted_older_fil_data)
        print(catalyst_ids_xtra_latest)

        not_existing_catal_id_older = []
        if catalyst_ids_xtra_older != []:
            # Extra catalyst id in older version
            not_existing_catal_id_older = catalyst_ids_xtra_older

            # Removing the extra catalyst id in older version
            sorted_older_fil_data = sorted_older_fil_data[
                ~(sorted_older_fil_data[primary_key].isin(not_existing_catal_id_older))]

        not_existing_catal_id_latest = []
        if catalyst_ids_xtra_latest != []:
            # Extra catalyst id in latest version
            not_existing_catal_id_latest = catalyst_ids_xtra_latest

            # Removing the extra catalyst id in latest version
            sorted_latest_fil_data = sorted_latest_fil_data[
                ~(sorted_latest_fil_data[primary_key].isin(not_existing_catal_id_latest))]

        print(len(sorted_latest_fil_data))
        print(len(sorted_older_fil_data))

        columns_to_change = ['skvid', 'skholisticid', 'cmcurrentage', 'bhrevenuetotalreportingcurrency',
                             'bhrevenueaveragereportingcurrency', 'bhrevenuetotalallbookings',
                             'bhrevenueaveragevalueofextras',
                             'bhrevenueaverageperpax', 'bhrevenueaveragequote', 'bhrevenuetotalmargin',
                             'bhrevenueaveragemargin', 'bhpaxaverageonquotes', 'bhquotelastamount',
                             'bhcsataverage', 'bhcsatwouldrecommend', 'bhbookingstotal',
                             'bhbookingstotalfinancialyeartodate', 'bhbookingstotalfinancialyear2',
                             'bhbookingsaverageleadtime', 'bhrevenuetotallocalcurrency', 'papropensitybucket',
                             'patimebucket', 'bhrevenueaveragediscount', 'papropensity',
                             'bhrevenueaveragelocalcurrency', 'bhrevenuetotalyear2',
                             'bbvisitscountpast30days', 'bbvisitscountpast365days', 'pacustomerrank',
                             'bhpaxaveragenumber',
                             'bhpaxminageonanybooking', 'bhpaxmaxageonanybooking', 'bhquotetotalnumber',
                             'bhquoteaveragenumbertobookings',
                             'bhquoteaveragetimetobooking', 'bbvisitscountpast7days', 'paquoteconversionrank',
                             'paquoteconversionbucket', 'paquoteconversiontimebucket', 'paquoteconversionquoteage',
                             'palikelyhoodinmarketrank', 'bhfeefolasttriprating']

        round_columns = ['bhrevenueyeartodatereportingcurrency', 'bhrevenuetotalreportingcurrency',
                         'bhrevenueaveragelocalcurrency',
                         'bhrevenueaveragereportingcurrency', 'bhrevenuetotalallbookings',
                         'bhrevenueaveragevalueofextras', 'bhrevenueaverageperpax', 'bhrevenueaveragequote',
                         'bhrevenuetotalmargin', 'bhrevenueaveragemargin', 'bhpaxaverageonquotes',
                         'bhrevenueyeartodatelocalcurrency', 'bhrevenuetotallocalcurrency', 'bhrevenuetotalyear2',
                         'bhpaxaveragenumber']

        # Comparing the both version data only
        df1 = sorted_older_fil_data
        df1 = df1.astype(str)
        for colum in columns_to_change:
            if colum in df1.columns:
                df1[colum] = df1[colum].str.replace('.0', '')

        for round_col in round_columns:
            decimals = 2
            if round_col in df1.columns:
                df1[round_col] = pd.to_numeric(df1[round_col], downcast='float', errors='coerce').apply(
                    lambda x: round(x, decimals))
        df1 = df1.astype(str)
        df1 = df1.replace("nan", "\\N")

        df1 = df1.applymap(lambda x: x.lower().strip())
        df1 = df1.set_index(primary_key).reset_index()
        # df1 = df1.reset_index(drop=True)
        # df1 = df1.head(10)
        #
        # Data 2
        df2 = sorted_latest_fil_data
        df2 = df2.astype(str)
        for colum in columns_to_change:
            if colum in df2.columns:
                df2[colum] = df2[colum].str.replace('.0', '')
        for round_col in round_columns:
            decimals = 2
            if round_col in df2.columns:
                df2[round_col] = pd.to_numeric(df2[round_col], downcast='float', errors='coerce').apply(
                    lambda x: round(x, decimals))
        df2 = df2.astype(str)
        df2 = df2.replace("nan", "\\N")
        df2 = df2.applymap(lambda x: x.lower().strip())
        df2 = df2.set_index(primary_key).reset_index()

        # df2 = df2.head(10)

        list_mismatch_records = []
        list_tables = {}
        list_col_mist = {}

        col_names_has_difference = []
        total_no_columns = len(df1.columns)

        file_output_path = ''
        if is_excel_output == "yes":
            # Create the excel file for push all the mismatch records
            file_output_path = "out_car_" + file_name_1 + "__" + file_name_2 + "_" + strftime(
                "%Y-%m-%d-%I_%M_%S" + ".xlsx")
            wb = openpyxl.Workbook()
            wb.save(path_file("results", file_output_path))
            wb.close()

        # df1 = df1.pivot_table(index=[primary_key], aggfunc='size')
        list_excel_results = []

        for columns in df1.columns:
            # Compare the two files data , give the results
            resuls = print_difference_two_df(df1, df2, columns, path_file("results", file_output_path), is_excel_output)

            list_mismatch_records.append(int(resuls[0]))
            list_col_mist[columns] = int(resuls[0])

            if resuls[1] != "MATCHED":
                col_names_has_difference.append(columns)
                list_tables[columns] = resuls[1]
            if resuls[3] != {}:
                list_excel_results.append(resuls[3])



        tota_diff = sum(list_mismatch_records)

        #
        if columns_xtra_older == '':
            columns_xtra_older = "None"

        if columns_xtra_latest == '':
            columns_xtra_latest = "None"

        if not_existing_catal_id_latest == []:
            not_existing_catal_id_latest = "None"
            len_not_existing_catal_id_latest = 0
        else:
            len_not_existing_catal_id_latest = len(not_existing_catal_id_latest)
            if len_not_existing_catal_id_latest > 10:
                not_existing_catal_id_latest = not_existing_catal_id_latest[:10]

        if not_existing_catal_id_older == []:
            not_existing_catal_id_older = "None"
            len_not_existing_catal_id_older = 0
        else:
            len_not_existing_catal_id_older = len(not_existing_catal_id_older)

        output_file_name = "output_for_version_" + file_name_1 + "__" + file_name_2 + "_" + strftime(
            "%Y-%m-%d-%I_%M_%S" + ".html")

        with open(path_file("results", output_file_name), 'w') as file:
            file.write("<html>")
            # file.write("<body bgcolor='#ccfff3'>")
            file.write("<table border=1 >")
            file.write("<tr>")
            file.write("<th> Number of rows in  <font color='red'> " + file_name_1 + "</font> version </th>")
            file.write("<th> Number of rows in <font color='red'>" + file_name_2 + "</font> version </th>")
            file.write("</tr>")
            file.write("<td>" + str(row_older) + "</td>")
            file.write("<td>" + str(row_latest) + "</td>")
            file.write("</tr>")
            file.write("</table>")
            file.write("<br>")

            file.write("<center><b>COLUMNS CHECKS<b></center>")
            file.write("<br>")
            file.write("<table border=1 >")
            file.write("<tr>")
            file.write("<th># Missing columns in  <font color='red'>" + file_name_2 + "</font> version </th>")
            file.write("<th> Columns names </th>")
            file.write("</tr>")
            file.write("<td>" + str(no_xtra_older) + "</td>")
            file.write("<td>" + str(columns_xtra_older) + "</td>")
            file.write("</tr>")
            file.write("</table>")
            file.write("<br>")

            file.write("<table border=1 >")
            file.write("<tr>")
            file.write("<th> # Additional Columns in <font color='red'>" + file_name_2 + "</font> version </th>")
            file.write("<th> Columns names </th>")
            file.write("</tr>")
            file.write("<td>" + str(no_xtra_latest) + "</td>")
            file.write("<td>" + str(columns_xtra_latest) + "</td>")
            file.write("</tr>")
            file.write("</table>")
            file.write("<br>")

            file.write("<center><b>CATALYST ID's CHECKS<b></center>")
            file.write("<br>")
            file.write("<table border=1 >")
            file.write("<tr>")
            file.write("<th> # Missing Catalyst id's in <font color='red'>" + file_name_2 + "</font> version </th>")
            file.write("<th> Sample Catalyst id's </th>")
            file.write("</tr>")
            file.write("<td>" + str(len_not_existing_catal_id_older) + "</td>")
            file.write("<td>" + str(not_existing_catal_id_older) + "</td>")
            file.write("</tr>")
            file.write("</table>")

            file.write("<br>")

            file.write("<table border=1 >")
            file.write("<tr>")
            file.write(
                "<th> # Additional Catalyst id's in  <font color='red'>" + file_name_2 + "</font> version </th>")
            file.write("<th> Sample Catalyst id's </th>")
            file.write("</tr>")
            file.write("<td>" + str(len_not_existing_catal_id_latest) + "</td>")
            file.write("<td>" + str(not_existing_catal_id_latest) + "</td>")
            file.write("</tr>")
            file.write("</table>")
            file.write("<br>")

            if duplcated_catalystids_older != []:
                file.write("<table border=1 >")
                file.write("<tr>")
                file.write(
                    "<th> # Duplicated Catalyst id's in  <font color='red'>" + file_name_1 + "</font> version </th>")
                file.write("<th> Sample Catalyst id's </th>")
                file.write("</tr>")
                file.write("<td>" + str(len(duplcated_catalystids_older)) + "</td>")
                file.write("<td>" + str(duplcated_catalystids_older) + "</td>")
                file.write("</tr>")
                file.write("</table>")
                file.write("<br>")

            if duplcated_catalystids_latest != []:
                file.write("<table border=1 >")
                file.write("<tr>")
                file.write(
                    "<th> # Duplicated Catalyst id's in  <font color='red'>" + file_name_2 + "</font> version </th>")
                file.write("<th> Sample Catalyst id's </th>")
                file.write("</tr>")
                file.write("<td>" + str(len(duplcated_catalystids_latest)) + "</td>")
                file.write("<td>" + str(duplcated_catalystids_latest) + "</td>")
                file.write("</tr>")
                file.write("</table>")
                file.write("<br>")

            file.write("<br>")
            file.write(
                "<b> Data mismatch between  <font color='red'>" + file_name_1 + "</font> and <font color='red'>" + file_name_2 + "</font> version<b>")
            file.write("<br>")
            file.write("<br>")
            file.write("<b> # No.of mismatch records = " + str(tota_diff) + "<b>")
            file.write("<br>")
            file.write("<br>")
            file.write("<br>")
            file.write("<table border=1 >")
            file.write("<tr>")
            file.write(
                "<th> # No.of Columns </th>")
            file.write("<th> No columns in <font color='red'> Impacted </font> </th>")
            file.write("<th> Column Names </th>")
            file.write("</tr>")
            file.write("<td>" + str(total_no_columns) + "</td>")
            if len(col_names_has_difference) == 0:
                len_col_names_has_difference = "None"
            else:
                len_col_names_has_difference = len(col_names_has_difference)

            file.write("<td>" + str(len_col_names_has_difference) + "</td>")
            file.write("<td>" + str(col_names_has_difference) + "</td>")
            file.write("</tr>")
            file.write("</table>")
            file.write("<br>")

            file.write("<center><b>IMPACTED ATTRIBUTES DETAILS<b></center>")
            file.write("<br>")
            file.write("<table border=1 >")
            file.write("<tr>")
            file.write("<th>  Attributes </th>")
            file.write("<th>  # Total Records Impacted </th>")
            file.write("<th> Top 2 Records </th>")
            file.write("</tr>")

            for column, html in list_tables.items():
                file.write("<tr>")
                file.write("<td><b>" + column + "</b></td>")
                file.write("<td><b>" + str(list_col_mist[column]) + "</b></td>")
                file.write("<td>" + str(html).replace('<table ', '<table border=1  ').replace('<th',
                                                                                              '<th bgcolor=#f18973 ') + "</td>")
                file.write("</tr>")

            file.write("</table>")

            file.write("</body>")
            file.write("</html>")
            file.flush()
            file.close()

        if is_excel_output == "yes":
            with pd.ExcelWriter(path_file("results", file_output_path), engine='openpyxl', mode='a') as writer:
                 for list_values in list_excel_results:
                    print(list_values)
                    for k, va in list_values.items():
                            #df_final = df_final.reset_index(drop=True)
                            df_final = pd.DataFrame(va).reset_index(drop=True)
                            df_final.to_excel(writer, sheet_name=k)
            writer.save()
            writer.close()

    except Exception as e:
        print("Error in Main = " + str(e))


def print_difference_two_df(df1, df2, column_name, file_output_path, is_excel_output):
    list_va = []
    dic_result = {}

    df2[column_name + "out"] = np.where(df1[column_name] == df2[column_name], 'True', 'False')

    result = df2[['skcatalystid', column_name, column_name + "out"]]

    result = result.apply(lambda row: row[result[column_name + "out"].isin(['False'])])
    total_rows_affected = len(result)

    # if is_excel_output == "yes":
    #     if total_rows_affected == 0:
    #         print("end***")
    #         return total_rows_affected, "MATCHED", list_va
    # else:
    if total_rows_affected == 0:
        return total_rows_affected, "MATCHED", list_va,dic_result
        # else:
        #     if len(result) > 2:
        #         result = result.head(2)

    result = result['skcatalystid']
    # print(result)

    list_va = result.values.tolist()

    df1 = df1.loc[df1['skcatalystid'].isin(list_va)][
        ['skcatalystid', 'skbrand', 'sktritonid', 'sktravelinkid', column_name]]
    df2 = df2.loc[df2['skcatalystid'].isin(list_va)][
        ['skcatalystid', 'skbrand', 'sktritonid', 'sktravelinkid', column_name]]

    df_all = pd.concat([df1, df2], axis='columns', keys=["File1", "File2"]
                       ).drop_duplicates(keep=False)
    df_final = df_all.swaplevel(axis='columns')[df1.columns]


    # this line is for excel
    dic_result[column_name] = df_final.to_dict()

    df_final = df_final.head(2)

    result_final = df_final.style.apply(highlight_diff, axis=None).hide_index().render()
    print("***************************************done")

    return total_rows_affected, result_final, list_va, dic_result


def filter_extra_catalystids_latest_version(sorted_latest_fil_data, sorted_older_fil_data):
    # Check the catalysit id in older version should exists in latest version
    catalyst_id_not_in_olderv = pd.Series(
        sorted_latest_fil_data.skcatalystid.isin(sorted_older_fil_data.skcatalystid).values.astype(int),
        sorted_latest_fil_data.skcatalystid.values)

    # Filter the extra  catalyst id in latest version
    li_not_cat = []
    for key, value in catalyst_id_not_in_olderv.items():
        if value == 0:
            li_not_cat.append(key)

    # print("Extra columns in latest-----")
    # print(li_not_cat)
    return li_not_cat


def filter_extra_catalyst_ids_older_version(sorted_latest_fil_data, sorted_older_fil_data):
    # Check the catalysit id in older version should exists in latest version
    catalyst_id_not_in_latest = pd.Series(
        sorted_older_fil_data.skcatalystid.isin(sorted_latest_fil_data.skcatalystid).values.astype(int),
        sorted_older_fil_data.skcatalystid.values)
    # print(catalyst_id_not_in_latest)
    # Filter the extra  catalyst id in older version
    li_not_ca_older = []
    for key, value in catalyst_id_not_in_latest.items():
        if value == 0:
            li_not_ca_older.append(key)

    # list(set(duplicate)
    return li_not_ca_older


def highlight_diff(data, color='yellow'):
    try:
        attr = 'background-color: {}'.format(color)
        other = data.xs("File1", axis='columns', level=-1)
        hightlighted = pd.DataFrame(np.where(data.ne(other, level=0), attr, ''),
                                    index=data.index, columns=data.columns)
        return hightlighted
    except Exception as e:
        print(str(e))
