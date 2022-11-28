import os

# lhspath = 'C:\\LHS\\'
# rhspath = 'C:\\RHS\\'

lhs_files = []
rhs_files = []

# to list all the file names from the given folder path
def read_file_names(folder_path):
    file_names = []
    for entry in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, entry)):
            # print(entry)
            if(entry.endswith(('.csv','.xls','.xlsx'))):
                file_names.append(entry)
    print(folder_path)
    print(file_names)
    return file_names
