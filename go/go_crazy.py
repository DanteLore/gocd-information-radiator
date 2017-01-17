import ssl
from gocd import Server


class GoCrazy:
    def __init__(self, server, username, password):

        # Turn off SSL certificate checking. Bad!
        ssl._create_default_https_context = ssl._create_unverified_context

        self.server = Server(server, username, password)

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

    def get_build_status(self):
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
