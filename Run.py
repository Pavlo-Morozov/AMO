import pandas as pd
# sheet_names = ['Creative backlog', 'Facebook Ads data', 'Campaigns_Adsets', 'Google Ad Manager revenue data']


def import_table(sheet_name):
    # Import the table from Google sheets


    # spreadsheets key url
    gsheetkey = "16KQkQx_N9520NXK7lu8s9pJn9mgS8Jg4xF6tudiiXug"

    url=f'https://docs.google.com/spreadsheet/ccc?key={gsheetkey}&output=xlsx'
    df = pd.read_excel(url,sheet_name=sheet_name)

    return df


def export_table(sheet_name, df):
    df.to_csv(f"Dataset\{sheet_name.replace(' ', '_')}.csv", index=False)


def backlog(sheet_name = "Creative backlog"):
    '''Loads baclog file'''

    # download backlog
    df = import_table(sheet_name)

    # Make "backlog_campaign_name" column for connection with 'Facebook Ads data'
    # List of columns to concatenate
    columns_to_concat = ['articleId', 'type', 'version', 'author', 'media']

    # Create the new column by concatenating the specified columns
    df['campaign_name'] = df.apply(
        lambda row: ' '.join(str(row[col]) for col in columns_to_concat), axis=1
    )

    export_table(sheet_name, df)


def ads_table():
    '''Merge Facebook and Google tables in one'''

    # Campaigns_Adsets
    adsets = import_table('Campaigns_Adsets')
    adsets = adsets.drop_duplicates()

    # Facebook
    facebook = import_table('Facebook Ads data')

    # delete "android " and brackets
    # I user regex, becaus later it can have other values (apple)
    facebook['campaign_name'] = facebook['campaign_name'].replace('(?<=v\d\s).*?(?=\()', '', regex=True)
    facebook['campaign_name'] = facebook['campaign_name'].replace('[()]', '', regex=True)

    # google
    google = import_table('Google Ad Manager revenue data')

    df = google.merge(adsets, on='adset_id', how='left').merge(facebook, on=['campaign_id', 'date'], how='outer')
    export_table('Facebook_Google', df)



if __name__ == "__main__":
    backlog()
    ads_table()
    print("Done!")

