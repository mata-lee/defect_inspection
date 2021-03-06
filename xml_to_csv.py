import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from tqdm import tqdm
#%%
def xml_to_csv(path):
    xml_list = []
    for xml_file in tqdm(glob.glob(path + '/*.xml'), desc = 'xml_to_csv'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df
#%%
image_path = os.path.join(os.getcwd(), '2. data/99. Object_detection/images/test')
xml_df = xml_to_csv(image_path)
xml_df.to_csv(os.path.join(os.getcwd(), '2. data/99. Object_detection/images/test') + '/test_labels.csv', index=None)
print('Successfully converted xml to csv.')
#%%
# def main():
#     image_path = os.path.join(os.getcwd(), 'annotations')
#     xml_df = xml_to_csv(image_path)
#     xml_df.to_csv('raccoon_labels.csv', index=None)
#     print('Successfully converted xml to csv.')
#
#
# main()