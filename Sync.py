import os
import shutil
import sys
# inputs: file path from computer and phone, syncdirection
# - Establish the common folder
# E.g.
# Desktop: D:\Music\Merge
# Laptop:  C:\Users\Alfred\Music\Merge
##
# -walk master folder and store in list os.walk
# -create ignore list for album_art
# -walk target folder and store in list2
# -Compare both list
# -if item not in list2, copy item to list2 (copy)
# -if item in list2 but not in list1, delete item in list2. (delete)
# -if item in list2, and also in list1, compare size. os.path.getsize(path)
# -print out items to be deleted
# -prompt to delete


##########
# Currently appending filenames with full path to list
# What if subfolder is missing?!
# os.walk in sync_to and write to txt file
# Subfolder list not comparing. Creates folder regardless. When os.makedir, string format is good
# change: delete: sync_to files must not be altered.

def sync(sync_from, sync_to):
    ls_diff = []
    ls_same_size = []
    filter_ls = filterlist()
    # Start of file list
    ls_from = []
    ls_from_sub = []
    # sync_from
    for folderName, subfolders, filenames in os.walk(sync_from):
        for item in filenames:
            ls_from.append(folderName[len(sync_from) + 1:] + '\\' + item)
        for sub in subfolders:
            ls_from_sub.append(folderName[len(sync_from):] + '\\' + sub)
    # sync_to
    ls_to = []
    ls_to_sub = []
    ls_to_add = []
    for folderName, subfolders, filenames in os.walk(sync_to):
        for item in filenames:
            ls_to.append(folderName[len(sync_to) + 1:] + '\\' + item)
        for sub in subfolders:
            # May be a problem if no subfolder
            ls_to_sub.append(folderName[len(sync_to):] + '\\' + sub)
    # End of list
    # Create subfolder in sync_to if not there
    for sub in ls_from_sub:
        if sub not in ls_to_sub:
            path_string = sync_to + sub
            # shutil.copy(sync_from + '\\' + sub, sync_to) #shutil.copy
            print('Folder to add: ' + path_string)
            if choice() == 'Y':
                os.makedirs(path_string)
                print('Added folder: ' + path_string)
    for file in ls_from:
        if file not in ls_to:  # Add file to sync_to
            i = 0
            rev_file_path = file[::-1]  # rev file path to extract file name
            # Was rev_file_path[rev_file_path.find('.')+1:rev_file_path.find('\\')][::-1]
            file_name = rev_file_path[:rev_file_path.find('\\')][::-1]
            while i < len(filter_ls):  # Scan file though filter list
                if filter_ls[i] in file_name:
                    i = len(filter_ls) + 1
                else:
                    i += 1
            if i == len(filter_ls):  # Completed filtering, copying file...
                ls_to_add.append(file)
                print('To add: ' + file)
    if len(ls_to_add) > 0:
        if choice() == 'Y':
            for item in ls_to_add:
                shutil.copy(sync_from + '\\' + item,
                            sync_to + '\\' + item)
                print('Added: ' + sync_to + '\\' + item)
        elif file in ls_to:  # Same File, Check for Size
            sync_from_path = sync_from + '\\' + file
            sync_to_path = sync_to + '\\' + file
            size_diff = os.path.getsize(
                sync_from_path) - os.path.getsize(sync_to_path)  # Check Size
            if size_diff > 0:  # From is bigger
                print(sync_from_path + ' is bigger by: ' + str(size_diff))
                print(sync_to_path + ' will be deleted.')
                if(choice() == 'Y'):
                    os.remove(sync_to_path)
                    shutil.copy(sync_from_path, sync_to_path)
                    print('removed: ' + sync_to_path)
                    print('added: ' + sync_from_path)
            elif size_diff < 0:  # To is bigger
                print(sync_to_path + ' is bigger by: ' + str(abs(size_diff)))
                print(sync_from_path + ' will be deleted.')
                if(choice() == 'Y'):
                    os.remove(sync_from_path)
                    shutil.copy(sync_to_path, sync_from_path)
                    print('Removed: ' + sync_from_path)
                    print('Added: ' + sync_to_path)
    ls_to_delete = []
    for file in ls_to:  # Delete file in sync_to
        if file not in ls_from:
            ls_to_delete.append(file)
            print('To delete: ' + sync_to + '\\' + file)
    if len(ls_to_delete) > 0:
        if choice() == 'Y':
            for item in ls_to_delete:
                delete_file_path = sync_to + '\\' + item
                os.remove(delete_file_path)
                print('Removed: ' + delete_file_path)
            # Delete empty subfolder in sync_to if its there
        for sub in ls_to_sub:
            if sub not in ls_from_sub:
                sub_path = sync_to + sub
                print('Folder to delete: ' + sub_path)
                if choice() == 'Y':
                    os.rmdir(sync_to + sub)
                    print('Deleted folder: ' + sub_path)


