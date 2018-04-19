from __future__ import print_function

import os
import gzip
import wget
from ftplib import FTP

class NoaaFTP:

    """Download solar data from noaa's FTP.

    Args:
        day (str or int):  event's day.
        month (str or int):  event's month.
        year (str or int):  events' year.
        station (str, optional):  Station (default Sagamore Hill).

    Attributes:
        day (str or int):  event's day.
        month (str or int):  event's month.
        year (str or int):  events' year.
        station (str, optional):  Station (default Sagamore Hill).
        filename (str): Name of the downloaded file.
        path (str): Absolute path for the file.
    """

    def __init__(self, day, month, year, station='Sagamore Hill', path):
        self._day = str(day)
        if len(self._day) == 1:
            self._day = '0' + self._day
        self._month = str(month)
        if len(self._month) == 1:
            self._month = '0' + self._month
        self._year = str(year)
        self._station = station
        self._path = path


    def __set_station_name(self):
        return self._station.lower().replace(' ', '-')


    def __change_month_upper(self):
        months = [
            "JAN", "FEV", "MAR", "APR", "MAY", "JUN",
            "JUL", "AUG", "SEP", "OUT", "NOV", "DEC"
        ]

        # Returns the corresponding month to dowload the file.
        index = int(self._month) - 1
        return months[index]


    def __change_month_lower(self):
        months = [
            "jan", "fev", "mar", "apr", "may", "jun",
            "jul", "aug", "sep", "out", "nov", "dec"
        ]

        # Returns the corresponding month to dowload the file.
        index = int(self._month) - 1
        return months[index]


    def __set_file_extension_upper(self):

        if self._station.lower() == "sagamore hill":
            extension = ".K7O.gz"
        elif self._station.lower() == "san vito":
            extension = ".LIS.gz"
        elif self._station.lower() == "palehua":
            extension = ".PHF.gz"
        elif self._station.lower() == "learmonth":
            extension = ".APL.gz"

        return extension

    def __set_file_extension_lower(self):

        if self._station.lower() == "sagamore hill":
            extension = ".k7o.gz"
        elif self._station.lower() == "san vito":
            extension = ".lis.gz"
        elif self._station.lower() == "palehua":
            extension = ".phf.gz"
        elif self._station.lower() == "learmonth":
            extension = ".apl.gz"

        return extension


    def download_data(self):
        try:
            ftp = FTP('ftp.ngdc.noaa.gov')
            print(ftp.getwelcome())
            ftp.login()
        except:
            print("Connection not stablished.")
            return False

        station_name = self.__set_station_name()

        filename = self._day + self.__change_month_upper() + self._year[2:]
        file_extension = self.__set_file_extension_upper()

        url = 'ftp://ftp.ngdc.noaa.gov/STP/space-weather/solar-data/'
        url += 'solar-features/solar-radio/rstn-1-second/'
        url += station_name + '/' + self._year + '/' + self._month + '/'

        # Tries to download with the file extension in lower case.
        # Then tries to download with the file extension in lower case.
        try:
            url += filename + file_extension
            filename = wget.download(url)
        except:
            url = url.split(filename)[0]
            filename = self._day + self.__change_month_lower() + self._year[2:]
            file_extension = self.__set_file_extension_lower()
            url += filename + file_extension
            wget.download(url)
        finally:
            self._filename = filename + file_extension


    def decompress_file(self):
        """
        This function doesn't really decompress the file, it saves the data
        inside a different file with the same name.
        """

        # Checks if the filename varialabe exists.
        try:
            print(self._filename)
        except NameError:
            print("You need to download the file first.")
            return False

        with gzip.open(self._filename, 'rb') as _file:
            file_content = _file.read()
            # Removes .gz from filename.
            final_name = self._filename.split('.gz')
            with open(final_name[0], 'wb') as final_file:
                # Saves the content to a new file.
                final_file.write(file_content)

        if os.path.exists(self._path + "data/"):
            print("Path exists")
        else:
            os.mkdir(self._path + "data/")

        os.rename(self._path + final_name[0],self._path + "data/" + final_name[0])
        os.remove(self.filename)


noaa = NoaaFTP(9, 4, 2002, path=os.path.dirname(os.path.abspath(__file__)) + "/")
noaa.download_data()
noaa.decompress_file()