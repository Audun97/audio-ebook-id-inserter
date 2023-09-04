import os
import xml.etree.ElementTree as ET
from mutagen.mp3 import MP3

def get_smil_files(book_dir):
    smil_folder = os.path.join(book_dir, 'smil')
    smil_files = []
    for file in os.listdir(smil_folder):
        if file.endswith(".smil"):
            smil_files.append(os.path.join(smil_folder, file))
    return smil_files

def parse_smil_files(smil_files, book_dir):
    smil_data = []
    total_duration = 0
    for smil_file in smil_files:
        tree = ET.parse(smil_file)
        root = tree.getroot()
        seq_element = root.find('.//{http://www.w3.org/ns/SMIL}seq')
        par_element = seq_element.find('.//{http://www.w3.org/ns/SMIL}par')
        audio_element = par_element.find('.//{http://www.w3.org/ns/SMIL}audio')
        audio_src = audio_element.attrib['src']
        audio_file = os.path.join(book_dir, audio_src[3:])
        audio = MP3(audio_file)
        seq_duration = audio.info.length
        total_duration += seq_duration
        smil_data.append({
            'id': seq_element.attrib['id'],
            'href': smil_file,
            'media-type': 'application/smil+xml',
            'duration': seq_duration
        })
    return smil_data, total_duration

def update_opf_file(book_dir, smil_data, total_duration):
    opf_file = os.path.join(book_dir, 'content.opf')
    tree = ET.parse(opf_file)
    root = tree.getroot()

    metadata = root.find('.//{http://www.idpf.org/2007/opf}metadata')
    manifest = root.find('.//{http://www.idpf.org/2007/opf}manifest')

    for smil_info in smil_data:
        # Add Media Overlays metadata
        media_duration = ET.SubElement(metadata, '{http://www.idpf.org/2007/opf}meta')
        media_duration.set('property', 'media:duration')
        media_duration.set('refines', f'#{smil_info["id"]}')
        media_duration.text = f'{smil_info["duration"]:.3f}'

        # Add Manifest item
        item = ET.SubElement(manifest, '{http://www.idpf.org/2007/opf}item')
        item.set('id', smil_info['id'])
        item.set('href', smil_info['href'])
        item.set('media-type', smil_info['media-type'])

    # Add total duration metadata
    total_duration_meta = ET.SubElement(metadata, '{http://www.idpf.org/2007/opf}meta')
    total_duration_meta.set('property', 'media:duration')
    total_duration_meta.text = f'{total_duration:.3f}'

    # Add Media Overlays active class metadata
    active_class_meta = ET.SubElement(metadata, '{http://www.idpf.org/2007/opf}meta')
    active_class_meta.set('property', 'media:active-class')
    active_class_meta.text = '-epub-media-overlay-active'

    tree.write(opf_file, encoding='utf-8', xml_declaration=True)

book_dir = 'test_book\\EPUB'

smil_files = get_smil_files(book_dir)
smil_data, total_duration = parse_smil_files(smil_files, book_dir)
update_opf_file(book_dir, smil_data, total_duration)

