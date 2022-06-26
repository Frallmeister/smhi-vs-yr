# smhi-vs-yr
Statistical analysis comparing weather forecasts from SMHI and YR

## SMHI

### Stations

| id    | Name                          |
|-------|-------------------------------|
| 71410 | Göteborg A                    | 
| 72420 | Göteborg-Landvetter Flygplats |
| 71380 | Vinga A                       |

### Parameters

| Parameter | Name | Summary |  Stations |
|-----------|------|---------|-----------|
| 1  |  Lufttemperatur  |  momentanvärde, 1 gång/tim |  71420, 72420  |
| 3  |  Vindriktning  |  medelvärde 10 min, 1 gång/tim |  71420, 72420  |
| 4  |  Vindhastighet  |  medelvärde 10 min, 1 gång/tim |  71420, 72420  |
| 6  |  Relativ Luftfuktighet  |  momentanvärde, 1 gång/tim |  71420, 72420  |
| 7  |  Nederbördsmängd  |  summa 1 timme, 1 gång/tim |  71420  |
| 9  |  Lufttryck reducerat havsytans nivå  |  vid havsytans nivå, momentanvärde, 1 gång/tim |  71420, 72420  |
| 12  |  Sikt  |  momentanvärde, 1 gång/tim |  71420, 72420  |
| 13  |  Rådande väder  |  momentanvärde, 1 gång/tim resp 8 gånger/dygn |  71420, 72420  |
| 14  |  Nederbördsmängd  |  summa 15 min, 4 gånger/tim |  71420  |
| 21  |  Byvind  |  max, 1 gång/tim |  71420  |
| 25  |  Max av MedelVindhastighet  |  maximum av medelvärde 10 min, under 3 timmar, 1 gång/tim |  71420  |
| 26  |  Lufttemperatur  |  min, 2 gånger per dygn, kl 06 och 18 |  71420, 72420  |
| 27  |  Lufttemperatur  |  max, 2 gånger per dygn, kl 06 och 18 |  71420  |
| 28  |  Molnbas  |  lägsta molnlager, momentanvärde, 1 gång/tim |  72420  |
| 29  |  Molnmängd  |  lägsta molnlager, momentanvärde, 1 gång/tim |  72420  |
| 30  |  Molnbas  |  andra molnlager, momentanvärde, 1 gång/tim |  72420  |
| 31  |  Molnmängd  |  andra molnlager, momentanvärde, 1 gång/tim |  72420  |
| 32  |  Molnbas  |  tredje molnlager, momentanvärde, 1 gång/tim |  72420  |
| 33  |  Molnmängd  |  tredje molnlager, momentanvärde, 1 gång/tim |  72420  |
| 34  |  Molnbas  |  fjärde molnlager, momentanvärde, 1 gång/tim |  72420  |
| 35  |  Molnmängd  |  fjärde molnlager, momentanvärde, 1 gång/tim |  72420  |
| 36  |  Molnbas  |  lägsta molnbas, momentanvärde, 1 gång/tim |  72420  |
| 38  |  Nederbördsintensitet  |  max av medel under 15 min, 4 gånger/tim |  71420, 72420  |
| 39  |  Daggpunktstemperatur  |  momentanvärde, 1 gång/tim |  71420, 72420  |

# Resources

## SMHI

[Open Data SMHI](https://opendata.smhi.se/apidocs/)

[SMHI Open Data API](https://opendata.smhi.se/apidocs/metfcst/index.html)

## YR
[Getting started](https://developer.yr.no/doc/)
[Using LocationForecast](https://developer.yr.no/doc/locationforecast/HowTO/)