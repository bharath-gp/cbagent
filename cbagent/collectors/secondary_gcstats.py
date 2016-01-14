import requests
import time

from cbagent.collectors import Collector
from logger import logger


class SecondaryGCStats(Collector):
    COLLECTOR = "secondary_gcstats"

    def _get_secondary_gcstats(self):
        server = self.index_node
        uri = "/stats/storage"
        response = self._get_http_content(path=uri, server=server)
        node_count = filter(lambda line: "node_count" in line, response.iter_lines())
        node_count = node_count[0].split('= ')[-1]
        gcstats = {"gc_node_count": node_count}
        return gcstats

    def _get_http_content(self, path, server=None, port=9102):
        server = server or self.master_node
        url = "http://{}:{}{}".format(server, port, path)
        try:
            r = self.session.get(url=url, auth=self.auth)
            if r.status_code in (200, 201, 202):
                return r.content
            else:
                logger.warn("Bad response: {}".format(url))
                return self.retry(path, server, port)
        except requests.ConnectionError:
            logger.warn("Connection error: {}".format(url))
            return self.retry(path, server, port)

    def retry(self, path, server=None, port=9102):
        time.sleep(self.interval)
        for node in self.nodes:
            if self._check_node(node):
                self.master_node = node
                self.nodes = list(self.get_nodes())
                break
        else:
            logger.interrupt("Failed to find at least one node")
        if server not in self.nodes:
            raise RuntimeError("Bad node {}".format(server or ""))
        else:
            return self._get_http_content(path, server, port)

    def sample(self):
        stats = self._get_secondary_gcstats()
        if stats:
            self.update_metric_metadata(stats.keys())
            self.store.append(stats, cluster=self.cluster,
                              collector=self.COLLECTOR)

    def update_metadata(self):
        self.mc.add_cluster()
