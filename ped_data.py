from os import read
import pandas as pd
import logging as log
from sodapy import Socrata

log.basicConfig(encoding='utf-8', level=log.INFO)


class CsvAggr:

    def calc_ped_data(self, source_csv, daily_dest_csv, monthly_dest_csv):

        df = pd.read_csv(source_csv)

        log.info("generating daily data...")

        day_df = df.groupby(['year','month','mdate','sensor_id']).agg({'hourly_counts':'sum','sensor_name':'first'})

        day_df.to_csv("temp.csv")

        day_df= day_df.groupby(['year','month','mdate'], as_index=False)['hourly_counts'].apply(lambda grp: grp.nlargest(10)).to_csv(daily_dest_csv)

        self.write_to_s3(daily_dest_csv)

        log.info("generating monthly data...")

        month_df =  df.groupby(['year','month','sensor_id']).agg({'date_time':'first','hourly_counts':'sum','sensor_name':'first'})

        month_df.groupby(['year','month'], as_index=False)['hourly_counts'].apply(lambda grp: grp.nlargest(10)).to_csv(monthly_dest_csv)

        self.write_to_s3(monthly_dest_csv)

    def get_csv(self):
        client = Socrata("data.melbourne.vic.gov.au", None)
        results = client.get("b2ak-trbp", limit=1000)

        # Convert to pandas DataFrame
        results_df = pd.DataFrame.from_records(results)

        results_df.to_csv('resources/ped_source.csv')

        log.info("Done generating csv source")

        return

    def write_to_s3(self, csv):
        
        import s3fs

        s3 = s3fs.S3FileSystem(anon=False, key='AKIAQQWQQYEA4MCBRJXK', secret='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')


        with s3.open('s3://firstpractise/belong-data-engg-challenge/{}'.format(csv),'w') as f:
            f.write(csv)

        log.info("Done writing to S3...")
        return



def main():
    

    log.info("Call CsvAggr main...")
    csvAggrObj = CsvAggr()

    csvAggrObj.get_csv()

    csvAggrObj.calc_ped_data('resources/ped_source.csv','daily_ped_count_results.csv','monthly_ped_count_results.csv')


if __name__ == "__main__":
    main()
    