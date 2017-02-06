import ssl
import threading
from gocd import Server
from datetime import datetime


class GoCrazy:
    def __init__(self, server, username, password, disable_ssl_check=True):

        # Turn off SSL certificate checking. Bad!
        if disable_ssl_check:
            ssl._create_default_https_context = ssl._create_unverified_context

        self.server = Server(server, username, password)

        self.response_fetched = datetime.min
        self.response_lock = threading.Lock()
        self.response = ""

    def get_build_result(self, pipeline):
        history = pipeline.history()

        if history.is_ok:
            runs = history.body['pipelines']
            if not runs or len(runs) == 0:
                return "NEVER RUN"

            last_run = runs[0]

            for stage in last_run['stages']:
                result = stage.get('result')
                if result and result != 'Passed':
                    return result

            return 'Passed'

    def is_paused(self, pipeline):
        status = pipeline.status().body
        return status['paused']

    def fetch_build_status(self):
        groups = self.server.pipeline_groups().response
        result = []

        for group in groups:
            group_name = group['name']

            for p in group['pipelines']:
                pipeline_name = p['name']
                pipeline = self.server.pipeline(pipeline_name)

                result.append({
                    "group": group_name,
                    "pipeline": pipeline_name,
                    "status": self.get_build_result(pipeline),
                    "paused": self.is_paused(pipeline)
                })

        return result

    def get_build_status(self):
        with self.response_lock:
            if (datetime.utcnow() - self.response_fetched).total_seconds() > 30:
                self.response = self.fetch_build_status()
                self.response_fetched = datetime.utcnow()
        return self.response