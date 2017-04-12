from xml.dom import minidom


class KML:
    def __init__(self):
        self.__root = minidom.parseString(
            """<?xml version="1.0" encoding="utf-8"?>
            <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
              <Document>
                <Style id="classical">
                  <IconStyle>
                    <scale>1</scale>
                    <Icon>
                      <href>https://raw.githubusercontent.com/yrjyrj123/image/master/classical.png</href>
                    </Icon>
                  </IconStyle>
                </Style>
                <Style id="lite">
                  <IconStyle>
                    <scale>1</scale>
                    <Icon>
                      <href>https://raw.githubusercontent.com/yrjyrj123/image/master/lite.png</href>
                    </Icon>
                  </IconStyle>
                </Style>
                 <Style id="red_packet">
                  <IconStyle>
                    <scale>1</scale>
                    <Icon>
                      <href>https://raw.githubusercontent.com/yrjyrj123/image/master/red_packet.png</href>
                    </Icon>
                  </IconStyle>
                </Style>
                <name>Mobike</name>
              </Document>
            </kml>
            """)
        self.__document_node = self.__root.getElementsByTagName("Document")[0]

    def add_bike(self, bike):
        placemark = self.__root.createElement("Placemark")
        self.__document_node.appendChild(placemark)
        name = self.__root.createElement("name")
        name.appendChild(self.__root.createTextNode(bike['bikeid']))
        placemark.appendChild(name)

        styleUrl = self.__root.createElement("styleUrl")
        styleUrl.appendChild(self.__root.createTextNode(bike['biketype']))
        placemark.appendChild(styleUrl)

        point = self.__root.createElement("Point")
        placemark.appendChild(point)
        coordinates = self.__root.createElement("coordinates")
        coordinates.appendChild(self.__root.createTextNode("%s,%s,%s" % (bike['lon'], bike['lat'], "0")))
        point.appendChild(coordinates)

    def get_kml(self):
        return self.__root.toxml()
