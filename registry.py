import urllib.request
import json
import dateutil.parser

REGISTRY_URL = "https://getwilds.org/registry/registry.json"


class WildsRegistry(object):
	"""WildsRegistry

	Examples:
		reg = WildsRegistry()
		reg
		reg.repos
		reg.updated
	"""
	def __init__(self):
		self.load_data()
		self.partition()

	def __repr__(self):
		return (
			f"< {type(self).__name__} >\n"
			f" updated: {self.updated}\n"
			" Count of each badge\n"
			f"  concept: {len(self.concept)}\n"
			f"  experimental: {len(self.experimental)}\n"
			f"  prototype: {len(self.prototype)}\n"
			f"  stable: {len(self.stable)}\n"
			f"  deprecated: {len(self.deprecated)}\n"
		)

	def load_data(self):
		with urllib.request.urlopen(REGISTRY_URL) as url:
			data = json.load(url)
			self.repos = data["repos"]
			self.updated = dateutil.parser.parse(data["updated"]).strftime("%Y-%m-%d")

	def partition(self):
		self.all = [w for w in self.repos if w["badges"]]

		for repo in self.all:
			status_badge = [x for x in repo["badges"] if "Status" in x["alt"]]
			repo['badge_status'] = status_badge[0]["href"].split("#")[-1]

		self.concept = [w for w in self.all if w["badge_status"] == "concept"]
		self.experimental = [w for w in self.all if w["badge_status"] == "experimental"]
		self.prototype = [w for w in self.all if w["badge_status"] == "prototype"]
		self.stable = [w for w in self.all if w["badge_status"] == "stable"]
		self.deprecated = [w for w in self.all if w["badge_status"] == "deprecated"]
