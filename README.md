# datagathering
Analysis of results by country, city and type
************ Source Data ************
Fields from csv file:
IP	Country	Download	Upload	Latency	ISP	Timestamp	Latitude	Longitude	
ConnectionType	DeviceID	POP	AppID	ExchangeName	Date Time	City Distance	City?	Hour	Peak?

Calculaations:
=SQRT(((H2-centre_lat)*length_lat)^2 + ((I2-centre_long)*length_long)^2)