def syncfromtxt(sync_from, sync_to, folder_change):  # Sync from txt####
    ls_add = []
    ls_from = []
    ls_delete = []
    filter_ls = filterlist()
    open_file = open(sync_to, encoding="utf8")
    ls_to = open_file.readlines()  # read sync_to txt file
    for folderName, subfolders, filenames in os.walk(sync_from):
        for item in filenames:  # Append to ls_from #add filer list here
            ls_from.append(
                folderName[len(sync_from) + 1:] + '\\' + item + '\n')
    for file in ls_from:
        if file not in ls_to:
            i = 0
            rev_file_path = file[::-1]  # rev file path to extract file name
            file_name = rev_file_path[:rev_file_path.find('\\')][::-1]
            while i < len(filter_ls):  # Scan file though filter list
                if filter_ls[i] in file_name:
                    i = len(filter_ls) + 1
                else:
                    i += 1
            if i == len(filter_ls):  # Completed filtering, copying file...
                ls_add.append(file)
    # Delete file
    for item in ls_to:
        if item not in ls_from:
            ls_delete.append(item)
    if len(ls_add) > 0 or len(ls_delete) > 0:  # Make folder if any changes
        new_folder_path = folder_change + 'folder_change'  # new_folder path
        os.makedirs(new_folder_path)  # Create folder_change folder
        print(new_folder_path + ' created')
        if len(ls_delete) > 0:
            # Create to_delete.txt
            path = '\\'.join([new_folder_path, '\\' + 'to_delete.txt'])
            print(path + ' created in ' + new_folder_path)
            # open new file in write
            new_file = open(path, "w", encoding="utf8")
            for item in ls_delete:
                new_file.write(item)
            new_file.close()
        if len(ls_add) > 0: # Add files
            # ls_to_add = [] #tag1
            path_add_txt = '\\'.join(
                [new_folder_path, '\\' + 'to_add.txt'])  # Create to_add.txt
            print(path_add_txt + ' created in ' + new_folder_path)
            # open new file in write
            new_file = open(path_add_txt, "w", encoding="utf8")
            for item in ls_add:
                new_file.write(item)
            new_file.close()
            add_path = new_folder_path + '\\' + 'to_add' # Create to_add folder
            os.makedirs(add_path)
            print(add_path + ' created')
            # ls_to_add.append(sync_from + '\\' +
            #                 item[:item.find('\n')], add_path) #tag1
            ls_playlist = []# for below
            for item in ls_add: #Need to create subfolder as well
            #Create Subfolder
                i=0
                first_count = item.count('\\')
                ls_temp = []
                string = ''
                while i < first_count:
                    if i > 0:
                        ls_temp.append(item[:item.find('\\')])
                        item = item[item.find('\\')+1:]
                        i += 1
                    elif i == 0:
                            playlist_path = item[:item.find('\\')] ##SEEMS LIKE IT IS TAKING THE FIRST ONE AND JOIN THE SECONDARY SUBFOLDER
                            if playlist_path not in ls_playlist:
                                ls_playlist.append(playlist_path)
                            ls_temp.append(playlist_path)
                            item = item[item.find('\\')+1:]
                            i +=1
                if first_count > 1:
                    for item in ls_temp:
                        string += item + '\\'
                    if string not in ls_playlist:
                        ls_playlist.append(string)


            print(str(ls_playlist)) ### Failed to add to list
            for item in ls_playlist:
                # print(item)
                os.makedirs(new_folder_path + '\\to_add\\' + item)

            for item in ls_add: #Add item to sub folders
                rev_file_path = item[::-1]
                filename = rev_file_path[rev_file_path.find('.')+1:rev_file_path.find('\\')][::-1]
                sync_to_path = add_path + '\\' + item[:item.find(filename)]
                shutil.copy(sync_from + '\\' +
                            item[:item.find('\n')], sync_to_path) # change add_path to include subfolder as well
                print('Added: ' + sync_to_path + '\\' + item[:item.find('\n')])
    print('Completed.')
