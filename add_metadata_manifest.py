import os
import xml.etree.ElementTree as ET

def get_smil_files(folder_path):
    smil_files = []
    for file in os.listdir(folder_path):
        if file.endswith(".smil"):
            smil_files.append(os.path.join(folder_path, file))
    return smil_files

def parse_smil_files(smil_files):
    smil_data = []
    for smil_file in smil_files:
        tree = ET.parse(smil_file)
        root = tree.getroot()
        seq_element = root.find('.//{http://www.w3.org/ns/SMIL}seq')
        smil_data.append({
            'id': seq_element.attrib['id'],
            'href': smil_file,
            'media-type': 'application/smil+xml'
        })
    return smil_data

def update_opf_file(opf_file, smil_data):
    tree = ET.parse(opf_file)
    root = tree.getroot()

    metadata = root.find('.//{http://www.idpf.org/2007/opf}metadata')
    manifest = root.find('.//{http://www.idpf.org/2007/opf}manifest')

    for smil_info in smil_data:
        # Add Media Overlays metadata
        media_duration = ET.SubElement(metadata, '{http://www.idpf.org/2007/opf}meta')
        media_duration.set('property', 'media:duration')
        media_duration.set('refines', f'#{smil_info["id"]}')
        media_duration.text = '00:00:00'  # Replace with the actual duration of the audio file

        # Add Manifest item
        item = ET.SubElement(manifest, '{http://www.idpf.org/2007/opf}item')
        item.set('id', smil_info['id'])
        item.set('href', smil_info['href'])
        item.set('media-type', smil_info['media-type'])

    tree.write(opf_file, encoding='utf-8', xml_declaration=True)


smil_folder = 'smil'
opf_file = r'C:\Users\Audun\Desktop\dostoy\epub\content.opf'

smil_files = get_smil_files(smil_folder)
smil_data = parse_smil_files(smil_files)
update_opf_file(opf_file, smil_data)

