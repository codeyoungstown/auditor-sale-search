# auditor-sale-search
CLI tool to search yesterday's posted sales on the Mahoning County Auditor website for transfers to a new owner. Outputs parcel ID, address, and a link to google maps if the property is a house.


## Requirements
Python and the beautifulsoup4 library installed. This also requires curl to be installed.

## Usage

Example:
```
nick@nick $ python sales.py "RISING STAR BAPTIST CHURCH"

Found transfers:
53-217-0-051.00-0 JACOBS RD
53-217-0-072.00-0 SHAW AVE
53-217-0-077.00-0 SHAW AVE
53-217-0-075.00-0 SHAW AVE
53-217-0-078.00-0 SHAW AVE
53-217-0-052.00-0 JACOBS RD
53-217-0-073.00-0 SHAW AVE
53-217-0-076.00-0 SHAW AVE
53-217-0-049.00-0 MYRON AVE
53-217-0-059.00-0 WARDLE AVE
53-217-0-071.00-0 SHAW AVE
53-217-0-074.00-0 1749 SHAW AVE https://www.google.com/maps/place/1749+SHAW+AVE+mahoning+county+oh/
```
