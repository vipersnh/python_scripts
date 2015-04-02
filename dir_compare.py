import os;
import sys;
import pdb;
import subprocess;
import argparse;
import signal;
import filecmp;

exclude_file_types = [".bin", ".o", ".d", ".zip", ".xlsx", ".png", ".exe"];

parser = argparse.ArgumentParser();
parser.add_argument('-f', dest='file_mode', action="store_true");
parser.add_argument('paths', nargs='+');
parse_res = parser.parse_args();
file_mode = parse_res.file_mode;
paths = parse_res.paths;

def interrupt_handler(signum, frame):
    print ("Signal handler called with signal");
    sys.exit(0);

signal.signal(signal.SIGINT, interrupt_handler);

if not file_mode :
    try :
        assert(len(paths)==2);
        assert(os.path.isdir(paths[0]));
        assert(os.path.isdir(paths[1]));
    except :
        print("Please pass src and dest directories only for comparison \n");
        sys.exit(0);
else :
    try:
        assert(len(paths)>=2);s
    except:
        print("Please pass src files and one dest directorys only for comparison \n");
        sys.exit(0);


def valid_file(file):
    if len(file.split("."))==2:
        [a,b] = file.split(".");
        if "."+b in exclude_file_types:
            return False;
        else:
            return True;
    else:
        return True;


def get_md5sum(file):
    md5sum = subprocess.check_output(["md5sum", file]).decode("utf-8").split("\n")[0].split(" ")[0];
    return md5sum;
    
def find_files_in_path(file, path):
    full_path = subprocess.check_output(["find", path, "-name", file]);
    full_path = full_path.decode("utf-8").split("\n")[0:-1];
    if len(full_path)==1:
        return [full_path];
    else :
        return full_path;

def file_read_compare(path_1, path_2):
    l1 = l2 = ' '
    with open(path_1, 'r') as f1, open(path_2, 'r') as f2:
        while l1 != '' and l2 != '':
            l1 = f1.readline()
            l2 = f2.readline()
            if l1 != l2:
                return False
    return True

def compare_files(src_file, dest_files):
    fname = os.path.split(src_file)[-1];
    print("Checking for "+fname);
#    md5sum_src = get_md5sum(src_file);
    for dest_file in dest_files:
#        if not filecmp.cmp(src_file, dest_file):
        if not file_read_compare(src_file, dest_file):
            subprocess.check_output(["gvim", "-d", src_file, dest_file]);
#        md5sum_dest = get_md5sum(dest_file);
#        if md5sum_src!=md5sum_dest:
#            print("Files mismatch for : "+fname);
#            subprocess.check_output(["gvim", "-d", src_file, dest_file]);
#        return;

if not file_mode:
    src_dir = paths[0];
    dest_dir = paths[1];
    
    for root, _, files in os.walk(src_dir):
        filename = "";
        for fname in files:
            if valid_file(fname):
                src_file_path  = root+os.sep+fname;
                dest_file_path = src_file_path.replace(src_dir, dest_dir, 1); 
                if os.path.isfile(dest_file_path):
                    compare_files(src_file_path, [dest_file_path]);
            else:
                print("Excluding file "+fname);
    
else:
    src_paths = paths[:-1];
    dest_path = paths[-1];
    for src_path in src_paths:
        if os.path.isfile(src_path):
            src_file = src_path;
            fname = os.path.split(src_path)[-1];
            dest_files = find_files_in_path(fname, dest_path);
            compare_files(src_file, dest_files);
        else:
            print("TODO: Handle folder in src");


