import sys
import file_compare as fic
import folder_compare as foc
from config_parser import CustomConfigParser as cp
import pytest
import datetime
import os
import logging

lhs_local_path = ""
rhs_local_path = ""
env = ""
env_1 = ""
is_excel_output_needed = ""

#def load_config(config):
    
#    return 
    
    
# Fetch the path of the given file
def path_file(folder, file_name):
    try:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', folder, file_name))
    except Exception as exception_message:
        raise ValueError(str(exception_message))

@pytest.mark.file_comparision
def test_compare_files():
    # read config file
    config_parsed = cp.config_parser('../config.ini')
    print (config_parsed)
    
    lhs_local_path = config_parsed.get('lhs_local_path')
    rhs_local_path = config_parsed.get('rhs_local_path')
    env = config_parsed.get('legacy_env')
    env_1 = config_parsed.get('new_env')
    is_excel_output_needed = config_parsed.get('enable_excel_output')

    # is_excel_ouput_needed = "no"
    # is_excel_ouput_needed = "yes"
    print("1")
    logging.info("test")
    print("2")
    
    # folder paths
    lhs_folder_path = lhs_local_path
    rhs_folder_path = rhs_local_path
    print(lhs_folder_path)
    print(rhs_folder_path)

    # to list down the common files between lhs & rhs folder paths (with .csv or .xls or .xlsx format)
    #common_files = foc.list_common_file_names(lhs_folder_path,rhs_folder_path)

    lhs_files = foc.read_file_names(lhs_folder_path)
    rhs_files = foc.read_file_names(rhs_folder_path)
    # To find the common files between the LHS and RHS folders
    common_files = list(set(lhs_files).intersection(rhs_files))

    print (common_files)

    lhs_alone_files = set(lhs_files).difference(set(rhs_files))
    print(lhs_alone_files)
    rhs_alone_files = set(rhs_files).difference(set(lhs_files))
    print(rhs_alone_files)

    dt = datetime.datetime.now()
    formatted_dt = "Overall_Comparision_Summary_" + dt.strftime("%Y")+dt.strftime("%m")+dt.strftime("%d")+"_"+dt.strftime("%H")+"_"+dt.strftime("%M")+"_"+dt.strftime("%S")+".html"
    print (formatted_dt)

    with open(path_file("results", formatted_dt), 'w') as file:
        file.write("<html>")
        file.write("<body>")
        file.write("<table border=1 >")
        file.write("<tr>")
        file.write("<th> File_path 1</th>")
        file.write("<th> File_path 2 </th>")
        file.write("<th> Result </th>")
        file.write("</tr>")

        if(common_files !=[]):
            for filex in common_files:
                print (filex)
                lhs_file_name = str(lhs_folder_path) + str(filex)
                print (lhs_file_name)
                rhs_file_name = str(rhs_folder_path) + str(filex)
                print(rhs_file_name)
                file.write("<tr>")
                file.write("<td>" + lhs_file_name + "</td>")
                file.write("<td>" + rhs_file_name + "</td>")
                result_msg = fic.validate_csv(lhs_file_name, rhs_file_name, env, env_1, is_excel_output_needed)

                file.write("<td>" + result_msg  + "</td>")
                file.write("</tr>")

        file.write("</table>")
        file.write("<br>")
        file.write("<table border=1 >")
        file.write("<tr>")
        file.write("<th> File_details</th>")
        file.write("<th> Result </th>")
        file.write("</tr>")

        if (lhs_alone_files != []):
            for filex in lhs_alone_files:
                print(filex)
                lhs_file_name = str(lhs_folder_path) + str(filex)
                print(lhs_file_name)
                file.write("<tr>")
                file.write("<td>" + lhs_file_name + "</td>")
                result_msg = "No match record on the RHS"

                file.write("<td>" + result_msg + "</td>")
                file.write("</tr>")

        file.write("</table>")
        file.write("<br>")

        file.write("<table border=1 >")
        file.write("<tr>")
        file.write("<th> File_details</th>")
        file.write("<th> Result </th>")
        file.write("</tr>")

        if (rhs_alone_files != []):
            for filex in rhs_alone_files:
                print(filex)
                rhs_file_name = str(rhs_folder_path) + str(filex)
                print(rhs_file_name)
                file.write("<tr>")
                file.write("<td>" + rhs_file_name + "</td>")
                result_msg = "No match record on the LHS"

                file.write("<td>" + result_msg + "</td>")
                file.write("</tr>")

        file.write("</table>")

        file.write("</body>")
        file.write("</html>")
        file.flush()
        file.close()



    #lhs_file_name = "C:\\LHS\\780aa013-a449-4be1-9d7c-be7df37dd027.csv"
    #rhs_file_name = "C:\\RHS\\780aa013-a449-4be1-9d7c-be7df37dd027.csv"

    #fic.validate_csv(lhs_file_name, rhs_file_name, env, env_1, is_excel_ouput_needed)
    #tc.validate_csv(file_name_1, file_name_2, is_excel_ouput_needed)



