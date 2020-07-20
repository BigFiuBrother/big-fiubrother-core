from . import ZookeeperClient


class ProcessSynchronizer:

    def __init__(self, configuration):
        self.zk_client = ZookeeperClient(configuration)

    def register_video_task(self, video_id):
        self.zk_client.create_node(
            self._to_path(video_id), b'data')

    def register_frame_task(self, video_id, frame_id):
        self.zk_client.create_node(
            self._to_path(video_id, frame_id), b'data')

    def complete_frame_task(self, video_id, frame_id):
        self.zk_client.delete_node(
            self._to_path(video_id, frame_id))

    def complete_video_task(self, video_id):
        self.zk_client.delete_node(self._to_path(video_id))

    def is_video_task_finished(self, video_id):
        children = self.zk_client.get_children(self._to_path(video_id))
        return [len(children) == 0, len(children)]

    def _to_path(self, *dirs):
        return '/' + '/'.join(dirs)

    def close(self):
        self.zk_client.close()
