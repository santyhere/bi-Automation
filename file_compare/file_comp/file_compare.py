
import pandas as pd
import numpy as np
from time import strftime
import os
import openpyxl
from pathlib import Path
#import logging

encoding = 'unicode_escape'

out_diff = []
file_name_1 = ""
file_name_2 = ""

is_file_created = False

# logging.basicConfig(filename='logs.log',
#             filemode='w',
#             level=logging.DEBUG)

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
def validate_csv(file_name_1, file_name_2, env, env_1, is_excel_output):
    try:
        ##print(file_name_1)
        ##print(file_name_2)
        ##print(env)
        ##print(env_1)
        ##print(is_excel_output)
        print("1")
#        logging.info("test")
        
        validate_result = "Match"
        global tota_diff
        tota_diff = 0
        global total_no_columns
        total_no_columns = ''
        global col_names_has_difference
        col_names_has_difference = []

        file_name_v1 = file_name_1
        file_name_v2 = file_name_2

        print("LHS----------->")
        # Read the file 1 csv file
        older_version_file = pd.read_csv(file_name_v1)
        print(older_version_file)
        #older_version_file = older_version_file.drop(['lastmodified'], axis=1)
        # created_by', 'batch_id', 'created_dt

        print("RHS----------->")
        # Read the file 2 csv file
        latest_version_file = pd.read_csv(file_name_v2)
        print(latest_version_file)

        #latest_version_file = latest_version_file.drop(['lastmodified'], axis=1)

        file_name_1 = split_version_file(file_name_v1)
        file_name_2 = split_version_file(file_name_v2)

        ##print(file_name_1)
        ##print(file_name_2)

        # Sort the values by the catalystid
        ##sorted_older_fil_data = older_version_file.sort_values(by=[primary_key], ascending=False)
        print("Sort LHS file ------------------>")
        older_version_file_columns = np.sort(older_version_file.columns.tolist())
        print(older_version_file_columns)
        # Sort the values by row
        sorted_older_fil_data_rowsort = older_version_file.sort_values(by=older_version_file_columns.tolist(),ascending=True)
        # Reorder / sort the orders
        sorted_older_fil_data = sorted_older_fil_data_rowsort.reindex(columns=older_version_file_columns)
        row_older = len(sorted_older_fil_data)
        print(sorted_older_fil_data_rowsort)
        print(sorted_older_fil_data)

        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

        print("Sort RHS file ------------------>")
        latest_version_file_columns = np.sort(latest_version_file.columns.tolist())
        ##sorted_latest_fil_data = latest_version_file.sort_values(by=[primary_key], ascending=False)
        sorted_latest_fil_data_rowsort = latest_version_file.sort_values(by=latest_version_file.columns.tolist(),ascending=True)
        sorted_latest_fil_data = sorted_latest_fil_data_rowsort.reindex(columns=latest_version_file_columns)
        print(sorted_latest_fil_data_rowsort)
        print(sorted_latest_fil_data)
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
                print(columns_xtra_latest)

                # Remove the xtra columnscolumns
                sorted_latest_fil_data = sorted_latest_fil_data.drop(columns=columns_xtra_latest, axis=1)

                # else:
                no_xtra_older = len(columns_difference_older)
                columns_xtra_older = columns_difference_older

                # Remove the xtra columns
                sorted_older_fil_data = sorted_older_fil_data.drop(columns=columns_xtra_older, axis=1)
                validate_result = "Column mismatch"
                print("1")
                print(sorted_older_fil_data)
            elif columns_difference_latest != []:
                no_xtra_latest = len(columns_difference_latest)
                columns_xtra_latest = columns_difference_latest
                print(columns_xtra_latest)

                # Remove the xtra columnscolumns
                sorted_latest_fil_data = sorted_latest_fil_data.drop(columns=columns_xtra_latest, axis=1)
                validate_result = "Column mismatch"
                print("2")
                print(sorted_latest_fil_data)
            else:
                no_xtra_older = len(columns_difference_older)
                columns_xtra_older = columns_difference_older

                # Remove the xtra columns
                sorted_older_fil_data = sorted_older_fil_data.drop(columns=columns_xtra_older, axis=1)
                validate_result = "Column mismatch"
                print("3")
                print(sorted_older_fil_data)

        print(len(sorted_latest_fil_data.columns))
        print(len(sorted_older_fil_data.columns))

        print(len(sorted_latest_fil_data))
        print(len(sorted_older_fil_data))

        duplcated_catalystids_older = []
        duplcated_catalystids_latest = []
        ##boolean = sorted_older_fil_data.duplicated(subset=[primary_key]).any()
        boolean = sorted_older_fil_data.duplicated().any()
        print("Check for duplicates")
        print(boolean)
        dup_left_df = []
        if boolean == True:
            ##older_df = sorted_older_fil_data[sorted_older_fil_data[primary_key].duplicated() == True]
            dup_left_df = sorted_older_fil_data[sorted_older_fil_data.duplicated() == True]
            print("duplicates---->")
            print(dup_left_df)

            ##sorted_older_fil_data = sorted_older_fil_data.drop_duplicates(subset=[primary_key], keep='first')
            sorted_older_fil_data = sorted_older_fil_data.drop_duplicates(keep='first')
            print(sorted_older_fil_data)

        boolean1 = sorted_latest_fil_data.duplicated().any()
        dup_right_df = []
        if boolean1 == True:
            dup_right_df = sorted_latest_fil_data[sorted_latest_fil_data.duplicated() == True]
            print("duplicates---->")
            print(dup_right_df)
            #duplcated_catalystids_latest = list(set(latest_df.tolist()))
            sorted_latest_fil_data = sorted_latest_fil_data.drop_duplicates(keep='first')
            print(sorted_older_fil_data)

        # find the xtra catalyst ids in  and remove it
        ##catalyst_ids_xtra_older = filter_extra_catalyst_ids_older_version(sorted_latest_fil_data, sorted_older_fil_data)
        ##print(catalyst_ids_xtra_older)

        # Flter the extra catalyst id in latest version
        ##catalyst_ids_xtra_latest = filter_extra_catalystids_latest_version(sorted_latest_fil_data,                                                                            sorted_older_fil_data)
        ##print(catalyst_ids_xtra_latest)

        # not_existing_catal_id_older = []
        # if catalyst_ids_xtra_older != []:
        #     # Extra catalyst id in older version
        #     not_existing_catal_id_older = catalyst_ids_xtra_older
        #
        #     # Removing the extra catalyst id in older version
        #     sorted_older_fil_data = sorted_older_fil_data[
        #         ~(sorted_older_fil_data[primary_key].isin(not_existing_catal_id_older))]
        #
        # not_existing_catal_id_latest = []
        # if catalyst_ids_xtra_latest != []:
        #     # Extra catalyst id in latest version
        #     not_existing_catal_id_latest = catalyst_ids_xtra_latest
        #
        #     # Removing the extra catalyst id in latest version
        #     sorted_latest_fil_data = sorted_latest_fil_data[
        #         ~(sorted_latest_fil_data[primary_key].isin(not_existing_catal_id_latest))]

        # remove dupl
        print(len(sorted_latest_fil_data))
        print(len(sorted_older_fil_data))
        print("Sort and duplicate removal completed")

        # columns_to_change = ['skvid', 'skholisticid', 'cmcurrentage', 'bhrevenuetotalreportingcurrency',
        #                      'bhrevenueaveragereportingcurrency', 'bhrevenuetotalallbookings',
        #                      'bhrevenueaveragevalueofextras',
        #                      'bhrevenueaverageperpax', 'bhrevenueaveragequote', 'bhrevenuetotalmargin',
        #                      'bhrevenueaveragemargin', 'bhpaxaverageonquotes', 'bhquotelastamount',
        #                      'bhcsataverage', 'bhcsatwouldrecommend', 'bhbookingstotal',
        #                      'bhbookingstotalfinancialyeartodate', 'bhbookingstotalfinancialyear2',
        #                      'bhbookingsaverageleadtime', 'bhrevenuetotallocalcurrency', 'papropensitybucket',
        #                      'patimebucket', 'bhrevenueaveragediscount', 'papropensity',
        #                      'bhrevenueaveragelocalcurrency', 'bhrevenuetotalyear2',
        #                      'bbvisitscountpast30days', 'bbvisitscountpast365days', 'pacustomerrank',
        #                      'bhpaxaveragenumber',
        #                      'bhpaxminageonanybooking', 'bhpaxmaxageonanybooking', 'bhquotetotalnumber',
        #                      'bhquoteaveragenumbertobookings',
        #                      'bhquoteaveragetimetobooking', 'bbvisitscountpast7days', 'paquoteconversionrank',
        #                      'paquoteconversionbucket', 'paquoteconversiontimebucket', 'paquoteconversionquoteage',
        #                      'palikelyhoodinmarketrank', 'bhfeefolasttriprating']
        #
        # #round_columns = ['bhrevenueyeartodatereportingcurrency', 'bhrevenuetotalreportingcurrency',
        #                  'bhrevenueaveragelocalcurrency',
        #                  'bhrevenueaveragereportingcurrency', 'bhrevenuetotalallbookings',
        #                  'bhrevenueaveragevalueofextras', 'bhrevenueaverageperpax', 'bhrevenueaveragequote',
        #                  'bhrevenuetotalmargin', 'bhrevenueaveragemargin', 'bhpaxaverageonquotes',
        #                  'bhrevenueyeartodatelocalcurrency', 'bhrevenuetotallocalcurrency', 'bhrevenuetotalyear2',
        #                  'bhpaxaveragenumber']

        # Comparing the both version data only
        df1 = sorted_older_fil_data
        df1 = df1.astype(str)
        print("before null and case corrections")
        print (df1)

        # for colum in columns_to_change:
        #     if colum in df1.columns:
        #         df1[colum] = df1[colum].str.replace('.0', '')
        #
        # for round_col in round_columns:
        #     decimals = 2
        #     if round_col in df1.columns:
        #         df1[round_col] = pd.to_numeric(df1[round_col], downcast='float', errors='coerce').apply(
        #             lambda x: round(x, decimals))

        # df1 = df1.astype(str)
        df1 = df1.replace("nan", "\\N")
        df1 = df1.applymap(lambda x: x.lower().strip())
        print("Data1 - > after null and case corrections")
        print(df1)
        df1 = df1.reset_index(drop=True)
        # df1 = df1.head(10)
        #
        # Data 2
        df2 = sorted_latest_fil_data
        df2 = df2.astype(str)
        # for colum in columns_to_change:
        #     if colum in df2.columns:
        #         df2[colum] = df2[colum].str.replace('.0', '')
        # for round_col in round_columns:
        #     decimals = 2
        #     if round_col in df2.columns:
        #         df2[round_col] = pd.to_numeric(df2[round_col], downcast='float', errors='coerce').apply(
        #             lambda x: round(x, decimals))
        # df2 = df2.astype(str)
        df2 = df2.replace("nan", "\\N")
        df2 = df2.applymap(lambda x: x.lower().strip())
        df2 = df2.reset_index(drop=True)
        print("Data2 - > after null and case corrections")
        print(df2)
        # df2 = df2.head(10)

        list_mismatch_records = []
        list_tables = {}
        list_col_mist = {}

        col_names_has_difference = []
        total_no_columns = len(df1.columns)

        # df1 = df1.pivot_table(index=[primary_key], aggfunc='size')

        # list_excel_results = []
        # for columns in df1.columns:
        #
        #     # Compare the two files data , give the results
        #     print(columns)
        #     resuls = print_difference_two_df(df1, df2,columns)
        #     print("------compare ------------------>")
        #     print(resuls)
        #
        print("Left--------------------------------------->")
        # identify LHS extra rows
        df_left = pd.merge(df1, df2, how='left', indicator=True)

        print(df_left)
        print("Left only records count : ")
        print(df_left._merge.value_counts()['left_only'])
        Left_only_rec_count = df_left._merge.value_counts()['left_only']

        print("Right--------------------------------------->")
        # identify RHS extra rows
        df_right = pd.merge(df1, df2, how='right', indicator=True)
        print(df_right)
        print("Right only records count : ")
        print(df_right._merge.value_counts()['right_only'])
        right_only_rec_count = df_right._merge.value_counts()['right_only']

        tota_diff = Left_only_rec_count + right_only_rec_count
        print(tota_diff)

        print(
            "XXXXXXXXXXXXXOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        if (tota_diff > 0):
            print (tota_diff)
            print (validate_result)
            if validate_result != "Match":
                print("XXXXXXXXXXXXXOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                validate_result = "Col & Row mismatch"
            else:
                validate_result = "Row mismatch"

        print(validate_result)
        print(
            "XXXXXXXXXXXXXOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

        print(file_name_1)
        print(file_name_2)
        print(Path(file_name_1).name)

        file_output_path = ''
        if is_excel_output == "yes":
            if(tota_diff>0):
                # Create the excel file for push all the mismatch records
                file_output_path = "Diff_Details_for_" +Path(file_name_1).name+ "_" + strftime(
                    "%Y-%m-%d-%I_%M_%S" + ".xlsx")
                wb = openpyxl.Workbook()
                wb.save(path_file("results", file_output_path))
                wb.close()

        # list_mismatch_records.append(int(resuls[0]))
        # list_col_mist[columns] = int(resuls[0])
        #
        #     if resuls[1] != "MATCHED":
        #         col_names_has_difference.append(columns)
        #         list_tables[columns] = resuls[1]
        #
        #     if resuls[3] != {}:
        #         list_excel_results.append(resuls[3])

        print("---------------------merge LHS & RHS")

        df_left = df_left.loc[df_left['_merge'] != "both"]
        df_right = df_right.loc[df_right['_merge'] != "both"]

        # concatenating file1 & 2 in single df
        list_excel_results = pd.concat((df_left, df_right),
                             axis='columns', keys=['First', 'Second'])

        print(list_excel_results)

        #
        if columns_xtra_older == '':
            columns_xtra_older = "None"

        if columns_xtra_latest == '':
            columns_xtra_latest = "None"

        # if not_existing_catal_id_latest == []:
        #     not_existing_catal_id_latest = "None"
        #     len_not_existing_catal_id_latest = 0
        # else:
        #     len_not_existing_catal_id_latest = len(not_existing_catal_id_latest)
        #     if len_not_existing_catal_id_latest > 10:
        #         not_existing_catal_id_latest = not_existing_catal_id_latest[:10]
        #
        # if not_existing_catal_id_older == []:
        #     not_existing_catal_id_older = "None"
        #     len_not_existing_catal_id_older = 0
        # else:
        #     len_not_existing_catal_id_older = len(not_existing_catal_id_older)

        output_file_name = "Summary_for_filename_" +  Path(file_name_1).name + "_" + strftime(
            "%Y-%m-%d-%I_%M_%S" + ".html")
        print(output_file_name)

        with open(path_file("results", output_file_name), 'w') as file:
            file.write("<html>")
            # file.write("<body bgcolor='#ccfff3'>")
            file.write("<table border=1 >")
            file.write("<tr>")
            file.write("<th> Number of rows in  <font color='red'> " + env + file_name_1 + "</font> version </th>")
            file.write("<th> Number of rows in <font color='red'>" + env_1 + file_name_2 + "</font> version </th>")
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
            file.write("<th># Matching columns </th>")
            file.write("<th> Columns names </th>")
            file.write("</tr>")
            file.write("<td>" + str(total_no_columns) + "</td>")
            file.write("<td>" + str(df2.columns.to_list()) + "</td>")
            file.write("</tr>")
            file.write("</table>")
            file.write("<br>")

            file.write("<br>")
            file.write("<table border=1 >")
            file.write("<tr>")
            file.write("<th># Missing columns in  <font color='red'>" + env_1 + file_name_2 + "</font> version </th>")
            file.write("<th> Columns names </th>")
            file.write("</tr>")
            file.write("<td>" + str(no_xtra_older) + "</td>")
            file.write("<td>" + str(columns_xtra_older) + "</td>")
            file.write("</tr>")
            file.write("</table>")
            file.write("<br>")

            file.write("<table border=1 >")
            file.write("<tr>")
            file.write("<th> # Additional Columns in <font color='red'>" + env_1 + file_name_2 + "</font> version </th>")
            file.write("<th> Columns names </th>")
            file.write("</tr>")
            file.write("<td>" + str(no_xtra_latest) + "</td>")
            file.write("<td>" + str(columns_xtra_latest) + "</td>")
            file.write("</tr>")
            file.write("</table>")
            file.write("<br>")

            file.write("<center><b>ROW-WISE CHECKS<b></center>")

            file.write("<br>")
            file.write(
                "<b> Data mismatch between  <font color='red'>" + env + file_name_1 + "</font> and <font color='red'>" + env_1 + file_name_2 + "</font> version<b>")
            file.write("<br>")
            file.write("<br>")
            file.write("<b> # No.of mismatch records = " + str(tota_diff) + "<b>")
            file.write("<br>")
            file.write("<br>")
            file.write("<br>")
            file.write("<table border=1 >")
            file.write("<tr>")
            file.write("<th> # Missing records in <font color='red'>" + env_1 + file_name_2 + "</font> version </th>")
            file.write("<th> Sample record </th>")
            file.write("</tr>")
            if len(df_right[df_right["_merge"] == "right_only"]) != 0:
                file.write("<td>" + str(len(df_left[df_left["_merge"]=="left_only"])) + "</td>")
                file.write("<td>" + str(df_left[df_left["_merge"]=="left_only"].values[0]) + "</td>")
            else :
                file.write("<td>" + str(0) + "</td>")
                file.write("<td>" + "No mismatch" + "</td>")
            file.write("</tr>")
            file.write("</table>")

            file.write("<br>")

            file.write("<table border=1 >")
            file.write("<tr>")
            file.write(
                "<th> # Additional records in  <font color='red'>" +env_1+  file_name_2 + "</font> version </th>")
            file.write("<th> Sample record </th>")
            file.write("</tr>")
            if len(df_right[df_right["_merge"]=="right_only"]) != 0:
                file.write("<td>" + str(len(df_right[df_right["_merge"] == "right_only"])) + "</td>")
                file.write("<td>" + str(df_right[df_right["_merge"]=="right_only"].values[0]) + "</td>")
            else :
                file.write("<td>" + str(0) + "</td>")
                file.write("<td>" + "No mismatch" + "</td>")
            file.write("</tr>")
            file.write("</table>")
            file.write("<br>")
            print("left duplicates")
            print(dup_left_df)
            if len(dup_left_df) != 0:
                print("left")
                file.write("<table border=1 >")
                file.write("<tr>")
                file.write(
                    "<th> # Duplicated Records LHS  <font color='red'>" + env + file_name_1 + "</font> version </th>")
                file.write("<th> Sample record </th>")
                file.write("</tr>")
                file.write("<td>" + str(len(dup_left_df)) + "</td>")
                file.write("<td>" + str(dup_left_df.values[0]) + "</td>")
                file.write("</tr>")
                file.write("</table>")
                file.write("<br>")
            print("right duplicates")
            print(dup_right_df)
            if len(dup_right_df) != 0:
                print("right")
                file.write("<table border=1 >")
                file.write("<tr>")
                file.write(
                    "<th> # Duplicated Records RHS  <font color='red'>" +env_1+  file_name_2 + "</font> version </th>")
                file.write("<th> Sample Record </th>")
                file.write("</tr>")
                file.write("<td>" + str(len(dup_right_df)) + "</td>")
                file.write("<td>" + str(dup_right_df.values[0]) + "</td>")
                file.write("</tr>")
                file.write("</table>")
                file.write("<br>")


            file.write("<br>")
            file.write("<br>")
            file.write("<br>")
            file.write("</body>")
            file.write("</html>")
            file.flush()
            file.close()

        print("conclusion part->writing to excel")
        print(list_excel_results)

        if is_excel_output == "yes":
            # print("File write started")
            # if(list_excel_results)
            if tota_diff > 0:
                with pd.ExcelWriter(path_file("results", file_output_path), engine='openpyxl', mode='a') as writer:
                    list_excel_results.to_excel(writer,sheet_name="comparision_result")
                # print("file save started")
            # #writer.save()
            # print("file saved")
            # print("file close started")
            # #writer.close()
            # print("file close started")
        return validate_result

    except Exception as e:
        print("Error in Main = " + str(e))
        return "Error"

# def print_difference_two_df(df1, df2, column_name):
#     list_va = []
#     dic_result = {}
#
#     print("print diff inside --------------->")
#     print(column_name)
#     print(df1[column_name])
#     print(df2[column_name])
#     df2[column_name + "out"] = np.where(df1[column_name] == df2[column_name], 'True', 'False')
#
#     result = df2[['xxx', column_name, column_name + "out"]]
#     print(result)
#
#     result = result.apply(lambda row: row[result[column_name + "out"].isin(['False'])])
#     total_rows_affected = len(result)
#
#
#     if total_rows_affected == 0:
#         return total_rows_affected, "MATCHED", list_va,dic_result
#
#
#     result = result['xxx']
#     # print(result)
#
#     list_va = result.values.tolist()
#     print(list_va)
#
#     df1 = df1.loc[df1['skcatalystid'].isin(list_va)][
#         ['skcatalystid', 'skbrand', 'sktritonid', 'sktravelinkid', column_name]]
#     df2 = df2.loc[df2['skcatalystid'].isin(list_va)][
#         ['skcatalystid', 'skbrand', 'sktritonid', 'sktravelinkid', column_name]]
#
#     df_all = pd.concat([df1, df2], axis='columns', keys=["File1", "File2"]
#                        ).drop_duplicates(keep=False)
#     df_final = df_all.swaplevel(axis='columns')[df1.columns]
#
#
#     # this line is for excel
#     dic_result[column_name] = df_final.to_dict()
#
#     df_final = df_final.head(2)
#
#     result_final = df_final.style.apply(highlight_diff, axis=None).hide_index().render()
#     print("***************************************done")
#
#     return total_rows_affected, result_final, list_va, dic_result


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
