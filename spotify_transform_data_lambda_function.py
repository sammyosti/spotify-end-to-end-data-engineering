import json
import boto3
from datetime import datetime
from io import StringIO
import pandas as pd

# Function to extract album information from the data
def album(data):
    album_list = []
    for row in data['items']:
        album_id = row['track']['album']['id']
        album_name = row['track']['album']['name']
        album_release_date = row['track']['album']['release_date']
        album_total_tracks = row['track']['album']['total_tracks']
        album_url = row['track']['album']['external_urls']['spotify']
        album_element = {'album_id': album_id, 'name': album_name, 'release_date': album_release_date, 'total_tracks': album_total_tracks,
                         'url': album_url}

        album_list.append(album_element)
    
    return album_list

# Function to extract artist information from the data
def artist(data):
    artist_list = []
    for row in data['items']:
        for key, value in row.items():
            if key == 'track':
                for artist in value['artists']:
                    artist_dict = {'artist_id': artist['id'], 'artist_name': artist['name'], 'external_url': artist['href']}
                    artist_list.append(artist_dict)
    return artist_list

# Function to extract song information from the data
def songs(data):
    song_list = []
    for row in data['items']:
        song_id = row['track']['id']
        song_name = row['track']['name']
        song_duration = row['track']['duration_ms']
        song_url = row['track']['external_urls']['spotify']
        song_popularity = row['track']['popularity']
        song_added = row['added_at']
        album_id = row['track']['album']['id']
        artist_id = row['track']['album']['artists'][0]['id']
        song_element = {'song_id': song_id, 'song_name': song_name, 'duration_ms': song_duration, 'url': song_url, 'popularity': song_popularity,
                        'song_added': song_added, 'album_id': album_id, 'artist_id': artist_id}
        song_list.append(song_element)
    
    return song_list

# Main Lambda handler function
def lambda_handler(event, context):
    s3 = boto3.client('s3')
    Bucket = 'spotify-etl-project-sammyosti'
    Key = 'raw_data/to_processed/'
    
    spotify_data = []
    spotify_keys = []

    # Attempt to list and read JSON files from the specified S3 bucket and prefix
    try:
        response = s3.list_objects(Bucket=Bucket, Prefix=Key)
        if 'Contents' in response:
            for file in response['Contents']:
                file_key = file['Key']
                if file_key.split('.')[-1] == 'json':  # Only process JSON files
                    response = s3.get_object(Bucket=Bucket, Key=file_key)
                    content = response['Body']
                    jsonObject = json.loads(content.read())
                    spotify_data.append(jsonObject)
                    spotify_keys.append(file_key)
        else:
            print("No files found in the specified bucket and prefix.")
            return
    except Exception as e:
        print(f"Error reading from S3: {e}")
        return
    
    # Attempting to process the data and transform it into CSV format
    try:
        for data in spotify_data:
            album_list = album(data)
            artist_list = artist(data)
            song_list = songs(data)
            
            # Creating dataframes from lists and remove duplicates
            album_df = pd.DataFrame.from_dict(album_list).drop_duplicates(subset=['album_id'])
            artist_df = pd.DataFrame.from_dict(artist_list).drop_duplicates(subset=['artist_id'])
            song_df = pd.DataFrame.from_dict(song_list)
            song_df['song_added'] = pd.to_datetime(song_df['song_added'])
            
            # Generating timestamps for unique file names
            timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
            
            # Defining S3 keys for the transformed data
            song_key = f'transformed_data/songs_data/songs_transformed_{timestamp}.csv'
            album_key = f'transformed_data/album_data/album_transformed_{timestamp}.csv'
            artist_key = f'transformed_data/artist_data/artist_transformed_{timestamp}.csv'
            
            # Saving dataframes to CSV and upload to S3
            song_buffer = StringIO()
            album_buffer = StringIO()
            artist_buffer = StringIO()
            
            song_df.to_csv(song_buffer, index=False)
            album_df.to_csv(album_buffer, index=False)
            artist_df.to_csv(artist_buffer, index=False)
            
            s3.put_object(Bucket=Bucket, Key=song_key, Body=song_buffer.getvalue())
            s3.put_object(Bucket=Bucket, Key=album_key, Body=album_buffer.getvalue())
            s3.put_object(Bucket=Bucket, Key=artist_key, Body=artist_buffer.getvalue())
            
        # Moving processed files to the 'processed' folder in S3 and delete originals
        s3_resource = boto3.resource('s3')
        for key in spotify_keys:
            copy_source = {'Bucket': Bucket, 'Key': key}
            s3_resource.meta.client.copy(copy_source, Bucket, 'raw_data/processed/' + key.split("/")[-1])
            s3_resource.Object(Bucket, key).delete()
    except Exception as e:
        print(f"Error processing data: {e}")
        
        
        
