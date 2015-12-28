import sys, shutil, os, os.path

if __name__ == '__main__':
    home = os.path.expanduser('~')
    if len(sys.argv) == 2:
        mode = sys.argv[1]
        if mode == 'comp':
            os.system('drive pull GDrive')
            shutil.rmtree(os.path.join(home, 'smart_server'))
            shutil.copytree(os.path.join(home, 'GDrive', 'smart_server'), os.path.join(home, 'smart_server'))
            print('Files copied from Google Drive to Koding')
        elif mode == 'cloud':
            shutil.rmtree(os.path.join(home, 'GDrive', 'smart_server'))
            shutil.copytree(os.path.join(home, 'smart_server'), os.path.join(home, 'GDrive', 'smart_server'))
            print('Files copied from Koding to GDrive')
            os.system('drive push GDrive')
        else:
            print('Arguments are: comp, cloud')
    else:
        print('Sync needs exactly 1 argument, ' + str(len(sys.argv) - 1) + ' supplied')