#### Move files and delete from txt
def change(change_folder_path, sync_to): #not working yet. waiting for subfolder
    ##Need to add if to_add or to_delete is not generated
    #Path
    to_add_folder_path = change_folder_path + '\\to_add'
    to_add_txt = change_folder_path + '\\to_add.txt'
    to_delete_txt = change_folder_path + '\\to_delete.txt'
    #list
    ls_delete = []
    ls_to_delete = []
    ls_add = []
    ls_to_add = []
    ls_to_sub = []
    ls_to_sub_2 = []
    for folderName, subfolders, filenames in os.walk(sync_to):
        for sub in subfolders:
            ls_to_sub.append(folderName[len(sync_to):] + '\\' + sub) #Make it the same as to_add playlist
    for sub in ls_to_sub:
        rev_sub = sub[::-1]
        ls_to_sub_2.append(rev_sub[:rev_sub.find('\\')][::-1])
    #open to delete
    try:
        open_file_delete = open(to_delete_txt, encoding="utf8")
    except IOError:
        print('Not found: ' + to_delete_txt)
    #readlines for delete
    ls_delete = open_file_delete.readlines()  # read sync_to txt file
    if len(ls_delete) > 0:
        for item in ls_delete:
            file_path_delete = sync_to + '\\' + item[:item.find('\n')]
            print('To delete: ' + file_path_delete)
        if choice() == 'Y':
            for item in ls_delete:
                file_path_delete = sync_to + '\\' + item[:item.find('\n')]
                os.remove(file_path_delete)
                print('Removed: ' + file_path_delete)
    ######## Need to test delete as well as delete subfolder as well
    open_file_delete.close()
    #open to add
    try:
        open_file_add = open(to_add_txt, encoding="utf8")
        ls_add = open_file_add.readlines()
    except IOError:
        print('Not found: ' + to_add_txt)
    # start for ls_to_add_sub
    ls_playlist = []
    for item in ls_add: #Need to create subfolder as well
    #Create Subfolder
        i=0
        first_count = item.count('\\')
        ls_temp = []
        string = ''
        while i < first_count:
            if i > 0:
                ls_temp.append(item[:item.find('\\')])
                item = item[item.find('\\')+1:]
                i += 1
            elif i == 0:
                    playlist_path = item[:item.find('\\')] ##SEEMS LIKE IT IS TAKING THE FIRST ONE AND JOIN THE SECONDARY SUBFOLDER
                    if playlist_path not in ls_playlist:
                        ls_playlist.append(playlist_path)
                    ls_temp.append(playlist_path)
                    item = item[item.find('\\')+1:]
                    i +=1
        if first_count > 1:
            for item in ls_temp:
                string += item + '\\'
            if string not in ls_playlist:
                ls_playlist.append(string)
    print('ls_playlist is: ' + str(ls_playlist)) #playlist from to_add.txt
    print('ls_to_sub is: ' + str(ls_to_sub)) #playlist currently in sync_to ##### Not working
    for item in ls_to_sub:
        print(item)
    for sub in ls_playlist:
        # # print(item)
        # os.makedirs(new_folder_path + '\\sync_to\\' + item) # end of ls_add_to_sub
            # Create subfolder in sync_to if not there ###Need to test again
        path_string = '\\' + sub
        if path_string.endswith('\\'): #remove '\\' if ends with '\\'
            path_string = path_string[:-1]
        print('path_string is:' + path_string)
        if path_string not in ls_to_sub:
            # path_string = sync_to + '\\' + sub
            # shutil.copy(sync_from + '\\' + sub, sync_to) #shutil.copy
            new_path_string = sync_to + path_string
            print('Folder to add: ' + new_path_string)
            if choice() == 'Y':
                os.makedirs(new_path_string)
                print('Added folder: ' + new_path_string)
    if len(ls_add) > 0:
        ls_to = []
        ls_from = []
        for item in ls_add:
            file_path_add_from = to_add_folder_path + '\\' + item[:item.find('\n')]
            file_path_add_to = sync_to + '\\' + item[:item.find('\n')]
            ls_from.append(file_path_add_from)
            ls_to.append(file_path_add_to)
            print('To add: ' + file_path_add_to)
        if choice() == 'Y':
            i = 0
            while i < len(ls_from):
                shutil.copy(ls_from[i], ls_to[i]) ##Awaiting adding of subfolder function
                print('Added: ' + ls_to[i])
                i += 1





