# try:
    # relative imports
from cvtool.CV import CVClass
# except ImportError:
#     from CV import CVClass
    


cv = CVClass("/Users/daniel.ellis/WIPwork/mip-cmor-tables/mip_cmor_tables/out/CMIP6Plus_CV.json")

from cvtool.ESGF import cv2ini

from cvtool.ESGF import read
base = '/Users/daniel.ellis/WIPwork/esgf-config/publisher-configs/ini/'
path = f'{base}esg.cmip6.ini'
cmip6 = read.ESGFIni(path)

# print(cmip6.headers)