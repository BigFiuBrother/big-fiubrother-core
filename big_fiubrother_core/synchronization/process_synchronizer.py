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

    def register_face_task(self, video_id, frame_id, face_id):
        self.zk_client.create_node(
            self._to_path(video_id, frame_id, face_id), b'data')

    # Cascades upwards and returns True if the 'video task' was also completed by this call
    def complete_face_task(self, video_id, frame_id, face_id):
        self.zk_client.delete_node(
            self._to_path(video_id, frame_id, face_id))

        remaining_faces = self.zk_client.get_children_count(self._to_path(video_id, frame_id))
        if remaining_faces == 0:
            return self.complete_frame_task(video_id, frame_id)

        return False

    # Cascades upwards and returns True if the 'video task' was also completed by this call
    def complete_frame_task(self, video_id, frame_id):
        if self.zk_client.safe_delete_node(self._to_path(video_id, frame_id)):
            remaining_frames = self.zk_client.get_children_count(self._to_path(video_id))
            if remaining_frames == 0:
                return self.complete_video_task(video_id)

        return False

    # returns True if the 'video task' was completed by this call
    def complete_video_task(self, video_id):
        return self.zk_client.safe_delete_node(self._to_path(video_id))

    def _to_path(self, *dirs):
        return ''.join(['/{}'.format(d) for d in dirs])

    def close(self):
        self.zk_client.close()
