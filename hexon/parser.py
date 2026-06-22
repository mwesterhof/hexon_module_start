from xml.etree import ElementTree


def xpath(path):
    def xpath_mapping(parser, data):
        return data.find(path).text
    return xpath_mapping


def method(name):
    def method_mapping(parser, data):
        return getattr(parser, name)(data)
    return method_mapping


hexon_parsers = {}

def parse(xml_body):
    vehicle_data = ElementTree.fromstring(xml_body)
    version = vehicle_data.attrib['versie']
    return hexon_parsers[version]().parse_data(vehicle_data)


class HexonParserMeta(type):
    def __new__(cls, name, parents, attribs):
        instance = super().__new__(cls, name, parents, attribs)
        if parents:
            hexon_parsers[instance.HEXON_VERSION] = instance
        return instance


class HexonParserBase(metaclass=HexonParserMeta):
    HEXON_VERSION = None

    def parse_data(self, vehicle_data):
        return {
            attrib: mapping(self, vehicle_data)
            for attrib, mapping in self.field_paths.items()
        }


class HexonParser2_25(HexonParserBase):
    HEXON_VERSION = '2.25'

    field_paths = {
        'hexon_id': xpath('voertuignr_hexon'),
        'title': xpath('type'),
        'price': xpath('verkoopprijs_particulier/prijzen[@land="nl"]/prijs/bedrag'),
        'brand': xpath('merk_orig'),
        'images': method('parse_images'),
    }

    def parse_images(self, data):
        return [
            {
                'url': img.find('url').text,
                'name': img.find('bestandsnaam').text
            }
            for img in data.findall('afbeeldingen/afbeelding')
        ]