def walkfoldertxt(file_path):
    path = '\\'.join([file_path, 'sync.txt'])  # new file path
    new_file = open(path, "w", encoding="utf8")  # open new file in write
    for folderName, subfolders, filenames in os.walk(file_path):
        for item in filenames:
            if item != 'sync.txt':
                new_file.write(
                    folderName[len(file_path) + 1:] + '\\' + item + '\n')
    new_file.close()
    print(path + ' created')


def choice():
    print("Make changes? Y or N:")
    reply = input().upper()
    if reply == 'Y' or reply == 'N':
        return reply
    else:
        print('Invalid Input!')


def filterlist():
    filter_ls = ['AlbumArt', 'Folder']
    return filter_ls

###GUI & Test Zone###
# test walkfolder again
##ls_add = []
##ls_from = []
##ls_delete = []
##open_file = open(r'D:\test_to\sync.txt', encoding="utf8")
# ls_to = open_file.readlines() #read sync_to txt file
# for folderName, subfolders, filenames in os.walk(r'D:\test_from'):
# for item in filenames: # Append to ls_from
##            ls_from.append(folderName[len(r'D:\test_from')+1:] + '\\' + item + '\n')
# for item in ls_from:
# if item not in ls_to:
# print(item)
# for item in ls_to:
# if item not in ls_from:
# print(item)


## test       sync
sync_from = r'D:\Music\ASMR'
sync_to = r'A:\Music\ASMR'
sync(sync_from, sync_to)

##sync_from = r'D:\test_from'
##sync_to = r'D:\test_to'
##sync(sync_from, sync_to)


# Test   syncfromtxt
# sync_from = r'D:\test_from'
# sync_to = r'D:\sync.txt'
# folder_change = 'D:\\'
# syncfromtxt(sync_from, sync_to, folder_change)

# Test   walkfoldertxt
# file_path = r'D:\test_to'
# walkfoldertxt(file_path)

##for folderName, subfolders, filenames in os.walk(r'This PC\Galaxy Note9\Phone\Music\Merge'):
##    print('The folder is ' + folderName)
##    print('The subfolders in ' + folderName + ' are: ' + str(subfolders))
##    print('The filenames in ' + folderName + ' are' + str(subfolders))

#Test Change
# change_folder_path = r'D:\folder_change'
# sync_to = r'D:\test_to'
# change(change_folder_path, sync_to)

#####Testing subfolder for txt
# ls = []
# string = r"Soundtrack\Significance - Nothing - J'Nique Nicole.m4a"
# i=0
# first_count = string.count('\\')
# while i < first_count:
#     if i > 0:
#         if i < first_count:
#                 ls.append(ls[i-1] + '\\' + string[:string.find('\\')])
#                 string = string[string.find('\\')+1:]
#                 i += 1
#     elif i == 0:
#             ls.append(string[:string.find('\\')])
#             string = string[string.find('\\')+1:]
#             i +=1

# if i == 0:
#         ls.append(string[:string.find('\\')])
#         string = string[string.find('\\')+1:]
#         i += 1
# elif i > 0:
#     if i < string.count('\\'):
#             ls.append(ls[i-1] + '\\' + string[:string.find('\\')])
#             string = string[string.find('\\')+1:]
#             i += 1

#This Ensure no duplicate item in list
# i = 0
# for item in ls:
#     if i == 0:
#          print(item)
#          i += 1
#     elif i < len(ls)+1:
#         if item != ls[:i]:
#             print(item)
#             i += 1

##Test sub
# for item in ls_playlist: #Create subfolders #####
#                 if x == 0:
#                      #os.makedirs(new_folder_path + '\\' + item)
#                     x += 1
#                     print(item)
#                 elif x < len(ls_playlist)+1:
#                     if item not in ls_playlist[:x]:
#                         print(item)
#                         # os.makedirs(new_folder_path + '\\' + item)
#                         x += 1
