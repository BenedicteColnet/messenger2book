class BaseChatAppModel():
    def parse_from_json(self, data_path, me, my_friend):
        """Reads a file containing data from a supported chat app service and reformats it."""
        assert data_path[-5:] == '.json', f'File should have a .json extension, found {data_path}'
        raw_data = self._load_data(data_path)
        processed_data = self._pre_process(raw_data, me, my_friend)
        return processed_data

    def _load_data(self, data_path):
        """Opens and reads the specified file in the chat app native format."""
        raise NotImplementedError()

    def _pre_process(self, raw_data):
        """Reformats the data from native chat app format to standardized format."""
        return raw_data
