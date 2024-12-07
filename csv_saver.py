class CSVSaver:
    """Class for using csv files"""
    @staticmethod
    def create_clear_file(filename: str) -> None:
        """Create file, if not exist, else clear file"""
        open(filename, 'w').close()

    @staticmethod
    def save(filename: str, data: list) -> None:
        """Save data as a row appended to file"""
        with open(filename, 'a') as f:
            f.write(','.join([str(x) for x in list(data)]))
            f.write('\n')

