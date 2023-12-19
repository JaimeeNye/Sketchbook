# Copies drum files into a directory organized by drum type
import os
from shutil import copyfile
import soundfile as sf
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument(
    'drum_dir',
    help='List of directories containing folders of drums sounds.',
    type=str)

parser.add_argument(
    'export_loc', 
    help='Directory where sounds will be copied to.', 
    type=str)

args = parser.parse_args()

ORIG_DIR = args.drum_dir
COPY_DIR = args.export_loc

def make_dir(dir_str):
    if not os.path.exists(dir_str):
        os.mkdir(dir_str)

def get_files(top_dir):
    all_files = []

    for path, subdirs, files in os.walk(top_dir):
        for name in files:
            all_files.append(os.path.join(path, name))

    return all_files


def copy_file_by_str(fp, drum_d, drum_dkey, export_loc):

    is_drum_type = False

    for v in drum_d[drum_dkey][0]:
        if (not is_drum_type) & (v in fp.lower()):
            is_drum_type = True
    
    str_excludes = []
    for w in drum_d[drum_dkey][1]:
        str_excludes.extend(drum_d[w][0])

    if len(drum_d[drum_dkey]) == 3:
        str_excludes.extend(drum_d[drum_dkey][2])

    if is_drum_type:
        for u in str_excludes:
            if (is_drum_type) & (u in fp.lower()):
                is_drum_type = False

    if (is_drum_type) & ('.' in fp):
        if ('.' + fp.split('.')[-1]) not in extension_excludes:  #not sure why these aren't caught in the initial extension filter
            try:
                x, fs = sf.read(fp)
                file_length = 2.0
                if (drum_dkey == 'fills') | (drum_dkey == 'fx'):
                    file_length = 4.0
                if (len(x) / fs) <= file_length:

                    new_fn = '_'.join(fp.split('/')[-3:]).replace('/','-')
                    new_fn = new_fn.replace(' ', '_')

                    new_dir = os.path.join(export_loc, drum_dkey)
                    make_dir(new_dir)

                    new_fp = os.path.join(new_dir, new_fn)
                    copyfile(fp, new_fp)
            except:
                print('**ERROR** ', fp)

############################################

dd = {}
dd['claps'] = (['clap', 'clp'], 
                ['fills'])

dd['closed_hats'] = (['closed','_hh','/hh_','hihat','clh','closed','_chh','_hat','hats','/hat','-hat', 'c-hat'], 
                ['open_hats', 'kicks'])

dd['cowbells'] = (['cowb'],
                [])

dd['cymbals'] = (['cymb', 'cyb','ride', 'crash', 'splash'], 
                ['kicks','snares','closed_hats','open_hats'], 
                ['rider'])

dd['fills'] = (['fill', 'flam', 'roll'], 
                ['kicks'], 
                ['synth'])

dd['fx'] = (['fx'], 
                ['kicks','snares','claps','cymbals'], 
                ['drum'])

dd['hand_drums'] = (['bong','cong','timba','hc','lc','mc'], 
                ['toms', 'kicks','snares','claps','cymbals','closed_hats','open_hats',],
                ['timbaland']) #lol

dd['kicks'] = (['kick','kik', 'kck'], 
                ['toms','fills'])

dd['open_hats'] = (['open', 'opn', 'ophh', 'hatop','ophat', 'o-hat', 'ohh'], 
                [])#['closed_hats'])

dd['percussion'] = (['perc', 'prc'], 
                ['shakers', 'toms', 'cowbells', 'claps','snares','kicks','sidesticks','woodblocks'])

dd['shakers'] = (['shake', 'maraca','tamb','guiro', 'cabasa', 'cuica', 'vibra','shkr', 'shk'], 
                ['kicks','snares', 'percussion'])

dd['sidesticks'] = (['sdst', 'stick','rim', 'rsh'],
                ['snares','woodblocks'], 
                ['grim','crim'])

dd['snares'] = (['snare', 'snr'], 
                ['claps', 'snaps','fills'])

dd['snaps'] = (['snap','snp'], 
                [])

dd['subs'] = (['sub', '808'], 
                ['kicks','snares','hand_drums','closed_hats','open_hats','claps','toms', 'sidesticks','woodblocks','cymbals'], 
                ['ch','oh','tom', 'cy'])

dd['toms'] = (['tom', 'timp', 'tm'], 
                ['snares','claps','closed_hats','open_hats', 'kicks', 'percussion','hand_drums'], 
                ['custom', 'bottom'])

dd['woodblocks'] = (['wood', 'clave', 'marim'], 
                ['snares', 'sidesticks'], 
                [])


############################################

all_files = get_files(ORIG_DIR)
print('Number of total files: ', len(all_files))

extension_excludes = ['.asd', '.als', '.mid', '.ogg', '.nka', '.nki', '.nksn', 
                    '.mfxp', '.mxsnd','.mxgrp', '.fxp', '.undo','.DS_Store', 
                    '.jpg', '.pdf', '.mp4', '.PAT', '.txt', '.rtf', '.json', 
                    '.tif', '.cfg', 'frm']

files_good_ext = []

for f in all_files:
    f_formatted = f.replace('\'','x').replace(" ", "x").lower()
    file_good = True
    ee_ind = 0

    while (file_good) & (ee_ind < len(extension_excludes)):
        if extension_excludes[ee_ind] in f_formatted:
            file_good = False
        ee_ind += 1

    if file_good:
        files_good_ext.append(f)


print('Number of files after filter by extension: ', len(files_good_ext))


str_excludes = ['loop', 'bpm', 'vocal', 'vcl', 'guitar', 'gtr', 'stab', 'chord', 'key', 'male',
                'marimb', 'organ']

files_good_str = []

for f in files_good_ext:
    f_formatted = f.replace('\'','x').replace(" ", "x").lower()
    file_good = True
    se_ind = 0

    while (file_good) & (se_ind < len(str_excludes)):
        if str_excludes[se_ind] in f_formatted:
            file_good = False
        se_ind += 1

    if file_good:
        files_good_str.append(f)


print('Number of files after filter by keyword: ', len(files_good_str))


if COPY_DIR[-1] != '/':
    COPY_DIR += '/'
COPY_DIR += 'drums_copied/'
make_dir(COPY_DIR)

total_copied_files = 0

print('\n', '---' + ORIG_DIR + '---')
for k in dd.keys():

    print('---' + k.upper() + '-'*(22 - len(k)))
    for af in files_good_str:
        copy_file_by_str(af, dd, k, COPY_DIR)
    
    k_dir = os.path.join(COPY_DIR, k)
    num_k_files = len(get_files(k_dir))
    total_copied_files += num_k_files

    if os.path.exists(k_dir):
        print('   ' , num_k_files, ' files copied', '\n')

print('\n', 'TOTAL FILES COPIED: ', total_copied_files, '\n', '\n', '\n')

print('If you see any **ERROR** messages above, no need to worry.'  )  
print('Those files either: ')
print('   a) contain a file extension I have missed/forgot to exclude')
print('   b) have an issue with their permissions I did not want to override.')
print('You can still copy and paste manually.', '\n')
