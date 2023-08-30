import os
import time
import shutil
import argparse

g_curDir = os.path.dirname(os.path.realpath(__file__))
g_vcpkg_root = ''

def DeleteOldExports():
    pass

def DoExport(vcpkg_installed_dir):
    print('DoExport...')
    print('vcpkg_installed_dir: %s'%vcpkg_installed_dir)
    print('g_curDir: %s'%g_curDir)
    print('g_vcpkg_root: %s'%g_vcpkg_root)

    # copy recursive from vcpkg_installed_dir to ./vcpkg-export-yyyyMMdd-hhmmss/installed
    timeStr = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
    exportDir = os.path.join(g_curDir, 'vcpkg-export-' + timeStr)
    
    print('copy from %s to %s'%(vcpkg_installed_dir, exportDir))
    shutil.copytree(vcpkg_installed_dir, os.path.join(exportDir, 'installed'))

    return exportDir

def CleanupExport(exportDir):
    print('CleanupExport...')
    print('Delete pdbs...')
    for root, dirs, files in os.walk(exportDir):
        for name in files:
            if os.path.splitext(name)[-1] == '.pdb':
                print('delete ' + os.path.join(root, name))
                os.remove(os.path.join(root, name))

def PatchExports(exportDir):
    print('PatchExports...')
    print('patching %s'%exportDir)
    print('copy vcpkg.exe...')
    shutil.copy(os.path.join(g_vcpkg_root, 'vcpkg.exe'), os.path.join(exportDir, 'vcpkg.exe'))
    print('copy triplets...')
    shutil.copytree(os.path.join(g_vcpkg_root, 'triplets'), os.path.join(exportDir, 'triplets'))

    # create .vcpkg-root file
    print('create a empty .vcpkg-root file...')
    with open(os.path.join(exportDir, '.vcpkg-root'), 'w') as f:
        f.write('')

    print('copy scripts')
    # copy scripts/buildsystems
    shutil.copytree(os.path.join(g_vcpkg_root, 'scripts/buildsystems'), os.path.join(exportDir, 'scripts/buildsystems'))
    # copy scripts/cmake
    shutil.copytree(os.path.join(g_vcpkg_root, 'scripts/cmake'), os.path.join(exportDir, 'scripts/cmake'))
    # copy scripts/ports.cmake
    shutil.copy(os.path.join(g_vcpkg_root, 'scripts/ports.cmake'), os.path.join( exportDir, 'scripts/ports.cmake'))

def ZipExports(exportDir):
    print('Compress exported packages to zip archive...')
    print('compress %s'%exportDir)
    # compress exportDir folder to zip archive
    exportDirName = os.path.basename(exportDir)
    shutil.make_archive(exportDir, 'zip', os.path.join(exportDir, '..'), exportDirName)
    zipSize = os.path.getsize(exportDir + '.zip')
    print('zip archive size %.2fM'%(zipSize/1024/1024))

def MakePkg(vcpkg_installed_dir):
    print('----------------------------------------')
    exportDir = DoExport(vcpkg_installed_dir)
    print('----------------------------------------')
    CleanupExport(exportDir)
    print('----------------------------------------')
    PatchExports(exportDir)
    print('----------------------------------------')
    ZipExports(exportDir)
    print('----------------------------------------')

def ArgsValid(args):
    # check --vcpkg-installed-dir
    if args.vcpkg_installed_dir is None:
        print('vcpkg installed dir is not specified')
        return False
    if not os.path.exists(args.vcpkg_installed_dir):
        print('vcpkg installed dir does not exist')
        return False
    
    # check --vcpkg-root
    if args.vcpkg_root is None:
        print('vcpkg root dir is not specified')
        return False
    if not os.path.exists(args.vcpkg_root):
        print('vcpkg root dir does not exist')
        return False
    
    # check vcpkg.exe
    vcpkg_exe = os.path.join(args.vcpkg_root, 'vcpkg.exe')
    if not os.path.exists(vcpkg_exe):
        print('vcpkg.exe does not exist, please run bootstrap-vcpkg.bat in vcpkg root dir: %s'%args.vcpkg_root)
        return False
    
    # set global vcpkg_root
    global g_vcpkg_root
    g_vcpkg_root = args.vcpkg_root

    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='package vkpkg ports.')
    
    # --vcpkg-installed-dir
    parser.add_argument('--vcpkg-installed-dir', dest='vcpkg_installed_dir', default=None, help='vcpkg installed dir')
    # --vcpkg-root
    parser.add_argument('--vcpkg-root', dest='vcpkg_root', default=None, help='vcpkg root dir')

    # parse args
    args = parser.parse_args()

    # check args
    if not ArgsValid(args):
        exit(1)

    # make package
    MakePkg(args.vcpkg_installed_dir)