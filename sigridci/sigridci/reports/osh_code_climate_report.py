# Copyright Software Improvement Group
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os

from .report import Report


class OpenSourceHealthCodeClimateReport(Report):

    def generate(self, analysisId, feedback, options):
        with open(os.path.abspath(f"{options.outputDir}/osh-feedback.json"), "w", encoding="utf-8") as f:
            findings = list(self.toCodeClimateFindings(feedback))
            json.dump(findings, f, indent=2)

    def toCodeClimateFindings(self, feedback):
        for dependency in feedback["dependencies"]:
            for file in dependency["files"]:
                for vulnerability in dependency["vulnerabilities"]:
                    if vulnerability["severity"] in ["CRITICAL", "HIGH"]:
                        yield {
                            "description" : f"{dependency['name']} - {vulnerability['description']}",
                            "check_name" : "Sigrid Open Source Health",
                            "fingerprint" : f"{dependency['name']}-{dependency['currentVersion']}-{vulnerability['cve']}",
                            "location" : {
                                "path" : file["path"]
                            }
                        }
