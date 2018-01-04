import json
import logging
import requests


class GoCdWrapper:
    def __init__(self, url, username, password, filter_groups=None):
        self.url = url
        self.username = username
        self.password = password
        if filter_groups:
            self.filter_groups = [fg.lower().strip(' ') for fg in filter_groups.split(',')]
        else:
            self.filter_groups = None

        self.logger = logging.getLogger("TESTING")
        self.logger.setLevel("DEBUG")
        self.logger.addHandler(logging.StreamHandler())

    def get_build_result(self, name):
        pipeline = self.fetch("/pipelines/{0}/instance/1".format(name))

        if not pipeline:
            return "NEVER RUN"

        for stage in pipeline['stages']:
            result = stage.get('result')
            if result and result != 'Passed':
                return result

        return 'Passed'

    def get_build_result_from_history(self, pipeline):
        history = self.fetch("/pipelines/{0}/history/0".format(pipeline))

        runs = history['pipelines']
        if not runs or len(runs) == 0:
            return "NEVER RUN"

        last_run = runs[0]

        for stage in last_run['stages']:
            result = stage.get('result')
            if result and result != 'Passed':
                return result

        return 'Passed'

    def is_paused(self, name):
        status = self.fetch("/pipelines/{0}/status".format(name))

        if not status:
            return None

        return status['paused']

    def fetch(self, url):
        response = requests.get(self.url.rstrip('/') + "/go/api/" + url.lstrip('/'),
                                auth=(self.username, self.password),
                                verify=False)
        self.logger.info("Fetched '{0}' status={1}".format(response.url, response.status_code))
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            return None

    def get_pipeline_groups(self):
        groups = self.fetch('/config/pipeline_groups')

        if self.filter_groups:
            return [g for g in groups if any(fg for fg in self.filter_groups if fg in g['name'].lower())]
        else:
            return groups

    def fetch_build_status(self):
        groups = self.get_pipeline_groups()
        result = []

        for group in groups:
            group_name = group['name']

            for p in group['pipelines']:
                pipeline_name = p['name']
                self.logger.info('Found pipeline ' + pipeline_name)

                paused = self.is_paused(pipeline_name)

                if paused:
                    build_status = "Paused"
                else:
                    build_status = self.get_build_result_from_history(pipeline_name)

                result.append({
                    "group": group_name,
                    "pipeline": pipeline_name,
                    "status": build_status,
                    "paused": paused
                })

        return result

    def get_build_status(self):
        self.logger.info("Fetching status from Go Server")
        return self.fetch_build_status()
