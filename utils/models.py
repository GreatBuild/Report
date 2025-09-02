class OutputFile:
    def __init__(self, source_dir, output_file_name, order):
        self.source_dir = source_dir
        self.output_file_name = output_file_name
        self.order = order
        self.level = 0

class HeaderOutputFile(OutputFile):
    def __init__(self, source_dir, output_file_name, order, header):
        super().__init__(source_dir, output_file_name, order)
        self.header = header
        self.level = 1