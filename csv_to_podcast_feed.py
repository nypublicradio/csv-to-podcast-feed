import argparse
import pandas as pd
from xml.etree.ElementTree import Element, SubElement, ElementTree
import datetime
import os

def generate_rss(input_csv, output_xml):
    # Read the CSV file
    df = pd.read_csv(input_csv)

    # Create the main RSS element
    rss = Element('rss', version='2.0')

    # Create the channel element and add it to the RSS element
    channel = SubElement(rss, 'channel')

    # Add mandatory channel elements
    SubElement(channel, 'title').text = 'My Podcast'
    SubElement(channel, 'description').text = 'Description of My Podcast'
    SubElement(channel, 'link').text = 'http://www.example.com'

    # Loop through the DataFrame to add episodes
    for index, row in df.iterrows():
        if not pd.isna(row['audio']):
            # Create an item for each episode and add it to the channel
            item = SubElement(channel, 'item')

            # Add episode details
            SubElement(item, 'title').text = str(row['show'])
            SubElement(item, 'description').text = str(row['tease'])
            SubElement(item, 'pubDate').text = datetime.datetime.strptime(row['airdate'], '%Y-%m-%d').strftime('%a, %d %b %Y 00:00:00 +0000')

            # Add the enclosure (audio file)
            SubElement(item, 'enclosure', url=str(row['audio']), length='0', type='audio/mpeg')

    # Create an ElementTree and write the RSS feed to a file
    tree = ElementTree(rss)
    tree.write(output_xml)

if __name__ == '__main__':
    # Initialize argument parser
    parser = argparse.ArgumentParser(description='Generate RSS feed from CSV.')

    # Add input and output file arguments
    parser.add_argument('-i', '--input', required=True, help='Input CSV file.')
    parser.add_argument('-o', '--output', required=False, help='Output XML file.')

    # Parse the arguments
    args = parser.parse_args()

    # Determine the output filename
    if args.output:
        output_file = args.output
    else:
        output_file = os.path.splitext(args.input)[0] + '.xml'

    # Generate the RSS feed
    generate_rss(args.input, output_file)

