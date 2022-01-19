import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

templist = []

a, b = Adafruit_DHT.read_retry(DHT_SENSOR,DHT_PIN)
print(a)

for x in range(2):
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR,DHT_PIN)
    print(temperature)
    templist.append(temperature)

print(templist)

tempavg = sum(templist)/len(templist)

print(tempavg)

