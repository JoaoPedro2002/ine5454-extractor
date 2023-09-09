from parsers.teammates_parser import TeammatesParser

if __name__ == "__main__":
    parser = TeammatesParser()
    parser.parse("jamesle01")
    print(parser.to_json())