"""Helpers to download and extract archives"""

# Adapted for viset from original authors below
# 
# Authors: Nicolas Pinto <pinto@rowland.harvard.edu>
#          Nicolas Poilvert <poilvert@rowland.harvard.edu>
# License: BSD 3 clause

from urllib2 import urlopen
from os import path
import hashlib
import sys
import viset.util
import archive
import os


def generate_sha1(filepath):
    sha1 = hashlib.sha1()
    f = open(filepath, 'rb')
    try:
        sha1.update(f.read())
    finally:
        f.close()
    return sha1.hexdigest()

def verify_sha1(filename, sha1):
    data = open(filename, 'rb').read()
    if sha1 != hashlib.sha1(data).hexdigest():
        raise IOError("[viset.cache]: File '%s': invalid SHA-1 hash!  This file must be deleted manually." % filename)

def verify_md5(filename, md5):
    data = open(filename, 'rb').read()
    if md5 != hashlib.md5(data).hexdigest():
        raise IOError("File '%s': invalid md5 hash! You may want to delete "
                      "this corrupted file..." % filename)


def download(url, output_filename, sha1=None, verbose=True, md5=None, timeout=None):
    """Downloads file at `url` and write it in `output_dirname`"""

    # socket.setdefaulttimeout(10)  # do not set globally
        
    page = urlopen(url, timeout=timeout)
    page_info = page.info()

    output_file = open(output_filename, 'wb+')

    # size of the download unit
    block_size = 2 ** 15
    dl_size = 0

    if verbose:
        print "[viset.cache]: Downloading '%s' to '%s'" % (url, output_filename)
    # display  progress only if we know the length
    if 'content-length' in page_info and verbose:
        # file size in Kilobytes
        file_size = int(page_info['content-length']) / 1024.
        while True:
            buffer = page.read(block_size)
            if not buffer:
                break
            dl_size += block_size / 1024
            output_file.write(buffer)
            percent = min(100, 100. * dl_size / file_size)
            status = r"Progress: %20d kilobytes [%4.1f%%]" \
                    % (dl_size, percent)
            status = status + chr(8) * (len(status) + 1) 
            print status, # space instead of newline
            sys.stdout.flush()
        print ''
    else:
        output_file.write(page.read())

    output_file.close()

    if sha1 is not None:
        verify_sha1(output_filename, sha1)

    if md5 is not None:
        verify_md5(output_filename, md5)


def extract(archive_filename, output_dirname, sha1=None, verbose=True):
    """Extracts `archive_filename` in `output_dirname`.

    Supported archives:
    -------------------
    * Zip formats and equivalents: .zip, .egg, .jar
    * Tar and compressed tar formats: .tar, .tar.gz, .tgz, .tar.bz2, .tz2
    * gzip compressed files
    """
    if verbose:
        print "[viset.cache]: Extracting '%s' to '%s'" % (archive_filename, output_dirname)
    if sha1 is not None:
        if verbose:
            print " SHA-1 verification..."
        verify_sha1(archive_filename, sha1)
    archive.extract(archive_filename, output_dirname, verbose=verbose)


def download_and_extract(url, output_dirname, sha1=None, verbose=True):
    """Downloads and extracts archive in `url` into `output_dirname`.

    Note that `output_dirname` has to exist and won't be created by this
    function.
    """
    archive_basename = path.basename(url)
    archive_filename = path.join(output_dirname, archive_basename)
    download(url, archive_filename, sha1=sha1, verbose=verbose)
    extract(archive_filename, output_dirname, sha1=sha1, verbose=verbose)

def download_extract_cleanup(url, output_dirname, sha1=None, verbose=True):
    download_and_extract(url, output_dirname, sha1, verbose)
    os.remove(path.join(output_dirname, path.basename(url)))

def extract_and_cleanup(archive_filename, output_dirname, sha1=None, verbose=True):
    download_and_extract(url, output_dirname, sha1, verbose)
    os.remove(path.join(output_dirname, path.basename(url)))
    
def cache_and_extract(url, output_dirname, sha1=None, verbose=True):
    if not viset.util.isfile(path.join(output_dirname, path.basename(url))):
        download_and_extract(url, output_dirname, sha1, verbose)
        



        
        
    
